# Crowded Speedway — runnable scratch repair

All repairs and test artifacts are confined to `tmp`. The archive has not been
modified. The original three supplied files are backed up in `speedway-originals/`.

## Run

Boot `speedway.dsk` in drive 1. It is a bootable 140 KB DOS 3.3 disk image in
DOS sector order. `HELLO` automatically runs `SPEEDWAY-RUN`.

If DOS is already running, mount the disk and enter:

```text
RUN SPEEDWAY-RUN
```

Use a 48 KB or larger Apple II with Applesoft ROMs (II+, IIe, or compatible),
normal approximately 1 MHz speed, and paddle 0 or the joystick's horizontal axis.
Press button 0 at the title screen to start. The same button brakes during play.
Holding it too long burns out the brake; that is original game behavior.

**Paddle calibration matters:** the original program treats paddle readings
48–79 as neutral, with 64 a useful center. Lower values steer left; higher values
steer right. An emulator centered at 128 will pull continuously right. Adjust its
emulated paddle position/range, or the real joystick's trim, accordingly. These
input thresholds are preserved rather than changing the historical controls.

For a real machine, transfer the image to a 5.25-inch floppy or use a compatible
disk-image interface, then boot it normally. Copying the `.dsk` file into a DOS
filesystem is not a disk transfer. Physical hardware has not been tested here.

## Repairs

- Restored all 162 missing hex rows at `$4BA0–$50A8`, covering bytes
  `$4BA0–$50AF`, from the archive's complete listing. The supplied hex file jumped
  directly from `$4B98` to `$50B0`. The supplied disk had 1,183 incorrect bytes in
  that omitted range, including executable routines and graphics.
- Changed staging `$4993` / runtime `$0993` from `44` to `A4`: `LDY $00` reloads
  the curve index before the road-position lookup.
- Changed staging `$4F56` / runtime `$0F56` from `0B` to `08`: the curve generator
  now calls the random routine at `$08F0`, rather than sprite data at `$0BF0`.
  These two runtime corrections are separate from the archive's literal source.
- Made the loader's inclusive move end at `$69FF`, matching the `$2600`-byte
  payload, instead of copying an extra byte at `$6A00`. Added an explicit PRINT
  separator and the automatic `HELLO` startup file.

The corrected monitor source has 1,216 consecutive eight-byte rows. The raw
`crowded speed way.bin` is 9,728 bytes, loaded at `$4400`; the BASIC loader moves
it to `$0400–$29FF` and enters at `$2970`. Do not BRUN the raw payload at `$4400`.
The game's low-memory relocation intentionally overwrites the BASIC program.
Reboot to run it again after a reset.

## Build the commented ca65 source

With GNU Make, `ca65`, `ld65`, Python 3, and `a2kit` on PATH:

```sh
make -C tmp
make -C tmp verify
```

The resulting disk is **`tmp/build/speedway.dsk`**. `src/speedway.s` contains the
commented disassembly; `src/memory.inc` names hardware and zero-page variables.
Sprite, screen, and HUD bytes live in the adjacent `.inc` files. `src/loader.s`
assembles the relocation stub; its bytes automatically become the BASIC DATA
line. See `DISASSEMBLY.md` for the memory map and source notes.

Normal builds use only `Makefile`, `src/`, and `tools/`. They do not read the hex
dump or an existing disk/binary. `make verify` additionally compares the assembled
payload, loader, generated BASIC, and entire disk against the working repaired
references at the top of `tmp`. Intentional source changes can fail that strict
comparison. Packaging always verifies disk-file payloads and the DOS BIN header.

`make -C tmp clean` removes only `tmp/build`. `python3 tmp/build-speedway.py` is a
compatibility shortcut for the new Makefile and also writes to `tmp/build`.

## Earlier runtime validation

MAME 0.285, unenhanced Apple IIe with a 6502 and emulated joystick: automatic
startup, steering both ways, braking, brake burnout, curve generation, scoring,
ten collisions, and native game over all passed over 575 gameplay loops. The
score reached 448. Restart reset the score and preserved the high score; another
80 gameplay loops passed. No game-code patches were injected by the test adapter.

The final rebuilt disk also cold-booted automatically to the title/button wait
in Apple2TS. `speedway-verification.json` contains hashes and test results.
`final-title.png` and `final-gameplay.png` show the tested program. Investigation
files and emulator receipts are retained in `speedway-debug/`.

The ca65 build reproduces that exact disk, so the existing runtime results also
apply to its unchanged output. No new emulator run was needed for this source
reconstruction. Clean standalone builds and the strict reference comparison are
recorded in `speedway-debug/disassembly/verification.json`. Each `make verify`
also writes `build/verification.json` with the current comparison results.
