---
name: kesekit-advisory-ko
description: KISA 보호나라 보안공지(2025년~, 보안 업데이트 권고·주의 권고·보안 조치·강화 권고)를 기반으로 사용 중인 제품·버전·의존성에 해당하는 공지를 찾아 영향 여부와 해결 버전을 판정하고, 기간별 공지 브리핑, CVE 조회, BPFDoor·루트킷·랜섬웨어·자격증명 노출·개발 공급망 공격 등 위협 대응 점검을 수행합니다. "KISA 보안공지", "보호나라", "보안 업데이트 권고", "우리 서버 취약한 버전", "패치 점검", "CVE 영향 확인", "최근 보안공지", "이번 달 보안 권고", "BPFDoor 점검", "랜섬웨어 대비 점검" 시 사용하세요.
---

# KESE KISA 보안공지 대응

KISA 보호나라(KrCERT/CC) 보안공지를 구조화한 데이터로 영향도 점검, 공지 브리핑, CVE 조회, 위협 대응 점검을 수행합니다.

## 데이터

| 파일 | 내용 |
|------|------|
| `references/kisa-advisories/overview.md` | 수집 기간·통계·공지 유형·스키마·갱신 방법 (먼저 읽기) |
| `references/kisa-advisories/advisories.json` | 공지별 영향/해결 버전 표, CVE, 요약, 참고사이트 링크, 첨부 파일명, 검색용 본문 (약 3MB — **직접 Read 금지**, 스크립트로 조회) |
| `references/kisa-advisories/vendor-index.md` | 벤더별 공지 목록 (Grep 용) |
| `references/kisa-advisories/threat-response.md` | 보안 조치·강화 권고 등에서 도출한 TR 점검항목 |
| `scripts/advisory_lookup.py` | 조회 CLI (Python 3.8+, 표준 라이브러리만 사용) |

스크립트는 이 SKILL.md가 있는 디렉터리를 기준으로 실행합니다. Python이 없으면 `vendor-index.md`를 Grep 하고 원문 링크를 안내합니다.

## 모드 선택

| # | 모드 | 사용 시점 |
|---|------|----------|
| 1 | **영향도 점검** | "우리 시스템에 해당하는 KISA 공지가 있나?", 제품·버전·의존성 목록 점검 |
| 2 | **공지 브리핑** | "최근 2주 보안공지 요약", "Cisco 관련 공지", "이번 달 패치 우선순위" |
| 3 | **CVE 조회** | 특정 CVE가 KISA 공지에 포함됐는지, 해결 버전은 무엇인지 |
| 4 | **위협 대응 점검** | BPFDoor, 리눅스 루트킷, 랜섬웨어, 자격증명 노출, 개발 공급망, 제품 사용 주의(EoL) |

요청이 모호하면 1 → 4 순서로 함께 수행할지 사용자에게 확인합니다.

---

## 1. 영향도 점검

### 1단계: 자산 인벤토리 (읽기 전용)

| 대상 | 확인 방법 |
|------|----------|
| OS·커널 | `cat /etc/os-release`, `uname -r` / Windows: `Get-ComputerInfo -Property OsName,OsVersion` |
| 서버 SW | `nginx -v`, `httpd -v` 또는 `apachectl -v`, Tomcat `version.sh`, `openssl version`, `ssh -V`, `sudo -V`, `psql --version`, `mysql --version`, `redis-server --version`, `mongod --version` |
| 패키지 | `dpkg -l` / `rpm -qa` (위 제품명으로 필터), Windows: `winget list` |
| 컨테이너·클러스터 | `docker version`, `kubectl version`, Dockerfile `FROM` 태그, Helm values의 이미지 태그 |
| 애플리케이션 의존성 | `package.json`·lockfile, `requirements.txt`·`poetry.lock`, `pom.xml`·`build.gradle`, `go.mod`, `composer.json`, `Gemfile.lock` |
| 네트워크·보안 장비 | 사용자에게 제조사·모델·펌웨어 버전 질문 (VPN, 방화벽, 게이트웨이, NAS, 공유기) |
| 업무·단말 SW | 사용자에게 질문 (브라우저, 압축 프로그램, 원격지원, 화상회의, 전자서명·보안 프로그램) |

결과를 `제품명 | 버전 | 위치(호스트/파일)` 목록으로 정리합니다.

### 2단계: 공지 조회

```bash
python scripts/advisory_lookup.py -q "nginx" -q "Apache HTTP Server" -q "OpenSSH"
python scripts/advisory_lookup.py -q "Tomcat" --since 2026-01-01 --max-rows 0
python scripts/advisory_lookup.py -q "next" -q "react" --format json      # 의존성 다수 → JSON으로 받아 정리
```

- 질의어의 모든 단어가 공지에 있어야 일치합니다. `Fortinet FortiOS`처럼 벤더+제품으로 검색하면 해당 제품 행만 추립니다. 공지 표기 예: `Connect Secure`, `FortiOS`, `PAN-OS`, `Apache HTTP Server`. 한·영 별칭(구글↔Google, 리눅스↔Linux 등)은 자동 확장됩니다.
- 결과의 `일치` 항목을 확인합니다: **제목·벤더**(전체 행 표시) / **표 행 n/m행**(관련 행만 표시, 숨긴 행 수 안내) / **본문 언급**(버전 표에는 해당 제품 행이 없음 → 원문을 확인하고, 근거가 없으면 **확인 필요**로 판정).
- 다른 벤더 공지에 포함된 제품도 잡힙니다 (예: NGINX → F5 공지).
- 행이 생략되면 `--id <번호> --max-rows 0`으로 전체 행을 확인합니다. 번호가 `공지`인 상단 고정 게시물은 출력에 표시된 nttId로 조회합니다.
- JSON 출력에서 `truncated` 또는 `rows_truncated`가 true면 `--limit 0 --max-rows 0`으로 다시 조회합니다.
- 출력에는 공지의 **참고사이트**(벤더 권고, NVD 등 `[n] URL`)와 첨부 파일명이 포함됩니다. 저장소에 원본 아카이브가 있으면 **원본 폴더** 경로가 함께 표시되므로 첨부 PDF를 Read로 열어 확인합니다.

### 3단계: 판정

| 판정 | 기준 |
|------|------|
| **취약** | 사용 버전이 `영향받는 버전` 범위에 포함되고 `해결 버전` 미만 |
| **양호** | 사용 버전이 같은 브랜치의 `해결 버전` 이상 |
| **확인 필요** | 버전 미상, 브랜치 불일치, `모든 버전`·`해결 버전으로 마이그레이션` 등 모호한 표기 |
| **해당없음** | 제품 미사용 |

- 표기: `이상`(≥), `이하`(≤), `미만`(<), `초과`(>), `이전 버전`(<). 해결 버전은 브랜치별로 다르므로 같은 major/minor 라인끼리 비교합니다.
- `EoL`·`지원 종료`가 해결 방안이면 **취약 + 교체 권고**로 판정합니다.
- 한 제품이 여러 공지에 나오면 모든 공지를 판정하고, 가장 높은 해결 버전을 최종 목표 버전으로 제시합니다.
- 버전 비교가 불확실하면 **확인 필요**로 두고 근거 행을 인용합니다. 추정으로 양호 판정하지 않습니다.

### 4단계: 우선순위

| 우선순위 | 기준 |
|----------|------|
| **긴급** | 인터넷 노출 장비·서비스(VPN, 방화벽, 게이트웨이, 웹서버, 원격관리)의 취약 판정, 또는 요약에 원격 코드 실행·인증 우회·명령 삽입이 포함된 취약 판정 |
| **높음** | 내부 서버·DB·CI/CD·컨테이너 플랫폼의 취약 판정 |
| **보통** | 단말·업무 SW의 취약 판정, 확인 필요 항목 |

### 5단계: 보고서

```
reports/kisa-advisory/
├── summary.md      ← 요약·우선순위·데이터 기준일
└── findings.md     ← 자산별 판정 상세 (근거 공지·행 인용)
```

```
============================================================
     KESE KISA 보안공지 영향도 점검 보고서
============================================================
데이터 기준: [coverage first ~ last] (KISA 보호나라 보안공지)
점검 대상: [호스트/프로젝트]
자산 [N]개 / 취약 [N] / 확인 필요 [N] / 양호 [N] / 해당없음 [N]
------------------------------------------------------------
| 우선순위 | 자산 | 사용 버전 | KISA 공지 | CVE | 목표 버전 | 판정 |
============================================================
```

---

## 2. 공지 브리핑

```bash
python scripts/advisory_lookup.py --since 2026-10-15 --limit 0          # 기간 목록
python scripts/advisory_lookup.py --since 2026-10-01 --stats            # 기간 통계 + 목록
python scripts/advisory_lookup.py --vendor Fortinet --limit 5           # 벤더별 최근 공지
python scripts/advisory_lookup.py --type "주의 권고" --since 2026-09-01  # 유형별
```

브리핑 구성: ① 기간·건수·유형별 분포 ② 주목할 공지 3~7건 (인터넷 노출 장비, 원격 코드 실행·인증 우회, 영향 CVE 다수, 보안 조치·강화 권고) ③ 조직 환경을 알면 해당 제품만 추린 조치 목록 ④ 데이터 기준일.

---

## 3. CVE 조회

```bash
python scripts/advisory_lookup.py --cve CVE-2025-0282 --cve CVE-2025-0283
```

결과가 없으면 "데이터 기준일 내 KISA 공지에 없음"으로 답하고, NVD·벤더 권고 확인을 안내합니다. 없다고 해서 안전하다는 뜻이 아님을 명시합니다.

---

## 4. 위협 대응 점검

`references/kisa-advisories/threat-response.md`를 Read 하고 대상 환경에 맞는 섹션의 TR 항목을 점검합니다.

| 환경 | 우선 섹션 |
|------|----------|
| Linux 서버 | A. 서버·시스템 침해 대응 |
| 웹·WAS·PHP | B. 웹·애플리케이션 |
| 개발·CI/CD·패키지 의존성·AI 개발도구 | C. 개발환경·SW 공급망 |
| 공유기·NAS·네트워크 장비 | D. 네트워크 장비·IoT·NAS |
| 지원 종료·사용 주의 제품 보유 | E. 제품 사용 주의 |
| 업무 PC·계정·표적형 공격(보안인증 SW, 해킹메일, 자동로그인) | F. 단말·계정·표적형 위협 |
| 임직원 보안 인식 교육 | G. 사회공학(피싱·스미싱) 동향 (표, TR 코드 없음) |

문서 끝의 "공지 번호 → 항목 색인"으로 특정 공지가 어느 TR 항목인지 찾을 수 있습니다. 점검 명령은 원문 그대로이며 root 권한이 필요한 것이 많으므로, 운영 시스템에서는 사용자 확인 후 실행하거나 명령을 안내만 합니다.

판정은 양호 / 부분이행 / 취약 / 해당없음으로 기록하고, TR 코드와 근거 공지(게시일·번호·원문 링크)를 함께 남깁니다. 결과는 `reports/kisa-advisory/threat-response.md`에 저장합니다.

---

## 연계

- 취약 항목 조치(업데이트 스크립트, 하드닝) → `/kesekit-fix-ko`
- KISA 공지는 주요 제품 위주이므로 라이브러리 의존성 전체를 대체하지 않습니다 → SBOM 기반 스캔(`grype`, `npm audit`, `pip-audit`, `govulncheck`)을 병행합니다
- CII 점검의 "패치 및 업데이트" 항목 근거 → 이 스킬의 영향도 점검 결과 인용

## 데이터 갱신 (유지보수자)

새 공지를 `문서/KISA_보안공지_2025-2026/`에 추가한 뒤 저장소 루트에서 `python scripts/build_kisa_advisories.py`를 실행합니다. 상세 절차는 `references/kisa-advisories/overview.md`를 참고합니다.

## 중요 규칙

- 점검은 **읽기 전용**입니다. 패키지 업데이트, 서비스 재시작, 설정 변경은 사용자 승인 후 별도로 수행합니다.
- `advisories.json`을 통째로 Read 하지 말고 스크립트나 Grep으로 필요한 부분만 조회합니다.
- 모든 보고서에 **데이터 기준일**을 명시하고, 기준일 이후 공지는 보호나라에서 확인하도록 안내합니다.
- 해결 버전은 공지 시점 기준입니다. 최종 조치 전 참고사이트의 벤더 권고 링크로 최신 내용을 확인하도록 안내합니다.
- 판정 근거로 공지 번호, 해당 행(제품·영향받는 버전·해결 버전), 참고사이트 링크를 그대로 인용합니다.
