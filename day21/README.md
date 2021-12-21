<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2>--- Day 21: Dirac Dice ---</h2><p>There's not much to do as you slowly descend to the bottom of the ocean. The submarine computer <span title="A STRANGE GAME.">challenges you to a nice game</span> of <em>Dirac Dice</em>.</p>
<p>This game consists of a single <a href="https://en.wikipedia.org/wiki/Dice" target="_blank">die</a>, two <a href="https://en.wikipedia.org/wiki/Glossary_of_board_games#piece" target="_blank">pawns</a>, and a game board with a circular track containing ten spaces marked <code>1</code> through <code>10</code> clockwise. Each player's <em>starting space</em> is chosen randomly (your puzzle input). Player 1 goes first.</p>
<p>Players take turns moving. On each player's turn, the player rolls the die <em>three times</em> and adds up the results. Then, the player moves their pawn that many times <em>forward</em> around the track (that is, moving clockwise on spaces in order of increasing value, wrapping back around to <code>1</code> after <code>10</code>). So, if a player is on space <code>7</code> and they roll <code>2</code>, <code>2</code>, and <code>1</code>, they would move forward 5 times, to spaces <code>8</code>, <code>9</code>, <code>10</code>, <code>1</code>, and finally stopping on <code>2</code>.</p>
<p>After each player moves, they increase their <em>score</em> by the value of the space their pawn stopped on. Players' scores start at <code>0</code>. So, if the first player starts on space <code>7</code> and rolls a total of <code>5</code>, they would stop on space <code>2</code> and add <code>2</code> to their score (for a total score of <code>2</code>). The game immediately ends as a win for any player whose score reaches <em>at least <code>1000</code></em>.</p>
<p>Since the first game is a practice game, the submarine opens a compartment labeled <em>deterministic dice</em> and a 100-sided die falls out. This die always rolls <code>1</code> first, then <code>2</code>, then <code>3</code>, and so on up to <code>100</code>, after which it starts over at <code>1</code> again. Play using this die.</p>
<p>For example, given these starting positions:</p>
<pre><code>Player 1 starting position: 4
Player 2 starting position: 8
</code></pre>
<p>This is how the game would go:</p>
<ul>
<li>Player 1 rolls <code>1</code>+<code>2</code>+<code>3</code> and moves to space <code>10</code> for a total score of <code>10</code>.</li>
<li>Player 2 rolls <code>4</code>+<code>5</code>+<code>6</code> and moves to space <code>3</code> for a total score of <code>3</code>.</li>
<li>Player 1 rolls <code>7</code>+<code>8</code>+<code>9</code> and moves to space <code>4</code> for a total score of <code>14</code>.</li>
<li>Player 2 rolls <code>10</code>+<code>11</code>+<code>12</code> and moves to space <code>6</code> for a total score of <code>9</code>.</li>
<li>Player 1 rolls <code>13</code>+<code>14</code>+<code>15</code> and moves to space <code>6</code> for a total score of <code>20</code>.</li>
<li>Player 2 rolls <code>16</code>+<code>17</code>+<code>18</code> and moves to space <code>7</code> for a total score of <code>16</code>.</li>
<li>Player 1 rolls <code>19</code>+<code>20</code>+<code>21</code> and moves to space <code>6</code> for a total score of <code>26</code>.</li>
<li>Player 2 rolls <code>22</code>+<code>23</code>+<code>24</code> and moves to space <code>6</code> for a total score of <code>22</code>.</li>
</ul>
<p>...after many turns...</p>
<ul>
<li>Player 2 rolls <code>82</code>+<code>83</code>+<code>84</code> and moves to space <code>6</code> for a total score of <code>742</code>.</li>
<li>Player 1 rolls <code>85</code>+<code>86</code>+<code>87</code> and moves to space <code>4</code> for a total score of <code>990</code>.</li>
<li>Player 2 rolls <code>88</code>+<code>89</code>+<code>90</code> and moves to space <code>3</code> for a total score of <code>745</code>.</li>
<li>Player 1 rolls <code>91</code>+<code>92</code>+<code>93</code> and moves to space <code>10</code> for a final score, <code>1000</code>.</li>
</ul>
<p>Since player 1 has at least <code>1000</code> points, player 1 wins and the game ends. At this point, the losing player had <code>745</code> points and the die had been rolled a total of <code>993</code> times; <code>745 * 993 = <em>739785</em></code>.</p>
<p>Play a practice game using the deterministic 100-sided die. The moment either player wins, <em>what do you get if you multiply the score of the losing player by the number of times the die was rolled during the game?</em></p>
</article>

</details>

## Solution 1

### Variant 1

```python

from itertools import cycle, islice

die = cycle(range(1, 101))

# represent positions in 0-9 instead of 1-10 for easier modulo
positions = {1: 0, -1: 4}
scores = {1: 0, -1: 0}

player = 1
rolls = 0
while max(scores.values()) < 1000:
    roll = sum(islice(die, 3))
    positions[player] = (positions[player] + roll) % 10
    scores[player] += positions[player] + 1
    player *= -1
    rolls += 3

print("Solution:", min(scores.values()) * rolls)


```

```

Runtime: 0.023400511003274005

Solution: 432450

```

<details><summary>Exercise Text (click to expand)</summary>

<article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>Now that you're warmed up, it's time to play the real game.</p>
<p>A second compartment opens, this time labeled <em>Dirac dice</em>. Out of it falls a single three-sided die.</p>
<p>As you experiment with the die, you feel a little strange. An informational brochure in the compartment explains that this is a <em>quantum die</em>: when you roll it, the universe <em>splits into multiple copies</em>, one copy for each possible outcome of the die. In this case, rolling the die always splits the universe into <em>three copies</em>: one where the outcome of the roll was <code>1</code>, one where it was <code>2</code>, and one where it was <code>3</code>.</p>
<p>The game is played the same as before, although to prevent things from getting too far out of hand, the game now ends when either player's score reaches at least <code><em>21</em></code>.</p>
<p>Using the same starting positions as in the example above, player 1 wins in <code><em>444356092776315</em></code> universes, while player 2 merely wins in <code>341960390180808</code> universes.</p>
<p>Using your given starting positions, determine every possible outcome. <em>Find the player that wins in more universes; in how many universes does that player win?</em></p>
</article>

</details>

## Solution 2

### Variant 1

```python

from itertools import product
from collections import Counter
from typing import Literal

# define my types so I don't get confused
PlayerState = tuple[int, int]  # pos, score
Player = Literal[0] | Literal[1]
GameState = tuple[PlayerState, PlayerState, Player]  # p1, p2, active_player

# represent positions in 0-9 instead of 1-10 for easier modulo
initial_state: GameState = ((0, 0), (4, 0), 0)

# cache already visited game states
winning_worlds: dict[GameState, tuple[int, int]] = {}

# possible dice rolls
possible_rolls = Counter(sum(vals) for vals in product((1, 2, 3), repeat=3))

# play game from state on, return winning worlds for (p1, p2)
def play(state: GameState) -> tuple[int, int]:
    # cache lookup
    if state in winning_worlds:
        return winning_worlds[state]

    # count winning worlds for all possible outcomes
    player = state[2]
    pos, score = state[player]
    wins = [0, 0]
    for roll, count in possible_rolls.items():
        new_pos = (pos + roll) % 10
        new_score = score + new_pos + 1
        if new_score > 20:
            wins[player] += count
        else:
            player_state = (new_pos, new_score)
            new_state = (
                player_state if player == 0 else state[0],
                player_state if player == 1 else state[1],
                (player + 1) % 2,
            )
            new_wins = play(new_state)
            wins[0] += new_wins[0] * count
            wins[1] += new_wins[1] * count
    wins = tuple(wins)
    winning_worlds[state] = wins
    return wins


wins = play(initial_state)
print("Solution:", max(wins))


```

```

Runtime: 0.18791675399552332

Solution: 138508043837521

```