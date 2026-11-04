# Crowded Speedway: ca65 source reconstruction

This reconstructs the repaired, working November 3 scratch version, including
its two earlier machine-code corrections. It does not change the archive.
Recovered names describe behavior inferred from the instructions and consumers;
they are not claimed to be the original author's labels.

## Build and edit

```sh
make -C tmp                  # build/speedway.dsk
make -C tmp binary           # assemble/link the game and relocation loader
make -C tmp verify           # strict comparison against the repaired references
make -C tmp clean            # remove build/ only
```

Tools: GNU Make, ca65/ld65 from cc65, Python 3 standard library, and a2kit.
The tested versions are cc65 V2.19 (git a162565ec) and a2kit 4.4.2. Executable
paths can be overridden, for example `make -C tmp CA65=/path/to/ca65`.

The normal build requires only `Makefile`, `src/`, and `tools/`; these can be
copied to an otherwise empty directory. It does not extract code from the dump,
read an old binary, or copy a base disk. a2kit supplies the bootable DOS 3.3
system tracks. No original DOS source reconstruction is claimed.

`src/speedway.s` is the editable instruction source. Data includes are editable
byte declarations, including all screen holes, delimiters, and retained tails.
The build contains no INCBIN. The prior `.hex`, `.bin`, `.bas`, and `.dsk` files
at the top of `tmp` are comparison references; normal builds leave them alone.
The old Python build entry point now delegates to Make to avoid ignoring source
edits.

Addresses are fixed to preserve the original layout. Assertions catch drift at
routine/data labels and at the payload end. Same-size instruction or data edits
are straightforward. Inserting bytes requires explicitly accommodating them in
the existing padding and updating the relevant fixed-address assumptions.
Address/byte comments describe the baseline and should be updated after edits.

## Loading and runtime map

DOS stores `CROWDED SPEED WAY` as a binary with load address `$4400`, length
`$2600`. Applesoft loads it, installs the 44-byte stub at `$0300`, declares GR,
and calls the stub. ROM MOVE copies `$4400–$69FF` to `$0400–$29FF`, including the
initial screen at `$0400`. After a delay, the stub jumps to `$2970`.

The linker assigns **runtime** addresses, not staging addresses. Add `$4000` to
an address in the annotated source to locate it in the monitor dump. This keeps
all branches, data references, and JSR/JMP operands correct after relocation.
The output is a raw payload; the disk packager adds the DOS BIN header.

| Runtime range | Contents / source |
| --- | --- |
| `$0000–$00A7` (selected bytes) | Game variables; see `src/memory.inc` |
| `$0300–$032B` | Relocation/delay stub, assembled from `src/loader.s` |
| `$0400–$07FF` | Initial orchard screen; later the live lores/text display |
| `$0800–$0ACF` | Math, perspective tables, random stream, road, traffic car 1 |
| `$0AD0–$0BFF` | Traffic sprites, row terminators, retained tail |
| `$0C00–$0E2F` | Left/right signs, traffic car 2, depth-order dispatch, padding |
| `$0E30–$0FFF` | Road/scenery blitters, road segments, paddle input, score |
| `$1000–$19FF` | Ten 256-byte horizontal scenery strips |
| `$1A00–$1ABF` | Curve/steering update and player-car drawing, padding |
| `$1AC0–$1B7F` | Player sprite poses (six rows of three 10-column poses), tail |
| `$1B80–$1CAF` | Cockpit details, brake, score subtraction, collision check |
| `$1CB0–$1D2F` | Two four-row crash pictures |
| `$1D30–$1EAF` | Crash animation, game loop, game over, title wait, HUD |
| `$1EB0–$1FFF` | HUD text and first four rows of start overlay, tail |
| `$2000–$23FF` | Page copied to the display at game over |
| `$2400–$27FF` | Title-screen page |
| `$2800–$287F` | Last three rows of start overlay, tail |
| `$2880–$29FF` | Start overlay/signals/sound, entry, initialization, restart |
| `$4000–$53FF` | Runtime-generated perspective/lane tables; not payload data |
| `$6000–$73FF` | Twenty runtime row buffers; not payload data |

All data ranges retain literal bytes. For example, scenery strips are not
ordinary Apple II screen pages, while the title includes the standard page
layout and holes. No PNG-to-asset conversion or complete visual interpretation
is claimed.

## Main flow and comments

`game_entry` builds perspective/path tables and initializes high score. `new_game`
shows the title and waits for PB0, resets state, renders the start view, and runs
the traffic-light sound/animation. `lose_car_and_restart` turns the HUD's colon
sentinel into digit 9 before the first round.

`game_loop` clears row buffers, updates the road/steering, draws the road, applies
braking, draws traffic in depth order and the signs, checks the player footprint,
draws the car, blits road/scenery, updates cockpit details, paces with speaker
toggles, and increments the score. Braking first subtracts one from the score to
cancel the later increment.

A collision jumps to `handle_crash`, which discards the collision check's JSR
return address with two PLA instructions. It flashes two pictures, delays, and
continues at `lose_car_and_restart`. This is a deliberate nonlocal transfer and
must not be rewritten as a normal returning subroutine. After the last car,
`game_over` saves the score, updates high score when appropriate, and eventually
jumps to `new_game` without clearing it.

The random source reads ROM bytes at `$E000` upward and XORs them with evolving
seed bytes. It is not a conventional LFSR and no uniform distribution is assumed.
Paddle 0 uses ROM PREAD (`$FB1E`), sound/pacing uses WAIT (`$FCA8`), and accesses
to `$C030` toggle the speaker. The original neutral paddle band is 48–79.

Two unreferenced instruction fragments are decoded but explicitly marked:
`$09AB–$09B2` (keyboard read/SPACE compare, with an unusual branch into the road
renderer), and `$295F–$2961` (JMP WAIT). No reachable caller was found for either.
Another suspicious sequence, CMP #$40 / STA at `$0A0A–$0A0D`, is preserved: it
stores depth directly as a lookup high byte, whereas the second car uses ORA
#$40. This task makes no additional gameplay repairs.

## Verification and limits

The payload accounts for 9,728 bytes: 2,673 bytes in 1,281 reachable instructions,
11 bytes in the two retained instruction fragments, and 7,044 bytes of data and
padding. Reachability starts at `$2970` and follows direct calls, jumps, branches,
and fallthrough; it does not imply every path was exercised in an emulator.
`src/coverage.json` records counts and routine descriptions.

`make verify` compares the assembled payload against all 1,216 repaired monitor
rows, compares the assembled stub against BASIC DATA, checks generated BASIC,
and compares every byte of the rebuilt disk against the working disk. Normal
packaging also checks both tokenized BASIC files and the game BIN file, including
load address `$4400` and length `$2600`.

Two separate empty source-only build directories reproduced the same complete
disk. An isolated one-byte source edit was also checked through assembly and disk
packaging. The delivered baseline source remains unchanged by that probe.
Results are in `speedway-debug/disassembly/verification.json`; `make verify`
writes the current baseline-comparison results to `build/verification.json`.

The output matches the exact previously tested disk, reusing its Apple2TS boot
and MAME 6502 gameplay/restart evidence described in `README-speedway.md` and
`speedway-verification.json`. No new emulator session or physical-machine test
was performed for this disassembly task.
