import heapq
import numpy as np
import functools as ft
from typing import Callable

class Monkey():
    def __init__(self, items: list[int], operation: Callable[[int], int],
                 divisor: int, pass_index: int, fail_index: int) -> None:
        self.items: list[int] = items
        self.operation: Callable[[int], int] = lambda x: operation(x)
        self.divisor = divisor
        self.test: Callable[[int], bool] = lambda x: x % self.divisor == 0
        self.pass_index: int = pass_index
        self.fail_index: int = fail_index

    def __repr__(self) -> str:
        return (f"{self.items} | % {self.divisor} == 0 | " +
                f"[{self.pass_index} or {self.fail_index}]")

    def do(self, divisor=3) -> tuple[int, int] | None:
        if len(self.items) == 0:
            return None

        item, *self.items = self.items
        item = self.operation(item) // divisor

        index = self.pass_index if self.test(item) else self.fail_index

        return (index, item)


    @staticmethod
    def generate_monkey(input: str):
        rows = input.splitlines()
        row1 = "  Starting items: "
        row2 = "  Operation: new = "
        row3 = "  Test: divisible by "
        row4 = "    If true: throw to monkey "
        row5 = "    If false: throw to monkey "

        op_dict = {'+': lambda x, y: x + y, '*': lambda x, y: x * y}
        choose_val = lambda a, b: a if b == 'old' else int(b)

        items = [int(x)for x in rows[1][len(row1):].split(", ")]

        op_parts = rows[2][len(row2):].split(' ')
        operation = lambda x: op_dict[op_parts[1]](
            np.uint64(choose_val(x, op_parts[0])),
            np.uint64(choose_val(x, op_parts[2]))
        )

        divisor = int(rows[3][len(row3):])

        pass_index = int(rows[4][len(row4):])
        fail_index = int(rows[5][len(row5):])

        return Monkey(items, operation, divisor, pass_index, fail_index)


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def preprocess(file_content: str) -> str:
    sections = file_content.split('\n\n')
    monkeys = [Monkey.generate_monkey(section) for section in sections]
    return monkeys


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(preprocessed_input)
        return output

    return wrapper


@process
def task1(monkeys: list[Monkey]) -> int:
    inspections = np.zeros_like(monkeys, dtype=int)

    for _ in range(20):
        for i, monkey in enumerate(monkeys):
            for _ in monkey.items:
                result = monkey.do()
                monkeys[result[0]].items.append(result[1])
                inspections[i] += 1

    return np.prod(heapq.nlargest(2, inspections))


@process
def task2(monkeys: list[Monkey]) -> int:
    mod = np.lcm.reduce([monkey.divisor for monkey in monkeys])
    inspections = np.zeros_like(monkeys, dtype=np.uint64)

    for _ in range(10000):
        for i, monkey in enumerate(monkeys):
            for _ in monkey.items:
                result = monkey.do(1)
                monkeys[result[0]].items.append(result[1] % mod)
                inspections[i] += 1

    return np.prod(heapq.nlargest(2, inspections))


if __name__ == "__main__":

    file_content = read_data("input11.txt")

    print("task1:\t", task1(file_content)) # 54054

    print("task2:\t", task2(file_content)) # 14314925001
