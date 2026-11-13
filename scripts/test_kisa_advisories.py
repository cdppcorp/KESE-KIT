"""Tests for scripts/build_kisa_advisories.py and the kesekit-advisory lookup script.

Run: python -m unittest discover -s scripts -p "test_*.py"
"""

from __future__ import annotations

import contextlib
import csv
import gzip
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


build = load_module("build_kisa_advisories", ROOT / "scripts" / "build_kisa_advisories.py")
lookup = load_module("advisory_lookup", ROOT / "skills-ko" / "kesekit-advisory-ko" / "scripts" / "advisory_lookup.py")
fetch = load_module("fetch_cve_enrichment", ROOT / "scripts" / "fetch_cve_enrichment.py")

IVANTI_TABLE = """
<p>□ 영향받는 제품 및 해결 방안</p>
<table>
 <tr><td>취약점</td><td>제품명</td><td>영향받는 버전</td><td>해결 버전</td></tr>
 <tr><td rowspan="2">CVE-2025-0282</td><td>Ivanti Connect Secure</td><td>22.7R2 이상 ~ 22.7R2.4 이하</td><td>22.7R2.5</td></tr>
 <tr><td>Ivanti Policy Secure</td><td>22.7R1 이상 ~ 22.7R1.2 이하</td><td>22.7R1.3</td></tr>
 <tr><td>CVE-2025-0283</td><td colspan="2">Ivanti Neurons<br>(ZTA 게이트웨이)</td><td>22.8R2</td></tr>
</table>
"""


class ExpandGridTest(unittest.TestCase):
    def test_rowspan_is_carried_to_following_rows(self):
        grid = build.parse_tables(IVANTI_TABLE)[0]
        self.assertEqual(grid[2][0], "CVE-2025-0282")
        self.assertEqual(grid[2][1], "Ivanti Policy Secure")

    def test_colspan_duplicates_cell_and_br_becomes_space(self):
        grid = build.parse_tables(IVANTI_TABLE)[0]
        self.assertEqual(grid[3][1:3], ["Ivanti Neurons (ZTA 게이트웨이)"] * 2)

    def test_grid_is_rectangular(self):
        grid = build.parse_tables("<table><tr><td>a</td><td>b</td></tr><tr><td>c</td></tr></table>")[0]
        self.assertEqual(grid, [["a", "b"], ["c", ""]])

    def test_empty_tr_consumes_rowspan(self):
        # Oracle #2180 regression: an empty <tr> inside a rowspan must not shift later rows.
        html = (
            "<table><tr><td>취약점</td><td>제품명</td><td>영향받는 버전</td><td>해결 버전</td></tr>"
            "<tr><td rowspan='3'>CVE-2021-35587</td><td rowspan='2'>OFM</td><td>11.1</td><td>migrate</td></tr>"
            "<tr></tr>"
            "<tr><td>OFM</td><td>12.2.1.3.0</td><td>Patch 33752617</td></tr></table>"
        )
        grid = build.parse_tables(html)[0]
        self.assertEqual(grid[-1], ["CVE-2021-35587", "OFM", "12.2.1.3.0", "Patch 33752617"])
        rows, _, lost = build.table_to_rows(grid)
        self.assertEqual(lost, 0)
        self.assertIn("12.2.1.3.0", [r["affected"] for r in rows])

    def test_rowspan_and_colspan_on_same_cell(self):
        html = "<table><tr><td rowspan='2' colspan='2'>X</td><td>a</td></tr><tr><td>b</td></tr></table>"
        self.assertEqual(build.parse_tables(html)[0], [["X", "X", "a"], ["X", "X", "b"]])

    def test_unclosed_table_is_flushed(self):
        self.assertEqual(build.parse_tables("<table><tr><td>a</td><td>b</td>"), [[["a", "b"]]])

    def test_nested_table_is_collected_separately(self):
        html = "<table><tr><td>wrap <table><tr><td>제품명</td><td>영향받는 버전</td></tr></table></td></tr></table>"
        tables = build.parse_tables(html)
        self.assertEqual(len(tables), 2)
        self.assertEqual(tables[0], [["제품명", "영향받는 버전"]])


class HeaderAndRowsTest(unittest.TestCase):
    def test_classify_header_variants(self):
        cases = {
            "취약점": "cve",
            "CVE 번호": "cve",
            "CVE 제목": "description",
            "제품명": "product",
            "제품 카테고리": "product",
            "영향받는 버전": "affected",
            "영향 버전": "affected",
            "해결 버전": "fixed",
            "해결버전": "fixed",
            "조치 방안": "fixed",
            "제조사명": "vendor",
            "최신 버전": "fixed",
            "안전한 버전": "fixed",
            "생태계": "ecosystem",
            "중요도": "severity",
            "": None,
        }
        for header, expected in cases.items():
            with self.subTest(header=header):
                self.assertEqual(build.classify_header(header), expected)

    def test_table_to_rows_maps_columns(self):
        rows, unmapped, lost = build.table_to_rows(build.parse_tables(IVANTI_TABLE)[0])
        self.assertIsNone(unmapped)
        self.assertEqual(lost, 0)
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            rows[1],
            {"cve": "CVE-2025-0282", "product": "Ivanti Policy Secure",
             "affected": "22.7R1 이상 ~ 22.7R1.2 이하", "fixed": "22.7R1.3"},
        )

    def test_cve_is_extracted_when_table_has_no_cve_column(self):
        grid = [["제품명", "영향받는 버전", "주요 취약점 내용"], ["Foo", "1.0 이하", "RCE (CVE-2026-1234)"]]
        rows, _, _ = build.table_to_rows(grid)
        self.assertEqual(rows[0]["cve"], "CVE-2026-1234")

    def test_vulnerability_type_in_cve_column_becomes_description(self):
        grid = [["취약점", "제품명", "영향받는 버전"], ["파일 업로드", "Foo", "1.0 이하"]]
        rows, _, _ = build.table_to_rows(grid)
        self.assertEqual(rows[0], {"description": "파일 업로드", "product": "Foo", "affected": "1.0 이하"})

    def test_caption_row_is_not_header(self):
        grid = [["영향받는 제품 및 버전"] * 3, ["제품명", "영향받는 버전", "해결 버전"], ["Foo", "1.0", "1.1"]]
        self.assertEqual(build.find_header(grid), 1)

    def test_cells_under_blank_header_are_counted_as_lost(self):
        grid = [["제품명", "영향받는 버전", ""], ["Foo", "1.0", "stray"]]
        self.assertEqual(build.table_to_rows(grid)[2], 1)

    def test_layout_wrapper_is_not_a_data_table(self):
        self.assertFalse(build.is_data_table([["□ 개요 o 긴 본문 ..."]]))
        self.assertTrue(build.is_data_table([["a", "b"]]))

    def test_long_cells_are_not_treated_as_header(self):
        grid = [["□ 개요 " + "x" * 80 + " 제품명 영향받는 버전"], ["data"]]
        self.assertIsNone(build.find_header(grid))


class TextHelpersTest(unittest.TestCase):
    def test_vendor_from_title(self):
        cases = {
            "MS 11월 보안 위협에 따른 정기 보안 업데이트 권고": "Microsoft",
            "Ivanti 제품 보안 업데이트 권고": "Ivanti",
            "포티넷 제품 보안 업데이트 권고": "Fortinet",
            "WordPress 플러그인 보안 업데이트 권고": "WordPress",
            "라온위즈(주) 제품 보안 업데이트 권고": "라온위즈",
            "PHP 보안취약점(PHP2Shell) 관련 기업 보안 대응 수칙": "PHP",
            "MS社 제품 보안 업데이트 권고": "Microsoft",
            "카드 배송 사칭 보이스피싱·스미싱 주의 권고": "기타",
            "국내 중소기업 대상 신규 랜섬웨어 공격 확산에 따른 보안 권고문": "기타",
        }
        for title, expected in cases.items():
            with self.subTest(title=title):
                self.assertEqual(build.vendor_from_title(title), expected)

    def test_make_summary_prefers_description_section(self):
        text = "제목\n게시일: x\n\n□ 개요  o 개요 내용  □ 설명  o 설명 내용 (CVE-2026-1)  □ 참고사이트 [1] url"
        self.assertEqual(build.make_summary(text), "o 설명 내용 (CVE-2026-1)")

    def test_extract_refs(self):
        text = (
            "제목\n원문: https://www.boho.or.kr/x\n\n□ 개요 o 발표 [1] 다운로드: https://vendor.example/dl.exe) "
            "□ 참고사이트 [1] https://www.php.net/archive/2026.php#2026-10-23-1 ［2］ https://nvd.nist.gov/vuln/detail/CVE-2026-1, "
            "[1] https://www.php.net/archive/2026.php#2026-10-23-1 https://example.org/a에서"
        )
        self.assertEqual(
            build.extract_refs(text),
            [
                {"n": "1", "url": "https://www.php.net/archive/2026.php#2026-10-23-1"},
                {"n": "2", "url": "https://nvd.nist.gov/vuln/detail/CVE-2026-1"},
                {"url": "https://vendor.example/dl.exe"},
                {"url": "https://example.org/a"},
            ],
        )

    def test_extract_refs_ignores_header_source_url(self):
        self.assertEqual(build.extract_refs("제목\n원문: https://www.boho.or.kr/x\n\n본문만"), [])

    def test_clip_adds_ellipsis(self):
        self.assertEqual(build.clip("abcdef", 4), "abc…")


class RecordAndOutputTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.source = Path(self.tmp.name) / "src"
        folder = self.source / "2025/01/2025-01-13_2117_Ivanti 제품 보안 업데이트 권고"
        folder.mkdir(parents=True)
        (folder / "본문.txt").write_text(
            "Ivanti 제품 보안 업데이트 권고\n게시일: 2025-01-13\n\n□ 설명  o 버퍼 오버플로우(CVE-2025-0282)",
            encoding="utf-8",
        )
        hidden = '<a href="https://nvd.nist.gov/vuln/detail/CVE-2024-11639"></a>'
        (folder / "본문.html").write_text(IVANTI_TABLE + hidden, encoding="utf-8")
        with (self.source / "목록.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["연도", "게시일", "번호", "유형", "제목", "조회수(수집시점)", "첨부개수", "첨부파일명", "폴더경로", "원문링크"])
            writer.writerow(["2025", "2025-01-13", "2117", "보안 업데이트 권고", "Ivanti 제품 보안 업데이트 권고", "1", "0", "",
                             "2025/01/2025-01-13_2117_Ivanti 제품 보안 업데이트 권고/",
                             "https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71627"])

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_record_ignores_hidden_link_cves(self):
        record = build.build_records(self.source)[0]
        self.assertEqual(record["vendor"], "Ivanti")
        self.assertEqual(record["ntt"], "71627")
        self.assertIn("버퍼 오버플로우", record["text"])
        self.assertEqual(record["refs"], [])
        self.assertIn("CVE-2025-0283", record["cves"])  # from the table
        self.assertNotIn("CVE-2024-11639", record["cves"])  # hidden <a href> residue
        self.assertEqual(len(record["affected"]), 3)

    def test_unexpected_url_is_dropped_with_warning(self):
        row = build.load_index(self.source)[0]
        record, issues = build.build_record({**row, "원문링크": "javascript:alert(1)"}, self.source)
        self.assertEqual(record["url"], "")
        self.assertTrue(any("unexpected source URL" in i for i in issues))

    def test_enrichment_is_embedded_for_dataset_cves_only(self):
        out = Path(self.tmp.name) / "out2"
        out.mkdir()
        (out / "overview.md").write_text(f"{build.STATS_BEGIN}\n{build.STATS_END}\n", encoding="utf-8")
        enrichment = (
            {"kev": {"version": "2026.11.10"}, "epss": {"date": "2026-11-13"}},
            {"CVE-2025-0282": {"kev": "2025-01-08", "epss": 0.99}, "CVE-1999-0001": {"epss": 0.1}},
        )
        stats = build.write_outputs(build.build_records(self.source), {"ko": out}, enrichment)
        data = json.loads((out / "advisories.json").read_text(encoding="utf-8"))
        self.assertEqual(list(data["cve_meta"]), ["CVE-2025-0282"])
        self.assertEqual(data["risk_sources"]["kev"]["version"], "2026.11.10")
        self.assertEqual(stats["kev_cves"], 1)
        self.assertIn("KEV 등재 **1개**", (out / "overview.md").read_text(encoding="utf-8"))

    def test_load_enrichment_drops_malformed_values(self):
        path = Path(self.tmp.name) / "enrichment.json"
        path.write_text(json.dumps({"sources": {"nvd": {"fetched": 3}}, "cves": {
            "CVE-2026-1001": {"kev": "2026-01-01", "epss": 1.5, "pct": 0.9, "cvss": "9.8", "cwe": ["CWE-79", 7]},
            "not-a-cve": {"epss": 0.5},
            "CVE-2026-1002": {"epss": True},
        }}), encoding="utf-8")
        sources, risk = build.load_enrichment(path)
        self.assertEqual(sources, {"nvd": {"fetched": 3}})
        self.assertEqual(risk, {"CVE-2026-1001": {"kev": "2026-01-01", "pct": 0.9, "cwe": ["CWE-79"]}})
        self.assertEqual(build.load_enrichment(Path(self.tmp.name) / "missing.json"), ({}, {}))

    def test_write_outputs_creates_json_index_and_stats(self):
        out = Path(self.tmp.name) / "out"
        out.mkdir()
        (out / "overview.md").write_text(f"# x\n{build.STATS_BEGIN}\nold\n{build.STATS_END}\n", encoding="utf-8")
        stats = build.write_outputs(build.build_records(self.source), {"ko": out})
        self.assertEqual(stats["total"], 1)
        self.assertNotIn(b"\r", (out / "advisories.json").read_bytes())  # LF on every OS
        raw = (out / "advisories.json").read_text(encoding="utf-8")
        data = json.loads(raw)
        self.assertEqual(data["coverage"]["count"], len(data["advisories"]))
        self.assertEqual(len(raw.splitlines()), 4)  # header + empty cve_meta, advisories opener, one advisory, closer
        self.assertIn("## Ivanti (1)", (out / "vendor-index.md").read_text(encoding="utf-8"))
        overview = (out / "overview.md").read_text(encoding="utf-8")
        self.assertIn("총 **1건**", overview)
        self.assertNotIn("old", overview)


def advisory(no, date, title, vendor, affected=(), cves=(), summary="", text="", ntt="", refs=()):
    return {"no": no, "ntt": ntt or no, "date": date, "type": "보안 업데이트 권고", "title": title, "vendor": vendor,
            "url": f"u{no}", "folder": f"f{no}/", "attachments": [], "summary": summary, "cves": list(cves),
            "affected": list(affected), "text": text, "refs": list(refs)}


SAMPLE_DATA = {
    "schema": 1,
    "coverage": {"first": "2026-01-01", "last": "2026-03-01", "count": 6},
    "advisories": [
        advisory("3", "2026-03-01", "PHP 보안 업데이트 권고", "PHP", cves=["CVE-2026-3"], summary="PHP 취약점",
                 refs=[{"n": "1", "url": "https://www.php.net/x"}, {"url": "https://nvd.nist.gov/y"}],
                 affected=[{"cve": "CVE-2026-3", "product": "PHP", "affected": "8.3.0 이상 8.3.9 미만", "fixed": "8.3.9"}]),
        advisory("2", "2026-02-01", "F5 제품 보안 업데이트 권고", "F5", cves=["CVE-2026-2", "CVE-2026-9"],
                 affected=[{"cve": "CVE-2026-2", "product": "NGINX Open Source", "affected": "1.30.5 이하", "fixed": "1.30.6"},
                           {"cve": "CVE-2026-9", "product": "BIG-IP", "affected": "17.1.0", "fixed": "17.1.1"}]),
        advisory("1", "2026-01-01", "리눅스 커널 보안 업데이트 권고", "Linux Kernel"),
        advisory("4", "2026-01-10", "Fortinet 제품 보안 업데이트 권고", "Fortinet", cves=["CVE-2026-21359", "CVE-2026-2135"],
                 affected=[{"cve": "CVE-2026-21359", "product": "FortiOS", "affected": "7.4.0 이상 7.4.3 이하", "fixed": "7.4.4"},
                           {"cve": "CVE-2026-2135", "product": "FortiProxy", "affected": "7.2.0", "fixed": "7.2.1"}]),
        advisory("5", "2026-01-20", "구글 Chrome 브라우저 보안 업데이트 권고", "Google",
                 affected=[{"product": "Google Chrome", "affected": "140 이하", "fixed": "141"}]),
        advisory("공지", "2026-01-05", "Linux 제품 보안 업데이트 권고", "Linux", ntt="72207",
                 text="Ubuntu, Debian 배포판별 업데이트 확인 ASP.NET Core",
                 affected=[{"product": "sudo", "affected": "1.9.16 이하", "fixed": "미배포(차기 정기 업데이트 예정)"}]),
    ],
    "risk_sources": {"kev": {"version": "2026.11.10"}, "epss": {"date": "2026-11-13"}},
    "cve_meta": {
        "CVE-2026-2135": {"kev": "2026-01-15", "ransomware": True, "epss": 0.9, "pct": 0.9999},
        "CVE-2026-21359": {"epss": 0.2, "pct": 0.95, "cvss": 9.8},
        "CVE-2026-3": {"epss": 0.01, "pct": 0.5},
    },
}


class LookupTest(unittest.TestCase):
    def setUp(self):
        self.advisories = SAMPLE_DATA["advisories"]

    def by_no(self, no):
        return next(a for a in self.advisories if a["no"] == no)

    def query(self, no, term):
        return lookup.match_query(self.by_no(no), lookup.build_query(term))

    def test_phrase_boundaries(self):
        cases = [("HP", "PHP 보안 업데이트", False), ("HP", "HP LaserJet", True), (".NET", "ASP.NET Core", True),
                 ("C++", "Visual C++2022", True), ("Node.js", "Node.js 22", True),
                 ("Apache HTTP Server", "Apache\xa0HTTP  Server", True), ("리눅스", "리눅스커널", True)]
        for term, text, expected in cases:
            with self.subTest(term=term, text=text):
                self.assertEqual(bool(lookup.compile_phrase(term).search(text)), expected)

    def test_korean_and_english_aliases(self):
        self.assertEqual(self.query("1", "linux kernel")[0], "title")
        self.assertEqual(self.query("5", "Google Chrome")[0], "title")
        self.assertEqual(self.query("5", "구글")[0], "title")
        self.assertIsNotNone(lookup.match_query(self.by_no("1"), lookup.build_query("리눅스")))

    def test_vendor_plus_product_query_narrows_to_product_rows(self):
        kind, rows = self.query("4", "Fortinet FortiOS")
        self.assertEqual(kind, "rows")
        self.assertEqual([r["product"] for r in rows], ["FortiOS"])

    def test_query_narrows_rows_when_title_does_not_match(self):
        kind, rows = self.query("2", "nginx")
        self.assertEqual((kind, [r["product"] for r in rows]), ("rows", ["NGINX Open Source"]))

    def test_vendor_match_returns_all_rows(self):
        kind, rows = self.query("4", "Fortinet")
        self.assertEqual((kind, len(rows)), ("title", 2))

    def test_body_only_mention_is_found_and_flagged(self):
        kind, rows = self.query("공지", "Ubuntu")
        self.assertEqual((kind, len(rows)), ("body", 1))
        self.assertIsNone(self.query("3", "Ubuntu"))

    def test_match_cve_is_exact(self):
        kind, rows = lookup.match_cve(self.by_no("4"), "cve-2026-2135")
        self.assertEqual((kind, [r["product"] for r in rows]), ("rows", ["FortiProxy"]))
        self.assertIsNone(lookup.match_cve(self.by_no("3"), "CVE-2026-9"))

    def test_vendor_filter_uses_word_match_and_aliases(self):
        args = lookup.parse_args([])
        self.assertTrue(lookup.vendor_matches(self.by_no("5"), lookup.build_query("구글")))
        self.assertFalse(lookup.vendor_matches(self.by_no("3"), lookup.build_query("HP")))
        self.assertTrue(lookup.passes_filters(self.by_no("3"), args, None))

    def run_main(self, *argv: str) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "advisories.json"
            data.write_text(json.dumps(SAMPLE_DATA, ensure_ascii=False), encoding="utf-8")
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = lookup.main([*argv, "--data", str(data)])
            self.assertEqual(code, 0)
            return buffer.getvalue()

    def test_main_json_output_for_query(self):
        result = json.loads(self.run_main("-q", "nginx", "--format", "json"))
        group = result["results"][0]
        self.assertEqual((group["total"], group["truncated"]), (1, False))
        match = group["matches"][0]
        self.assertEqual((match["no"], match["match"], match["rows_total"], match["rows_matched"]), ("2", "rows", 2, 1))
        self.assertNotIn("affected", match)
        self.assertNotIn("text", match)

    def test_main_json_reports_truncation(self):
        result = json.loads(self.run_main("-q", "Fortinet", "--format", "json", "--max-rows", "1"))
        match = result["results"][0]["matches"][0]
        self.assertEqual((len(match["rows"]), match["rows_truncated"]), (1, True))
        brief = json.loads(self.run_main("--format", "json", "--limit", "2"))
        self.assertEqual((brief["total"], brief["truncated"], len(brief["advisories"])), (6, True, 2))

    def test_main_markdown_counts_hidden_rows(self):
        out = self.run_main("-q", "nginx", "--lang", "en")
        self.assertIn("table rows 1/2", out)
        self.assertIn("1 row(s) unrelated to the query hidden", out)

    def test_references_are_rendered(self):
        out = self.run_main("--id", "3")
        self.assertIn("- 참고사이트:\n  - [1] https://www.php.net/x\n  - https://nvd.nist.gov/y", out)
        match = json.loads(self.run_main("--id", "3", "--format", "json"))["results"][0]["matches"][0]
        self.assertEqual(match["refs"][0]["url"], "https://www.php.net/x")

    def test_local_folder_shown_only_when_archive_exists(self):
        original = lookup.REPO_SOURCE
        with tempfile.TemporaryDirectory() as tmp:
            lookup.REPO_SOURCE = Path(tmp)
            try:
                self.assertIsNone(lookup.local_folder(self.by_no("3")))
                (Path(tmp) / "f3").mkdir()
                self.assertEqual(lookup.local_folder(self.by_no("3")), str(Path(tmp) / "f3/"))
            finally:
                lookup.REPO_SOURCE = original

    def test_risk_aggregation(self):
        risk = lookup.risk_of(["CVE-2026-21359", "CVE-2026-2135", "CVE-2026-404"], SAMPLE_DATA["cve_meta"])
        self.assertEqual(risk["kev"], ["CVE-2026-2135"])
        self.assertTrue(risk["ransomware"])
        self.assertEqual((risk["cvss"], risk["cvss_cve"]), (9.8, "CVE-2026-21359"))
        self.assertEqual((risk["epss"], risk["epss_cve"]), (0.9, "CVE-2026-2135"))
        self.assertEqual(lookup.compact_risk(risk), "KEV · CVSS 9.8 · EPSS 0.90")
        self.assertEqual(lookup.risk_of(["CVE-2026-404"], SAMPLE_DATA["cve_meta"]), {})

    def test_risk_signals_in_markdown(self):
        out = self.run_main("--id", "4")
        self.assertIn("> 위험 지표 기준: KEV 2026.11.10 · EPSS 2026-11-13 · NVD CVSS 미수집", out)
        self.assertIn("KEV 등재 1건 (CVE-2026-2135) · 랜섬웨어 악용 · 최고 CVSS 9.8 (CVE-2026-21359)", out)
        self.assertIn("(상위 <0.1%, CVE-2026-2135)", out)
        self.assertIn("| CVE-2026-2135 | FortiProxy | 7.2.0 | 7.2.1 | KEV · EPSS 0.90 |", out)

    def test_kev_filter_and_risk_sort(self):
        out = self.run_main("--kev", "--lang", "en")
        self.assertIn("| 2026-01-10 | 4 |", out)
        self.assertNotIn("| 2026-03-01 | 3 |", out)
        ranked = self.run_main("--sort", "risk", "--lang", "en").splitlines()
        rows = [line for line in ranked if line.startswith("| 2026")]
        self.assertTrue(rows[0].startswith("| 2026-01-10 | 4 |"))  # KEV first
        self.assertTrue(rows[1].startswith("| 2026-03-01 | 3 |"))  # then EPSS 0.01, then no signals by date

    def test_pending_fix_warning(self):
        self.assertTrue(lookup.is_pending(self.by_no("공지")))
        self.assertFalse(lookup.is_pending(self.by_no("3")))
        self.assertIn("fix not released", self.run_main("--id", "72207", "--lang", "en"))

    def test_json_includes_risk(self):
        match = json.loads(self.run_main("--id", "4", "--format", "json"))["results"][0]["matches"][0]
        self.assertEqual(match["risk"]["kev"], ["CVE-2026-2135"])
        self.assertEqual(match["rows"][1]["risk"]["kev"], ["CVE-2026-2135"])
        self.assertNotIn("risk", json.loads(self.run_main("--id", "1", "--format", "json"))["results"][0]["matches"][0])

    def test_doctor_reports_freshness(self):
        import datetime as dt
        with tempfile.TemporaryDirectory() as tmp:
            fresh = lookup.render_doctor(SAMPLE_DATA, lookup.LABELS["en"], dt.date(2026, 11, 20), Path(tmp), Path(tmp) / "x.md")
            text = "\n".join(fresh)
            self.assertIn("[WARN] 6 notices, newest 2026-03-01 (264 day(s) ago)", text)
            self.assertIn("[OK] CISA KEV catalog 2026.11.10\n", text + "\n")  # no release date -> no age
            self.assertIn("[OK] EPSS scores 2026-11-13 (7 day(s) ago)", text)
            self.assertIn("[INFO] NVD CVSS not fetched", text)
            self.assertIn("[INFO] Raw notice archive present", text)
            self.assertIn("[WARN] Threat-response checklist (threat-response.md) missing", text)
            stale = "\n".join(lookup.render_doctor(SAMPLE_DATA, lookup.LABELS["en"], dt.date(2026, 12, 31),
                                                    Path(tmp) / "none", lookup.THREAT_RESPONSE))
            self.assertIn("older than 30 days", stale)
            self.assertIn("[WARN] EPSS scores", stale)
            bare = {**SAMPLE_DATA, "risk_sources": {}}
            self.assertIn("[WARN] No CVE risk signals",
                          "\n".join(lookup.render_doctor(bare, lookup.LABELS["en"], dt.date(2026, 3, 5))))
            future = "\n".join(lookup.render_doctor(SAMPLE_DATA, lookup.LABELS["en"], dt.date(2026, 1, 1)))
            self.assertIn("[OK] EPSS scores 2026-11-13\n", future + "\n")  # clock skew: no negative age

    def test_doctor_cli(self):
        self.assertIn("## 실행 환경 점검", self.run_main("--doctor", "--lang", "ko"))

    def test_id_accepts_ntt_for_pinned_notices(self):
        out = self.run_main("--id", "72207", "--lang", "en")
        self.assertIn("#공지 (nttId 72207)", out)

    def test_main_brief_respects_since_and_limit(self):
        out = self.run_main("--since", "2026-02-01", "--limit", "1", "--lang", "en")
        self.assertIn("| 2026-03-01 | 3 |", out)
        self.assertNotIn("| 2026-02-01 | 2 |", out)
        self.assertIn("1 more notice(s)", out)

    def test_main_reports_no_match(self):
        self.assertIn("일치하는 공지 없음", self.run_main("--cve", "CVE-2020-0001", "--lang", "ko"))
        self.assertIn("filters are active", self.run_main("-q", "PHP", "--until", "2026-01-02", "--lang", "en"))

    def test_invalid_inputs_are_rejected(self):
        bad = (["--since", "2026/01/01"], ["--since", "2026-13-45"], ["--cve", "CVE-12"], ["-q", " "],
               ["--since", "2026-02-01", "--until", "2026-01-01"], ["--limit", "-1"], ["--vendor", ""])
        for argv in bad:
            with self.subTest(argv=argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    lookup.parse_args(argv)


KEV_SAMPLE = json.dumps({
    "catalogVersion": "2026.11.10", "dateReleased": "2026-11-10T19:03:29Z",
    "vulnerabilities": [
        {"cveID": "CVE-2025-0282", "dateAdded": "2025-01-08", "knownRansomwareCampaignUse": "Known"},
        {"cveID": "CVE-2024-0001", "dateAdded": "2024-01-01", "knownRansomwareCampaignUse": "Unknown"},
        {"cveID": "CVE-2026-0002", "dateAdded": "bogus"},
        "junk",
    ],
}).encode()

NVD_SAMPLE = json.dumps({"vulnerabilities": [{"cve": {
    "id": "CVE-2025-0282",
    "metrics": {
        "cvssMetricV31": [
            {"type": "Secondary", "cvssData": {"version": "3.1", "baseScore": 8.0, "baseSeverity": "HIGH"}},
            {"type": "Primary", "cvssData": {"version": "3.1", "baseScore": 9.0, "baseSeverity": "CRITICAL"}},
        ],
        "ssvcV203": [{"source": "x", "ssvcData": {}}],
    },
    "weaknesses": [{"description": [{"value": "CWE-121"}, {"value": "NVD-CWE-noinfo"}]},
                   {"description": [{"value": "CWE-787"}]}],
}}]}).encode()


class FetchEnrichmentTest(unittest.TestCase):
    def test_parse_kev(self):
        found, meta = fetch.parse_kev(KEV_SAMPLE, {"CVE-2025-0282", "CVE-2026-0002"})
        self.assertEqual(found, {"CVE-2025-0282": {"kev": "2025-01-08", "ransomware": True},
                                 "CVE-2026-0002": {"kev": "unknown"}})
        self.assertEqual((meta["catalogVersion"], meta["entries"]), ("2026.11.10", 4))
        with self.assertRaises(ValueError):
            fetch.parse_kev(b"{}", set())

    def test_parse_epss(self):
        csv_text = "#model_version:v2026.06.15,score_date:2026-11-13T12:03:22Z\ncve,epss,percentile\n" \
                   "CVE-2025-0282,0.99981,0.99981\nCVE-2025-0283,1.7,0.5\nCVE-2020-1,0.1,0.2\n"
        found, meta = fetch.parse_epss(gzip.compress(csv_text.encode()), {"CVE-2025-0282", "CVE-2025-0283"})
        self.assertEqual(found, {"CVE-2025-0282": {"epss": 0.99981, "pct": 0.99981}})
        self.assertEqual(meta["score_date"], "2026-11-13T12:03:22Z")
        with self.assertRaises(ValueError):
            fetch.parse_epss(gzip.compress(csv_text.encode()), {"CVE-1999-9999"})

    def test_parse_nvd_prefers_primary_and_skips_non_cvss(self):
        self.assertEqual(fetch.parse_nvd(NVD_SAMPLE),
                         {"cvss": 9.0, "cvss_v": "3.1", "sev": "CRITICAL", "cwe": ["CWE-121", "CWE-787"]})
        self.assertEqual(fetch.parse_nvd(b'{"vulnerabilities": []}'), {})
        v2 = json.dumps({"vulnerabilities": [{"cve": {"metrics": {"cvssMetricV2": [
            {"type": "Primary", "baseSeverity": "HIGH", "cvssData": {"version": "2.0", "baseScore": 7.5}}]}}}]}).encode()
        self.assertEqual(fetch.parse_nvd(v2), {"cvss": 7.5, "cvss_v": "2.0", "sev": "HIGH"})

    def test_merge_keeps_nvd_and_refreshes_kev_epss(self):
        cache = {"CVE-1": {"kev": "2020-01-01", "epss": 0.5, "pct": 0.9, "cvss": 9.8, "nvd": "2026-11-01"},
                 "CVE-OLD": {"epss": 0.1}}
        merged = fetch.merge_risk(cache, {"CVE-1", "CVE-2"}, {}, {"CVE-2": {"epss": 0.2, "pct": 0.8}})
        self.assertEqual(merged, {"CVE-1": {"cvss": 9.8, "nvd": "2026-11-01"}, "CVE-2": {"epss": 0.2, "pct": 0.8}})

    def test_cache_round_trip_is_lf_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data" / "cve-enrichment.json"
            fetch.write_cache(path, {"kev": {"catalogVersion": "x"}}, {"CVE-2": {"epss": 0.2}, "CVE-1": {"kev": "d"}})
            self.assertNotIn(b"\r", path.read_bytes())
            self.assertEqual(path.read_text(encoding="utf-8").splitlines()[1], '"CVE-1":{"kev":"d"},')
            sources, cves = fetch.load_cache(path)
            self.assertEqual((sources["kev"]["catalogVersion"], len(cves)), ("x", 2))


class LoadTest(unittest.TestCase):
    def check_rejected(self, content: str, message: str):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "advisories.json"
            path.write_text(content, encoding="utf-8")
            with self.assertRaises(SystemExit) as ctx:
                lookup.load(path)
            self.assertIn(message, str(ctx.exception))

    def test_load_rejects_bad_data(self):
        self.check_rejected("{not json", "cannot read")
        self.check_rejected("[]", "unsupported data schema")
        self.check_rejected('{"schema": 1, "advisories": [{"no": "1"}]}', "must be a string")
        bad_rows = {"schema": 1, "advisories": [{**SAMPLE_DATA["advisories"][0], "affected": "x"}]}
        self.check_rejected(json.dumps(bad_rows), "must be a list")
        bad_refs = {"schema": 1, "advisories": [{**SAMPLE_DATA["advisories"][0], "refs": [{"n": "1"}]}]}
        self.check_rejected(json.dumps(bad_refs), "field 'refs'")

    def test_load_missing_file(self):
        with self.assertRaises(SystemExit):
            lookup.load(Path(tempfile.gettempdir()) / "does-not-exist-kese.json")


class BundledDataTest(unittest.TestCase):
    def test_en_and_ko_bundles_are_identical_and_valid(self):
        ko = ROOT / "skills-ko" / "kesekit-advisory-ko"
        en = ROOT / "skills" / "kesekit-advisory"
        for rel in ("references/kisa-advisories/advisories.json", "scripts/advisory_lookup.py"):
            with self.subTest(file=rel):
                self.assertEqual((ko / rel).read_bytes(), (en / rel).read_bytes())
        data = lookup.load(ko / "references" / "kisa-advisories" / "advisories.json")
        self.assertEqual(data["coverage"]["count"], len(data["advisories"]))
        ntts = [a["ntt"] for a in data["advisories"]]
        self.assertEqual(len(ntts), len(set(ntts)))

    def test_bundled_risk_signals(self):
        data = lookup.load(ROOT / "skills" / "kesekit-advisory" / "references" / "kisa-advisories" / "advisories.json")
        referenced = {c for a in data["advisories"] for c in a["cves"]}
        self.assertTrue(set(data["cve_meta"]) <= referenced)
        self.assertIn("kev", data["cve_meta"]["CVE-2025-0282"])  # Ivanti Connect Secure, exploited in the wild

    def test_oracle_2180_regression_in_bundle(self):
        data = lookup.load(ROOT / "skills" / "kesekit-advisory" / "references" / "kisa-advisories" / "advisories.json")
        oracle = next(a for a in data["advisories"] if a["no"] == "2180")
        rows = [r for r in oracle["affected"] if r.get("cve") == "CVE-2021-35587"]
        self.assertIn("12.2.1.3.0", [r.get("affected") for r in rows])


if __name__ == "__main__":
    unittest.main()
