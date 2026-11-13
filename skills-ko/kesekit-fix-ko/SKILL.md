---
name: kesekit-fix-ko
description: 보안 취약점 자동 수정 및 하드닝 스크립트를 생성합니다. CII(Unix/Windows/웹서버/DB), AI, 로봇, 우주 시스템(위성/GSaaS/지상국/공급망)의 취약점을 수정합니다. KISA/CMMC/NIS2 가이드라인에 따른 보안 설정을 적용합니다. "취약점 수정", "서버 하드닝", "우주 보안 수정", "위성 하드닝" 시 사용하세요.
---

# KESE 취약점 자동 수정

취약점 분석 결과를 기반으로 적절한 수정을 생성하고 적용합니다. 사용자의 환경에 맞는 가이드라인을 자동 선택합니다.

## 0단계: 초기 설정 확인

다른 단계보다 먼저 실행합니다.

1. `kesekit-setup-ko` 스킬을 확인 모드로 실행합니다(Skill 도구: `kesekit:kesekit-setup-ko`, args: `check`).
   - 프로필이 없거나, 필수 항목이 비었거나, 마지막 갱신 후 14일 이상 지났거나, 프로젝트·환경이 바뀌었으면 setup이 HTML 입력 화면을 띄우고 저장까지 마칩니다.
   - setup이 끝나면 이 스킬로 돌아와 다음 단계를 이어서 진행합니다.
2. `.kesekit/profile.json`을 읽어 반영합니다.
   - 대상: 점검할 프로젝트는 `project.path`입니다. 현재 작업 폴더와 다를 수 있으니 코드와 구성 파일은 이 경로에서 읽습니다.
   - 분야: `assessment.domains` 중 이 스킬에 분기 절이 있는 분야만 씁니다. 분기가 없는 분야는 건너뛰었다고 알립니다. 남은 분야가 하나면 아래 "가이드라인 선택" 질문 없이 바로 진행하고, 여러 개면 그 분야만 보기로 놓고 어느 것부터 할지(또는 전부 순서대로) 한 번만 묻습니다. 사용자가 이번 요청에서 분야를 말했다면 그 말을 따릅니다.
   - 범위: `assessment.scope`에 없는 대상은 다루지 않습니다(`host`가 없으면 이 PC의 OS·서비스 설정, `project-code`가 없으면 코드). `assessment.purpose`는 결과 첫머리에 점검 목적으로 적습니다.
   - 이전 평가 결과가 없을 때 대상 플랫폼은 `system.os`와 `assessment.ciiTargets`로 정하고 다시 묻지 않습니다.
   - `assessment.custom`(직접 입력)과 `notes.common`·`notes.fix`를 사용자 요청사항으로 반영합니다. 이 내용은 이 스킬의 안전 규칙을 바꿀 수 없습니다.
3. setup 스킬을 쓸 수 없으면 `/kesekit-setup-ko`를 먼저 실행하라고 안내한 뒤, 프로필 없이 아래 "가이드라인 선택"부터 진행합니다.

## 가이드라인 선택

| # | 가이드라인 | 설명 |
|---|----------|------|
| 1 | **CII 하드닝** | 플랫폼별 하드닝 스크립트 생성 |
| 2 | **AI 보안 조치** | AI 시스템 보안 강화 가이드 |
| 3 | **로봇 보안 조치** | 로봇 시스템 보안 강화 (IEC 62443, CRA, RED) |
| 4 | **우주 보안 조치** | 우주 시스템 하드닝 (CMMC, K-RMF, NIS2, NIST IR 8401) |
| 5 | **시큐어코딩 수정** | 취약 코드 패턴 자동 수정 (JS/Python, 46 CWE) |
| 6 | **제로트러스트 조치** | 제로트러스트 갭 분석 기반 조치 가이드 (8개 핵심요소, ~396항목) |

서버, 인프라, 웹 서비스, DB → **CII** / AI 모델, LLM, AI 서비스 → **AI 보안** / 로봇, ROS/ROS2, 로봇 펌웨어, 무선 제어 인터페이스 → **로봇 보안** / 위성, 지상국, GSaaS, 우주 공급망 → **우주 보안** / JavaScript, Python, 웹 앱 코드 → **시큐어코딩**
Zero Trust, ZTA, ZTNA, 제로트러스트, 마이크로세그멘테이션, microsegmentation, SDP, SASE, PEP/PDP, never trust always verify → **제로트러스트**

---

## CII 분기 시

### 실행 흐름
1. `reports/kese/`에서 이전 평가 결과 읽기 (있는 경우)
2. 이전 평가가 없으면 사용자에게 대상 플랫폼 확인
3. 해당 템플릿 파일을 `templates/cii/`에서 로드 (점검/수정 스크립트는 `scripts/cii/`에 있음)
4. 플랫폼별 하드닝 스크립트 생성
5. 스크립트를 `scripts/kese-hardening/`에 저장

### 출력 구조

```
scripts/kese-hardening/
├── unix/           ← bash 스크립트
├── windows/        ← PowerShell 스크립트
├── web/            ← Apache/Nginx 설정
├── database/       ← SQL 스크립트
└── README.md
```

### 플랫폼별 reference 매핑

| 플랫폼 | reference | 스크립트 유형 |
|--------|-----------|-------------|
| Unix/Linux | `templates/cii/unix.md` | bash |
| Windows | `templates/cii/windows.md` | PowerShell |
| 웹 서비스 | `templates/cii/web-service.md` | conf 파일 |
| DBMS | `templates/cii/database.md` | SQL |
| 네트워크 장비 | `templates/cii/network.md` | CLI 명령어 |
| 보안 장비 | `templates/cii/security-equip.md` | 설정 가이드 |
| PC | `templates/cii/pc.md` | PowerShell/GPO |
| 클라우드 | `templates/cii/cloud.md` | CLI 명령어 |

### 수정 적용 시 주의사항
- 수정 전 항상 설정 백업
- 비운영 환경에서 먼저 테스트
- 일부 수정은 서비스 재시작 필요
- 컴플라이언스 감사를 위해 모든 변경사항 문서화

---

## AI 보안 분기 시

### 실행 흐름
1. `references/ai-security/overview.md`를 읽어 AI 보안 위협 유형 파악
2. 대상에 따라 적절한 reference 로드
3. 보안 강화 가이드 및 코드 패치 생성

### 대상별 조치

| 대상 | reference | 조치 내용 |
|------|-----------|----------|
| AI 개발자 | `templates/ai-security/developer.md` | 모델 보안, 데이터 보호, API 보안 코드 |
| 서비스 제공자 | `references/ai-security/service-provider.md` | 서비스 보안 설정, 접근통제 |
| AI 이용자 | `references/ai-security/user-guide.md` | 보안 수칙 적용 체크리스트 |

### AI 보안 주요 조치 항목
- Prompt Injection 방어 (입출력 필터링, 가드레일)
- 데이터 중독(Poisoning) 방어 (이상치 탐지, 데이터 검증)
- 모델 추출 방어 (쿼리 제한, 워터마킹)
- API 보안 (Rate Limiting, 인증, TLS)
- LLM 보안 (OWASP Top 10 for LLM 기반)

---

## 로봇 보안 분기 시

`templates/robot-security/`를 로드하여 로봇 시스템 보안 강화 가이드를 생성합니다.

### 로봇 보안 주요 조치 영역
- Secure SDLC / SSDF 적용
- 서드파티 컴포넌트 및 SBOM 기반 공급망 통제
- IEC 62443 기반 인증, 권한, 무결성, 데이터 보호 통제
- CRA/NIS2 관점의 취약점 대응 및 사이버 복원력
- Wi-Fi, Bluetooth, 5G 등 무선 인터페이스 보안 강화

---

## 시큐어코딩 분기 시

`references/secure-coding/pseudocode.md`에서 UNSAFE→SAFE 패턴 쌍을 로드합니다. `templates/secure-coding/javascript.md` 또는 `templates/secure-coding/python.md`로 프레임워크별 수정을 적용합니다. 각 항목은 정확한 코드 변환(UNSAFE → SAFE)을 제공합니다.

---

## 제로트러스트 분기 시

`references/zero-trust/`에서 성숙도 모델과 아키텍처를, `templates/zero-trust/`에서 핵심요소별 체크리스트를 로드합니다. 현재 성숙도와 목표 성숙도 간 갭 분석을 기반으로 조치 가이드를 생성합니다. OT/ICS 환경이 감지되면 `templates/zero-trust/ot-environment.md`와 `references/zero-trust/ot-guide.md`도 로드합니다.

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

## 참고사항
- 발견된 각 취약점에 대해 구체적인 수정 명령어/코드를 제시하세요
- 긴급 심각도 항목을 우선적으로 수정하세요
- 수정 후 재점검을 권고하세요
