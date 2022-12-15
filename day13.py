import functools as ft


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def get_array(input: str):
    left_indices = [i for i, char in enumerate(input) if char == '[']
    right_indices = [i for i, char in enumerate(input) if char == ']']

    if len(left_indices) == 0: 
        return int(input)
    if len(left_indices) == 1 and len(input) == 2:
        return []
    elif len(left_indices) == 1 and len(input) != 2:
        return [int(char) for char in input[1:-1].split(',')]

    left_outer = input[left_indices[0] + 1 : left_indices[1] - 1]
    right_outer = input[right_indices[-2] + 2 : right_indices[-1]]

    left_numbers = [int(char) for char in left_outer.split(',') if char]
    right_numbers = [int(char) for char in right_outer.split(',') if char]

    closed_groups = list()
    open_counter = 0
    close_counter = 0
    tmp = ''
    for char in input[left_indices[1] : right_indices[-2] + 1]:
        if char == '[': open_counter += 1
        elif char == ']': close_counter += 1

        if open_counter == close_counter:
            tmp += char if char != ',' else ''
        else:
            tmp += char if tmp or char != ',' else ''

        if open_counter == close_counter and len(tmp) != 0:
            if char == ',' or char == ']':
                closed_groups.append(tmp)
                tmp = ''

    return [*left_numbers,
            *[get_array(group) for group in closed_groups],
            *right_numbers]


def preprocess(file_content: str) -> str:
    groups_raw = [group.splitlines() for group in file_content.split('\n\n')]
    groups = [[get_array(part) for part in group] for group in groups_raw]
    return groups


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(preprocessed_input)
        return output

    return wrapper


def compare(left: list | int, right: list | int) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    elif isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]

    i = -1
    for i, (l, r) in enumerate(zip(left, right)):
        result = compare(l, r)
        if result != None:
            return result

    if len(left) == len(right):
        return None
    if len(left) == (i + 1):
        return True
    else :
        return False


@process
def task1(groups: list[list | int]) -> int:
    indices = [i for i, group in enumerate(groups, 1) if compare(*group)]
    return sum(indices)


@process
def task2(groups: list[list | int]) -> int:
    flattened_groups = [part for group in groups for part in group]
    flattened_groups.append([[2]])
    flattened_groups.append([[6]])
    sorted_parts = sorted(flattened_groups,
                          key=ft.cmp_to_key(lambda x, y: compare(x, y)*-2+1))
    return (sorted_parts.index([[2]]) + 1) * (sorted_parts.index([[6]]) + 1)


if __name__ == "__main__":

    file_content = read_data("input13.txt")

    print("task1:\t", task1(file_content)) # 5882

    print("task2:\t", task2(file_content)) # 24948
