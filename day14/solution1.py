from collections import Counter, defaultdict
from pathlib import Path

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse data
polymer = data[0]
rules = defaultdict(str, (line.split(" -> ") for line in data[2:]))

# iteration
steps = 10
for step in range(steps):
    polymer = "".join(c + rules[polymer[i : i + 2]] for i, c in enumerate(polymer))

# count most/least common
counts = Counter(polymer)
sorted_counts = counts.most_common()
most, least = sorted_counts[0][1], sorted_counts[-1][1]
print("Solution:", most - least)
