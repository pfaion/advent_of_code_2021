<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2>--- Day 4: Giant Squid ---</h2><p>You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you <em>can</em> see, however, is a giant squid that has attached itself to the outside of your submarine.</p>
<p>Maybe it wants to play <a href="https://en.wikipedia.org/wiki/Bingo_(American_version)" target="_blank">bingo</a>?</p>
<p>Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is <em>marked</em> on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board <em>wins</em>. (Diagonals don't count.)</p>
<p>The submarine has a <em>bingo subsystem</em> to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:</p>
<pre><code>7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
</code></pre>
<p>After the first five numbers are drawn (<code>7</code>, <code>4</code>, <code>9</code>, <code>5</code>, and <code>11</code>), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):</p>
<pre><code>22 13 17 <em>11</em>  0         3 15  0  2 22        14 21 17 24  <em>4</em>
 8  2 23  <em>4</em> 24         <em>9</em> 18 13 17  <em>5</em>        10 16 15  <em>9</em> 19
21  <em>9</em> 14 16  <em>7</em>        19  8  <em>7</em> 25 23        18  8 23 26 20
 6 10  3 18  <em>5</em>        20 <em>11</em> 10 24  <em>4</em>        22 <em>11</em> 13  6  <em>5</em>
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  <em>7</em>
</code></pre>
<p>After the next six numbers are drawn (<code>17</code>, <code>23</code>, <code>2</code>, <code>0</code>, <code>14</code>, and <code>21</code>), there are still no winners:</p>
<pre><code>22 13 <em>17</em> <em>11</em>  <em>0</em>         3 15  <em>0</em>  <em>2</em> 22        <em>14</em> <em>21</em> <em>17</em> 24  <em>4</em>
 8  <em>2</em> <em>23</em>  <em>4</em> 24         <em>9</em> 18 13 <em>17</em>  <em>5</em>        10 16 15  <em>9</em> 19
<em>21</em>  <em>9</em> <em>14</em> 16  <em>7</em>        19  8  <em>7</em> 25 <em>23</em>        18  8 <em>23</em> 26 20
 6 10  3 18  <em>5</em>        20 <em>11</em> 10 24  <em>4</em>        22 <em>11</em> 13  6  <em>5</em>
 1 12 20 15 19        <em>14</em> <em>21</em> 16 12  6         <em>2</em>  <em>0</em> 12  3  <em>7</em>
</code></pre>
<p>Finally, <code>24</code> is drawn:</p>
<pre><code>22 13 <em>17</em> <em>11</em>  <em>0</em>         3 15  <em>0</em>  <em>2</em> 22        <em>14</em> <em>21</em> <em>17</em> <em>24</em>  <em>4</em>
 8  <em>2</em> <em>23</em>  <em>4</em> <em>24</em>         <em>9</em> 18 13 <em>17</em>  <em>5</em>        10 16 15  <em>9</em> 19
<em>21</em>  <em>9</em> <em>14</em> 16  <em>7</em>        19  8  <em>7</em> 25 <em>23</em>        18  8 <em>23</em> 26 20
 6 10  3 18  <em>5</em>        20 <em>11</em> 10 <em>24</em>  <em>4</em>        22 <em>11</em> 13  6  <em>5</em>
 1 12 20 15 19        <em>14</em> <em>21</em> 16 12  6         <em>2</em>  <em>0</em> 12  3  <em>7</em>
</code></pre>
<p>At this point, the third board <em>wins</em> because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: <code><em>14 21 17 24  4</em></code>).</p>
<p>The <em>score</em> of the winning board can now be calculated. Start by finding the <em>sum of all unmarked numbers</em> on that board; in this case, the sum is <code>188</code>. Then, multiply that sum by <em>the number that was just called</em> when the board won, <code>24</code>, to get the final score, <code>188 * 24 = <em>4512</em></code>.</p>
<p>To guarantee victory against the giant squid, figure out which board will win first. <em>What will your final score be if you choose that board?</em></p>
</article>

</details>

## Solution 1

### Variant 1

```python

from pathlib import Path
from typing import Iterable, List, Iterator, Optional, Set

# load data
data_file = Path(__file__).with_name("data.txt")
data_raw = data_file.read_text().splitlines()

# helper
def batchwise(iterable: Iterable, batch_size: int) -> Iterator:
    args = [iter(iterable)] * batch_size
    return zip(*args)


# board representation
all_indices = list(range(25))
winning_index_sets: List[Set[int]] = []
for row_batch in batchwise(all_indices, 5):
    winning_index_sets.append(set(row_batch))
for col_batch in zip(*batchwise(all_indices, 5)):
    winning_index_sets.append(set(col_batch))


class Board:
    def __init__(self, numbers: List[int]):
        self.numbers = numbers
        self.marked_idxs: Set[int] = set()

    def mark(self, number: int):
        try:
            self.marked_idxs.add(self.numbers.index(number))
        except ValueError:
            pass

    def bingo(self) -> bool:
        return any(winning.issubset(self.marked_idxs) for winning in winning_index_sets)

    def score(self) -> int:
        return sum(
            num for idx, num in enumerate(self.numbers) if idx not in self.marked_idxs
        )


# parse data
number_sequence = map(int, data_raw[0].split(","))
boards: List[Board] = []
for _blank, *rows in batchwise(data_raw[1:], batch_size=6):
    flat = " ".join(rows).split()
    boards.append(Board(numbers=[int(v) for v in flat]))

# simulate game loop
number_generator = iter(number_sequence)
winning_board: Optional[Board] = None
while winning_board is None:
    number = next(number_generator)
    for board in boards:
        board.mark(number)
        if board.bingo():
            winning_board = board
            break

# solution
print("Solution:", winning_board.score() * number)


```

```

Runtime: 0.04153806300018914

Solution: 50008

```

<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>On the other hand, it might be wise to try a different strategy: <span title="That's 'cuz a submarine don't pull things' antennas out of their sockets when they lose. Giant squid are known to do that.">let the giant squid win</span>.</p>
<p>You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to <em>figure out which board will win last</em> and choose that one. That way, no matter which boards it picks, it will win for sure.</p>
<p>In the above example, the second board is the last to win, which happens after <code>13</code> is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to <code>148</code> for a final score of <code>148 * 13 = <em>1924</em></code>.</p>
<p>Figure out which board will win last. <em>Once it wins, what would its final score be?</em></p>
</article>

</details>

## Solution 2

### Variant 1

```python

from pathlib import Path
from typing import Iterable, Iterator, List, Set

# load data
data_file = Path(__file__).with_name("data.txt")
data_raw = data_file.read_text().splitlines()

# helper
def batchwise(iterable: Iterable, batch_size: int) -> Iterator:
    args = [iter(iterable)] * batch_size
    return zip(*args)


# board representation
all_indices = list(range(25))
winning_index_sets: List[Set[int]] = []
for row_batch in batchwise(all_indices, 5):
    winning_index_sets.append(set(row_batch))
for col_batch in zip(*batchwise(all_indices, 5)):
    winning_index_sets.append(set(col_batch))


class Board:
    def __init__(self, numbers: List[int]):
        self.numbers = numbers
        self.marked_idxs: Set[int] = set()

    def mark(self, number: int):
        try:
            self.marked_idxs.add(self.numbers.index(number))
        except ValueError:
            pass

    def bingo(self) -> bool:
        return any(winning.issubset(self.marked_idxs) for winning in winning_index_sets)

    def score(self) -> int:
        return sum(
            num for idx, num in enumerate(self.numbers) if idx not in self.marked_idxs
        )


# parse data
number_sequence = map(int, data_raw[0].split(","))
boards: List[Board] = []
for _blank, *rows in batchwise(data_raw[1:], batch_size=6):
    flat = " ".join(rows).split()
    boards.append(Board(numbers=[int(v) for v in flat]))

# simulate game loop
for number in number_sequence:
    for board in boards:
        board.mark(number)
    # take out boards that won
    remaining_boards = [board for board in boards if not board.bingo()]
    if not remaining_boards:
        # we assume that there was only one board left, otherwise the task makes no sense
        last_board = boards[0]
        break
    boards = remaining_boards

# solution
print("Solution:", last_board.score() * number)


```

```

Runtime: 0.04604454702348448

Solution: 17408

```