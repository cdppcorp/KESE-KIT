#!/usr/bin/env python3
"""Query KISA security notices bundled with the kesekit-advisory skills.

Examples:
  python advisory_lookup.py -q nginx -q "Fortinet FortiOS"          # product exposure lookup
  python advisory_lookup.py --cve CVE-2025-0282                     # is this CVE in a KISA notice?
  python advisory_lookup.py --since 2026-10-15 --limit 0            # briefing: notices since a date
  python advisory_lookup.py --vendor Cisco --limit 5
  python advisory_lookup.py --id 2632 --max-rows 0                  # one notice (number or nttId), every row
  python advisory_lookup.py --stats

A query matches when every word appears in the notice. Each result says where it matched:
title/vendor (all rows shown), table rows (only matching rows shown, hidden rows counted),
or body text only (product mentioned in the notice text but not in its version table).

Standard library only (Python 3.8+). Data: ../references/kisa-advisories/advisories.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = SCRIPT_DIR.parent / "references" / "kisa-advisories" / "advisories.json"
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.I)
ROW_FIELDS = ("cve", "vendor", "product", "ecosystem", "affected", "fixed", "severity")
REQUIRED_STR = ("no", "date", "type", "title", "vendor", "url", "summary")
REQUIRED_LIST = ("cves", "affected")
MATCH_RANK = {"title": 3, "rows": 2, "body": 1}

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
ALIASES = {member: [o for o in group if o != member] for group in ALIAS_GROUPS for member in group}

LABELS = {
    "ko": {
        "coverage": "데이터 기준: {first} ~ {last} (KISA 보호나라 보안공지 {count}건)",
        "query": "질의",
        "found": "{n}건",
        "none": "일치하는 공지 없음 — 데이터 기준일 이후 공지는 보호나라에서 직접 확인하세요. 없다고 안전하다는 뜻은 아닙니다.",
        "none_filtered": "일치하는 공지 없음 (--since/--until/--vendor/--type 필터 적용 중)",
        "source": "원문",
        "match": "일치",
        "match_title": "제목·벤더 (전체 행 표시)",
        "match_rows": "표 행 {shown}/{total}행",
        "match_body": "본문 언급 (버전 표에는 해당 제품 행 없음 — 원문 확인)",
        "summary": "요약",
        "cves": "CVE",
        "attachments": "첨부",
        "more_rows": "… {n}행 생략 (전체: --id {id} --max-rows 0)",
        "hidden_rows": "… 질의와 무관한 행 {n}개 숨김 (전체: --id {id})",
        "more_items": "… {n}건 더 있음 (--limit 0 으로 전체 보기)",
        "cols": {"cve": "CVE", "vendor": "제조사", "product": "제품", "ecosystem": "생태계",
                 "affected": "영향받는 버전", "fixed": "해결 버전", "severity": "심각도"},
        "brief_cols": "| 게시일 | 번호 | 유형 | 벤더 | 제목 | CVE 수 |",
        "stats_type": "유형별", "stats_vendor": "벤더 상위", "stats_month": "월별",
    },
    "en": {
        "coverage": "Data coverage: {first} ~ {last} ({count} KISA Boho-nara notices)",
        "query": "Query",
        "found": "{n} notice(s)",
        "none": "No matching notice — check Boho-nara directly for notices after the coverage date. No match does not mean safe.",
        "none_filtered": "No matching notice (--since/--until/--vendor/--type filters are active)",
        "source": "Source",
        "match": "Matched in",
        "match_title": "title/vendor (all rows shown)",
        "match_rows": "table rows {shown}/{total}",
        "match_body": "body text only (no row for this product in the version table — read the notice)",
        "summary": "Summary",
        "cves": "CVEs",
        "attachments": "Attachments",
        "more_rows": "… {n} more row(s) (all rows: --id {id} --max-rows 0)",
        "hidden_rows": "… {n} row(s) unrelated to the query hidden (all rows: --id {id})",
        "more_items": "… {n} more notice(s) (use --limit 0 for all)",
        "cols": {"cve": "CVE", "vendor": "Vendor", "product": "Product", "ecosystem": "Ecosystem",
                 "affected": "Affected", "fixed": "Fixed", "severity": "Severity"},
        "brief_cols": "| Date | No. | Type | Vendor | Title | CVEs |",
        "stats_type": "By type", "stats_vendor": "Top vendors", "stats_month": "By month",
    },
}


def default_lang() -> str:
    return "ko" if "skills-ko" in SCRIPT_DIR.parts else "en"


# --------------------------------------------------------------------------- data loading


def load(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"error: data file not found: {path}")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"error: cannot read {path}: {exc}")
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("advisories"), list):
        raise SystemExit(f"error: unsupported data schema in {path}")
    for index, advisory in enumerate(data["advisories"]):
        problem = record_problem(advisory)
        if problem:
            raise SystemExit(f"error: {path}: advisory #{index} {problem}")
    return data


def record_problem(advisory: object) -> str | None:
    if not isinstance(advisory, dict):
        return "is not an object"
    for key in REQUIRED_STR:
        if not isinstance(advisory.get(key), str):
            return f"field '{key}' must be a string"
    for key in REQUIRED_LIST:
        if not isinstance(advisory.get(key), list):
            return f"field '{key}' must be a list"
    if not all(isinstance(row, dict) for row in advisory["affected"]):
        return "field 'affected' must contain objects"
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
    return ("title", advisory["affected"]) if ident in (advisory["no"], advisory.get("ntt")) else None


def vendor_matches(advisory: dict, variants: list[list[list[re.Pattern]]]) -> bool:
    return any(all(token_hits(t, advisory["vendor"]) for t in v) for v in variants)


def passes_filters(advisory: dict, args: argparse.Namespace, vendor_query) -> bool:
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


def render_rows(rows: list[dict], args: argparse.Namespace, labels: dict, ident: str) -> list[str]:
    cols = [f for f in ROW_FIELDS if any(r.get(f) for r in rows)]
    if not cols:
        return []
    shown = limit(rows, args.max_rows)
    out = ["| " + " | ".join(labels["cols"][c] for c in cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(md(r.get(c, "")) for c in cols) + " |" for r in shown]
    if len(rows) > len(shown):
        out.append(labels["more_rows"].format(n=len(rows) - len(shown), id=ident))
    return out


def match_label(kind: str, rows: list[dict], advisory: dict, labels: dict) -> str:
    if kind == "rows":
        return labels["match_rows"].format(shown=len(rows), total=len(advisory["affected"]))
    return labels["match_" + kind]


def render_advisory(advisory: dict, kind: str, rows: list[dict], args: argparse.Namespace, labels: dict) -> list[str]:
    a = advisory
    ident = ref_id(a)
    number = a["no"] if a["no"].isdigit() else f"{a['no']} (nttId {a.get('ntt', '?')})"
    out = [
        f"### [{a['date']}] #{number} {a['title']} ({a['type']})",
        f"- {labels['source']}: {a['url'] or '-'}",
        f"- {labels['match']}: {match_label(kind, rows, a, labels)}",
    ]
    if a["summary"]:
        out.append(f"- {labels['summary']}: {a['summary']}")
    if a["cves"]:
        cves = a["cves"] if len(a["cves"]) <= 12 else a["cves"][:12] + [f"… +{len(a['cves']) - 12}"]
        out.append(f"- {labels['cves']}: {', '.join(cves)}")
    if a.get("attachments"):
        out.append(f"- {labels['attachments']}: {', '.join(a['attachments'])}")
    table = render_rows(rows, args, labels, ident)
    if table:
        out += [""] + table
    hidden = len(a["affected"]) - len(rows)
    if kind == "rows" and hidden > 0:
        out.append(labels["hidden_rows"].format(n=hidden, id=ident))
    return out + [""]


def render_brief(items: list[dict], labels: dict) -> list[str]:
    out = [labels["brief_cols"], "|---|---|---|---|---|:-:|"]
    out += [
        f"| {a['date']} | {a['no']} | {md(a['type'])} | {md(a['vendor'])} | {md(a['title'])} | {len(a['cves'])} |"
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


def slim(advisory: dict) -> dict:
    """Advisory without bulky fields, for JSON output."""
    out = {k: v for k, v in advisory.items() if k not in ("affected", "tables", "text")}
    out["rows_total"] = len(advisory["affected"])
    return out


def json_payload(cov: dict, groups: list, advisories: list[dict], args: argparse.Namespace) -> dict:
    if not groups:
        shown = limit(advisories, args.limit)
        return {"coverage": cov, "total": len(advisories), "truncated": len(shown) < len(advisories),
                "advisories": [slim(a) for a in shown]}
    results = []
    for key, found in groups:
        shown = limit(found, args.limit)
        matches = []
        for advisory, kind, rows in shown:
            kept = limit(rows, args.max_rows)
            matches.append({**slim(advisory), "match": kind, "rows_matched": len(rows),
                            "rows_truncated": len(kept) < len(rows), "rows": kept})
        results.append({"query": key, "total": len(found), "truncated": len(shown) < len(found), "matches": matches})
    return {"coverage": cov, "results": results}


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
    parser.add_argument("--stats", action="store_true", help="print counts by type/vendor/month")
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
    data = load(args.data)
    labels = LABELS[args.lang]
    vendor_query = build_query(args.vendor) if args.vendor else None
    advisories = [a for a in data["advisories"] if passes_filters(a, args, vendor_query)]
    filtered = bool(args.since or args.until or args.vendor or args.type)
    cov = data.get("coverage", {})
    groups = run_matches(advisories, args)

    if args.format == "json":
        json.dump(json_payload(cov, groups, advisories, args), sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0

    coverage = labels["coverage"].format(first=cov.get("first"), last=cov.get("last"), count=cov.get("count"))
    out = [f"> {coverage}", ""]
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
                out += render_advisory(advisory, kind, rows, args, labels)
            if len(shown) < len(found):
                out += [labels["more_items"].format(n=len(found) - len(shown)), ""]
    elif not args.stats or filtered:
        shown = limit(advisories, args.limit)
        out += render_brief(shown, labels)
        if len(shown) < len(advisories):
            out.append(labels["more_items"].format(n=len(advisories) - len(shown)))
    sys.stdout.write("\n".join(out).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
