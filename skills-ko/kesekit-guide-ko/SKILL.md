---
name: kesekit-guide-ko
description: AI 도구(Claude, ChatGPT, Cursor, Copilot)용 시큐어 코딩 프롬프트와 가이드를 생성합니다. KISA CII, CWE 매핑, AI 보안, 로봇 보안, 우주 보안(CCSDS/위성 프로토콜/GSaaS/공급망) 가이드를 지원합니다. "보안 가이드 생성", "시큐어코딩 가이드", "우주 시큐어코딩", "위성 보안 가이드" 시 사용하세요.
---

# KESE 시큐어 코딩 프롬프트 생성기

KISA 가이드라인과 국제 표준(OWASP, CWE)을 기반으로 AI 도구용 시큐어 코딩 프롬프트를 생성합니다.

## 가이드라인 선택

| # | 가이드라인 | 설명 |
|---|----------|------|
| 1 | **CII 시큐어코딩** | 전통적 보안 취약점 (SQL Injection, XSS 등) |
| 2 | **AI 보안 시큐어코딩** | AI 특화 보안 (Prompt Injection, 데이터 중독 등) |
| 3 | **로봇 보안 시큐어코딩** | 로봇 특화 보안 (IEC 62443, 펌웨어, 통신 프로토콜) |
| 4 | **우주 보안 시큐어코딩** | 우주 특화 보안 (CCSDS, 위성 프로토콜, GSaaS, 공급망) |
| 5 | **시큐어코딩 (언어별)** | 언어별 시큐어코딩 (JS, Python, pseudo code) |
| 6 | **제로트러스트 가이드** | 제로트러스트 아키텍처 및 성숙도 평가 가이드 (8개 핵심요소, ~396항목) |

웹/서버/DB 개발 → **CII** / AI 모델/LLM/AI 서비스 개발 → **AI 보안** / 로봇 펌웨어, ROS/ROS2, 로봇 API, 산업 프로토콜 개발 → **로봇 보안** / 위성 통신, 지상국, GSaaS API, 우주 공급망 → **우주 보안** / JavaScript, Python, 기타 언어 → **시큐어코딩 (언어별)**
Zero Trust, ZTA, ZTNA, 제로트러스트, 마이크로세그멘테이션, microsegmentation, SDP, SASE, PEP/PDP, never trust always verify → **제로트러스트**

---

## CII 분기 시

`templates/cii/webapp.md`를 참조하여 CWE 기반 시큐어 코딩 프롬프트를 생성합니다. 점검/수정 스크립트는 `scripts/cii/`에 있습니다.

### 실행 흐름
1. 사용자에게 대상 컨텍스트 확인 (언어, 프레임워크, 기능 유형)
2. 커스터마이징된 시큐어 코딩 프롬프트 생성
3. 관련 CWE 패턴 및 KISA 가이드라인 포함
4. 복사-붙여넣기 형식으로 프롬프트 제공

### 주요 CWE 패턴

| CWE | 이름 | 방지 방법 |
|-----|------|----------|
| CWE-20 | 부적절한 입력 검증 | 모든 입력 검증 |
| CWE-22 | 경로 조작 | 경로 정규화 및 검증 |
| CWE-78 | OS Command Injection | shell 피하기, 인자 리스트 |
| CWE-79 | XSS | 출력 인코딩, CSP |
| CWE-89 | SQL Injection | 매개변수화된 쿼리 |
| CWE-94 | Code Injection | eval(), exec() 피하기 |
| CWE-287 | 부적절한 인증 | 검증된 프레임워크 사용 |
| CWE-327 | 약한 암호화 | AES-256, RSA-2048+ |
| CWE-352 | CSRF | CSRF 토큰 |
| CWE-434 | 무제한 업로드 | 타입, 크기, 이름 검증 |
| CWE-502 | 안전하지 않은 역직렬화 | JSON 사용 |
| CWE-611 | XXE | 외부 엔티티 비활성화 |
| CWE-798 | 하드코딩된 자격 증명 | 환경 변수 사용 |
| CWE-918 | SSRF | URL 검증, 사설 IP 차단 |

### 언어별 프롬프트 생성
사용자가 지정한 언어에 맞게 시큐어 코딩 프롬프트를 생성합니다:
- **Python**: SQL Injection, Command Injection, 경로 조작, 역직렬화, 패스워드 해싱
- **JavaScript/Node.js**: XSS, SQL Injection, Command Injection, 안전한 난수
- **Java**: SQL Injection, XXE, 경로 조작, 역직렬화
- **Go, Rust, C#** 등 요청 시 해당 언어에 맞게 생성

### 기능별 프롬프트 생성
- 인증 구현, 파일 업로드, API 보안, 세션 관리 등

---

## AI 보안 분기 시

`templates/ai-security/developer.md`와 `references/ai-security/overview.md`를 참조하여 AI 특화 시큐어 코딩 프롬프트를 생성합니다.

### AI 보안 위협별 방어 프롬프트

| 위협 | 방어 방법 |
|------|----------|
| Prompt Injection | 입출력 필터링, 시스템/사용자 프롬프트 분리, 가드레일 |
| 데이터 중독 | 이상치 탐지, 데이터 무결성 검증, 적대적 훈련 |
| 모델 추출 | 쿼리 제한, 출력 제한, 워터마킹, 차등 프라이버시 |
| 민감 정보 노출 | 출력 필터링, PII 마스킹, 학습 데이터 정제 |
| 적대적 예제 | 적대적 훈련, 입력 전처리, 앙상블 방어 |
| LLM 탈옥 | 콘텐츠 필터링, 안전 가드레일, 출력 모니터링 |

### AI 보안 시큐어 코딩 영역
1. **데이터 파이프라인 보안** — 수집, 전처리, 저장 암호화
2. **모델 학습 보안** — 환경 격리, 데이터 검증, 연합학습 보안
3. **모델 배포 보안** — API 인증, Rate Limiting, TLS
4. **LLM 운영 보안** — Prompt Guard, 출력 검증, RAG 보안
5. **모델 파기 보안** — 안전한 삭제, API 비활성화

---

## 로봇 보안 분기 시

`templates/robot-security/overview.md`를 먼저 읽고, 목적에 따라 `ssdf.md`, `supply-chain.md`, `iec62443.md`, `cyber-resilience.md`, `wireless.md`를 참조하여 로봇 특화 시큐어 코딩 프롬프트를 생성합니다.

### 로봇 보안 시큐어 코딩 영역
1. **펌웨어/임베디드 보안** — 안전한 부팅, 무결성 검증, 업데이트 보안
2. **ROS/ROS2 및 미들웨어 보안** — 노드 인증, 토픽/서비스 접근 통제
3. **원격 관리/API 보안** — 인증, 권한, 감사 로그
4. **산업용/무선 프로토콜 보안** — IEC 62443, RED 요구사항 반영
5. **공급망 보안** — SBOM, 서드파티 의존성 검증, 배포 무결성

---

## 시큐어코딩 (언어별) 분기 시

`references/secure-coding/overview.md`에서 7개 카테고리와 49개 CWE 매핑을 참조합니다. `references/secure-coding/pseudocode.md`에서 언어 무관 패턴(46항목, UNSAFE/SAFE 쌍)을 참조합니다. 언어별 프롬프트는 `templates/secure-coding/javascript.md`(Express.js, Sequelize, Node.js) 또는 `templates/secure-coding/python.md`(Django, Flask, SQLAlchemy)를 사용합니다.

### 자동 판별 기준
- JavaScript, Node.js, Express, React, Vue → `templates/secure-coding/javascript.md`
- Python, Django, Flask, FastAPI → `templates/secure-coding/python.md`
- 기타 언어 (Go, Java, Rust, C#) → `references/secure-coding/pseudocode.md` (AI가 패턴 적응)
- 일반 / 언어 무관 → `references/secure-coding/pseudocode.md`

---

## 제로트러스트 분기 시

`references/zero-trust/overview.md`에서 ZT 아키텍처를, `references/zero-trust/maturity-model.md`에서 성숙도 정의를 참조합니다. `templates/zero-trust/overview.md`에서 평가 가이드를 참조합니다. 핵심요소별 템플릿을 기반으로 ZT 구현 프롬프트를 생성합니다. OT/ICS 환경은 `templates/zero-trust/ot-environment.md`와 `references/zero-trust/ot-guide.md`를 참조합니다.

| 주제 | reference 파일 |
|------|---------------|
| 개요 | `templates/zero-trust/overview.md` |
| 식별자 및 디바이스 | `templates/zero-trust/identity-device.md` |
| 네트워크 및 시스템 | `templates/zero-trust/network-system.md` |
| 애플리케이션 및 데이터 | `templates/zero-trust/app-data.md` |
| 가시성 및 자동화 | `templates/zero-trust/visibility-automation.md` |
| OT/ICS 환경 | `templates/zero-trust/ot-environment.md` |
| ZT 아키텍처 참조 | `references/zero-trust/overview.md` |
| 성숙도 모델 상세 | `references/zero-trust/maturity-model.md` |
| OT 배포 가이드 | `references/zero-trust/ot-guide.md` |

8개 핵심요소, ~396개 항목, 4단계 성숙도. 표준: KISA 제로트러스트 가이드라인 2.0, NIST SP 800-207, CISA ZT Maturity Model.

---

## 사용법

관련 프롬프트를 복사하여 AI 어시스턴트 대화에 붙여넣은 후 코드 작성을 요청하세요.

```
[여기에 시큐어 코딩 요구사항 붙여넣기]

이제 Python/FastAPI로 사용자 등록 엔드포인트를 구현해주세요.
```
