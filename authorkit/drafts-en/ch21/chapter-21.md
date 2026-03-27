# Chapter 21. Public Procurement Market Response

> Part IV. Practical Application

---

## Overview

To enter the public procurement market, security requirements must be met. This chapter covers procurement agency security requirements, proposal writing guide, and security review response methods.

```
┌─────────────────────────────────────────────────────────────────┐
│                Public Procurement Market Entry                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   Preparation Phase                        │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  ┌─────────┐    ┌─────────┐    ┌─────────┐              │  │
│  │  │ Certif- │    │ Track   │    │Personnel│              │  │
│  │  │ ication │    │ Record  │    │ Secure  │              │  │
│  │  │         │    │         │    │         │              │  │
│  │  │• ISMS   │    │• Public │    │• CISA   │              │  │
│  │  │• ISO    │    │  project│    │• CISSP  │              │  │
│  │  │  27001  │    │  exp.   │    │• OSCP   │              │  │
│  │  │• GS Cert│    │         │    │         │              │  │
│  │  │• CC Cert│    │         │    │         │              │  │
│  │  └────┬────┘    └────┬────┘    └────┬────┘              │  │
│  └───────┼──────────────┼──────────────┼────────────────────┘  │
│          └──────────────┼──────────────┘                        │
│                         ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Bidding Phase                           │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │  e-Procurement ──▶ Proposal ──▶ Technical  ──▶ Award/    │  │
│  │   Portal          Preparation   Evaluation     Contract   │  │
│  │  (g2b.go.kr)                  (Security pts)              │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                Execution and Review Phase                  │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │  Development ──▶ Security Review ──▶ Review Pass ──▶Deploy│  │
│  │  (Secure coding)   Application      (Remediation)         │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 21-1. Procurement Agency Security Requirements

### Government e-Procurement (www.g2b.go.kr)

Public procurement electronic bidding system

| Category | Content |
|----------|---------|
| Procurement methods | Open competition, limited competition, negotiation |
| Contract types | Goods, services, construction |
| Registration requirements | Business registration, procurement registration |

### IT Project Security Requirements

#### Mandatory Security Review

| Target | Criteria |
|--------|----------|
| Mandatory | Over 100M KRW or critical infrastructure connected |
| Recommended | IT projects over 10M KRW |

#### Security Certification Requirements

| Certification | Required Situation |
|---------------|-------------------|
| ISMS | Large-scale information system operation |
| ISMS-P | Personal information processing systems |
| ISO 27001 | International certification required |
| CC Certification | Security product deployment |

### Procurement Product Security Requirements

#### Software Products

| Item | Requirement |
|------|-------------|
| Secure Coding | Ministry of Interior guide compliance |
| Vulnerability Assessment | KISA or professional agency assessment |
| Source Code | Escrow or submission |

#### Information Security Products

| Item | Requirement |
|------|-------------|
| CC Certification | Domestic CC certification required |
| Technical Support | Domestic support capability |
| Maintenance | Maintenance plan submission |

---

## 21-2. Proposal Writing Guide

### Proposal Security Section Structure

```markdown
## Security Plan

### 1. Development Security
#### 1.1 Secure Coding
- Applied Guide: Ministry of Interior Secure Coding Guide
- Assessment Tool: [Tool name]
- Assessment Frequency: Per development phase

#### 1.2 Source Code Review
- Review Method: Static analysis + dynamic analysis
- Review Agency: [Agency name/self]
- Remediation Plan: 100% remediation of findings

### 2. System Security
#### 2.1 Access Control
- Network Segregation: DMZ, work network, DB network
- Firewall Policy: Least privilege principle
- Access Logs: Retain 6+ months

#### 2.2 Authentication/Authorization
- Authentication Method: ID/PW + OTP
- Authorization Management: RBAC-based
- Privileged Accounts: Separate management

### 3. Data Security
#### 3.1 Encryption
- In-transit: TLS 1.2 or higher
- At-rest: AES-256
- Key Management: HSM or separate management

#### 3.2 Personal Information
- Collection minimization
- Masking
- Disposal procedures

### 4. Operational Security
#### 4.1 Security Monitoring
- 24x7 monitoring
- Anomaly detection/response
- Monthly reporting

#### 4.2 Vulnerability Management
- Regular assessment: Annually
- Patch management: Monthly
```

### Proposal Differentiation Points

| Area | Differentiation Points |
|------|----------------------|
| Certification | ISMS/ISO 27001 holder |
| Experience | Similar public project track record |
| Tools | Proprietary security assessment tools |
| Personnel | Information security professionals |
| Methodology | Security development methodology |

### Proposal Evaluation Security Scoring

| Evaluation Item | Score Example |
|-----------------|:-------------:|
| Technical (including security) | 50-60 pts |
| Price | 30-40 pts |
| Other (track record, etc.) | 10-20 pts |

> **TIP**
> Security items often comprise 10-20% of technical evaluation. Emphasize specific methodologies and experience.

---

## 21-3. Security Review Response

### What is Security Review?

A procedure to review whether security requirements are met when deploying or developing information systems in administrative agencies

| Item | Content |
|------|---------|
| Legal Basis | e-Government Act Article 56 |
| Target | Public organization information systems |
| Review Agency | NIS (national/public) or self-review |

### Security Review Procedure

```
1. Review Application
   - Submit project overview, system architecture
     ↓
2. Document Review
   - Security requirement compliance check
     ↓
3. On-site Review (if necessary)
   - Verify actual deployment environment
     ↓
4. Review Result Notification
   - Pass / Remediation Required / Fail
     ↓
5. Remediation (if necessary)
   - Address findings and re-review
```

### Security Review Preparation Checklist

| Area | Check Items | Check |
|------|-------------|:-----:|
| **Network** | Network segregation applied | ☐ |
| | Firewall policy appropriateness | ☐ |
| | Encrypted communication applied | ☐ |
| **System** | Security settings applied | ☐ |
| | CC-certified products deployed | ☐ |
| | Access control applied | ☐ |
| **Application** | Secure coding applied | ☐ |
| | Vulnerability assessment completed | ☐ |
| | Input validation | ☐ |
| **Data** | Encryption applied | ☐ |
| | Personal information protection | ☐ |
| | Log management | ☐ |
| **Administrative** | Security policy established | ☐ |
| | Operational procedures established | ☐ |
| | Training plan | ☐ |

### Common Security Review Findings

| Area | Frequent Findings |
|------|-------------------|
| Network | Unnecessary ports open, inadequate segregation |
| System | Default accounts unchanged, patches not applied |
| Application | SQL Injection, XSS vulnerabilities |
| Data | Unencrypted transmission/storage |
| Administrative | Logs not retained, procedures not established |

### Security Review Timeline Example

| Phase | Duration | Activities |
|-------|:--------:|------------|
| Preparation | 2 weeks | Document preparation, self-assessment |
| Application | 1 day | Submit review application |
| Document review | 2-4 weeks | Review in progress |
| Remediation | 1-2 weeks | Address findings |
| Completion | 1 week | Final review pass |

---

## Public Procurement Entry Preparation

### Pre-Certification Acquisition

| Certification | Benefits | Duration |
|---------------|----------|:--------:|
| ISMS | Bidding bonus points, credibility | 6 months-1 year |
| ISO 27001 | International certification | 3-6 months |
| GS Certification | Software quality | 2-3 months |
| CC Certification | Security products required | 6 months-1 year |

### Track Record Building

| Method | Description |
|--------|-------------|
| Direct execution | Execute without subcontracting |
| Joint venture | Joint execution with experienced company |
| Solo track record | Start with small projects |

### Professional Personnel

| Qualification | Field |
|---------------|-------|
| Information Security Engineer | Overall security |
| CISA/CISSP | Audit/management |
| OSCP | Penetration testing |

---

## Summary

| Item | Key Content |
|------|-------------|
| Procurement Requirements | CC certification, secure coding, vulnerability assessment |
| Proposal | Detailed security plan, methodology presentation |
| Security Review | Advance preparation, checklist utilization |
| Preparation | ISMS certification, track record, personnel |

---

*Next Chapter: Chapter 22. Automation Tool Development*
