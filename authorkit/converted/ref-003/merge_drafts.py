"""기존 챕터별 draft를 합본하고 목차를 자동 생성하는 스크립트"""
import re
from pathlib import Path

BASE = Path("C:/Users/Nowzero/PycharmProjects/Skills/KESE-KIT/authorkit")
ARCHIVE_KO = BASE / "archive" / "drafts-ko-chapters"
ARCHIVE_EN = BASE / "archive" / "drafts-en-chapters"
OUT_KO = BASE / "drafts" / "KESE-KIT-KO" / "KESE-KIT-완전판.md"
OUT_EN = BASE / "drafts" / "KESE-KIT-EN" / "KESE-KIT-Complete-Guide.md"

# 장 제목 패턴
CHAPTER_RE = re.compile(r"^#\s+(\d+장[\.\s].*|부록|Part\s+[IVX]+\.?.*)$")
# 절 제목 패턴 (N-M. 제목)
SECTION_RE = re.compile(r"^##\s+(\d+-\d+[\.\s].*)$")
# Part 제목 패턴
PART_RE = re.compile(r"^#\s+(Part\s+[IVX]+\.?.*)$")


def merge_chapters(archive_dir: Path, output_path: Path, title: str, subtitle: str):
    chapters = []
    for ch_dir in sorted(archive_dir.iterdir()):
        if not ch_dir.is_dir():
            continue
        for md_file in ch_dir.glob("*.md"):
            chapters.append((ch_dir.name, md_file))

    toc_entries = []
    chapter_contents = []
    in_code_block = False

    for folder_name, md_file in chapters:
        content = md_file.read_text(encoding="utf-8")
        chapter_contents.append((folder_name, content))

        for line in content.splitlines():
            stripped = line.strip()

            # 코드 블록 내부 무시
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # # 레벨: 장 제목 또는 Part 제목만
            if stripped.startswith("# ") and not stripped.startswith("## "):
                heading = stripped[2:].strip()
                # Part 제목
                if re.match(r"Part\s+[IVX]+", heading):
                    anchor = make_anchor(heading)
                    toc_entries.append((0, heading, anchor))
                # 장 제목 (N장)
                elif re.match(r"\d+장", heading):
                    anchor = make_anchor(heading)
                    toc_entries.append((1, heading, anchor))
                # "부록"
                elif "부록" in heading or "Appendix" in heading:
                    anchor = make_anchor(heading)
                    toc_entries.append((1, heading, anchor))
                continue

            # ## 레벨: N-M 형식 절 제목만
            if stripped.startswith("## ") and not stripped.startswith("### "):
                heading = stripped[3:].strip()
                if re.match(r"\d+-\d+[\.\s]", heading):
                    anchor = make_anchor(heading)
                    toc_entries.append((2, heading, anchor))

    # 합본 조립
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"## {subtitle}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("# 목차")
    lines.append("")

    for level, text, anchor in toc_entries:
        if level == 0:  # Part
            lines.append(f"\n### {text}\n")
        elif level == 1:  # 장
            lines.append(f"- **[{text}](#{anchor})**")
        elif level == 2:  # 절
            lines.append(f"  - [{text}](#{anchor})")

    lines.append("")
    lines.append("---")
    lines.append("")

    for folder_name, content in chapter_contents:
        lines.append(content)
        lines.append("")
        lines.append("---")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(chapters), len(toc_entries), len(lines)


def make_anchor(text: str) -> str:
    anchor = text.lower()
    anchor = re.sub(r"[^\w가-힣\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor).strip("-")
    return anchor


if ARCHIVE_KO.exists():
    ch, toc, ln = merge_chapters(ARCHIVE_KO, OUT_KO, "KESE KIT", "주요정보통신기반시설 취약점 분석·평가 실무 가이드")
    print(f"[KO] {ch}개 챕터, 목차 {toc}항목, {ln}줄")

if ARCHIVE_EN.exists():
    ch, toc, ln = merge_chapters(ARCHIVE_EN, OUT_EN, "KESE KIT", "CII Vulnerability Assessment Practical Guide")
    print(f"[EN] {ch}개 챕터, 목차 {toc}항목, {ln}줄")
