from collections import Counter
from itertools import pairwise
from pathlib import Path

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse data
pair_counts = Counter(a + b for a, b in pairwise(data[0]))
insertions = dict(line.split(" -> ") for line in data[2:])

# transform each pair and count chars in parallel
char_counts = Counter(data[0])
for step in range(40):
    for pair, count in list(pair_counts.items()):
        char = insertions[pair]
        char_counts[char] += count
        pair_counts[pair[0] + char] += count
        pair_counts[char + pair[1]] += count
        pair_counts[pair] -= count

# count most/least common
sorted_counts = sorted(char_counts.values())
print("Solution:", sorted_counts[-1] - sorted_counts[0])
