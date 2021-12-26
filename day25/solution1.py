from pathlib import Path
from itertools import count
from copy import deepcopy

data = Path(__file__).with_name("data.txt").read_text().splitlines()
area = [list(line) for line in data]
rows = len(area)
cols = len(area[0])

for step in count(1):
    anyone_moved = False
    new_area = deepcopy(area)
    for r, row in enumerate(area):
        for c, val in enumerate(row):
            new_c = (c + 1) % cols
            if val == ">" and row[new_c] == ".":
                anyone_moved = True
                new_area[r][c] = "."
                new_area[r][new_c] = ">"
    area = new_area
    new_area = deepcopy(area)
    for r, row in enumerate(area):
        for c, val in enumerate(row):
            new_r = (r + 1) % rows
            if val == "v" and area[new_r][c] == ".":
                anyone_moved = True
                new_area[r][c] = "."
                new_area[new_r][c] = "v"
    area = new_area
    if not anyone_moved:
        break

print("Solution:", step)
