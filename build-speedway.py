#!/usr/bin/env python3
"""Compatibility entry point: build the ca65 project using its Makefile."""
from pathlib import Path
import subprocess

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    subprocess.run(["make", "-C", str(root), "all"], check=True)
    print(f"Disk image: {root / 'build' / 'speedway.dsk'}")
