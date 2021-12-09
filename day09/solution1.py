from pathlib import Path
from itertools import product
from typing import Callable, Iterable, Iterator

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse as 2D list of ints
heightmap = [[int(n) for n in line] for line in data]
n_rows = len(heightmap)
n_cols = len(heightmap[0])


def get_neighbors(row: int, col: int) -> list[int]:
    neighbors = []
    if row > 0:
        neighbors.append(heightmap[row - 1][col])
    if row < n_rows - 1:
        neighbors.append(heightmap[row + 1][col])
    if col > 0:
        neighbors.append(heightmap[row][col - 1])
    if col < n_cols - 1:
        neighbors.append(heightmap[row][col + 1])
    return neighbors


def is_low_point(point: int, neighbors: list[int]) -> bool:
    return all(point < neighbor for neighbor in neighbors)


coordinates = product(range(n_rows), range(n_cols))
low_points = (
    point
    for row, col in coordinates
    if is_low_point(point := heightmap[row][col], get_neighbors(row, col))
)
risk_levels = (point + 1 for point in low_points)

print("Solution:", sum(risk_levels))
