from collections import defaultdict
from pathlib import Path

# load
data = Path(__file__).with_name("data.txt").read_text().splitlines()

# parse
algorithm = data[0].translate(str.maketrans({".": "0", "#": "1"}))
image_raw = data[2:]
image = defaultdict(lambda: "0")
row_min, col_min, row_max, col_max = (0, 0, len(image_raw) - 1, len(image_raw[0]) - 1)
for r, row in enumerate(image_raw):
    for c, val in enumerate(row):
        image[(r, c)] = "0" if val == "." else "1"

# process
offsets = (-1, 0, 1)
for step in range(2):

    # expand image range
    row_min -= 1
    col_min -= 1
    row_max += 1
    col_max += 1

    # important: the infinite area might change as well, just change default value
    inf_area = image.default_factory() * 9
    index = int(inf_area, 2)
    new_default = algorithm[index]
    new_image = defaultdict(lambda d=new_default: d)

    # map all other (non infinite) pixels
    for r in range(row_min, row_max + 1):
        for c in range(col_min, col_max + 1):
            batch = "".join(image[(r + i, c + j)] for i in offsets for j in offsets)
            index = int(batch, 2)
            new_image[(r, c)] = algorithm[index]

    image = new_image

n_lit = len([v for v in image.values() if v == "1"])
print("Solution", n_lit)
