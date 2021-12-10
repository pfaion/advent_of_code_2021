from pathlib import Path

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

score = 0
for line in data:
    stack = []
    for c in line:
        if c in pairs.keys():
            stack.append(pairs[c])
        elif c != stack.pop():
            score += scores[c]
            break


print("Solution:", score)
