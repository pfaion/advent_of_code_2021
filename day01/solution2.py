from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

data_file = Path(__file__).parent / "input.txt"
data = [int(line.strip()) for line in data_file.read_text().splitlines()]


def sliding_window(data: Iterable, window_size: int) -> Iterator[Sequence]:
    input_iterator = iter(data)
    window = []
    for value in input_iterator:
        window.append(value)
        if len(window) < window_size:
            continue
        yield tuple(window)
        window.pop(0)


sums = [sum(values) for values in sliding_window(data, 3)]
num_increments = sum(1 for a, b in sliding_window(sums, 2) if b > a)

print(num_increments)
