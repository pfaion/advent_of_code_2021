from pathlib import Path
from collections import defaultdict

# load data
data = Path(__file__).with_name("data.txt").read_text()

# parse data (padded)
width = data.index("\n") + 1
wall = float("inf")
risk_levels = [int(char) if char != "\n" else wall for char in data]
risk_levels += [wall] * (width + 1)  # +1 because last row doesn't have \n

# Dijkstra's algorithm; use indices to identify nodes
start = 0
end = len(risk_levels) - width - 2
nodes = {i for i, risk in enumerate(risk_levels) if risk != wall}
costs = defaultdict(lambda: wall, {start: 0})
best_preceding = dict()
while end != (node := min(nodes, key=lambda n: costs[n])):
    nodes.remove(node)
    for neighbor in (node + offset for offset in (-width, -1, +1, width)):
        cost = costs[node] + risk_levels[neighbor]
        if cost < costs[neighbor]:
            costs[neighbor] = cost
            best_preceding[neighbor] = node

# compute total risk from (indirectly known) path
total_risk = risk_levels[end]
node = end
while start != (node := best_preceding[node]):
    total_risk += risk_levels[node]

print("Solution:", total_risk)
