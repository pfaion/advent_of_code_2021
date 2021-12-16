from pathlib import Path
from collections import defaultdict
from queue import PriorityQueue

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse data into full map with coordinate tuples
data_rows, data_cols = len(data), len(data[0])
n_rows, n_cols = data_rows * 5, data_cols * 5
risk_levels = {
    (r + dr * data_rows, c + dc * data_cols): (int(data[r][c]) - 1 + dr + dc) % 9 + 1
    for r in range(data_rows)
    for c in range(data_cols)
    for dr in range(5)
    for dc in range(5)
}

# A* algorithm; represent nodes as coordinate tuples
start = (0, 0)
end = (n_rows - 1, n_cols - 1)
nodes = PriorityQueue()
nodes.put((0, start))  # weight doesn't matter here
known_risks = defaultdict(lambda: float("inf"), {start: 0})

# search loop
while end != (node := nodes.get()[1]):

    row, col = node
    neighbors = ((row + dr, col + dc) for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)))
    neighbors = ((r, c) for r, c in neighbors if 0 <= r < n_rows and 0 <= c < n_cols)
    for neighbor in neighbors:

        risk = known_risks[node] + risk_levels[neighbor]
        if risk < known_risks[neighbor]:
            known_risks[neighbor] = risk

            # use manhattan distance to estimate remaining risk to end
            estimated_rest_risk = abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])
            nodes.put((risk + estimated_rest_risk, neighbor))

print("Solution:", known_risks[end])
