from collections import Counter
from itertools import pairwise
from math import ceil
from pathlib import Path

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse data
# only work locally on existing pairs, no need to know te whole polymer
pair_counts = Counter(a + b for a, b, in pairwise(data[0]))
insertions = dict((line.split(" -> ") for line in data[2:]))

# transform each pair
steps = 40
for step in range(steps):
    new = Counter()
    for pair, count in pair_counts.items():
        if count == 0 or pair not in insertions:
            continue
        insertion = insertions[pair]
        new[pair[0] + insertion] += count
        new[insertion + pair[1]] += count
    pair_counts = new

# count single chars from pair counts
char_counts = Counter()
for (a, b), count in pair_counts.items():
    char_counts[a] += count / 2
    char_counts[b] += count / 2
# first and last char are only in one pair, so will have fraction counts, just ceil them
for char, count in char_counts.items():
    char_counts[char] = ceil(count)

# count most/least common
sorted_counts = char_counts.most_common()
most, least = sorted_counts[0][1], sorted_counts[-1][1]
print("Solution:", most - least)
