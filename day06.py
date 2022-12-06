import collections as col


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def find_unique_sequence_index(source: str, sequence_length: int) -> int:
    sequence = col.deque(maxlen=sequence_length)
    sequence.extend(source[0:sequence_length - 1])
    for i, char in enumerate(file_content[sequence_length - 1:]):
        sequence.append(char)
        if len(set(sequence)) == sequence_length:
            return i + sequence_length
    return 0


def task1(file_content: str) -> int:
    return find_unique_sequence_index(file_content, 4)


def task2(file_content: str) -> str:
    return find_unique_sequence_index(file_content, 14)


if __name__ == "__main__":

    file_content = read_data("input06.txt")

    print("task1:\t", task1(file_content=file_content)) # 1920

    print("task2:\t", task2(file_content=file_content)) # 2334
