"""전체 draft를 합본 — 기존 1~22장(archive) + 신규 23~26장 + 부록"""
import re
from pathlib import Path

BASE = Path("C:/Users/Nowzero/PycharmProjects/Skills/KESE-KIT/authorkit")
ARCHIVE_KO = BASE / "archive" / "drafts-ko-chapters"
NEW_DRAFTS = BASE / "drafts" / "KESE-KIT-KO"
OUT = NEW_DRAFTS / "KESE-KIT-완전판.md"

CHAPTER_RE = re.compile(r"^#\s+(\d+장[\.\s].*|부록|Part\s+[IVX]+\.?.*)$")
SECTION_RE = re.compile(r"^##\s+(\d+-\d+[\.\s].*)$")


def make_anchor(text):
    anchor = text.lower()
    anchor = re.sub(r"[^\w가-힣\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor).strip("-")
    return anchor


def extract_toc(content):
    entries = []
    in_code = False
    for line in content.splitlines():
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if s.startswith("# ") and not s.startswith("## "):
            h = s[2:].strip()
            if re.match(r"Part\s+[IVX]+", h):
                entries.append((0, h, make_anchor(h)))
            elif re.match(r"\d+장", h):
                entries.append((1, h, make_anchor(h)))
            elif "부록" in h or "Appendix" in h:
                entries.append((1, h, make_anchor(h)))
        elif s.startswith("## ") and not s.startswith("### "):
            h = s[3:].strip()
            if re.match(r"\d+-\d+[\.\s]", h):
                entries.append((2, h, make_anchor(h)))
    return entries


# 1) 기존 1~22장 + 부록 수집
old_chapters = []
for ch_dir in sorted(ARCHIVE_KO.iterdir()):
    if not ch_dir.is_dir():
        continue
    for md in ch_dir.glob("*.md"):
        old_chapters.append((ch_dir.name, md.read_text(encoding="utf-8")))

# 2) 신규 23~26장 수집
new_ch_dirs = sorted([
    d for d in NEW_DRAFTS.iterdir()
    if d.is_dir() and d.name.startswith("ch")
])
new_chapters = []
for ch_dir in new_ch_dirs:
    section_new = ch_dir / "section-new.md"
    if section_new.exists():
        new_chapters.append((ch_dir.name, section_new.read_text(encoding="utf-8")))

all_chapters = old_chapters + new_chapters

# 3) TOC 생성
all_toc = []
for _, content in all_chapters:
    all_toc.extend(extract_toc(content))

# 4) 합본 조립
lines = []
lines.append("# KESE KIT")
lines.append("")
lines.append("## 주요정보통신기반시설 취약점 분석·평가 실무 가이드")
lines.append("")
lines.append("**Korea Enhanced Security Evaluation - KISA Infrastructure Toolkit**")
lines.append("")
lines.append("---")
lines.append("")
lines.append("# 목차")
lines.append("")

for level, text, anchor in all_toc:
    if level == 0:
        lines.append(f"\n### {text}\n")
    elif level == 1:
        lines.append(f"- **[{text}](#{anchor})**")
    elif level == 2:
        lines.append(f"  - [{text}](#{anchor})")

lines.append("")
lines.append("---")
lines.append("")

for folder, content in all_chapters:
    lines.append(content)
    lines.append("")
    lines.append("---")
    lines.append("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"합본 완료: {OUT.name}")
print(f"  챕터: {len(old_chapters)}(기존) + {len(new_chapters)}(신규) = {len(all_chapters)}개")
print(f"  목차: {len(all_toc)}항목")
print(f"  총 줄수: {len(lines)}")
