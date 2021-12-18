import re
from itertools import accumulate, permutations
from pathlib import Path

numbers = Path(__file__).with_name("data.txt").read_text().splitlines()

# who needs hierarchical data, we do string operations! :D


def add(n1: str, n2: str) -> str:
    result = f"[{n1},{n2}]"
    while True:

        # check if we need to explode first
        depths = accumulate({"[": 1, "]": -1}.get(char, 0) for char in result)
        first_depth_5 = next((i for i, depth in enumerate(depths) if depth == 5), None)
        if (explode_start := first_depth_5) is not None:
            # extract numbers from pair to explode
            explode_stop = result.index("]", explode_start)
            left = result[:explode_start]
            a, b = map(int, result[explode_start + 1 : explode_stop].split(","))
            right = result[explode_stop + 1 :]
            # adjust number to the left (tricky, need to search in reversed string)
            if match := re.search(r"\d+", left[::-1]):
                num = int(match.group(0)[::-1])
                left = left[: -match.end()] + str(num + a) + left[-match.start() :]
            # adjust next number to the right
            if match := re.search(r"\d+", right):
                num = int(match.group(0))
                right = right[: match.start()] + str(num + b) + right[match.end() :]
            # fuse again and replace pair
            result = left + "0" + right

        # or check if we need to split
        elif split := re.search(r"\d\d+", result):
            num = int(split.group(0))
            result = re.sub(r"\d\d+", f"[{num // 2},{(num + 1) // 2}]", result, count=1)

        # otherwise we're done
        else:
            return result


def magnitude(number: str) -> int:
    formula = number.replace("[", "(3*").replace(",", " + 2*").replace("]", ")")
    return eval(formula)


max_magnitude = max(magnitude(add(a, b)) for a, b in permutations(numbers, r=2))
print("Solution:", max_magnitude)
