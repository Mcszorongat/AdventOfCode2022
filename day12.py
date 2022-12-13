import numpy as np
import heapq as hq
import functools as ft


def read_data(filename: str) -> str:
    with open(filename, "r") as f:
        file_content = f.read()
    return file_content


def preprocess(file_content: str) -> tuple[np.ndarray[int, int],
                                     tuple[int], tuple[int]]:
    lines = file_content.splitlines()
    height_map = np.array([[ord(char) for char in line] for line in lines],
                          dtype=int)
    start = list(zip(*np.where(height_map == ord('S'))))[0]
    end = list(zip(*np.where(height_map == ord('E'))))[0]
    height_map[start] = ord('a')
    height_map[end] = height_map.max()

    return height_map, start, end


def process(func):
    @ft.wraps(func)
    def wrapper(*args, **kwargs):
        preprocessed_input = preprocess(*args, **kwargs)
        output = func(*preprocessed_input)
        return output

    return wrapper


def get_neighbour_coords(node: tuple[int, int], limits: tuple[int, int]):
    xs = set(abs(x) for x in [node[0] - 1, node[0] + 1] if x < limits[0])
    ys = set(abs(y) for y in [node[1] - 1, node[1] + 1] if y < limits[1])
    horizontal_neighbours = [(x, node[1]) for x in xs]
    vertical_neighbours = [(node[0], y) for y in ys]

    return horizontal_neighbours + vertical_neighbours


def update_cost_map(cost_map: np.ndarray[int, int],
                    height_map: np.ndarray[int, int]) -> None:
    visited_nodes = set()
    start = list(zip(*np.where(cost_map == cost_map.min())))[0]
    heap = [(cost_map[start], start)]

    while len(heap):
        distance, current_node = hq.heappop(heap)

        if current_node in visited_nodes:
            continue
        visited_nodes.add(current_node)

        for neighbour in get_neighbour_coords(current_node, height_map.shape):
            if (height_map[neighbour] - height_map[current_node] > 1):
                continue
            if distance + 1 < cost_map[neighbour]:
                cost_map[neighbour] = distance + 1
            hq.heappush(heap, (distance + 1, neighbour))


@process
def task1(height_map: np.ndarray[int, int],
          start: tuple[int], end: tuple[int]) -> int:

    cost_map = np.infty * np.ones_like(height_map)
    cost_map[start] = 0

    update_cost_map(cost_map, height_map)

    return cost_map[end]


@process
def task2(height_map: np.ndarray[int, int], _, end: tuple[int]) -> int:

    cost_map = np.infty * np.ones_like(-height_map)
    cost_map[end] = 0
    
    update_cost_map(cost_map, -height_map)

    return min(cost_map[-height_map == (-height_map).max()])


if __name__ == "__main__":

    file_content = read_data("input12.txt")

    print("task1:\t", task1(file_content)) # 534

    print("task2:\t", task2(file_content)) # 525
