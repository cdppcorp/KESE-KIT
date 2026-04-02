# Identity & Device Checklist

> Zero Trust Maturity Assessment — Identity (ID) & Device (DV)
> Source: 제로트러스트 가이드라인 2.0 (KISA, 2024.12)

## ID — 식별자 및 신원 (Identity) (53 Items)

| ID | Sub-capability | Verification | Maturity | Severity |
|----|---------------|-------------|----------|----------|
| ZT-ID-01 | 사용자 인벤토리 | 사용자 목록에 대한 문서화가 되어있는가? | Traditional | Critical |
| ZT-ID-02 | 사용자 인벤토리 | 사용자 역할에 따른 상세 인벤토리가 구축되어 있는가? | Initial | High |
| ZT-ID-03 | 사용자 인벤토리 | 자동화된 인벤토리 관리 기구가 도입되어 있는가? | Advanced | Medium |
| ZT-ID-04 | 사용자 인벤토리 | 비정상적인 사용자 활동에 대한 탐지가 가능한가? | Advanced | Medium |
| ZT-ID-05 | 사용자 인벤토리 | AI 기반 사용자 행동에 따른 관리가 되는가? | Optimal | Low |
| ZT-ID-06 | 사용자 인벤토리 | 인벤토리가 통합되어 사용자 및 권한 관리 최적화가 되어 있는가? | Optimal | Low |
| ZT-ID-07 | ID 연계 및 사용자 자격 증명 | 사용자 자격 증명에 대한 ID 연계 솔루션이 적용되어 있는가? | Traditional | Critical |
| ZT-ID-08 | ID 연계 및 사용자 자격 증명 | 여러 시스템 간 사용자 자격 증명에 대한 연동이 되어 있는가? | Initial | High |
| ZT-ID-09 | ID 연계 및 사용자 자격 증명 | ID 통합 관리 시스템이 구축되어 있는가? | Advanced | Medium |
| ZT-ID-10 | ID 연계 및 사용자 자격 증명 | 글로벌 수준의 ID 연계 솔루션이 적용되어 있는가? | Optimal | Low |
| ZT-ID-11 | 다중인증 (MFA) | 패스워드와 단순한 MFA(SMS, 이메일)가 같이 적용되어 있는가? | Traditional | Critical |
| ZT-ID-12 | 다중인증 (MFA) | 인증 앱, 하드웨어 토큰 등 다양한 MFA가 구현되어 있는가? | Initial | High |
| ZT-ID-13 | 다중인증 (MFA) | FIDO 기반 인증 기법이 적용되어 있는가? | Initial | High |
| ZT-ID-14 | 다중인증 (MFA) | 상황에 따른 맞춤형 MFA가 지원 가능한가? | Advanced | Medium |
| ZT-ID-15 | 다중인증 (MFA) | 컨텍스트(단말 위치, 네트워크, 접속 시간 등)를 고려한 ID 인증 방식이 적용되어 있는가? | Advanced | Medium |
| ZT-ID-16 | 다중인증 (MFA) | 비정상적 로그인 시도를 실시간으로 탐지하고 대응 가능한가? | Optimal | Low |
| ZT-ID-17 | 지속 인증 | 세션 기반 인증이 수행되는가? | Traditional | Critical |
| ZT-ID-18 | 지속 인증 | 사용자의 행동 및 접속 상태 모니터링이 가능한가? | Traditional | Critical |
| ZT-ID-19 | 지속 인증 | 이상행위가 탐지되면 세션 중간에 추가 인증하는 시스템이 도입되어 있는가? | Initial | High |
| ZT-ID-20 | 지속 인증 | 동적 인증 기술을 토대로 실시간으로 인증 상태에 대한 조정이 가능한가? | Advanced | Medium |
| ZT-ID-21 | 지속 인증 | 이상 행위 발생 시 자동 재인증 요구, 세션 종료 등 인증에 대한 지속적 검증이 실시간으로 가능한가? | Optimal | Low |
| ZT-ID-22 | 통합 ICAM 플랫폼 | ICAM 시스템이 구축되어 있는가? | Traditional | Critical |
| ZT-ID-23 | 통합 ICAM 플랫폼 | ICAM 시스템 기반 중앙 집중 관리 및 모니터링이 되는가? | Initial | High |
| ZT-ID-24 | 통합 ICAM 플랫폼 | 사용자 인증 및 접근 관리에 대한 정책이 표준화되어 있는가? | Initial | High |
| ZT-ID-25 | 통합 ICAM 플랫폼 | 사용자 및 권한 관리에 대한 기본적인 위험도 평가가 도입 되었는가? | Initial | High |
| ZT-ID-26 | 통합 ICAM 플랫폼 | 다양한 보안 기술 및 시스템 통합으로 ICAM 플랫폼이 안정화되었는가? | Advanced | Medium |
| ZT-ID-27 | 통합 ICAM 플랫폼 | ICAM 플랫폼이 자동화되어 있는가? | Advanced | Medium |
| ZT-ID-28 | 통합 ICAM 플랫폼 | AI 기반의 ICAM 플랫폼을 통해 보안 강화가 이루어지는가? | Optimal | Low |
| ZT-ID-29 | 통합 ICAM 플랫폼 | 실시간 분석을 통한 ID 위험 평가가 이루어지는가? | Optimal | Low |
| ZT-ID-30 | 행동, 컨텍스트 기반 ID 및 생체 인식 | 기본적인(지문, 얼굴인식) 생체 인식 기술이 적용되어 있는가? | Traditional | Critical |
| ZT-ID-31 | 행동, 컨텍스트 기반 ID 및 생체 인식 | 사용자 행동 패턴이 수동으로 분석되는가? | Traditional | Critical |
| ZT-ID-32 | 행동, 컨텍스트 기반 ID 및 생체 인식 | 행동 및 생체 인식 기술을 통합하여 인증이 가능한가? | Initial | High |
| ZT-ID-33 | 행동, 컨텍스트 기반 ID 및 생체 인식 | 컨텍스트 정보 기반 접근권한이 조정되는가? | Initial | High |
| ZT-ID-34 | 행동, 컨텍스트 기반 ID 및 생체 인식 | 실시간 사용자 행동 및 컨텍스트 변화 반영으로 접근제어 조정이 가능한가? | Advanced | Medium |
| ZT-ID-35 | 행동, 컨텍스트 기반 ID 및 생체 인식 | AI 기반 행동 분석 및 생체 인식 솔루션이 도입되어 있는가? | Optimal | Low |
| ZT-ID-36 | 조건부 사용자 접근 | 사용자 활동 및 조건을 수집할 수 있는 기초 시스템을 구축하였는가? | Traditional | Critical |
| ZT-ID-37 | 조건부 사용자 접근 | 조건부 접근 정책에 대한 개념을 정의하였는가? | Traditional | Critical |
| ZT-ID-38 | 조건부 사용자 접근 | 시스템 별 각기 다른 접속 관리 기능이 있는가? | Traditional | Critical |
| ZT-ID-39 | 조건부 사용자 접근 | 특정 조건에 따른 사용자 접근제어가 가능한가? | Initial | High |
| ZT-ID-40 | 조건부 사용자 접근 | 시간, 위치 기반으로 최소 권한 원칙에 따른 접근제어가 가능한가? | Initial | High |
| ZT-ID-41 | 조건부 사용자 접근 | 세션별 접근권한 부여가 가능한가? | Advanced | Medium |
| ZT-ID-42 | 조건부 사용자 접근 | 조건을 정교하게 나누어 다단계 접근 정책이 적용되어 있는가? | Advanced | Medium |
| ZT-ID-43 | 조건부 사용자 접근 | 리소스별 접근권한 부여가 가능한가? | Advanced | Medium |
| ZT-ID-44 | 조건부 사용자 접근 | 동적 접근 정책을 실시간으로 적용 가능한가? | Optimal | Low |
| ZT-ID-45 | 조건부 사용자 접근 | AI 기반 실시간 상황 파악을 통한 사용자 접속 관리가 가능한가? | Optimal | Low |
| ZT-ID-46 | 최소 권한 접근 | 최소 권한 원칙에 대한 정의가 이루어져 있는가? | Traditional | Critical |
| ZT-ID-47 | 최소 권한 접근 | 권한 부여에 대한 절차가 문서화 되어 있는가? | Traditional | Critical |
| ZT-ID-48 | 최소 권한 접근 | 권한 부여 절차가 표준화 되어 있는가? | Initial | High |
| ZT-ID-49 | 최소 권한 접근 | 권한 요청 및 변경 관리 시스템이 도입되어 있는가? | Initial | High |
| ZT-ID-50 | 최소 권한 접근 | 자동화된 권한 상승이 가능한가? | Advanced | Medium |
| ZT-ID-51 | 최소 권한 접근 | 권한 관리 정책이 지속적으로 업데이트 되는가? | Advanced | Medium |
| ZT-ID-52 | 최소 권한 접근 | 권한 관리가 동적으로 변경 가능한가? | Optimal | Low |
| ZT-ID-53 | 최소 권한 접근 | 최소 권한 원칙이 실시간으로 조정 가능한가? | Optimal | Low |

### ID Sub-capability Protection Measures Summary

| Sub-capability | Traditional | Initial | Advanced | Optimal |
|---------------|------------|---------|----------|---------|
| 사용자 인벤토리 | 사용자 목록 문서화 | 역할별 상세 인벤토리 | 자동화 관리, 비정상 활동 탐지 | AI 기반 관리, 통합 최적화 |
| ID 연계 및 사용자 자격 증명 | ID 연계 솔루션 적용 | 시스템 간 연동 | 통합 관리 시스템 | 글로벌 수준 연계 |
| 다중인증 (MFA) | 패스워드+SMS/이메일 MFA | 인증 앱/토큰, FIDO | 맞춤형 MFA, 컨텍스트 인증 | 비정상 로그인 실시간 탐지 |
| 지속 인증 | 세션 기반 인증, 상태 모니터링 | 세션 중간 추가 인증 | 동적 인증 기술 | 자동 재인증, 실시간 검증 |
| 통합 ICAM 플랫폼 | ICAM 시스템 구축 | 중앙 관리, 정책 표준화, 위험도 평가 | 시스템 통합 안정화, 자동화 | AI 기반 보안 강화, 실시간 ID 위험 평가 |
| 행동/컨텍스트 기반 ID 및 생체 인식 | 기본 생체 인식, 수동 행동 분석 | 통합 인증, 컨텍스트 접근권한 | 실시간 접근제어 조정 | AI 기반 행동/생체 인식 |
| 조건부 사용자 접근 | 기초 시스템, 개념 정의, 접속 관리 | 조건부 접근제어, 최소 권한 | 세션/리소스별 권한, 다단계 정책 | 동적 정책, AI 실시간 관리 |
| 최소 권한 접근 | 원칙 정의, 절차 문서화 | 표준화, 변경 관리 시스템 | 자동 권한 상승, 정책 업데이트 | 동적 변경, 실시간 조정 |

---

## DV — 기기 및 엔드포인트 (Device) (40 Items)

| ID | Sub-capability | Verification | Maturity | Severity |
|----|---------------|-------------|----------|----------|
| ZT-DV-01 | 기기 감지 및 규정 준수 | 리소스에 연결된 기기를 식별할 수 있는가? | Traditional | Critical |
| ZT-DV-02 | 기기 감지 및 규정 준수 | 수동으로 규정 준수에 대한 확인이 가능한가? | Traditional | Critical |
| ZT-DV-03 | 기기 감지 및 규정 준수 | 실시간으로 기기를 탐지하고 규정 준수를 평가할 수 있는가? | Initial | High |
| ZT-DV-04 | 기기 감지 및 규정 준수 | 비준수 기기에 대한 경고 및 접근 제한이 되는가? | Initial | High |
| ZT-DV-05 | 기기 감지 및 규정 준수 | 자동으로 규정 기준을 적용하고 교정 조치가 가능한가? | Advanced | Medium |
| ZT-DV-06 | 기기 감지 및 규정 준수 | 규정 준수에 대한 모니터링 및 이에 따른 접근권한 부여가 가능한가? | Advanced | Medium |
| ZT-DV-07 | 기기 감지 및 규정 준수 | 규정 준수 여부에 따라 동적으로 권한이 수정되는가? | Optimal | Low |
| ZT-DV-08 | 기기 감지 및 규정 준수 | 규정 준수 평가를 AI 기반으로 실시간으로 할 수 있는가? | Optimal | Low |
| ZT-DV-09 | 실시간 검사를 통한 기기 권한 부여 | 자산 접근 기기에 대한 정보가 수집되는가? | Traditional | Critical |
| ZT-DV-10 | 실시간 검사를 통한 기기 권한 부여 | 기기가 자산에 접근하기 전 수동 검사를 수행하는가? | Initial | High |
| ZT-DV-11 | 실시간 검사를 통한 기기 권한 부여 | 기기의 상태를 자동으로 평가하고 보안 기준을 충족하는 기기만 접근 허용이 되는가? | Advanced | Medium |
| ZT-DV-12 | 실시간 검사를 통한 기기 권한 부여 | 보안 상태에 따라 기기의 접근권한을 조정할 수 있는가? | Optimal | Low |
| ZT-DV-13 | 실시간 검사를 통한 기기 권한 부여 | 종합적인 기기 보안 전략을 구현하여 다른 보안 시스템과 연동하였는가? | Optimal | Low |
| ZT-DV-14 | 기기 인벤토리 | 기기의 인벤토리를 작성하고 수동으로 업데이트 하는가? | Traditional | Critical |
| ZT-DV-15 | 기기 인벤토리 | 주요 기기에 대한 정보를 수집하고 관리하는가? | Traditional | Critical |
| ZT-DV-16 | 기기 인벤토리 | 기기 인벤토리를 자동화하고 모든 기기를 실시간으로 기록하는가? | Initial | High |
| ZT-DV-17 | 기기 인벤토리 | 기기 인벤토리에 비정상적이거나 승인되지 않은 기기를 탐지하는 기능을 포함하는가? | Advanced | Medium |
| ZT-DV-18 | 기기 인벤토리 | 인벤토리 분석을 통하여 보안 취약점을 파악하는가? | Advanced | Medium |
| ZT-DV-19 | 기기 인벤토리 | 실시간 모니터링 및 이상 행위 예측 분석을 통해 기기 관리를 수행하는가? | Optimal | Low |
| ZT-DV-20 | 통합 엔드포인트 관리 및 모바일 기기 관리 | 기본적인 엔드포인트 및 모바일 기기 관리 시스템이 도입되었는가? | Traditional | Critical |
| ZT-DV-21 | 통합 엔드포인트 관리 및 모바일 기기 관리 | 기본적인 보안 정책을 설정하였는가? | Traditional | Critical |
| ZT-DV-22 | 통합 엔드포인트 관리 및 모바일 기기 관리 | 엔드포인트 및 모바일 기기의 보안 설정을 중앙에서 관리하고 보안 업데이트를 자동 배포하는가? | Initial | High |
| ZT-DV-23 | 통합 엔드포인트 관리 및 모바일 기기 관리 | 기기 상태를 지속적으로 모니터링 하는가? | Initial | High |
| ZT-DV-24 | 통합 엔드포인트 관리 및 모바일 기기 관리 | 모든 엔드포인트와 모바일 기기에 대하여 보안 정책을 중앙에서 자동으로 적용하고 관리하는가? | Advanced | Medium |
| ZT-DV-25 | 통합 엔드포인트 관리 및 모바일 기기 관리 | 모든 기기의 보안을 중앙에서 통합적으로 관리하고, 자동화된 위협 대응이 가능한가? | Optimal | Low |
| ZT-DV-26 | 엔드포인트 및 확장된 탐지/대응 (EDR 및 XDR) | 기본적인 EDR 솔루션을 도입하였는가? | Traditional | Critical |
| ZT-DV-27 | 엔드포인트 및 확장된 탐지/대응 (EDR 및 XDR) | EDR 시스템을 고도화하여 실시간 위협 탐지 및 자동 대응이 가능한가? | Initial | High |
| ZT-DV-28 | 엔드포인트 및 확장된 탐지/대응 (EDR 및 XDR) | XDR 솔루션을 도입하였는가? | Advanced | Medium |
| ZT-DV-29 | 엔드포인트 및 확장된 탐지/대응 (EDR 및 XDR) | AI 기반 EDR/XDR 솔루션을 통해 실시간으로 모든 기기에 대한 위협 탐지가 가능한가? | Optimal | Low |
| ZT-DV-30 | 자산, 취약성 및 패치 관리 자동화 | 자산 및 취약성을 수동으로 평가하는가? | Traditional | Critical |
| ZT-DV-31 | 자산, 취약성 및 패치 관리 자동화 | 주요 자산 및 취약성 목록이 작성되어 있는가? | Traditional | Critical |
| ZT-DV-32 | 자산, 취약성 및 패치 관리 자동화 | 자동화된 취약성 평가 및 패치 관리 도구를 도입하여 취약성 발견 시 자동 패치가 이루어지는가? | Initial | High |
| ZT-DV-33 | 자산, 취약성 및 패치 관리 자동화 | 모든 자산에 대해 지속적인 취약성 평가 및 패치 관리가 자동화되어 있는가? | Advanced | Medium |
| ZT-DV-34 | 자산, 취약성 및 패치 관리 자동화 | 취약성 및 패치 관리 시스템을 다른 보안 시스템과 통합하여 종합적인 보안 관리가 가능한가? | Advanced | Medium |
| ZT-DV-35 | 자산, 취약성 및 패치 관리 자동화 | 취약점을 사전에 식별하고 자동으로 패치 적용이 가능한가? | Optimal | Low |
| ZT-DV-36 | 자산, 취약성 및 패치 관리 자동화 | 자산 관리, 취약성 평가, 패치 관리 시스템이 통합되어 있는가? | Optimal | Low |

### DV Sub-capability Protection Measures Summary

| Sub-capability | Traditional | Initial | Advanced | Optimal |
|---------------|------------|---------|----------|---------|
| 기기 감지 및 규정 준수 | 기기 식별, 수동 규정 확인 | 실시간 탐지, 비준수 경고 | 자동 교정, 접근권한 연동 | 동적 권한 수정, AI 실시간 평가 |
| 실시간 검사를 통한 기기 권한 부여 | 기기 정보 수집 | 수동 검사 수행 | 자동 평가 및 접근 허용 | 접근권한 조정, 보안 시스템 연동 |
| 기기 인벤토리 | 수동 인벤토리, 정보 수집 | 자동화 기록 | 비정상 기기 탐지, 취약점 파악 | 실시간 모니터링, 예측 분석 |
| 통합 엔드포인트/모바일 기기 관리 | 관리 시스템 도입, 보안 정책 설정 | 중앙 관리, 지속 모니터링 | 중앙 자동 적용 | 통합 관리, 자동 위협 대응 |
| EDR 및 XDR | 기본 EDR 도입 | 실시간 탐지/자동 대응 | XDR 도입 | AI 기반 통합 위협 탐지 |
| 자산/취약성/패치 관리 자동화 | 수동 평가, 목록 작성 | 자동 패치 도입 | 지속적 자동화, 시스템 통합 | 사전 식별, 통합 관리 |

---

## Total: 89 Items (ID: 53 + DV: 36)
