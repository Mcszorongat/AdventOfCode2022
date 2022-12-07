from __future__ import annotations
import functools as ft
import itertools as it


class Content:
    def __init__(self, name):
        self.name = name


class File(Content):
    def __init__(self, name: str, size: int ):
        Content.__init__(self, name)
        self.size = size

    def draw_tree(self, level):
        return '  '*level + '- ' + self.name + f' (file, size={self.size})'


class Directory(Content):
    def __init__(self, name: str):
        Content.__init__(self, name)
        self.__separator = '/'
        self.files: dict[str, File] = dict()
        self.directories: dict[str, Directory] = dict()


    def draw_tree(self, level=0) -> str:
        tree = ['  '*level + '- ' + self.name + ' (dir)',
                *[file.draw_tree(level + 1) for file in self.files.values()],
                *[directory.draw_tree(level + 1)
                  for directory in self.directories.values()]]
        return '\n'.join(tree)

    def add_content(self, content: Content) -> None:
        if isinstance(content, File):
            self.files.update({content.name: content})
        elif isinstance(content, Directory):
            self.directories.update({content.name: content})

    def get_size(self) -> int:
        directory_sizes = [directory.get_size()
                           for directory in self.directories.values()]
        file_sizes = [file.size for file in self.files.values()]
        return sum(directory_sizes) + sum(file_sizes)

    def get_sub_directory(self, relative_path: str) -> Directory:
        first_part, *rest = relative_path.split(self.__separator)
        sub_directory = self.directories.get(first_part)

        if sub_directory and len(rest):
            return sub_directory.get_sub_directory(self.__separator.join(rest))
        elif sub_directory and not len(rest):
            return sub_directory
        elif not sub_directory:
            self.directories.update({first_part: Directory(first_part)})
            return self.get_sub_directory(relative_path)

    def get_directories_with_sizes(self) -> list[(str, int)]:
        own = [(self.name, self.get_size())]
        if len(self.directories.values()):
            children = list(it.chain(*[x.get_directories_with_sizes()
                                    for x in self.directories.values()]))
            own.extend(children)
        return own


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read().splitlines()
    return file_content


def preprocess(file_content: str) -> Directory:
    root = Directory('/')
    directories = []
    current_directory = root

    for line in file_content:
        if line.endswith(r'ls'): continue
        elif line.startswith(r'$ cd'):
            directory = line[5:]
            if directory == r'/':
                directories = []
                current_directory = root
            elif directory == r'..':
                directories.pop()
                if len(directories):
                    current_directory = root.get_sub_directory('/'.join(directories))
                else:
                    current_directory = root
            else:
                directories.append(directory)
                current_directory = root.get_sub_directory('/'.join(directories))
        else:
            if line.startswith('dir'):
                current_directory.add_content(Directory(line[4:]))
            else:
                size, name = line.split(' ')
                current_directory.add_content(File(name, int(size)))
    return root


def postprocess(task_output: str) -> str:
    return task_output


def process():
    def process(func):
        @ft.wraps(func)
        def wrapper(*args, **kwargs):
            preprocessed_input = preprocess(*args, **kwargs)
            output = func(preprocessed_input)
            postprocessed_output = postprocess(output)
            return postprocessed_output

        return wrapper

    return process


@process()
def task1(root: Directory) -> int:
    dirs_with_sizes = root.get_directories_with_sizes()
    fitting_sizes = [size for _, size in dirs_with_sizes if size < 100000]

    return sum(fitting_sizes)


@process()
def task2(root: Directory) -> int:
    dirs_with_sizes = root.get_directories_with_sizes()
    free_space = 70000000 - dirs_with_sizes[0][1]
    needed_space = 30000000 - free_space
    sizes = [x[1] for x in dirs_with_sizes]
    over_required = list(filter(lambda x: x > needed_space, sizes))

    return min(over_required)


if __name__ == "__main__":

    file_content = read_data("input07.txt")

    print("task1:\t", task1(file_content=file_content)) # 1449447

    print("task2:\t", task2(file_content=file_content)) # 8679207
