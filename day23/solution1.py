from pathlib import Path
from queue import PriorityQueue
from typing import Iterable

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# represent world by list of available fields
space = ["."] * 19
# parse shrimp starting positions
for i, c in enumerate(data[2][3:10:2]):
    space[11 + i] = c
for i, c in enumerate(data[3][3:10:2]):
    space[15 + i] = c

costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
homes = {"A": (11, 15), "B": (12, 16), "C": (13, 17), "D": (14, 18)}


# debug helper functions for printing (left it in for final transition)
def rep(space: list[str], cost: int = 0) -> str:
    return """\
  {:^9}  
#############
#{}{}{}{}{}{}{}{}{}{}{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#  
  #########  """.format(
        cost, *space
    )


def rep_all(spaces: list[list[str]], costs: list[int]) -> str:
    reps = (rep(space, cost).splitlines() for space, cost in zip(spaces, costs))
    lines_segments = zip(*reps)
    lines = [" ".join(segments) for segments in lines_segments]
    return "\n".join(lines)


Path = list[int]

# get all positions on a path
def get_path(start: int, stop: int) -> Path:
    if start < 11:  # hallway to home
        assert stop >= 11
        target_door = ((stop - 4 if stop >= 15 else stop) - 10) * 2
        path = list(range(start, target_door, (1 if target_door > start else -1)))
        # exclude start, include end
        path = path[1:] + [target_door]
        # first slot
        path.append(10 + target_door // 2)
        # second slot
        if stop >= 15:
            path.append(path[-1] + 4)
        return path
    elif stop < 11:  # home to hallway
        reverse = get_path(stop, start)
        return reverse[-2::-1] + [stop]
    elif not any(
        start in slots and stop in slots for slots in homes.values()
    ):  # home to different home
        # to door
        if start >= 15:
            path = [start - 4, (start - 14) * 2]
        else:
            path = [(start - 10) * 2]
        door = path[-1]
        path += get_path(door, stop)
        return path
    else:  # home to same home
        return [stop]


# check if shrimp can move back to home
def is_home_ready(space: list[str], c: str) -> bool:
    return all(space[slot] in (c, ".") for slot in homes[c])


# yield all possible paths for given shrimp
def possible_shrimp_paths(space: list[str], pos: int) -> Iterable[Path]:
    non_door_hallway = (0, 1, 3, 5, 7, 9, 10)
    c = space[pos]
    if pos < 11:  # in hallway
        if is_home_ready(space, c):
            for slot in homes[c]:
                yield get_path(pos, slot)
    elif pos in homes[c]:  # in correct home
        for other_slot in set(homes[c]) - {pos}:  # stay in home
            yield get_path(pos, other_slot)
        for end in non_door_hallway:  # move to hallway
            yield get_path(pos, end)
    else:  # in other home
        for end in non_door_hallway:  # move to hallway
            yield get_path(pos, end)
        if is_home_ready(space, c):  # move to correct home
            for slot in homes[c]:
                yield get_path(pos, slot)


# yield all unblocked paths for given shrimp
def free_shrimp_paths(space: list[str], pos: int) -> Iterable[Path]:
    for path in possible_shrimp_paths(space, pos):
        if all(space[p] == "." for p in path):
            yield path


# get all valid shrimp moves for a given state
def moves(space: list[str]) -> Iterable[tuple[int, int, int]]:
    for shrimp_pos, c in ((i, c) for i, c in enumerate(space) if c != "."):
        for path in free_shrimp_paths(space, shrimp_pos):
            cost = len(path) * costs[c]
            yield shrimp_pos, path[-1], cost


# transform state by applying move
def apply_move(space: list[str], start: int, stop: int) -> list[str]:
    new_space = space.copy()
    new_space[start], new_space[stop] = new_space[stop], new_space[start]
    return new_space


# check if state is finished
def finished(space: list[str]) -> bool:
    for c, slots in homes.items():
        if not all(space[slot] == c for slot in slots):
            return False
    return True


# solve the puzzle
def solve_smallest_cost(space: list[str]) -> int:
    cache = {}
    search_space = PriorityQueue()
    search_space.put((0, [space], [0]))
    while True:
        cost, spaces, costs = search_space.get()
        space = spaces[-1]
        if finished(space):
            print(rep_all(spaces, costs))
            return cost
        for start, stop, move_cost in moves(space):
            new_space = apply_move(space, start, stop)
            new_cost = cost + move_cost
            cacheable_space = tuple(new_space)
            if cacheable_space not in cache or new_cost < cache[cacheable_space]:
                cache[cacheable_space] = new_cost
                search_space.put((new_cost, spaces + [new_space], costs + [move_cost]))


print("Solution:", solve_smallest_cost(space))
