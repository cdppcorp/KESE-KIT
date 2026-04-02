# Zero Trust Architecture Reference

> Reference: NIST SP 800-207, KISA 제로트러스트 가이드라인 2.0, CISA Zero Trust Maturity Model
> Purpose: Provide architectural context for Zero Trust maturity assessment

## Zero Trust Architecture (ZTA)

### Core Logical Components

```
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │   PDP    │  │  Policy  │  │   Trust Algorithm    │  │
│  │ (Policy  │  │  Engine  │  │   (Risk Score +      │  │
│  │ Decision │  │          │  │    Context Analysis)  │  │
│  │  Point)  │  │          │  │                       │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │   PEP   │  ← Policy Enforcement Point
                    │         │
                    └────┬────┘
                         │
┌─────────────────────────────────────────────────────────┐
│                    Data Plane                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ Subject  │  │ Resource │  │   Enterprise          │  │
│  │ (User/   │→→│ (App/    │  │   Resources           │  │
│  │  Device) │  │  Data)   │  │                       │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Deployment Models (NIST SP 800-207)

1. **SDP (Software Defined Perimeter)**: Agent/gateway-based model
2. **Micro-segmentation**: Network-centric approach
3. **Network Infrastructure + SDP**: Hybrid approach

### KISA Zero Trust Guidelines 2.0 — 8 Elements

| Element | Korean | Scope |
|---------|--------|-------|
| Identity | 식별자 및 신원 | User identity management, MFA, continuous authentication |
| Device | 디바이스 및 엔드포인트 | Device inventory, health checks, compliance |
| Network | 네트워크 | Macro/micro segmentation, SDN, encrypted traffic |
| System | 시스템 | System hardening, patching, configuration management |
| Application | 애플리케이션 및 워크로드 | Resource authorization, remote access, monitoring |
| Data | 데이터 | Classification, DLP, encryption, access control |
| Visibility | 가시성 및 분석 | Logging, SIEM, threat analysis |
| Automation | 자동화 및 오케스트레이션 | SOAR, automated response, policy orchestration |

### Related Standards

| Standard | Organization | Focus |
|----------|-------------|-------|
| NIST SP 800-207 | NIST | ZTA reference architecture |
| CISA Zero Trust Maturity Model | CISA | Federal ZT maturity assessment |
| 제로트러스트 가이드라인 2.0 | KISA | Korean ZT implementation guide |
| NIST SP 800-82 | NIST | OT/ICS security guide |
| IEC 62443 | IEC | Industrial automation security |

### Key Concepts

- **PDP (Policy Decision Point)**: Evaluates access requests against policy
- **PEP (Policy Enforcement Point)**: Enforces PDP decisions at the access point
- **SDP (Software Defined Perimeter)**: Creates dynamic, identity-based perimeters
- **SASE (Secure Access Service Edge)**: Cloud-delivered convergence of network and security
- **ZTNA (Zero Trust Network Access)**: Application-level access without VPN
- **Microsegmentation**: Granular network isolation at workload level
