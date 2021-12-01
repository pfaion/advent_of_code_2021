from pathlib import Path
from typing import Sequence

here = Path(__file__).parent
data_folder = here / "data"


def load_ints(name: str) -> Sequence[int]:
    data_file = data_folder / name
    return [int(line.strip()) for line in data_file.read_text().splitlines()]
