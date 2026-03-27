# KESE - KISA Enhanced Security Evaluation Kit

주요정보통신기반시설(CII) 취약점 분석평가를 위한 Claude Code 스킬 플러그인입니다.

[English](#english) | [한국어](#한국어)

---

## English

### Overview

KESE (KISA Enhanced Security Evaluation Kit) is a Claude Code plugin that provides comprehensive vulnerability assessment capabilities based on KISA (Korea Internet & Security Agency) guidelines for Critical Information Infrastructure (CII).

### Features

| Skill | Description |
|-------|-------------|
| `/kesekit-en:start` | Run full CII vulnerability assessment (Technical 424 + Administrative 127 + Physical 9 items) |
| `/kesekit-en:check` | Pre-deployment CII compliance checklist |
| `/kesekit-en:fix` | Auto-generate hardening scripts for Unix/Windows/Web/DB |
| `/kesekit-en:guide` | Generate secure coding prompts for AI tools |

### Assessment Coverage

**Technical Assessment (424 items)**
- Unix/Linux (U-01~U-68): Account, File, Service, Patch, Log management
- Windows (W-01~W-73): Account, Service, Patch, Log, Security management
- Web Service (WS-01~WS-47): Input validation, Security features, Error handling
- Security Equipment (S-01~S-19): Firewall, IDS/IPS configuration
- Network Equipment (N-01~N-40): Router, Switch configuration
- Control System (C-01~C-45): SCADA, PLC security
- PC/Terminal (PC-01~PC-18): Endpoint security
- Database (D-01~D-32): DB access control, Encryption
- Virtualization (V-01~V-36): VM security, Hypervisor
- Cloud (CL-01~CL-14): Cloud-specific controls

**Administrative Assessment (127 items)**
- Information Security Policy & Organization (A-01~A-22)
- Asset & Risk Management (A-23~A-43)
- Human Resources Security (A-44~A-60)
- Access Control (A-61~A-85)
- Operations Security (A-86~A-103)
- Incident Response & Business Continuity (A-104~A-118)

**Physical Assessment (9 items)**
- Protected Area Designation (B-01)
- Access Control (B-02~B-05)
- Asset & Environment Management (B-06~B-09)

### Installation

```bash
# Install from marketplace
claude plugins install kesekit-en@kesekit
```

### Usage

```bash
# Start full security assessment
/kesekit-en:start

# Run pre-deployment checklist
/kesekit-en:check

# Generate hardening scripts
/kesekit-en:fix

# Get secure coding prompts
/kesekit-en:guide
```

---

## 한국어

### 개요

KESE(KISA Enhanced Security Evaluation Kit)는 KISA(한국인터넷진흥원) 가이드라인에 기반한 주요정보통신기반시설(CII) 취약점 분석평가 기능을 제공하는 Claude Code 플러그인입니다.

### 기능

| 스킬 | 설명 |
|------|------|
| `/kesekit-ko:start` | 전체 CII 취약점 분석평가 실행 (기술적 424 + 관리적 127 + 물리적 9항목) |
| `/kesekit-ko:check` | 배포 전 CII 컴플라이언스 체크리스트 |
| `/kesekit-ko:fix` | Unix/Windows/Web/DB용 하드닝 스크립트 자동 생성 |
| `/kesekit-ko:guide` | AI 도구용 시큐어코딩 프롬프트 생성 |

### 평가 범위

**기술적 취약점 평가 (424항목)**
- Unix/Linux (U-01~U-68): 계정, 파일, 서비스, 패치, 로그 관리
- Windows (W-01~W-73): 계정, 서비스, 패치, 로그, 보안 관리
- 웹 서비스 (WS-01~WS-47): 입력값 검증, 보안 기능, 에러 처리
- 보안장비 (S-01~S-19): 방화벽, IDS/IPS 설정
- 네트워크장비 (N-01~N-40): 라우터, 스위치 설정
- 제어시스템 (C-01~C-45): SCADA, PLC 보안
- PC/단말 (PC-01~PC-18): 엔드포인트 보안
- 데이터베이스 (D-01~D-32): DB 접근 제어, 암호화
- 가상화 (V-01~V-36): VM 보안, 하이퍼바이저
- 클라우드 (CL-01~CL-14): 클라우드 특화 통제

**관리적 취약점 평가 (127항목)**
- 정보보호 정책 및 조직 (A-01~A-22)
- 자산 및 위험 관리 (A-23~A-43)
- 인적 보안 (A-44~A-60)
- 접근 통제 (A-61~A-85)
- 운영 보안 (A-86~A-103)
- 침해사고 대응 및 업무 연속성 (A-104~A-118)

**물리적 취약점 평가 (9항목)**
- 보호구역 지정 (B-01)
- 출입 통제 (B-02~B-05)
- 자산 및 환경 관리 (B-06~B-09)

### 설치

```bash
# 마켓플레이스에서 설치
claude plugins install kesekit-ko@kesekit
```

### 사용법

```bash
# 전체 보안 평가 시작
/kesekit-ko:start

# 배포 전 체크리스트 실행
/kesekit-ko:check

# 하드닝 스크립트 생성
/kesekit-ko:fix

# 시큐어코딩 프롬프트 가져오기
/kesekit-ko:guide
```

---

## 책자 자료

### 통합 가이드북

KESE KIT의 전체 내용을 담은 통합 가이드북도 제공됩니다:

| 파일 | 설명 |
|------|------|
| `authorkit/KESE-KIT-완전판.md` | 한글 통합본 (22개 장 + 부록) |
| `authorkit/KESE-KIT-Complete-Guide.md` | 영문 통합본 (22 Chapters) |

### 챕터별 가이드

| Part | 챕터 | 주제 |
|------|------|------|
| I | 1-2 | 기반시설 보안 개요, 취약점 분석 방법론 |
| II | 3-12 | 기술적 취약점 (Unix, Windows, Web, DB, 네트워크 등) |
| III | 13-19 | 관리적/물리적 취약점 |
| IV | 20-22 | 실무 적용 (공공사업, 조달, 자동화) |

---

## 법적 근거

본 평가는 다음 법적 근거를 따릅니다:

- **정보통신기반 보호법** (Act on Protection of Information and Communications Infrastructure)
- **전자정부법** (e-Government Act)
- **개인정보 보호법** (Personal Information Protection Act)
- **국가정보보안 기본지침** (National Information Security Basic Guidelines)

---

## 관련 자료

- [KISA 기술적 취약점 분석평가 상세 가이드](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## 프로젝트 구조

```
KESE/
├── .claude-plugin/
│   └── marketplace.json           ← 플러그인 메타데이터
├── skills/                         ← 영문 스킬
│   ├── start/SKILL.md
│   ├── check/SKILL.md
│   ├── fix/SKILL.md
│   └── guide/SKILL.md
├── skills-ko/                      ← 한글 스킬
│   ├── start/SKILL.md
│   ├── check/SKILL.md
│   ├── fix/SKILL.md
│   └── guide/SKILL.md
├── authorkit/
│   ├── drafts/                     ← 한글 챕터별 파일
│   ├── drafts-en/                  ← 영문 챕터별 파일
│   ├── KESE-KIT-완전판.md          ← 한글 통합본
│   └── KESE-KIT-Complete-Guide.md  ← 영문 통합본
└── README.md
```

---

## License

MIT License

## Author

CDPP Corp (https://github.com/cdppcorp)
