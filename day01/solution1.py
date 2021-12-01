from pathlib import Path
from typing import Any, Iterable, Iterator, Tuple

data_file = Path(__file__).parent / "input.txt"
data = [int(line.strip()) for line in data_file.read_text().splitlines()]


def pairwise(data: Iterable) -> Iterator[Tuple[Any, Any]]:
    input_iterator = iter(data)
    prev = next(input_iterator)
    for current in input_iterator:
        yield prev, current
        prev = current


num_increments = 0
for a, b in pairwise(data):
    if b > a:
        num_increments += 1

print(num_increments)
