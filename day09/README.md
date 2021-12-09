<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2>--- Day 9: Smoke Basin ---</h2><p>These caves seem to be <a href="https://en.wikipedia.org/wiki/Lava_tube" target="_blank">lava tubes</a>. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly <span title="This was originally going to be a puzzle about watersheds, but we're already under water.">settles like rain</span>.</p>
<p>If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).</p>
<p>Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:</p>
<pre><code>2<em>1</em>9994321<em>0</em>
3987894921
98<em>5</em>6789892
8767896789
989996<em>5</em>678
</code></pre>
<p>Each number corresponds to the height of a particular location, where <code>9</code> is the highest and <code>0</code> is the lowest a location can be.</p>
<p>Your first goal is to find the <em>low points</em> - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)</p>
<p>In the above example, there are <em>four</em> low points, all highlighted: two are in the first row (a <code>1</code> and a <code>0</code>), one is in the third row (a <code>5</code>), and one is in the bottom row (also a <code>5</code>). All other locations on the heightmap have some lower adjacent location, and so are not low points.</p>
<p>The <em>risk level</em> of a low point is <em>1 plus its height</em>. In the above example, the risk levels of the low points are <code>2</code>, <code>1</code>, <code>6</code>, and <code>6</code>. The sum of the risk levels of all low points in the heightmap is therefore <code><em>15</em></code>.</p>
<p>Find all of the low points on your heightmap. <em>What is the sum of the risk levels of all low points on your heightmap?</em></p>
</article>

</details>

## Solution 1

### Variant 1

```python

from pathlib import Path
from itertools import product
from typing import Callable, Iterable, Iterator

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse as 2D list of ints
heightmap = [[int(n) for n in line] for line in data]
n_rows = len(heightmap)
n_cols = len(heightmap[0])


def get_neighbors(row: int, col: int) -> list[int]:
    neighbors = []
    if row > 0:
        neighbors.append(heightmap[row - 1][col])
    if row < n_rows - 1:
        neighbors.append(heightmap[row + 1][col])
    if col > 0:
        neighbors.append(heightmap[row][col - 1])
    if col < n_cols - 1:
        neighbors.append(heightmap[row][col + 1])
    return neighbors


def is_low_point(point: int, neighbors: list[int]) -> bool:
    return all(point < neighbor for neighbor in neighbors)


coordinates = product(range(n_rows), range(n_cols))
low_points = (
    point
    for row, col in coordinates
    if is_low_point(point := heightmap[row][col], get_neighbors(row, col))
)
risk_levels = (point + 1 for point in low_points)

print("Solution:", sum(risk_levels))


```

Runtime: 0.05693229100143071

Solution: 425

<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>Next, you need to find the largest basins so you know what areas are most important to avoid.</p>
<p>A <em>basin</em> is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height <code>9</code> do not count as being in any basin, and all other locations will always be part of exactly one basin.</p>
<p>The <em>size</em> of a basin is the number of locations within the basin, including the low point. The example above has four basins.</p>
<p>The top-left basin, size <code>3</code>:</p>
<pre><code><em>21</em>99943210
<em>3</em>987894921
9856789892
8767896789
9899965678
</code></pre>
<p>The top-right basin, size <code>9</code>:</p>
<pre><code>21999<em>43210</em>
398789<em>4</em>9<em>21</em>
985678989<em>2</em>
8767896789
9899965678
</code></pre>
<p>The middle basin, size <code>14</code>:</p>
<pre><code>2199943210
39<em>878</em>94921
9<em>85678</em>9892
<em>87678</em>96789
9<em>8</em>99965678
</code></pre>
<p>The bottom-right basin, size <code>9</code>:</p>
<pre><code>2199943210
3987894921
9856789<em>8</em>92
876789<em>678</em>9
98999<em>65678</em>
</code></pre>
<p>Find the three largest basins and multiply their sizes together. In the above example, this is <code>9 * 14 * 9 = <em>1134</em></code>.</p>
<p><em>What do you get if you multiply together the sizes of the three largest basins?</em></p>
</article>

</details>

## Solution 2

### Variant 1

```python

import math
from itertools import chain, product
from pathlib import Path
from typing import Iterator, Sequence

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse as 2D list of ints
heightmap = [[int(n) for n in line] for line in data]
n_rows = len(heightmap)
n_cols = len(heightmap[0])

Point = tuple[int, int]


def get_height(point: Point) -> int:
    row, col = point
    return heightmap[row][col]


def get_neighbors(point: Point) -> Iterator[Point]:
    row, col = point
    if row > 0:
        yield (row - 1, col)
    if row < n_rows - 1:
        yield (row + 1, col)
    if col > 0:
        yield (row, col - 1)
    if col < n_cols - 1:
        yield (row, col + 1)


def is_low_point(point: Point) -> bool:
    height = get_height(point)
    return all(height < get_height(neighbor) for neighbor in get_neighbors(point))


flatten = chain.from_iterable


def get_basein(start: Point) -> Sequence[int]:
    basein = {start}
    visited = set()
    while basein != visited:
        unvisited = basein - visited
        all_neighbors = set(flatten(map(get_neighbors, unvisited)))
        basein |= {neighbor for neighbor in all_neighbors if get_height(neighbor) < 9}
        visited |= unvisited
    return basein


coordinates = product(range(n_rows), range(n_cols))
low_point_coordinates = filter(is_low_point, coordinates)
low_point_baseins = map(get_basein, low_point_coordinates)
basein_lengths = map(len, low_point_baseins)
result = math.prod(sorted(basein_lengths)[-3:])

print("Solution:", result)


```

Runtime: 0.06344393800100079

Solution: 1135260