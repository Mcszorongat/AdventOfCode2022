import re
import functools as ft


def read_data(filename: str) -> tuple[str, str]:
    with open(filename, "r") as f:
        file_content = f.read()
    starting_drawing, procedures = file_content.split('\n\n')
    return starting_drawing, procedures


def preprocess(drawing: str, procedures: str) -> tuple[list[str], list[int]]:

    drawing_list = [line[1::4] for line in drawing.splitlines()]

    drawing_list = [''.join(line).replace(' ', '')
                        for line in zip(*reversed(drawing_list))]

    procedures = [list(map(int, re.findall(r'\d+', line)))
                      for line in procedures.splitlines()]

    return drawing_list, procedures


def postprocess(drawing_list: list[str]) -> str:
    return ''.join([line[-1] for line in drawing_list if len(line) > 0])


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(*preprocessed_input)
        postprocessed_output = postprocess(output)
        return postprocessed_output

    return wrapper


def execute_procedure(drawing, procedure, one_by_one=True) -> None:
    s = -1 if one_by_one else 1
    drawing[procedure[2] - 1] += drawing[procedure[1] - 1][-procedure[0]:][::s]
    drawing[procedure[1] - 1] = drawing[procedure[1] - 1][:-procedure[0]]



@process
def task1(drawing: list[str], procedures: list[int]) -> list[str]:
    for procedure in procedures:
        execute_procedure(drawing, procedure)

    return drawing


@process
def task2(drawing: list[str], procedures: list[int]) -> list[str]:
    for procedure in procedures:
        execute_procedure(drawing, procedure, one_by_one=False)

    return drawing


if __name__ == "__main__":

    drawing, procedures = read_data("input05.txt")

    print("task1:\t", task1(drawing, procedures)) # MQTPGLLDN

    print("task2:\t", task2(drawing, procedures)) # LVZPSTTCZ
