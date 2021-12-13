from itertools import product
from pathlib import Path

# load data
data = Path(__file__).with_name("data.txt").read_text()
points_raw, folds_raw = data.split("\n\n")

# parse data
points = {tuple(map(int, line.split(","))) for line in points_raw.splitlines()}
folds = [(line[11], int(line.split("=")[1])) for line in folds_raw.splitlines()]

# first folds
axis, fold = folds[0]
if axis == "y":
    points = {(x, y) if y <= fold else (x, 2 * fold - y) for x, y in points}
else:
    points = {(x, y) if x <= fold else (2 * fold - x, y) for x, y in points}

print("Solution:", len(points))
