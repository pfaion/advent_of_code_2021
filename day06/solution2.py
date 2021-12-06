from pathlib import Path
from collections import Counter

# load data
data_file = Path(__file__).with_name("data.txt")
ages = map(int, data_file.read_text().splitlines()[0].split(","))

# better representation as dict
fish_per_age = Counter(ages)

# simulate
n_days = 256
for _ in range(n_days):
    fish_per_age = Counter({age - 1: n_fish for age, n_fish in fish_per_age.items()})
    fish_per_age[8] += fish_per_age[-1]
    fish_per_age[6] += fish_per_age[-1]
    fish_per_age.pop(-1, _)

print("Solution:", sum(fish_per_age.values()))
