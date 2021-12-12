from collections import defaultdict
from pathlib import Path
from typing import Iterable

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse into adjacency "list" (set here for easy bidirectionality)
graph: dict[str, set[str]] = defaultdict(set)
for line in data:
    a, b = line.split("-")
    graph[a].add(b)
    graph[b].add(a)


def find_path_extensions(path: list[str]) -> Iterable[list[str]]:
    for next_node in graph[path[-1]]:
        if next_node == "end":
            yield path + ["end"]
        elif not next_node[0].islower() or next_node not in path:
            yield from find_path_extensions(path + [next_node])


paths = list(find_path_extensions(["start"]))
print("Solution:", len(paths))
