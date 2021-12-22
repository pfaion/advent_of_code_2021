from math import prod
from pathlib import Path
from typing import Iterable

# load
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse
steps = []
for line in data:
    mode, tmp = line.split(" ")
    low, high = zip(*(map(int, ax.split("=")[1].split("..")) for ax in tmp.split(",")))
    steps.append((mode, low, high))


# model 1D range interactions (subtraction, intersection)
Point1D = int
Cube1D = tuple[Point1D, Point1D]


def subtract1D(
    low0: Point1D, high0: Point1D, low1: Point1D, high1: Point1D
) -> list[Cube1D]:
    if high1 < low0:
        #     000
        # 111
        return [(low0, high0)]
    elif high0 < low1:
        # 000
        #     111
        return [(low0, high0)]
    elif low1 <= low0 and high0 <= high1:
        #   0000
        # 11111111
        return []
    elif low0 < low1 and high1 < high0:
        # 000000
        #   11
        return [(low0, low1 - 1), (high1 + 1, high0)]
    elif low1 <= low0 and high1 < high0:
        #   0000
        # 1111
        return [(high1 + 1, high0)]
    elif low0 < low1 and high0 <= high1:
        # 0000
        #   1111
        return [(low0, low1 - 1)]
    assert False


def intersect1D(
    low0: Point1D, high0: Point1D, low1: Point1D, high1: Point1D
) -> list[Cube1D]:
    if high1 < low0:
        #     000
        # 111
        return []
    elif high0 < low1:
        # 000
        #     111
        return []
    else:
        return [(max(low0, low1), min(high0, high1))]


# model 3D cuboid subtraction
Point = tuple[int, int, int]
Cube = tuple[Point, Point]


def subtract(low0: Point, high0: Point, low1: Point, high1: Point) -> Iterable[Cube]:
    xl0, yl0, zl0 = low0
    xh0, yh0, zh0 = high0
    xl1, yl1, zl1 = low1
    xh1, yh1, zh1 = high1
    for xlow, xhigh in subtract1D(xl0, xh0, xl1, xh1):
        yield ((xlow, yl0, zl0), (xhigh, yh0, zh0))
    for xlow, xhigh in intersect1D(xl1, xh1, xl0, xh0):
        for ylow, yhigh in subtract1D(yl0, yh0, yl1, yh1):
            yield ((xlow, ylow, zl0), (xhigh, yhigh, zh0))
        for ylow, yhigh in intersect1D(yl1, yh1, yl0, yh0):
            for zlow, zhigh in subtract1D(zl0, zh0, zl1, zh1):
                yield ((xlow, ylow, zlow), (xhigh, yhigh, zhigh))


# actually simulate
on = []
for i, (mode, low, high) in enumerate(steps):
    # subtract cuboid from all existing cuboids (like "off")
    on = [remaining for l, h in on for remaining in subtract(l, h, low, high)]
    # add it again for "on", don't need to account for overlaps now!
    if mode == "on":
        on.append((low, high))
count = sum(prod(h - l + 1 for l, h in zip(low, high)) for low, high in on)
print("Solution:", count)
