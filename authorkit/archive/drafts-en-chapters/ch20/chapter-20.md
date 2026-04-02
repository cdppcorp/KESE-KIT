# Chapter 20. Government Project Environment Application

> Part IV. Practical Application

---

## Overview

Government and public sector projects have different security requirements from private sector projects. This chapter covers public organization security requirements, information security budget guidelines, and pre-certified product utilization methods.

```
┌─────────────────────────────────────────────────────────────────┐
│              Government Project Security Requirements            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │  Legal Basis    │                          │
│                    │(Info Comm Infra │                          │
│                    │ Protection Act, │                          │
│                    │ e-Government Act)│                         │
│                    └────────┬────────┘                          │
│                             │                                    │
│            ┌────────────────┼────────────────┐                  │
│            │                │                │                  │
│            ▼                ▼                ▼                  │
│     ┌───────────┐    ┌───────────┐    ┌───────────┐            │
│     │ Security  │    │ Certified │    │ Security  │            │
│     │  Budget   │    │ Products  │    │  Review   │            │
│     │ (5~10%)   │    │(CC Cert.) │    │(e-Gov Act │            │
│     └─────┬─────┘    └─────┬─────┘    │ Art.56)   │            │
│           │                │           └─────┬─────┘            │
│           └────────────────┼─────────────────┘                  │
│                            │                                     │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Public SI Project Security Lifecycle             │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐      │  │
│  │  │ Plan │─▶│Analyze│─▶│Design│─▶│Develop│─▶│ Test │─▶Deploy│  │
│  │  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘      │  │
│  │     │         │         │         │         │           │  │
│  │  Security   Risk     Security  Secure   Vuln.          │  │
│  │  Require-  Analysis  Architec- Coding   Assessment/    │  │
│  │  ments      PIA      ture              Pentest         │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 20-1. Public Organization Security Requirements

### Key Legal Basis

| Law/Guideline | Key Content |
|---------------|-------------|
| Act on Protection of Information and Communications Infrastructure | Critical infrastructure protection |
| e-Government Act | Electronic government security |
| National Information Security Basic Guidelines | Public organization security standards |
| Personal Information Protection Act | Personal information protection |
| Cloud Computing Act | Public cloud security |

### Security Requirements by Organization Type

| Classification | Organization Examples | Security Level |
|----------------|----------------------|:--------------:|
| National agencies | Central administrative agencies | Highest |
| Local governments | Provincial/city offices | High |
| Public organizations | Public corporations | High |
| Educational institutions | Universities, education offices | Medium-High |

### Public SI Project Security Checklist

| Phase | Security Activities |
|-------|---------------------|
| Planning | Security requirements definition, budget allocation |
| Analysis | Security risk analysis, privacy impact assessment |
| Design | Security architecture, access control design |
| Development | Secure coding, security configuration |
| Testing | Security testing, vulnerability assessment |
| Deployment | Security review, handover |

---

## 20-2. Information Security Budget Guidelines

### Information Security Budget Guidelines

Information security budget ratio within public organization IT project budgets:

| Category | Recommended Ratio | Notes |
|----------|:-----------------:|-------|
| General IT projects | 5% or more | Baseline |
| Personal information systems | 7% or more | Recommended |
| Critical information infrastructure | 10% or more | Required |

### Information Security Budget Items

| Category | Detail Items |
|----------|--------------|
| Personnel | Security staff costs, training |
| Systems | Security equipment, licenses |
| Services | Security monitoring, vulnerability assessment |
| Consulting | ISMS certification, security consulting |

### Budget Calculation Example

```
[IT Project Budget: 1 Billion KRW]

Information Security Budget (10%): 100 Million KRW
├── Security Systems: 50M KRW
│   ├── Firewall: 20M KRW
│   ├── WAF: 15M KRW
│   └── Access Control: 15M KRW
├── Security Services: 30M KRW
│   ├── Vulnerability Assessment: 10M KRW
│   ├── Penetration Testing: 10M KRW
│   └── Security Training: 10M KRW
└── Security Consulting: 20M KRW
    └── ISMS Certification Consulting: 20M KRW
```

---

## 20-3. Pre-Certified Product Utilization

### CC Certification (Common Criteria)

Information security product certification based on international Common Criteria

| Level | Description | Application |
|:-----:|-------------|-------------|
| EAL1 | Functional testing | - |
| EAL2 | Structural testing | General |
| EAL3 | Methodical testing | General |
| EAL4 | Methodical design/test | Public |
| EAL5 | Semi-formal design/test | Defense |
| EAL6~7 | Formal design | Defense/Classified |

### Public Organization Product Deployment Standards

| Product Type | Required Certification |
|--------------|----------------------|
| Firewall | CC Certification |
| IDS (Intrusion Detection System) | CC Certification |
| IPS (Intrusion Prevention System) | CC Certification |
| VPN | CC Certification |
| ESM (Enterprise Security Management) | CC Certification |
| Database Access Control | CC Certification |
| PC Security | CC Certification |

### CC Certified Product Verification

1. **IT Security Certification Office** (www.itscc.kr)
   - Certified product list lookup
   - Certificate validity verification

2. **Verification Items**
   - Certificate validity period
   - Certification scope
   - Evaluation assurance level

### Security Conformance Validation

Validation for national cryptographic products

| Category | Details |
|----------|---------|
| Validation Agency | National Security Research Institute |
| Target Products | Cryptographic modules, network encryption devices, etc. |
| Verification Method | Security conformance validated product list lookup |

---

## Public Project Security Requirements Example

### RFP Security Section

```markdown
## Security Requirements

### 1. General Requirements
- Compliance with information security regulations
- Deployment of CC-certified products for public use
- Minimum 10% information security budget allocation

### 2. Technical Requirements

#### 2.1 Network Security
- Internal/external network segregation
- Firewall deployment (CC-certified)
- IDS deployment (CC-certified)

#### 2.2 System Security
- Server access control solution deployment
- System vulnerability assessment
- Security patch management system

#### 2.3 Data Security
- Encryption of sensitive data
- DB access control solution (CC-certified)
- Personal information masking

#### 2.4 Application Security
- Secure coding implementation
- Source code security vulnerability assessment
- Web application firewall deployment

### 3. Administrative Requirements
- Security policy/guideline establishment
- Security training implementation
- Incident response plan establishment

### 4. Verification and Acceptance Requirements
- Vulnerability analysis and assessment
- Penetration testing
- Security review approval
```

---

## Public Project Security Assessment Schedule Example

| Phase | Activity | Timing | Deliverables |
|-------|----------|--------|--------------|
| Analysis | Security requirements analysis | Analysis phase | Security requirements specification |
| Design | Security architecture design | Design phase | Security design document |
| Development | Secure coding | During development | Source code review results |
| Testing | Vulnerability assessment | Testing phase | Vulnerability assessment report |
| Testing | Penetration testing | Testing phase | Penetration testing report |
| Deployment | Security review | Pre-deployment | Security review results |

---

## Tips for Vibe Coders

### Essential Checks for Government Projects

1. **Secure Budget Allocation**
   - Request security budget specification at RFP stage
   - Secure minimum 5~10%

2. **Early CC Certification Review**
   - Confirm product list during design phase
   - Verify certification validity period

3. **Secure Coding**
   - Follow Ministry of Interior secure coding guide
   - Use source code review tools

4. **Vulnerability Assessment Schedule**
   - Allocate sufficient assessment time after development
   - Consider remediation period

> **TIP**
> Even with vibe coding for rapid development, allocate sufficient time for security assessments. When using AI code generation, include OWASP Top 10 and CWE Top 25 considerations in prompts to reduce security vulnerabilities.

---

## Summary

| Item | Key Content |
|------|-------------|
| Legal Requirements | Act on Protection of Information Infrastructure, e-Government Act |
| Budget Standards | 5~10% of IT budget |
| Product Certification | CC certification required (public organizations) |
| Development Security | Secure coding + vulnerability assessment |

---

*Next Chapter: Chapter 21. Public Procurement Market Response*
