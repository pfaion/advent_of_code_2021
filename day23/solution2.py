from functools import cache
from pathlib import Path
from queue import PriorityQueue
from typing import Iterable

# load data
data = Path(__file__).with_name("data.txt").read_text().splitlines()
data = data[0:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + data[3:]

# represent world by list of available fields
space = ["."] * (11 + 4 * 4)
# parse shrimp starting positions
for home_row in range(4):
    for i, c in enumerate(data[2 + home_row][3:10:2]):
        space[11 + (4 * home_row) + i] = c

costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
homes = {c: tuple(range(11 + i, 24 + i, 4)) for i, c in enumerate("ABCD")}


# debug helper functions for printing (left it in for final transition)
def rep(space: list[str], cost: int = 0) -> str:
    return """\
  {:^9}  
#############
#{}{}{}{}{}{}{}{}{}{}{}#
###{}#{}#{}#{}###
  #{}#{}#{}#{}#  
  #{}#{}#{}#{}#  
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
@cache
def get_path(start: int, stop: int) -> Path:
    # hallway to home
    if start < 11:
        assert stop >= 11  # we cannot move hallway to hallway anyways
        # find door
        first_slot = stop
        while first_slot >= 15:
            first_slot -= 4
        target_door = (first_slot - 10) * 2
        # path to door
        path = list(range(start, target_door, (1 if target_door > start else -1)))
        path = path[1:] + [target_door]
        # first slot
        path.append(first_slot)
        # go to final slot
        while path[-1] != stop:
            path.append(path[-1] + 4)
        return path

    # home to hallway
    elif stop < 11:
        reverse = get_path(stop, start)
        return reverse[-2::-1] + [stop]

    # home to different home
    elif not any(start in slots and stop in slots for slots in homes.values()):
        # to first slot
        first_slot = start
        while first_slot >= 15:
            first_slot -= 4
        target_door = (first_slot - 10) * 2
        path = list(range(start, first_slot, -4))
        path = path[1:] + [first_slot, target_door]
        path += get_path(target_door, stop)
        return path

    # home to same home
    else:
        path = list(range(start, stop, (4 if start < stop else -4)))
        path = path[1:] + [stop]
        return path


# check if shrimp can move back to home
def is_home_ready(space: list[str], c: str) -> bool:
    return all(space[slot] in (c, ".") for slot in homes[c])


# yield all possible paths for given shrimp
def possible_shrimp_paths(space: list[str], pos: int) -> Iterable[Path]:
    non_door_hallway = (0, 1, 3, 5, 7, 9, 10)
    c = space[pos]

    # in hallway
    if pos < 11:
        if is_home_ready(space, c):
            last_free_pos = max(slot for slot in homes[c] if space[slot] == ".")
            yield get_path(pos, last_free_pos)

    # in correct home
    elif pos in homes[c]:
        # move to hallway
        for end in non_door_hallway:
            yield get_path(pos, end)

    # in other home
    else:
        # move to hallway
        for end in non_door_hallway:
            yield get_path(pos, end)
        # move to correct home
        if is_home_ready(space, c):
            last_free_pos = max(slot for slot in homes[c] if space[slot] == ".")
            yield get_path(pos, last_free_pos)


# yield all unblocked paths for given shrimp
def free_shrimp_paths(space: list[str], pos: int) -> Iterable[Path]:
    for path in possible_shrimp_paths(space, pos):
        if all(space[p] == "." for p in path):
            yield path


# get all valid shrimp moves for a given state
def moves(space: list[str]) -> list[tuple[int, int, int]]:
    m = []
    for shrimp_pos, c in ((i, c) for i, c in enumerate(space) if c != "."):
        for path in free_shrimp_paths(space, shrimp_pos):
            stop = path[-1]
            cost = len(path) * costs[c]
            # if there's a possible move that moves a shrimp to the last pos in
            # their home, we should always do that!
            if shrimp_pos not in homes[c] and is_home_ready(space, c):
                last_free_pos = max(slot for slot in homes[c] if space[slot] == ".")
                if stop == last_free_pos:
                    return [(shrimp_pos, stop, cost)]

            m.append((shrimp_pos, stop, cost))
    return m


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
            print("Solving moves:")
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
