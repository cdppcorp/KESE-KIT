"""Tests for scripts/build_kisa_advisories.py and the kesekit-advisory lookup script.

Run: python -m unittest discover -s scripts -p "test_*.py"
"""

from __future__ import annotations

import contextlib
import csv
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
        self.assertIn("CVE-2025-0283", record["cves"])  # from the table
        self.assertNotIn("CVE-2024-11639", record["cves"])  # hidden <a href> residue
        self.assertEqual(len(record["affected"]), 3)

    def test_unexpected_url_is_dropped_with_warning(self):
        row = build.load_index(self.source)[0]
        record, issues = build.build_record({**row, "원문링크": "javascript:alert(1)"}, self.source)
        self.assertEqual(record["url"], "")
        self.assertTrue(any("unexpected source URL" in i for i in issues))

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
        self.assertEqual(len(raw.splitlines()), 3)  # header line, one advisory, closing line
        self.assertIn("## Ivanti (1)", (out / "vendor-index.md").read_text(encoding="utf-8"))
        overview = (out / "overview.md").read_text(encoding="utf-8")
        self.assertIn("총 **1건**", overview)
        self.assertNotIn("old", overview)


def advisory(no, date, title, vendor, affected=(), cves=(), summary="", text="", ntt=""):
    return {"no": no, "ntt": ntt or no, "date": date, "type": "보안 업데이트 권고", "title": title, "vendor": vendor,
            "url": f"u{no}", "folder": "", "attachments": [], "summary": summary, "cves": list(cves),
            "affected": list(affected), "text": text}


SAMPLE_DATA = {
    "schema": 1,
    "coverage": {"first": "2026-01-01", "last": "2026-03-01", "count": 6},
    "advisories": [
        advisory("3", "2026-03-01", "PHP 보안 업데이트 권고", "PHP", cves=["CVE-2026-3"], summary="PHP 취약점",
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
                 affected=[{"product": "sudo", "affected": "1.9.16 이하", "fixed": "1.9.17"}]),
    ],
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

    def test_oracle_2180_regression_in_bundle(self):
        data = lookup.load(ROOT / "skills" / "kesekit-advisory" / "references" / "kisa-advisories" / "advisories.json")
        oracle = next(a for a in data["advisories"] if a["no"] == "2180")
        rows = [r for r in oracle["affected"] if r.get("cve") == "CVE-2021-35587"]
        self.assertIn("12.2.1.3.0", [r.get("affected") for r in rows])


if __name__ == "__main__":
    unittest.main()
