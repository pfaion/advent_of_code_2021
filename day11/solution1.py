from pathlib import Path
from itertools import product
from typing import Counter

# load data
data = Path(__file__).with_name("data.txt").read_text()

# parse data (padded)
wall = float("-inf")
energies = [wall if char == "\n" else int(char) for char in data]
width = energies.index(wall) + 1
energies += [wall] * (width + 1)

# helper
neighbor_idxs = (-width - 1, -width, -width + 1, -1, +1, width - 1, width, width + 1)

# simulation
steps = 100
flashes = 0
for step in range(steps):

    # initial step
    energies = [e + 1 for e in energies]

    # iteratively update neighbors
    flashing = set()
    while True:
        new = set(i for i, e in enumerate(energies) if e > 9) - flashing
        if not new:
            break
        flashing |= new
        neighbors = Counter(i + offset for i, offset in product(new, neighbor_idxs))
        for i, count in neighbors.items():
            energies[i] += count
    flashes += len(flashing)

    # reset energy of flashed octopi
    energies = [e if e <= 9 else 0 for e in energies]

print("Solution:", flashes)
