# KESE - KISA Enhanced Security Evaluation Kit

주요정보통신기반시설(CII) 취약점 분석평가, AI 보안 평가, 로봇 보안 점검, 우주 보안 점검, 시큐어코딩 가이드, 제로트러스트 보안 평가, SW 공급망 보안(SBOM), KISA 보안공지 대응을 위한 Claude Code 스킬 플러그인입니다.

🌐 [한국어](#빠른-시작) | [English](#english) | [Français](docs/README.fr.md) | [日本語](docs/README.ja.md) | [中文](docs/README.zh.md) | [Русский](docs/README.ru.md) | [Español](docs/README.es.md) | [Deutsch](docs/README.de.md) | [Português](docs/README.pt.md) | [Italiano](docs/README.it.md) | [العربية](docs/README.ar.md) | [हिन्दी](docs/README.hi.md) | [Türkçe](docs/README.tr.md) | [Tiếng Việt](docs/README.vi.md) | [ภาษาไทย](docs/README.th.md) | [Bahasa Indonesia](docs/README.id.md) | [Polski](docs/README.pl.md) | [Nederlands](docs/README.nl.md) | [Svenska](docs/README.sv.md) | [Українська](docs/README.uk.md)

---

## 빠른 시작

### 1단계: 설치

터미널(CMD, PowerShell, bash 등)에서 Claude Code를 실행합니다:

```bash
claude
```

Claude Code 안에서 다음 명령어로 마켓플레이스 등록 및 플러그인 설치를 합니다:

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@cdppcorp-KESE-KIT
```

> **업데이트 시:**
> ```
> /plugin marketplace update cdppcorp-KESE-KIT
> /plugin update kesekit@cdppcorp-KESE-KIT
> /reload-plugins
> ```

### 2단계: 사용

Claude Code 프롬프트에 슬래시 명령어를 입력합니다:

```
/kesekit-start-ko     보안 취약점 분석평가 실행
/kesekit-check-ko     배포 전 보안 체크리스트
/kesekit-fix-ko       취약점 자동 수정 / 하드닝 스크립트 생성
/kesekit-guide-ko     시큐어코딩 가이드 프롬프트 생성
/kesekit-advisory-ko  KISA 보안공지 영향도 점검 / 브리핑 / 위협 대응
```

영문 버전도 사용 가능합니다:

```
/kesekit-start        Full security assessment
/kesekit-check        Pre-deployment checklist
/kesekit-fix          Generate hardening scripts
/kesekit-guide        Secure coding prompts
/kesekit-advisory     KISA security notice exposure check
```

### 사용 예시

```
# 프로젝트 폴더에서 Claude Code 실행 후:

> /kesekit-start-ko
  → "어떤 시스템을 점검하시겠습니까?" 질문에 답변
  → 예: "Ubuntu 22.04 웹 서버", "Windows Server 2022", "AI 모델 배포 환경"

> /kesekit-check-ko
  → 배포 전 보안 컴플라이언스 자동 체크

> /kesekit-fix-ko
  → 취약점 분석 결과를 기반으로 하드닝 스크립트 자동 생성

> /kesekit-guide-ko
  → "Python Flask 인증 구현" 같은 요청에 시큐어코딩 프롬프트 제공

> /kesekit-advisory-ko
  → "nginx 1.30.2, OpenSSH 9.8, FortiOS 7.4.3 쓰는데 해당 공지 있어?"
  → KISA 보안공지 기준 취약/양호 판정과 해결 버전 제시
```

---

## 개요

KESE(KISA Enhanced Security Evaluation Kit)는 KISA(한국인터넷진흥원) 가이드라인에 기반한 보안 취약점 분석평가 기능을 제공하는 Claude Code 플러그인입니다. 주요정보통신기반시설(CII) 취약점 분석평가, AI 보안 평가, 로봇 보안 점검, 우주 보안 점검, 제로트러스트 보안 평가, SW 공급망 보안(SBOM), KISA 보안공지 대응을 지원합니다.

### 기능

| 스킬 | 설명 |
|------|------|
| `/kesekit-start-ko` | 전체 보안 취약점 분석평가 실행 (CII 560+ / AI 보안 / 로봇 보안 / 우주 보안 / 시큐어코딩 / 제로트러스트 / SW 공급망) |
| `/kesekit-check-ko` | 배포 전 보안 컴플라이언스 체크리스트 (CII / AI / 로봇 / 우주 / 시큐어코딩 / 제로트러스트 / SW 공급망) |
| `/kesekit-fix-ko` | 하드닝 스크립트 및 보안 수정 자동 생성 (CII / AI / 로봇 / 우주 / 시큐어코딩 / 제로트러스트 / SW 공급망) |
| `/kesekit-guide-ko` | AI 도구용 시큐어코딩 프롬프트 생성 (CII / AI / 로봇 / 우주 / JS·Python·범용 / 제로트러스트 / SW 공급망) |
| `/kesekit-advisory-ko` | KISA 보안공지 대응 (영향도 점검 / 공지 브리핑 / CVE 조회 / 위협 대응 점검) |

### 지원 가이드라인

#### 1. 주요정보통신기반시설(CII) — 560+항목

**기술적 취약점 평가**
| 시스템 | 코드 | 항목 수 |
|--------|------|:------:|
| Unix/Linux 서버 | U-01~U-67 | 67 |
| Windows 서버 | W-01~W-64 | 64 |
| 웹 서비스 | WEB-01~WEB-26 | 26 |
| 보안 장비 | S-01~S-23 | 23 |
| 네트워크 장비 | N-01~N-38 | 38 |
| 제어시스템 | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| 이동통신 | M-01~M-04 | 4 |
| Web Application | 21개 코드 | 21 |
| 가상화 장비 | HV-01~HV-25 | 25 |
| 클라우드 | CA-01~CA-19 | 19 |

**관리적 취약점 평가**: A-1~A-127 (127항목, 14개 영역)
**물리적 취약점 평가**: P-1~P-18 (18항목)

#### 2. AI 보안 안내서 — 54+항목

| 대상 | 항목 수 | 생명주기 |
|------|:------:|---------|
| AI 개발자 | 54 | 6단계 (계획→데이터→모델개발→배포→모니터링→파기) |
| AI 서비스 제공자 | ~43 | 6단계 (계획→개발→운영→유지보수→피드백→파기) |
| AI 이용자 | 7 | 보안 수칙 |

#### 3. 로봇 보안 — ~103항목

| 카테고리 | 코드 | 항목 수 | 참조 표준 |
|---------|------|:------:|----------|
| 보안 SW 개발 (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| 공급망 보안 | SC-01~07 | 7 | NIST SP 800-161 |
| 식별 및 인증 | IA-01~11 | 11 | IEC 62443 |
| 사용 통제 | UC-01~11 | 11 | IEC 62443 |
| 시스템 무결성 | SI-01~11 | 11 | IEC 62443 |
| 데이터 보호 | DP-01~04 | 4 | IEC 62443 |
| 데이터 흐름 제한 | DFR-01~02 | 2 | IEC 62443 |
| 이벤트 대응 | ER-01~03 | 3 | IEC 62443 |
| 자원 가용성 | RA-01~08 | 8 | IEC 62443 |
| 사이버 복원력 | CR-01~13 | 13 | EU CRA |
| 무선 보안 | WS-01~14 | 14 | EU RED |

대상: 산업용 / 서비스용 / 의료용 로봇 (ISO 8373)

#### 4. 우주 보안 — 53항목

| 분야 | 코드 | 항목 수 | 참조 표준 |
|------|------|:------:|----------|
| 접근통제 | AC-01~12 | 12 | CMMC, K-RMF |
| 식별 및 인증 | IA-01~02 | 2 | CMMC, NIS2 |
| 시스템 및 통신 보안 | SC-01~07 | 7 | NIST IR 8401 |
| 시스템 및 정보 무결성 | SI-01~04 | 4 | NIST CSF |
| 시스템/서비스 운영관리 | SO-01~09 | 9 | ISMS-P |
| 사고 대응 | IR-01~02 | 2 | NIS2 |
| 인원 보안 | PS-01~02 | 2 | CMMC |
| 물리보안 | PE-01~03 | 3 | K-RMF |
| 위험평가 및 보안 평가 | RA-01~02 | 2 | NIST CSF |
| 보안 거버넌스 | SG-01~04 | 4 | ISMS-P |
| 비상 계획 | CP-01~02 | 2 | NIST IR 8270 |
| 공급망 관리 | SM-01~04 | 4 | CMMC, NIS2 |

대상: 위성 운영사, GSaaS 제공자, 지상국 운영사, 우주 공급망 참여기업

#### 5. 시큐어코딩 가이드 — 46항목

| 카테고리 | 항목 수 | CWE 수 | 참조 표준 |
|---------|:------:|:------:|----------|
| 입력데이터 검증 및 표현 | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| 보안기능 | 16 | 16 | CWE/SANS Top 25 |
| 시간 및 상태 | 2 | 3 | CWE |
| 에러처리 | 3 | 3 | CWE |
| 코드오류 | 3 | 3 | CWE |
| 캡슐화 | 4 | 5 | CWE |
| API 오용 | 2 | 1 | CWE |

**지원 언어:**
| 언어 | 항목 수 | 프레임워크 |
|------|:------:|-----------|
| Pseudo Code (범용) | 46 | 언어 무관 패턴 |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

대상: JavaScript/Python 웹 개발자, AI 도구(Claude, Cursor, Copilot) 사용자, 바이브코딩 개발자

#### 6. 제로트러스트 보안 — ~421항목

| 핵심 요소 | 코드 | 항목 수 | 성숙도 |
|----------|------|:------:|--------|
| 식별자·신원 | ZT-ID-01~53 | 53 | 기존/초기/향상/최적화 |
| 기기·엔드포인트 | ZT-DV-01~36 | 36 | 기존/초기/향상/최적화 |
| 네트워크 | ZT-NW-01~54 | 54 | 기존/초기/향상/최적화 |
| 시스템 | ZT-SY-01~49 | 49 | 기존/초기/향상/최적화 |
| 애플리케이션·워크로드 | ZT-AP-01~60 | 60 | 기존/초기/향상/최적화 |
| 데이터 | ZT-DA-01~58 | 58 | 기존/초기/향상/최적화 |
| 가시성·분석 | ZT-VA-01~43 | 43 | 기존/초기/향상/최적화 |
| 자동화·통합 | ZT-AU-01~43 | 43 | 기존/초기/향상/최적화 |
| OT/ICS 특화 | ZT-OT-01~25 | 25 | 기존/초기/향상/최적화 |

**성숙도 4단계**: 기존(Traditional) → 초기(Initial) → 향상(Advanced) → 최적화(Optimal)
**참조 표준**: KISA 제로트러스트 가이드라인 2.0, NIST SP 800-207, CISA ZT Maturity Model

대상: 제로트러스트 도입 기업, OT/ICS 환경, 클라우드 전환 조직, 보안 성숙도 평가 담당자

#### 7. SW 공급망 보안 — 29항목

| 단계 | 코드 | 항목 수 | 참조 표준 |
|------|------|:------:|----------|
| 설계 단계 | SC-01~05 | 5 | NIST SP 800-161r1 |
| 개발 단계 | SC-06~16 | 11 | NIST SP 800-218 (SSDF) |
| 공급(유통) 단계 | SC-17~19 | 3 | NTIA SBOM |
| 도입 및 운영 단계 | SC-20~26 | 7 | NIS-SBOM |
| 유지보수 단계 | SC-27~29 | 3 | NIS-SBOM |

**SBOM 표준**: SPDX (ISO/IEC 5962), CycloneDX (OWASP), NIS-SBOM (20개 항목)
**지원 도구**: Syft, Grype, CycloneDX CLI, npm audit, pip-audit, govulncheck
**규제 동향**: 미국 EO 14028 (SBOM 제출 의무화), EU CRA (2026 하반기 시행), NIS-SBOM (공공기관)

대상: SW 개발기업, 공공조달 납품사, 정부과제 개발자, 바이브코딩 개발자

#### 8. KISA 보안공지 대응 — 519건 (2025-01 ~ 2026-11)

KISA 보호나라(KrCERT/CC) 보안공지를 구조화한 데이터로 **우리 시스템에 해당하는 공지가 있는지** 판정합니다.

| 모드 | 내용 | 근거 데이터 |
|------|------|------------|
| 영향도 점검 | 설치 제품·버전·의존성 ↔ 공지의 영향받는 버전/해결 버전 대조, 긴급/높음/보통 우선순위 | 보안 업데이트 권고 428건, 버전 행 12,256행 |
| 공지 브리핑 | 기간·벤더·유형별 최신 공지 요약과 조치 우선순위 | 전체 519건 |
| CVE 조회 | 특정 CVE의 KISA 공지 포함 여부와 해결 버전 | 고유 CVE 8,833개 |
| 위협 대응 점검 | BPFDoor, 리눅스 커널 루트킷, 랜섬웨어, 자격증명 노출, 개발 공급망 공격, 제품 사용 주의(EoL) — TR-01~TR-43 (43항목) + 피싱·스미싱 동향 35건 | 비패치성 공지 91건 (보안 조치·강화 18, 취약점 조치 7, 주의 63, 기타 3) |

**조회 도구**: `scripts/advisory_lookup.py` (Python 표준 라이브러리, 제품/CVE/벤더/기간/유형 필터)
**최신화**: 새 공지를 `문서/KISA_보안공지_2025-2026/`에 추가 후 `python scripts/build_kisa_advisories.py` 실행 → EN/KO 스킬 데이터 일괄 재생성

대상: 서버·네트워크 운영자, 패치 관리 담당자, 보안관제·CERT, 배포 전 점검 담당자

### 원본 문서

본 플러그인은 다음 공식 보안 가이드라인을 기반으로 재구성되었습니다:

| # | 문서명 | 발행기관 | 연도 | 페이지 | PDF / MD |
|---|--------|---------|:----:|:------:|:--------:|
| 1 | **주요정보통신기반시설 기술적 취약점 분석·평가방법 상세가이드** | KISA | 2026 | 873 | [PDF](문서/주요정보통신기반시설%20기술적%20취약점%20분석·평가%20방법%20상세가이드.pdf) / [MD](문서/주요정보통신기반시설_기술적_취약점_상세가이드.md) |
| 2 | **주요정보통신기반시설 관리·물리적 취약점 분석·평가 방법 안내서** | KISA | 2026 | 332 | [PDF](문서/주요정보통신기반시설%20관리·물리적%20취약점%20분석·평가%20방법%20안내서.pdf) / [MD](문서/주요정보통신기반시설_관리물리적_취약점_가이드.md) |
| 3 | **인공지능(AI) 보안 안내서** | 과기정통부 / KISA | 2026 | 239 | [PDF](문서/인공지능%28AI%29%20보안%20안내서%28정오%20수정%29.pdf) / [MD](문서/인공지능_AI_보안_안내서.md) |
| 4 | **로봇 보안모델(고도화)** | KISA | 2026 | 156 | [PDF](문서/로봇%20보안모델%28고도화%29.pdf) / [MD](문서/로봇_보안모델.md) |
| 5 | **로봇 보안취약점 점검 체크리스트 해설서** | KISA | 2026 | 225 | [PDF](문서/로봇%20보안취약점%20점검%20체크리스트%20해설서.pdf) / [MD](문서/로봇_보안취약점_점검_체크리스트_해설서.md) |
| 6 | **우주 보안모델 Part1** (위성활용 서비스) | 과기정통부 / KISA | 2024 | 134 | [PDF](문서/우주%20보안모델%20Part1.pdf) / [MD](문서/우주_보안모델_Part1.md) |
| 7 | **우주 보안모델 Part2** (GSaaS/우주 공급망) | 과기정통부 / KISA | 2025 | 223 | [PDF](문서/우주%20보안모델%20Part2.pdf) / [MD](문서/우주_보안모델_Part2.md) |
| 8 | **우주 보안모델 해설서 및 사례집** | 과기정통부 / KISA | 2025 | 218 | [PDF](문서/우주%20보안모델%20해설서%20및%20사례집.pdf) / [MD](문서/우주_보안모델_해설서_및_사례집.md) |
| 9 | **Javascript 시큐어코딩 가이드** (2023년 개정본) | KISA | 2023 | 159 | [PDF](문서/Javascript_시큐어코딩_가이드%282023년_개정본%29.pdf) / [MD](문서/Javascript_시큐어코딩_가이드.md) |
| 10 | **Python 시큐어코딩 가이드** (2023년 개정본) | KISA | 2023 | 176 | [PDF](문서/Python_시큐어코딩_가이드%282023년_개정본%29.pdf) / [MD](문서/Python_시큐어코딩_가이드.md) |
| 11 | **Pseudo Code 시큐어코딩 가이드** (범용) | KESE-KIT | 2026 | - | [MD](문서/Pseudocode_시큐어코딩_가이드.md) |
| 12 | **제로트러스트 가이드라인 2.0** | 한국제로트러스트포럼 / KISA | 2024 | 245 | [PDF](문서/제로트러스트_가이드라인_2.0.pdf) / [MD](문서/제로트러스트_가이드라인_2.0.md) |
| 13 | **제로트러스트 성숙도 모델 해설서** | 한국제로트러스트포럼 / KISA | 2024 | 182 | [PDF](문서/제로트러스트_성숙도_모델_해설서.pdf) / [MD](문서/제로트러스트_성숙도_모델_해설서.md) |
| 14 | **OT 환경의 제로트러스트 적용 안내서** | 과기정통부 / KISA | 2025 | 67 | [PDF](문서/OT_환경의_제로트러스트_적용_안내서.pdf) / [MD](문서/OT_환경의_제로트러스트_적용_안내서.md) |
| 15 | **SW 공급망 보안 가이드라인 (요약본)** | 국정원 / 과기정통부 / KISA | 2024 | 22 | [PDF](문서/240513-(요약본)_SW_공급망_보안_가이드라인.pdf) / [MD](문서/SW_공급망_보안_가이드라인_요약본.md) |
| 16 | **SW 공급망 보안 가이드라인 (전체본)** | 국정원 / 과기정통부 / KISA | 2024 | 100 | [PDF](문서/240525-(전체본)_SW_공급망_보안_가이드라인_최종%20수정본.pdf) / [MD](문서/SW_공급망_보안_가이드라인_전체본.md) |
| 17 | **인공지능기본법 교안** (11장 60개 절, 실무 해설) | 과기정통부·한국AI소프트웨어산업협회 발행 / KESE-KIT 편집 | 2026 | - | [MD](문서/AI_기본법_교안/) |
| 18 | **KISA 보호나라 보안공지** (519건, 2025-01 ~ 2026-11) | KISA | 2025–2026 | - | [목록·본문](문서/KISA_보안공지_2025-2026/) |

### v2.x에서 마이그레이션

v3.0에서 모든 스킬이 단일 `kesekit` 네임스페이스로 통합되었습니다. v2.x 이하를 사용하셨다면 기존 플러그인을 삭제 후 재설치하세요:

```
/plugin uninstall kesekit
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@cdppcorp-KESE-KIT
```

명령어 변경사항:

| 이전 (v2.x) | 이후 (v3.0+) |
|-------------|------------|
| `/start` | `/kesekit-start` |
| `/check` | `/kesekit-check` |
| `/fix` | `/kesekit-fix` |
| `/guide` | `/kesekit-guide` |
| `/start-ko` | `/kesekit-start-ko` |
| `/check-ko` | `/kesekit-check-ko` |
| `/fix-ko` | `/kesekit-fix-ko` |
| `/guide-ko` | `/kesekit-guide-ko` |

> **참고:** 기존 `/start`, `/check`, `/fix`, `/guide` 명령어는 더 이상 동작하지 않습니다. `/kesekit-*` (하이픈) 형식의 접두사를 사용하세요.

---

## English

### Quick Start

#### Step 1: Install

Launch Claude Code in your terminal:

```bash
claude
```

Inside Claude Code, register the marketplace and install the plugin:

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@cdppcorp-KESE-KIT
```

> **To update:**
> ```
> /plugin marketplace update cdppcorp-KESE-KIT
> /plugin update kesekit@cdppcorp-KESE-KIT
> /reload-plugins
> ```

#### Step 2: Use

Type slash commands at the Claude Code prompt:

```
/kesekit-start     Full security vulnerability assessment
/kesekit-check     Pre-deployment security checklist
/kesekit-fix       Auto-fix vulnerabilities / generate hardening scripts
/kesekit-guide     Generate secure coding prompts
/kesekit-advisory  KISA security notice exposure check / briefing / threat response
```

Korean versions are also available:

```
/kesekit-start-ko  보안 취약점 분석평가
/kesekit-check-ko  배포 전 체크리스트
/kesekit-fix-ko    하드닝 스크립트 생성
/kesekit-guide-ko  시큐어코딩 가이드
/kesekit-advisory-ko  KISA 보안공지 대응
```

#### Usage Examples

```
# After launching Claude Code in your project folder:

> /kesekit-start
  → Answer "What system do you want to assess?"
  → e.g. "Ubuntu 22.04 web server", "Windows Server 2022", "AI model deployment"

> /kesekit-check
  → Automated pre-deployment compliance check

> /kesekit-fix
  → Generate hardening scripts from assessment results

> /kesekit-guide
  → Request like "Python Flask authentication" → get secure coding prompt

> /kesekit-advisory
  → "We run nginx 1.30.2, OpenSSH 9.8, FortiOS 7.4.3 — any KISA notices?"
  → Vulnerable/Pass verdicts with fixed versions from KISA notices
```

### Supported Guidelines

#### 1. Critical Information Infrastructure (CII) — 560+ Items

**Technical Assessment**
| System | Code | Items |
|--------|------|:-----:|
| Unix/Linux Server | U-01~U-67 | 67 |
| Windows Server | W-01~W-64 | 64 |
| Web Service | WEB-01~WEB-26 | 26 |
| Security Equipment | S-01~S-23 | 23 |
| Network Equipment | N-01~N-38 | 38 |
| Control System | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobile | M-01~M-04 | 4 |
| Web Application | 21 codes | 21 |
| Virtualization | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Administrative Assessment**: A-1~A-127 (127 items, 14 domains)
**Physical Assessment**: P-1~P-18 (18 items)

#### 8. KISA Security Notices — 519 notices (2025-01 ~ 2026-11)

Structured KISA Boho-nara (KrCERT/CC) security notices for answering **"does any KISA notice affect our systems?"**

| Mode | What it does | Data |
|------|-------------|------|
| Exposure check | Installed products/versions/dependencies vs. affected/fixed versions, Critical/High/Medium priority | 428 security update advisories, 12,256 version rows |
| Notice briefing | Recent notices by period, vendor, or type with action priorities | All 519 notices |
| CVE lookup | Whether a CVE is in a KISA notice and its fixed version | 8,833 unique CVEs |
| Threat response | BPFDoor, Linux kernel rootkits, ransomware, exposed credentials, dev supply-chain attacks, product-use cautions (EoL) — TR-01~TR-43 (43 items) + 35 phishing/smishing trend rows | 91 non-patch notices (18 hardening, 7 mitigation, 63 caution, 3 other) |

**Lookup tool**: `scripts/advisory_lookup.py` (Python standard library; product/CVE/vendor/period/type filters)
**Refresh**: add new notices under `문서/KISA_보안공지_2025-2026/`, then run `python scripts/build_kisa_advisories.py` to regenerate the EN/KO skill data

### Overview

KESE (KISA Enhanced Security Evaluation Kit) is a Claude Code plugin that provides comprehensive vulnerability assessment capabilities based on KISA (Korea Internet & Security Agency) guidelines. Supports Critical Information Infrastructure (CII), AI Security, Robot Security, Space Security, Secure Coding, Zero Trust, SW Supply Chain Security (SBOM) assessments, and KISA security notice response.

### Features

| Skill | Description |
|-------|-------------|
| `/kesekit-start` | Run full security vulnerability assessment (CII 560+ / AI / Robot / Space / Secure Coding / Zero Trust / Supply Chain) |
| `/kesekit-check` | Pre-deployment security compliance checklist (CII / AI / Robot / Space / Secure Coding / Zero Trust / Supply Chain) |
| `/kesekit-fix` | Auto-generate hardening scripts and security fixes (CII / AI / Robot / Space / Secure Coding / Zero Trust / Supply Chain) |
| `/kesekit-guide` | Generate secure coding prompts for AI, robot, space, zero trust, and supply chain security |
| `/kesekit-advisory` | KISA security notice response (exposure check / briefing / CVE lookup / threat response) |

### Source Documents

| # | Document | Publisher | Year | Pages |
|---|----------|-----------|:----:|:-----:|
| 1 | **Technical Vulnerability Assessment Guide for CII** | KISA | 2026 | 873 |
| 2 | **Administrative & Physical Vulnerability Assessment Guide for CII** | KISA | 2026 | 332 |
| 3 | **AI Security Guide** | MSIT / KISA | 2026 | 239 |
| 4 | **Robot Security Model** | KISA | 2026 | 156 |
| 5 | **Robot Security Checklist Guide** | KISA | 2026 | 225 |
| 6 | **Space Security Model Part1** | MSIT / KISA | 2024 | 134 |
| 7 | **Space Security Model Part2** (GSaaS/Supply Chain) | MSIT / KISA | 2025 | 223 |
| 8 | **Space Security Explanation Guide** | MSIT / KISA | 2025 | 218 |
| 9 | **SW Supply Chain Security Guideline (Summary)** | NIS / MSIT / KISA | 2024 | 22 |
| 10 | **SW Supply Chain Security Guideline (Full)** | NIS / MSIT / KISA | 2024 | 100 |
| 11 | **KISA Boho-nara Security Notices** (519 notices, 2025-01 ~ 2026-11) | KISA | 2025–2026 | - |

---

## 프로젝트 구조

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← 플러그인 메타데이터
├── skills/                            ← 영문 스킬 (kesekit-start/check/fix/guide/advisory)
│   ├── kesekit-advisory/             ← KISA 보안공지 대응 스킬
│   │   ├── references/kisa-advisories/ ← advisories.json, 벤더 인덱스, 위협 대응 TR 항목
│   │   └── scripts/advisory_lookup.py  ← 공지 조회 CLI
│   └── kesekit-*/                    ← start/check/fix/guide
│       ├── SKILL.md                  ← 라우터 (분야 자동 감지)
│       ├── references/               ← 순수 설명/기준 문서
│       │   ├── ai-security/          ← 개요, 서비스제공자, 이용자 가이드
│       │   ├── secure-coding/        ← CWE 매핑, 의사코드 패턴
│       │   ├── space-security/       ← 개요, 공급망 위협 시나리오
│       │   ├── supply-chain/         ← C-SCRM, SBOM, 규제 동향
│       │   └── zero-trust/           ← 성숙도 모델, OT 가이드
│       ├── templates/                ← 별지 서식, 체크리스트 테이블
│       │   ├── cii/                  ← CII 14개 점검항목 테이블
│       │   ├── ai-security/          ← AI 개발자 검증항목
│       │   ├── robot-security/       ← 로봇 보안 6개 체크리스트
│       │   ├── secure-coding/        ← JS/Python 시큐어코딩
│       │   ├── space-security/       ← 우주 보안 4개 점검항목
│       │   ├── supply-chain/         ← SBOM 29개 자가점검 체크리스트
│       │   └── zero-trust/           ← ZT 8요소 성숙도 점검
│       └── scripts/                  ← 실행 가능한 점검/수정 스크립트
│           ├── cii/                  ← bash, PowerShell, SQL
│           ├── robot-security/       ← 방화벽, SBOM, 인증서
│           ├── supply-chain/         ← SBOM 생성, 취약점 스캔
│           └── zero-trust/           ← ID/네트워크/가시성 점검
├── skills-ko/                         ← 한글 스킬 (동일 구조)
├── 문서/                              ← 원본 PDF + MD 참고자료
│   ├── *.pdf / *.md                  ← 가이드라인 원본 (16건)
│   ├── AI_기본법_교안/               ← AI 기본법 실무 교안 (60개 절)
│   └── KISA_보안공지_2025-2026/      ← 보호나라 보안공지 원본 (목록.csv + 공지별 본문·첨부)
├── authorkit/                         ← 변환 산출물 및 작업 파일
├── scripts/                           ← validate-content.mjs, build_kisa_advisories.py (+ 테스트)
├── docs/                              ← 18개 국어 README
├── CONTRIBUTING.md                    ← 가이드라인 추가 방법
└── README.md
```

---

## 변경 이력

### v3.4.0 (2026-11-14)

**새 스킬 추가: KISA 보안공지 대응 (`/kesekit-advisory`, `/kesekit-advisory-ko`)**
- 출처: KISA 보호나라 보안공지 519건 (2025-01-06 ~ 2026-11-13) — 보안 업데이트 권고 428, 주의 권고 63, 보안 조치·강화 권고 18, 취약점 조치 권고 7, 기타 3
- 4개 모드: 영향도 점검(영향받는/해결 버전 대조), 공지 브리핑, CVE 조회, 위협 대응 점검
- 위협 대응 점검: 비패치성 공지 91건 → TR-01~TR-43 (서버 침해·웹·개발 공급망·네트워크 장비·EoL 제품·단말/표적형) + 피싱·스미싱 동향 35건, 점검 명령은 원문 그대로 수록
- `scripts/build_kisa_advisories.py`: 공지 HTML 표(rowspan/colspan) 파싱 → `advisories.json`(버전 행 12,256행, 고유 CVE 8,833개), 벤더 인덱스(163개 벤더), 통계 자동 갱신
- `advisory_lookup.py`: 제품(영문 단어 경계·한영 별칭)/CVE/벤더/기간/유형 조회, Markdown·JSON 출력
- 공지별 참고사이트(`[n] URL`, 벤더 권고·NVD 등) 2,005개와 첨부 파일명 수록, 저장소에 원본이 있으면 첨부 열람용 로컬 경로 표시
- start/check/fix 스킬(EN/KO)에 KISA 보안공지 분기 연결, CII 패치 관리 항목의 근거로 활용
- CI: advisory 데이터 스키마·EN/KO 동일성·통계 일치 검증, Python 단위 테스트 추가
- `marketplace.json` 버전을 3.4.0으로 갱신 (기존 3.2.0에 머물러 있던 불일치 해소)

### v3.3.0 (2026-04-08)

**새 가이드라인 추가: SW 공급망 보안 (SBOM)**
- 출처: SW 공급망 보안 가이드라인 요약본 22p + 전체본 100p (국정원·과기정통부·KISA, 2024.05)
- 5개 단계(설계/개발/공급/운영/유지보수), 29개 자가점검 항목 (SC-01~SC-29)
- SBOM 표준: SPDX, CycloneDX, NIS-SBOM (20개 기본항목)
- SBOM 생성 스크립트 (Syft, CycloneDX CLI, npm/pip/maven/go)
- 보안취약점 스캔 스크립트 (Grype, npm audit, pip-audit, govulncheck)
- CI/CD 파이프라인 통합 가이드 (GitHub Actions, GitLab CI)
- 규제 동향: 미국 EO 14028, EU CRA (2026 하반기), NIS-SBOM
- 8개 스킬(EN/KO)에 `references/supply-chain/` + `templates/supply-chain/` + `scripts/supply-chain/` 배치
- authorkit: PDF juice → analyze → draft 통합본 작성 완료

### v3.2.0 (2026-04-02)

**새 가이드라인 추가: 시큐어코딩 가이드**
- 출처: KISA Javascript 시큐어코딩 가이드 159p + Python 시큐어코딩 가이드 176p (2023년 개정본)
- 7개 카테고리, 46개 항목, 49 CWE 매핑
- 범용 Pseudo Code 가이드 신규 작성 (언어 무관 UNSAFE/SAFE 패턴)
- JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy) 프레임워크별 코드 예시
- 공식문서 Markdown 변환 (JS 3,241줄 + Python 4,377줄 + 이미지 127개)
- 8개 스킬(EN/KO) 모두에 `references/secure-coding/` + `templates/secure-coding/` 배치

### v3.1.0 (2026-04-02)

**구조 리팩토링 — references/templates/scripts 3분류 분리**

| 변경 | 이전 (v3.0) | 이후 (v3.1) |
|------|------------|------------|
| 리소스 구조 | references/ 단일 디렉터리 | references/ + templates/ + scripts/ 3분류 |
| 스크립트 | 인라인 코드 블록 (345줄) | 독립 스크립트 파일 (7,000+줄) |
| 체크리스트 | references에 혼재 | templates/로 분리 |
| 명령어 형식 | `/kesekit-start` | `/kesekit-start` (네임스페이스:스킬) |

**CII 스크립트 대폭 보강 (원본 873페이지 가이드 기반)**
- Unix: 112 → 1,531줄 (U-01~U-67, Linux/Solaris/AIX/HP-UX)
- Windows: 80 → 1,489줄 (W-01~W-64, PowerShell/레지스트리)
- Web Application: 31 → 880줄 (21개 취약점, Java/PHP/JS 코드 예시)
- Web Service: 30 → 725줄 (WEB-01~WEB-26, Apache/Nginx/IIS/Tomcat)
- Network: 28 → 892줄 (N-01~N-38, Cisco/Juniper)
- Database: 18 → 649줄 (D-01~D-26, Oracle/MySQL/MSSQL/PostgreSQL)
- Cloud: 20 → 517줄 (CA-01~CA-19, AWS/Azure/GCP CLI)
- PC: 26 → 348줄 (PC-01~PC-18, PowerShell/GPO)

**로봇 보안 스크립트 신규 추가**
- 출처: 로봇 보안취약점 점검 체크리스트 해설서 (ref-005)
- firewall-hardening, resource-management, sbom-audit, cert-and-protocol 4개 파일

### v3.0.0 (2026-04-02)

**Breaking Change: 명령어 형식 변경**
- 모든 스킬이 단일 `kesekit` 네임스페이스로 통합
- 명령어 형식: `/start` → `/kesekit-start` (네임스페이스 접두사 추가)
- 기존 사용자는 재설치 필요: `/plugin uninstall kesekit` → `/plugin install kesekit@cdppcorp-KESE-KIT`

**새 가이드라인 추가: 우주 보안**
- 출처: 우주 보안모델 Part1 134p + Part2 223p + 해설서 218p (과기정통부/KISA)
- 12개 분야(AC/IA/SC/SI/SO/IR/PS/PE/RA/SG/CP/SM), 53개 체크리스트 항목
- 대상: 위성 운영사, GSaaS 제공자, 지상국 운영사, 우주 공급망 참여기업
- 참조 표준: CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, CCSDS
- 6개 위협 시나리오 포함 (GSaaS 3개 + 공급망 3개)
- PaddleOCR 기반 한국어 PDF OCR 변환 파이프라인 구축

### v2.1.0 (2026-03-30)

**새 가이드라인 추가: 로봇 보안**
- 출처: 로봇 보안모델(고도화) 156p + 로봇 보안취약점 점검 체크리스트 해설서 225p
- 11개 카테고리, ~103개 체크리스트 항목
- 참조 표준: NIST SP 800-218, IEC 62443, EU CRA, EU RED, NIS2
- 6개 reference 파일 추가

### v2.0.0 (2026-03-30)

**구조 리팩토링 — Progressive Disclosure 패턴 적용**

| 변경 | 이전 (v1.0) | 이후 (v2.0) |
|------|------------|------------|
| SKILL.md | 모든 지식이 인라인 (270~465줄) | 라우터만 (~50~80줄) |
| 가이드라인 | CII만 지원 | CII + AI 보안 지원 |
| 지식 저장 | SKILL.md에 하드코딩 | `references/` 분리 (18개 파일) |
| 항목 코드 | 일부 항목만 포함 | 2026 가이드 기반 전체 항목 |
| 확장성 | 새 가이드라인 추가 시 스킬 수 증가 | 스킬 4개 고정, references만 추가 |

**새 가이드라인 추가: AI 보안 안내서**
- 출처: 과학기술정보통신부·한국인터넷진흥원 「인공지능(AI) 보안 안내서」
- AI 개발자 54개 검증항목 (6단계 생명주기)
- AI 서비스 제공자 보안 요구사항
- AI 이용자 보안 수칙 7개

**CII 가이드라인 업데이트**
- 2026 상세가이드 기반으로 전체 항목 재추출
- 항목 코드 체계 반영 (WEB, HV, CA 등 신규 코드)

### v1.0.0 (2026-03-29)

- 초기 릴리스
- CII 취약점 분석평가 스킬 4개 (한/영)
- 기술적(424) + 관리적(127) + 물리적(9) 항목

---

## 법적 근거

- **정보통신기반 보호법** (Act on Protection of Information and Communications Infrastructure)
- **전자정부법** (e-Government Act)
- **개인정보 보호법** (Personal Information Protection Act)
- **인공지능 기본법** (AI Basic Act, 2026.1.22 시행)

---

## 관련 자료

- [KISA 기술적 취약점 분석평가 상세 가이드](https://www.kisa.or.kr)
- [인공지능(AI) 보안 안내서](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Built With

| Plugin | Description |
|--------|-------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | 책 집필 지원 스킬 - PDF 분석, 구조 추출, 퇴고/재작성 |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Windows 환경 Claude Code 플러그인 훅 호환성 |

---

## License

MIT License

## Author

CDPP Corp (https://github.com/cdppcorp)
