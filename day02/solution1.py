from pathlib import Path

# load data
data_file = Path(__file__).with_name("day02.txt")
commands_raw = data_file.read_text().splitlines()

# parse data
directions, distances = zip(*(cmd.split() for cmd in commands_raw))
distances = map(int, distances)

# loop over commands and accumulate
horizontal_position, depth = (0, 0)
for direction, distance in zip(directions, distances):
    match direction:
        case "forward":
            horizontal_position += distance
        case "up":
            depth -= distance
        case "down":
            depth += distance

print("Solution:", horizontal_position * depth)