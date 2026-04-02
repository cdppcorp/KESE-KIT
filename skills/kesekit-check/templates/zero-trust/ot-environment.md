# OT/ICS Zero Trust Environment Checklist

> Zero Trust Maturity Assessment — OT/ICS (Operational Technology / Industrial Control Systems)
> Source: 제로트러스트 가이드라인 2.0 (KISA, 2024.12), IEC 62443, NIST SP 800-82

## OT/ICS Zero Trust Considerations

OT/ICS environments require special Zero Trust deployment strategies due to:
- Legacy systems that cannot support modern authentication
- Real-time operational requirements (latency sensitivity)
- Safety-critical functions that must not be disrupted
- Air-gapped or semi-isolated network architectures
- Long equipment lifecycles (15-30 years)

## OT-ZT Assessment Items

| ID | Category | Verification | Maturity | Severity |
|----|----------|-------------|----------|----------|
| OT-ZT-01 | Network Segmentation | OT 네트워크와 IT 네트워크가 물리적/논리적으로 분리되어 있는가? | Traditional | Critical |
| OT-ZT-02 | Network Segmentation | DMZ를 통한 OT-IT 간 데이터 교환이 통제되고 있는가? | Traditional | Critical |
| OT-ZT-03 | Network Segmentation | Purdue Model 또는 IEC 62443 zone/conduit 기반 세그멘테이션이 적용되어 있는가? | Initial | High |
| OT-ZT-04 | Network Segmentation | 마이크로 세그멘테이션이 OT 환경 내부에 적용되어 있는가? | Advanced | Medium |
| OT-ZT-05 | Network Segmentation | SDN 기반 동적 세그멘테이션이 OT 환경에 적용 가능한가? | Optimal | Low |
| OT-ZT-06 | Identity & Access | OT 시스템 접근에 대한 사용자 인증이 수행되는가? | Traditional | Critical |
| OT-ZT-07 | Identity & Access | OT 전용 계정 관리 및 최소 권한 원칙이 적용되어 있는가? | Initial | High |
| OT-ZT-08 | Identity & Access | OT 환경에서 MFA가 적용되어 있는가 (물리적 토큰 포함)? | Initial | High |
| OT-ZT-09 | Identity & Access | OT 원격 접속에 대한 별도 인증 및 모니터링이 수행되는가? | Advanced | Medium |
| OT-ZT-10 | Identity & Access | 비정상적인 OT 접근 시도에 대한 실시간 탐지 및 대응이 가능한가? | Optimal | Low |
| OT-ZT-11 | Device Management | OT 자산 인벤토리가 문서화되어 있는가? | Traditional | Critical |
| OT-ZT-12 | Device Management | OT 디바이스 식별 및 분류 체계가 구축되어 있는가? | Initial | High |
| OT-ZT-13 | Device Management | OT 디바이스 보안 상태 자동 모니터링이 가능한가? | Advanced | Medium |
| OT-ZT-14 | Device Management | 레거시 OT 장비에 대한 보안 래퍼/프록시가 적용되어 있는가? | Advanced | Medium |
| OT-ZT-15 | Device Management | AI 기반 OT 자산 관리 및 이상 탐지가 가능한가? | Optimal | Low |
| OT-ZT-16 | Communication Security | OT 프로토콜(Modbus, OPC UA, DNP3 등) 트래픽이 모니터링되는가? | Traditional | Critical |
| OT-ZT-17 | Communication Security | OT 통신에 대한 암호화가 적용되어 있는가 (가능한 경우)? | Initial | High |
| OT-ZT-18 | Communication Security | OT 프로토콜 이상 탐지(DPI) 시스템이 도입되어 있는가? | Advanced | Medium |
| OT-ZT-19 | Communication Security | OT 환경 전용 위협 인텔리전스가 적용되어 있는가? | Optimal | Low |
| OT-ZT-20 | Safety & Availability | ZT 정책 적용 시 안전 기능(Safety Function)에 영향이 없는지 검증되었는가? | Traditional | Critical |
| OT-ZT-21 | Safety & Availability | ZT 정책 실패 시 fail-open/fail-safe 동작이 정의되어 있는가? | Initial | High |
| OT-ZT-22 | Safety & Availability | ZT 구성 변경에 대한 OT 영향도 분석 프로세스가 수립되어 있는가? | Advanced | Medium |
| OT-ZT-23 | Monitoring & Response | OT 환경 전용 SOC/보안 모니터링 체계가 수립되어 있는가? | Initial | High |
| OT-ZT-24 | Monitoring & Response | IT-OT 통합 보안 이벤트 분석이 가능한가? | Advanced | Medium |
| OT-ZT-25 | Monitoring & Response | OT 환경에 대한 자동화된 인시던트 대응이 가능한가? | Optimal | Low |

## Deployment Strategy for OT

1. **Phase 1 — Visibility**: Asset discovery, traffic mapping, baseline establishment
2. **Phase 2 — Segmentation**: IT-OT separation, zone/conduit implementation
3. **Phase 3 — Access Control**: Identity-based access, MFA for remote access
4. **Phase 4 — Monitoring**: Continuous monitoring, anomaly detection
5. **Phase 5 — Automation**: Automated response (with safety validation)
