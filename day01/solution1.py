import operator
from itertools import pairwise, starmap
from pathlib import Path

# load data as ints
data_file = Path(__file__).with_name("day01.txt")
sea_floor_depths = map(int, data_file.read_text().splitlines())

# compute number of pairs (a, b) where a < b
depth_pairs = pairwise(sea_floor_depths)
pair_increases = starmap(operator.lt, depth_pairs)
n_increments = sum(pair_increases)

print("Solution:", n_increments)
