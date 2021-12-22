from pathlib import Path
from itertools import product

# load
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse
steps = []
for line in data:
    mode, tmp = line.split(" ")
    low, high = zip(*(map(int, ax.split("=")[1].split("..")) for ax in tmp.split(",")))
    if any(l > 50 for l in low) or any(h < -50 for h in high):
        continue
    steps.append((mode, low, high))


# apply
on = set()
for mode, low, high in steps:
    for point in product(*(range(l, h + 1) for l, h in zip(low, high))):
        if mode == "on":
            on.add(point)
        elif point in on:
            on.remove(point)

print("Solution:", len(on))
