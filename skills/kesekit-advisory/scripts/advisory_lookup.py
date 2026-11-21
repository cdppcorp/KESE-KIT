#!/usr/bin/env python3
"""Query KISA security notices bundled with the kesekit-advisory skills.

Examples:
  python advisory_lookup.py -q nginx -q "Fortinet FortiOS"          # product exposure lookup
  python advisory_lookup.py --cve CVE-2025-0282                     # is this CVE in a KISA notice?
  python advisory_lookup.py --since 2026-10-15 --limit 0            # briefing: notices since a date
  python advisory_lookup.py --vendor Cisco --limit 5
  python advisory_lookup.py --id 2632 --max-rows 0                  # one notice (number or nttId), every row
  python advisory_lookup.py --stats
  python advisory_lookup.py --doctor                               # runtime/data freshness check (run first)
  python advisory_lookup.py --kev --since 2026-10-01 --sort risk   # actively exploited (CISA KEV) first

A query matches when every word appears in the notice. Each result says where it matched:
title/vendor (all rows shown), table rows (only matching rows shown, hidden rows counted),
or body text only (product mentioned in the notice text but not in its version table).

Standard library only (Python 3.8+). Data: ../references/kisa-advisories/advisories.json
plus pre-notice.json next to it (vulnerabilities disclosed by the vendor / in CVE records before
KISA posts a notice; an entry drops out once all of its CVEs appear in KISA notices).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import platform
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = SCRIPT_DIR.parent / "references" / "kisa-advisories" / "advisories.json"
# Raw notice archive (본문 + attachments) when the skill runs inside the KESE-KIT repository.
REPO_SOURCE = SCRIPT_DIR.parents[2] / "문서" / "KISA_보안공지_2025-2026" / "KISA_보안공지_2025-2026"
REFS_SHOWN = 15
STALE_DAYS = 30  # notice data / EPSS older than this triggers a warning
THREAT_RESPONSE = SCRIPT_DIR.parent / "references" / "kisa-advisories" / "threat-response.md"
PRE_NOTICE_FILE = "pre-notice.json"  # read from the same folder as the KISA data file
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.I)
ROW_FIELDS = ("cve", "vendor", "product", "ecosystem", "affected", "fixed", "severity")
REQUIRED_STR = ("no", "date", "type", "title", "vendor", "url", "summary")
REQUIRED_LIST = ("cves", "affected")
MATCH_RANK = {"title": 3, "rows": 2, "body": 1}
# Notices whose fix is not out yet: the vendor advisory must be checked live.
PENDING_RE = re.compile(r"업데이트 예정|미배포|제조사 미공개|패치 미제공")
# 'Fixed' cells that name no fix (KISA tables: "패치 미발표", "None", "Not applicable", "없음").
NO_FIX_RE = re.compile(r"미발표|미제공|없음|not applicable|\bnone\b|\bn/a\b", re.I)
DIGIT_RE = re.compile(r"\d")
CATCH_ALL_VENDOR = "기타"  # vendor of unrelated notices; never matched as "the same vendor"

# Spellings that appear in KISA titles/tables. Every member of a group expands to the others.
ALIAS_GROUPS = [
    ("linux", "리눅스"),
    ("linux kernel", "리눅스 커널"),
    ("microsoft", "마이크로소프트", "ms"),
    ("google", "구글"),
    ("chrome", "크롬"),
    ("android", "안드로이드"),
    ("apple", "애플"),
    ("samsung", "삼성", "삼성전자"),
    ("apache", "아파치"),
    ("fortinet", "포티넷"),
    ("oracle", "오라클"),
    ("java", "자바"),
    ("cisco", "시스코"),
    ("nvidia", "엔비디아"),
    ("adobe", "어도비"),
    ("ivanti", "이반티"),
    ("citrix", "시트릭스"),
    ("vmware", "브이엠웨어"),
    ("windows", "윈도우"),
    ("wordpress", "워드프레스"),
    ("ubuntu", "우분투"),
    ("debian", "데비안"),
    ("red hat", "redhat", "레드햇"),
    ("mozilla", "모질라"),
    ("firefox", "파이어폭스"),
    ("synology", "시놀로지"),
    ("qnap", "큐냅"),
    ("kakao", "카카오"),
    ("hancom", "한컴"),
]
# Vulnerability nicknames that KISA notices do not spell out, mapped to their CVE ids.
# Add only mappings confirmed by the vendor or the discoverer's advisory. One-way: the nickname
# expands to its CVEs, a CVE expands only to the nickname (sibling CVEs never match each other).
NICKNAME_GROUPS = [
    ("java4shell", "cve-2026-114938"),  # Calif.io disclosure, Oracle CSPU Nov 2026 (KISA #2640)
    # Theori Xint disclosure (nginx2root.com), F5 CVE records 2026-11-18; the Linux SCTP kernel bug has no CVE yet
    ("nginx2root", "cve-2026-123007", "cve-2026-123634", "cve-2026-123633", "cve-2026-121810", "cve-2026-113425"),
    # KISA pinned notice 2026-10-22 (nttId 72230): "PHP 보안취약점(PHP2Shell) … (CVE-2026-109618, CVE-2026-109619)";
    # the fixed versions are in the patch notice #2574
    ("php2shell", "cve-2026-109618", "cve-2026-109619"),
]
ALIASES = {
    **{member: [o for o in group if o != member] for group in ALIAS_GROUPS for member in group},
    **{nickname: list(cves) for nickname, *cves in NICKNAME_GROUPS},
    **{cve: [nickname] for nickname, *cves in NICKNAME_GROUPS for cve in cves},
}

LABELS = {
    "ko": {
        "coverage": "데이터 기준: {first} ~ {last} (KISA 보호나라 보안공지 {count}건)",
        "query": "질의",
        "found": "{n}건",
        "none": "일치하는 공지 없음 — 데이터 기준일 이후 공지는 보호나라에서 직접 확인하세요. 없다고 안전하다는 뜻은 아닙니다.",
        "none_filtered": "일치하는 공지 없음 (--since/--until/--vendor/--type/--kev 필터 적용 중)",
        "source": "원문",
        "match": "일치",
        "match_title": "제목·벤더 (전체 행 표시)",
        "match_rows": "표 행 {shown}/{total}행",
        "match_body": "본문 언급 (버전 표에는 해당 제품 행 없음 — 원문 확인)",
        "summary": "요약",
        "cves": "CVE",
        "attachments": "첨부",
        "refs": "참고사이트",
        "risk": "위험 지표",
        "risk_sources": "위험 지표 기준: KEV {kev} · EPSS {epss} · NVD CVSS {nvd}",
        "nvd_none": "미수집",
        "kev_count": "KEV 등재 {n}건 ({cves})",
        "ransomware": "랜섬웨어 악용",
        "max_cvss": "최고 CVSS {score:g} ({cve})",
        "max_epss": "최고 EPSS {score:.3f} (상위 {top}%, {cve})",
        "pending": "주의: 해결 버전 미배포·후속 업데이트 예정 공지 — 참고사이트의 벤더 권고를 실시간으로 확인하세요",
        "pending_fixed": "후속 공지 #{no}({date})에 해결 버전이 나왔습니다 — 해결 버전은 그 공지로 판정하세요 (--id {id})",
        "local": "원본 폴더 (본문·첨부 열람)",
        "more_rows": "… {n}행 생략 (전체: --id {id} --max-rows 0)",
        "hidden_rows": "… 질의와 무관한 행 {n}개 숨김 (전체: --id {id})",
        "more_items": "… {n}건 더 있음 (--limit 0 으로 전체 보기)",
        "cols": {"cve": "CVE", "vendor": "제조사", "product": "제품", "ecosystem": "생태계",
                 "affected": "영향받는 버전", "fixed": "해결 버전", "severity": "심각도", "risk": "위험"},
        "brief_cols": "| 게시일 | 번호 | 유형 | 벤더 | 제목 | CVE 수 | 위험 |",
        "stats_type": "유형별", "stats_vendor": "벤더 상위", "stats_month": "월별",
        "doctor_title": "## 실행 환경 점검",
        "doctor_python": "Python {ver} · {os} · {exe}",
        "doctor_data": "공지 데이터 {count}건, 최신 공지 {last}{age}",
        "doctor_data_stale": " — {days}일 이상 지남: 이후 공지는 보호나라에서 확인하거나 데이터를 갱신하세요",
        "doctor_kev": "CISA KEV 카탈로그 {version}{age}",
        "doctor_epss": "EPSS 점수 {date}{age}",
        "ago": " ({n}일 전)",
        "doctor_epss_stale": " — 오래됨: scripts/fetch_cve_enrichment.py 로 갱신 권장",
        "doctor_risk_missing": "CVE 위험 지표 없음 — 우선순위는 요약 키워드로만 판단 (scripts/fetch_cve_enrichment.py 실행 후 재빌드)",
        "doctor_nvd": "NVD CVSS {n}건 수집",
        "doctor_nvd_missing": "NVD CVSS 미수집 — 우선순위는 KEV·EPSS·요약 키워드로 판단",
        "doctor_archive": "원본 아카이브 있음 (본문·첨부 열람 가능): {path}",
        "doctor_archive_missing": "원본 아카이브 없음 — 첨부는 공지 원문 링크로 확인",
        "doctor_threat": "위협 대응 점검 문서 (threat-response.md) {state}",
        "present": "있음", "missing": "없음",
        "pre_notice": "KISA 공지 전 항목 — 벤더·CVE 원문 기준 (확인일 {checked}). KISA 공지가 나오면 그 공지로 다시 판정하세요",
        "pre_notice_count": "KISA 공지 전 항목 {n}건 (벤더·CVE 원문, 확인일 {checked}): {titles}",
        "doctor_pre_retired": "KISA 공지에 반영돼 빠진 공지 전 항목: {titles} — pre-notice.json에서 지워도 됩니다",
        "doctor_pre_stale": " — 확인일이 {days}일 넘게 지남: 벤더 권고와 보호나라를 다시 확인하고 checked를 갱신하세요",
    },
    "en": {
        "coverage": "Data coverage: {first} ~ {last} ({count} KISA Boho-nara notices)",
        "query": "Query",
        "found": "{n} notice(s)",
        "none": "No matching notice — check Boho-nara directly for notices after the coverage date. No match does not mean safe.",
        "none_filtered": "No matching notice (--since/--until/--vendor/--type/--kev filters are active)",
        "source": "Source",
        "match": "Matched in",
        "match_title": "title/vendor (all rows shown)",
        "match_rows": "table rows {shown}/{total}",
        "match_body": "body text only (no row for this product in the version table — read the notice)",
        "summary": "Summary",
        "cves": "CVEs",
        "attachments": "Attachments",
        "refs": "References",
        "risk": "Risk signals",
        "risk_sources": "Risk signals as of: KEV {kev} · EPSS {epss} · NVD CVSS {nvd}",
        "nvd_none": "not fetched",
        "kev_count": "{n} in CISA KEV ({cves})",
        "ransomware": "used in ransomware",
        "max_cvss": "max CVSS {score:g} ({cve})",
        "max_epss": "max EPSS {score:.3f} (top {top}%, {cve})",
        "pending": "Caution: fix not released / notice to be updated — check the vendor advisory in References live",
        "pending_fixed": "Fix released in a later notice #{no} ({date}) — judge the fix against that notice (--id {id})",
        "local": "Source folder (notice body and attachments)",
        "more_rows": "… {n} more row(s) (all rows: --id {id} --max-rows 0)",
        "hidden_rows": "… {n} row(s) unrelated to the query hidden (all rows: --id {id})",
        "more_items": "… {n} more notice(s) (use --limit 0 for all)",
        "cols": {"cve": "CVE", "vendor": "Vendor", "product": "Product", "ecosystem": "Ecosystem",
                 "affected": "Affected", "fixed": "Fixed", "severity": "Severity", "risk": "Risk"},
        "brief_cols": "| Date | No. | Type | Vendor | Title | CVEs | Risk |",
        "stats_type": "By type", "stats_vendor": "Top vendors", "stats_month": "By month",
        "doctor_title": "## Runtime check",
        "doctor_python": "Python {ver} · {os} · {exe}",
        "doctor_data": "{count} notices, newest {last}{age}",
        "doctor_data_stale": " — older than {days} days: check Boho-nara for later notices or refresh the data",
        "doctor_kev": "CISA KEV catalog {version}{age}",
        "doctor_epss": "EPSS scores {date}{age}",
        "ago": " ({n} day(s) ago)",
        "doctor_epss_stale": " — stale: refresh with scripts/fetch_cve_enrichment.py",
        "doctor_risk_missing": "No CVE risk signals — priority falls back to summary keywords (run scripts/fetch_cve_enrichment.py, then rebuild)",
        "doctor_nvd": "NVD CVSS fetched for {n} CVE(s)",
        "doctor_nvd_missing": "NVD CVSS not fetched — priority uses KEV, EPSS and summary keywords",
        "doctor_archive": "Raw notice archive present (bodies and attachments readable): {path}",
        "doctor_archive_missing": "Raw notice archive absent — open attachments via the notice URL",
        "doctor_threat": "Threat-response checklist (threat-response.md) {state}",
        "present": "present", "missing": "missing",
        "pre_notice": "KISA pre-notice entry — based on the vendor/CVE record (checked {checked}). "
                      "Re-judge with the KISA notice once it is posted",
        "pre_notice_count": "{n} KISA pre-notice entr(ies) (vendor/CVE records, checked {checked}): {titles}",
        "doctor_pre_retired": "Retired pre-notice entries (now in a KISA notice): {titles} — safe to delete from pre-notice.json",
        "doctor_pre_stale": " — checked more than {days} days ago: re-check the vendor advisory and Boho-nara, then update 'checked'",
    },
}


def default_lang() -> str:
    return "ko" if "skills-ko" in SCRIPT_DIR.parts else "en"


# --------------------------------------------------------------------------- data loading


def read_json(path: Path) -> object:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"error: data file not found: {path}")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"error: cannot read {path}: {exc}")


def validate(data: object, path: Path) -> dict:
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("advisories"), list):
        raise SystemExit(f"error: unsupported data schema in {path}")
    for index, advisory in enumerate(data["advisories"]):
        problem = record_problem(advisory)
        if problem:
            raise SystemExit(f"error: {path}: advisory #{index} {problem}")
    meta = data.get("cve_meta", {})
    if not isinstance(meta, dict) or not all(isinstance(v, dict) for v in meta.values()):
        raise SystemExit(f"error: {path}: 'cve_meta' must map CVE ids to objects")
    return data


def load(path: Path) -> dict:
    return validate(read_json(path), path)


def load_pre_notice(path: Path) -> dict | None:
    """Optional pre-notice.json (same schema as advisories.json); None when the file is absent."""
    return validate(read_json(path), path) if path.is_file() else None


def insert_by_date(entries: list[dict], advisories: list[dict]) -> list[dict]:
    """New list: KISA order kept (newest first), each entry placed before the first notice not newer than it."""
    out = list(advisories)
    for entry in sorted(entries, key=lambda e: e["date"]):
        index = next((i for i, a in enumerate(out) if a["date"] <= entry["date"]), len(out))
        out.insert(index, entry)
    return out


def merge_pre_notice(data: dict, pre: dict | None) -> dict:
    """Return the KISA data with pre-notice entries merged in by date; the inputs are not modified.

    An entry is retired once all of its CVEs appear in KISA notices (they are the source from then on);
    an entry without CVEs is never retired. Per CVE, KISA-side risk signals win over the pre-notice ones.
    Coverage stays the KISA coverage.
    """
    if not pre:
        return data
    known = {c.upper() for a in data["advisories"] for c in a["cves"]}
    checked = str(pre.get("checked", ""))
    active, retired = [], []
    for entry in pre["advisories"]:
        cves = {c.upper() for c in entry["cves"]}
        if cves and cves <= known:
            retired.append(entry["title"])
        else:
            active.append({**entry, "pre_notice": True, "checked": checked})
    kisa_meta = data.get("cve_meta", {})
    pre_meta = {cve.upper(): value for cve, value in pre.get("cve_meta", {}).items()}
    meta = {cve: {**pre_meta.get(cve, {}), **kisa_meta.get(cve, {})} for cve in {*pre_meta, *kisa_meta}}
    return {**data, "advisories": insert_by_date(active, data["advisories"]), "cve_meta": meta,
            "pre_notice": {"checked": checked, "active": [a["title"] for a in active], "retired": retired}}


def record_problem(advisory: object) -> str | None:
    if not isinstance(advisory, dict):
        return "is not an object"
    for key in REQUIRED_STR:
        if not isinstance(advisory.get(key), str):
            return f"field '{key}' must be a string"
    for key in REQUIRED_LIST:
        if not isinstance(advisory.get(key), list):
            return f"field '{key}' must be a list"
    if not all(isinstance(c, str) for c in advisory["cves"]):  # id format: scripts/validate-content.mjs
        return "field 'cves' must hold strings"
    if not all(isinstance(row, dict) for row in advisory["affected"]):
        return "field 'affected' must contain objects"
    if not all(isinstance(value, str) for row in advisory["affected"] for value in row.values()):
        return "rows in 'affected' must hold string values"
    refs = advisory.get("refs", [])
    if not isinstance(refs, list) or not all(isinstance(r, dict) and isinstance(r.get("url"), str) for r in refs):
        return "field 'refs' must be a list of {url, n?} objects"
    return None


# --------------------------------------------------------------------------- matching


def compile_phrase(phrase: str) -> re.Pattern:
    """Whitespace-tolerant pattern; word boundaries only next to ASCII letters/digits.

    'HP' does not hit 'PHP', '.NET' still hits 'ASP.NET', Korean matches as a substring.
    """
    body = r"\s+".join(re.escape(part) for part in phrase.split())
    if phrase[0].isascii() and phrase[0].isalnum():
        body = r"(?<![A-Za-z0-9])" + body
    if phrase[-1].isascii() and phrase[-1].isalnum():
        body += r"(?![A-Za-z0-9])"
    return re.compile(body, re.I)


def build_query(term: str) -> list[list[list[re.Pattern]]]:
    """Return query variants; a variant is a list of tokens, a token a list of alternative patterns."""
    words = term.split()
    variants = [[[compile_phrase(w)] + [compile_phrase(a) for a in ALIASES.get(w.lower(), [])] for w in words]]
    for alias in ALIASES.get(" ".join(words).lower(), []) if len(words) > 1 else []:
        variants.append([[compile_phrase(alias)]])
    return variants


def token_hits(token: list[re.Pattern], text: str) -> bool:
    return any(p.search(text) for p in token)


def row_text(row: dict) -> str:
    return " ".join(str(v) for v in row.values())


def body_text(advisory: dict) -> str:
    tables = " ".join(" ".join(" ".join(r) for r in t.get("rows", [])) for t in advisory.get("tables", []))
    return " ".join((advisory["summary"], advisory.get("text", ""), tables))


def match_variant(advisory: dict, tokens: list[list[re.Pattern]]) -> tuple[str, list[dict]] | None:
    header = f"{advisory['vendor']} {advisory['title']}"
    remaining = [t for t in tokens if not token_hits(t, header)]
    if not remaining:
        return "title", advisory["affected"]
    rows = [r for r in advisory["affected"] if all(token_hits(t, row_text(r)) for t in remaining)]
    if rows:
        return "rows", rows
    everything = " ".join([body_text(advisory)] + [row_text(r) for r in advisory["affected"]])
    if all(token_hits(t, everything) for t in remaining):
        return "body", advisory["affected"]
    return None


def match_query(advisory: dict, variants: list[list[list[re.Pattern]]]) -> tuple[str, list[dict]] | None:
    results = [m for m in (match_variant(advisory, v) for v in variants) if m]
    return max(results, key=lambda m: MATCH_RANK[m[0]]) if results else None


def match_cve(advisory: dict, cve: str) -> tuple[str, list[dict]] | None:
    cve = cve.upper()
    if cve not in {c.upper() for c in advisory["cves"]}:
        return None
    rows = [r for r in advisory["affected"] if cve in {c.upper() for c in CVE_RE.findall(r.get("cve", ""))}]
    return ("rows", rows) if rows else ("body", advisory["affected"])


def match_id(advisory: dict, ident: str) -> tuple[str, list[dict]] | None:
    ident = ident.lower()  # pre-notice ids are words (nginx2root); KISA ids are digits or '공지'
    return ("title", advisory["affected"]) if ident in (advisory["no"].lower(), str(advisory.get("ntt", "")).lower()) else None


def vendor_matches(advisory: dict, variants: list[list[list[re.Pattern]]]) -> bool:
    return any(all(token_hits(t, advisory["vendor"]) for t in v) for v in variants)


def number(value: object) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def risk_of(cves: list[str], meta: dict) -> dict:
    """Aggregate KEV / CVSS / EPSS over the given CVE ids."""
    entries = [(c, meta[c]) for c in dict.fromkeys(c.upper() for c in cves) if c in meta]
    out: dict = {}
    kev = [c for c, m in entries if m.get("kev")]
    if kev:
        out["kev"] = kev
    if any(m.get("ransomware") is True for _, m in entries):
        out["ransomware"] = True
    cvss = [(number(m.get("cvss")), c) for c, m in entries if number(m.get("cvss")) is not None]
    if cvss:
        out["cvss"], out["cvss_cve"] = max(cvss)
    epss = [(number(m.get("epss")), number(m.get("pct")), c) for c, m in entries if number(m.get("epss")) is not None]
    if epss:
        score, pct, cve = max(epss, key=lambda e: e[0])
        out.update(epss=score, epss_cve=cve, **({"epss_pct": pct} if pct is not None else {}))
    return out


def row_cves(row: dict) -> list[str]:
    return CVE_RE.findall(row.get("cve", ""))


def risk_key(risk: dict) -> tuple:
    return (bool(risk.get("kev")), risk.get("epss", 0.0), risk.get("cvss", 0.0))


def is_pending(advisory: dict) -> bool:
    texts = [advisory.get("text", "")] + [r.get("fixed", "") for r in advisory["affected"]]
    return any(PENDING_RE.search(t) for t in texts)


def has_fix(row: dict) -> bool:
    """True when the row names a fixed version: it has a number and no 'not released / no fix' wording."""
    fixed = row.get("fixed", "").strip()
    return bool(DIGIT_RE.search(fixed)) and not PENDING_RE.search(fixed) and not NO_FIX_RE.search(fixed)


def cve_rows(advisory: dict, cve: str) -> list[dict]:
    return [r for r in advisory["affected"] if cve in {c.upper() for c in row_cves(r)}]


def product_key(row: dict) -> str:
    return " ".join(row.get("product", "").lower().split())


def fixes_cve(notice: dict, cve: str, products: set[str]) -> bool:
    """Every row of the CVE in the notice has a fixed version, and every product in products is among them
    (prefix match either way, so 'PHP' is covered by 'PHP 8.2')."""
    rows = cve_rows(notice, cve)
    if not rows or not all(has_fix(r) for r in rows):
        return False
    fixed = [key for key in map(product_key, rows) if key]
    return all(any(f.startswith(p) or p.startswith(f) for f in fixed) for p in products)


def mark_later_fixes(data: dict) -> dict:
    """Return the data with 'fixed_by' on each pending KISA notice whose open CVEs are all fixed in one later
    notice of the same vendor (the earliest such notice); the inputs are not modified.

    Open CVEs are those not already fixed by the notice itself or an earlier or same-date notice of the
    same vendor (e.g. #2581 cites PHP2Shell, fixed in #2574). The later notice must have a fixed version on
    every row of each open CVE and cover every product the pending notice lists for it. Other vendors'
    notices, the catch-all vendor '기타', notices without CVEs and pre-notice entries never count.
    """
    kisa = sorted((a for a in data["advisories"] if not a.get("pre_notice")), key=lambda a: a["date"])

    def later_fix(advisory: dict) -> dict | None:
        cves, vendor = {c.upper() for c in advisory["cves"]}, advisory["vendor"]
        if advisory.get("pre_notice") or not cves or vendor == CATCH_ALL_VENDOR or not is_pending(advisory):
            return None
        same_vendor = [b for b in kisa if b["vendor"] == vendor]
        earlier = [b for b in same_vendor if b["date"] <= advisory["date"]]  # includes the notice itself
        open_cves = {c for c in cves if not any(fixes_cve(b, c, set()) for b in earlier)}
        if not open_cves:
            return None
        needed = {c: {product_key(r) for r in cve_rows(advisory, c)} - {""} for c in open_cves}
        return next((b for b in same_vendor if b["date"] > advisory["date"]
                     and all(fixes_cve(b, c, needed[c]) for c in open_cves)), None)

    out = []
    for a in data["advisories"]:
        later = later_fix(a)
        out.append({**a, "fixed_by": {"no": later["no"], "date": later["date"], "id": ref_id(later)}} if later else a)
    return {**data, "advisories": out}


def passes_filters(advisory: dict, args: argparse.Namespace, vendor_query, meta: dict | None = None) -> bool:
    if getattr(args, "kev", False) and not risk_of(advisory["cves"], meta or {}).get("kev"):
        return False
    if args.since and advisory["date"] < args.since:
        return False
    if args.until and advisory["date"] > args.until:
        return False
    if vendor_query and not vendor_matches(advisory, vendor_query):
        return False
    if args.type and args.type not in advisory["type"]:
        return False
    return True


def collect(advisories: list[dict], matcher) -> list[tuple[dict, str, list[dict]]]:
    found = []
    for advisory in advisories:
        result = matcher(advisory)
        if result:
            found.append((advisory, result[0], result[1]))
    return found


def run_matches(advisories: list[dict], args: argparse.Namespace) -> list[tuple[str, list]]:
    """Group results per query term / CVE / id, preserving the requested order."""
    groups = []
    for term in args.query:
        variants = build_query(term)
        groups.append((term, collect(advisories, lambda a, v=variants: match_query(a, v))))
    for cve in args.cve:
        groups.append((cve.upper(), collect(advisories, lambda a, c=cve: match_cve(a, c))))
    if args.id:
        groups.append((f"#{args.id}", collect(advisories, lambda a: match_id(a, args.id))))
    return groups


# --------------------------------------------------------------------------- rendering


def ref_id(advisory: dict) -> str:
    """Unambiguous id for follow-up commands (pinned notices are numbered '공지')."""
    return advisory["no"] if advisory["no"].isdigit() else advisory.get("ntt") or advisory["no"]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def limit(items: list, count: int) -> list:
    return items if count <= 0 else items[:count]


def compact_risk(risk: dict) -> str:
    parts = []
    if risk.get("kev"):
        parts.append("KEV" if len(risk["kev"]) == 1 else f"KEV×{len(risk['kev'])}")
    if "cvss" in risk:
        parts.append(f"CVSS {risk['cvss']:g}")
    if "epss" in risk:
        parts.append(f"EPSS {risk['epss']:.2f}")
    return " · ".join(parts)


def format_risk(risk: dict, labels: dict) -> str:
    parts = []
    if risk.get("kev"):
        shown = risk["kev"][:5] + ([f"… +{len(risk['kev']) - 5}"] if len(risk["kev"]) > 5 else [])
        parts.append(labels["kev_count"].format(n=len(risk["kev"]), cves=", ".join(shown)))
    if risk.get("ransomware"):
        parts.append(labels["ransomware"])
    if "cvss" in risk:
        parts.append(labels["max_cvss"].format(score=risk["cvss"], cve=risk["cvss_cve"]))
    if "epss" in risk:
        top = (1 - risk["epss_pct"]) * 100 if "epss_pct" in risk else 100.0
        top_text = "<0.1" if top < 0.1 else f"{top:.1f}"
        parts.append(labels["max_epss"].format(score=risk["epss"], top=top_text, cve=risk["epss_cve"]))
    return " · ".join(parts)


def render_rows(rows: list[dict], args: argparse.Namespace, labels: dict, ident: str, meta: dict | None = None) -> list[str]:
    meta = meta or {}
    shown = limit(rows, args.max_rows)
    risks = [compact_risk(risk_of(row_cves(r), meta)) for r in shown]
    cols = [f for f in ROW_FIELDS if any(r.get(f) for r in rows)]
    if not cols:
        return []
    with_risk = any(risks)
    header = [labels["cols"][c] for c in cols] + ([labels["cols"]["risk"]] if with_risk else [])
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join([md(r.get(c, "")) for c in cols] + ([risk] if with_risk else [])) + " |"
            for r, risk in zip(shown, risks)]
    if len(rows) > len(shown):
        out.append(labels["more_rows"].format(n=len(rows) - len(shown), id=ident))
    return out


def match_label(kind: str, rows: list[dict], advisory: dict, labels: dict) -> str:
    if kind == "rows":
        return labels["match_rows"].format(shown=len(rows), total=len(advisory["affected"]))
    return labels["match_" + kind]


def render_refs(refs: list[dict], labels: dict) -> list[str]:
    if not refs:
        return []
    out = [f"- {labels['refs']}:"]
    out += [f"  - [{r['n']}] {r['url']}" if r.get("n") else f"  - {r['url']}" for r in refs[:REFS_SHOWN]]
    if len(refs) > REFS_SHOWN:
        out.append(f"  - … +{len(refs) - REFS_SHOWN}")
    return out


def local_folder(advisory: dict) -> str | None:
    """Absolute path of the archived notice folder, if the raw archive is present next to the skill."""
    if not advisory.get("folder"):
        return None
    path = REPO_SOURCE / advisory["folder"]
    return str(path) if path.is_dir() else None


def render_advisory(advisory: dict, kind: str, rows: list[dict], args: argparse.Namespace, labels: dict,
                    meta: dict | None = None) -> list[str]:
    a = advisory
    ident = ref_id(a)
    number = a["no"] if a["no"].isdigit() else f"{a['no']} (nttId {a.get('ntt', '?')})"
    if a.get("pre_notice"):
        out = [f"### [{a['date']}] {a['title']} ({a['type']})", f"- {labels['source']}: {a['url'] or '-'}",
               f"- {labels['pre_notice'].format(checked=a.get('checked') or '-')}"]
    else:
        out = [f"### [{a['date']}] #{number} {a['title']} ({a['type']})", f"- {labels['source']}: {a['url'] or '-'}"]
    out.append(f"- {labels['match']}: {match_label(kind, rows, a, labels)}")
    risk = risk_of(a["cves"], meta or {})
    if risk:
        out.append(f"- {labels['risk']}: {format_risk(risk, labels)}")
    if a.get("fixed_by"):
        out.append(f"- {labels['pending_fixed'].format(**a['fixed_by'])}")
    elif is_pending(a):
        out.append(f"- {labels['pending']}")
    if a["summary"]:
        out.append(f"- {labels['summary']}: {a['summary']}")
    if a["cves"]:
        cves = a["cves"] if len(a["cves"]) <= 12 else a["cves"][:12] + [f"… +{len(a['cves']) - 12}"]
        out.append(f"- {labels['cves']}: {', '.join(cves)}")
    if a.get("attachments"):
        out.append(f"- {labels['attachments']}: {', '.join(a['attachments'])}")
    out += render_refs(a.get("refs", []), labels)
    folder = local_folder(a)
    if folder:
        out.append(f"- {labels['local']}: {folder}")
    table = render_rows(rows, args, labels, ident, meta)
    if table:
        out += [""] + table
    hidden = len(a["affected"]) - len(rows)
    if kind == "rows" and hidden > 0:
        out.append(labels["hidden_rows"].format(n=hidden, id=ident))
    return out + [""]


def render_brief(items: list[dict], labels: dict, meta: dict | None = None) -> list[str]:
    out = [labels["brief_cols"], "|---|---|---|---|---|:-:|---|"]
    out += [
        f"| {a['date']} | {a['no']} | {md(a['type'])} | {md(a['vendor'])} | {md(a['title'])} | {len(a['cves'])} | "
        f"{compact_risk(risk_of(a['cves'], meta or {}))} |"
        for a in items
    ]
    return out


def render_stats(advisories: list[dict], labels: dict) -> list[str]:
    by_type = Counter(a["type"] for a in advisories).most_common()
    by_vendor = Counter(a["vendor"] for a in advisories if a["vendor"] != "기타").most_common(20)
    by_month = sorted(Counter(a["date"][:7] for a in advisories).items())
    return [
        f"- {labels['stats_type']}: " + ", ".join(f"{k} {v}" for k, v in by_type),
        f"- {labels['stats_vendor']}: " + ", ".join(f"{k}({v})" for k, v in by_vendor),
        f"- {labels['stats_month']}: " + ", ".join(f"{k} {v}" for k, v in by_month),
    ]


def slim(advisory: dict, meta: dict | None = None) -> dict:
    """Advisory without bulky fields, for JSON output."""
    out = {k: v for k, v in advisory.items() if k not in ("affected", "tables", "text")}
    out["rows_total"] = len(advisory["affected"])
    risk = risk_of(advisory["cves"], meta or {})
    if risk:
        out["risk"] = risk
    if is_pending(advisory) and not advisory.get("fixed_by"):
        out["fix_pending"] = True
    folder = local_folder(advisory)
    if folder:
        out["local_folder"] = folder
    return out


def json_rows(rows: list[dict], meta: dict) -> list[dict]:
    out = []
    for row in rows:
        risk = risk_of(row_cves(row), meta)
        out.append({**row, "risk": risk} if risk else row)
    return out


def json_payload(data: dict, groups: list, advisories: list[dict], args: argparse.Namespace) -> dict:
    meta = data.get("cve_meta", {})
    base = {"coverage": data.get("coverage", {}), "risk_sources": data.get("risk_sources", {})}
    if data.get("pre_notice"):
        base["pre_notice"] = data["pre_notice"]
    if not groups:
        shown = limit(advisories, args.limit)
        return {**base, "total": len(advisories), "truncated": len(shown) < len(advisories),
                "advisories": [slim(a, meta) for a in shown]}
    results = []
    for key, found in groups:
        shown = limit(found, args.limit)
        matches = []
        for advisory, kind, rows in shown:
            kept = limit(rows, args.max_rows)
            matches.append({**slim(advisory, meta), "match": kind, "rows_matched": len(rows),
                            "rows_truncated": len(kept) < len(rows), "rows": json_rows(kept, meta)})
        results.append({"query": key, "total": len(found), "truncated": len(shown) < len(found), "matches": matches})
    return {**base, "results": results}


def risk_sources_line(data: dict, labels: dict) -> str | None:
    src = data.get("risk_sources") or {}
    if not src:
        return None
    nvd = (src.get("nvd") or {}).get("fetched")
    return labels["risk_sources"].format(kev=(src.get("kev") or {}).get("version", "-"),
                                         epss=(src.get("epss") or {}).get("date", "-"),
                                         nvd=nvd if nvd else labels["nvd_none"])


def pre_notice_line(data: dict, labels: dict) -> str | None:
    pre = data.get("pre_notice") or {}
    if not pre.get("active"):
        return None
    return labels["pre_notice_count"].format(n=len(pre["active"]), checked=pre.get("checked") or "-",
                                             titles=", ".join(pre["active"]))


def days_since(text: str, today: dt.date) -> int | None:
    try:
        return (today - dt.date.fromisoformat(str(text)[:10])).days
    except ValueError:
        return None


def render_doctor(data: dict, labels: dict, today: dt.date, archive: Path = REPO_SOURCE,
                  threat: Path = THREAT_RESPONSE) -> list[str]:
    """Runtime and data-freshness report. Status: OK / WARN / INFO."""
    out = [labels["doctor_title"], ""]

    def line(status: str, text: str) -> None:
        out.append(f"- [{status}] {text}")

    def ago(days: int | None) -> str:  # omitted when unknown or in the future (clock skew)
        return labels["ago"].format(n=days) if days is not None and days >= 0 else ""

    python_ok = sys.version_info >= (3, 8)
    line("OK" if python_ok else "WARN", labels["doctor_python"].format(
        ver=platform.python_version(), os=f"{platform.system()} {platform.release()}", exe=sys.executable))
    cov = data.get("coverage", {})
    age = days_since(cov.get("last", ""), today)
    stale = age is None or age > STALE_DAYS
    line("WARN" if stale else "OK", labels["doctor_data"].format(count=cov.get("count"), last=cov.get("last"), age=ago(age))
         + (labels["doctor_data_stale"].format(days=STALE_DAYS) if stale else ""))
    src = data.get("risk_sources") or {}
    if src.get("kev") or src.get("epss"):
        kev, epss = src.get("kev") or {}, src.get("epss") or {}
        kev_age = days_since(kev.get("released", ""), today)
        line("OK" if kev else "WARN", labels["doctor_kev"].format(version=kev.get("version", "-"), age=ago(kev_age)))
        epss_age = days_since(epss.get("date", ""), today)
        epss_stale = epss_age is None or epss_age > STALE_DAYS
        line("WARN" if epss_stale else "OK", labels["doctor_epss"].format(date=epss.get("date", "-"), age=ago(epss_age))
             + (labels["doctor_epss_stale"] if epss_stale else ""))
    else:
        line("WARN", labels["doctor_risk_missing"])
    nvd = (src.get("nvd") or {}).get("fetched")
    line("OK" if nvd else "INFO", labels["doctor_nvd"].format(n=nvd) if nvd else labels["doctor_nvd_missing"])
    pre_active, pre_retired = pre_notice_line(data, labels), (data.get("pre_notice") or {}).get("retired")
    if pre_active:
        pre_age = days_since((data.get("pre_notice") or {}).get("checked", ""), today)
        pre_stale = pre_age is None or pre_age > STALE_DAYS
        line("WARN" if pre_stale else "INFO",
             pre_active + (labels["doctor_pre_stale"].format(days=STALE_DAYS) if pre_stale else ""))
    if pre_retired:
        line("INFO", labels["doctor_pre_retired"].format(titles=", ".join(pre_retired)))
    line("INFO", labels["doctor_archive"].format(path=archive) if archive.is_dir() else labels["doctor_archive_missing"])
    has_threat = threat.is_file()
    line("OK" if has_threat else "WARN", labels["doctor_threat"].format(state=labels["present" if has_threat else "missing"]))
    return out


# --------------------------------------------------------------------------- CLI


def valid_date(value: str) -> str:
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a valid YYYY-MM-DD date, got {value!r}")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-q", "--query", action="append", default=[], help="product/vendor words (repeatable, OR between -q)")
    parser.add_argument("--cve", action="append", default=[], help="CVE ID (repeatable)")
    parser.add_argument("--id", help="KISA notice number (e.g. 2632) or nttId from the source URL")
    parser.add_argument("--vendor", help="filter by normalised vendor (word match, Korean/English aliases)")
    parser.add_argument("--type", help="filter by notice type substring, e.g. '보안 업데이트'")
    parser.add_argument("--since", type=valid_date, help="YYYY-MM-DD (inclusive)")
    parser.add_argument("--until", type=valid_date, help="YYYY-MM-DD (inclusive)")
    parser.add_argument("--limit", type=int, default=20, help="max notices per query (0 = all, default 20)")
    parser.add_argument("--max-rows", type=int, default=15, help="max table rows per notice (0 = all, default 15)")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    parser.add_argument("--kev", action="store_true", help="only notices with a CVE in the CISA KEV catalog")
    parser.add_argument("--sort", choices=("date", "risk"), default="date", help="order results (risk = KEV, EPSS, CVSS)")
    parser.add_argument("--stats", action="store_true", help="print counts by type/vendor/month")
    parser.add_argument("--doctor", action="store_true", help="check runtime and data freshness, then exit")
    parser.add_argument("--lang", choices=("ko", "en"), default=default_lang())
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.since and args.until and args.since > args.until:
        parser.error(f"--since {args.since} is after --until {args.until}")
    if args.limit < 0 or args.max_rows < 0:
        parser.error("--limit and --max-rows must be 0 (all) or positive")
    bad = [c for c in args.cve if not CVE_RE.fullmatch(c.strip())]
    if bad:
        parser.error(f"invalid CVE id(s): {', '.join(bad)}")
    args.cve = [c.strip() for c in args.cve]
    if any(not q.split() for q in args.query) or (args.vendor is not None and not args.vendor.split()):
        parser.error("-q/--vendor must not be blank")
    args.query = [" ".join(q.split()) for q in args.query]
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    data = mark_later_fixes(merge_pre_notice(load(args.data), load_pre_notice(args.data.parent / PRE_NOTICE_FILE)))
    labels = LABELS[args.lang]
    if args.doctor:
        sys.stdout.write("\n".join(render_doctor(data, labels, dt.date.today())) + "\n")
        return 0
    meta = data.get("cve_meta", {})
    vendor_query = build_query(args.vendor) if args.vendor else None
    advisories = [a for a in data["advisories"] if passes_filters(a, args, vendor_query, meta)]
    if args.sort == "risk":
        advisories = sorted(advisories, key=lambda a: risk_key(risk_of(a["cves"], meta)), reverse=True)
    filtered = bool(args.since or args.until or args.vendor or args.type or args.kev)
    cov = data.get("coverage", {})
    groups = run_matches(advisories, args)

    if args.format == "json":
        json.dump(json_payload(data, groups, advisories, args), sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0

    coverage = labels["coverage"].format(first=cov.get("first"), last=cov.get("last"), count=cov.get("count"))
    sources, pre_line = risk_sources_line(data, labels), pre_notice_line(data, labels)
    out = [f"> {coverage}"] + [f"> {line}" for line in (sources, pre_line) if line] + [""]
    if args.stats:
        out += render_stats(advisories, labels) + [""]
    if groups:
        for key, found in groups:
            out += [f"## {labels['query']}: {key} — {labels['found'].format(n=len(found))}", ""]
            if not found:
                out += [labels["none_filtered" if filtered else "none"], ""]
                continue
            shown = limit(found, args.limit)
            for advisory, kind, rows in shown:
                out += render_advisory(advisory, kind, rows, args, labels, meta)
            if len(shown) < len(found):
                out += [labels["more_items"].format(n=len(found) - len(shown)), ""]
    elif not args.stats or filtered:
        shown = limit(advisories, args.limit)
        out += render_brief(shown, labels, meta)
        if len(shown) < len(advisories):
            out.append(labels["more_items"].format(n=len(advisories) - len(shown)))
    sys.stdout.write("\n".join(out).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
