import math
from itertools import chain, product
from pathlib import Path
from typing import Iterator, Sequence

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse as 2D list of ints
heightmap = [[int(n) for n in line] for line in data]
n_rows = len(heightmap)
n_cols = len(heightmap[0])

Point = tuple[int, int]


def get_height(point: Point) -> int:
    row, col = point
    return heightmap[row][col]


def get_neighbors(point: Point) -> Iterator[Point]:
    row, col = point
    if row > 0:
        yield (row - 1, col)
    if row < n_rows - 1:
        yield (row + 1, col)
    if col > 0:
        yield (row, col - 1)
    if col < n_cols - 1:
        yield (row, col + 1)


def is_low_point(point: Point) -> bool:
    height = get_height(point)
    return all(height < get_height(neighbor) for neighbor in get_neighbors(point))


flatten = chain.from_iterable


def get_basein(start: Point) -> Sequence[int]:
    basein = {start}
    visited = set()
    while basein != visited:
        unvisited = basein - visited
        all_neighbors = set(flatten(map(get_neighbors, unvisited)))
        basein |= {neighbor for neighbor in all_neighbors if get_height(neighbor) < 9}
        visited |= unvisited
    return basein


coordinates = product(range(n_rows), range(n_cols))
low_point_coordinates = filter(is_low_point, coordinates)
low_point_baseins = map(get_basein, low_point_coordinates)
basein_lengths = map(len, low_point_baseins)
result = math.prod(sorted(basein_lengths)[-3:])

print("Solution:", result)
