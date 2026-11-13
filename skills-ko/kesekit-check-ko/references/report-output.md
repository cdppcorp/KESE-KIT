# 보고서 출력 형식

결과 보고서를 파일로 만들 때 따르는 공통 규칙입니다. 형식은 프로필의 `output.reportFormat`이고, 값이 없으면 `html`입니다. 사용자가 이번 요청에서 다른 형식을 말하면 그 말을 따릅니다.

## 공통 규칙

1. **결과 Markdown을 먼저 씁니다.** 스킬마다 정한 항목별 결과 파일(예: `reports/kese/summary.md`, `technical/*.md`)은 형식과 상관없이 항상 남깁니다. `/kesekit-fix` 같은 다른 스킬이 이 파일을 읽습니다.
2. **최종 보고서는 같은 폴더에 `report.<확장자>`로 만듭니다.** 예: `reports/kese/report.html`, `reports/kisa-advisory/report.pdf`.
3. **모든 형식이 아래 "보고서 구성"과 "발견 사항 쓰는 법"을 따릅니다.** 형식은 겉모습만 다르고 내용과 순서는 같습니다.
4. **비밀값은 가립니다.** 비밀번호, 토큰, 키, 개인정보는 보고서에 그대로 쓰지 않습니다(예: `sk_live_****`).
5. **변환 도구가 없거나 변환에 실패하면 HTML로 대체**하고, 무엇이 없어서 대체했는지와 설치 방법을 알립니다.
6. **설치는 사용자 동의 후에만** 합니다. 패키지 설치와 `npx`로 내려받아 실행하는 것 모두 해당합니다.
7. 도구는 setup이 탐지한 `reportTools`를 참고하되, 보고서를 만들기 직전에 다시 확인합니다.
8. 변환 명령의 경로는 작은따옴표로 감쌉니다. 따옴표·백틱·제어 문자가 든 경로는 쓰지 않습니다.

## 보고서 구성

공식 점검 보고서처럼 씁니다. 대시보드처럼 큰 숫자 카드, 둥근 배지 나열, 이모지, 장식용 그라데이션은 쓰지 않습니다.

| 순서 | 내용 |
|------|------|
| 표지 | 보고서 제목, 한 줄 요약, 문서 정보표(점검 대상·목적·기준·범위·일시·기준 버전·작성), 보안 등급 |
| 목차 | 장 번호(1. / 1.1) 그대로 |
| 1. 점검 개요 | 1.1 목적, 1.2 대상 및 범위(표), 1.3 기준 및 방법과 판정·위험도 정의(표) |
| 2. 결과 요약 | 2.1 종합 판정(적합·조건부 적합·부적합)과 결론 3~5개(잘된 점과 우려 함께), 2.2 영역별 판정 현황(표), 2.3 주요 발견 사항(위험도 높은 순 표) |
| 3. 세부 결과 | 영역마다 3.n: 무엇을 어떻게 봤는지, 항목별 판정 표(양호 항목도 근거 한 줄), 발견 사항 상세 |
| 4. 조치 계획 | 순서·조치·관련 발견 사항·담당·완료 기준 표, 재점검 계획 |
| 5. 부록 | 점검 환경과 한계(한 것·하지 않은 것·결과에 영향을 주는 한계), 참고 기준 |

- 판정은 양호·부분이행·취약·해당없음·확인 필요, 위험도는 긴급·높음·중간·낮음을 씁니다. 색을 쓸 때도 반드시 글자를 함께 씁니다.
- 발견 사항 번호는 보고서 전체에서 F1, F2 …로 이어 붙이고, 요약 표·항목 표·조치 계획에서 같은 번호로 연결합니다.
- 해당 내용이 없는 장도 지우지 말고 "해당 없음"과 그 이유를 씁니다.

## 발견 사항 쓰는 법

부분이행·취약·확인 필요인 항목마다 아래 칸을 **모두** 씁니다. 일반적인 설명을 늘어놓지 말고, 이번에 실제로 본 코드·설정(현재 상태)을 근거로 씁니다.

| 칸 | 쓸 내용 |
|----|---------|
| 관련 기준 | KISA 항목 코드, CWE, 판정 |
| 위치 | 파일:줄, 설정 파일 이름과 키, 서버·장비 이름 |
| 현황 | 지금 어떻게 되어 있는지와 그렇게 판단한 근거. 확인하지 못한 부분은 "확인 필요"로 나눔 |
| 문제점 | 이대로 두면 생길 수 있는 문제. **누가, 어떤 조건에서, 무엇을 할 수 있고, 피해가 무엇인지** 구체적으로 |
| 예시 | 악용·장애 시나리오를 ①②③ 단계로. 코드·설정이면 **현재**와 **개선 예**를 함께 보여 줌 |
| 조치 방안 | 바로 따라 할 수 있는 단계. 가능하면 고친 코드·명령 |
| 확인 필요 | 코드만으로 확정하지 못한 것과 확인 방법(없으면 생략) |

## 형식별 방법

| 형식 | 결과 파일 | 만드는 방법 | 필요한 도구 |
|------|-----------|-------------|-------------|
| `html` (기본) | `report.html` | `templates/report/report.html` 견본을 복사해 채움 | 없음 |
| `pdf` | `report.pdf` | `report.html`을 만든 뒤 브라우저로 PDF 인쇄 | Edge·Chrome·Chromium, 없으면 LibreOffice |
| `hwpx` | `report.hwpx` | 같은 구성으로 `report-hwpx.md`를 쓴 뒤 kordoc으로 변환 | kordoc (Node.js 20 이상) |
| `pptx` | `report.pptx` | 같은 구성을 줄여 `report-slides.md`를 쓴 뒤 pandoc으로 변환 | pandoc, 없으면 python-pptx |
| `md` | 항목별 결과 Markdown | 1번에서 쓴 파일이 곧 보고서. `summary.md`를 "보고서 구성"의 1·2·4·5장 순서로 정리 | 없음 |

## HTML 보고서

- 같은 스킬 폴더의 `templates/report/report.html` 견본을 `report.html`로 복사한 뒤 `{{ }}` 자리를 채웁니다. 견본의 `<style>`, 클래스 이름, 장 번호 체계는 바꾸지 않습니다.
- "반복" 주석이 붙은 블록(영역, 항목 행, 발견 사항, 조치 행)은 필요한 만큼 복제합니다.
- 파일 하나로 끝납니다. `<script>`와 외부 글꼴·이미지·CSS URL은 넣지 않고, 모든 값은 HTML 이스케이프합니다(`&`, `<`, `>`, `"`).
- 견본은 A4 인쇄용 스타일을 갖고 있어 PDF로 바꿔도 같은 모양입니다.

## PDF

`report.html`을 먼저 만든 뒤 변환합니다.

```powershell
# Windows: Edge(Windows 기본 탑재) 또는 Chrome
$browser = @("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") |
  Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
& $browser --headless --disable-gpu --no-pdf-header-footer --print-to-pdf='<보고서 폴더>\report.pdf' '<report.html 절대 경로>'
```

```bash
# Linux: chromium, chromium-browser, google-chrome, microsoft-edge 중 있는 것
chromium --headless --disable-gpu --no-pdf-header-footer --print-to-pdf='<보고서 폴더>/report.pdf' 'file://<report.html 절대 경로>'
# macOS: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' 또는 Microsoft Edge 앱으로 같은 인자를 씁니다
```

브라우저가 없고 LibreOffice가 있으면 `soffice --headless --convert-to pdf --outdir '<보고서 폴더>' '<report.html>'`로 변환합니다. 명령이 끝나면 `report.pdf`가 생겼는지, 크기가 0이 아닌지 확인합니다.

## HWPX (kordoc)

1. kordoc을 쓸 수 있는지 이 순서로 확인합니다.
   - `kordoc --version`이 되면 설치된 kordoc을 씁니다.
   - Claude 도구 목록에 kordoc MCP 도구가 있으면 그것으로 Markdown을 HWPX로 바꿉니다.
   - `node --version`이 20 이상이면 `npx -y kordoc`로 내려받아 실행할 수 있습니다. 외부 패키지를 받아 실행하는 일이므로 **먼저 사용자에게 묻고**, 동의할 때만 실행합니다.
   - 모두 아니면 HTML로 대체하고 설치 방법을 안내합니다: Node.js 20 이상 설치 → `npm install -g kordoc`.
2. `report-hwpx.md`를 "보고서 구성" 순서로 씁니다. `#` 제목 하나, `##`·`###` 장 제목(번호 포함), GFM 표. 발견 사항은 `### F1 제목 (높음)` 아래에 "발견 사항 쓰는 법"의 칸을 2열 표(칸 | 내용)로 씁니다. HTML 태그는 쓰지 않습니다.
3. 변환합니다: `kordoc generate '<보고서 폴더>/report-hwpx.md' --preset 보고서 -o '<보고서 폴더>/report.hwpx'` (npx로 실행할 때는 `npx -y kordoc generate …`)
4. 가능하면 `kordoc lint '<보고서 폴더>/report.hwpx' --preset 보고서`로 서식을 점검하고, 경고가 있으면 요약에 적습니다.

## PPTX

1. `pandoc --version`이 되면 pandoc을 씁니다. 안 되면 Python에서 `import pptx`가 되는지 보고 python-pptx를 씁니다. 둘 다 없으면 HTML로 대체하고 설치 방법을 안내합니다(Windows `winget install JohnMacFarlane.Pandoc`, macOS `brew install pandoc`, Debian·Ubuntu `sudo apt install pandoc`).
2. `report-slides.md`를 씁니다. 슬라이드마다 `##` 제목 하나와 글머리 기호 5줄 이내 또는 작은 표 하나. 구성: 표지(제목·대상·일시) → 종합 판정 → 판정 현황 → 주요 발견 사항 → 발견 사항마다 1장(현황·문제점·예시·조치를 한 줄씩) → 조치 계획.
3. 변환합니다: `pandoc '<보고서 폴더>/report-slides.md' -o '<보고서 폴더>/report.pptx'`
4. python-pptx만 있으면 같은 구성으로 슬라이드를 만드는 짧은 스크립트를 `.kesekit/`에 써서 실행한 뒤 지웁니다.
