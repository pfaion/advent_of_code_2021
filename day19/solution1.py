from itertools import combinations, product
from math import prod
from pathlib import Path

data = Path(__file__).with_name("data.txt").read_text()

Point = tuple[int, int, int]
Matrix = tuple[tuple[int]]
Transform = tuple[Point, Matrix, Point]

scanner_data: list[set[Point]] = [
    {tuple(map(int, line.split(","))) for line in block.splitlines()[1:]}
    for block in data.split("\n\n")
]


def R(a, b, c) -> Matrix:
    sin = lambda t: {0: 0, 90: 1, 180: 0, 270: -1}[t]
    cos = lambda t: {0: 1, 90: 0, 180: -1, 270: 0}[t]
    return (
        (
            cos(a) * cos(b),
            cos(a) * sin(b) * sin(c) - sin(a) * cos(c),
            cos(a) * sin(b) * cos(c) + sin(a) * sin(c),
        ),
        (
            sin(a) * cos(b),
            sin(a) * sin(b) * sin(c) + cos(a) * cos(c),
            sin(a) * sin(b) * cos(c) - cos(a) * sin(c),
        ),
        (-sin(b), cos(b) * sin(c), cos(b) * cos(c)),
    )


angles = [0, 90, 180, 270]
all_rotations = {R(a, b, c) for a, b, c in product(angles, repeat=3)}


def rotate(point: Point, mat: Matrix) -> Point:
    return tuple(sum(map(prod, zip(point, row))) for row in mat)


def sub(p1: Point, p2: Point) -> Point:
    return tuple(a - b for a, b in zip(p1, p2))


def add(p1: Point, p2: Point) -> Point:
    return tuple(a + b for a, b in zip(p1, p2))


def transform(point: Point, transform: Transform) -> Point:
    a, mat, b = transform
    shifted = sub(point, a)
    rotated = rotate(shifted, mat)
    shifted_back = add(rotated, b)
    return shifted_back


def find_transform(points0: set[Point], points1: set[Point]) -> Transform | None:
    # we need to find reference points, assume p0 and p1 are corresponding
    for p0, p1 in product(points0, points1):
        # assuming that p0 corresponds to p1, there should be 11 other points in
        # beacons1 that can be rotated (around p1) onto points in beacons0
        other_relative0 = {
            (x - p0[0], y - p0[1], z - p0[2]) for x, y, z in set(points0) - {p0}
        }
        other_relative1 = {
            (x - p1[0], y - p1[1], z - p1[2]) for x, y, z in set(points1) - {p1}
        }
        # try every possible rotation and see if we end up with at least 11 matches
        for mat in all_rotations:
            rotated1 = {rotate(p, mat) for p in other_relative1}
            n_matching = len(rotated1 & other_relative0)
            if n_matching >= 11:
                return p1, mat, p0


# actual search, try merging matching scanner data until only one scanner is left
while len(scanner_data) > 1:
    remaining_indices = list(range(len(scanner_data)))
    for i, j in combinations(remaining_indices, 2):
        if (t := find_transform(scanner_data[i], scanner_data[j])) is not None:
            scanner_data[i] |= {transform(p, t) for p in scanner_data[j]}
            del scanner_data[j]
            break

print("Solution:", len(scanner_data[0]))
