from __future__ import annotations
import functools as ft
import itertools as it


class Item:
    def __init__(self, name: str, size: int, parent: Item):
        self.name: str = name
        self._size: int = size
        self._parent: Item = parent

    def __lt__(self, other: Item):
        return self.name < other.name

    def get_size(self) -> int:
        return self._size
    def set_size(self, value: int) -> None:
        self._size = value
    size = property(get_size, set_size)

    def get_parent(self) -> Item:
        return self._parent if self._parent else self
    def set_parent(self, value: Item) -> None:
        self._parent = value
    parent = property(get_parent, set_parent)

    def get_tree(self, level: int = 0) -> str:
        return f'{"  "*(level)}- {self}'


class File(Item):
    def __init__(self, name: str, size: int, parent: Item):
        Item.__init__(self, name, size, parent)

    def __str__(self):
        return f'{self.name} (file, size={self.size})'


class Directory(Item):
    def __init__(self, name: str, parent: Item):
        Item.__init__(self, name, -1, parent)
        self.__separator = '/'
        self._content: dict[str, Item] = dict()

        self.files: dict[str, File] = dict()
        self.directories: dict[str, Directory] = dict()

    def __str__(self) -> str:
        return f'{self.name} (dir)'

    def get_size(self) -> int:
        content_sizes = [content.size for content in self._content.values()]
        return sum(content_sizes)

    def set_size(self) -> None:
        pass

    size = property(get_size, set_size)

    def add_content(self, content: Item) -> Item:
        self._content.update({content.name: content})
        return content

    def get_subdirectory(self, name: str) -> Directory:
        if (name == '.'):
            return self
        else:
            subdirectory = self._content.get(name)
            if not subdirectory:
                self.add_content(subdirectory := Directory(name, self))
        return subdirectory

    # def get_subdirectory_by_path(self, relative_path: str) -> Directory:
    #     name, *rest = relative_path.split(self.__separator)
    #     subdirectory = self.get_subdirectory(name)

    #     if len(rest):
    #         return subdirectory.get_subdirectory_by_path(self.__separator.join(rest))
    #     else:
    #         return subdirectory

    def get_tree(self, level:int=0) -> str:
        contents = list(self._content.values())
        # contents.sort()
        tree = [f'{"  "*level}- {self}',
                *[content.get_tree(level + 1) for content in contents]]
        return '\n'.join(tree)


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read().splitlines()
    return file_content


def preprocess(file_content: str) -> Directory:
    root = Directory('/', None)
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
                size, name = line.split(' ')
                current_directory.add_content(File(name, int(size),
                                                   current_directory))
            else:
                pass
                # current_directory.add_content(Directory(line[4:],
                #                                         current_directory))
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
    if len(directory._content.values()):
        directories: list[Directory] = list(filter(
            lambda content: isinstance(content, Directory),
            directory._content.values()
        ))
        children = list(it.chain(*[get_directory_sizes(directory)
                                    for directory in directories]))
        own.extend(children)

    return own


@process()
def task1(root: Directory) -> int:
    upper_limit = 100000
    fitting_sizes = list(filter(lambda size: size < upper_limit,
                                get_directory_sizes(root)))

    return sum(fitting_sizes)


@process()
def task2(root: Directory) -> int:
    total_space = 70000000
    required_free_space = 30000000
    dir_sizes = get_directory_sizes(root)
    actual_free_space =  total_space - max(dir_sizes)
    minimum_space_to_free = required_free_space - actual_free_space
    fitting_sizes = list(filter(lambda size: size > minimum_space_to_free,
                                dir_sizes))

    return min(fitting_sizes)


if __name__ == "__main__":

    file_content = read_data("input07.txt")

    print("task1:\t", task1(file_content=file_content)) # 1449447

    print("task2:\t", task2(file_content=file_content)) # 8679207
