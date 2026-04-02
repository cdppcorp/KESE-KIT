# KESE - KISA Enhanced Security Evaluation Kit

주요정보통신기반시설(CII) 취약점 분석평가, AI 보안 평가, 로봇 보안 점검, 우주 보안 점검을 위한 Claude Code 스킬 플러그인입니다.

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
/kesekit:start-ko     보안 취약점 분석평가 실행
/kesekit:check-ko     배포 전 보안 체크리스트
/kesekit:fix-ko       취약점 자동 수정 / 하드닝 스크립트 생성
/kesekit:guide-ko     시큐어코딩 가이드 프롬프트 생성
```

영문 버전도 사용 가능합니다:

```
/kesekit:start        Full security assessment
/kesekit:check        Pre-deployment checklist
/kesekit:fix          Generate hardening scripts
/kesekit:guide        Secure coding prompts
```

### 사용 예시

```
# 프로젝트 폴더에서 Claude Code 실행 후:

> /kesekit:start-ko
  → "어떤 시스템을 점검하시겠습니까?" 질문에 답변
  → 예: "Ubuntu 22.04 웹 서버", "Windows Server 2022", "AI 모델 배포 환경"

> /kesekit:check-ko
  → 배포 전 보안 컴플라이언스 자동 체크

> /kesekit:fix-ko
  → 취약점 분석 결과를 기반으로 하드닝 스크립트 자동 생성

> /kesekit:guide-ko
  → "Python Flask 인증 구현" 같은 요청에 시큐어코딩 프롬프트 제공
```

---

## 개요

KESE(KISA Enhanced Security Evaluation Kit)는 KISA(한국인터넷진흥원) 가이드라인에 기반한 보안 취약점 분석평가 기능을 제공하는 Claude Code 플러그인입니다. 주요정보통신기반시설(CII) 취약점 분석평가, AI 보안 평가, 로봇 보안 점검, 우주 보안 점검을 지원합니다.

### 기능

| 스킬 | 설명 |
|------|------|
| `/kesekit:start-ko` | 전체 보안 취약점 분석평가 실행 (CII 560+ / AI 보안 / 로봇 보안 / 우주 보안) |
| `/kesekit:check-ko` | 배포 전 보안 컴플라이언스 체크리스트 (CII / AI / 로봇 / 우주) |
| `/kesekit:fix-ko` | 하드닝 스크립트 및 보안 수정 자동 생성 (CII / AI / 로봇 / 우주) |
| `/kesekit:guide-ko` | AI 도구용 시큐어코딩 프롬프트 생성 및 로봇/우주 보안 개발 가이드 |

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

### 원본 문서

본 플러그인은 다음 공식 보안 가이드라인을 기반으로 재구성되었습니다:

| # | 문서명 | 발행기관 | 연도 | 페이지 | PDF |
|---|--------|---------|:----:|:------:|:---:|
| 1 | **주요정보통신기반시설 기술적 취약점 분석·평가방법 상세가이드** | KISA | 2026 | 873 | [PDF](문서/주요정보통신기반시설%20기술적%20취약점%20분석·평가%20방법%20상세가이드.pdf) |
| 2 | **주요정보통신기반시설 관리·물리적 취약점 분석·평가 방법 안내서** | KISA | 2026 | 332 | [PDF](문서/주요정보통신기반시설%20관리·물리적%20취약점%20분석·평가%20방법%20안내서.pdf) |
| 3 | **인공지능(AI) 보안 안내서** | 과기정통부 / KISA | 2026 | 239 | [PDF](문서/인공지능(AI)%20보안%20안내서(정오%20수정).pdf) |
| 4 | **로봇 보안모델(고도화)** | KISA | 2026 | 156 | [PDF](문서/로봇%20보안모델(고도화).pdf) |
| 5 | **로봇 보안취약점 점검 체크리스트 해설서** | KISA | 2026 | 225 | [PDF](문서/로봇%20보안취약점%20점검%20체크리스트%20해설서.pdf) |
| 6 | **우주 보안모델 Part1** (위성활용 서비스) | 과기정통부 / KISA | 2024 | 134 | - |
| 7 | **우주 보안모델 Part2** (GSaaS/우주 공급망) | 과기정통부 / KISA | 2025 | 223 | - |
| 8 | **우주 보안모델 해설서 및 사례집** | 과기정통부 / KISA | 2025 | 218 | - |

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
| `/start` | `/kesekit:start` |
| `/check` | `/kesekit:check` |
| `/fix` | `/kesekit:fix` |
| `/guide` | `/kesekit:guide` |
| `/start-ko` | `/kesekit:start-ko` |
| `/check-ko` | `/kesekit:check-ko` |
| `/fix-ko` | `/kesekit:fix-ko` |
| `/guide-ko` | `/kesekit:guide-ko` |

> **참고:** 기존 `/start`, `/check`, `/fix`, `/guide` 명령어는 더 이상 동작하지 않습니다. `/kesekit:*` (콜론) 형식의 네임스페이스 접두사를 사용하세요.

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
/kesekit:start     Full security vulnerability assessment
/kesekit:check     Pre-deployment security checklist
/kesekit:fix       Auto-fix vulnerabilities / generate hardening scripts
/kesekit:guide     Generate secure coding prompts
```

Korean versions are also available:

```
/kesekit:start-ko  보안 취약점 분석평가
/kesekit:check-ko  배포 전 체크리스트
/kesekit:fix-ko    하드닝 스크립트 생성
/kesekit:guide-ko  시큐어코딩 가이드
```

#### Usage Examples

```
# After launching Claude Code in your project folder:

> /kesekit:start
  → Answer "What system do you want to assess?"
  → e.g. "Ubuntu 22.04 web server", "Windows Server 2022", "AI model deployment"

> /kesekit:check
  → Automated pre-deployment compliance check

> /kesekit:fix
  → Generate hardening scripts from assessment results

> /kesekit:guide
  → Request like "Python Flask authentication" → get secure coding prompt
```

### Overview

KESE (KISA Enhanced Security Evaluation Kit) is a Claude Code plugin that provides comprehensive vulnerability assessment capabilities based on KISA (Korea Internet & Security Agency) guidelines. Supports Critical Information Infrastructure (CII), AI Security, Robot Security, and Space Security assessments.

### Features

| Skill | Description |
|-------|-------------|
| `/kesekit:start` | Run full security vulnerability assessment (CII 560+ / AI Security / Robot Security / Space Security) |
| `/kesekit:check` | Pre-deployment security compliance checklist (CII / AI / Robot / Space) |
| `/kesekit:fix` | Auto-generate hardening scripts and security fixes (CII / AI / Robot / Space) |
| `/kesekit:guide` | Generate secure coding prompts for AI, robot, and space-aware secure development |

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

---

## 프로젝트 구조

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← 플러그인 메타데이터
├── skills/                            ← 영문 스킬
│   ├── kesekit-start/
│   │   ├── SKILL.md                  ← 라우터 (~80줄)
│   │   ├── references/               ← 순수 설명/기준 문서
│   │   │   ├── ai-security/          ← 개요, 서비스제공자, 이용자 가이드
│   │   │   └── space-security/       ← 개요, 공급망 위협 시나리오
│   │   ├── templates/                ← 별지 서식, 체크리스트 테이블
│   │   │   ├── cii/                  ← CII 14개 점검항목 테이블
│   │   │   ├── ai-security/          ← AI 개발자 검증항목, 이용자 체크리스트
│   │   │   ├── robot-security/       ← 로봇 보안 6개 체크리스트
│   │   │   └── space-security/       ← 우주 보안 4개 점검항목 테이블
│   │   └── scripts/                  ← 실행 가능한 점검/수정 스크립트
│   │       ├── cii/                  ← bash, PowerShell, SQL 스크립트
│   │       └── robot-security/       ← 방화벽, SBOM, 인증서 스크립트
│   ├── kesekit-check/
│   ├── kesekit-fix/                   ← scripts/space-security/ 추가 포함
│   └── kesekit-guide/
├── skills-ko/                         ← 한글 스킬 (동일 구조)
├── 문서/                              ← 원본 PDF 문서 (8개)
├── authorkit/                         ← 변환 산출물 및 작업 파일
├── docs/                              ← 20개 국어 README
├── CONTRIBUTING.md                    ← 가이드라인 추가 방법
└── README.md
```

---

## 변경 이력

### v3.1.0 (2026-04-02)

**구조 리팩토링 — references/templates/scripts 3분류 분리**

| 변경 | 이전 (v3.0) | 이후 (v3.1) |
|------|------------|------------|
| 리소스 구조 | references/ 단일 디렉터리 | references/ + templates/ + scripts/ 3분류 |
| 스크립트 | 인라인 코드 블록 (345줄) | 독립 스크립트 파일 (7,000+줄) |
| 체크리스트 | references에 혼재 | templates/로 분리 |
| 명령어 형식 | `/kesekit-start` | `/kesekit:start` (네임스페이스:스킬) |

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
- 명령어 형식: `/start` → `/kesekit:start` (네임스페이스 접두사 추가)
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
