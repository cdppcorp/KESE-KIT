---
name: kesekit-fix-ko
description: 보안 취약점 자동 수정 및 하드닝 스크립트를 생성합니다. CII(Unix/Windows/웹서버/DB), AI, 로봇, 우주 시스템(위성/GSaaS/지상국/공급망)의 취약점을 수정합니다. KISA/CMMC/NIS2 가이드라인에 따른 보안 설정을 적용합니다. "취약점 수정", "서버 하드닝", "우주 보안 수정", "위성 하드닝" 시 사용하세요.
---

# KESE 취약점 자동 수정

취약점 분석 결과를 기반으로 적절한 수정을 생성하고 적용합니다. 사용자의 환경에 맞는 가이드라인을 자동 선택합니다.

## 가이드라인 선택

| # | 가이드라인 | 설명 |
|---|----------|------|
| 1 | **CII 하드닝** | 플랫폼별 하드닝 스크립트 생성 |
| 2 | **AI 보안 조치** | AI 시스템 보안 강화 가이드 |
| 3 | **로봇 보안 조치** | 로봇 시스템 보안 강화 (IEC 62443, CRA, RED) |

서버, 인프라, 웹 서비스, DB → **CII** / AI 모델, LLM, AI 서비스 → **AI 보안** / 로봇, ROS/ROS2, 로봇 펌웨어, 무선 제어 인터페이스 → **로봇 보안**

---

## CII 분기 시

### 실행 흐름
1. `reports/kese/`에서 이전 평가 결과 읽기 (있는 경우)
2. 이전 평가가 없으면 사용자에게 대상 플랫폼 확인
3. 해당 reference 파일을 `references/cii/`에서 로드
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
| Unix/Linux | `references/cii/unix.md` | bash |
| Windows | `references/cii/windows.md` | PowerShell |
| 웹 서비스 | `references/cii/web-service.md` | conf 파일 |
| DBMS | `references/cii/database.md` | SQL |
| 네트워크 장비 | `references/cii/network.md` | CLI 명령어 |
| 보안 장비 | `references/cii/security-equip.md` | 설정 가이드 |
| PC | `references/cii/pc.md` | PowerShell/GPO |
| 클라우드 | `references/cii/cloud.md` | CLI 명령어 |

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
| AI 개발자 | `references/ai-security/developer.md` | 모델 보안, 데이터 보호, API 보안 코드 |
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

`references/robot-security/`를 로드하여 로봇 시스템 보안 강화 가이드를 생성합니다.

### 로봇 보안 주요 조치 영역
- Secure SDLC / SSDF 적용
- 서드파티 컴포넌트 및 SBOM 기반 공급망 통제
- IEC 62443 기반 인증, 권한, 무결성, 데이터 보호 통제
- CRA/NIS2 관점의 취약점 대응 및 사이버 복원력
- Wi-Fi, Bluetooth, 5G 등 무선 인터페이스 보안 강화

---

## 참고사항
- 발견된 각 취약점에 대해 구체적인 수정 명령어/코드를 제시하세요
- 긴급 심각도 항목을 우선적으로 수정하세요
- 수정 후 재점검을 권고하세요
