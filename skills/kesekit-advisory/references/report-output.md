# Report Output Formats

Shared rules for writing report files. The format is `output.reportFormat` in the profile; when it is missing, use `html`. If the user names another format in this request, follow the user.

## Shared Rules

1. **Write the result Markdown first.** Each skill's per-item result files (e.g. `reports/kese/summary.md`, `technical/*.md`) are always kept, whatever the format. Other skills such as `/kesekit-fix` read them.
2. **Write the final report next to them as `report.<extension>`**, e.g. `reports/kese/report.html` or `reports/kisa-advisory/report.pdf`.
3. **Every format follows "Report Structure" and "Writing a Finding" below.** Formats differ only in appearance; the content and order are the same.
4. **Mask secrets.** Never put passwords, tokens, keys, or personal data in a report as-is (e.g. `sk_live_****`).
5. **If the converter is missing or conversion fails, fall back to HTML**, and say what was missing and how to install it.
6. **Install nothing without the user's consent.** This covers package installs and downloading and running a package with `npx`.
7. Use `reportTools` detected by setup as a hint, but check again right before writing the report.
8. Wrap paths in single quotes in conversion commands. Never use a path containing quotes, backticks, or control characters.

## Report Structure

Write it like a formal assessment report. No dashboard-style big number cards, rows of pill badges, emoji, or decorative gradients.

| Order | Content |
|-------|---------|
| Cover | Title, one-line summary, document information table (target, purpose, criteria, scope, date, baseline, prepared by), classification |
| Contents | Section numbers (1. / 1.1) as-is |
| 1. Overview | 1.1 Purpose, 1.2 Target and scope (table), 1.3 Criteria and method with verdict and severity definitions (tables) |
| 2. Summary | 2.1 Overall verdict (pass, conditional pass, fail) and 3–5 conclusions covering strengths and concerns, 2.2 Verdict counts per area (table), 2.3 Key findings (table, highest severity first) |
| 3. Details | 3.n per area: what was reviewed and how, verdict per item (table, one line of evidence for good items too), finding details |
| 4. Remediation plan | Table of step, action, related findings, owner, done-when; re-assessment plan |
| 5. Appendix | Environment and limitations (done, not done, limitations affecting results), references |

- Verdicts are good, partial, vulnerable, N/A, and to verify; severities are critical, high, medium, and low. When using color, always show the text too.
- Number findings F1, F2 … across the whole report and use the same numbers in the summary table, item tables, and remediation plan.
- Never drop a section; write "Not applicable" and why.

## Writing a Finding

For every partial, vulnerable, or to-verify item, fill in **all** of the fields below. Do not pad with generic explanations; write from the code and settings actually examined in this run (the current state).

| Field | What to write |
|-------|---------------|
| Criteria | KISA item code, CWE, verdict |
| Location | file:line, configuration file and key, server or device name |
| Current state | How it is right now and the evidence for that judgment. Separate anything unconfirmed as "to verify" |
| Risk | What can go wrong if left as is: **who can do what, under which conditions, and the impact**, concretely |
| Example | An abuse or failure scenario in steps ①②③. For code or settings, show **Current** and **Improved** side by side in sequence |
| Remediation | Steps someone can follow right away; fixed code or commands where possible |
| To verify | What could not be confirmed from code alone and how to check it (omit if none) |

## Methods per Format

| Format | Output file | How | Tools needed |
|--------|-------------|-----|--------------|
| `html` (default) | `report.html` | Copy the `templates/report/report.html` template and fill it in | None |
| `pdf` | `report.pdf` | Write `report.html`, then print it to PDF with a browser | Edge, Chrome, or Chromium |
| `hwpx` | `report.hwpx` | Write `report-hwpx.md` with the same structure, then convert it with kordoc | kordoc (Node.js 20 or later) |
| `pptx` | `report.pptx` | Write a condensed `report-slides.md`, then convert it with pandoc | pandoc; otherwise python-pptx |
| `md` | The per-item result Markdown | The files from rule 1 are the report. Organize `summary.md` as sections 1, 2, 4, and 5 of "Report Structure" | None |

## HTML Report

- Copy the `templates/report/report.html` template from the same skill folder to `report.html` and fill in every `{{ }}`. Do not change the template's `<style>`, class names, or section numbering.
- Duplicate the blocks marked "repeat" (areas, item rows, findings, plan rows) as needed.
- It is a single file. No `<script>` and no external fonts, images, or CSS URLs; HTML-escape every value (`&`, `<`, `>`, `"`).
- The template has A4 print styles, so the PDF looks the same.

## PDF

Write `report.html` first, then convert it.

```powershell
# Windows: Edge (built into Windows) or Chrome. The browser returns at once, so wait for the PDF to appear.
$browser = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") |
  Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
$pdf = '<report folder>\report.pdf'
Remove-Item -LiteralPath $pdf -ErrorAction SilentlyContinue
& $browser --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$pdf" '<absolute path of report.html>'
$deadline = (Get-Date).AddSeconds(60)
while (-not ((Test-Path -LiteralPath $pdf) -and (Get-Item -LiteralPath $pdf).Length -gt 0) -and (Get-Date) -lt $deadline) { Start-Sleep -Milliseconds 500 }
Start-Sleep -Seconds 1
```

```bash
# Linux: whichever of chromium, chromium-browser, google-chrome, microsoft-edge exists
chromium --headless --disable-gpu --no-pdf-header-footer --print-to-pdf='<report folder>/report.pdf' 'file://<absolute path of report.html>'
# macOS: same arguments with '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' or the Microsoft Edge app
```

If `report.pdf` does not appear within 60 seconds or is empty, treat the conversion as failed and fall back to HTML; do the same when no browser is available. LibreOffice is not used for PDF because it cannot reproduce this template's layout (grid and print styles).

## HWPX (kordoc)

1. Check whether kordoc is usable, in this order:
   - If `kordoc --version` works, use the installed kordoc.
   - If Claude's tool list has kordoc MCP tools, use them to turn the Markdown into HWPX.
   - If `node --version` is 20 or later, kordoc can be downloaded and run with `npx -y kordoc`. That runs an external package, so **ask the user first** and run it only with their consent.
   - Otherwise fall back to HTML and explain how to install it: install Node.js 20 or later → `npm install -g kordoc`.
2. Write `report-hwpx.md` in the "Report Structure" order: one `#` title, `##` and `###` section headings with numbers, and GFM tables. Under `### F1 Title (High)`, write each finding's fields from "Writing a Finding" as a two-column table (field | content). No HTML tags.
3. Convert: `kordoc generate '<report folder>/report-hwpx.md' --preset 보고서 -o '<report folder>/report.hwpx'` (with npx: `npx -y kordoc generate …`). `보고서` is kordoc's report preset name; keep it in Korean.
4. If possible, check the layout with `kordoc lint '<report folder>/report.hwpx' --preset 보고서` and note any warnings in the summary.

## PPTX

1. Use pandoc if `pandoc --version` works. Otherwise use python-pptx if Python can `import pptx`. If neither is available, fall back to HTML and explain how to install pandoc (Windows `winget install JohnMacFarlane.Pandoc`, macOS `brew install pandoc`, Debian/Ubuntu `sudo apt install pandoc`).
2. Write `report-slides.md`: one `##` title per slide with at most 5 bullets or one small table. Layout: cover (title, target, date) → overall verdict → verdict counts → key findings → one slide per finding (current state, risk, example, remediation in one line each) → remediation plan.
3. Convert: `pandoc '<report folder>/report-slides.md' -o '<report folder>/report.pptx'`
4. If only python-pptx is available, write a short script in `.kesekit/` that builds slides with the same layout, run it, then delete it.
