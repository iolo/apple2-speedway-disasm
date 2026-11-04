Crowded Speedway — repaired ca65 source edition

Requirements: GNU Make, ca65 and ld65 from cc65, Python 3, a2kit.
Run make in this directory. Output: build/speedway.dsk.
Run make verify to compare against the bundled repaired references.
Run make clean to remove build/ only.

Edit src/speedway.s, src/loader.s, and the data includes.
Normal builds do not read the reference dump, BASIC listing, or disk.
The BASIC DATA line is generated from the assembled relocation loader.
Addresses are fixed; assertions reject layout drift.

The disk boots automatically. Use paddle 0 and button 0. Neutral is 48–79
(raw PDL value), approximately 64. Normal Apple II speed is expected.

This is a November 2026 scratch reconstruction of the December 1984 article.
Source labels/comments are recovered explanations, not original author labels.
The two earlier runtime repairs are included; no further gameplay changes.
The original archive remains unchanged.
