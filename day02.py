import numpy as np


def read_data(filename: str) -> list[str]:
    with open(filename) as f:
        matches = [match.split() for match in f.read().splitlines()]
    return matches


def evaluate_rounds(matches):
    encoding_dict = {'A': 1, 'B': 2, 'C': 3}
    result_array = [3, 0, 6]

    encoded_matches = np.array([[encoding_dict[x[0]], encoding_dict[x[1]]]
                                for x in matches])
    outcomes = encoded_matches[:, 0] - encoded_matches[:, 1]
    score = [result_array[np.mod(outcome, 3)] for outcome in outcomes]

    return sum(encoded_matches[:, 1] + score)


def task1(matches: list[str]) -> int:
    assumed_matches = [[match[0], chr(ord(match[1])-23)] for match in matches]

    return evaluate_rounds(assumed_matches)


def task2(matches: list[str]) -> int:
    action_dict = {'X': -1, 'Y': 0, 'Z': -2}
    picks_array = ['A', 'B', 'C']
    matches = [
        [match[0],
        picks_array[picks_array.index(match[0]) + action_dict[match[1]]]]
        for match in matches
    ]

    return evaluate_rounds(matches)


if __name__ == "__main__":
    
    matches = read_data("input02.txt")

    print("task1:\t", task1(matches=matches)) # 12772

    print("task2:\t", task2(matches=matches)) # 11618
