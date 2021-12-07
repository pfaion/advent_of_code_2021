from pathlib import Path
from statistics import median

# load data
data_file = Path(__file__).with_name("data.txt")
positions = [int(v) for v in data_file.read_text().strip().split(",")]

# median minimizes the sum absolute differences
target = median(positions)
fuel_required = int(sum(abs(pos - target) for pos in positions))

print("Solution:", fuel_required)
