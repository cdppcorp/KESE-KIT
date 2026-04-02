# Zero Trust Overview

> Zero Trust Maturity Assessment — Overview & Assessment Guide
> Source: 제로트러스트 가이드라인 2.0 (KISA, 2024.12), NIST SP 800-207, CISA ZT Maturity Model

## Zero Trust Principles

- **Never Trust, Always Verify**: Every access request must be authenticated and authorized regardless of network location
- **Assume Breach**: Minimize blast radius through microsegmentation and least-privilege access
- **Verify Explicitly**: Use all available data points (identity, location, device health, service/workload, data classification, anomalies)

## 8 Core Elements

| # | Element | Code | Items |
|---|---------|------|:-----:|
| 1 | Identity (식별자 및 신원) | ID | 53 |
| 2 | Device (디바이스 및 엔드포인트) | DV | ~50 |
| 3 | Network (네트워크) | NW | 54 |
| 4 | System (시스템) | SY | ~45 |
| 5 | Application (애플리케이션 및 워크로드) | AP | 60 |
| 6 | Data (데이터) | DA | ~50 |
| 7 | Visibility (가시성 및 분석) | VA | 43 |
| 8 | Automation (자동화 및 오케스트레이션) | AU | ~41 |

**Total: ~396 items across 4 maturity levels**

## 4 Maturity Levels

| Level | Description | Target |
|-------|-------------|--------|
| **Traditional** | Perimeter-based security, manual processes | Baseline awareness |
| **Initial** | Some ZT controls adopted, partial automation | Early adopters |
| **Advanced** | Centralized management, context-aware policies, AI-assisted | Mature organizations |
| **Optimal** | Fully automated, real-time adaptive, AI-driven orchestration | Industry leaders |

## Assessment Flow

1. Determine target maturity level based on organizational goals
2. Select relevant core elements based on system context
3. Assess each item at or below the target maturity level
4. Items above target maturity level are informational (not scored)
5. Generate gap analysis comparing current state vs. target

## Template Files

| Topic | File |
|-------|------|
| Identity & Device | `templates/zero-trust/identity-device.md` |
| Network & System | `templates/zero-trust/network-system.md` |
| Application & Data | `templates/zero-trust/app-data.md` |
| Visibility & Automation | `templates/zero-trust/visibility-automation.md` |
| OT/ICS Environment | `templates/zero-trust/ot-environment.md` |

## Reference Files

| Topic | File |
|-------|------|
| ZT Architecture Reference | `references/zero-trust/overview.md` |
| Maturity Model Details | `references/zero-trust/maturity-model.md` |
| OT Deployment Guide | `references/zero-trust/ot-guide.md` |

## Judgment Criteria

| Judgment | Description |
|----------|-------------|
| Pass (양호) | ZT control properly implemented at target maturity level |
| Partial (부분이행) | Control partially implemented, improvement needed |
| Fail (취약) | Control not implemented or significantly below target |
| N/A (해당없음) | Not applicable to the environment |
