import numpy as np
import functools as ft


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def preprocess(file_content: str) -> list[np.ndarray[int, int]]:
    v = np.array([1, 0]) # Direction vector.
    dirs = {'R': 0, 'U': 1, 'L': 2, 'D': 3} # Direction map.
    rot_mx = np.matrix([[0, 1], [-1, 0]]) # Positive rotation matrix.

    # Split the lines to get separate direction and repetition.
    raw_instructions = [line.split(' ') for line in file_content.splitlines()]
    # Repeat the coded value of the direction 'repetition' times.
    step_by_step_instructions = [dirs[direction]
                                 for direction, repetition in raw_instructions
                                 for _ in range(int(repetition))]
    # For every coded direction value calculate the direction vector.
    moves = [
        np.array(v@rot_mx**direction, dtype=np.int8).flatten(order='C')
        for direction in step_by_step_instructions
    ]

    return moves


def postprocess(tail_position_list: set[tuple[int, int]]) -> int:
    return len(tail_position_list)


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(preprocessed_input)
        postprocessed_output = postprocess(output)
        return postprocessed_output

    return wrapper


def move_point_towards_point(p1: np.ndarray[int, int],
                             p2: np.ndarray[int, int]) -> bool:
    if np.linalg.norm(p1 - p2) > 1.5:
        p1 += np.sign(p2 - p1)
        return True
    else:
        return False


def move_points(points: list[np.ndarray[int, int]],
                moves: list[np.ndarray[int, int]]) -> set[tuple[int, int]]:
    tail_point_set = set(tuple(points[-1]))

    for i in range(len(moves)):
        points[0] += moves[i]
        for j in range(1, len(points)):
            if not move_point_towards_point(points[j], points[j - 1]):
                break
            if j == len(points) - 1:
                tail_point_set.add(tuple(points[-1]))

    return tail_point_set


@process
def task1(moves: list[np.ndarray[int, int]]) -> int:
    return move_points(np.zeros((2, 2)), moves)


@process
def task2(moves: list[np.ndarray[int, int]]) -> int:
    return move_points(np.zeros((10, 2)), moves)


if __name__ == "__main__":

    file_content = read_data("input09.txt")

    print("task1:\t", task1(file_content=file_content)) # 6332

    print("task2:\t", task2(file_content=file_content)) # 2511
