<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2>--- Day 23: Amphipod ---</h2><p>A group of <a href="https://en.wikipedia.org/wiki/Amphipoda" target="_blank">amphipods</a> notice your fancy submarine and flag you down. "With such an impressive shell," one amphipod <span title="What? You didn't know amphipods can talk?">says</span>, "surely you can help us with a question that has stumped our best scientists."</p>
<p>They go on to explain that a group of timid, stubborn amphipods live in a nearby burrow. Four types of amphipods live there: <em>Amber</em> (<code>A</code>), <em>Bronze</em> (<code>B</code>), <em>Copper</em> (<code>C</code>), and <em>Desert</em> (<code>D</code>). They live in a burrow that consists of a <em>hallway</em> and four <em>side rooms</em>. The side rooms are initially full of amphipods, and the hallway is initially empty.</p>
<p>They give you a <em>diagram of the situation</em> (your puzzle input), including locations of each amphipod (<code>A</code>, <code>B</code>, <code>C</code>, or <code>D</code>, each of which is occupying an otherwise open space), walls (<code>#</code>), and open space (<code>.</code>).</p>
<p>For example:</p>
<pre><code>#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
</code></pre>
<p>The amphipods would like a method to organize every amphipod into side rooms so that each side room contains one type of amphipod and the types are sorted <code>A</code>-<code>D</code> going left to right, like this:</p>
<pre><code>#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
</code></pre>
<p>Amphipods can move up, down, left, or right so long as they are moving into an unoccupied open space. Each type of amphipod requires a different amount of <em>energy</em> to move one step: Amber amphipods require <code>1</code> energy per step, Bronze amphipods require <code>10</code> energy, Copper amphipods require <code>100</code>, and Desert ones require <code>1000</code>. The amphipods would like you to find a way to organize the amphipods that requires the <em>least total energy</em>.</p>
<p>However, because they are timid and stubborn, the amphipods have some extra rules:</p>
<ul>
<li>Amphipods will never <em>stop on the space immediately outside any room</em>. They can move into that space so long as they immediately continue moving. (Specifically, this refers to the four open spaces in the hallway that are directly above an amphipod starting position.)</li>
<li>Amphipods will never <em>move from the hallway into a room</em> unless that room is their destination room <em>and</em> that room contains no amphipods which do not also have that room as their own destination. If an amphipod's starting room is not its destination room, it can stay in that room until it leaves the room. (For example, an Amber amphipod will not move from the hallway into the right three rooms, and will only move into the leftmost room if that room is empty or if it only contains other Amber amphipods.)</li>
<li>Once an amphipod stops moving in the hallway, <em>it will stay in that spot until it can move into a room</em>. (That is, once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and will not move again until they can move fully into a room.)</li>
</ul>
<p>In the above example, the amphipods can be organized using a minimum of <code><em>12521</em></code> energy. One way to do this is shown below.</p>
<p>Starting configuration:</p>
<pre><code>#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
</code></pre>
<p>One Bronze amphipod moves into the hallway, taking 4 steps and using <code>40</code> energy:</p>
<pre><code>#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
</code></pre>
<p>The only Copper amphipod not in its side room moves there, taking 4 steps and using <code>400</code> energy:</p>
<pre><code>#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########
</code></pre>
<p>A Desert amphipod moves out of the way, taking 3 steps and using <code>3000</code> energy, and then the Bronze amphipod takes its place, taking 3 steps and using <code>30</code> energy:</p>
<pre><code>#############
#.....D.....#
###B#.#C#D###
  #A#B#C#A#
  #########
</code></pre>
<p>The leftmost Bronze amphipod moves to its room using <code>40</code> energy:</p>
<pre><code>#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########
</code></pre>
<p>Both amphipods in the rightmost room move into the hallway, using <code>2003</code> energy in total:</p>
<pre><code>#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########
</code></pre>
<p>Both Desert amphipods move into the rightmost room using <code>7000</code> energy:</p>
<pre><code>#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########
</code></pre>
<p>Finally, the last Amber amphipod moves into its room, using <code>8</code> energy:</p>
<pre><code>#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
</code></pre>
<p><em>What is the least energy required to organize the amphipods?</em></p>
</article>

</details>

## Solution 1

### Variant 1

```python

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


```

```

Runtime: 28.77195117699739

0             5             5            40           2000           500          3000           200           400           30             3             3            10            20            100           200          3000          2000     
############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# #############
#...........# #A..........# #AA.........# #AA.........# #AA.......D.# #AA...C...D.# #AA...C.D.D.# #AA.....D.D.# #AA...C.D.D.# #AA.B.C.D.D.# #A..B.C.D.D.# #...B.C.D.D.# #...B.C.D.D.# #.....C.D.D.# #.....C.D.D.# #.......D.D.# #.........D.# #...........#
###C#A#B#D### ###C#.#B#D### ###C#.#B#D### ###C#B#.#D### ###C#B#.#.### ###C#B#.#.### ###C#B#.#.### ###C#B#C#.### ###.#B#C#.### ###.#B#C#.### ###.#B#C#.### ###A#B#C#.### ###A#.#C#.### ###A#B#C#.### ###A#B#.#.### ###A#B#C#.### ###A#B#C#.### ###A#B#C#D###
  #B#A#D#C#     #B#A#D#C#     #B#.#D#C#     #B#.#D#C#     #B#.#D#C#     #B#.#D#.#     #B#.#.#.#     #B#.#.#.#     #B#.#.#.#     #.#.#.#.#     #A#.#.#.#     #A#.#.#.#     #A#B#.#.#     #A#B#.#.#     #A#B#C#.#     #A#B#C#.#     #A#B#C#D#     #A#B#C#D#  
  #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########  
Solution: 11516

```

<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>As you prepare to give the amphipods your solution, you notice that the diagram they handed you was actually folded up. As you unfold it, you discover an extra part of the diagram.</p>
<p>Between the first and second lines of text that contain amphipod starting positions, insert the following lines:</p>
<pre><code>  #D#C#B#A#
  #D#B#A#C#
</code></pre>
<p>So, the above example now becomes:</p>
<pre><code>#############
#...........#
###B#C#B#D###
  <em>#D#C#B#A#
  #D#B#A#C#</em>
  #A#D#C#A#
  #########
</code></pre>
<p>The amphipods still want to be organized into rooms similar to before:</p>
<pre><code>#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
</code></pre>
<p>In this updated example, the least energy required to organize these amphipods is <code><em>44169</em></code>:</p>
<pre><code>#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A..D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...D.....AD#
###.#B#C#.###
  #A#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
</code></pre>
<p>Using the initial configuration from the full diagram, <em>what is the least energy required to organize the amphipods?</em></p>
</article>

</details>

## Solution 2

### Variant 1

```python

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


```

```

Runtime: 9.228639979002764

Solving moves:
      0            50           2000           10            70            800           700          5000            6           9000           500           600           200           500          10000         10000           4            500           40             5            50            60            80             6             6             7             8            70      
############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# ############# #############
#...........# #..........B# #.........DB# #A........DB# #AB.......DB# #AB.C.....DB# #AB.C.C...DB# #AB.C.C....B# #AB.C.C...AB# #AB.C.C...AB# #AB.C.....AB# #AB.......AB# #AB.C.....AB# #AB.......AB# #AB.......AB# #AB.......AB# #AB.....A.AB# #AB.....A.AB# #AB.B...A.AB# #AB.B.A.A.AB# #AB...A.A.AB# #A....A.A.AB# #A....A.A.AB# #.....A.A.AB# #.......A.AB# #.........AB# #..........B# #...........#
###C#A#B#D### ###C#A#.#D### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###C#A#.#.### ###.#A#.#.### ###.#A#.#.### ###.#A#.#.### ###.#A#.#D### ###.#.#.#D### ###.#.#C#D### ###.#.#C#D### ###.#.#C#D### ###.#.#C#D### ###.#.#C#D### ###.#.#C#D### ###.#.#C#D### ###.#.#C#D### ###.#.#C#D### ###A#.#C#D### ###A#B#C#D###
  #D#C#B#A#     #D#C#B#A#     #D#C#B#A#     #D#C#B#.#     #D#C#.#.#     #D#C#.#.#     #D#C#.#.#     #D#C#.#.#     #D#C#.#.#     #D#C#.#.#     #D#C#.#.#     #D#C#.#.#     #D#C#.#.#     #D#C#C#.#     #.#C#C#D#     #.#C#C#D#     #.#C#C#D#     #.#.#C#D#     #.#.#C#D#     #.#.#C#D#     #.#.#C#D#     #.#.#C#D#     #.#B#C#D#     #.#B#C#D#     #.#B#C#D#     #A#B#C#D#     #A#B#C#D#     #A#B#C#D#  
  #D#B#A#C#     #D#B#A#C#     #D#B#A#C#     #D#B#A#C#     #D#B#A#C#     #D#B#A#.#     #D#B#A#.#     #D#B#A#.#     #D#B#.#.#     #D#B#.#D#     #D#B#.#D#     #D#B#C#D#     #D#B#C#D#     #D#B#C#D#     #D#B#C#D#     #.#B#C#D#     #.#B#C#D#     #.#B#C#D#     #.#.#C#D#     #.#.#C#D#     #.#.#C#D#     #.#B#C#D#     #.#B#C#D#     #.#B#C#D#     #A#B#C#D#     #A#B#C#D#     #A#B#C#D#     #A#B#C#D#  
  #B#A#D#C#     #B#A#D#C#     #B#A#D#C#     #B#A#D#C#     #B#A#D#C#     #B#A#D#C#     #B#A#D#.#     #B#A#D#D#     #B#A#D#D#     #B#A#.#D#     #B#A#C#D#     #B#A#C#D#     #B#A#C#D#     #B#A#C#D#     #B#A#C#D#     #B#A#C#D#     #B#A#C#D#     #B#A#C#D#     #B#A#C#D#     #B#.#C#D#     #B#B#C#D#     #B#B#C#D#     #.#B#C#D#     #A#B#C#D#     #A#B#C#D#     #A#B#C#D#     #A#B#C#D#     #A#B#C#D#  
  #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########     #########  
Solution: 40272

```