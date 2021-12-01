# Advent Of Code

## Day 1: Sonar Sweep

You're minding your own business on a ship at sea when the overboard alarm goes off! You rush to see if you can help. Apparently, one of the Elves tripped and accidentally sent the sleigh keys flying into the ocean!

Before you know it, you're inside a submarine the Elves keep ready for situations like this. It's covered in Christmas lights (because of course it is), and it even has an experimental antenna that should be able to track the keys if you can boost its signal strength high enough; there's a little meter that indicates the antenna's signal strength by displaying 0-50 _stars_.

Your instincts tell you that in order to save Christmas, you'll need to get all _fifty stars_ by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants _one star_. Good luck!

As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.

For example, suppose you had the following report:

    199
    200
    208
    210
    200
    207
    240
    269
    260
    263

This report indicates that, scanning outward from the submarine, the sonar sweep found depths of `199`, `200`, `208`, `210`, and so on.

The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get <span title="Does this premise seem fishy to you?">carried into deeper water</span> by an ocean current or a fish or something.

To do this, count _the number of times a depth measurement increases_ from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:

    199 (N/A - no previous measurement)
    200 (increased)
    208 (increased)
    210 (increased)
    200 (decreased)
    207 (increased)
    240 (increased)
    269 (increased)
    260 (decreased)
    263 (increased)

In this example, there are _`7`_ measurements that are larger than the previous measurement.

_How many measurements are larger than the previous measurement?_

### Solution Puzzle 1

For this we simply need to iterate over the list of numbers in pairs.


```python
import tools
from itertools import pairwise

numbers = tools.load_ints("day01.txt")
n_increments = sum(1 for a, b in pairwise(numbers) if b > a)

print(n_increments)
```

    1532


### Part Two

Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.

Instead, consider sums of a _three-measurement sliding window_. Again considering the above example:

    199  A      
    200  A B    
    208  A B C  
    210    B C D
    200  E   C D
    207  E F   D
    240  E F G  
    269    F G H
    260      G H
    263        H

Start by comparing the first and second three-measurement windows. The measurements in the first window are marked `A` (`199`, `200`, `208`); their sum is `199 + 200 + 208 = 607`. The second window is marked `B` (`200`, `208`, `210`); its sum is `618`. The sum of measurements in the second window is larger than the sum of the first, so this first comparison _increased_.

Your goal now is to count _the number of times the sum of measurements in this sliding window increases_ from the previous sum. So, compare `A` with `B`, then compare `B` with `C`, then `C` with `D`, and so on. Stop when there aren't enough measurements left to create a new three-measurement sum.

In the above example, the sum of each three-measurement window is as follows:

    A: 607 (N/A - no previous sum)
    B: 618 (increased)
    C: 618 (no change)
    D: 617 (decreased)
    E: 647 (increased)
    F: 716 (increased)
    G: 769 (increased)
    H: 792 (increased)

In this example, there are _`5`_ sums that are larger than the previous sum.

Consider sums of a three-measurement sliding window. _How many sums are larger than the previous sum?_

### Solution Puzzle 2

Here we need something like `pairwise`, but for triples. Generalized, this is a sliding window function. Unfortunately there is none in the standard library, so we create our own.


```python
from typing import Iterable, Iterator, Sequence
from collections import deque

def window(data: Iterable, window_size: int) -> Iterator[Sequence]:
    input_iterator = iter(data)
    window = deque()
    for value in input_iterator:
        window.append(value)
        if len(window) < window_size:
            continue
        yield tuple(window)
        window.popleft()
```

With this function we can quickly compute the sums and calculate the number of windowed measurement increments.


```python
sums = [sum(values) for values in window(numbers, 3)]
n_increments = sum(1 for a, b in pairwise(sums) if b > a)

print(n_increments)
```

    1571


<article class="day-desc"><h2>--- Day 1: Sonar Sweep ---</h2><p>You're minding your own business on a ship at sea when the overboard alarm goes off! You rush to see if you can help. Apparently, one of the Elves tripped and accidentally sent the sleigh keys flying into the ocean!</p>
<p>Before you know it, you're inside a submarine the Elves keep ready for situations like this. It's covered in Christmas lights (because of course it is), and it even has an experimental antenna that should be able to track the keys if you can boost its signal strength high enough; there's a little meter that indicates the antenna's signal strength by displaying 0-50 <em class="star">stars</em>.</p>
<p>Your instincts tell you that in order to save Christmas, you'll need to get all <em class="star">fifty stars</em> by December 25th.</p>
<p>Collect stars by solving puzzles.  Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first.  Each puzzle grants <em class="star">one star</em>. Good luck!</p>
<p>As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.</p>
<p>For example, suppose you had the following report:</p>
<pre><code>199
200
208
210
200
207
240
269
260
263
</code></pre>
<p>This report indicates that, scanning outward from the submarine, the sonar sweep found depths of <code>199</code>, <code>200</code>, <code>208</code>, <code>210</code>, and so on.</p>
<p>The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get <span title="Does this premise seem fishy to you?">carried into deeper water</span> by an ocean current or a fish or something.</p>
<p>To do this, count <em>the number of times a depth measurement increases</em> from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:</p>
<pre><code>199 (N/A - no previous measurement)
200 (<em>increased</em>)
208 (<em>increased</em>)
210 (<em>increased</em>)
200 (decreased)
207 (<em>increased</em>)
240 (<em>increased</em>)
269 (<em>increased</em>)
260 (decreased)
263 (<em>increased</em>)
</code></pre>
<p>In this example, there are <em><code>7</code></em> measurements that are larger than the previous measurement.</p>
<p><em>How many measurements are larger than the previous measurement?</em></p>
</article>


