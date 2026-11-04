#!/usr/bin/env python3
"""Package assembled raw binaries on a new bootable DOS 3.3 disk."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a2kit", default="a2kit")
    for name in ("payload", "loader", "template", "hello", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()

    def run(*arguments, data=None):
        return subprocess.run([args.a2kit, *map(str, arguments)], input=data,
                              stdout=subprocess.PIPE, check=True).stdout

    payload = args.payload.read_bytes()
    loader = args.loader.read_bytes()
    if len(payload) != 0x2600 or len(loader) != 44:
        raise ValueError("Expected a $2600-byte payload and a 44-byte loader")
    template = args.template.read_text()
    for token in ("@LAST_LOADER_ADDRESS@", "@LOADER_DATA@"):
        if template.count(token) != 1:
            raise ValueError(f"Expected exactly one {token} in BASIC template")
    basic = template.replace("@LAST_LOADER_ADDRESS@", str(768 + len(loader) - 1))
    basic = basic.replace("@LOADER_DATA@", ", ".join(map(str, loader))).encode()
    sources = [("hello", "HELLO", args.hello.read_bytes()),
               ("speedway-run", "SPEEDWAY-RUN", basic)]
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="disk-", dir=args.output.parent) as work:
        disk = Path(work) / "speedway.dsk"
        run("mkdsk", "-o", "dos33", "-v", "254", "-t", "do", "-b", "-d", disk)
        basic_tokens = {}
        for stem, name, text in sources:
            tokens = run("tokenize", "-a", "2049", "-t", "atxt", data=text)
            run("put", "-d", disk, "-f", name, "-t", "atok", "-a", "2049", data=tokens)
            if run("get", "-d", disk, "-f", name, "-t", "atok") != tokens:
                raise ValueError(f"Disk token round trip failed for {name}")
            basic_tokens[stem] = tokens
        run("put", "-d", disk, "-f", "CROWDED SPEED WAY", "-t", "bin", "-a", "17408", data=payload)
        if run("get", "-d", disk, "-f", "CROWDED SPEED WAY", "-t", "bin") != payload:
            raise ValueError("Disk payload round trip failed")
        # Validate the DOS binary load/length header, not just extracted bytes.
        file_image = json.loads(run("get", "-d", disk, "-f", "CROWDED SPEED WAY", "-t", "any"))
        if file_image["fs_type"] != "04" or bytes.fromhex(file_image["chunks"]["0"])[:4] != b"\x00\x44\x00\x26":
            raise ValueError("Incorrect DOS BIN type, load address, or length")
        if disk.stat().st_size != 143360:
            raise ValueError("Expected a 140 KB DOS-order floppy image")
        disk.replace(args.output)

    out = args.output.parent
    (out / "speedway-run.bas").write_bytes(basic)
    for stem, tokens in basic_tokens.items():
        (out / (stem + ".atok")).write_bytes(tokens)
    manifest = {
        "format": "DOS 3.3, 140 KB DOS sector order",
        "load_address": "$4400", "runtime_range": "$0400-$29FF",
        "entry": "$2970", "loader_address": "$0300",
        "payload_bytes": len(payload),
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "loader_sha256": hashlib.sha256(loader).hexdigest(),
        "disk_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
        "disk_round_trip": "passed (BIN header/payload and both BASIC files)",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(run("catalog", "-d", args.output).decode(), end="")
    print(f"Built {args.output}: {len(payload)} assembled payload bytes; all disk files verified.")


if __name__ == "__main__":
    main()
