from collections import Counter
from itertools import chain, starmap
from pathlib import Path
from typing import Iterable

# loda data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse data
all_inputs, all_outputs = zip(
    *([section.split() for section in line.split(" | ")] for line in data)
)


# define some static helpers
wires = "abcdefg"
digit_patterns = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


# Determine the wire mapping for a set of observed wire activities.
def find_mapping(inputs: Iterable[str]) -> str:
    # makes use of the fact that in a full set of wire activities, many wires
    # have a unique number of occurrences
    all_chars = chain.from_iterable(inputs)
    char_counts = Counter(all_chars)
    # the remaining two ambiguities can be resolved by looking at the patterns
    # for wiring the digits 1 and 4, which can be unique identified by their
    # wire count
    one_pattern = next(pattern for pattern in inputs if len(pattern) == 2)
    four_pattern = next(pattern for pattern in inputs if len(pattern) == 4)
    mapping = dict()
    for char, count in char_counts.items():
        if count == 4:
            mapping["e"] = char
        elif count == 6:
            mapping["b"] = char
        elif count == 7 and char in four_pattern:
            mapping["d"] = char
        elif count == 7 and char not in four_pattern:
            mapping["g"] = char
        elif count == 8 and char in one_pattern:
            mapping["c"] = char
        elif count == 8 and char not in one_pattern:
            mapping["a"] = char
        elif count == 9:
            mapping["f"] = char
    return "".join(map(mapping.get, wires))


def to_digit(pattern: Iterable[str], mapping: Iterable[str]) -> int:
    lookup = {input: output for input, output in zip(mapping, wires)}
    actual_pattern = "".join(sorted(lookup[char] for char in pattern))
    return digit_patterns[actual_pattern]


def decode_outputs(outputs: Iterable[str], mapping: Iterable[str]) -> int:
    digits = [to_digit(pattern, mapping) for pattern in outputs]
    return sum(digit * (10 ** exp) for exp, digit in enumerate(reversed(digits)))


# transform the data
mappings = map(find_mapping, all_inputs)
numbers = starmap(decode_outputs, zip(all_outputs, mappings))

print("Solution:", sum(numbers))
