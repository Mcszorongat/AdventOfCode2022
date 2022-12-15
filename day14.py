import numpy as np
import functools as ft


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def endpoints_to_points(p1: np.ndarray[int, int],
                         p2: np.ndarray[int, int]) -> list[np.ndarray]:
    length = np.int32(np.linalg.norm(p2 - p1))
    step_vector = (p2 - p1) // length
    return [p1 + i * step_vector for i in range(length + 1)]


def change_matrix_value(matrix, offset, point, value=1):
    coordinates = point - offset
    if coordinates[0] < 0 or coordinates[1] < 0:
        upper = -min(0, coordinates[0])
        left = -min(0, coordinates[1])
        matrix = np.pad(matrix,
                        pad_width=((upper, 0), (left, 0)),
                        mode='constant',
                        constant_values=0)
        offset -= np.array([upper, left])
        coordinates += np.array([upper, left])

    if (coordinates[0] >= matrix.shape[0] or
            coordinates[1] >= matrix.shape[1]):
        lower = max(0, coordinates[0] - matrix.shape[0] + 1)
        right = max(0, coordinates[1] - matrix.shape[1] + 1)
        matrix = np.pad(matrix,
                        pad_width=((0, lower), (0, right)),
                        mode='constant',
                        constant_values=0)

    matrix[*coordinates] = value

    return matrix, offset


def generate_matrix_from_points(points: np.ndarray) -> np.ndarray:
    matrix = np.matrix([[1]], dtype=np.uint8)
    offset = points[0]

    for point in points[1:]:
        matrix, offset = change_matrix_value(matrix, offset, point)

    matrix, _ = change_matrix_value(matrix, offset, np.array([500, 0]), 2)

    return matrix


def preprocess(file_content: str) -> str:
    lines = file_content.splitlines()
    parsed_lines = [[np.array(corner.split(','), dtype=int)
                     for corner in line.split(' -> ')]
                    for line in lines]
    pairs = [[(group[i], group[i+1]) for i in range(len(group) - 1)]
             for group in parsed_lines]
    points = list(set([tuple([*coord])
                       for pair in pairs
                       for coords in pair
                       for coord in endpoints_to_points(*coords)]))
    return generate_matrix_from_points(np.array(points))


def postprocess(matrix: np.matrix) -> int:
    return len(matrix[matrix == 3])


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(preprocessed_input)
        postprocessed_output = postprocess(output)
        return postprocessed_output

    return wrapper


def fall(matrix: np.matrix, source: np.ndarray[int, int]) -> np.matrix:
    destination = tuple([*source])
    final_position = False

    while not final_position:
        # Fallen off.
        if ((destination[0] < 0 or destination[0] == matrix.shape[0]) or
            (destination[1] < 0 or destination[1] + 1 == matrix.shape[1])):
            destination = np.array([-1, -1])
            final_position = True
        # Straight down.
        elif matrix[destination[0], destination[1] + 1] == 0:
            destination = np.array([destination[0], destination[1] + 1])
        # To the left.
        elif matrix[destination[0] - 1, destination[1] + 1] == 0:
            destination = np.array([destination[0] - 1, destination[1] + 1])
        # To the right.
        elif matrix[destination[0] + 1, destination[1] + 1] == 0:
            destination = np.array([destination[0] + 1, destination[1] + 1])
        # Nowhere to go.
        else:
            final_position = True

    return destination


@process
def task1(matrix: np.matrix[int, int]) -> np.matrix[int, int]:
    source = np.array(list(zip(*np.where(matrix == 2)))[0])
    matrix[*source] = 0

    new_point = fall(matrix, source) # Init.
    while (new_point != np.array([-1, -1])).any():
        matrix[*new_point] = 3
        new_point = fall(matrix, source)

    return matrix


@process
def task2(matrix: np.ndarray[np.ndarray[int]]) -> int:
    source = np.array(list(zip(*np.where(matrix == 2)))[0])
    _, height = matrix.shape
    lower_plus = height - (matrix.shape[0] - source[0])
    upper_plus = (height - 1) - source[0]

    matrix = np.pad(matrix,
                    pad_width=((upper_plus + 2, lower_plus + 2), (0, 0)),
                    mode='constant',
                    constant_values=0)
    matrix = np.pad(matrix, ((0, 0), (0, 1)), 'constant', constant_values=0)
    matrix = np.pad(matrix, ((0, 0), (0, 1)), 'constant', constant_values=1)
    source = np.array(list(zip(*np.where(matrix == 2)))[0]) # Update.
    matrix[*source] = 3 # By the time we stop it would be there.

    new_point = fall(matrix, source) # Init.
    while (new_point != source).any():
        matrix[*new_point] = 3
        new_point = fall(matrix, source)

    return matrix


if __name__ == "__main__":

    file_content = read_data("input14.txt")

    print("task1:\t", task1(file_content=file_content)) # 825

    print("task2:\t", task2(file_content=file_content)) # 26729
