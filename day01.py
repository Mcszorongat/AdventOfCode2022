def read_data(filename: str) -> list[int]:
    with open(filename, "r") as f:
        calory_arrays = f.read().split("\n\n")
    calories = [sum([int(calory) for calory in array.split("\n")])
             for array in calory_arrays]
    return sorted(calories)


def task1(sorted_calories: list[int]) -> int:
    return sorted_calories[-1]


def task2(sorted_calories: list[int]) -> int:
    return sum(sorted_calories[-3:])


if __name__ == "__main__":

    sorted_calories = read_data("input01.txt")

    print("task1:\t", task1(sorted_calories=sorted_calories)) # 69693

    print("task2:\t", task2(sorted_calories=sorted_calories)) # 200945
