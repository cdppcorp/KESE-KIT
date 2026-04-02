# Zero Trust Maturity Model

> Reference: KISA 제로트러스트 가이드라인 2.0 (2024.12), CISA Zero Trust Maturity Model v2.0
> Purpose: Detailed maturity level definitions and scoring guidance

## Maturity Level Definitions

### Traditional (전통적)
- Perimeter-based security model (castle-and-moat)
- Manual identity management and access control
- Static, rule-based security policies
- Limited visibility into internal traffic

### Initial (기본)
- Beginning adoption of ZT principles
- Some automated identity management (SSO, basic MFA)
- Initial network segmentation beyond perimeter
- Centralized logging introduced

### Advanced (고도화)
- Context-aware, dynamic access policies
- AI-assisted threat detection and response
- Comprehensive microsegmentation
- Real-time monitoring and analytics

### Optimal (최적화)
- Fully automated, self-adaptive security
- AI-driven orchestration and response
- Predictive threat analysis
- Continuous verification at all layers
- Zero standing privileges

## Scoring Framework

### Per-Item Scoring

| Score | Criteria |
|-------|----------|
| 3 | Fully implemented and operational |
| 2 | Partially implemented, gaps exist |
| 1 | Planned but not yet implemented |
| 0 | Not implemented, no plans |

### Element Maturity Calculation

```
Element Score = (Sum of item scores for target level) / (Max possible score) x 100%

Maturity Rating:
  >= 80%  → Mature (at or above target level)
  60-79%  → Developing (approaching target level)
  40-59%  → Emerging (significant gaps remain)
  < 40%   → Insufficient (major remediation needed)
```

## Cross-Element Dependencies

| Element | Depends On |
|---------|-----------|
| Identity | — (foundation element) |
| Device | Identity |
| Network | Identity, Device |
| System | Network, Identity |
| Application | Identity, Device, Network |
| Data | Application, Identity |
| Visibility | All elements (observability layer) |
| Automation | Visibility (requires data to automate) |

## Assessment Prioritization

1. Start with **Identity** — foundation of all ZT controls
2. Then **Device** — ensure endpoint trust
3. Then **Network** — establish segmentation
4. Then **Application** and **Data** — protect workloads
5. Finally **Visibility** and **Automation** — enable continuous improvement
