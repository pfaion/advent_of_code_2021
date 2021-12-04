#!/usr/bin/env python

from os import read
from pathlib import Path
import subprocess


here = Path(__file__).parent

for folder in here.glob("day*"):
    try:
        # load data
        part1 = (folder / "part1.html").read_text()
        solution1 = folder / "solution1.py"
        code1 = solution1.read_text()
        result1 = subprocess.check_output(
            f"/usr/bin/env python {solution1}", shell=True, encoding="utf-8"
        )
        part2 = (folder / "part2.html").read_text()
        solution2 = folder / "solution2.py"
        code2 = solution2.read_text()
        result2 = subprocess.check_output(
            f"/usr/bin/env python {solution2}", shell=True, encoding="utf-8"
        )
        # write data
        readme = folder / "README.md"
        readme.write_text(
            "\n\n".join(
                (
                    part1,
                    "## Solution 1",
                    "```python",
                    code1,
                    "```",
                    result1,
                    part2,
                    "## Solution 2",
                    "```python",
                    code2,
                    "```",
                    result2,
                )
            )
        )
    except Exception:
        continue
