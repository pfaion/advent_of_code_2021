<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2>--- Day 17: Trick Shot ---</h2><p>You finally decode the Elves' message. <code><span title="Maybe you need to turn the message 90 degrees counterclockwise?">HI</span></code>, the message says. You continue searching for the sleigh keys.</p>
<p>Ahead of you is what appears to be a large <a href="https://en.wikipedia.org/wiki/Oceanic_trench" target="_blank">ocean trench</a>. Could the keys have fallen into it? You'd better send a probe to investigate.</p>
<p>The probe launcher on your submarine can fire the probe with any <a href="https://en.wikipedia.org/wiki/Integer" target="_blank">integer</a> velocity in the <code>x</code> (forward) and <code>y</code> (upward, or downward if negative) directions. For example, an initial <code>x,y</code> velocity like <code>0,10</code> would fire the probe straight up, while an initial velocity like <code>10,-1</code> would fire the probe forward at a slight downward angle.</p>
<p>The probe's <code>x,y</code> position starts at <code>0,0</code>. Then, it will follow some trajectory by moving in <em>steps</em>. On each step, these changes occur in the following order:</p>
<ul>
<li>The probe's <code>x</code> position increases by its <code>x</code> velocity.</li>
<li>The probe's <code>y</code> position increases by its <code>y</code> velocity.</li>
<li>Due to drag, the probe's <code>x</code> velocity changes by <code>1</code> toward the value <code>0</code>; that is, it decreases by <code>1</code> if it is greater than <code>0</code>, increases by <code>1</code> if it is less than <code>0</code>, or does not change if it is already <code>0</code>.</li>
<li>Due to gravity, the probe's <code>y</code> velocity decreases by <code>1</code>.</li>
</ul>
<p>For the probe to successfully make it into the trench, the probe must be on some trajectory that causes it to be within a <em>target area</em> after any step. The submarine computer has already calculated this target area (your puzzle input). For example:</p>
<pre><code>target area: x=20..30, y=-10..-5</code></pre>
<p>This target area means that you need to find initial <code>x,y</code> velocity values such that after any step, the probe's <code>x</code> position is at least <code>20</code> and at most <code>30</code>, <em>and</em> the probe's <code>y</code> position is at least <code>-10</code> and at most <code>-5</code>.</p>
<p>Given this target area, one initial velocity that causes the probe to be within the target area after any step is <code>7,2</code>:</p>
<pre><code>.............#....#............
.......#..............#........
...............................
S........................#.....
...............................
...............................
...........................#...
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTT#TT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
</code></pre>
<p>In this diagram, <code>S</code> is the probe's initial position, <code>0,0</code>. The <code>x</code> coordinate increases to the right, and the <code>y</code> coordinate increases upward. In the bottom right, positions that are within the target area are shown as <code>T</code>. After each step (until the target area is reached), the position of the probe is marked with <code>#</code>. (The bottom-right <code>#</code> is both a position the probe reaches and a position in the target area.)</p>
<p>Another initial velocity that causes the probe to be within the target area after any step is <code>6,3</code>:</p>
<pre><code>...............#..#............
...........#........#..........
...............................
......#..............#.........
...............................
...............................
S....................#.........
...............................
...............................
...............................
.....................#.........
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................T#TTTTTTTTT
....................TTTTTTTTTTT
</code></pre>
<p>Another one is <code>9,0</code>:</p>
<pre><code>S........#.....................
.................#.............
...............................
........................#......
...............................
....................TTTTTTTTTTT
....................TTTTTTTTTT#
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
....................TTTTTTTTTTT
</code></pre>
<p>One initial velocity that <em>doesn't</em> cause the probe to be within the target area after any step is <code>17,-4</code>:</p>
<pre><code>S..............................................................
...............................................................
...............................................................
...............................................................
.................#.............................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT................................
....................TTTTTTTTTTT..#.............................
....................TTTTTTTTTTT................................
...............................................................
...............................................................
...............................................................
...............................................................
................................................#..............
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
...............................................................
..............................................................#
</code></pre>
<p>The probe appears to pass through the target area, but is never within it after any step. Instead, it continues down and to the right - only the first few steps are shown.</p>
<p>If you're going to fire a highly scientific probe out of a super cool probe launcher, you might as well do it with <em>style</em>. How high can you make the probe go while still reaching the target area?</p>
<p>In the above example, using an initial velocity of <code>6,9</code> is the best you can do, causing the probe to reach a maximum <code>y</code> position of <code><em>45</em></code>. (Any higher initial <code>y</code> velocity causes the probe to overshoot the target area entirely.)</p>
<p>Find the initial velocity that causes the probe to reach the highest <code>y</code> position and still eventually be within the target area after any step. <em>What is the highest <code>y</code> position it reaches on this trajectory?</em></p>
</article>

</details>

## Solution 1

### Variant 1

```python

from math import ceil, sqrt

target_x_min, target_x_max = 155, 182
target_y_min, target_y_max = -117, -67


def simulate(vx: int, vy: int) -> tuple[int, bool]:
    x, y, y_max = 0, 0, 0
    while True:
        # update step
        x += vx
        y += vy
        if vx < 0:
            vx += 1
        elif vx > 0:
            vx -= 1
        vy -= 1

        y_max = max(y_max, y)

        # check if hit target
        if target_x_min <= x <= target_x_max and target_y_min <= y <= target_y_max:
            return y_max, True

        # check if over- or undershoot
        if (
            (x > target_x_max)
            or (vx == 0 and x < target_x_min)
            or (vy <= 0 and y < target_y_min)
        ):
            return y_max, False


y_max = 0

# for initial velocity of vx0, position x will stop changing upon reaching
# 1 + 2 + ... + vx0 = vx0 * (vx0 + 1) / 2
# if we try to hit target_x_min, solving for vx0 gives us
# bound = -0.5 +/- sqrt(0.25 + 2 * target_x_min)
vx0_lower_bound = ceil(-0.5 + sqrt(0.25 + 2 * target_x_min))
# if we have vx0 > target_x_max, we will always overshoot
vx0_upper_bound = target_x_max
for vx0 in range(vx0_lower_bound, vx0_upper_bound + 1):
    # as lower bound we can simply chose target_y_min, or we undershoot
    vy0_lower_bound = target_y_min
    # after going up, we always hit y=0 again, exactly after 2*vx + 2 steps
    # the velocity at that point will be -vy0 - 1
    # that means the next y will also be -vy0 - 1
    # the higest y will be reached by having the largest initial vy0 that still lets us hit the target
    # so to hit the target at the lowest point, we need target_y_min = -vy0 - 1
    # so we simulate up to vy0 = -1 - target_y_min
    vy0_upper_bound = -1 - target_y_min
    for vy0 in range(vy0_lower_bound, vy0_upper_bound + 1):
        trajectory_y_max, success = simulate(vx0, vy0)
        if success:
            y_max = max(y_max, trajectory_y_max)

print("Solution:", y_max)


```

```

Runtime: 0.1260455430019647

Solution: 6786

```

<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>Maybe a fancy trick shot isn't the best idea; after all, you only have one probe, so you had better not miss.</p>
<p>To get the best idea of what your options are for launching the probe, you need to find <em>every initial velocity</em> that causes the probe to eventually be within the target area after any step.</p>
<p>In the above example, there are <code><em>112</em></code> different initial velocity values that meet these criteria:</p>
<pre><code>23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7
</code></pre>
<p><em>How many distinct initial velocity values cause the probe to be within the target area after any step?</em></p>
</article>

</details>

## Solution 2

### Variant 1

```python

from math import ceil, sqrt

target_x_min, target_x_max = 155, 182
target_y_min, target_y_max = -117, -67


def simulate(vx: int, vy: int) -> bool:
    x, y = 0, 0
    while True:
        # update step
        x += vx
        y += vy
        if vx < 0:
            vx += 1
        elif vx > 0:
            vx -= 1
        vy -= 1

        # check if hit target
        if target_x_min <= x <= target_x_max and target_y_min <= y <= target_y_max:
            return True

        # check if over- or undershoot
        if (
            (x > target_x_max)
            or (vx == 0 and x < target_x_min)
            or (vy <= 0 and y < target_y_min)
        ):
            return False


n_hits = 0

# for initial velocity of vx0, position x will stop changing upon reaching
# 1 + 2 + ... + vx0 = vx0 * (vx0 + 1) / 2
# if we try to hit target_x_min, solving for vx0 gives us
# bound = -0.5 +/- sqrt(0.25 + 2 * target_x_min)
vx0_lower_bound = ceil(-0.5 + sqrt(0.25 + 2 * target_x_min))
# if we have vx0 > target_x_max, we will always overshoot
vx0_upper_bound = target_x_max
for vx0 in range(vx0_lower_bound, vx0_upper_bound + 1):
    # as lower bound we can simply chose target_y_min, or we undershoot
    vy0_lower_bound = target_y_min
    # after going up, we always hit y=0 again, exactly after 2*vx + 2 steps
    # the velocity at that point will be -vy0 - 1
    # that means the next y will also be -vy0 - 1
    # the higest y will be reached by having the largest initial vy0 that still lets us hit the target
    # so to hit the target at the lowest point, we need target_y_min = -vy0 - 1
    # so we simulate up to vy0 = -1 - target_y_min
    vy0_upper_bound = -1 - target_y_min
    for vy0 in range(vy0_lower_bound, vy0_upper_bound + 1):
        if simulate(vx0, vy0):
            n_hits += 1

print("Solution:", n_hits)


```

```

Runtime: 0.07090324303135276

Solution: 2313

```