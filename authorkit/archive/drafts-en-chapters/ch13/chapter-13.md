# Chapter 13. Information Security Policy and Organization

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Administrative vulnerability assessment, unlike technical assessment, involves reviewing policies, guidelines, and procedures, along with conducting interviews with relevant personnel. This chapter covers Information Security Policy (A-1 ~ A-7) and Information Security Organization (A-8 ~ A-9).

```
┌─────────────────────────────────────────────────────────────────┐
│        Information Security Policy and Organization (A-1 ~ A-9)  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │   Executive     │                          │
│                    │   Approval      │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Information Security Policy (A-1 ~ A-7)         │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │  A-1 Policy Est.   A-2 Impl. Docs   A-3 Distribution     │   │
│  │  A-4 Validity Rev  A-5 Stakeholder  A-6 Annual Plan      │   │
│  │  A-7 Long-term Plan                                       │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │         Information Security Organization (A-8 ~ A-9)     │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │                                                          │   │
│  │   ┌─────────────┐           ┌─────────────┐             │   │
│  │   │ A-8 Dedic.  │           │ A-9 Committee│            │   │
│  │   │   Team      │           │              │             │   │
│  │   │ • CISO      │           │ • Deliberate │             │   │
│  │   │ • Policy    │◀─────────▶│ • Budget     │             │   │
│  │   │ • SOC       │           │ • Plan       │             │   │
│  │   │ • Tech      │           │   Approval   │             │   │
│  │   └─────────────┘           └─────────────┘             │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Information Security Policy | A-1 ~ A-7 | 7 |
| Information Security Organization | A-8 ~ A-9 | 2 |

> **TIP**
> Administrative assessment requires a combination of document review + interviews + on-site inspection. Prepare a list of required documents in advance for efficiency.

---

## 13-1. Information Security Policy (A-1 ~ A-7)

### A-1. Establish Policy and Obtain Executive Approval

| Item | Content |
|------|---------|
| **Assessment Item** | Establish information security policies/guidelines applicable to the entire organization and obtain executive approval |
| **Related Dept.** | Information Security Department |

#### Assessment Points

- Existence of organization's top-level information security policy document
- Official approval by CEO/head of organization (approval document or signed copy)
- Clear basis and criteria for information security activities

#### Judgment Criteria

| Judgment | Criteria |
|:--------:|----------|
| Good | Top-level information security policy established with executive approval |
| Partial | Policy exists but approval history unclear |
| Vulnerable | No information security policy established |

#### Related Regulations

| Category | Regulation |
|----------|------------|
| Common | Act on Protection of Information and Communications Infrastructure, Article 10 (Protection Guidelines) |
| Common | Personal Information Protection Act, Article 29 (Security Measures) |
| Public | National Information Security Basic Guidelines, Articles 4, 7 |
| Financial | Electronic Financial Transactions Act, Article 21 (Security Requirements) |

---

### A-2. Establish Implementation Documents

| Item | Content |
|------|---------|
| **Assessment Item** | Define and document methods, procedures, and frequencies needed to implement information security policy |
| **Related Dept.** | Information Security Department, System Operations Department |

#### Required Implementation Documents

| Document Type | Examples |
|---------------|----------|
| Guidelines | Information System Operation Guidelines, Access Control Guidelines |
| Procedures | Account Management Procedure, Change Management Procedure |
| Manuals | Security Incident Response Manual |
| Guides | Secure Password Creation Guide |

---

### A-3. Policy Publication and Distribution

| Item | Content |
|------|---------|
| **Assessment Item** | Provide information security policies and implementation documents in an accessible format to all employees and stakeholders |
| **Related Dept.** | Information Security Department |

#### Distribution Methods

- Internal bulletin board posting
- Email distribution
- Groupware announcement
- Printed copy distribution

---

### A-4. Policy Validity Review

| Item | Content |
|------|---------|
| **Assessment Item** | Periodically or upon significant changes, review and evaluate the validity of information security policies and implementation documents, then revise and supplement |
| **Review Frequency** | At least annually |

#### Review Triggers

- Regular review: At least annually
- Ad-hoc review: Upon significant changes
  - Enactment/amendment of security-related regulations
  - Organizational restructuring, new service introduction
  - New system deployment
  - Security incident occurrence
  - Discovery of new threats/vulnerabilities

---

### A-5. Stakeholder Review

| Item | Content |
|------|---------|
| **Assessment Item** | Obtain stakeholder review when enacting/revising information security policies and implementation documents, and reflect their input |
| **Related Dept.** | Information Security Department, Related Departments |

#### Stakeholders

- Chief Information Security Officer (CISO)
- IT Operations Department
- Business Department Representatives
- Legal/Audit Department

---

### A-6. Annual Information Security Work Plan

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement detailed annual information security work plan |
| **Related Dept.** | Information Security Department |

#### Annual Plan Components

| Item | Content |
|------|---------|
| Vulnerability Assessment | Annual assessment schedule and scope |
| Training | Employee security awareness training plan |
| Drills | Security incident response exercises |
| Budget | Information security budget allocation |
| Systems | Security system deployment/renewal plan |

---

### A-7. Long-term Plan

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement long-term (3+ years) plan to strengthen organizational information security |
| **Related Dept.** | Information Security Department, Executive Management |

#### Long-term Plan Example

| Year | Objectives |
|:----:|------------|
| Year 1 | Foundation: Policy systematization, essential security systems deployment |
| Year 2 | Enhancement: Security operations strengthening, automation tools development |
| Year 3 | Maturity: ISMS certification, continuous improvement framework |

---

## 13-2. Information Security Organization (A-8 ~ A-9)

### A-8. Dedicated Information Security Team

| Item | Content |
|------|---------|
| **Assessment Item** | Establish a dedicated team and personnel to plan, execute, and review information security activities |
| **Related Dept.** | Information Security Department, HR Department |

#### Organization Structure Example

```
[CEO/Executive Director]
        ↓
[Chief Information Security Officer (CISO)]
        ↓
[Dedicated Information Security Department]
    ├── Policy/Planning Team
    ├── Security Operations Center (SOC)
    └── Technical Security Team
```

#### Assessment Points

- Existence of dedicated information security team or designated personnel
- Information security organization shown in organizational chart
- Defined roles and responsibilities for personnel

---

### A-9. Information Security Committee

| Item | Content |
|------|---------|
| **Assessment Item** | Information Security Committee is established with documented roles and responsibilities |
| **Related Dept.** | Information Security Department, Executive Management |

#### Committee Composition

| Role | Responsibility |
|------|----------------|
| Chairperson | CEO or Deputy Head |
| Secretary | Chief Information Security Officer (CISO) |
| Members | Department Heads, External Experts |

#### Committee Responsibilities

- Deliberate and approve information security policies
- Determine response direction for major security incidents
- Review information security budget
- Approve annual information security plan

#### Meeting Frequency

- Regular meetings: At least twice annually
- Ad-hoc meetings: Upon significant issues

---

## 13-3. Policy/Guideline Document Templates

### Information Security Policy Table of Contents Example

```markdown
Chapter 1. General Provisions
  Article 1 (Purpose)
  Article 2 (Scope)
  Article 3 (Definitions)
  Article 4 (Responsibilities and Obligations)

Chapter 2. Information Security Organization
  Article 5 (Information Security Committee)
  Article 6 (Chief Information Security Officer)
  Article 7 (Information Security Personnel)

Chapter 3. Information Asset Management
  Article 8 (Asset Classification)
  Article 9 (Asset Protection)

Chapter 4. Human Resource Security
  Article 10 (Pre-employment Security)
  Article 11 (During Employment Security)
  Article 12 (Termination Security)

Chapter 5. Physical Security
  Article 13 (Protected Areas)
  Article 14 (Access Control)

Chapter 6. Technical Security
  Article 15 (Access Control)
  Article 16 (Encryption)
  Article 17 (Network Security)

Chapter 7. Operational Security
  Article 18 (Change Management)
  Article 19 (Backup)
  Article 20 (Log Management)

Chapter 8. Incident Response
  Article 21 (Incident Reporting)
  Article 22 (Incident Handling)
  Article 23 (Prevention of Recurrence)

Chapter 9. Supplementary Provisions
  Article 24 (Disciplinary Actions for Violations)
  Article 25 (Effective Date)
```

---

### Policy Validity Review Checklist

| Review Item | Y/N | Notes |
|-------------|:---:|-------|
| Reflected changes in related laws | | |
| Reflected organizational changes | | |
| Reflected system changes | | |
| Consistency of terminology | | |
| Clarity of roles/responsibilities | | |
| Feasibility | | |
| Measurable criteria included | | |

---

## Assessment Execution Guide

### Preparation

1. **Document Request List**
   - Information security policy
   - Implementation guidelines/procedures
   - Organizational chart
   - Information Security Committee meeting minutes
   - Annual plan
   - Long-term plan

2. **Interview Subject Selection**
   - Chief Information Security Officer (CISO)
   - Information security personnel
   - IT operations personnel

### Assessment Verification Items

| Item | Verification Method |
|------|---------------------|
| A-1 | Policy document + approval document review |
| A-2 | Implementation document existence + revision history |
| A-3 | Distribution history or posting location verification |
| A-4 | Validity review result document |
| A-5 | Stakeholder review feedback document |
| A-6 | Annual plan and implementation results |
| A-7 | Long-term plan document |
| A-8 | Organizational chart + job descriptions |
| A-9 | Committee regulations + meeting minutes |

---

## Summary

| Item | Key Assessment Content | Priority |
|------|------------------------|:--------:|
| A-1 | Top-level policy + executive approval | Highest |
| A-2 | Implementation documents (guidelines/procedures) | Highest |
| A-6 | Annual plan establishment and implementation | High |
| A-8 | Dedicated team/personnel designation | Highest |
| A-9 | Information Security Committee composition and operation | High |

---

*Next Chapter: Chapter 14. Asset Management and Risk Management*
