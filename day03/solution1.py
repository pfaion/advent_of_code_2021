from pathlib import Path
from statistics import mode

# load data
data_file = Path(__file__).with_name("data.txt")
diagnostics = data_file.read_text().splitlines()

# tranform rows to columns
bit_columns = zip(*diagnostics)

# apply simple statistics (turn into strings)
most_common = "".join(map(mode, bit_columns))
least_common = "".join(map(lambda bit: "0" if bit == "1" else "1", most_common))

# turn into numbers
gamma_rate = int(most_common, 2)
epsilon_rate = int(least_common, 2)

print("Solution:", gamma_rate * epsilon_rate)
