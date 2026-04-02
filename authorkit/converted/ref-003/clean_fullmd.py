"""ref-003 full.md 정리 스크립트 — cleaned.md 생성"""
import re
from pathlib import Path

SRC = Path(__file__).parent / "full.md"
DST = Path(__file__).parent / "cleaned.md"

lines = SRC.read_text(encoding="utf-8").splitlines()

# --- 1. 페이지 번호 잔재 제거 ---
# 로마 숫자 단독 줄
roman_re = re.compile(r"^(i{1,3}|iv|vi{0,3}|ix|x{0,3})$", re.IGNORECASE)
# 아라비아 숫자 단독 줄 (1~999) - 페이지 번호로 추정
arabic_page_re = re.compile(r"^\d{1,3}$")
# "인공지능(AI) 보안 안내서" 단독 줄 (헤더/푸터 반복)
header_footer_re = re.compile(r"^인공지능\(AI\)\s*보안\s*안내서\s*$")

# --- 2. 목차 점선 제거 ---
dotline_re = re.compile(r"[·]{3,}")

# --- 3. 장 제목 패턴 (본문에서의 실제 장 제목) ---
chapter_title_re = re.compile(r"^(제\d+\s*장)\s*$")

# --- 4. 섹션 번호 패턴 (체크리스트에서 단독 줄로 나오는 번호) ---
# "01", "02" 등 0-padded 2자리 (페이지 번호 잔재)
zeropad_re = re.compile(r"^0[1-9]$")

cleaned = []
i = 0
removed_count = 0
stats = {"page_nums": 0, "roman": 0, "header_footer": 0, "dotline": 0, "zeropad": 0}

while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    # 빈 줄은 그대로 유지
    if stripped == "":
        cleaned.append(line)
        i += 1
        continue

    # 페이지 구분 주석은 유지
    if stripped.startswith("<!-- Page"):
        cleaned.append(line)
        i += 1
        continue

    # --- 필터링 ---

    # 로마 숫자 단독 줄 제거
    if roman_re.match(stripped):
        stats["roman"] += 1
        i += 1
        continue

    # 0-padded 숫자 제거 (01~09)
    if zeropad_re.match(stripped):
        stats["zeropad"] += 1
        i += 1
        continue

    # 아라비아 숫자 단독 줄 제거 (페이지 번호)
    # 단, #### 뒤의 번호(1.1.1 등)나 목록 번호는 제외
    if arabic_page_re.match(stripped):
        # 앞뒤 문맥 확인: 페이지 구분선 근처면 페이지 번호
        prev_meaningful = ""
        for j in range(i - 1, max(i - 5, -1), -1):
            if j >= 0 and lines[j].strip():
                prev_meaningful = lines[j].strip()
                break
        next_meaningful = ""
        for j in range(i + 1, min(i + 5, len(lines))):
            if lines[j].strip():
                next_meaningful = lines[j].strip()
                break

        # 페이지 구분선(---) 또는 Page 주석 근처면 페이지 번호
        is_page_num = (
            prev_meaningful.startswith("---")
            or prev_meaningful.startswith("<!-- Page")
            or next_meaningful.startswith("---")
            or next_meaningful.startswith("<!-- Page")
            or header_footer_re.match(prev_meaningful)
            or header_footer_re.match(next_meaningful)
        )

        # 섹션 번호처럼 보이는 것 (1~6 범위에서 뒤에 .이 따라오는 경우) 보존
        if is_page_num:
            stats["page_nums"] += 1
            i += 1
            continue

    # 헤더/푸터 반복 제거
    if header_footer_re.match(stripped):
        stats["header_footer"] += 1
        i += 1
        continue

    # --- 변환 ---

    # 목차 점선 정리
    if dotline_re.search(line):
        # 점선과 페이지 번호 제거, 제목만 남김
        clean_line = dotline_re.sub("", line).strip()
        # 뒤의 페이지 번호도 제거
        clean_line = re.sub(r"\s+\d+\s*$", "", clean_line)
        if clean_line:
            cleaned.append(clean_line)
        stats["dotline"] += 1
        i += 1
        continue

    # 그 외는 그대로 유지
    cleaned.append(line)
    i += 1

# --- 5. 헤딩 레벨 정규화 ---
# 페이지 구분 후 나오는 "제N장" 패턴을 ## 으로 통일
normalized = []
for i, line in enumerate(cleaned):
    stripped = line.strip()

    # "제N장" 단독 줄 → ## 제N장
    if re.match(r"^제\d+\s*장\s*$", stripped):
        normalized.append(f"## {stripped}")
        continue

    # "제N장" + 부제 → ## 제N장 부제
    m = re.match(r"^(제\d+\s*장)\s+(.+)$", stripped)
    if m and not stripped.startswith("#"):
        normalized.append(f"## {stripped}")
        continue

    normalized.append(line)

# --- 6. 연속 빈 줄 3개 이상을 2개로 축소 ---
final = []
blank_count = 0
for line in normalized:
    if line.strip() == "":
        blank_count += 1
        if blank_count <= 2:
            final.append(line)
    else:
        blank_count = 0
        final.append(line)

# --- 저장 ---
content = "\n".join(final)
DST.write_text(content, encoding="utf-8")

total_removed = sum(stats.values())
print(f"정리 완료: {SRC.name} → {DST.name}")
print(f"  원본: {len(lines)}줄 → 정리본: {len(final)}줄 (제거: {len(lines) - len(final)}줄)")
print(f"  제거 상세:")
print(f"    페이지 번호(아라비아): {stats['page_nums']}")
print(f"    페이지 번호(로마): {stats['roman']}")
print(f"    0-padded 번호: {stats['zeropad']}")
print(f"    헤더/푸터 반복: {stats['header_footer']}")
print(f"    목차 점선 정리: {stats['dotline']}")
