from pathlib import Path
from statistics import mode
from typing import List

# load data
data_file = Path(__file__).with_name("data.txt")
diagnostics = data_file.read_text().splitlines()

# since we need similar behavior for both ratings, encapsulate that in function
def find_rating(diagnostics: List[str], *, use_most_common: bool) -> int:

    # copy list since we need to remove values
    diagnostics = list(diagnostics)

    # we potentially need to look at all bit positions
    n_bits = len(diagnostics[0])
    for bit_position in range(n_bits):
        bit_column = [val[bit_position] for val in diagnostics]

        # cound most and least common for current bit position from remaining (!) values
        counts = [bit_column.count(val) for val in ("0", "1")]
        most_common = "1" if counts[1] >= counts[0] else "0"
        least_common = "0" if most_common == "1" else "1"
        target_bit = most_common if use_most_common else least_common

        # filter values based on target value for current bit position
        diagnostics = [val for val in diagnostics if val[bit_position] == target_bit]
        if len(diagnostics) == 1:
            return int(diagnostics[0], 2)


oxygen_rating = find_rating(diagnostics, use_most_common=True)
co2_rating = find_rating(diagnostics, use_most_common=False)

print("Solution:", oxygen_rating * co2_rating)
