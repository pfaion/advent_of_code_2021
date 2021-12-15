from pathlib import Path
from collections import defaultdict
from queue import PriorityQueue

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse and transform data (padded)
wall = float("inf")
risk_levels = []
for ry in range(5):
    for line in data:
        for rx in range(5):
            risk_levels += [((int(v) - 1 + ry + rx) % 9) + 1 for v in line]
        risk_levels += [wall]
width = risk_levels.index(wall) + 1
risk_levels += [wall] * width
height = len(risk_levels) // width

# A* algorithm; use indices to identify nodes
start = 0
end = len(risk_levels) - width - 2
known_risks = defaultdict(lambda: wall, {start: 0})


def risk_estimation(node: int) -> float | int:
    # use manhattan distance as remaining risk estimation
    row = node // height
    col = node % width
    estimated_risk_to_end = abs(row - height - 1) + abs(col - width - 1)
    return known_risks[node] + estimated_risk_to_end


# search loop
nodes = PriorityQueue()
nodes.put((risk_estimation(start), start))
while end != (node := nodes.get()[1]):
    for neighbor in (node + offset for offset in (-width, -1, +1, width)):
        risk = known_risks[node] + risk_levels[neighbor]
        if risk < known_risks[neighbor]:
            known_risks[neighbor] = risk
            nodes.put((risk, neighbor))


print("Solution:", known_risks[end])
