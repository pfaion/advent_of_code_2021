import operator
from itertools import pairwise, starmap, islice
from pathlib import Path
from collections import deque

# load data as ints
data_file = Path(__file__).with_name("day01.txt")
sea_floor_depths = map(int, data_file.read_text().splitlines())

# helper function: generalize 'pairwise' to arbitrary tuples
def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


# compute sums of sliding triples first
depth_triples = sliding_window(sea_floor_depths, 3)
triple_sums = map(sum, depth_triples)

# compute similar to puzzle one: how many triple sums increase
sum_pairs = pairwise(triple_sums)
sum_increases = starmap(operator.lt, sum_pairs)
n_increments = sum(sum_increases)

print("Solution:", n_increments)
