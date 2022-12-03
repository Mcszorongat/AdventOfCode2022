def read_data(filename: str) -> list[str]:
    with open(filename) as f:
        rucksack_contents = f.read().splitlines()
    return rucksack_contents


def convert(lines: list[str]) -> list[int]:
    return [bytes(line.encode()) for line in lines]


def transform(int_lists: list[int]) -> list[int]:
    return [[number - ord('a') + 1 if number > ord('Z') else
             number - 2*ord('A') + ord('Z') + 2
             for number in int_list]
            for int_list in int_lists]


def task1(rucksack_contents: list[str]) -> int:
    encoded_lists = transform(convert(rucksack_contents))
    priority_list = [
        set(cont[0:len(cont)//2]).intersection(cont[len(cont)//2:]).pop()
        for cont in encoded_lists
    ]

    return sum(priority_list)


def task2(rucksack_contents: list[str]) -> int:
    encoded_lists = transform(convert(rucksack_contents))
    priority_list = [set(g[0]).intersection(g[1]).intersection(g[2]).pop()
                     for g in zip(*[iter(encoded_lists)] * 3)]

    return sum(priority_list)


if __name__ == "__main__":

    rucksack_contents = read_data("input03.txt")

    print("task1: ", task1(rucksack_contents=rucksack_contents)) # 8039

    print("task2: ", task2(rucksack_contents=rucksack_contents)) # 2510
