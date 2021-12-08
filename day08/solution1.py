from pathlib import Path
from itertools import chain

# load data
data_file = Path(__file__).with_name("data.txt")
data = data_file.read_text().splitlines()

# parse data
outputs = [line.split(" | ")[1].split() for line in data]
outputs_flat = chain.from_iterable(outputs)

unique_lengths = {2, 3, 4, 7}
n_unique_outputs = len(
    [entry for entry in outputs_flat if len(entry) in unique_lengths]
)

print("Solution:", n_unique_outputs)
