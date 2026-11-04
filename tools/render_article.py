#!/usr/bin/env python3
"""Write the offline revised article and bundled downloads inside tmp/docs."""
from pathlib import Path
from html import escape
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
ARCHIVE = ROOT.parent / 'archive/pdf/1984-12/packages/crowded-speedway-complete-r01'
for directory in ['images', 'downloads', 'source/src', 'source/tools', 'reference']:
    (DOCS / directory).mkdir(parents=True, exist_ok=True)

for src, dst in [
    (ROOT/'final-title.png', DOCS/'images/title.png'),
    (ROOT/'final-gameplay.png', DOCS/'images/gameplay.png'),
    (ARCHIVE/'segments/opening/ocr-page90/p88-screenshot.png', DOCS/'images/1984-start.png'),
    (ROOT/'build/speedway.dsk', DOCS/'downloads/speedway.dsk'),
    (ARCHIVE/'article.txt', DOCS/'reference/original-article.txt'),
    (ROOT/'speedway-verification.json', DOCS/'reference/runtime-verification.json'),
    (ROOT/'build/verification.json', DOCS/'reference/build-verification.json'),
    (ROOT/'DISASSEMBLY.md', DOCS/'reference/disassembly-notes.md'),
]:
    shutil.copy2(src, dst)

files = [Path('Makefile')] + sorted(Path('src')/p.name for p in (ROOT/'src').iterdir() if p.is_file())
files += [Path('tools/package_disk.py'), Path('tools/verify_build.py')]
for path in files:
    target = DOCS/'source'/path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT/path, target)

readme = '''Crowded Speedway — repaired ca65 source edition\n\nRequirements: GNU Make, ca65 and ld65 from cc65, Python 3, a2kit.\nRun make in this directory. Output: build/speedway.dsk.\nRun make verify to compare against the bundled repaired references.\nRun make clean to remove build/ only.\n\nEdit src/speedway.s, src/loader.s, and the data includes.\nNormal builds do not read the reference dump, BASIC listing, or disk.\nThe BASIC DATA line is generated from the assembled relocation loader.\nAddresses are fixed; assertions reject layout drift.\n\nThe disk boots automatically. Use paddle 0 and button 0. Neutral is 48–79\n(raw PDL value), approximately 64. Normal Apple II speed is expected.\n\nThis is a November 2026 scratch reconstruction of the December 1984 article.\nSource labels/comments are recovered explanations, not original author labels.\nThe two earlier runtime repairs are included; no further gameplay changes.\nThe original archive remains unchanged.\n'''
(DOCS/'source/README.txt').write_text(readme)
zip_entries = {str(path): (ROOT/path).read_bytes() for path in files}
zip_entries['README.txt'] = readme.encode()
for name in ['crowded speed way.hex', 'speedway-run.bas', 'speedway.dsk']:
    zip_entries[name] = (ROOT/name).read_bytes()
with zipfile.ZipFile(DOCS/'downloads/crowded-speedway-source.zip', 'w', zipfile.ZIP_DEFLATED) as out:
    for name, data in sorted(zip_entries.items()):
        info = zipfile.ZipInfo('crowded-speedway/'+name, date_time=(2026,11,4,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        out.writestr(info, data)


def pre(text):
    return '<pre><code>'+escape(text.rstrip())+'</code></pre>'


def source(name):
    return (ROOT/name).read_text()


def routine(label, end):
    text = source('src/speedway.s')
    body = text[text.index(label+':'):text.index(end+':')]
    body = body.split('; Retained bytes')[0]
    result = []
    for line in body.splitlines():
        if '.assert ' in line:
            continue
        # Article excerpts keep labels/instructions; full appendix retains annotations.
        if not line.strip().startswith(';'):
            result.append(line.split(';')[0].rstrip())
    return '\n'.join(result).strip()

appendix = []
for name, title in [('src/speedway.s','Complete annotated game disassembly'),
                    ('src/memory.inc','Zero-page variables, hardware, and ROM symbols'),
                    ('src/loader.s','Complete relocation loader'),
                    ('src/speedway.cfg','Game linker configuration'),
                    ('src/loader.cfg','Loader linker configuration')]:
    appendix.append(f'<details id="file-{Path(name).name.replace(chr(46),chr(45))}"><summary>{escape(title)} — {escape(name)}</summary>'
                    f'<p><a href="source/{name}" download>Download this file</a></p>{pre(source(name))}</details>')
appendix.append('<h3>Graphics, HUD, and retained data</h3><p>These are the exact byte declarations used by the assembler. Screen holes, row terminators, and unused tails are retained.</p>')
for path in sorted((ROOT/'src').glob('*.inc')):
    if path.name == 'memory.inc':
        continue
    appendix.append(f'<details><summary>{escape(path.name)}</summary><p><a href="source/src/{path.name}" download>Download this include</a></p>{pre(path.read_text())}</details>')
appendix.append('<h3>Packaging and verification scripts</h3>')
for name in ['tools/package_disk.py','tools/verify_build.py']:
    appendix.append(f'<details><summary>{escape(name)}</summary>{pre(source(name))}</details>')

manifest = json.loads((ROOT/'build/manifest.json').read_text())
page = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Crowded Speedway from the December 1984 issue: a revised Apple II article with screenshots, repaired ca65 source, and a reproducible DOS 3.3 disk build.">
<title>Crowded Speedway — December 1984, revisited</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { max-width: 960px; margin: 2.5rem auto; padding: 0 1.4rem; color: #202020; background: #fff; font: 18px/1.65 Georgia, "Times New Roman", serif; }
  a { color: #145d37; text-underline-offset: .15em; }
  a:hover { color: #08351c; }
  a:focus-visible, summary:focus-visible { outline: 2px solid #145d37; outline-offset: 4px; }
  header { border-top: 4px solid #145d37; padding-top: 1rem; }
  .issue, .byline, figcaption, footer { font-size: .88rem; color: #505050; }
  .issue { letter-spacing: .08em; text-transform: uppercase; margin: 0; }
  h1 { font-size: clamp(2.3rem, 7vw, 4rem); line-height: 1.05; margin: .65rem 0; font-weight: normal; }
  .subtitle { font-size: 1.3rem; margin: 0 0 1rem; }
  h2 { margin: 2.8rem 0 1rem; padding-top: .6rem; border-top: 1px solid #c8c8c8; line-height: 1.3; }
  h3 { margin: 1.8rem 0 .6rem; line-height: 1.4; }
  p { margin: .8rem 0; }
  .lead { font-size: 1.15rem; }
  nav { margin: 1.6rem 0; }
  nav ul { padding-left: 1.4rem; columns: 2; column-gap: 2rem; }
  nav li { break-inside: avoid; }
  figure { margin: 1.5rem 0; }
  .lead-image { max-width: 640px; margin: 1.7rem auto; }
  .screen { aspect-ratio: 35 / 24; background: #000; }
  .screen img { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
  .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; align-items: start; }
  .pair figure { margin: .6rem 0; }
  .scan { width: 100%; height: auto; display: block; }
  figcaption { line-height: 1.45; margin-top: .65rem; }
  code, pre { font-family: "Courier New", Courier, monospace; font-size: .88em; }
  pre { overflow: auto; padding: 1rem; background: #f4f4f1; border-left: 3px solid #b5c4b8; line-height: 1.5; tab-size: 4; }
  pre code { font-size: 1em; }
  details { border-top: 1px solid #ddd; padding: .8rem 0; }
  details pre { max-height: 36rem; font-size: .76rem; }
  summary { cursor: pointer; font-weight: bold; }
  .table-wrap { overflow-x: auto; margin: 1rem 0; }
  table { width: 100%; border-collapse: collapse; font-size: .92em; }
  th, td { padding: .55rem .7rem; text-align: left; vertical-align: top; border-bottom: 1px solid #ddd; }
  th { border-bottom: 2px solid #777; }
  blockquote { border-left: 3px solid #ccc; margin: 1.2rem 0; padding-left: 1.2rem; }
  .note { padding-left: 1rem; border-left: 3px solid #145d37; }
  .hash { overflow-wrap: anywhere; }
  footer { border-top: 1px solid #aaa; margin-top: 3rem; padding-top: 1rem; }
  @media (max-width: 600px) { body { margin: 1rem auto; padding: 0 1rem; font-size: 17px; } .pair { grid-template-columns: 1fr; } nav ul { columns: 1; } pre { padding: .75rem; } }
  @media print { body { max-width: none; margin: 0; font-size: 11pt; } a { color: inherit; } nav { display: none; } h2, h3 { break-after: avoid; } figure, tr { break-inside: avoid; } pre { white-space: pre-wrap; overflow-wrap: anywhere; } }
</style>
</head>
<body>
<header id="top">
<p class="issue">December 1984 · Apple II · pp. 88–97</p>
<h1>Crowded Speedway</h1>
<p class="subtitle">A magazine listing, back on the road.</p>
<p class="byline">Original title: <span lang="ko">크라우디드 스피드 웨이</span><br>
Original credit: <span lang="ko">편집부 편역</span> — editorial translation and adaptation.<br>
Revised English edition with recovered source and build notes · 4 November 2026</p>
<p class="lead">A road full of cars, a paddle in your hand, and one brake you cannot afford to burn out. This December 1984 Apple II game makes a convincing race from low-resolution graphics. Here is the article revisited, with a working disk, fresh screenshots, and assembly source you can build with the cc65 tools.</p>
<figure class="lead-image">
<div class="screen"><img src="images/gameplay.png" width="560" height="192" alt="Crowded Speedway running in MAME: a winding grey road, green roadside scenery, the player's car, and score text below."></div>
<figcaption>On the road again. A capture from the repaired program running on MAME’s unenhanced Apple IIe. The raw 560 × 192 capture is displayed with doubled vertical scale.</figcaption>
</figure>
<p class="downloads"><a href="downloads/speedway.dsk" download>Download the bootable disk</a> · <a href="downloads/crowded-speedway-source.zip" download>Download the complete source package</a></p>
</header>
<nav aria-label="Article contents">
<ul>
<li><a href="#race">1. The race</a></li>
<li><a href="#run">2. Run it on an Apple II</a></li>
<li><a href="#machine">3. How the program works</a></li>
<li><a href="#repairs">4. From printed bytes to working code</a></li>
<li><a href="#build">5. Build it with cc65</a></li>
<li><a href="#reading">6. Reading the disassembly</a></li>
<li><a href="#checks">7. What has been verified</a></li>
<li><a href="#source">8. Complete source listings</a></li>
<li><a href="#provenance">Sources and editorial notes</a></li>
</ul>
</nav>
<main>
<article>
<section id="race">
<h2>1. The race</h2>
<p>The original editors describe a race around Jeju Island, with Hallasan in the background. The highway is crowded: cars approach along the road, large signs loom at its edges, and a sharp curve can suddenly leave the car badly placed. The scenery moves with the road and your steering, helping a small block-graphics display feel like a much wider world.</p>
<p>You need paddle 0 or the horizontal axis of an Apple II joystick. Press button 0 at the title screen to begin. During the race, that same button is the brake. Use it in short bursts to make room among the traffic. Keep it held down and the brake will burn out; it then stays unusable for the rest of the game.</p>
<p>The score rises as you drive and stops rising while the working brake is held. You have ten cars to use up. After a collision the program flashes an explosion, reduces the allowance, and puts you back on the road. At game over it compares the score with the high score, then lets you start again.</p>
<div class="pair">
<figure>
<img class="scan" src="images/1984-start.png" width="839" height="570" alt="The original magazine's black-and-white photograph of the game: START above a chequered starting line." loading="lazy">
<figcaption>The starting line as photographed in the December 1984 article, printed page 88. This is a scan crop from the restored source.</figcaption>
</figure>
<figure>
<div class="screen"><img src="images/title.png" width="560" height="192" alt="The repaired game's colour title screen reading CROWDED SPEED WAY, with PUSH SW0 below." loading="lazy"></div>
<figcaption>The repaired game’s title screen in MAME. “PUSH SW0” means paddle/joystick button 0. As above, the capture is displayed at twice its raw vertical scale.</figcaption>
</figure>
</div>
<p>The 1984 article credits an earlier appearance in the January 1983 issue of Japan’s <cite>ASCII</cite>. That attribution is reported here from the Korean article; the earlier Japanese publication has not been independently checked for this edition.</p>
</section>
<section id="run">
<h2>2. Run it on an Apple II</h2>
<p>The supplied image is a bootable 140 KB DOS 3.3 disk in DOS sector order. Mount it as drive 1 and boot. Its <code>HELLO</code> program automatically runs <code>SPEEDWAY-RUN</code>. If DOS is already running with the disk mounted, enter:</p>
@@RUN@@
<p>Use an Apple II with Applesoft ROMs and at least 48 KB of RAM: an II+, IIe, or compatible machine. Run at normal Apple II speed, about 1 MHz. On a real machine, transfer the image to a 5.25-inch floppy or use a compatible disk-image interface; placing a <code>.dsk</code> file inside a DOS filesystem does not turn it into a boot disk.</p>
<p class="note"><strong>Check the paddle’s centre.</strong> The original code regards raw paddle readings 48–79 as neutral, with 64 a useful target. Lower values steer left; higher values steer right. An emulator that centres the input at 128 will pull right continuously. Adjust the emulated paddle position or range, or the physical joystick’s trim.</p>
<p>The brief orchard picture at startup belongs to the program: the loader copies it into screen memory, waits, and then starts the game. The move also overwrites Applesoft’s program area. A reset does not leave the BASIC listing intact; reboot to start cleanly.</p>
</section>
<section id="machine">
<h2>3. How the program works</h2>
<h3>Low resolution, a wide road</h3>
<p>The article makes a point of using <code>GR</code> rather than high-resolution graphics. In mixed mode the Apple II gives it a 40 × 40 graphics area with four text lines below. Most of the convincing depth comes from the arrangement of the data and the way it is copied.</p>
<p>At startup the program calculates perspective and lane tables in <code>$4000–$53FF</code>. During play it builds twenty separate 256-byte rows in <code>$6000–$73FF</code>. The road is a span of <code>$AA</code> bytes on a <code>$CC</code> background. Traffic, signs, and the player’s car are added to those rows before a 40-column window is copied to the display.</p>
<p>Each lores display byte contains two vertically adjacent colour pixels. The road blitter combines the low nibble of one row buffer with the high nibble of the next, then writes to the Apple II’s interleaved screen addresses. Ten separate 256-byte scenery strips provide the horizon and roadside view. Moving their source index makes the landscape scroll.</p>
<h3>The game loop</h3>
<p>The recovered loop is short enough to show the order of work. Collision is tested before the player’s car is drawn, so the car’s own pixels do not become obstacles. The road and scenery are copied to the screen only after the row buffers are ready.</p>
@@LOOP@@
<p>At <code>update_brake</code>, a working brake subtracts one from the text-based score. The unconditional increment at the end of the loop adds it back, cancelling the usual increase. Score digits are high-bit Apple II characters, not packed BCD.</p>
<h3>Where the program lives</h3>
<div class="table-wrap"><table>
<caption>Selected runtime regions after relocation</caption>
<thead><tr><th scope="col">Address</th><th scope="col">Use</th></tr></thead>
<tbody>
<tr><td><code>$0300–$032B</code></td><td>The 44-byte relocation and delay stub.</td></tr>
<tr><td><code>$0400–$07FF</code></td><td>The initial orchard page, then the live screen.</td></tr>
<tr><td><code>$0800–$0FFF</code></td><td>Math, road/traffic routines, sprites, input, and blitters.</td></tr>
<tr><td><code>$1000–$19FF</code></td><td>Ten horizontal scenery strips.</td></tr>
<tr><td><code>$1A00–$1FFF</code></td><td>Steering, player/crash sprites, brake, main loop, HUD, and data.</td></tr>
<tr><td><code>$2000–$27FF</code></td><td>Game-over and title-screen pages.</td></tr>
<tr><td><code>$2800–$29FF</code></td><td>Start overlay, signals, sounds, initialization, and restart.</td></tr>
<tr><td><code>$4000–$53FF</code></td><td>Generated perspective and lane tables.</td></tr>
<tr><td><code>$6000–$73FF</code></td><td>Generated road/object row buffers.</td></tr>
</tbody></table></div>
<p>The important zero-page variables are named in <a href="source/src/memory.inc"><code>memory.inc</code></a>: curvature at <code>$00</code>, signed viewport offset at <code>$01</code>, scenery index at <code>$09</code>, road-section state at <code>$0A–$0D</code>, and brake state at <code>$0E–$10</code>. The two traffic cars use state at <code>$60–$68</code> and <code>$90–$98</code>; the signs use <code>$70–$75</code> and <code>$80–$85</code>.</p>
</section>
<section id="repairs">
<h2>4. From printed bytes to working code</h2>
<p>The original procedure was to type an Applesoft loader, enter the long machine-code listing through the monitor, and save the payload at <code>$4400</code>. The restored article preserves what the pages say. A runnable edition needs a separate record of corrections, because a faithful transcription and a working program are different checks.</p>
<div class="table-wrap"><table>
<caption>Corrections included in this runnable edition</caption>
<thead><tr><th scope="col">Location</th><th scope="col">Change</th><th scope="col">Reason</th></tr></thead>
<tbody>
<tr><td>Dump <code>$4BA0–$50AF</code></td><td>Restore 162 omitted rows.</td><td>The extracted hex file skipped 1,296 bytes. The supplied disk had 1,183 incorrect bytes in that range, including code and graphics.</td></tr>
<tr><td>Dump <code>$4993</code><br>Runtime <code>$0993</code></td><td><code>44 → A4</code></td><td>Restore <code>LDY $00</code> before the road-position lookup.</td></tr>
<tr><td>Dump <code>$4F56</code><br>Runtime <code>$0F56</code></td><td><code>0B → 08</code></td><td>Call the random routine at <code>$08F0</code>, rather than sprite data at <code>$0BF0</code>.</td></tr>
<tr><td>Applesoft DATA loader</td><td>End the move at <code>$69FF</code>.</td><td>ROM MOVE uses an inclusive end. The printed <code>$6A00</code> endpoint copied one extra byte.</td></tr>
<tr><td>Disk startup</td><td>Add <code>HELLO</code> and an explicit PRINT separator.</td><td>The packaged disk boots directly into the repaired loader.</td></tr>
</tbody></table></div>
<p><strong>A note on the printed extra-cars tip.</strong> The article suggests changing the byte at <code>$5CD0</code> to an INC instruction. In this dump, that address contains crash-picture data. The actual decrement is at runtime <code>$1DC0</code>, corresponding to dump address <code>$5DC0</code>. This edition preserves the ten-car logic and does not claim to validate the printed extended-play modification.</p>
<p>The original filename spellings and uncertain source readings remain in the <a href="reference/original-article.txt" hreflang="ko">restored Korean article and hex listing</a>. This revised page consistently uses the working filenames <code>SPEEDWAY-RUN</code> and <code>CROWDED SPEED WAY</code>.</p>
</section>
<section id="build">
<h2>5. Build it with cc65</h2>
<p>The modern version uses two tools from the cc65 suite: <strong>ca65</strong> assembles the 6502 source and <strong>ld65</strong> links it at its runtime addresses. No C compiler or C runtime is involved. Python 3 and <strong>a2kit</strong> generate the BASIC DATA line, tokenize the BASIC programs, and construct a fresh bootable DOS 3.3 disk.</p>
<p>Install GNU Make, ca65/ld65, Python 3, and a2kit so their executables are on your PATH. The build was verified with cc65 V2.19 (git a162565ec) and a2kit 4.4.2. Download <a href="downloads/crowded-speedway-source.zip" download>the source package</a>, then:</p>
@@PORTABLE_BUILD@@
<p>The result is <code>build/speedway.dsk</code>. The archive includes repaired comparison files for <code>make verify</code>. The normal <code>make</code> target builds from <code>Makefile</code>, <code>src/</code>, and <code>tools/</code> alone; it does not extract an old binary or copy a base game disk. a2kit supplies the DOS boot tracks.</p>
<p>In the original scratch workspace, the equivalent commands are:</p>
@@WORKSPACE_BUILD@@
<p><code>make clean</code> removes only the project’s <code>build/</code> directory. <code>make binary</code> assembles the game and loader without packaging a disk. Executable paths can be overridden, for example <code>make CA65=/path/to/ca65</code>.</p>
<h3>The Makefile</h3>
<p>The BASIC DATA line is generated from the assembled <code>loader.bin</code>. Editing the loader’s assembly therefore changes the bytes that BASIC installs; there is no second hand-maintained byte list to keep in sync.</p>
<details><summary>Complete Makefile</summary>
@@MAKEFILE@@
</details>
<p><a href="source/Makefile" download>Download Makefile</a> · <a href="source/tools/package_disk.py" download>Disk packager</a> · <a href="source/tools/verify_build.py" download>Reference verifier</a></p>
</section>
<section id="reading">
<h2>6. Reading the disassembly</h2>
<h3>Assemble for the address where the code will run</h3>
<p>The payload is loaded at <code>$4400–$69FF</code>, but executed at <code>$0400–$29FF</code>. All source labels, branches, and absolute references use the second range. Add <code>$4000</code> to a runtime address to find its byte in the monitor dump.</p>
@@LINKER@@
<p>The separate loader at <code>$0300</code> sets the monitor’s source, end, and destination pointers, calls MOVE at <code>$FE2C</code>, delays, and jumps to <code>game_entry</code> at <code>$2970</code>. Its complete source appears below. The raw payload is not meant to be BRUN at its staging address.</p>
<h3>Code where there is code; bytes where there are pictures</h3>
<p>Following calls, jumps, branches, and fallthrough from <code>$2970</code> identifies <strong>1,281 reachable instructions occupying 2,673 bytes</strong>. Another 11 bytes are two unreferenced instruction fragments. The remaining 7,044 bytes are retained data and padding. The source therefore does not mistake rows of scenery pixels for executable opcodes.</p>
<p>Medium and large traffic sprites use <code>$FF</code> row terminators. Player sprites use zero for transparency. Title and game-over images retain every byte of their 1 KB page layouts, including screen holes. These live in readable <code>.byte</code> includes; the build has no <code>INCBIN</code> dependency.</p>
<h3>A crash is a nonlocal jump</h3>
<p>The collision checker is called with JSR, but on a collision it jumps directly to <code>handle_crash</code>. The handler starts with two PLA instructions to remove that return address from the stack. After the animation it continues into the next-car path. Rewriting it as an ordinary returning subroutine would change the program’s control flow.</p>
@@CRASH@@
<h3>What the comments do—and do not—claim</h3>
<p>Names such as <code>draw_road</code> and <code>update_brake</code> describe recovered behavior, not original author labels. Uncertain visual details are identified as such. The source also preserves an unusual CMP/STA sequence in the first traffic car’s lookup setup at <code>$0A0A–$0A0D</code>, and labels two unreferenced fragments at <code>$09AB–$09B2</code> and <code>$295F–$2961</code>. This disassembly adds no further gameplay repairs.</p>
<p>Address assertions keep the fixed layout honest. Same-size instruction and data edits are straightforward; inserting bytes requires accommodating them in padding and checking the fixed-address assumptions. The source’s address/byte comments describe the baseline.</p>
</section>
<section id="checks">
<h2>7. What has been verified</h2>
<ul>
<li>The assembled 9,728-byte payload matches all 1,216 rows of the corrected monitor dump.</li>
<li>The assembled 44-byte stub matches the repaired BASIC DATA line, and the generated BASIC listing is identical.</li>
<li>The entire rebuilt 143,360-byte disk matches the working repaired disk, including its filesystem layout.</li>
<li>Two separate clean source-only builds produced the same disk. A one-byte source-edit probe reached both the binary and the disk; the baseline was restored afterward.</li>
<li>The repaired disk booted automatically in Apple2TS. In MAME 0.285 on an unenhanced IIe, 575 gameplay updates exercised both steering directions, curves, braking, brake burnout, ten collisions, and game over. Restart preserved the high score, followed by another 80 gameplay updates.</li>
</ul>
<p>The disassembly build reproduces that exact disk, so it reuses the earlier emulator results. No new emulator run was performed for the source reconstruction or this HTML edition, and a physical-machine test is not claimed.</p>
<p><a href="reference/build-verification.json">Build comparison results</a> · <a href="reference/runtime-verification.json">Runtime test results</a></p>
<p class="hash"><strong>Disk SHA-256:</strong><br><code>@@DISK_HASH@@</code></p>
</section>
<section id="source">
<h2>8. Complete source listings</h2>
<p>Open a listing to read it here, or download the complete package with all includes, linker configurations, Makefile, BASIC template, and packaging scripts. Everything on this page works from local files: no JavaScript, web fonts, or external assets are required.</p>
<p><a href="downloads/crowded-speedway-source.zip" download>Complete source ZIP</a> · <a href="source/src/coverage.json">Routine and coverage index</a> · <a href="reference/disassembly-notes.md">Detailed reconstruction notes</a></p>
@@APPENDIX@@
<h3>Applesoft startup</h3>
<p>This is the repaired loader generated by the build. Its DATA bytes come from <code>src/loader.s</code>; the editable template is <a href="source/src/speedway-run.bas.in" download><code>speedway-run.bas.in</code></a>. The boot program is <a href="source/src/hello.bas" download><code>HELLO</code></a>.</p>
@@BASIC@@
</section>
<section id="provenance">
<h2>Sources and editorial notes</h2>
<p>This is a revised English reading and programming edition of the December 1984 article, printed pages 88–97, based on the existing restoration. The original title, editorial credit, rules, GR explanation, two-listing workflow, and earlier Japanese attribution come from that source. The page replaces the long monitor-type-in presentation with a repaired, annotated ca65 reconstruction and a reproducible build.</p>
<p>The magazine image above is a crop from printed page 88. The two colour captures come from the repaired program running in MAME. Their vertical display scale is corrected in the page layout; the original PNG files are unchanged. Modern source comments, repair notes, memory labels, test results, and build instructions are editorial additions.</p>
<p><a href="reference/original-article.txt" hreflang="ko">Original restored Korean article and listings</a> · <a href="images/title.png">Raw title capture</a> · <a href="images/gameplay.png">Raw gameplay capture</a></p>
<p>The archive itself remains unchanged. This edition and its bundled files are confined to <code>tmp/docs/</code>.</p>
</section>
</article>
</main>
<footer><p>Crowded Speedway · December 1984 / revised 2026 · <a href="#top">Back to the top</a></p></footer>
</body>
</html>
'''
replacements = {
    'RUN': pre('RUN SPEEDWAY-RUN'),
    'LOOP': pre(routine('game_loop','game_over')),
    'PORTABLE_BUILD': pre('unzip crowded-speedway-source.zip\ncd crowded-speedway\nmake\nmake verify'),
    'WORKSPACE_BUILD': pre('make -C tmp\nmake -C tmp verify\n# Output: tmp/build/speedway.dsk'),
    'MAKEFILE': pre(source('Makefile')),
    'LINKER': pre(source('src/speedway.cfg')),
    'CRASH': pre('check_player_collision:\n        ; ... test the player footprint ...\n        jmp     handle_crash\n\nhandle_crash:\n        pla     ; discard collision checker return address, low byte\n        pla     ; discard high byte\n        ; ... draw crash frames and delay ...\n        jmp     lose_car_and_restart'),
    'DISK_HASH': escape(manifest['disk_sha256']),
    'APPENDIX': '\n'.join(appendix),
    'BASIC': pre(source('build/speedway-run.bas')),
}
for key,value in replacements.items():
    token='@@'+key+'@@'
    if page.count(token)!=1:
        raise ValueError(f'Expected one occurrence of {token}')
    page=page.replace(token,value)
(DOCS/'index.html').write_text(page)
# This is a portable snapshot: all local links must stay inside docs/.
checksums={str(path.relative_to(DOCS)):hashlib.sha256(path.read_bytes()).hexdigest()
           for path in sorted(DOCS.rglob('*')) if path.is_file() and path.name!='checksums.json'}
(DOCS/'checksums.json').write_text(json.dumps(checksums,indent=2)+'\n')
print(f'Wrote {DOCS / "index.html"} ({len(page.encode()):,} bytes) and {len(checksums)-1} supporting files.')
