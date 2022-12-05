from functools import wraps


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def preprocess(file_content: str) -> list[list[range]]:
    return [
        [list(map(int, section.split('-'))) for section in row.split(',')]
        for row in  file_content.splitlines()
    ]


def postprocess(task_output: list[int]) -> int:
    return sum(task_output)


def process(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(preprocessed_input)
        postprocessed_output = postprocess(output)
        return postprocessed_output

    return wrapper


@process
def task1(file_content: list[list[int]]) -> list[int]:
    contain_list = [((s1[0] >= s2[0] and s1[1] <= s2[1]) or
                     (s1[0] <= s2[0] and s1[1] >= s2[1])) * 1
                    for s1, s2 in file_content]
    return contain_list


@process
def task2(file_content: list[list[int]]) -> list[int]:
    contain_list = [(s1[0] <= s2[1] and s1[1] >= s2[0]) * 1
                    for s1, s2 in file_content]
    return contain_list


if __name__ == "__main__":

    file_content = read_data("input04.txt")

    print("task1:\t", task1(file_content=file_content)) # 459

    print("task2:\t", task2(file_content=file_content)) # 779
