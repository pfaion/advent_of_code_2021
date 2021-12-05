import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List

# load data
data_file = Path(__file__).with_name("data.txt")
data_raw = data_file.read_text().splitlines()


# helper function
def interpolate(a: int, b: int) -> Iterator[int]:
    if a < b:
        return range(a, b + 1)
    else:
        return range(a, b - 1, -1)


# data structure
@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def __iter__(self) -> Iterator:
        if self.x1 == self.x2:
            for y in interpolate(self.y1, self.y2):
                yield self.x1, y
        elif self.y1 == self.y2:
            for x in interpolate(self.x1, self.x2):
                yield x, self.y1
        else:
            yield from zip(interpolate(self.x1, self.x2), interpolate(self.y1, self.y2))


# parse data
lines: List[Line] = []
for entry in data_raw:
    if match := re.match(r"(\d+),(\d+) -> (\d+),(\d+)", entry):
        args = map(int, match.groups())
        lines.append(Line(*args))

# accumulate lines
sparse_map = Counter()
for line in lines:
    for point in line:
        sparse_map[point] += 1


# count points with overlaps
n_overlaps = sum(1 for _point, count in sparse_map.items() if count >= 2)

print("Solution:", n_overlaps)
