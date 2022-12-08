import numpy as np


def read_data(filename: str) -> np.ndarray[int]:
    with open(filename, "r") as f:
        matrix = np.genfromtxt(f, delimiter=1, dtype=int)
    return matrix


def task1(matrix: np.ndarray[int, int]) -> np.ndarray[int, int]:
    visibility_matrix = np.zeros(matrix.shape, dtype=int)

    for rotation in range(0, 4):
        temp_visiblity_matrix = np.copy(np.rot90(matrix, k=rotation))
        maximum = -1 * np.ones((temp_visiblity_matrix.shape[0], 1))

        for ii in range(temp_visiblity_matrix.shape[1]):
            temp = maximum
            maximum = np.maximum(maximum, temp_visiblity_matrix[:, [ii]])
            temp_visiblity_matrix[:, [ii]] =\
                temp_visiblity_matrix[:, [ii]] > temp

        visibility_matrix += np.rot90(temp_visiblity_matrix, k=4-rotation)

    return np.sum(visibility_matrix > 0)


def task2(matrix: np.ndarray[int, int]) -> np.ndarray[int, int]:
    scenic_score_matrix = np.ones(matrix.shape, dtype=int)
    scenic_score_matrix[0:, (0,-1)] = 0
    scenic_score_matrix[(0,-1), 0:] = 0

    for rotation in range(0, 4):
        temp_view_matrix = np.copy(np.rot90(matrix, k=rotation))

        for ii in range(temp_view_matrix.shape[1] - 1):
            temp_view_column = np.zeros((temp_view_matrix.shape[0], 1),
                                        dtype=int)
            maximum = np.zeros((temp_view_matrix.shape[0], 1), dtype=int)

            for jj in range(ii + 1, temp_view_matrix.shape[1]):
                temp_view_column += temp_view_matrix[:, [jj]] >= maximum
                maximum = np.maximum(maximum,
                                     10 * (temp_view_matrix[:, [ii]] <=
                                           temp_view_matrix[:, [jj]]))

            temp_view_matrix[:, [ii]] = temp_view_column

        scenic_score_matrix *= np.rot90(temp_view_matrix, k=4-rotation)

    return np.max(scenic_score_matrix)


if __name__ == "__main__":

    matrix = read_data("input08.txt")

    print("task1:\t", task1(matrix=matrix)) # 1835

    print("task2:\t", task2(matrix=matrix)) # 263670
