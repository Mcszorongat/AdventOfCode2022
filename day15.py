import functools as ft
import multiprocessing as mp


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def distance_from_row(row: int, p: tuple[int, int]) -> int:
    return abs(row - p[1])


def preprocess(file_content: str) -> list[tuple[tuple, tuple, int]]:
    replaces = [['Sensor at x=', ''],
                [', y=', ','],
                [': closest beacon is at x=', ' ']]

    lines = file_content.replace(replaces[0][0], replaces[0][1]).\
                         replace(replaces[1][0], replaces[1][1]).\
                         replace(replaces[2][0], replaces[2][1]).\
                         splitlines()\

    raw_pairs = [line.split(' ') for line in lines]
    processed_pairs = [[tuple([int(x) for x in part.split(',')]) for part in pair]
            for pair in raw_pairs]
    return [[pair[0], pair[1], distance(pair[0], pair[1])] for pair in processed_pairs]


def postprocess(task_output: str) -> str:
    return task_output


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(preprocessed_input)
        postprocessed_output = postprocess(output)
        return postprocessed_output

    return wrapper


@process
def task1(S_B_pairs: list[tuple[tuple, tuple, int]]) -> int:
    line_y = 2_000_000

    relevant_rows = [(S, B, distance_from_row(line_y, S), R)
                     for S, B, R in S_B_pairs
                     if distance_from_row(line_y, S) <= R]

    widths = set([x for S, _, D, R in relevant_rows
                  for x in range(S[0] - (R - D), S[0] + (R - D) + 1)])
    bacons_in_row = set([x for _, (x, y), _, _
                         in relevant_rows if y == line_y])

    return len(widths - bacons_in_row)


def sum_adjacent_ranges(ranges: list[tuple[int, int]]) -> tuple[int, int] | int:
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    start = sorted_ranges[0][0]
    stop = sorted_ranges[0][1]
    if start > 0:
        return 0
    for sorted_range in sorted_ranges[1:]:
        if stop < sorted_range[0]:
            return stop
        stop = max(stop, sorted_range[1])
    return (start, stop)


def search_space(S_B_pairs, lines, limit_x):
    start = lines[0]
    work_load = len(lines)
    for line_y in lines:
        relevant_rows = [(S, B, distance_from_row(line_y, S), R)
                        for S, B, R in S_B_pairs
                        if distance_from_row(line_y, S) <= R]

        limits = [(S[0] - (R - D), S[0] + (R - D))
                  for S, _, D, R in relevant_rows]
        limited_limits = [(min(limit_x, max(0, lower)),
                           min(limit_x, max(0, upper)))
                          for lower, upper in limits]

        sum_of_ranges = sum_adjacent_ranges(limited_limits)
        if isinstance(sum_of_ranges, int):
            return (sum_of_ranges, line_y)
        elif sum_of_ranges[1] < limit_x:
            return (limit_x, line_y)

        if (line_y - start) % ((work_load)//100) == 0:
            print(f"{(line_y - start) // ((work_load-1)//100)}%")
    return None


@process
def task2(S_B_pairs: list[tuple[tuple, tuple, int]]) -> int:
    limit = 4_000_000
    get_input = lambda x, y: (S_B_pairs, range(x, y + 1), limit)

    cores = 12
    inputs = [get_input(i * (limit // cores), (i + 1) * (limit // cores))
              for i in range(0, cores)]

    with mp.Pool(processes=cores) as pool:
        results = pool.starmap(search_space, [input for input in inputs])

    x, y = [result for result in results if result != None][0]

    return x * 4_000_000 + y


if __name__ == "__main__":

    file_content = read_data("input15.txt")

    print("task1:\t", task1(file_content)) # 5809294

    print("task2:\t", task2(file_content)) # 10693731308112
