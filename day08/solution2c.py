from collections import defaultdict
from itertools import starmap
from pathlib import Path
from typing import Callable, Iterable, TypeVar

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse data
all_inputs, all_outputs = zip(
    *([section.split() for section in line.split(" | ")] for line in data)
)

# some helper functions:
T = TypeVar("T")


def pop(input: list[T], predicate=Callable) -> T:
    # pop first element that matches the predicate from input list
    index = next(i for i, elem in enumerate(input) if predicate(elem))
    return input.pop(index)


def sorted_str(input: Iterable[str]) -> str:
    # sorts an iterable of strings and concatenates it into a single string
    # mostly useful for turning iterables of single chars into sorted strings
    return "".join(sorted(input))


# given a full set of wire activations, determines which activation corresponds
# to which digit
def find_mapping(inputs: Iterable[str]) -> dict[str, int]:

    # we rely heavily on set operations, so turn each input string into a set of
    # active wires
    string_sets = map(set, inputs)

    # group input patterns by length
    patterns_by_length = defaultdict(list)
    for pattern in string_sets:
        patterns_by_length[len(pattern)].append(pattern)

    # determine mappings of pattern to digit
    digit_ptrn: dict[int, set[str]] = dict()

    # first the digits with unique lengths
    digit_ptrn[1] = patterns_by_length[2].pop()
    digit_ptrn[4] = patterns_by_length[4].pop()
    digit_ptrn[7] = patterns_by_length[3].pop()
    digit_ptrn[8] = patterns_by_length[7].pop()

    # now other ambiguities can be solved with set operations on already known digits
    digit_ptrn[3] = pop(patterns_by_length[5], digit_ptrn[1].issubset)
    digit_ptrn[2] = pop(patterns_by_length[5], lambda p: len(p & digit_ptrn[4]) == 2)
    digit_ptrn[5] = patterns_by_length[5].pop()

    digit_ptrn[9] = pop(patterns_by_length[6], digit_ptrn[4].issubset)
    digit_ptrn[6] = pop(patterns_by_length[6], digit_ptrn[5].issubset)
    digit_ptrn[0] = patterns_by_length[6].pop()

    return {sorted_str(pattern): digit for digit, pattern in digit_ptrn.items()}


def decode_outputs(outputs: Iterable[str], mapping: dict[str, int]) -> int:
    outputs = map(sorted_str, outputs)
    digits = [mapping[pattern] for pattern in outputs]
    return sum(digit * (10 ** exp) for exp, digit in enumerate(reversed(digits)))


# transform the data
mappings = map(find_mapping, all_inputs)
numbers = starmap(decode_outputs, zip(all_outputs, mappings))

print("Solution:", sum(numbers))
