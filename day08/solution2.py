from itertools import permutations, starmap
from pathlib import Path
from typing import Sequence

# loda data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse data
segments_data = [[part.split() for part in line.split(" | ")] for line in data]

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
possible_mappings = list(permutations(wires))
all_digits = set(range(10))

# define helper functions:


def to_digit(pattern: Sequence[str], mapping: Sequence[str]) -> int:
    lookup = {input: output for input, output in zip(mapping, wires)}
    actual_pattern = "".join(sorted(lookup[char] for char in pattern))
    # will raise KeyError if pattern is nonexistent
    return digit_patterns[actual_pattern]


def find_possible_mapping(inputs: Sequence[str]) -> Sequence[str]:
    # brute-force approach, can probably be optimized heavily!
    for mapping in possible_mappings:
        try:
            resulting_input_digits = {to_digit(pattern, mapping) for pattern in inputs}
        except KeyError:
            continue
        if resulting_input_digits == all_digits:
            return mapping


def decode_outputs(outputs: Sequence[str], mapping: Sequence[str]) -> int:
    digits = [to_digit(pattern, mapping) for pattern in outputs]
    return sum(digit * (10 ** exp) for exp, digit in enumerate(reversed(digits)))


# map all data
all_inputs, all_outputs = zip(*segments_data)
mappings = map(find_possible_mapping, all_inputs)
numbers = starmap(decode_outputs, zip(all_outputs, mappings))

print("Solution:", sum(numbers))
