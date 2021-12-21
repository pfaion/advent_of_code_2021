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
