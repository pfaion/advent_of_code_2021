import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List

# load data
data_file = Path(__file__).with_name("data.txt")
data_raw = data_file.read_text().splitlines()


# data structure
@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def is_cardinal(self) -> bool:
        return (self.x1 == self.x2) or (self.y1 == self.y2)

    def __iter__(self) -> Iterator:
        if not self.is_cardinal():
            raise NotImplementedError()

        if self.x1 == self.x2:
            y1, y2 = sorted((self.y1, self.y2))
            for y in range(y1, y2 + 1):
                yield self.x1, y
        elif self.y1 == self.y2:
            x1, x2 = sorted((self.x1, self.x2))
            for x in range(x1, x2 + 1):
                yield x, self.y1


# parse data
lines: List[Line] = []
for entry in data_raw:
    if match := re.match(r"(\d+),(\d+) -> (\d+),(\d+)", entry):
        args = map(int, match.groups())
        lines.append(Line(*args))

# accumulate lines
sparse_map = Counter()
for line in lines:
    if not line.is_cardinal():
        continue
    for point in line:
        sparse_map[point] += 1

# count points with overlaps
n_overlaps = sum(1 for _point, count in sparse_map.items() if count >= 2)

print("Solution:", n_overlaps)
