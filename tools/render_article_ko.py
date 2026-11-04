#!/usr/bin/env python3
"""Render the Korean article while preserving all executable source listings."""
from collections import Counter
from html import escape
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
source = (DOCS / "index.html").read_text()
records = json.loads((ROOT / "tools/article.ko.json").read_text())
translations = {}
for record in records:
    old, new = record["source"], record["translation"]
    if old in translations and translations[old] != new:
        raise ValueError("Conflicting translations for the same source fragment")
    translations[old] = new

pattern = r"<(?P<tag>title|p|h[1-3]|figcaption|li|th|td|caption|summary)(?P<attrs>(?:\s[^>]*)?)>(?P<body>.*?)</(?P=tag)>"
used = Counter()


def translate(match):
    text = match["body"]
    if text not in translations:
        raise ValueError(f"Untranslated source fragment: {text[:100]}")
    used[text] += 1
    return f'<{match["tag"]}{match["attrs"]}>{translations[text]}</{match["tag"]}>'


page = re.sub(pattern, translate, source, flags=re.S)
if set(used) != set(translations):
    raise ValueError("Stale translations: the English article changed")
page = page.replace('<html lang="en">', '<html lang="ko">', 1)
page = page.replace(
    '<meta name="description" content="Crowded Speedway from the December 1984 issue: a revised Apple II article with screenshots, repaired ca65 source, and a reproducible DOS 3.3 disk build.">',
    '<meta name="description" content="1984년 12월호의 크라우디드 스피드 웨이를 다시 읽다. Apple II 실행 화면, 수정한 ca65 소스, cc65 빌드 방법과 DOS 3.3 부팅 디스크를 담은 한국어 개정판.">',
    1,
)
page = page.replace(
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<link rel="alternate" hreflang="en" href="index.html">\n'
    '<link rel="alternate" hreflang="ko" href="index.ko.html">',
    1,
)
page = page.replace('aria-label="Article contents"', 'aria-label="기사 목차"')
page = page.replace('<header id="top">', '<header id="top">\n'
                    '<p><a href="index.html" lang="en" hreflang="en">English version</a></p>', 1)
image_alts = {
    "Crowded Speedway running in MAME: a winding grey road, green roadside scenery, the player's car, and score text below.":
        "MAME에서 실행한 크라우디드 스피드 웨이. 굽은 회색 도로와 초록색 길가 풍경, 플레이어의 차가 보이고 아래에는 점수가 표시된다.",
    "The original magazine's black-and-white photograph of the game: START above a chequered starting line.":
        "원 잡지에 실린 게임의 흑백 사진. 체크무늬 출발선 위에 START라는 글자가 보인다.",
    "The repaired game's colour title screen reading CROWDED SPEED WAY, with PUSH SW0 below.":
        "수정한 게임의 컬러 타이틀 화면. CROWDED SPEED WAY 아래에 PUSH SW0라는 안내가 표시된다.",
}
for old, new in image_alts.items():
    page = page.replace('alt="' + old + '"', 'alt="' + escape(new, quote=True) + '"')
page = page.replace('<pre><code>', '<pre><code lang="en">')
page = page.replace('</style>', '''
  /* Local serif fallbacks keep Korean readable without web-font requests. */
  body { font-family: "Noto Serif CJK KR", "Nanum Myeongjo", Batang, Georgia, serif;
         line-height: 1.8; word-break: keep-all; overflow-wrap: anywhere; }
  .issue { letter-spacing: .02em; }
  pre { word-break: normal; overflow-wrap: normal; }
</style>''', 1)

# The translation must not alter any code, source comments, or shell commands.
code_pattern = r"<pre><code(?:\s[^>]*)?>(.*?)</code></pre>"
if re.findall(code_pattern, source, re.S) != re.findall(code_pattern, page, re.S):
    raise ValueError("A code listing changed during translation")
(DOCS / "index.ko.html").write_text(page)
checksums = {
    str(path.relative_to(DOCS)): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(DOCS.rglob("*"))
    if path.is_file() and path.name != "checksums.json"
}
(DOCS / "checksums.json").write_text(json.dumps(checksums, indent=2) + "\n")
print(f"Wrote {DOCS / 'index.ko.html'}; translated {sum(used.values())} article blocks; all code listings unchanged.")
