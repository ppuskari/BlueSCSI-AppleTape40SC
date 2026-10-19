#!/usr/bin/env python3
"""Generate a blank experimental 4848-block image, NOT a formatted QIC tape."""
import argparse
from pathlib import Path
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("path", type=Path)
a = p.parse_args()
size = 4848 * 8192
with a.path.open("xb") as output:
    output.truncate(size)
print(f"Created {a.path}: {size} bytes (4848 x 8192)")
