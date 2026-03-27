# Chapter 1. Introduction

> Part I. Fundamentals

---

## 1-1. What is KESE KIT?

KESE KIT (Korea Enhanced Security Evaluation - KISA Infrastructure Toolkit) is a practical guide for systematically conducting vulnerability analysis and assessment of Critical Information Infrastructure (CII).

### Purpose of KESE KIT

KESE KIT was developed with the following objectives:

1. **Enhance practitioner capabilities**: Help vulnerability assessment practitioners accurately understand and apply inspection items.
2. **Support inspection automation**: Automate repetitive technical inspections with scripts to improve efficiency.
3. **Provide consistent evaluation criteria**: Ensure assessment consistency by clarifying Good/Partial/Vulnerable judgment criteria.
4. **Optimize for government project environments**: Provide practical guidance reflecting the unique requirements of public institutions and government projects.

### KESE KIT Structure

```
┌─────────────────────────────────────────────────────────────┐
│                        KESE KIT                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Technical  │  │Administrative│  │  Physical   │         │
│  │Vulnerabilities│ │Vulnerabilities│ │Vulnerabilities│       │
│  │   (~424)    │  │    (127)    │  │     (9)     │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Automation Scripts / Tools                 │   │
│  │           (Bash, PowerShell, Python)                │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Checklists / Forms / Reports               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

| Component | Description |
|-----------|-------------|
| Technical Vulnerability Assessment | 12 domains including Unix, Windows, Web, DBMS, Network |
| Administrative Vulnerability Assessment | 14 areas including Policy, Organization, HR Security, Access Control |
| Physical Vulnerability Assessment | Physical security, Protected area management |
| Automation Scripts | Automation tools for technical inspection items |
| Checklists/Forms | Templates ready for immediate practical use |

> **TIP**
> KESE KIT is based on the official guide from the Korea Internet & Security Agency (KISA), restructured with a focus on practical application.

---

## 1-2. Understanding Critical Information Infrastructure (CII)

### What is Critical Information Infrastructure?

Critical Information Infrastructure (CII) refers to electronic control and management systems related to national security, administration, defense, public safety, finance, telecommunications, transportation, energy, and other sectors. If compromised, these systems could have significant impacts on national security and the economy and society.

### Legal Basis

Critical Information Infrastructure is designated and managed under the "Act on the Protection of Information and Communications Infrastructure."

```
Article 8 of the Act on the Protection of Information and Communications Infrastructure
(Designation of Critical Information Infrastructure)

① The head of a central administrative agency may designate information and
   communications infrastructure that requires protection from electronic
   intrusion activities as critical information infrastructure, considering
   the following matters within their jurisdiction.
```

### CII Designation Status (By Sector)

| Sector | Examples |
|--------|----------|
| Finance | Bank computer networks, Securities trading systems |
| Telecommunications | Major carrier networks |
| Energy | Power grid control systems, Gas supply networks |
| Transportation | Air traffic control systems, Railway control systems |
| Healthcare | Major hospital medical information systems |
| Administration | Resident registration systems, National Tax Service systems |

> **WARNING**
> Organizations managing CII-designated facilities must conduct mandatory annual vulnerability analysis and assessment. Non-compliance may result in legal penalties.

---

## 1-3. Necessity of Vulnerability Analysis and Assessment

### Legal Obligation

Under Article 9 of the "Act on the Protection of Information and Communications Infrastructure," organizations managing critical information infrastructure must conduct regular vulnerability analysis and assessment.

```
Article 9 of the Act on the Protection of Information and Communications Infrastructure
(Vulnerability Analysis and Assessment)

① The head of a managing organization shall analyze and assess vulnerabilities
   of their critical information infrastructure regularly as prescribed by
   Presidential Decree.
```

### Assessment Performers

| Performer | Description |
|-----------|-------------|
| Self-assessment | Conducted by the organization's own personnel |
| External delegation | Delegated to KISA or specialized information security service companies |

### Assessment Categories

Vulnerability analysis and assessment is divided into three main categories:

| Category | Items | Key Content |
|----------|:-----:|-------------|
| Technical Vulnerabilities | ~424 | System security: servers, networks, databases, web |
| Administrative Vulnerabilities | 127 | Policy, organization, HR security, access control |
| Physical Vulnerabilities | 9 | Physical security, protected area management |

### Utilizing Assessment Results

Vulnerability analysis and assessment results are used as follows:

1. **Developing protection measures**: Establish improvement plans for identified vulnerabilities
2. **Budget justification**: Provide objective basis for information security budget requests
3. **Executive reporting**: Report on organization's security posture
4. **Regulatory compliance**: Evidence of legal obligation fulfillment

---

## 1-4. Book Structure and How to Use It

### Overall Structure

KESE KIT consists of 4 Parts and Appendices.

| Part | Content | Target Audience |
|------|---------|-----------------|
| **Part I** | Fundamentals | All readers |
| **Part II** | Technical Vulnerability Assessment | System/Security administrators |
| **Part III** | Administrative/Physical Vulnerability Assessment | Security managers, Policy officers |
| **Part IV** | Practical Application | Government project managers, Developers |
| **Appendix** | Checklists, Forms, Glossary | Everyone |

### Detailed Part Contents

#### Part I. Fundamentals (Chapters 1-2)
- Concepts and legal basis of Critical Information Infrastructure
- Understanding the vulnerability analysis and assessment framework

#### Part II. Technical Vulnerability Assessment (Chapters 3-12)
- Unix/Linux, Windows server inspection
- Web service, Web application inspection
- DBMS, Network, Security equipment inspection
- Virtualization, Cloud, Control system inspection

#### Part III. Administrative/Physical Vulnerability Assessment (Chapters 13-19)
- Information security policy and organization
- Asset management, Risk management
- HR security, Third-party security
- Access control, Operations management
- Incident response, Business continuity
- Physical security

#### Part IV. Practical Application (Chapters 20-22)
- Applying to government project environments
- Responding to public procurement market
- Building automation tools

### How to Use

> **TIP**
> This book doesn't need to be read sequentially from beginning to end. Select and reference the chapters you need based on your responsibilities.

---

## 1-5. Learning Paths by Reader Type

### Recommended Paths by Reader Type

#### Developers Using Vibe Coding
```
Chapter 1 → Chapter 6 (Web Application) → Chapter 22 (Automation Tools) → Appendix
```
Understand the core of web application security and learn how to automate security during development.

#### Server Operations Staff
```
Chapter 1 → Chapter 2 → Chapter 3 (Unix) → Chapter 4 (Windows) → Chapter 7 (DBMS) → Appendix
```
Learn how to directly inspect and remediate vulnerabilities on servers you operate.

#### Government Project Developers
```
Chapter 1 → Chapter 2 → Chapter 20 (Government Projects) → Chapter 21 (Public Procurement) → Required technical chapters
```
First understand security requirements for government project environments, then study necessary technical areas.

#### Security Managers/CISO
```
Chapter 1 → Chapter 2 → Chapter 13 (Policy) → Chapter 14 (Asset Management) → Chapter 18 (Incident Response) → Full overview
```
Learn how to inspect and improve organization's security framework from a management perspective.

#### Those New to Servers
```
Chapter 1 → Chapter 2 → Chapter 3 (Unix basics) → Chapter 5 (Web service basics) → Gradual expansion
```
Build inspection capabilities by learning step by step from the basics.

### Quick Reference Guide

| Situation | Reference Chapter |
|-----------|-------------------|
| "Need to inspect Linux servers" | Chapter 3 |
| "Need to inspect web vulnerabilities" | Chapters 5, 6 |
| "Need to establish information security policy" | Chapter 13 |
| "Need incident response procedures" | Chapter 18 |
| "Want to create inspection scripts" | Chapter 22 |

---

## Summary

- **KESE KIT** is a practical guide for vulnerability analysis and assessment of Critical Information Infrastructure (CII).
- Under Article 9 of the "Act on the Protection of Information and Communications Infrastructure," CII managing organizations must conduct annual vulnerability analysis and assessment.
- Assessment items are categorized into **Technical** (~424), **Administrative** (127), and **Physical** (9) domains.
- Structured so readers can **selectively study** based on their role and needs.

---

*Next Chapter: Chapter 2. Legal Framework and Assessment Framework*
