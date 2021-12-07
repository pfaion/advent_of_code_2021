from pathlib import Path

# load data
data_file = Path(__file__).with_name("data.txt")
positions = [int(v) for v in data_file.read_text().strip().split(",")]


def fuel_required(target: int) -> int:
    distances = (abs(target - pos) for pos in positions)
    # cut down complexity from n*n to n with formula for:
    # sum(range(n + 1)) == n * (n + 1) / 2
    fuel_for_distances = (d * (d + 1) / 2 for d in distances)
    return int(sum(fuel_for_distances))


possible_targets = range(min(positions), max(positions) + 1)
possible_fuel_required = (fuel_required(target) for target in possible_targets)


print("Solution:", min(possible_fuel_required))
