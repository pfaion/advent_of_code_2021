from pathlib import Path

# load data
data_file = Path(__file__).with_name("data.txt")
positions = [int(v) for v in data_file.read_text().strip().split(",")]

# fuel function (distance function)
def fuel_required(target: int) -> int:
    distances = (abs(target - pos) for pos in positions)
    # using formula for triangular numbers: sum(range(n + 1)) == n * (n + 1) / 2
    # this gives us an O(n) distance function
    fuel_for_distances = (d * (d + 1) / 2 for d in distances)
    return round(sum(fuel_for_distances))


# ------------------------------------------------------------------------------
# First idea:
# Brute-forcing in O(n^2)
possible_targets = range(min(positions), max(positions) + 1)
possible_fuel_required = (fuel_required(target) for target in possible_targets)

print("Solution (A):", min(possible_fuel_required))

# ------------------------------------------------------------------------------
# Second idea:
# It can be shown that the optimal target is in the range (mean +/- 0.5), which
# gives us an O(n) solution. Since we are looking for the discretized target:
#   - if the mean is a natural number, that must be the target
#   - else the target could be either ceil(mean) or floor(mean)

from statistics import mean
from math import floor, ceil

p = mean(positions)
possible_targets = {floor(p), ceil(p)}
possible_fuel_required = (fuel_required(target) for target in possible_targets)

print("Solution (B):", min(possible_fuel_required))
