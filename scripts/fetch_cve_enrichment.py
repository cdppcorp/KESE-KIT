#!/usr/bin/env python3
"""Fetch public CVE risk signals for the CVEs referenced by the KISA advisory data.

Sources (public, free to redistribute):
  CISA KEV catalog  actively exploited CVEs (date added, known ransomware use)
  FIRST EPSS        exploit prediction score + percentile (refreshed daily)
  NVD API 2.0       CVSS base score/severity and CWE (optional, --nvd)

Writes scripts/data/cve-enrichment.json; scripts/build_kisa_advisories.py merges it into
the skills' advisories.json. Typical refresh:

  python scripts/fetch_cve_enrichment.py                         # KEV + EPSS, seconds
  NVD_API_KEY=<key> python scripts/fetch_cve_enrichment.py --nvd # + CVSS/CWE, ~1.5 h with a key
  python scripts/build_kisa_advisories.py

Without NVD_API_KEY, --nvd is limited to 5 requests per 30 s (about 15 h for 9k CVEs).
NVD results are cached and resumable: rerunning only fetches CVEs not fetched yet.
Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ADVISORIES = REPO_ROOT / "skills" / "kesekit-advisory" / "references" / "kisa-advisories" / "advisories.json"
DEFAULT_OUT = REPO_ROOT / "scripts" / "data" / "cve-enrichment.json"

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL = "https://epss.empiricalsecurity.com/epss_scores-current.csv.gz"
NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={}"
USER_AGENT = "cve-enrichment-fetcher/1.0"
TIMEOUT_SECONDS = 60
MAX_RESPONSE_BYTES = 64 * 1024 * 1024
NVD_DELAY_WITH_KEY = 0.7  # 50 requests / 30 s
NVD_DELAY_WITHOUT_KEY = 6.5  # 5 requests / 30 s
NVD_RETRY_STATUSES = (403, 429, 500, 502, 503, 504)
NVD_MAX_ATTEMPTS = 4
NVD_SAVE_EVERY = 25
NVD_METRIC_ORDER = ("cvssMetricV31", "cvssMetricV40", "cvssMetricV30", "cvssMetricV2")

CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,7}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RISK_KEYS = ("kev", "ransomware", "epss", "pct")  # replaced on every KEV/EPSS refresh


def today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def http_get(url: str, headers: dict | None = None) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        data = response.read(MAX_RESPONSE_BYTES + 1)
    if len(data) > MAX_RESPONSE_BYTES:
        raise ValueError(f"response from {url} exceeds {MAX_RESPONSE_BYTES} bytes")
    return data


# --------------------------------------------------------------------------- parsers (pure)


def parse_kev(raw: bytes, wanted: set[str]) -> tuple[dict, dict]:
    doc = json.loads(raw)
    vulns = doc.get("vulnerabilities") if isinstance(doc, dict) else None
    if not isinstance(vulns, list):
        raise ValueError("KEV feed has no 'vulnerabilities' list")
    found: dict[str, dict] = {}
    for vuln in vulns:
        if not isinstance(vuln, dict):
            continue
        cve = str(vuln.get("cveID", "")).strip().upper()
        if cve not in wanted:
            continue
        added = str(vuln.get("dateAdded", ""))
        entry = {"kev": added if DATE_RE.match(added) else "unknown"}
        if vuln.get("knownRansomwareCampaignUse") == "Known":
            entry["ransomware"] = True
        found[cve] = entry
    meta = {
        "url": KEV_URL,
        "catalogVersion": str(doc.get("catalogVersion", "")),
        "dateReleased": str(doc.get("dateReleased", "")),
        "entries": len(vulns),
    }
    return found, meta


def parse_epss(raw_gz: bytes, wanted: set[str]) -> tuple[dict, dict]:
    lines = gzip.decompress(raw_gz).decode("utf-8").splitlines()
    meta = {"url": EPSS_URL}
    if lines and lines[0].startswith("#"):
        for part in lines[0].lstrip("#").split(","):
            key, _, value = part.partition(":")
            if key.strip() in ("model_version", "score_date"):
                meta[key.strip()] = value.strip()
        lines = lines[1:]
    found: dict[str, dict] = {}
    for row in csv.DictReader(lines):
        cve = (row.get("cve") or "").strip().upper()
        if cve not in wanted:
            continue
        try:
            epss, pct = float(row["epss"]), float(row["percentile"])
        except (KeyError, TypeError, ValueError):
            continue
        if 0.0 <= epss <= 1.0 and 0.0 <= pct <= 1.0:
            found[cve] = {"epss": round(epss, 5), "pct": round(pct, 5)}
    if not found and wanted:
        raise ValueError("EPSS feed matched none of the wanted CVEs; format may have changed")
    return found, meta


def parse_nvd(raw: bytes) -> dict:
    """CVSS/CWE for one CVE from an NVD API 2.0 response ({} when NVD has no record yet)."""
    doc = json.loads(raw)
    vulns = doc.get("vulnerabilities") if isinstance(doc, dict) else None
    if not vulns:
        return {}
    cve = vulns[0].get("cve", {}) if isinstance(vulns[0], dict) else {}
    entry: dict = {}
    metrics = cve.get("metrics") or {}
    for key in NVD_METRIC_ORDER:
        candidates = [m for m in metrics.get(key) or [] if isinstance(m, dict) and isinstance(m.get("cvssData"), dict)]
        candidates.sort(key=lambda m: m.get("type") != "Primary")  # NVD's own score first
        for metric in candidates:
            data = metric["cvssData"]
            score = data.get("baseScore")
            if isinstance(score, (int, float)) and 0 <= score <= 10:
                entry["cvss"] = float(score)
                entry["cvss_v"] = str(data.get("version", ""))
                severity = data.get("baseSeverity") or metric.get("baseSeverity")
                if isinstance(severity, str) and severity:
                    entry["sev"] = severity.upper()
                break
        if "cvss" in entry:
            break
    cwes = {
        str(d.get("value"))
        for w in cve.get("weaknesses") or [] if isinstance(w, dict)
        for d in w.get("description") or [] if isinstance(d, dict)
        if str(d.get("value", "")).startswith("CWE-")
    }
    if cwes:
        entry["cwe"] = sorted(cwes)
    return entry


def merge_risk(cache: dict, wanted: set[str], kev: dict, epss: dict) -> dict:
    """New per-CVE map: fresh KEV/EPSS values, previously fetched NVD fields kept."""
    merged = {}
    for cve in sorted(wanted):
        kept = {k: v for k, v in cache.get(cve, {}).items() if k not in RISK_KEYS}
        entry = {**kept, **kev.get(cve, {}), **epss.get(cve, {})}
        if entry:
            merged[cve] = entry
    return merged


# --------------------------------------------------------------------------- IO


def load_wanted(advisories_path: Path) -> set[str]:
    doc = json.loads(advisories_path.read_text(encoding="utf-8"))
    cves = {str(c).upper() for a in doc.get("advisories", []) for c in a.get("cves", [])}
    return {c for c in cves if CVE_RE.match(c)}


def load_cache(path: Path) -> tuple[dict, dict]:
    if not path.exists():
        return {}, {}
    doc = json.loads(path.read_text(encoding="utf-8"))
    return doc.get("sources", {}), doc.get("cves", {})


def write_cache(path: Path, sources: dict, cves: dict) -> None:
    """One CVE per line so refreshes diff line by line; LF on every OS."""
    compact = {"separators": (",", ":"), "ensure_ascii": False}
    head = json.dumps({"schema": 1, "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       "sources": sources}, **compact)
    items = sorted(cves.items())
    lines = [head[:-1] + ',"cves":{']
    lines += [f"{json.dumps(k)}:{json.dumps(v, **compact)}" + ("," if i < len(items) - 1 else "")
              for i, (k, v) in enumerate(items)]
    lines.append("}}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    tmp.replace(path)


def fetch_nvd(cves: dict, wanted: set[str], api_key: str | None, limit: int, save) -> int:
    """Fetch CVSS/CWE for CVEs not fetched yet. Mutates `cves` in place and checkpoints via save()."""
    delay = NVD_DELAY_WITH_KEY if api_key else NVD_DELAY_WITHOUT_KEY
    todo = [c for c in sorted(wanted) if "nvd" not in cves.get(c, {})]
    if limit > 0:
        todo = todo[:limit]
    headers = {"apiKey": api_key} if api_key else None
    print(f"NVD: {len(todo)} CVE(s) to fetch, ~{len(todo) * delay / 60:.0f} min", file=sys.stderr)
    for done, cve in enumerate(todo, 1):
        raw = nvd_request(cve, headers)
        cves[cve] = {**cves.get(cve, {}), **parse_nvd(raw), "nvd": today()}
        if done % NVD_SAVE_EVERY == 0 or done == len(todo):
            save()
            print(f"NVD: {done}/{len(todo)}", file=sys.stderr)
        time.sleep(delay)
    return len(todo)


def nvd_request(cve: str, headers: dict | None) -> bytes:
    for attempt in range(1, NVD_MAX_ATTEMPTS + 1):
        try:
            return http_get(NVD_URL.format(cve), headers)
        except urllib.error.HTTPError as exc:
            if exc.code not in NVD_RETRY_STATUSES or attempt == NVD_MAX_ATTEMPTS:
                raise
        except urllib.error.URLError:
            if attempt == NVD_MAX_ATTEMPTS:
                raise
        time.sleep(30 * attempt)
    raise RuntimeError("unreachable")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--advisories", type=Path, default=DEFAULT_ADVISORIES, help="built advisories.json to read CVE ids from")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--nvd", action="store_true", help="also fetch CVSS/CWE from NVD (uses NVD_API_KEY if set)")
    parser.add_argument("--nvd-limit", type=int, default=0, help="max NVD requests this run (0 = all pending)")
    parser.add_argument("--skip-kev-epss", action="store_true", help="only continue the NVD fetch")
    args = parser.parse_args(argv)

    wanted = load_wanted(args.advisories)
    sources, cves = load_cache(args.out)
    if not args.skip_kev_epss:
        kev, kev_meta = parse_kev(http_get(KEV_URL), wanted)
        epss, epss_meta = parse_epss(http_get(EPSS_URL), wanted)
        cves = merge_risk(cves, wanted, kev, epss)
        sources = {**sources, "kev": kev_meta, "epss": epss_meta}
        print(f"KEV {kev_meta['catalogVersion']}: {len(kev)} CVE(s); EPSS {epss_meta.get('score_date', '?')}: {len(epss)} CVE(s)",
              file=sys.stderr)
    write_cache(args.out, sources, cves)

    if args.nvd:
        api_key = os.environ.get("NVD_API_KEY") or None

        def save() -> None:
            fetched = sum(1 for v in cves.values() if "nvd" in v)
            write_cache(args.out, {**sources, "nvd": {"url": NVD_URL.format("<id>"), "fetched": fetched}}, cves)

        fetch_nvd(cves, wanted, api_key, args.nvd_limit, save)
    print(f"wrote {args.out} ({len(cves)} CVE(s) of {len(wanted)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
