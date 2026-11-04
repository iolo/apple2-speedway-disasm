#!/usr/bin/env python3
"""Compare the source build with the previously repaired, working artifacts."""
import argparse
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("build", "hex", "basic", "disk"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    reference = bytearray()
    for line in args.hex.read_text().splitlines():
        row = re.fullmatch(r"([0-9A-F]{4}):((?: [0-9A-F]{2}){8})", line)
        if row is None or int(row[1], 16) != 0x4400 + len(reference):
            raise ValueError(f"Malformed or discontinuous reference row: {line!r}")
        reference.extend(bytes.fromhex(row[2]))
    payload = (args.build / "speedway.bin").read_bytes()
    if len(reference) != 0x2600 or payload != reference:
        raise ValueError("Assembled payload differs from repaired hex reference")
    fields = re.search(r"^190\s+DATA\s+(.+)$", args.basic.read_text(), re.MULTILINE)
    if fields is None:
        raise ValueError("Reference BASIC has no line 190 DATA")
    if (args.build / "loader.bin").read_bytes() != bytes(map(int, fields[1].split(","))):
        raise ValueError("Assembled loader differs from repaired BASIC DATA")
    if (args.build / "speedway-run.bas").read_bytes() != args.basic.read_bytes():
        raise ValueError("Generated BASIC differs from repaired loader listing")
    if (args.build / "speedway.dsk").read_bytes() != args.disk.read_bytes():
        raise ValueError("Rebuilt disk differs from the previously working disk")
    print("PASS: assembled payload, 44-byte loader, generated BASIC, and entire disk are byte-identical.")


if __name__ == "__main__":
    main()
