from pathlib import Path
from itertools import chain

# load data
data_file = Path(__file__).with_name("data.txt")
positions = [int(v) for v in data_file.read_text().strip().split(",")]


def fuel_required(target: int) -> int:
    # get raw distances
    distances = (abs(target - pos) for pos in positions)
    # each "distance" is decomposed into steps that we need to sum
    steps = (range(distance + 1) for distance in distances)
    # sum steps for each position
    return int(sum(chain.from_iterable(steps)))


possible_targets = range(min(positions), max(positions) + 1)
possible_fuel_required = (fuel_required(target) for target in possible_targets)

print("Solution:", min(possible_fuel_required))
