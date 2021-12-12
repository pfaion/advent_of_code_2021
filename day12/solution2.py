from collections import Counter, defaultdict
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
    for next_cave in graph[path[-1]]:
        if next_cave == "end":
            yield path + ["end"]
            continue
        if next_cave == "start":
            continue
        if not next_cave[0].islower() or next_cave not in path:
            yield from find_path_extensions(path + [next_cave])
            continue

        cave_visits = Counter(path)
        if cave_visits[next_cave] == 1 and not any(
            visits > 1 for cave, visits in cave_visits.items() if cave[0].islower()
        ):
            yield from find_path_extensions(path + [next_cave])


paths = list(find_path_extensions(["start"]))
print("Solution:", len(paths))
