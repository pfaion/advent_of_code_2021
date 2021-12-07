<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2>--- Day 7: The Treachery of Whales ---</h2><p>A giant <a href="https://en.wikipedia.org/wiki/Sperm_whale" target="_blank">whale</a> has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!</p>
<p>Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a <em>massive underground cave system</em> just beyond where they're aiming!</p>
<p>The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?</p>
<p>There's one major catch - crab submarines can only move horizontally.</p>
<p>You quickly make a list of <em>the horizontal position of each crab</em> (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.</p>
<p>For example, consider the following horizontal positions:</p>
<pre><code>16,1,2,0,4,2,7,1,2,14</code></pre>
<p>This means there's a crab with horizontal position <code>16</code>, a crab with horizontal position <code>1</code>, and so on.</p>
<p>Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position <code>2</code>:</p>
<ul>
<li>Move from <code>16</code> to <code>2</code>: <code>14</code> fuel</li>
<li>Move from <code>1</code> to <code>2</code>: <code>1</code> fuel</li>
<li>Move from <code>2</code> to <code>2</code>: <code>0</code> fuel</li>
<li>Move from <code>0</code> to <code>2</code>: <code>2</code> fuel</li>
<li>Move from <code>4</code> to <code>2</code>: <code>2</code> fuel</li>
<li>Move from <code>2</code> to <code>2</code>: <code>0</code> fuel</li>
<li>Move from <code>7</code> to <code>2</code>: <code>5</code> fuel</li>
<li>Move from <code>1</code> to <code>2</code>: <code>1</code> fuel</li>
<li>Move from <code>2</code> to <code>2</code>: <code>0</code> fuel</li>
<li>Move from <code>14</code> to <code>2</code>: <code>12</code> fuel</li>
</ul>
<p>This costs a total of <code><em>37</em></code> fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position <code>1</code> (<code>41</code> fuel), position <code>3</code> (<code>39</code> fuel), or position <code>10</code> (<code>71</code> fuel).</p>
<p>Determine the horizontal position that the crabs can align to using the least fuel possible. <em>How much fuel must they spend to align to that position?</em></p>
</article>

</details>

## Solution 1

```python

from pathlib import Path
from statistics import median

# load data
data_file = Path(__file__).with_name("data.txt")
positions = [int(v) for v in data_file.read_text().strip().split(",")]

# median minimizes the sum absolute differences
target = median(positions)
fuel_required = int(sum(abs(pos - target) for pos in positions))

print("Solution:", fuel_required)


```

Solution: 328318



<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?</p>
<p>As it turns out, crab submarine engines <span title="This appears to be due to the modial interaction of magneto-reluctance and capacitive duractance.">don't burn fuel at a constant rate</span>. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs <code>1</code>, the second step costs <code>2</code>, the third step costs <code>3</code>, and so on.</p>
<p>As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes <code>5</code>:</p>
<ul>
<li>Move from <code>16</code> to <code>5</code>: <code>66</code> fuel</li>
<li>Move from <code>1</code> to <code>5</code>: <code>10</code> fuel</li>
<li>Move from <code>2</code> to <code>5</code>: <code>6</code> fuel</li>
<li>Move from <code>0</code> to <code>5</code>: <code>15</code> fuel</li>
<li>Move from <code>4</code> to <code>5</code>: <code>1</code> fuel</li>
<li>Move from <code>2</code> to <code>5</code>: <code>6</code> fuel</li>
<li>Move from <code>7</code> to <code>5</code>: <code>3</code> fuel</li>
<li>Move from <code>1</code> to <code>5</code>: <code>10</code> fuel</li>
<li>Move from <code>2</code> to <code>5</code>: <code>6</code> fuel</li>
<li>Move from <code>14</code> to <code>5</code>: <code>45</code> fuel</li>
</ul>
<p>This costs a total of <code><em>168</em></code> fuel. This is the new cheapest possible outcome; the old alignment position (<code>2</code>) now costs <code>206</code> fuel instead.</p>
<p>Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! <em>How much fuel must they spend to align to that position?</em></p>
</article>

</details>

## Solution 2

```python

from pathlib import Path

# load data
data_file = Path(__file__).with_name("data.txt")
positions = [int(v) for v in data_file.read_text().strip().split(",")]

# fuel function (distance function)
def fuel_required(target: int) -> int:
    distances = (abs(target - pos) for pos in positions)
    # using formula for triangular numbers: sum(range(n + 1)) == n * (n + 1) / 2
    # this gives us an O(n) distance function
    fuel_for_distances = (d * (d + 1) / 2 for d in distances)
    return round(sum(fuel_for_distances))


# ------------------------------------------------------------------------------
# First idea:
# Brute-forcing in O(n^2)
possible_targets = range(min(positions), max(positions) + 1)
possible_fuel_required = (fuel_required(target) for target in possible_targets)

print("Solution (A):", min(possible_fuel_required))

# ------------------------------------------------------------------------------
# Second idea:
# It can be shown that the optimal target is in the range (mean +/- 0.5), which
# gives us an O(n) solution. Since we are looking for the discretized target:
#   - if the mean is a natural number, that must be the target
#   - else the target could be either ceil(mean) or floor(mean)

from statistics import mean
from math import floor, ceil

p = mean(positions)
possible_targets = {floor(p), ceil(p)}
possible_fuel_required = (fuel_required(target) for target in possible_targets)

print("Solution (B):", min(possible_fuel_required))


```

Solution (A): 89791146

Solution (B): 89791146

