from pathlib import Path
from typing import Iterable, List, Iterator, Optional, Set

# load data
data_file = Path(__file__).with_name("data.txt")
data_raw = data_file.read_text().splitlines()

# helper
def batchwise(iterable: Iterable, batch_size: int) -> Iterator:
    args = [iter(iterable)] * batch_size
    return zip(*args)


# board representation
all_indices = list(range(25))
winning_index_sets: List[Set[int]] = []
for row_batch in batchwise(all_indices, 5):
    winning_index_sets.append(set(row_batch))
for col_batch in zip(*batchwise(all_indices, 5)):
    winning_index_sets.append(set(col_batch))


class Board:
    def __init__(self, numbers: List[int]):
        self.numbers = numbers
        self.marked_idxs: Set[int] = set()

    def mark(self, number: int):
        try:
            self.marked_idxs.add(self.numbers.index(number))
        except ValueError:
            pass

    def bingo(self) -> bool:
        return any(winning.issubset(self.marked_idxs) for winning in winning_index_sets)

    def score(self) -> int:
        return sum(
            num for idx, num in enumerate(self.numbers) if idx not in self.marked_idxs
        )


# parse data
number_sequence = map(int, data_raw[0].split(","))
boards: List[Board] = []
for _blank, *rows in batchwise(data_raw[1:], batch_size=6):
    flat = " ".join(rows).split()
    boards.append(Board(numbers=[int(v) for v in flat]))

# simulate game loop
number_generator = iter(number_sequence)
winning_board: Optional[Board] = None
while winning_board is None:
    number = next(number_generator)
    for board in boards:
        board.mark(number)
        if board.bingo():
            winning_board = board
            break

# solution
print("Solution:", winning_board.score() * number)
