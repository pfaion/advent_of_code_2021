<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2>--- Day 13: Transparent Origami ---</h2><p>You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.</p>
<p>Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:</p>
<pre><code>Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.
</code></pre>
<p>Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of <a href="https://en.wikipedia.org/wiki/Transparency_(projection)" target="_blank">transparent paper</a>! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:</p>
<pre><code>6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
</code></pre>
<p>The first section is a list of dots on the transparent paper. <code>0,0</code> represents the top-left coordinate.  The first value, <code>x</code>, increases to the right.  The second value, <code>y</code>, increases downward.  So, the coordinate <code>3,0</code> is to the right of <code>0,0</code>, and the coordinate <code>0,7</code> is below <code>0,0</code>. The coordinates in this example form the following pattern, where <code>#</code> is a dot on the paper and <code>.</code> is an empty, unmarked position:</p>
<pre><code>...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
</code></pre>
<p>Then, there is a list of <em>fold instructions</em>. Each instruction indicates a line on the transparent paper and wants you to fold the paper <em>up</em> (for horizontal <code>y=...</code> lines) or <em>left</em> (for vertical <code>x=...</code> lines). In this example, the first fold instruction is <code>fold along y=7</code>, which designates the line formed by all of the positions where <code>y</code> is <code>7</code> (marked here with <code>-</code>):</p>
<pre><code>...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
</code></pre>
<p>Because this is a horizontal line, fold the bottom half <em>up</em>. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:</p>
<pre><code>#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........
</code></pre>
<p>Now, only <code>17</code> dots are visible.</p>
<p>Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at <code>0,0</code> and <code>0,1</code>). Because the paper is transparent, the dot just below them in the result (at <code>0,3</code>) remains visible, as it can be seen through the transparent paper.</p>
<p>Also notice that some dots can end up <em>overlapping</em>; in this case, the dots merge together and become a single dot.</p>
<p>The second fold instruction is <code>fold along x=5</code>, which indicates this line:</p>
<pre><code>#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....
</code></pre>
<p>Because this is a vertical line, fold <em>left</em>:</p>
<pre><code>#####
#...#
#...#
#...#
#####
.....
.....
</code></pre>
<p>The instructions made a square!</p>
<p>The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, <code><em>17</em></code> dots are visible - dots that end up overlapping after the fold is completed count as a single dot.</p>
<p><em>How many dots are visible after completing just the first fold instruction on your transparent paper?</em></p>
</article>

</details>

## Solution 1

### Variant 1

```python

from itertools import product
from pathlib import Path

# load data
data = Path(__file__).with_name("data.txt").read_text()
points_raw, folds_raw = data.split("\n\n")

# parse data
points = {tuple(map(int, line.split(","))) for line in points_raw.splitlines()}
folds = [(line[11], int(line.split("=")[1])) for line in folds_raw.splitlines()]

# first folds
axis, fold = folds[0]
if axis == "y":
    points = {(x, y) if y <= fold else (x, 2 * fold - y) for x, y in points}
else:
    points = {(x, y) if x <= fold else (2 * fold - x, y) for x, y in points}

print("Solution:", len(points))


```

```

Runtime: 0.02867035599774681

Solution: 785

```

<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p><span title="How can you fold it that many times? You tell me, I'm not the one folding it.">Finish folding</span> the transparent paper according to the instructions. The manual says the code is always <em>eight capital letters</em>.</p>
<p><em>What code do you use to activate the infrared thermal imaging camera system?</em></p>
</article>

</details>

## Solution 2

### Variant 1

```python

from pathlib import Path

# load data
data = Path(__file__).with_name("data.txt").read_text()
points_raw, folds_raw = data.split("\n\n")

# parse data
points = {tuple(map(int, line.split(","))) for line in points_raw.splitlines()}
folds = [(line[11], int(line.split("=")[1])) for line in folds_raw.splitlines()]

# folds
for axis, fold in folds:
    if axis == "y":
        points = {(x, y) if y <= fold else (x, 2 * fold - y) for x, y in points}
    else:
        points = {(x, y) if x <= fold else (2 * fold - x, y) for x, y in points}

print("Solution:")
x_max = max(x for x, y in points)
y_max = max(y for x, y in points)
for y in range(y_max + 1):
    for x in range(x_max + 1):
        print("\N{FULL BLOCK}" if (x, y) in points else " ", end="")
    print()


```

```

Runtime: 0.030223483976442367

Solution:
????????????   ??????  ??????  ???  ???   ??????  ??????   ??????  ???  ???
???       ??? ???  ??? ???  ???    ??? ???  ??? ???  ??? ???  ???
?????????     ??? ???  ??? ????????????    ??? ???    ???  ??? ????????????
???       ??? ???????????? ???  ???    ??? ??? ?????? ???????????? ???  ???
???    ???  ??? ???  ??? ???  ??? ???  ??? ???  ??? ???  ??? ???  ???
???     ??????  ???  ??? ???  ???  ??????   ????????? ???  ??? ???  ???

```