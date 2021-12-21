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
