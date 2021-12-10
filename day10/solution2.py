from pathlib import Path

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
scores = {")": 1, "]": 2, "}": 3, ">": 4}

line_scores = []
for line in data:
    score = 0
    stack = []
    for c in line:
        if c in pairs.keys():
            stack.append(pairs[c])
        elif c != stack[-1]:
            break
        else:
            stack.pop()
    else:
        for c in reversed(stack):
            score *= 5
            score += scores[c]
        line_scores.append(score)


print("Solution:", sorted(line_scores)[len(line_scores) // 2])
