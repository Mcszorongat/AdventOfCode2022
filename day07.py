from __future__ import annotations
import functools as ft
import itertools as it


class Item:
    def __init__(self, name: str, size: int, parent: Item):
        self.name: str = name
        self._size: int = size
        self._parent: Item = parent

    def get_size(self) -> int:
        return self._size
    size = property(get_size, None)

    def get_parent(self) -> Item:
        return self._parent if self._parent else self
    parent = property(get_parent, None)

    def get_tree(self, level: int = 0) -> str:
        return f'{"  "*(level)}- {self}'


class File(Item):
    def __init__(self, name: str, size: int, parent: Item):
        Item.__init__(self, name, size, parent)

    def __str__(self):
        return f'{self.name} (file, size={self.size})'


class Directory(Item):
    def __init__(self, name: str, parent: Item = None):
        Item.__init__(self, name, -1, parent)
        self.content: dict[str, Item] = dict()

    def __str__(self) -> str:
        return f'{self.name} (dir)'

    def get_size(self) -> int:
        return sum([content.size for content in self.content.values()])

    size = property(get_size, None)

    def add_content(self, content: Item) -> None:
        self.content.update({content.name: content})

    def get_subdirectory(self, name: str) -> Directory:
        if (name == '.'):
            return self
        else:
            subdirectory = self.content.get(name)
            if not subdirectory:
                self.add_content(subdirectory := Directory(name, self))
        return subdirectory

    def get_tree(self, level:int=0) -> str:
        contents = list(self.content.values())
        return '\n'.join([f'{"  "*level}- {self}',
                *[content.get_tree(level + 1) for content in contents]])


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read().splitlines()
    return file_content


def preprocess(file_content: str) -> Directory:
    root = Directory('/')
    current_directory = root

    for line in file_content:
        if line.endswith(r'ls'):
            continue
        elif line.startswith(r'$ cd '):
            destination = line[5:]
            if (destination == r'/'):
                current_directory = root
            elif (destination == r'..'):
                current_directory = current_directory.parent
            else:
                current_directory = current_directory.get_subdirectory(
                    destination
                )
        else:
            if not line.startswith('dir'):
                size, *name = line.split(' ')
                current_directory.add_content(File(' '.join(name), int(size),
                                                   current_directory))
    return root


def process():
    def process(func):
        @ft.wraps(func)
        def wrapper(*args, **kwargs):
            preprocessed_input = preprocess(*args, **kwargs)
            output = func(preprocessed_input)
            return output
        return wrapper
    return process


def get_directory_sizes(directory: Directory) -> list[int]:
    own = [directory.size]
    if len(directory.content.values()):
        directories: list[Directory] = list(filter(
            lambda content: isinstance(content, Directory),
            directory.content.values()
        ))
        children = list(it.chain(*[get_directory_sizes(directory)
                                    for directory in directories]))
        own.extend(children)
    return own


@process()
def task1(root: Directory) -> int:
    upper_limit = 100_000
    fitting_sizes = list(filter(lambda size: size < upper_limit,
                                get_directory_sizes(root)))
    return sum(fitting_sizes)


@process()
def task2(root: Directory) -> int:
    total_space = 70_000_000
    required_free_space = 30_000_000
    dir_sizes = get_directory_sizes(root)
    actual_free_space =  total_space - max(dir_sizes)

    return min(list(filter(
        lambda size: size > required_free_space - actual_free_space,
        dir_sizes
    )))


if __name__ == "__main__":

    file_content = read_data("input07.txt")

    print("task1:\t", task1(file_content=file_content)) # 1449447

    print("task2:\t", task2(file_content=file_content)) # 8679207
