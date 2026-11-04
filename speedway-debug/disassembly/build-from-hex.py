#!/usr/bin/env python3
"""Build the scratch DOS 3.3 disk; all outputs stay beside this script."""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent


def a2kit(*args, data=None):
    return subprocess.run(
        ["a2kit", *map(str, args)], input=data, check=True,
        stdout=subprocess.PIPE,
    ).stdout


def main():
    payload = bytearray()
    for line in (ROOT / "crowded speed way.hex").read_text().splitlines():
        match = re.fullmatch(r"([0-9A-F]{4}):((?: [0-9A-F]{2}){8})", line)
        if not match:
            raise ValueError(f"Malformed monitor row: {line!r}")
        address = int(match[1], 16)
        if address != 0x4400 + len(payload):
            raise ValueError(f"Missing, duplicate, or unordered row at ${address:04X}")
        payload.extend(bytes.fromhex(match[2]))
    assert len(payload) == 0x2600, "Expected exactly $4400-$69FF"
    (ROOT / "crowded speed way.bin").write_bytes(payload)
    with tempfile.TemporaryDirectory(prefix="speedway-build-", dir=ROOT) as work:
        disk = Path(work) / "speedway.dsk"
        a2kit("mkdsk", "-o", "dos33", "-v", "254", "-t", "do", "-b", "-d", disk)
        for source, name in [("hello.bas", "HELLO"), ("speedway-run.bas", "SPEEDWAY-RUN")]:
            tokens = a2kit("tokenize", "-a", "2049", "-t", "atxt", data=(ROOT / source).read_bytes())
            a2kit("put", "-d", disk, "-f", name, "-t", "atok", "-a", "2049", data=tokens)
        a2kit("put", "-d", disk, "-f", "CROWDED SPEED WAY", "-t", "bin", "-a", "17408", data=payload)
        extracted = a2kit("get", "-d", disk, "-f", "CROWDED SPEED WAY", "-t", "bin")
        assert extracted == payload, "Disk binary differs from corrected source"
        assert disk.stat().st_size == 143360
        disk.replace(ROOT / "speedway.dsk")
    print(a2kit("catalog", "-d", ROOT / "speedway.dsk").decode(), end="")
    print("Verified: 1,216 contiguous rows, 9,728 payload bytes, exact disk round trip.")


if __name__ == "__main__":
    main()
