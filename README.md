# KESE - KISA Enhanced Security Evaluation Kit

주요정보통신기반시설(CII) 취약점 분석평가, AI 보안 평가, 로봇 보안 점검, 우주 보안 점검을 위한 Claude Code 스킬 플러그인입니다.

🌐 [한국어](#한국어) | [English](#english) | [Français](docs/README.fr.md) | [日本語](docs/README.ja.md) | [中文](docs/README.zh.md) | [Русский](docs/README.ru.md) | [Español](docs/README.es.md) | [Deutsch](docs/README.de.md) | [Português](docs/README.pt.md) | [Italiano](docs/README.it.md) | [العربية](docs/README.ar.md) | [हिन्दी](docs/README.hi.md) | [Türkçe](docs/README.tr.md) | [Tiếng Việt](docs/README.vi.md) | [ภาษาไทย](docs/README.th.md) | [Bahasa Indonesia](docs/README.id.md) | [Polski](docs/README.pl.md) | [Nederlands](docs/README.nl.md) | [Svenska](docs/README.sv.md) | [Українська](docs/README.uk.md)

---

## English

### Overview

KESE (KISA Enhanced Security Evaluation Kit) is a Claude Code plugin that provides comprehensive vulnerability assessment capabilities based on KISA (Korea Internet & Security Agency) guidelines. Supports Critical Information Infrastructure (CII), AI Security, Robot Security, and Space Security assessments.

### Source Documents

This plugin is built upon the following official security guidelines:

| # | Document | Publisher | Year | Pages | PDF |
|---|----------|-----------|:----:|:-----:|:---:|
| 1 | **Technical Vulnerability Assessment Guide for CII** | KISA | 2026 | 873 | [PDF](문서/주요정보통신기반시설%20기술적%20취약점%20분석·평가%20방법%20상세가이드.pdf) |
| 2 | **Administrative & Physical Vulnerability Assessment Guide for CII** | KISA | 2026 | 332 | [PDF](문서/주요정보통신기반시설%20관리·물리적%20취약점%20분석·평가%20방법%20안내서.pdf) |
| 3 | **AI Security Guide** (인공지능(AI) 보안 안내서) | MSIT / KISA | 2026 | 239 | [PDF](문서/인공지능(AI)%20보안%20안내서(정오%20수정).pdf) |
| 4 | **Robot Security Model** (로봇 보안모델(고도화)) | KISA | 2026 | 156 | [PDF](문서/로봇%20보안모델(고도화).pdf) |
| 5 | **Robot Security Checklist Guide** (로봇 보안취약점 점검 체크리스트 해설서) | KISA | 2026 | 225 | [PDF](문서/로봇%20보안취약점%20점검%20체크리스트%20해설서.pdf) |
| 6 | **Space Security Model Part1** (우주 보안모델 Part1) | MSIT / KISA | 2024 | 134 | - |
| 7 | **Space Security Model Part2** (우주 보안모델 Part2 - GSaaS/Supply Chain) | MSIT / KISA | 2025 | 223 | - |
| 8 | **Space Security Explanation Guide** (우주 보안모델 해설서 및 사례집) | MSIT / KISA | 2025 | 218 | - |

### Features

| Skill | Description |
|-------|-------------|
| `/kesekit-start` | Run full security vulnerability assessment (CII 560+ / AI Security / Robot Security / Space Security) |
| `/kesekit-check` | Pre-deployment security compliance checklist (CII / AI / Robot / Space) |
| `/kesekit-fix` | Auto-generate hardening scripts and security fixes (CII / AI / Robot / Space) |
| `/kesekit-guide` | Generate secure coding prompts for AI, robot, and space-aware secure development |

### Supported Guidelines

#### 1. CII (Critical Information Infrastructure) — 560+ items

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

#### 2. AI Security Guide — 54+ items

| Target | Items | Lifecycle |
|--------|:-----:|-----------|
| AI Developer | 54 | 6-stage (Plan→Data→Model→Deploy→Monitor→Decommission) |
| Service Provider | ~43 | 6-stage (Plan→Dev→Ops→Maintain→Feedback→Decommission) |
| User | 7 | Security best practices |

#### 3. Robot Security — ~103 items

| Category | Code | Items | Standard |
|----------|------|:-----:|----------|
| Secure SW Dev (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Supply Chain | SC-01~07 | 7 | NIST SP 800-161 |
| Identification & Auth | IA-01~11 | 11 | IEC 62443 |
| Use Control | UC-01~11 | 11 | IEC 62443 |
| System Integrity | SI-01~11 | 11 | IEC 62443 |
| Data Protection | DP-01~04 | 4 | IEC 62443 |
| Data Flow Restriction | DFR-01~02 | 2 | IEC 62443 |
| Event Response | ER-01~03 | 3 | IEC 62443 |
| Resource Availability | RA-01~08 | 8 | IEC 62443 |
| Cyber Resilience | CR-01~13 | 13 | EU CRA |
| Wireless Security | WS-01~14 | 14 | EU RED |

Target: Industrial / Service / Medical robots (ISO 8373)

#### 4. Space Security — 53 items

| Domain | Code | Items | Standard |
|--------|------|:-----:|----------|
| Access Control | AC-01~12 | 12 | CMMC, K-RMF |
| Identification & Authentication | IA-01~02 | 2 | CMMC, NIS2 |
| System & Communication Security | SC-01~07 | 7 | NIST IR 8401 |
| System & Information Integrity | SI-01~04 | 4 | NIST CSF |
| System/Service Operations | SO-01~09 | 9 | ISMS-P |
| Incident Response | IR-01~02 | 2 | NIS2 |
| Personnel Security | PS-01~02 | 2 | CMMC |
| Physical Security | PE-01~03 | 3 | K-RMF |
| Risk Assessment | RA-01~02 | 2 | NIST CSF |
| Security Governance | SG-01~04 | 4 | ISMS-P |
| Contingency Planning | CP-01~02 | 2 | NIST IR 8270 |
| Supply Chain Management | SM-01~04 | 4 | CMMC, NIS2 |

Target: Satellite operators, GSaaS providers, Ground station operators, Space supply chain

### Installation

```bash
claude plugins install kesekit
```

### Usage

```bash
# English
/kesekit-start     # Full security assessment
/kesekit-check     # Pre-deployment checklist
/kesekit-fix       # Generate hardening scripts
/kesekit-guide     # Secure coding prompts

# Korean (한국어)
/kesekit-start-ko  # 전체 보안 평가
/kesekit-check-ko  # 배포 전 체크리스트
/kesekit-fix-ko    # 하드닝 스크립트 생성
/kesekit-guide-ko  # 시큐어코딩 프롬프트
```

---

## 한국어

### 개요

KESE(KISA Enhanced Security Evaluation Kit)는 KISA(한국인터넷진흥원) 가이드라인에 기반한 보안 취약점 분석평가 기능을 제공하는 Claude Code 플러그인입니다. 주요정보통신기반시설(CII) 취약점 분석평가, AI 보안 평가, 로봇 보안 점검, 우주 보안 점검을 지원합니다.

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

### 기능

| 스킬 | 설명 |
|------|------|
| `/kesekit-start-ko` | 전체 보안 취약점 분석평가 실행 (CII 560+ / AI 보안 / 로봇 보안 / 우주 보안) |
| `/kesekit-check-ko` | 배포 전 보안 컴플라이언스 체크리스트 (CII / AI / 로봇 / 우주) |
| `/kesekit-fix-ko` | 하드닝 스크립트 및 보안 수정 자동 생성 (CII / AI / 로봇 / 우주) |
| `/kesekit-guide-ko` | AI 도구용 시큐어코딩 프롬프트 생성 및 로봇/우주 보안 개발 가이드 |

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

### 설치

```bash
claude plugins install kesekit
```

### 사용법

```bash
# 한국어
/kesekit-start-ko   # 전체 보안 평가 시작
/kesekit-check-ko   # 배포 전 체크리스트 실행
/kesekit-fix-ko     # 하드닝 스크립트 생성
/kesekit-guide-ko   # 시큐어코딩 프롬프트 가져오기

# English
/kesekit-start       # Full security assessment
/kesekit-check       # Pre-deployment checklist
/kesekit-fix         # Generate hardening scripts
/kesekit-guide       # Secure coding prompts
```

---

## 프로젝트 구조

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← 플러그인 메타데이터
├── skills/                            ← 영문 스킬 (라우터)
│   ├── kesekit-start/
│   │   ├── SKILL.md                  ← 라우터 (~80줄)
│   │   └── references/               ← 가이드라인별 지식
│   │       ├── cii/                  ← CII 14개 reference
│   │       ├── ai-security/          ← AI 보안 4개 reference
│   │       ├── robot-security/       ← 로봇 보안 6개 reference
│   │       └── space-security/       ← 우주 보안 6개 reference
│   ├── kesekit-check/
│   ├── kesekit-fix/
│   └── kesekit-guide/
├── skills-ko/                         ← 한글 스킬 (동일 구조)
├── 문서/                              ← 원본 PDF 문서 (8개)
├── authorkit/                         ← 변환 산출물 및 작업 파일
│   ├── converted/
│   │   ├── ref-001/                  ← 관리·물리적 가이드 (full.md)
│   │   ├── ref-002/                  ← 기술적 가이드 (full.md)
│   │   ├── ref-003/                  ← AI 보안 안내서 (full.md)
│   │   ├── ref-004/                  ← 로봇 보안모델 (full.md)
│   │   ├── ref-005/                  ← 로봇 체크리스트 해설서 (full.md)
│   │   ├── ref-006/                  ← 우주 보안모델 Part1 요약본 (full.md)
│   │   ├── ref-007/                  ← 우주 보안모델 Part1 (full.md)
│   │   ├── ref-008/                  ← 우주 보안모델 Part2 요약본 (full.md)
│   │   ├── ref-009/                  ← 우주 보안모델 Part2 (full.md)
│   │   └── ref-010/                  ← 우주 보안모델 해설서 (full.md)
│   └── ...
├── docs/                              ← 20개 국어 README
├── CONTRIBUTING.md                    ← 가이드라인 추가 방법
└── README.md
```

---

## 변경 이력

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

### v2.1.0 (2026-03-30)

**새 가이드라인 추가: 로봇 보안**
- 출처: 로봇 보안모델(고도화) 156p + 로봇 보안취약점 점검 체크리스트 해설서 225p
- 11개 카테고리, ~103개 체크리스트 항목
- 참조 표준: NIST SP 800-218, IEC 62443, EU CRA, EU RED, NIS2
- 6개 reference 파일 추가

### v3.0.0 (2026-04-02)

**새 가이드라인 추가: 우주 보안**
- 출처: 우주 보안모델 Part1 134p + Part2 223p + 해설서 218p (과기정통부/KISA)
- 12개 분야(AC/IA/SC/SI/SO/IR/PS/PE/RA/SG/CP/SM), 53개 체크리스트 항목
- 대상: 위성 운영사, GSaaS 제공자, 지상국 운영사, 우주 공급망 참여기업
- 참조 표준: CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, CCSDS
- 6개 위협 시나리오 포함 (GSaaS 3개 + 공급망 3개)
- PaddleOCR 기반 한국어 PDF OCR 변환 파이프라인 구축

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
