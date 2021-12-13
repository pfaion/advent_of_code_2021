#!/usr/bin/env python

import argparse
import subprocess
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all", action="store_true")
args = parser.parse_args()


def run_timed(path: Path) -> tuple[str, float]:
    t0 = time.perf_counter()
    result = subprocess.check_output(
        f"/usr/bin/env python {path}", shell=True, encoding="utf-8"
    ).strip()
    t1 = time.perf_counter()
    return result, (t1 - t0)


here = Path(__file__).parent

folders = here.glob("day*")
if not args.all:
    folders = [max(folders)]

for folder in folders:
    print(f"Making nice: {folder.name}")
    content = []
    for part in (1, 2):
        html = (folder / f"part{part}.html").read_text()
        content += [
            "<details><summary>Exercise Text (click to expand)</summary>",
            html,
            "</details>",
            f"## Solution {part}",
        ]
        for i, variant in enumerate(sorted(folder.glob(f"solution{part}*.py"))):
            code = variant.read_text()
            result, duration = run_timed(variant)
            content += [
                f"### Variant {i + 1}",
                "```python",
                code,
                "```",
                "```",
                f"Runtime: {duration}",
                result,
                "```",
            ]

    readme = folder / "README.md"
    readme.write_text("\n\n".join(content))
