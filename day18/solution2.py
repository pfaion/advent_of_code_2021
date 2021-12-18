from pathlib import Path
import re
from itertools import permutations

numbers = Path(__file__).with_name("data.txt").read_text().splitlines()

# who needs hierarchical data, we do string operations! :D


def find_depth_4(number: str) -> int | None:
    counter = 0
    for i, char in enumerate(number):
        if char == "[":
            if counter == 4:
                return i
            counter += 1
        elif char == "]":
            counter -= 1
    return None


def add(n1: str, n2: str) -> str:
    result = f"[{n1},{n2}]"
    while True:

        # check if we need to explode first
        if (explode_start := find_depth_4(result)) is not None:
            # extract numbers from pair to explode
            explode_stop = result.index("]", explode_start)
            part_left = result[:explode_start]
            part_explode = result[explode_start : explode_stop + 1]
            part_right = result[explode_stop + 1 :]
            a, b = map(int, part_explode[1:-1].split(","))
            # adjust number to the left (tricky, need to search in reversed string)
            if left := re.search(r"\d+", part_left[::-1]):
                num = int(left.group(0)[::-1])
                part_left = (
                    part_left[: -left.end()] + str(num + a) + part_left[-left.start() :]
                )
            # adjust next number to the right
            if right := re.search(r"\d+", part_right):
                num = int(right.group(0))
                part_right = (
                    part_right[: right.start()]
                    + str(num + b)
                    + part_right[right.end() :]
                )
            result = part_left + "0" + part_right

        # or check if we need to split
        elif split := re.search(r"\d\d+", result):
            num = int(split.group(0))
            a = num // 2
            b = num - a
            result = re.sub(r"\d\d+", f"[{a},{b}]", result, count=1)

        # otherwise we're done
        else:
            return result


def magnitude(number: str) -> int:
    magnitude_formula = (
        number.replace("[", "(3*").replace(",", " + 2*").replace("]", ")")
    )
    return eval(magnitude_formula)


max_magnitude = 0
for a, b in permutations(numbers, r=2):
    mag = magnitude(add(a, b))
    if mag > max_magnitude:
        max_magnitude = mag

print("Solution:", max_magnitude)
