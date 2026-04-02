---
name: kesekit-start-ko
description: KISA 기반 보안 취약점 분석평가를 수행합니다. 주요정보통신기반시설(CII) 기술/관리/물리 취약점(560항목), AI 보안 안내서, 로봇 보안 체크리스트, 우주 보안(위성/GSaaS/공급망 53항목) 평가를 지원합니다. "보안 점검", "취약점 분석", "기반시설 감사", "KISA 점검", "보안 평가", "AI 보안 점검", "로봇 보안 평가", "우주 보안 평가", "위성 보안" 시 사용하세요.
---

# KESE 보안 취약점 분석평가

KISA 가이드라인에 따른 보안 취약점 분석평가를 수행합니다. 사용자의 환경과 목적에 맞는 가이드라인을 자동으로 선택하여 평가를 진행합니다.

## 가이드라인 선택

사용자에게 어떤 분야의 보안 점검을 원하는지 확인합니다. 명확하지 않으면 아래 목록을 보여주고 선택하게 합니다.

### 사용 가능한 가이드라인

| # | 가이드라인 | 설명 | 항목 수 |
|---|----------|------|:------:|
| 1 | **주요정보통신기반시설(CII)** | 기술적(424)+관리적(127)+물리적(18) 취약점 | ~560 |
| 2 | **AI 보안** | AI 개발자/서비스제공자/이용자 보안 요구사항 | ~54 |
| 3 | **로봇 보안** | 산업용/서비스용/의료용 로봇 보안 체크리스트 (11개 카테고리) | ~103 |

### 자동 판별 기준

- 서버, 네트워크, 데이터베이스, 웹 서비스, 방화벽 등 → **CII**
- AI 모델, LLM, 생성형 AI, 머신러닝, 프롬프트 등 → **AI 보안**
- 로봇, 산업용 로봇, 서비스 로봇, 의료용 로봇, ROS, PLC 등 → **로봇 보안**
- 클라우드, 가상화 → 맥락에 따라 CII 또는 AI 보안

---

## CII 분기 시

`templates/cii/` 디렉터리에서 대상 시스템에 해당하는 평가 템플릿 파일을 읽어 평가를 수행합니다. 점검/수정 스크립트는 `scripts/cii/`에 있습니다.

### 1단계: 환경 탐지

자동 탐지 또는 사용자 질문으로 대상 시스템을 파악합니다:

| 시스템 | reference 파일 | 항목 수 |
|--------|---------------|:------:|
| Unix/Linux 서버 | `templates/cii/unix.md` | 67 |
| Windows 서버 | `templates/cii/windows.md` | 64 |
| 웹 서비스 | `templates/cii/web-service.md` | 26 |
| 보안 장비 | `templates/cii/security-equip.md` | 23 |
| 네트워크 장비 | `templates/cii/network.md` | 38 |
| 제어시스템 | `templates/cii/control-system.md` | 46 |
| PC | `templates/cii/pc.md` | 18 |
| DBMS | `templates/cii/database.md` | 26 |
| 이동통신 | `templates/cii/mobile.md` | 4 |
| Web Application | `templates/cii/webapp.md` | 21 |
| 가상화 장비 | `templates/cii/virtualization.md` | 25 |
| 클라우드 | `templates/cii/cloud.md` | 19 |
| 관리적 취약점 | `templates/cii/admin.md` | 127 |
| 물리적 취약점 | `templates/cii/physical.md` | 18 |

### 2단계: 취약점 분석

해당 reference 파일을 Read로 로드한 후, 각 항목에 대해 점검합니다.

### 3단계: 보고서 생성

```
reports/kese/
├── summary.md          ← 전체 평가 요약
├── technical/          ← 시스템별 기술적 취약점 결과
├── administrative/     ← 관리적 취약점 결과
└── physical/           ← 물리적 취약점 결과
```

### 판단 기준

| 판단 | 설명 |
|------|------|
| 양호 | 보안 설정이 적절히 적용됨 |
| 부분이행 | 일부 구현되었으나 개선 필요 |
| 취약 | 보안 취약점 존재 |
| 해당없음 | 해당 환경에 적용 불가 |

---

## AI 보안 분기 시

`references/ai-security/` 디렉터리에서 대상에 해당하는 reference를 읽어 평가를 수행합니다.

### 1단계: 대상 확인

| 대상 | reference 파일 |
|------|---------------|
| 전체 개요 | `references/ai-security/overview.md` |
| AI 개발자 | `templates/ai-security/developer.md` |
| AI 서비스 제공자 | `references/ai-security/service-provider.md` |
| AI 이용자 | `references/ai-security/user-guide.md` |

### 2단계: 생명주기별 평가

AI 보안은 6단계 생명주기에 따라 점검합니다:
1. 계획 및 설계
2. 데이터 수집 및 준비
3. 모델 개발
4. 모델 배포
5. 모니터링 및 유지보수
6. 파기

### 3단계: 보고서 생성

```
reports/ai-security/
├── summary.md          ← 전체 평가 요약
├── developer.md        ← 개발자 보안 검증 결과
├── service-provider.md ← 서비스 제공자 검증 결과
└── user-checklist.md   ← 이용자 체크리스트 결과
```

---

## 로봇 보안 분기 시

`templates/robot-security/` 디렉터리에서 해당 템플릿을 읽어 평가를 수행합니다.

### 1단계: 대상 확인

| 대상 | reference 파일 |
|------|---------------|
| 전체 개요 | `templates/robot-security/overview.md` |
| SSDF (보안 SW 개발) | `templates/robot-security/ssdf.md` |
| 공급망 보안 | `templates/robot-security/supply-chain.md` |
| IEC 62443 기반 (IA, UC, SI, DP, DFR, ER, RA) | `templates/robot-security/iec62443.md` |
| 사이버 복원력 | `templates/robot-security/cyber-resilience.md` |
| 무선 보안 | `templates/robot-security/wireless.md` |

### 2단계: 카테고리별 평가

11개 카테고리, 총 ~103개 체크리스트 항목을 점검합니다.

### 3단계: 보고서 생성

```
reports/robot-security/
├── summary.md          ← 전체 평가 요약
├── ssdf.md             ← SSDF 19항목 결과
├── supply-chain.md     ← 공급망 7항목 결과
├── iec62443.md         ← IEC 62443 50항목 결과
├── cyber-resilience.md ← 사이버 복원력 13항목 결과
└── wireless.md         ← 무선 보안 14항목 결과
```

---

## 우선순위

### 긴급 (즉시 조치)
- 계정 관리 취약점, 미패치 취약점, 인젝션, 민감 데이터 미암호화

### 높음 (일정 내 조치)
- 설정 취약점, 보안 헤더 누락, 불완전한 로깅

### 보통 (개선 권고)
- 하드닝 권고, 문서화 부족

## 참고사항
- 평가 중 파일을 수정하지 마세요 — 읽기 전용입니다
- 해당 기술이 환경에 없는 경우 해당없음으로 표시하세요
- 발견된 각 취약점에 대해 구체적인 조치 방안을 제시하세요
