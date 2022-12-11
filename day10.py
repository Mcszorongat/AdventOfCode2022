import numpy as np
import functools as ft


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def preprocess(file_content: str) -> list[int]:
    lines = file_content.replace('noop', '0').replace('addx ', '').splitlines()
    instructions = [int(line) for line in lines]
    return instructions


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(preprocessed_input)
        return output

    return wrapper


def sim_accu(instructions: list[int]):
    accumulator = [1]
    for inst in instructions:
        accumulator += [accumulator[-1], accumulator[-1] + inst] \
                       if inst else \
                       [accumulator[-1]]
    return accumulator


@process
def task1(instructions: list[int]) -> int:
    return sum(np.array(range(20, 221, 40)) * sim_accu(instructions)[19::40])


@process
def task2(instructions: list[int]) -> str:
    accumulator = sim_accu(instructions[0:-1])
    shape = np.array([6, len(accumulator) // 6])

    accumulator_array = np.array(accumulator).reshape(*shape)
    index_array = np.array([list(range(0, 40))]).repeat(6, axis=0)
    rows = np.array([' '] * len(accumulator)).reshape(*shape)
    rows[np.abs(index_array - accumulator_array) < 2] = '#'

    return '\n\t'.join([''.join(row) for row in rows])


if __name__ == "__main__":

    file_content = read_data("input10.txt")

    print("task1:\t", task1(file_content=file_content)) # 13060

    print(f"task2:\t{task2(file_content=file_content)}") # FJUBULRZ
