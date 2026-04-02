# KESE KIT

## CII Vulnerability Assessment Practical Guide

---

# 목차

  - [1-1. What is KESE KIT?](#1-1-what-is-kese-kit)
  - [1-2. Understanding Critical Information Infrastructure (CII)](#1-2-understanding-critical-information-infrastructure-cii)
  - [1-3. Necessity of Vulnerability Analysis and Assessment](#1-3-necessity-of-vulnerability-analysis-and-assessment)
  - [1-4. Book Structure and How to Use It](#1-4-book-structure-and-how-to-use-it)
  - [1-5. Learning Paths by Reader Type](#1-5-learning-paths-by-reader-type)
  - [2-1. Overview of the Act on Protection of Information and Communications Infrastructure](#2-1-overview-of-the-act-on-protection-of-information-and-communications-infrastructure)
  - [2-2. Vulnerability Analysis and Assessment Obligation (Article 9)](#2-2-vulnerability-analysis-and-assessment-obligation-article-9)
  - [2-3. Role of KISA and Assessment Framework](#2-3-role-of-kisa-and-assessment-framework)
  - [2-4. Assessment Item Classification (Administrative/Physical/Technical)](#2-4-assessment-item-classification-administrativephysicaltechnical)
  - [2-5. Judgment Criteria (Good/Partial/Vulnerable)](#2-5-judgment-criteria-goodpartialvulnerable)
  - [3-1. Account Management (U-01 ~ U-13)](#3-1-account-management-u-01-u-13)
  - [3-2. File and Directory Management (U-14 ~ U-33)](#3-2-file-and-directory-management-u-14-u-33)
  - [3-3. Service Management (U-34 ~ U-63)](#3-3-service-management-u-34-u-63)
  - [3-4. Patch Management (U-64)](#3-4-patch-management-u-64)
  - [3-5. Log Management (U-65 ~ U-68)](#3-5-log-management-u-65-u-68)
  - [3-6. Automation Scripts](#3-6-automation-scripts)
  - [4-1. Account Management (W-01 ~ W-14)](#4-1-account-management-w-01-w-14)
  - [4-2. Service Management (W-15 ~ W-39)](#4-2-service-management-w-15-w-39)
  - [4-3. Patch Management (W-40 ~ W-41)](#4-3-patch-management-w-40-w-41)
  - [4-4. Log Management (W-42 ~ W-47)](#4-4-log-management-w-42-w-47)
  - [4-5. Security Management (W-48 ~ W-73)](#4-5-security-management-w-48-w-73)
  - [4-6. PowerShell Assessment Script](#4-6-powershell-assessment-script)
  - [5-1. Account Management (WS-01 ~ WS-05)](#5-1-account-management-ws-01-ws-05)
  - [5-2. Service Management (WS-06 ~ WS-30)](#5-2-service-management-ws-06-ws-30)
  - [5-3. Security Settings (WS-31 ~ WS-43)](#5-3-security-settings-ws-31-ws-43)
  - [5-4. Patch and Log Management (WS-44 ~ WS-47)](#5-4-patch-and-log-management-ws-44-ws-47)
  - [6-1. Input Validation (SQL Injection, XSS, CSRF)](#6-1-input-validation-sql-injection-xss-csrf)
  - [6-2. Authentication and Session Management](#6-2-authentication-and-session-management)
  - [6-3. Access Control and Authorization Verification](#6-3-access-control-and-authorization-verification)
  - [6-4. Information Disclosure Prevention](#6-4-information-disclosure-prevention)
  - [6-5. Security in Vibe Coding Environments](#6-5-security-in-vibe-coding-environments)
  - [7-1. Account Management (D-01 ~ D-16)](#7-1-account-management-d-01-d-16)
  - [7-2. Access Management (D-17 ~ D-23)](#7-2-access-management-d-17-d-23)
  - [7-3. Option Management (D-24 ~ D-30)](#7-3-option-management-d-24-d-30)
  - [7-4. Patch Management (D-31 ~ D-32)](#7-4-patch-management-d-31-d-32)
  - [7-5. DB Assessment Scripts](#7-5-db-assessment-scripts)
  - [8-1. Account Management (N-01 ~ N-10)](#8-1-account-management-n-01-n-10)
  - [8-2. Access Management (N-11 ~ N-18)](#8-2-access-management-n-11-n-18)
  - [8-3. Patch Management (N-19)](#8-3-patch-management-n-19)
  - [8-4. Log Management (N-20 ~ N-24)](#8-4-log-management-n-20-n-24)
  - [8-5. Feature Management (N-25 ~ N-40)](#8-5-feature-management-n-25-n-40)
  - [9-1. Firewall Assessment (S-01 ~ S-19)](#9-1-firewall-assessment-s-01-s-19)
  - [9-2. IDS/IPS Assessment](#9-2-idsips-assessment)
  - [9-3. WAF Assessment](#9-3-waf-assessment)
  - [10-1. Virtualization Equipment (V-01 ~ V-36)](#10-1-virtualization-equipment-v-01-v-36)
  - [10-2. Cloud Environment (CL-01 ~ CL-14)](#10-2-cloud-environment-cl-01-cl-14)
  - [10-3. Container Security (Docker, K8s)](#10-3-container-security-docker-k8s)
  - [11-1. Account Management (PC-01 ~ PC-04)](#11-1-account-management-pc-01-pc-04)
  - [11-2. Access Management (PC-05 ~ PC-11)](#11-2-access-management-pc-05-pc-11)
  - [11-3. Patch Management (PC-12 ~ PC-13)](#11-3-patch-management-pc-12-pc-13)
  - [11-4. Security Management (PC-14 ~ PC-18)](#11-4-security-management-pc-14-pc-18)
  - [12-1. Control System Characteristics](#12-1-control-system-characteristics)
  - [12-2. Account/Service Management (C-01 ~ C-14)](#12-2-accountservice-management-c-01-c-14)
  - [12-3. Network/Physical Access Control (C-19 ~ C-27)](#12-3-networkphysical-access-control-c-19-c-27)
  - [12-4. Security Threat Detection and Recovery (C-28 ~ C-38)](#12-4-security-threat-detection-and-recovery-c-28-c-38)
  - [13-1. Information Security Policy (A-1 ~ A-7)](#13-1-information-security-policy-a-1-a-7)
  - [13-2. Information Security Organization (A-8 ~ A-9)](#13-2-information-security-organization-a-8-a-9)
  - [13-3. Policy/Guideline Document Templates](#13-3-policyguideline-document-templates)
  - [14-1. Asset Classification (A-10 ~ A-14)](#14-1-asset-classification-a-10-a-14)
  - [14-2. Risk Management (A-15 ~ A-17)](#14-2-risk-management-a-15-a-17)
  - [14-3. Audit (A-18 ~ A-20)](#14-3-audit-a-18-a-20)
  - [14-4. Asset Inventory Management Automation](#14-4-asset-inventory-management-automation)
  - [15-1. Human Resource Security (A-21 ~ A-26)](#15-1-human-resource-security-a-21-a-26)
  - [15-2. External Party Security (A-27 ~ A-33)](#15-2-external-party-security-a-27-a-33)
  - [15-3. Security Pledge Templates](#15-3-security-pledge-templates)
  - [16-1. Training (A-34 ~ A-38)](#16-1-training-a-34-a-38)
  - [16-2. Authentication and Authorization (A-39 ~ A-42)](#16-2-authentication-and-authorization-a-39-a-42)
  - [16-3. Access Control (A-43 ~ A-55)](#16-3-access-control-a-43-a-55)
  - [17-1. Operations Management (A-56 ~ A-93)](#17-1-operations-management-a-56-a-93)
  - [17-2. Security Management (A-94 ~ A-103)](#17-2-security-management-a-94-a-103)
  - [17-3. Network Air-Gap Configuration](#17-3-network-air-gap-configuration)
  - [18-1. Incident Response (A-104 ~ A-113)](#18-1-incident-response-a-104-a-113)
  - [18-2. Business Continuity (A-114 ~ A-118)](#18-2-business-continuity-a-114-a-118)
  - [18-3. Incident Reporting Procedures](#18-3-incident-reporting-procedures)
  - [19-1. Physical Security Assessment (B-1 ~ B-9)](#19-1-physical-security-assessment-b-1-b-9)
  - [19-2. Protected Area Management](#19-2-protected-area-management)
  - [20-1. Public Organization Security Requirements](#20-1-public-organization-security-requirements)
  - [20-2. Information Security Budget Guidelines](#20-2-information-security-budget-guidelines)
  - [20-3. Pre-Certified Product Utilization](#20-3-pre-certified-product-utilization)
  - [21-1. Procurement Agency Security Requirements](#21-1-procurement-agency-security-requirements)
  - [21-2. Proposal Writing Guide](#21-2-proposal-writing-guide)
  - [21-3. Security Review Response](#21-3-security-review-response)
  - [22-1. Assessment Script Architecture](#22-1-assessment-script-architecture)
  - [22-2. Integrated Assessment Scripts](#22-2-integrated-assessment-scripts)
  - [22-3. Result Collection and Reporting](#22-3-result-collection-and-reporting)
  - [22-4. CI/CD Pipeline Integration](#22-4-cicd-pipeline-integration)

---

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


---

# Chapter 2. Legal Framework and Assessment Framework

> Part I. Fundamentals

---

## 2-1. Overview of the Act on Protection of Information and Communications Infrastructure

### Purpose of the Act

The "Act on the Protection of Information and Communications Infrastructure" aims to ensure stable operation of critical information infrastructure by establishing and implementing protection measures against electronic intrusion activities, thereby ensuring national security and stability of citizens' lives.

### Key Provisions

| Article | Content | Related Work |
|---------|---------|--------------|
| Article 5 | Critical Information Infrastructure Protection Committee | Policy deliberation and coordination |
| Article 8 | Designation of Critical Information Infrastructure | CII designation criteria |
| Article 9 | Vulnerability Analysis and Assessment | **Core obligation provision** |
| Article 10 | Protection Guidelines | Protection measure standards |
| Article 12 | Notification of Security Incidents | Incident reporting obligation |
| Article 13 | Response to Security Incidents | Recovery and response |

### Legal Framework

```
Act on Protection of Information and Communications Infrastructure (Law)
    ├── Enforcement Decree (Presidential Decree)
    ├── Enforcement Rules (Ministerial Ordinance)
    └── Protection Guidelines (KISA Notice)
        ├── Technical Vulnerability Analysis and Assessment Detailed Guide
        └── Administrative/Physical Vulnerability Analysis and Assessment Guide
```

> **TIP**
> The inspection items covered in this book are based on KISA's official guides. Check for the latest version when laws are amended or guides are updated.

---

## 2-2. Vulnerability Analysis and Assessment Obligation (Article 9)

### Original Legal Text

```
Article 9 of the Act on Protection of Information and Communications Infrastructure
(Vulnerability Analysis and Assessment)

① The head of a managing organization shall regularly analyze and assess
   vulnerabilities of their critical information infrastructure as prescribed
   by Presidential Decree.

② The head of a central administrative agency may order the head of the
   relevant managing organization to analyze and assess vulnerabilities of
   critical information infrastructure in any of the following cases:
   1. When necessary to protect critical information infrastructure from
      new types of electronic intrusion activities
   2. When significant changes have occurred in the critical information
      infrastructure requiring separate vulnerability analysis and assessment

③ When the head of a managing organization intends to analyze and assess
   vulnerabilities pursuant to paragraphs (1) and (2), they may have KISA
   or an information security service company designated under Article 23
   of the "Act on Promotion of Information Security Industry" analyze and
   assess the vulnerabilities of their critical information infrastructure
   as prescribed by Presidential Decree.
```

### Assessment Frequency

| Type | Frequency | Notes |
|------|-----------|-------|
| Regular assessment | **At least annually** | Mandatory |
| Ad-hoc assessment | When significant changes occur | By order of central administrative agency |

### Assessment Methods

Vulnerability analysis and assessment can be performed in one of three ways:

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| **Self-assessment** | Conducted by organization's own personnel | Cost savings, Internal capability building | Possible lack of expertise |
| **KISA delegation** | Delegated to Korea Internet & Security Agency | High expertise, Credibility | Schedule coordination needed |
| **Specialized company delegation** | Delegated to information security service company | Expertise, Flexible scheduling | Cost incurred |

> **WARNING**
> Failure to conduct vulnerability analysis and assessment or falsely reporting results may result in legal penalties.

---

## 2-3. Role of KISA and Assessment Framework

### Role of Korea Internet & Security Agency (KISA)

The Korea Internet & Security Agency (KISA) performs the following roles related to critical information infrastructure protection:

| Role | Content |
|------|---------|
| Conducting vulnerability analysis and assessment | Direct execution when delegated by managing organizations |
| Guide development and distribution | Developing inspection items and methodologies |
| Technical support | Technical support for self-assessment |
| Professional training | Training vulnerability assessment professionals |
| Incident response | Technical support during security incidents |

### Assessment Framework Structure

```
┌─────────────────────────────────────────────────────────┐
│              Central Administrative Agencies             │
│     (Ministry of Science and ICT, etc.)                 │
└─────────────────────┬───────────────────────────────────┘
                      │ Policy guidelines
                      ▼
┌─────────────────────────────────────────────────────────┐
│          Korea Internet & Security Agency (KISA)         │
│    - Guide development    - Assessment    - Support     │
└─────────────────────┬───────────────────────────────────┘
                      │ Guides/Support
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  Managing Organizations                  │
│          (Organizations operating CII)                   │
│    - Self-assessment or delegated assessment            │
│    - Results reporting and protection measure implementation │
└─────────────────────────────────────────────────────────┘
```

### Assessment Process

```
┌─────────────────────────────────────────────────────────────────┐
│              Vulnerability Analysis and Assessment Process       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│   │1. Planning│───▶│2. Data   │───▶│3. Vuln.  │                  │
│   │          │    │Collection│    │Assessment│                  │
│   └──────────┘    └──────────┘    └────┬─────┘                  │
│                                        │                         │
│                                        ▼                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│   │6. Protect│◀───│5. Report │◀───│4. Result │                  │
│   │ Measures │    │  Writing │    │ Analysis │                  │
│   └────┬─────┘    └──────────┘    └──────────┘                  │
│        │                                                         │
│        ▼                                                         │
│   ┌──────────┐                                                   │
│   │7. Impl.  │                                                   │
│   │  Review  │                                                   │
│   └──────────┘                                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Phase | Activities | Deliverables |
|:-----:|------------|--------------|
| 1 | Planning | Assessment plan |
| 2 | Data collection | System inventory, Network diagrams |
| 3 | Vulnerability assessment | Assessment results |
| 4 | Result analysis | Vulnerability list |
| 5 | Report writing | Vulnerability analysis and assessment report |
| 6 | Protection measure development | Remediation plan |
| 7 | Implementation review | Implementation review results |

---

## 2-4. Assessment Item Classification (Administrative/Physical/Technical)

### Overview of Three Categories

Vulnerability analysis and assessment items are divided into three main categories:

```
┌─────────────────────────────────────────────────────────────────┐
│           Vulnerability Analysis and Assessment Categories       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               Technical Vulnerabilities                    │  │
│  │                   (~424 items)                             │  │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐        │  │
│  │  │Unix │ │ Win │ │ Web │ │DBMS │ │ Net │ │Other│        │  │
│  │  │(68) │ │(73) │ │(47) │ │(32) │ │(40) │ │(164)│        │  │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│  ┌─────────────────┐  ┌─────────────┐  ┌─────────────────┐     │
│  │  Administrative │  │ Information │  │    Physical     │     │
│  │ Vulnerabilities │  │  Security   │  │ Vulnerabilities │     │
│  │  (127 items)    │  │ Management  │  │   (9 items)     │     │
│  │                 │  │   System    │  │                 │     │
│  │Policy/Org/Asset │  │  ┌───────┐  │  │ Protected area  │     │
│  │HR/Access/Ops   │  │  │Unified│  │  │ Access/CCTV    │     │
│  │Incident/BCP    │  │  │Security│  │  │ Environment    │     │
│  │                 │  │  └───────┘  │  │                 │     │
│  └─────────────────┘  └─────────────┘  └─────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Category | Item Code | Items | Assessment Method |
|----------|-----------|:-----:|-------------------|
| **Technical** | U, W, WS, S, N, C, PC, D, M, V, CL | ~424 | System inspection, Scripts |
| **Administrative** | A | 127 | Document review, Interviews |
| **Physical** | B | 9 | On-site inspection |

### Technical Vulnerability Classification

Technical vulnerabilities are subdivided by system type:

| Code | Target System | Items | Key Inspection Areas |
|:----:|---------------|:-----:|---------------------|
| U | Unix/Linux servers | 68 | Accounts, File permissions, Services, Patches |
| W | Windows servers | 73 | Accounts, Services, Patches, Security settings |
| WS | Web services | 47 | Apache, Nginx configuration |
| S | Security equipment | 19 | Firewall, IDS/IPS |
| N | Network equipment | 40 | Routers, Switches |
| C | Control systems | 45 | SCADA, PLC |
| PC | PC/Terminals | 18 | Endpoint security |
| D | DBMS | 32 | Oracle, MySQL, MSSQL |
| M | Mobile communications | 2 | Mobile infrastructure |
| V | Virtualization equipment | 36 | VMware, Hyper-V |
| CL | Cloud | 14 | AWS, Azure, GCP |

### Administrative Vulnerability Classification

Administrative vulnerabilities consist of 14 domains:

| Domain | Item Code | Key Inspection Content |
|--------|-----------|------------------------|
| Information security policy | A-1 ~ A-7 | Policy establishment, approval, distribution |
| Information security organization | A-8 ~ A-9 | Dedicated organization, Committee |
| Asset classification | A-10 ~ A-14 | Asset identification, Classification |
| Risk management | A-15 ~ A-17 | Risk assessment, Protection measures |
| Audit | A-18 ~ A-20 | Regular audit, Follow-up |
| HR security | A-21 ~ A-26 | Hiring, Termination, Discipline |
| Third-party security | A-27 ~ A-33 | Outsourcing, Service management |
| Education and training | A-34 ~ A-38 | Security training, Awareness |
| Authentication and authorization | A-39 ~ A-42 | Accounts, Password policy |
| Access control | A-43 ~ A-55 | Network, System access |
| Operations management | A-56 ~ A-93 | Change, Backup, Log management |
| Security management | A-94 ~ A-113 | Encryption, Malware response |
| Incident response | A-114 ~ A-121 | Security incident response system |
| Business continuity | A-122 ~ A-127 | BCP, DR |

### Physical Vulnerability Classification

Physical vulnerabilities consist of 1 domain with 9 items:

| Domain | Item Code | Key Inspection Content |
|--------|-----------|------------------------|
| Physical security | B-1 ~ B-9 | Protected areas, Access control, CCTV |

---

## 2-5. Judgment Criteria (Good/Partial/Vulnerable)

### Three-Level Judgment System

Each inspection item is judged as one of the following three levels:

| Judgment | Meaning | Action Required |
|:--------:|---------|:---------------:|
| **Good** | Clearly meets inspection criteria | Not required |
| **Partial Compliance** | Partially meets, improvement elements exist | Required |
| **Vulnerable** | Does not meet inspection criteria | Immediately required |

### Considerations for Judgment

> **TIP**
> Judgment criteria are general recommendations. Actual judgments should comprehensively consider each infrastructure's policies, operational conditions, and risk acceptance levels.

1. **Existence of compensating controls**: Items judged vulnerable may be assessed as Good if there are valid security measures and justification
2. **Business environment specificity**: Consider industry-specific unique requirements
3. **Risk acceptance decisions**: Document justification when deciding to accept risks

### Severity Classification

Technical vulnerability items are classified as High/Medium/Low based on severity:

| Severity | Meaning | Action Priority |
|:--------:|---------|:---------------:|
| **High** | Severe impact if compromised | Immediate action |
| **Medium** | Moderate impact if compromised | Short-term action |
| **Low** | Minor impact if compromised | Medium to long-term action |

### Judgment Examples

#### Example 1: U-01 Restrict Remote Access to root Account

| Judgment | Situation |
|:--------:|-----------|
| Good | Direct remote access to root account is blocked |
| Vulnerable | SSH remote access using root account is possible |

#### Example 2: A-1 Information Security Policy Establishment

| Judgment | Situation |
|:--------:|-----------|
| Good | Information security policy is established and approved by management |
| Partial Compliance | Policy exists but no management approval record |
| Vulnerable | Information security policy is not established |

---

## Summary

- Under **Article 9** of the "Act on the Protection of Information and Communications Infrastructure," CII managing organizations must conduct vulnerability analysis and assessment **at least annually**.
- Assessment can be performed through **self-assessment**, **KISA delegation**, or **specialized company delegation**.
- Assessment items are categorized into **Technical** (~424), **Administrative** (127), and **Physical** (9) domains.
- Judgments are made on a **Good/Partial/Vulnerable** three-level scale, comprehensively considering each organization's circumstances.

---

*Next Chapter: Chapter 3. Unix/Linux Server Assessment*


---

# Chapter 3. Unix/Linux Server Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Unix/Linux servers are core infrastructure for Critical Information Infrastructure. This chapter covers 68 assessment items (U-01 ~ U-68) divided into 5 domains.

```
┌─────────────────────────────────────────────────────────────────┐
│           Unix/Linux Server Vulnerability Assessment Domains     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │   Account   │   │  File/Dir   │   │   Service   │          │
│   │ Management  │   │ Management  │   │ Management  │          │
│   │  U-01~U-13  │   │  U-14~U-33  │   │  U-34~U-63  │          │
│   │   (13)      │   │   (20)      │   │   (30)      │          │
│   │             │   │             │   │             │          │
│   │ • root      │   │ • Permissions│  │ • Unnecessary│         │
│   │   access    │   │ • SUID/SGID │   │   services  │          │
│   │ • Password  │   │ • Ownership │   │ • SNMP      │          │
│   │ • Lockout   │   │             │   │   security  │          │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘          │
│          │                 │                 │                  │
│          └────────────────┬┴─────────────────┘                  │
│                           │                                      │
│          ┌────────────────┴────────────────┐                    │
│          ▼                                 ▼                    │
│   ┌─────────────┐                   ┌─────────────┐            │
│   │   Patch     │                   │    Log      │            │
│   │ Management  │                   │ Management  │            │
│   │    U-64     │                   │  U-65~U-68  │            │
│   │    (1)      │                   │    (4)      │            │
│   │             │                   │             │            │
│   │ • Security  │                   │ • Log config│            │
│   │   patches   │                   │ • Retention │            │
│   └─────────────┘                   └─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | U-01 ~ U-13 | 13 |
| File and Directory Management | U-14 ~ U-33 | 20 |
| Service Management | U-34 ~ U-63 | 30 |
| Patch Management | U-64 | 1 |
| Log Management | U-65 ~ U-68 | 4 |

---

## 3-1. Account Management (U-01 ~ U-13)

Account management is the first line of defense for server security. Improper account management is a major cause of unauthorized access.

### U-01. Restrict Remote Access to root Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access by restricting direct remote access to root account |
| **Criteria** | Good: Direct root access blocked / Vulnerable: Direct root access allowed |

#### Assessment Method

```bash
# Check SSH configuration
cat /etc/ssh/sshd_config | grep -i "PermitRootLogin"

# Check Telnet usage (not recommended)
cat /etc/securetty
```

#### Remediation

```bash
# Edit /etc/ssh/sshd_config
PermitRootLogin no

# Restart SSH service
systemctl restart sshd
```

> **TIP**
> When root access is needed, connect with a regular account first and use `su -` or `sudo`.

---

### U-02. Configure Password Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Enforce password complexity and periodic changes |
| **Criteria** | Good: Policy configured / Vulnerable: Policy not configured |

#### Assessment Method

```bash
# Check password policy
cat /etc/login.defs | grep -E "PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_MIN_LEN|PASS_WARN_AGE"

# Check PAM configuration (RHEL/CentOS)
cat /etc/pam.d/system-auth | grep pam_pwquality
```

#### Recommended Settings

| Item | Recommended | Description |
|------|:-----------:|-------------|
| PASS_MAX_DAYS | 90 | Maximum password age |
| PASS_MIN_DAYS | 1 | Minimum password age |
| PASS_MIN_LEN | 8 | Minimum length |
| PASS_WARN_AGE | 7 | Warning days before expiry |

#### Remediation

```bash
# Edit /etc/login.defs
PASS_MAX_DAYS   90
PASS_MIN_DAYS   1
PASS_MIN_LEN    8
PASS_WARN_AGE   7
```

---

### U-03. Configure Account Lockout Threshold

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent brute force attacks |
| **Criteria** | Good: Set to 5 or less / Vulnerable: Not configured or exceeded |

#### Assessment Method

```bash
# Check PAM configuration
cat /etc/pam.d/system-auth | grep pam_tally2
# or
cat /etc/pam.d/system-auth | grep pam_faillock
```

#### Remediation

```bash
# /etc/pam.d/system-auth (RHEL 7 and later)
auth required pam_faillock.so preauth silent deny=5 unlock_time=600
auth required pam_faillock.so authfail deny=5 unlock_time=600
```

> **WARNING**
> Be careful with `even_deny_root` option to prevent locking out the root account.

---

### U-04. Password File Protection

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Protect password hashes using Shadow passwords |
| **Criteria** | Good: Shadow used / Vulnerable: Passwords stored in passwd |

#### Assessment Method

```bash
# Check second field in /etc/passwd
cat /etc/passwd | awk -F: '{print $1":"$2}'
# 'x' indicates shadow is in use
```

---

### U-05. Prohibit UID '0' for Non-root Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Detect unauthorized accounts with root privileges |
| **Criteria** | Good: Only root has UID 0 / Vulnerable: Other accounts have UID 0 |

#### Assessment Method

```bash
# Check accounts with UID 0
awk -F: '$3==0 {print $1}' /etc/passwd
```

#### Remediation

Delete or change UID for any non-root accounts with UID 0.

---

### U-06. Restrict su Command Access

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Restrict su command usage to specific groups |
| **Criteria** | Good: Only wheel group can use su / Vulnerable: No restrictions |

#### Assessment Method

```bash
# Check PAM configuration
cat /etc/pam.d/su | grep pam_wheel
```

#### Remediation

```bash
# Edit /etc/pam.d/su (uncomment)
auth required pam_wheel.so use_uid

# Add user to wheel group
usermod -aG wheel [username]
```

---

### U-07 ~ U-13. Other Account Management Items

| Code | Item | Severity | Key Check |
|------|------|:--------:|-----------|
| U-07 | Remove unnecessary accounts | Low | Unused accounts in `/etc/passwd` |
| U-08 | Minimize admin group members | Medium | wheel/root group members |
| U-09 | Prohibit GID without accounts | Low | `/etc/group` integrity |
| U-10 | Prohibit duplicate UIDs | Medium | Check for duplicate UIDs |
| U-11 | User shell verification | Low | Unnecessary accounts `/sbin/nologin` |
| U-12 | Session timeout configuration | Low | TMOUT environment variable |
| U-13 | Secure password encryption algorithm | Medium | SHA-512 recommended |

---

## 3-2. File and Directory Management (U-14 ~ U-33)

File permission management is key to protecting system integrity.

### U-14. root Home and PATH Directory Permissions

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent '.' in PATH environment variable |
| **Criteria** | Good: PATH without '.' / Vulnerable: '.' included |

#### Assessment Method

```bash
# Check PATH environment variable
echo $PATH | grep -E "^\.|:\.|:$"

# Check root profile
cat /root/.bash_profile | grep PATH
```

> **WARNING**
> Including current directory (`.`) in PATH risks executing malicious programs.

---

### U-16 ~ U-22. Key System File Permissions

| Code | Target File | Recommended | Owner |
|------|------------|:-----------:|:-----:|
| U-16 | /etc/passwd | 644 | root |
| U-18 | /etc/shadow | 400 | root |
| U-19 | /etc/hosts | 600 | root |
| U-20 | /etc/(x)inetd.conf | 600 | root |
| U-21 | /etc/(r)syslog.conf | 640 | root |
| U-22 | /etc/services | 644 | root |

#### Batch Assessment Script

```bash
#!/bin/bash
# Key file permission check

FILES=(
    "/etc/passwd:644:root"
    "/etc/shadow:400:root"
    "/etc/hosts:600:root"
    "/etc/services:644:root"
)

for item in "${FILES[@]}"; do
    IFS=':' read -r file perm owner <<< "$item"
    if [ -f "$file" ]; then
        actual_perm=$(stat -c "%a" "$file")
        actual_owner=$(stat -c "%U" "$file")
        if [ "$actual_perm" -le "$perm" ] && [ "$actual_owner" == "$owner" ]; then
            echo "[Good] $file (Permission: $actual_perm, Owner: $actual_owner)"
        else
            echo "[Vulnerable] $file (Permission: $actual_perm, Owner: $actual_owner)"
        fi
    fi
done
```

---

### U-23. SUID, SGID, Sticky Bit File Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent privilege escalation through unnecessary SUID/SGID files |

#### Assessment Method

```bash
# Find SUID files
find / -perm -4000 -type f 2>/dev/null

# Find SGID files
find / -perm -2000 -type f 2>/dev/null

# Find SUID + SGID files
find / -perm -6000 -type f 2>/dev/null
```

#### Key SUID Files to Check

| File | Required | Action |
|------|:--------:|--------|
| /usr/bin/passwd | Yes | Maintain |
| /usr/bin/su | Yes | Maintain |
| /usr/bin/chsh | Review | Remove if unnecessary |
| /usr/bin/newgrp | Review | Remove if unnecessary |

---

### U-25. World Writable File Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Detect files writable by all users |

#### Assessment Method

```bash
# Find world writable files
find / -perm -2 -type f 2>/dev/null

# Find world writable directories (without sticky bit)
find / -perm -2 -type d ! -perm -1000 2>/dev/null
```

---

## 3-3. Service Management (U-34 ~ U-63)

Unnecessary services increase the attack surface. Run only essential services.

### U-34. Disable Finger Service

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent user information disclosure |
| **Criteria** | Good: Disabled / Vulnerable: Enabled |

#### Assessment Method

```bash
# Check Finger service
systemctl status finger 2>/dev/null
# or
chkconfig --list finger 2>/dev/null
```

---

### U-36. Disable r-series Services

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block remote access without authentication |
| **Target Services** | rsh, rlogin, rexec |

#### Assessment Method

```bash
# Check r-series services
systemctl status rsh.socket rlogin.socket rexec.socket 2>/dev/null

# Check inetd/xinetd configuration
cat /etc/xinetd.d/rsh 2>/dev/null | grep disable
```

> **WARNING**
> r-series services use unencrypted communication. Replace with SSH.

---

### U-52. Disable Telnet Service

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Block plaintext communication services |
| **Criteria** | Good: Disabled or SSH used / Vulnerable: Telnet enabled |

#### Assessment Method

```bash
# Check Telnet service
systemctl status telnet.socket 2>/dev/null

# Check port
netstat -tlnp | grep :23
```

---

### U-58 ~ U-61. SNMP Security

| Code | Item | Severity |
|------|------|:--------:|
| U-58 | Check unnecessary SNMP service | Medium |
| U-59 | Use secure SNMP version | High |
| U-60 | SNMP Community String complexity | Medium |
| U-61 | SNMP Access Control configuration | High |

#### Assessment Method

```bash
# Check SNMP service
systemctl status snmpd

# Check Community String
cat /etc/snmp/snmpd.conf | grep -i community
```

> **TIP**
> Use SNMP v3 and always change default Community Strings (public, private).

---

## 3-4. Patch Management (U-64)

### U-64. Apply Regular Security Patches and Vendor Recommendations

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Apply patches for known vulnerabilities |
| **Criteria** | Good: Latest patches applied / Vulnerable: Not applied |

#### Assessment Method

```bash
# RHEL/CentOS
yum check-update

# Ubuntu/Debian
apt list --upgradable

# Check kernel version
uname -r
```

#### Remediation

```bash
# RHEL/CentOS
yum update -y

# Ubuntu/Debian
apt update && apt upgrade -y
```

> **WARNING**
> In production environments, verify patches in test environments before applying.

---

## 3-5. Log Management (U-65 ~ U-68)

### U-65. Log Policy Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Appropriate log recording and retention |

#### Assessment Method

```bash
# Check syslog configuration
cat /etc/rsyslog.conf

# Check key log file existence
ls -la /var/log/messages /var/log/secure /var/log/wtmp
```

### U-66. Log Management per Policy

| Log File | Content | Recommended Retention |
|----------|---------|:--------------------:|
| /var/log/messages | System messages | 6 months |
| /var/log/secure | Authentication logs | 6 months |
| /var/log/wtmp | Login records | 6 months |
| /var/log/btmp | Failed logins | 6 months |

---

## 3-6. Automation Scripts

### Integrated Assessment Script

Below is a Bash script that automatically checks key items.

```bash
#!/bin/bash
#===============================================
# KESE KIT - Unix/Linux Server Vulnerability Auto-Check
# Version: 1.0
#===============================================

REPORT_FILE="unix_check_$(date +%Y%m%d_%H%M%S).txt"

echo "=============================================" | tee $REPORT_FILE
echo "KESE KIT Unix/Linux Vulnerability Check Results" | tee -a $REPORT_FILE
echo "Check Date: $(date)" | tee -a $REPORT_FILE
echo "Hostname: $(hostname)" | tee -a $REPORT_FILE
echo "=============================================" | tee -a $REPORT_FILE

# U-01: root remote access restriction
echo -e "\n[U-01] root Remote Access Restriction" | tee -a $REPORT_FILE
SSH_ROOT=$(grep -i "^PermitRootLogin" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
if [ "$SSH_ROOT" == "no" ]; then
    echo "  [Good] PermitRootLogin = no" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] PermitRootLogin = $SSH_ROOT" | tee -a $REPORT_FILE
fi

# U-04: Password file protection
echo -e "\n[U-04] Password File Protection (Shadow Usage)" | tee -a $REPORT_FILE
SHADOW_CHECK=$(awk -F: '$2!="x" && $2!="*" && $2!="!!" {print $1}' /etc/passwd)
if [ -z "$SHADOW_CHECK" ]; then
    echo "  [Good] Shadow password in use" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Accounts not using Shadow: $SHADOW_CHECK" | tee -a $REPORT_FILE
fi

# U-05: Non-root UID 0 accounts
echo -e "\n[U-05] Non-root UID 0 Accounts" | tee -a $REPORT_FILE
UID_ZERO=$(awk -F: '$3==0 && $1!="root" {print $1}' /etc/passwd)
if [ -z "$UID_ZERO" ]; then
    echo "  [Good] Only root has UID 0" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] UID 0 accounts: $UID_ZERO" | tee -a $REPORT_FILE
fi

# U-16: /etc/passwd permission
echo -e "\n[U-16] /etc/passwd Permission" | tee -a $REPORT_FILE
PASSWD_PERM=$(stat -c "%a" /etc/passwd)
if [ "$PASSWD_PERM" -le "644" ]; then
    echo "  [Good] Permission: $PASSWD_PERM" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Permission: $PASSWD_PERM (644 or less recommended)" | tee -a $REPORT_FILE
fi

# U-18: /etc/shadow permission
echo -e "\n[U-18] /etc/shadow Permission" | tee -a $REPORT_FILE
SHADOW_PERM=$(stat -c "%a" /etc/shadow)
if [ "$SHADOW_PERM" -le "400" ]; then
    echo "  [Good] Permission: $SHADOW_PERM" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Permission: $SHADOW_PERM (400 or less recommended)" | tee -a $REPORT_FILE
fi

# U-52: Telnet service
echo -e "\n[U-52] Telnet Service" | tee -a $REPORT_FILE
TELNET_CHECK=$(systemctl is-active telnet.socket 2>/dev/null)
if [ "$TELNET_CHECK" != "active" ]; then
    echo "  [Good] Telnet disabled" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Telnet enabled" | tee -a $REPORT_FILE
fi

echo -e "\n=============================================" | tee -a $REPORT_FILE
echo "Check complete. Results file: $REPORT_FILE" | tee -a $REPORT_FILE
```

### Script Usage

```bash
# Grant execution permission
chmod +x unix_check.sh

# Execute (root privileges required)
sudo ./unix_check.sh

# View results
cat unix_check_*.txt
```

> **TIP**
> Register this script in cron for periodic checks.
> ```
> # Run every Monday at 2 AM
> 0 2 * * 1 /path/to/unix_check.sh
> ```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | root remote access, password policy, account lockout | Highest |
| File Permissions | Key config file permissions, SUID/SGID | High |
| Service Management | Disable unnecessary services, SNMP security | High |
| Patch Management | Apply latest security patches | Highest |
| Log Management | Log configuration and retention | Medium |

---

*Next Chapter: Chapter 4. Windows Server Assessment*


---

# Chapter 4. Windows Server Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Windows servers are used in enterprise environments for various roles including Active Directory, file servers, and web servers. This chapter covers 73 assessment items (W-01 ~ W-73) divided into 5 domains.

```
┌─────────────────────────────────────────────────────────────────┐
│           Windows Server Vulnerability Assessment Domains (73)   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                Security Management (W-48~W-73, 26)          │ │
│  │   Firewall | Antivirus | Screen Saver | Registry | Perms   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▲                                   │
│        ┌─────────────────────┼─────────────────────┐            │
│        │                     │                     │            │
│  ┌─────┴─────┐        ┌─────┴─────┐        ┌─────┴─────┐       │
│  │  Account  │        │  Service  │        │    Log    │       │
│  │ Management│        │ Management│        │ Management│       │
│  │ W-01~W-14 │        │ W-15~W-39 │        │ W-42~W-47 │       │
│  │   (14)    │        │   (25)    │        │    (6)    │       │
│  │           │        │           │        │           │       │
│  │• Admin   │        │• Unnecessary│       │• Audit    │       │
│  │  rename  │        │  services │        │  policy   │       │
│  │• Guest   │        │• IIS check│        │• Log size │       │
│  │  disable │        │• Shared   │        │• Event    │       │
│  │• Lockout │        │  folders  │        │  logs     │       │
│  └───────────┘        └───────────┘        └───────────┘       │
│                              │                                   │
│                       ┌─────┴─────┐                             │
│                       │   Patch   │                             │
│                       │ Management│                             │
│                       │ W-40~W-41 │                             │
│                       │    (2)    │                             │
│                       │           │                             │
│                       │• Service  │                             │
│                       │  Pack     │                             │
│                       │• Security │                             │
│                       │  patches  │                             │
│                       └───────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | W-01 ~ W-14 | 14 |
| Service Management | W-15 ~ W-39 | 25 |
| Patch Management | W-40 ~ W-41 | 2 |
| Log Management | W-42 ~ W-47 | 6 |
| Security Management | W-48 ~ W-73 | 26 |

---

## 4-1. Account Management (W-01 ~ W-14)

### W-01. Rename Administrator Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent attacks targeting default admin account name |
| **Criteria** | Good: Name changed / Vulnerable: Default name used |

#### Assessment Method (PowerShell)

```powershell
# Check Administrator account
Get-LocalUser | Where-Object {$_.SID -like "*-500"}

# Or Command Prompt
net user administrator
```

#### Remediation

```powershell
# Rename account with PowerShell
Rename-LocalUser -Name "Administrator" -NewName "NewAdminName"

# Or via Local Security Policy
# secpol.msc > Local Policies > Security Options > Accounts: Rename administrator account
```

> **TIP**
> Choose an unpredictable name, but document it for management convenience.

---

### W-02. Disable Guest Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block anonymous access |
| **Criteria** | Good: Disabled / Vulnerable: Enabled |

#### Assessment Method

```powershell
# Check Guest account status
Get-LocalUser -Name "Guest" | Select-Object Name, Enabled
```

#### Remediation

```powershell
# Disable Guest account
Disable-LocalUser -Name "Guest"
```

---

### W-03. Remove Unnecessary Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access through unused accounts |

#### Assessment Method

```powershell
# List all local accounts
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Find accounts not logged in for 90+ days
$threshold = (Get-Date).AddDays(-90)
Get-LocalUser | Where-Object {$_.LastLogon -lt $threshold}
```

---

### W-04. Configure Password Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Enforce strong password usage |

#### Assessment Method

```powershell
# Check password policy
net accounts

# Or PowerShell
Get-ADDefaultDomainPasswordPolicy  # Domain environment
```

#### Recommended Settings

| Policy | Recommended |
|--------|:-----------:|
| Minimum password length | 8+ characters |
| Password complexity | Enabled |
| Maximum password age | 90 days |
| Minimum password age | 1 day |
| Password history | 12 |

#### Remediation

```powershell
# Configure via Local Security Policy (secpol.msc) or Group Policy (gpedit.msc)
# Computer Configuration > Windows Settings > Security Settings > Account Policies > Password Policy
```

---

### W-05. Configure Account Lockout Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent brute force attacks |

#### Assessment Method

```powershell
# Check account lockout policy
net accounts
```

#### Recommended Settings

| Policy | Recommended |
|--------|:-----------:|
| Account lockout threshold | 5 attempts |
| Account lockout duration | 30 minutes |
| Reset account lockout counter after | 30 minutes |

---

### W-06 ~ W-14. Other Account Management Items

| Code | Item | Severity | Key Check |
|------|------|:--------:|-----------|
| W-06 | Minimize admin group members | High | Administrators group members |
| W-07 | Local account management | Medium | Unnecessary local accounts |
| W-08 | Disable reversible encryption for passwords | Medium | Policy setting |
| W-09 | Restrict remote access for local accounts | Medium | UAC remote restriction |
| W-10 | Session timeout configuration | Low | Screen lock |
| W-11 | Don't display last logged on user | Low | Logon screen |
| W-12 | Display legal notice at logon | Low | Legal warning |
| W-13 | Don't allow anonymous enumeration of SAM accounts | High | Block anonymous enumeration |
| W-14 | Disable Remote Registry service | High | Remote Registry |

---

## 4-2. Service Management (W-15 ~ W-39)

### W-15. Disable Unnecessary Services

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Minimize attack surface |

#### Services Recommended for Disabling

| Service | Description | Disable |
|---------|-------------|:-------:|
| Telnet | Remote access (plaintext) | Yes |
| TFTP | File transfer (no auth) | Yes |
| FTP Publishing | FTP server | Review |
| Remote Registry | Remote registry access | Yes |
| Simple TCP/IP Services | Echo, Daytime, etc. | Yes |

#### Assessment Method

```powershell
# List running services
Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, DisplayName

# Check specific service status
Get-Service -Name "RemoteRegistry" | Select-Object Name, Status, StartType
```

#### Remediation

```powershell
# Stop and disable service
Stop-Service -Name "RemoteRegistry"
Set-Service -Name "RemoteRegistry" -StartupType Disabled
```

---

### W-20. IIS Service Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Disable unnecessary web server |

#### Assessment Method

```powershell
# Check if IIS is installed
Get-WindowsFeature -Name Web-Server

# IIS service status
Get-Service -Name "W3SVC"
```

---

### W-25. Shared Folder Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Remove unnecessary shares, verify permissions |

#### Assessment Method

```powershell
# List shared folders
Get-SmbShare

# Check administrative shares
Get-SmbShare | Where-Object {$_.Name -match '\$$'}

# Check share permissions
Get-SmbShareAccess -Name "ShareName"
```

> **WARNING**
> Administrative shares (C$, ADMIN$, etc.) are created by default for management. Remove if unnecessary, but review impact first.

---

## 4-3. Patch Management (W-40 ~ W-41)

### W-40. Apply Latest Service Pack

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Apply patches for known vulnerabilities |

#### Assessment Method

```powershell
# Check OS version and build
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber

# Check installed hotfixes
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

---

### W-41. Apply Latest Security Patches

#### Assessment Method

```powershell
# Check Windows Update history
Get-WindowsUpdateLog  # Windows 10/Server 2016 and later

# Or check for updates
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$Updates = $UpdateSearcher.Search("IsInstalled=0")
$Updates.Updates | Select-Object Title
```

---

## 4-4. Log Management (W-42 ~ W-47)

### W-42. Configure Log Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Record appropriate audit logs |

#### Recommended Audit Policies

| Policy | Success | Failure |
|--------|:-------:|:-------:|
| Audit account logon events | Yes | Yes |
| Audit account management | Yes | Yes |
| Audit logon events | Yes | Yes |
| Audit object access | Yes | Yes |
| Audit policy change | Yes | Yes |
| Audit system events | Yes | Yes |

#### Assessment Method

```powershell
# Check audit policy
auditpol /get /category:*
```

---

### W-43. Configure Log File Size

#### Recommended Settings

| Log | Max Size | Retention Policy |
|-----|:--------:|------------------|
| Application | 64MB+ | Overwrite as needed |
| Security | 128MB+ | Archive then overwrite |
| System | 64MB+ | Overwrite as needed |

#### Assessment Method

```powershell
# Check event log settings
Get-EventLog -List | Select-Object Log, MaximumKilobytes
```

---

## 4-5. Security Management (W-48 ~ W-73)

### W-48. Screen Saver Configuration

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Protect unattended terminals |

#### Recommended Settings

- Wait time: 10 minutes or less
- Password protect on resume: Enabled

---

### W-56. Windows Firewall Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Network access control |

#### Assessment Method

```powershell
# Check firewall status
Get-NetFirewallProfile | Select-Object Name, Enabled

# Check inbound rules
Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object Name, Action
```

---

### W-67. Use Updated Antivirus Software

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Malware defense |

#### Assessment Method

```powershell
# Check Windows Defender status
Get-MpComputerStatus | Select-Object AntivirusEnabled, AntispywareEnabled, RealTimeProtectionEnabled

# Check latest definition update
Get-MpComputerStatus | Select-Object AntivirusSignatureLastUpdated
```

---

## 4-6. PowerShell Assessment Script

### Integrated Assessment Script

```powershell
#===============================================
# KESE KIT - Windows Server Vulnerability Auto-Check
# Version: 1.0
#===============================================

$ReportFile = "windows_check_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

function Write-Report {
    param([string]$Message)
    Write-Host $Message
    Add-Content -Path $ReportFile -Value $Message
}

Write-Report "============================================="
Write-Report "KESE KIT Windows Vulnerability Check Results"
Write-Report "Check Date: $(Get-Date)"
Write-Report "Hostname: $env:COMPUTERNAME"
Write-Report "============================================="

# W-01: Administrator account name change
Write-Report "`n[W-01] Administrator Account Name Change"
$AdminUser = Get-LocalUser | Where-Object {$_.SID -like "*-500"}
if ($AdminUser.Name -ne "Administrator") {
    Write-Report "  [Good] Account renamed: $($AdminUser.Name)"
} else {
    Write-Report "  [Vulnerable] Using default account name"
}

# W-02: Guest account disabled
Write-Report "`n[W-02] Guest Account Disabled"
$GuestUser = Get-LocalUser -Name "Guest"
if ($GuestUser.Enabled -eq $false) {
    Write-Report "  [Good] Guest account disabled"
} else {
    Write-Report "  [Vulnerable] Guest account enabled"
}

# W-05: Account lockout policy
Write-Report "`n[W-05] Account Lockout Policy"
$NetAccounts = net accounts
$LockoutThreshold = ($NetAccounts | Select-String "Lockout threshold").ToString().Split(":")[1].Trim()
if ($LockoutThreshold -ne "Never" -and [int]$LockoutThreshold -le 5) {
    Write-Report "  [Good] Lockout threshold: $LockoutThreshold"
} else {
    Write-Report "  [Vulnerable] Lockout threshold: $LockoutThreshold (5 or less recommended)"
}

# W-14: Remote Registry service
Write-Report "`n[W-14] Remote Registry Service"
$RemoteReg = Get-Service -Name "RemoteRegistry" -ErrorAction SilentlyContinue
if ($RemoteReg.Status -ne "Running") {
    Write-Report "  [Good] Remote Registry disabled"
} else {
    Write-Report "  [Vulnerable] Remote Registry running"
}

# W-56: Windows Firewall
Write-Report "`n[W-56] Windows Firewall"
$Firewall = Get-NetFirewallProfile
$AllEnabled = ($Firewall | Where-Object {$_.Enabled -eq $true}).Count -eq 3
if ($AllEnabled) {
    Write-Report "  [Good] All firewall profiles enabled"
} else {
    Write-Report "  [Vulnerable] Some firewall profiles disabled"
}

# W-67: Antivirus software
Write-Report "`n[W-67] Antivirus Software"
try {
    $Defender = Get-MpComputerStatus
    if ($Defender.AntivirusEnabled) {
        Write-Report "  [Good] Windows Defender enabled"
    } else {
        Write-Report "  [Vulnerable] Windows Defender disabled"
    }
} catch {
    Write-Report "  [Info] Unable to check Windows Defender status"
}

Write-Report "`n============================================="
Write-Report "Check complete. Results file: $ReportFile"
```

### Script Usage

```powershell
# Run PowerShell as Administrator
# Set execution policy (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run script
.\windows_check.ps1

# View results
Get-Content .\windows_check_*.txt
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Administrator rename, Guest disable, lockout policy | Highest |
| Service Management | Disable unnecessary services, shared folder check | High |
| Patch Management | Apply latest security patches | Highest |
| Log Management | Audit policy configuration, log size | Medium |
| Security Management | Firewall, antivirus, screen saver | High |

---

*Next Chapter: Chapter 5. Web Service Assessment*


---

# Chapter 5. Web Service Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Web service assessment covers configuration checks for web server software like Apache and Nginx. This chapter covers 47 assessment items (WS-01 ~ WS-47) divided into 4 domains.

```
┌─────────────────────────────────────────────────────────────────┐
│          Web Service Vulnerability Assessment Domains (47)       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│               ┌─────────────────────────────┐                   │
│               │    Web Server (Apache/Nginx)         │                   │
│               └──────────────┬──────────────┘                   │
│                              │                                   │
│      ┌───────────────────────┼───────────────────────┐          │
│      │                       │                       │          │
│      ▼                       ▼                       ▼          │
│ ┌─────────┐           ┌─────────┐           ┌─────────┐        │
│ │ Account │           │ Service │           │ Security│        │
│ │  Mgmt   │           │  Mgmt   │           │ Settings│        │
│ │WS-01~05 │           │WS-06~30 │           │WS-31~43 │        │
│ │  (5)    │           │  (25)   │           │  (13)   │        │
│ │         │           │         │           │         │        │
│ │• Dedicated│         │• Dir    │           │• SSL/TLS│        │
│ │  account │          │  listing│           │• Security│       │
│ │• Shell   │          │  remove │           │  headers│        │
│ │  restrict│          │• Version│           │• Error  │        │
│ │• Perms   │          │  hide   │           │  pages  │        │
│ └────┬────┘           └────┬────┘           └────┬────┘        │
│      │                     │                     │              │
│      └─────────────────────┼─────────────────────┘              │
│                            ▼                                     │
│                    ┌─────────────┐                              │
│                    │ Patch/Log   │                              │
│                    │   Mgmt      │                              │
│                    │ WS-44~47   │                              │
│                    │   (4)      │                              │
│                    │            │                              │
│                    │• Latest    │                              │
│                    │  version   │                              │
│                    │• Log config│                              │
│                    └─────────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | WS-01 ~ WS-05 | 5 |
| Service Management | WS-06 ~ WS-30 | 25 |
| Security Settings | WS-31 ~ WS-43 | 13 |
| Patch and Log Management | WS-44 ~ WS-47 | 4 |

---

## 5-1. Account Management (WS-01 ~ WS-05)

### WS-01. Use Dedicated Web Service Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Verify web service runs with minimal privilege account |
| **Criteria** | Good: Dedicated account (www-data, apache, etc.) / Vulnerable: Running as root |

#### Assessment Method

```bash
# Check Apache process account
ps aux | grep httpd | grep -v grep
ps aux | grep apache2 | grep -v grep

# Check Nginx process account
ps aux | grep nginx | grep -v grep
```

#### Remediation (Apache)

```bash
# /etc/httpd/conf/httpd.conf or /etc/apache2/envvars
User www-data
Group www-data
```

#### Remediation (Nginx)

```bash
# /etc/nginx/nginx.conf
user www-data;
```

> **WARNING**
> Running a web server as root puts the entire system at risk if vulnerabilities are exploited.

---

### WS-02. Restrict Web Service Account Shell

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block interactive login for web service account |

#### Assessment Method

```bash
# Check web service account shell
grep -E "www-data|apache|nginx" /etc/passwd
```

#### Recommended Setting

```bash
# Set shell to nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

---

### WS-03 ~ WS-05. Other Account Management

| Code | Item | Severity |
|------|------|:--------:|
| WS-03 | Web service account home directory permissions | Medium |
| WS-04 | Web service configuration file permissions | High |
| WS-05 | Web service log file permissions | Medium |

---

## 5-2. Service Management (WS-06 ~ WS-30)

### WS-06. Disable Directory Listing

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent directory content disclosure |
| **Criteria** | Good: Disabled / Vulnerable: Enabled |

#### Assessment Method (Apache)

```bash
# Check for Indexes option in httpd.conf
grep -r "Options.*Indexes" /etc/httpd/
grep -r "Options.*Indexes" /etc/apache2/
```

#### Remediation (Apache)

```apache
# Remove Indexes option
<Directory /var/www/html>
    Options -Indexes +FollowSymLinks
</Directory>
```

#### Remediation (Nginx)

```nginx
# Set autoindex off
location / {
    autoindex off;
}
```

---

### WS-07. Hide Web Server Version Information

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent targeted attacks through server version disclosure |

#### Assessment Method

```bash
# Check HTTP headers
curl -I http://localhost

# Check Server header in response
# Example: Server: Apache/2.4.41 (Ubuntu)
```

#### Remediation (Apache)

```apache
# /etc/httpd/conf/httpd.conf
ServerTokens Prod
ServerSignature Off
```

#### Remediation (Nginx)

```nginx
# /etc/nginx/nginx.conf
server_tokens off;
```

---

### WS-10. Restrict Unnecessary HTTP Methods

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block dangerous methods like PUT, DELETE |

#### Assessment Method

```bash
# Check allowed methods with OPTIONS
curl -X OPTIONS -I http://localhost
```

#### Remediation (Apache)

```apache
<Directory /var/www/html>
    <LimitExcept GET POST>
        Require all denied
    </LimitExcept>
</Directory>
```

#### Remediation (Nginx)

```nginx
if ($request_method !~ ^(GET|POST|HEAD)$ ) {
    return 405;
}
```

---

### WS-15. Restrict Symbolic Link Usage

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent filesystem access through symbolic links |

#### Remediation (Apache)

```apache
<Directory /var/www/html>
    Options -FollowSymLinks
    # Or use SymLinksIfOwnerMatch
    Options +SymLinksIfOwnerMatch
</Directory>
```

---

### WS-20. Remove Default Pages/Documents

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent information disclosure through default installation pages |

#### Check Targets

- Apache default page (/var/www/html/index.html)
- Nginx default page
- Sample applications
- Manual directories (/manual/)

---

## 5-3. Security Settings (WS-31 ~ WS-43)

### WS-31. Customize Error Pages

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent system information disclosure through error messages |

#### Remediation (Apache)

```apache
# Custom error page configuration
ErrorDocument 400 /error/400.html
ErrorDocument 401 /error/401.html
ErrorDocument 403 /error/403.html
ErrorDocument 404 /error/404.html
ErrorDocument 500 /error/500.html
```

#### Remediation (Nginx)

```nginx
error_page 404 /404.html;
error_page 500 502 503 504 /50x.html;

location = /404.html {
    root /var/www/error;
    internal;
}
```

---

### WS-35. SSL/TLS Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Ensure secure encrypted communication |

#### Recommended Settings (Apache)

```apache
# Allow only modern protocols
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1

# Secure cipher suites
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384

# Server cipher suite preference
SSLHonorCipherOrder on
```

#### Recommended Settings (Nginx)

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
```

> **TIP**
> You can test SSL configuration at SSL Labs (https://www.ssllabs.com/ssltest/).

---

### WS-40. Configure HTTP Security Headers

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| X-Content-Type-Options | Prevent MIME sniffing | nosniff |
| X-Frame-Options | Prevent clickjacking | DENY or SAMEORIGIN |
| X-XSS-Protection | XSS filter | 1; mode=block |
| Strict-Transport-Security | Force HTTPS | max-age=31536000 |
| Content-Security-Policy | Restrict content sources | Configure per policy |

#### Remediation (Apache)

```apache
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

#### Remediation (Nginx)

```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## 5-4. Patch and Log Management (WS-44 ~ WS-47)

### WS-44. Use Latest Web Server Version

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Patch known vulnerabilities |

#### Assessment Method

```bash
# Check Apache version
httpd -v
apache2 -v

# Check Nginx version
nginx -v
```

---

### WS-46. Log Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Record access and error logs |

#### Recommended Log Format (Apache)

```apache
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
CustomLog /var/log/httpd/access_log combined
ErrorLog /var/log/httpd/error_log
LogLevel warn
```

#### Recommended Log Format (Nginx)

```nginx
log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_x_forwarded_for"';

access_log /var/log/nginx/access.log main;
error_log /var/log/nginx/error.log warn;
```

---

## Web Service Assessment Script

### Apache Assessment Script

```bash
#!/bin/bash
#===============================================
# KESE KIT - Apache Web Server Vulnerability Check
#===============================================

echo "===== Apache Web Server Check ====="
echo "Check Date: $(date)"

# WS-01: Check running account
echo -e "\n[WS-01] Web Service Running Account"
APACHE_USER=$(ps aux | grep -E "httpd|apache2" | grep -v grep | head -1 | awk '{print $1}')
if [ "$APACHE_USER" != "root" ]; then
    echo "  [Good] Running account: $APACHE_USER"
else
    echo "  [Vulnerable] Running as root"
fi

# WS-06: Directory listing
echo -e "\n[WS-06] Directory Listing"
if grep -rq "Options.*Indexes" /etc/httpd/ /etc/apache2/ 2>/dev/null; then
    echo "  [Vulnerable] Indexes option found"
else
    echo "  [Good] Directory listing disabled"
fi

# WS-07: Version information
echo -e "\n[WS-07] Server Version Information"
SERVER_HEADER=$(curl -sI http://localhost 2>/dev/null | grep -i "^Server:")
if echo "$SERVER_HEADER" | grep -qE "[0-9]+\.[0-9]+"; then
    echo "  [Vulnerable] Version exposed: $SERVER_HEADER"
else
    echo "  [Good] Version information hidden"
fi

echo -e "\n===== Check Complete ====="
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Dedicated account, shell restriction | Highest |
| Service Management | Directory listing, version hiding, method restriction | Highest |
| Security Settings | SSL/TLS, security headers | High |
| Patch/Log | Latest version, log configuration | High |

---

*Next Chapter: Chapter 6. Web Application Assessment*


---

# Chapter 6. Web Application Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Web application vulnerabilities are assessed based on OWASP Top 10. This chapter is especially important for those developing in **Vibe Coding** environments.

```
┌─────────────────────────────────────────────────────────────────┐
│              Web Application Security Vulnerability Domains      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │   User Input    │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Input     │    │   Auth/     │    │   Access    │         │
│  │ Validation  │    │  Session    │    │  Control    │         │
│  │             │    │ Management  │    │             │         │
│  │ ┌─────────┐│    │ ┌─────────┐│    │ ┌─────────┐│         │
│  │ │SQL Inj. ││    │ │ Session ││    │ │Vertical ││         │
│  │ └─────────┘│    │ └─────────┘│    │ │Privilege││         │
│  │ ┌─────────┐│    │ ┌─────────┐│    │ │Escalation│         │
│  │ │  XSS    ││    │ │Password ││    │ └─────────┘│         │
│  │ └─────────┘│    │ │Storage  ││    │ ┌─────────┐│         │
│  │ ┌─────────┐│    │ └─────────┘│    │ │Horizontal│         │
│  │ │  CSRF   ││    │ ┌─────────┐│    │ │Privilege││         │
│  │ └─────────┘│    │ │ Cookie  ││    │ │Escalation│         │
│  └─────────────┘    │ │Security ││    │ └─────────┘│         │
│         │           │ └─────────┘│    └─────────────┘         │
│         │           └─────────────┘           │               │
│         │                   │                 │               │
│         └───────────────────┼─────────────────┘               │
│                             ▼                                    │
│                    ┌─────────────────┐                          │
│                    │ Information     │                          │
│                    │ Disclosure      │                          │
│                    │                 │                          │
│                    │ • Error messages│                          │
│                    │ • Source comments│                         │
│                    │ • Version info  │                          │
│                    └─────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Key Vulnerabilities |
|--------|---------------------|
| Input Validation | SQL Injection, XSS, CSRF |
| Auth/Session Management | Session fixation, Cookie security |
| Access Control | Privilege bypass, Path manipulation |
| Information Disclosure | Error messages, Comments, Directories |

---

## 6-1. Input Validation (SQL Injection, XSS, CSRF)

### SQL Injection

| Item | Content |
|------|---------|
| **Severity** | High |
| **Risk Level** | OWASP Top 10 A03:2021 |
| **Impact** | Data leakage, modification, deletion, system compromise |

#### Vulnerable Code Example (Python)

```python
# Vulnerable: User input directly inserted into query
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# Attack example: username = "admin' OR '1'='1"
# Resulting query: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

#### Secure Code (Parameterized Query)

```python
# Secure: Using parameterized query
def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

#### Secure Methods by Framework

| Framework | Secure Method |
|-----------|---------------|
| Django | ORM usage, `filter()`, `get()` |
| Flask-SQLAlchemy | ORM usage, `query.filter_by()` |
| Node.js (mysql2) | Prepared Statements |
| Java (JDBC) | PreparedStatement |
| PHP (PDO) | Prepared Statements |

> **WARNING**
> Even when using ORM, be careful with `raw()` or direct SQL queries.

---

### XSS (Cross-Site Scripting)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Risk Level** | OWASP Top 10 A03:2021 |
| **Types** | Stored XSS, Reflected XSS, DOM XSS |

#### Vulnerable Code Example

```html
<!-- Vulnerable: User input directly output -->
<div>Welcome, <%= user.name %>!</div>

<!-- Attack example: name = "<script>alert('XSS')</script>" -->
```

#### Secure Code (HTML Escape)

```html
<!-- Secure: HTML escape applied -->
<div>Welcome, <%= escape(user.name) %>!</div>

<!-- Or use framework auto-escaping -->
<!-- Django: {{ user.name }} (auto-escape) -->
<!-- React: {user.name} (auto-escape) -->
```

#### XSS Defense Checklist

| Item | Defense Method |
|------|----------------|
| Escape on output | HTML Entity encoding |
| Content-Type setting | `text/html; charset=utf-8` |
| HttpOnly cookies | HttpOnly flag on session cookies |
| CSP header | Content-Security-Policy configuration |

---

### CSRF (Cross-Site Request Forgery)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Risk Level** | OWASP Top 10 A01:2021 |
| **Impact** | Unauthorized actions using user privileges |

#### Vulnerable Scenario

```html
<!-- On attacker's site -->
<img src="https://bank.com/transfer?to=attacker&amount=1000000" />
<!-- Automatic transfer if victim visits while logged in -->
```

#### Defense Method: CSRF Token

```html
<!-- Include CSRF token in form -->
<form method="POST" action="/transfer">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <input type="text" name="to" />
    <input type="number" name="amount" />
    <button type="submit">Transfer</button>
</form>
```

#### CSRF Defense by Framework

| Framework | Method |
|-----------|--------|
| Django | `{% csrf_token %}` |
| Flask | Flask-WTF extension |
| Spring | `_csrf.token` |
| Express | csurf middleware |

---

## 6-2. Authentication and Session Management

### Secure Session Management

| Item | Recommended Setting |
|------|---------------------|
| Session ID length | 128 bits or more |
| Session ID generation | Use cryptographic random |
| Session timeout | Within 30 minutes (critical systems) |
| Session regeneration after login | Required |

#### Session Cookie Security Settings

```python
# Django settings.py
SESSION_COOKIE_SECURE = True      # HTTPS only
SESSION_COOKIE_HTTPONLY = True    # Block JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF defense
SESSION_COOKIE_AGE = 1800         # 30 minutes
```

---

### Password Storage

| Method | Security | Recommended |
|--------|:--------:|:-----------:|
| Plaintext storage | Very vulnerable | No |
| MD5/SHA-1 | Vulnerable | No |
| SHA-256 (no salt) | Vulnerable | No |
| bcrypt/scrypt/Argon2 | Secure | Yes |

#### Secure Password Hashing (Python)

```python
import bcrypt

# Hash password
password = "user_password".encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# Verify password
if bcrypt.checkpw(password, hashed):
    print("Password match")
```

---

## 6-3. Access Control and Authorization Verification

### Vertical Privilege Escalation

| Item | Content |
|------|---------|
| **Description** | Regular user accessing admin functions |
| **Defense** | Server-side authorization verification required |

#### Vulnerable Code

```python
# Vulnerable: Admin page accessible by URL only
@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html')
```

#### Secure Code

```python
# Secure: Authorization verification added
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    return render_template('admin_users.html')
```

---

### Horizontal Privilege Escalation

| Item | Content |
|------|---------|
| **Description** | Accessing another user's data |
| **Defense** | Resource ownership verification |

#### Vulnerable Code

```python
# Vulnerable: Only checks user ID
@app.route('/user/<int:user_id>/profile')
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
```

#### Secure Code

```python
# Secure: Compare current user with requested user
@app.route('/user/<int:user_id>/profile')
@login_required
def user_profile(user_id):
    if current_user.id != user_id:
        abort(403)
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
```

---

## 6-4. Information Disclosure Prevention

### Error Message Management

| Environment | Error Display |
|-------------|---------------|
| Development | Detailed errors (for debugging) |
| Production | Generic error messages only |

#### Secure Error Handling (Django)

```python
# settings.py
DEBUG = False  # Production environment

# Custom error handlers
handler404 = 'myapp.views.custom_404'
handler500 = 'myapp.views.custom_500'
```

---

### Remove Comments and Unnecessary Information

| Remove Target | Risk |
|---------------|------|
| Developer notes in HTML comments | Logic disclosure |
| Commented-out code | Feature disclosure |
| Version information | Vulnerability identification |
| Test account information | Unauthorized access |

---

## 6-5. Security in Vibe Coding Environments

### AI Code Generation Security Checklist

Code generated by Vibe Coding (AI-based coding) requires security review.

| Review Item | Check For |
|-------------|-----------|
| SQL queries | Parameterized query usage |
| User input | Validation/escaping |
| Auth/permissions | Server-side verification |
| Sensitive info | Hardcoding |
| Dependencies | Known vulnerabilities |

### AI Prompt Security Guide

```
# Secure prompt example
"Create a user login function.
Use parameterized queries to prevent SQL Injection,
hash passwords with bcrypt,
and apply CSRF tokens."
```

> **TIP**
> Never deploy AI-generated code to production without security review.

---

### Security Automation Tools

| Tool | Purpose | Type |
|------|---------|------|
| Bandit | Python static analysis | SAST |
| ESLint (security) | JavaScript static analysis | SAST |
| OWASP ZAP | Dynamic analysis | DAST |
| npm audit | Dependency vulnerabilities | SCA |
| pip-audit | Python dependencies | SCA |

#### Usage Examples

```bash
# Python code security analysis
pip install bandit
bandit -r ./src

# JavaScript dependency vulnerability check
npm audit

# Python dependency vulnerability check
pip install pip-audit
pip-audit
```

---

## Web Application Security Testing Script

### Basic Vulnerability Testing

```python
#!/usr/bin/env python3
"""
KESE KIT - Web Application Basic Security Test
"""

import requests
import sys

def test_sql_injection(url, param):
    """SQL Injection basic test"""
    payloads = ["'", "' OR '1'='1", "1; DROP TABLE users--"]

    for payload in payloads:
        try:
            response = requests.get(url, params={param: payload}, timeout=5)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                print(f"[Vulnerable] SQL Injection possible: {payload}")
                return True
        except:
            pass

    print("[Good] SQL Injection basic test passed")
    return False

def test_xss(url, param):
    """XSS basic test"""
    payload = "<script>alert('XSS')</script>"

    try:
        response = requests.get(url, params={param: payload}, timeout=5)
        if payload in response.text:
            print(f"[Vulnerable] XSS possible: Script reflected as-is")
            return True
    except:
        pass

    print("[Good] XSS basic test passed")
    return False

def test_security_headers(url):
    """Security headers test"""
    headers_to_check = [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection",
        "Strict-Transport-Security",
        "Content-Security-Policy"
    ]

    try:
        response = requests.get(url, timeout=5)
        missing = []

        for header in headers_to_check:
            if header not in response.headers:
                missing.append(header)

        if missing:
            print(f"[Vulnerable] Missing security headers: {', '.join(missing)}")
        else:
            print("[Good] All security headers configured")

    except Exception as e:
        print(f"[Error] Test failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_security_test.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    print(f"===== Web Security Basic Test: {target_url} =====\n")

    test_security_headers(target_url)
```

---

## Summary

| Domain | Key Defense | Priority |
|--------|-------------|:--------:|
| SQL Injection | Parameterized queries, ORM | Highest |
| XSS | Output escaping, CSP | Highest |
| CSRF | CSRF tokens | High |
| Auth/Session | Secure session management, bcrypt | Highest |
| Access Control | Server-side authorization verification | High |
| Information Disclosure | Error message management | Medium |

---

## Vibe Coding Security Summary

1. **Review AI-generated code**: Always review from security perspective
2. **Input validation**: Never trust any user input
3. **Output encoding**: Context-specific encoding for HTML, SQL, JavaScript
4. **Dependency management**: Regular vulnerability scanning
5. **Automation tool usage**: Integrate SAST, DAST tools in CI/CD

---

*Next Chapter: Chapter 7. Database (DBMS) Assessment*


---

# Chapter 7. Database (DBMS) Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

DBMS is a critical asset that stores organizational core data. This chapter covers 32 assessment items (D-01 ~ D-32).

```
┌─────────────────────────────────────────────────────────────────┐
│            DBMS Vulnerability Assessment Domains (32 items)      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│       ┌─────────────────────────────────────────────────┐       │
│       │              Supported DBMS Platforms           │       │
│       │  Oracle | MySQL | MSSQL | PostgreSQL | MariaDB  │       │
│       └───────────────────────┬─────────────────────────┘       │
│                               │                                  │
│       ┌───────────────────────┼───────────────────────┐         │
│       │                       │                       │         │
│       ▼                       ▼                       ▼         │
│ ┌───────────┐          ┌───────────┐          ┌───────────┐    │
│ │  Account  │          │  Access   │          │  Option   │    │
│ │ Management│          │ Management│          │ Management│    │
│ │ D-01~D-16 │          │ D-17~D-23 │          │ D-24~D-30 │    │
│ │   (16)    │          │   (7)     │          │   (7)     │    │
│ │           │          │           │          │           │    │
│ │• Default  │          │• Remote   │          │• Security │    │
│ │  accounts │          │  access   │          │  params   │    │
│ │• Password │          │  restrict │          │• Audit    │    │
│ │  policy   │          │• Least    │          │  settings │    │
│ │• Unused   │          │  privilege│          │           │    │
│ │  accounts │          │           │          │           │    │
│ └─────┬─────┘          └─────┬─────┘          └─────┬─────┘    │
│       │                      │                      │           │
│       └──────────────────────┼──────────────────────┘           │
│                              ▼                                   │
│                       ┌───────────┐                             │
│                       │   Patch   │                             │
│                       │ Management│                             │
│                       │ D-31~D-32 │                             │
│                       │   (2)     │                             │
│                       │• Security │                             │
│                       │  patches  │                             │
│                       └───────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | D-01 ~ D-16 | 16 |
| Access Management | D-17 ~ D-23 | 7 |
| Option Management | D-24 ~ D-30 | 7 |
| Patch Management | D-31 ~ D-32 | 2 |

---

## 7-1. Account Management (D-01 ~ D-16)

### D-01. Change Default Account Password

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target DB** | Oracle, MySQL, MSSQL, PostgreSQL |
| **Criteria** | Good: Default password changed / Vulnerable: Default used |

#### Default Account List

| DBMS | Default Account | Default Password |
|------|-----------------|------------------|
| Oracle | SYS, SYSTEM | change_on_install, manager |
| MySQL | root | (empty string) |
| MSSQL | sa | (set during installation) |
| PostgreSQL | postgres | (set during installation) |

#### Assessment Method (MySQL)

```sql
-- Check accounts without password
SELECT user, host FROM mysql.user WHERE authentication_string = '';
```

#### Assessment Method (Oracle)

```sql
-- Check accounts using default password
SELECT username, account_status FROM dba_users
WHERE username IN ('SYS', 'SYSTEM', 'DBSNMP', 'SCOTT');
```

---

### D-02. Remove Unnecessary Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access through unused accounts |

#### Assessment Method (MySQL)

```sql
-- Check all accounts
SELECT user, host, account_locked FROM mysql.user;
```

#### Assessment Method (Oracle)

```sql
-- Check account status
SELECT username, account_status, expiry_date, lock_date
FROM dba_users
ORDER BY username;
```

---

### D-05. Configure Password Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Recommended** | Complexity, length, expiration period |

#### MySQL Password Policy

```sql
-- Check password policy
SHOW VARIABLES LIKE 'validate_password%';

-- Configure policy
SET GLOBAL validate_password.length = 8;
SET GLOBAL validate_password.policy = MEDIUM;
```

#### Oracle Password Policy (Profile)

```sql
-- Create profile
CREATE PROFILE secure_profile LIMIT
    PASSWORD_LIFE_TIME 90
    PASSWORD_GRACE_TIME 7
    PASSWORD_REUSE_TIME 365
    PASSWORD_REUSE_MAX 12
    FAILED_LOGIN_ATTEMPTS 5
    PASSWORD_LOCK_TIME 1/24;

-- Apply profile
ALTER USER username PROFILE secure_profile;
```

---

## 7-2. Access Management (D-17 ~ D-23)

### D-17. Restrict Remote Access

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block unauthorized remote access |

#### MySQL Remote Access Restriction

```sql
-- Check accounts with remote access
SELECT user, host FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1');

-- Allow specific IP only
CREATE USER 'user'@'192.168.1.%' IDENTIFIED BY 'password';
```

#### PostgreSQL Access Control (pg_hba.conf)

```
# Allow local connections only
local   all   all                 md5
host    all   all   127.0.0.1/32  md5
# Allow specific network
host    all   all   192.168.1.0/24  md5
```

---

### D-19. Principle of Least Privilege

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Grant only minimum required privileges |

#### MySQL Permission Check

```sql
-- Check user privileges
SHOW GRANTS FOR 'username'@'host';

-- Full privilege status
SELECT * FROM mysql.user WHERE user = 'username'\G
```

> **WARNING**
> `GRANT ALL PRIVILEGES` violates least privilege principle. Grant only necessary permissions individually.

---

## 7-3. Option Management (D-24 ~ D-30)

### D-24. Configure Security-Related Parameters

#### Oracle Security Parameters

| Parameter | Recommended | Description |
|-----------|:-----------:|-------------|
| REMOTE_LOGIN_PASSWORDFILE | EXCLUSIVE | Remote password file |
| REMOTE_OS_AUTHENT | FALSE | Disable OS authentication |
| O7_DICTIONARY_ACCESSIBILITY | FALSE | Restrict data dictionary access |
| AUDIT_TRAIL | DB | Enable auditing |

#### MySQL Security Parameters

| Parameter | Recommended | Description |
|-----------|:-----------:|-------------|
| local_infile | OFF | Disable local file load |
| skip_symbolic_links | ON | Disable symbolic links |
| secure_file_priv | Specified path | Restrict file operations path |

---

## 7-4. Patch Management (D-31 ~ D-32)

### D-31. Apply Latest Security Patches

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Patch known vulnerabilities |

#### Version Check Methods

```sql
-- MySQL
SELECT VERSION();

-- Oracle
SELECT * FROM V$VERSION;

-- PostgreSQL
SELECT version();

-- MSSQL
SELECT @@VERSION;
```

---

## 7-5. DB Assessment Scripts

### MySQL Assessment Script

```bash
#!/bin/bash
# KESE KIT - MySQL Assessment Script

MYSQL_USER="root"
MYSQL_PASS="your_password"

echo "===== MySQL Security Assessment ====="

# D-01: Accounts with empty password
echo -e "\n[D-01] Accounts with Empty Password"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host FROM mysql.user WHERE authentication_string = '';" 2>/dev/null

# D-02: All accounts list
echo -e "\n[D-02] All Accounts List"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host, account_locked FROM mysql.user;" 2>/dev/null

# D-17: Accounts with remote access
echo -e "\n[D-17] Accounts with Remote Access"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1', '::1');" 2>/dev/null

echo -e "\n===== Assessment Complete ====="
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password change, remove unused accounts | Highest |
| Access Management | Remote access restriction, least privilege | Highest |
| Option Management | Security parameter settings | High |
| Patch Management | Apply latest patches | Highest |

---

*Next Chapter: Chapter 8. Network Equipment Assessment*


---

# Chapter 8. Network Equipment Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Network equipment (routers, switches) is the core of infrastructure. This chapter covers 40 assessment items (N-01 ~ N-40).

```
┌─────────────────────────────────────────────────────────────────┐
│        Network Equipment Vulnerability Assessment Domains (40)   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │Network Equipment│                          │
│                    │ Router | Switch │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│     ┌───────────────────────┼───────────────────────┐           │
│     │           │           │           │           │           │
│     ▼           ▼           ▼           ▼           ▼           │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐         │
│ │Account│  │ Access│  │ Patch │  │  Log  │  │Feature│         │
│ │ Mgmt  │  │ Mgmt  │  │ Mgmt  │  │ Mgmt  │  │ Mgmt  │         │
│ │N-01~10│  │N-11~18│  │ N-19  │  │N-20~24│  │N-25~40│         │
│ │ (10)  │  │  (8)  │  │  (1)  │  │  (5)  │  │ (16)  │         │
│ │       │  │       │  │       │  │       │  │       │         │
│ │•Default│ │• ACL  │  │• Firm-│  │• Sys- │  │• SNMP │         │
│ │ acct  │  │• SSH  │  │  ware │  │  log  │  │• CDP  │         │
│ │•Encrypt│ │•Telnet│  │       │  │• NTP  │  │•Unnec-│         │
│ │       │  │ block │  │       │  │       │  │ essary│         │
│ │       │  │       │  │       │  │       │  │ svc   │         │
│ └───────┘  └───────┘  └───────┘  └───────┘  └───────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | N-01 ~ N-10 | 10 |
| Access Management | N-11 ~ N-18 | 8 |
| Patch Management | N-19 | 1 |
| Log Management | N-20 ~ N-24 | 5 |
| Feature Management | N-25 ~ N-40 | 16 |

---

## 8-1. Account Management (N-01 ~ N-10)

### N-01. Change Default Account Password

| Item | Content |
|------|---------|
| **Severity** | High |
| **Criteria** | Good: Default password changed / Vulnerable: Default used |

#### Cisco Equipment Default Accounts

| Account | Default Password | Action |
|---------|------------------|--------|
| cisco | cisco | Change required |
| admin | admin | Change required |
| enable | (none) | Configuration required |

#### Remediation (Cisco IOS)

```
enable
configure terminal
username admin privilege 15 secret [strong_password]
enable secret [strong_password]
```

---

### N-04. Encrypt Stored Passwords

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent plaintext passwords in config files |

#### Assessment Method (Cisco)

```
show running-config | include password
# "password 7" or plaintext indicates vulnerability
```

#### Remediation

```
configure terminal
service password-encryption
# Use enable secret instead of enable password
enable secret [password]
```

---

## 8-2. Access Management (N-11 ~ N-18)

### N-11. Restrict Remote Access (ACL)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Allow access only from management networks |

#### Remediation (Cisco)

```
! Create management ACL
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 deny any log

! Apply to VTY lines
line vty 0 4
 access-class 10 in
 transport input ssh
```

---

### N-12. Use SSH (Disable Telnet)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Use encrypted management access |

#### Remediation (Cisco)

```
! Enable SSH
hostname Router1
ip domain-name example.com
crypto key generate rsa modulus 2048
ip ssh version 2

! Disable Telnet
line vty 0 4
 transport input ssh
```

---

## 8-3. Patch Management (N-19)

### N-19. Apply Latest Firmware

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Patch known vulnerabilities |

#### Version Check (Cisco)

```
show version
```

> **WARNING**
> Always backup current configuration before firmware upgrade.

---

## 8-4. Log Management (N-20 ~ N-24)

### N-20. Configure Logging

#### Remediation (Cisco)

```
! Syslog server configuration
logging host 192.168.1.100
logging trap informational
logging facility local7

! Add timestamps
service timestamps log datetime msec
```

---

## 8-5. Feature Management (N-25 ~ N-40)

### N-25. SNMP Security Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access via SNMP |

#### Remediation

```
! Delete default communities
no snmp-server community public
no snmp-server community private

! Use complex community or SNMPv3
snmp-server community [complex_string] RO 10
snmp-server group v3group v3 priv
snmp-server user v3user v3group v3 auth sha [auth_password] priv aes 256 [priv_password]
```

---

### N-30. Disable Unnecessary Services

#### Recommended to Disable

```
no ip http server
no ip http secure-server
no cdp run
no ip source-route
no service tcp-small-servers
no service udp-small-servers
no ip finger
no ip bootp server
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password, encrypted storage | Highest |
| Access Management | SSH usage, ACL configuration | Highest |
| Patch Management | Latest firmware | High |
| Log Management | Syslog configuration | Medium |
| Feature Management | SNMP security, disable unnecessary services | High |

---

*Next Chapter: Chapter 9. Security Equipment Assessment*


---

# Chapter 9. Security Equipment Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Security equipment (Firewall, IDS/IPS, WAF) is a core element of security. This chapter covers 19 assessment items (S-01 ~ S-19).

```
┌─────────────────────────────────────────────────────────────────┐
│        Security Equipment Vulnerability Assessment Domains (19)  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Security Equipment Types                  │ │
│  │                                                            │ │
│  │   ┌──────────┐    ┌──────────┐    ┌──────────┐           │ │
│  │   │ Firewall │    │ IDS/IPS  │    │   WAF    │           │ │
│  │   │          │    │Intrusion │    │   Web    │           │ │
│  │   │          │    │Detection/│    │Application│          │ │
│  │   │          │    │Prevention│    │ Firewall │           │ │
│  │   └────┬─────┘    └────┬─────┘    └────┬─────┘           │ │
│  │        │               │               │                  │ │
│  │        └───────────────┼───────────────┘                  │ │
│  │                        │                                  │ │
│  └────────────────────────┼──────────────────────────────────┘ │
│                           │                                     │
│           ┌───────────────┼───────────────┐                    │
│           │               │               │                    │
│           ▼               ▼               ▼                    │
│    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│    │Account/Access│ │ Patch/Log  │ │   Feature   │            │
│    │  Management │ │ Management │ │  Management │            │
│    │  S-01~S-08  │ │  S-09~S-12 │ │  S-13~S-19  │            │
│    │    (8)      │ │    (4)     │ │    (7)      │            │
│    │             │ │            │ │             │            │
│    │• Default    │ │• Firmware  │ │• Policy     │            │
│    │  accounts   │ │• Signature │ │  optimization│           │
│    │• Admin      │ │• Log       │ │• Ruleset    │            │
│    │  access     │ │  retention │ │  management │            │
│    └─────────────┘ └─────────────┘ └─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | S-01 ~ S-05 | 5 |
| Access Management | S-06 ~ S-08 | 3 |
| Patch Management | S-09 | 1 |
| Log Management | S-10 ~ S-12 | 3 |
| Feature Management | S-13 ~ S-19 | 7 |

---

## 9-1. Firewall Assessment (S-01 ~ S-19)

### S-01. Change Default Account Password

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | Firewall, IDS/IPS, UTM |
| **Criteria** | Good: Changed / Vulnerable: Default |

#### Key Security Equipment Default Accounts

| Equipment | Default Account | Action |
|-----------|-----------------|--------|
| Palo Alto | admin/admin | Change required |
| FortiGate | admin/(none) | Set password |
| Cisco ASA | - | Set enable password |

---

### S-06. Management Access Control

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Restrict management interface access |

#### Recommended Settings

- Separate management interface on isolated network
- Allow access only from specific IPs
- Use SSH or HTTPS (disable HTTP/Telnet)

---

### S-13. Policy Optimization

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Remove unnecessary allow policies |

#### Check Points

| Item | Check For |
|------|-----------|
| Any-Any policies | Source/destination is Any |
| Unused policies | Hit count is 0 |
| Duplicate policies | Same effect duplicated |
| Order issues | Broader policies above specific ones |

> **TIP**
> Regularly review policies and remove unused ones.

---

## 9-2. IDS/IPS Assessment

### Signature Updates

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Detect latest attack patterns |

#### Check Points

- Auto-update configuration
- Update frequency check (daily recommended)
- Last update date verification

---

## 9-3. WAF Assessment

### Web Attack Defense Settings

| Attack Type | Defense Setting |
|-------------|-----------------|
| SQL Injection | Detect/Block |
| XSS | Detect/Block |
| CSRF | Detect |
| File Inclusion | Detect/Block |
| Command Injection | Detect/Block |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password change | Highest |
| Access Management | Management interface restriction | Highest |
| Feature Management | Policy optimization, signature updates | High |

---

*Next Chapter: Chapter 10. Virtualization and Cloud Assessment*


---

# Chapter 10. Virtualization and Cloud Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Virtualization and cloud environments are core to modern infrastructure. This chapter covers Virtualization equipment (V-01 ~ V-36) and Cloud (CL-01 ~ CL-14) assessments.

```
┌─────────────────────────────────────────────────────────────────┐
│     Virtualization and Cloud Vulnerability Assessment (50)       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐    ┌────────────────────────┐      │
│  │   Virtualization Env   │    │      Cloud Env         │      │
│  │     V-01 ~ V-36        │    │     CL-01 ~ CL-14      │      │
│  │        (36)            │    │        (14)            │      │
│  └───────────┬────────────┘    └───────────┬────────────┘      │
│              │                              │                    │
│              ▼                              ▼                    │
│  ┌────────────────────────┐    ┌────────────────────────┐      │
│  │ • VMware vSphere       │    │ • AWS                  │      │
│  │ • Microsoft Hyper-V    │    │ • Microsoft Azure      │      │
│  │ • KVM/QEMU             │    │ • Google Cloud (GCP)   │      │
│  │ • Citrix Xen           │    │ • NHN Cloud / NCP      │      │
│  └───────────┬────────────┘    └───────────┬────────────┘      │
│              │                              │                    │
│              └──────────────┬───────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Common Assessment Domains                 │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │   │ Account │  │ Network │  │ Storage │  │Container│   │   │
│  │   │  Mgmt   │  │Isolation│  │Security │  │Security │   │   │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘   │   │
│  │                                                         │   │
│  │  • IAM Policy       • VLAN/VPC      • Encryption       │   │
│  │  • MFA              • Security Group • Block public    │   │
│  │  • Least privilege  • Firewall rules • Backup policy   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10-1. Virtualization Equipment (V-01 ~ V-36)

### V-01. Hypervisor Account Management

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | VMware vSphere, Hyper-V, KVM |
| **Purpose** | Hypervisor admin account security |

#### VMware vSphere Assessment

```powershell
# Check users with PowerCLI
Connect-VIServer -Server vcenter.example.com
Get-VIPermission | Select Principal, Role
```

---

### V-12. Virtual Network Segregation

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Network isolation between VMs |

#### Recommendations

- Separate VLAN/port groups by purpose
- Isolate management network
- Separate production/development environments

---

### V-25. Snapshot Management

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent performance degradation from snapshot accumulation |

#### Check Points

- Identify old snapshots (7+ days)
- Verify snapshot chain length

```powershell
# VMware snapshot check
Get-VM | Get-Snapshot | Select VM, Name, Created, SizeGB
```

---

## 10-2. Cloud Environment (CL-01 ~ CL-14)

### CL-01. IAM Account Management

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | AWS, Azure, GCP |
| **Purpose** | Cloud account and permission management |

#### AWS IAM Assessment

```bash
# Check unused accounts
aws iam generate-credential-report
aws iam get-credential-report --output text | base64 -d

# Check users without MFA
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
    mfa=$(aws iam list-mfa-devices --user-name $user --query 'MFADevices' --output text)
    if [ -z "$mfa" ]; then
        echo "No MFA: $user"
    fi
done
```

---

### CL-04. Principle of Least Privilege

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent excessive permission grants |

#### AWS Permission Assessment

```bash
# Users with AdministratorAccess policy
aws iam list-entities-for-policy \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

> **WARNING**
> Minimize AdministratorAccess and *:* permissions.

---

### CL-07. Storage Security

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block public access, encryption |

#### AWS S3 Bucket Assessment

```bash
# Check public buckets
aws s3api list-buckets --query 'Buckets[*].Name' --output text | while read bucket; do
    acl=$(aws s3api get-bucket-acl --bucket $bucket --query 'Grants[?Grantee.URI==`http://acs.amazonaws.com/groups/global/AllUsers`]' --output text)
    if [ -n "$acl" ]; then
        echo "Public bucket: $bucket"
    fi
done
```

---

## 10-3. Container Security (Docker, K8s)

### Docker Security Assessment

| Item | Check For |
|------|-----------|
| Image vulnerabilities | Base image vulnerability scan |
| Privileged execution | Prohibit --privileged flag |
| root execution | Use non-root user in container |
| Network | Prohibit unnecessary port exposure |

#### Docker Assessment Commands

```bash
# Check privileged mode containers
docker ps --quiet | xargs docker inspect --format '{{.Name}}: Privileged={{.HostConfig.Privileged}}'

# Containers running as root
docker ps --quiet | xargs docker inspect --format '{{.Name}}: User={{.Config.User}}'
```

### Kubernetes Security Assessment

```bash
# Check Pod Security
kubectl get pods --all-namespaces -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged==true) | .metadata.name'

# Check ServiceAccount permissions
kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[].kind=="ServiceAccount")'
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Virtualization | Hypervisor accounts, network segregation | Highest |
| Cloud | IAM, least privilege, storage security | Highest |
| Container | Image vulnerabilities, privilege restriction | High |

---

*Next Chapter: Chapter 11. PC and Endpoint Assessment*


---

# Chapter 11. PC and Endpoint Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

PCs and endpoints are the points of direct contact with users. This chapter covers 18 assessment items (PC-01 ~ PC-18).

```
┌─────────────────────────────────────────────────────────────────┐
│           PC/Endpoint Vulnerability Assessment Domains (18)      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │     User PC     │                          │
│                    │   (Endpoint)    │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│     ┌───────────────────────┼───────────────────────┐           │
│     │           │           │           │           │           │
│     ▼           ▼           ▼           ▼           ▼           │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐         │
│ │Account│  │ Access│  │ Patch │  │Security│ │ Data  │         │
│ │ Mgmt  │  │ Mgmt  │  │ Mgmt  │  │ Mgmt   │ │Protect│         │
│ │PC-01~4│  │PC-05~11│ │PC-12~13│ │PC-14~18│ │(Integ)│         │
│ │  (4)  │  │  (7)  │  │  (2)  │  │  (5)   │ │       │         │
│ │       │  │       │  │       │  │        │ │       │         │
│ │•Unnec-│  │•Shared│  │• OS   │  │•Anti-  │ │•Encrypt│        │
│ │ essary│  │ folder│  │ patch │  │ virus  │ │•DLP   │         │
│ │ acct  │  │• USB  │  │• App  │  │•Fire-  │ │       │         │
│ │•Screen│  │ block │  │ patch │  │ wall   │ │       │         │
│ │ saver │  │       │  │       │  │        │ │       │         │
│ └───────┘  └───────┘  └───────┘  └────────┘ └───────┘         │
│                             │                                    │
│                             ▼                                    │
│              ┌───────────────────────────┐                      │
│              │ Unified Endpoint Security │                      │
│              │    (EDR / MDM / NAC)      │                      │
│              └───────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | PC-01 ~ PC-04 | 4 |
| Access Management | PC-05 ~ PC-11 | 7 |
| Patch Management | PC-12 ~ PC-13 | 2 |
| Security Management | PC-14 ~ PC-18 | 5 |

---

## 11-1. Account Management (PC-01 ~ PC-04)

### PC-01. Remove Unnecessary Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access through unused accounts |

#### Assessment Method (Windows)

```powershell
# Check local accounts
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Verify Guest account is disabled
Get-LocalUser -Name "Guest" | Select-Object Enabled
```

---

### PC-03. Screen Saver Configuration

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Recommended** | Within 10 minutes, password protected |

#### Assessment Method (Windows Registry)

```powershell
# Check registry
Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" | Select-Object ScreenSaveActive, ScreenSaverIsSecure, ScreenSaveTimeOut
```

---

## 11-2. Access Management (PC-05 ~ PC-11)

### PC-05. Shared Folder Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Remove unnecessary shares |

#### Assessment Method

```powershell
# Check shared folders
Get-SmbShare | Select-Object Name, Path, Description

# Check shares accessible by Everyone
Get-SmbShareAccess -Name "ShareName" | Where-Object {$_.AccountName -eq "Everyone"}
```

---

### PC-08. Restrict Removable Storage Media

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent data leakage via USB |

#### Group Policy Configuration

```
Computer Configuration > Administrative Templates > System > Removable Storage Access
- Removable Disks: Deny read access
- Removable Disks: Deny write access
```

---

## 11-3. Patch Management (PC-12 ~ PC-13)

### PC-12. Operating System Patches

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Apply latest security patches |

#### Assessment Method

```powershell
# Check recently installed updates
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5

# Check pending updates
(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0").Updates | Select-Object Title
```

---

## 11-4. Security Management (PC-14 ~ PC-18)

### PC-14. Antivirus Installation and Updates

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Malware defense |

#### Assessment Method (Windows Defender)

```powershell
# Windows Defender status
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated
```

---

### PC-17. Personal Firewall Usage

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Network attack defense |

#### Assessment Method

```powershell
# Windows Firewall status
Get-NetFirewallProfile | Select-Object Name, Enabled
```

---

## PC Assessment Script

```powershell
#===============================================
# KESE KIT - PC Security Assessment Script
#===============================================

Write-Host "===== PC Security Assessment =====" -ForegroundColor Cyan

# PC-01: Guest account
Write-Host "`n[PC-01] Guest Account Status"
$guest = Get-LocalUser -Name "Guest"
if ($guest.Enabled) { Write-Host "  [Vulnerable] Guest enabled" -ForegroundColor Red }
else { Write-Host "  [Good] Guest disabled" -ForegroundColor Green }

# PC-05: Shared folders
Write-Host "`n[PC-05] Shared Folders"
Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | ForEach-Object {
    Write-Host "  Share: $($_.Name) - $($_.Path)"
}

# PC-14: Antivirus status
Write-Host "`n[PC-14] Antivirus Status"
$defender = Get-MpComputerStatus
if ($defender.AntivirusEnabled -and $defender.RealTimeProtectionEnabled) {
    Write-Host "  [Good] Windows Defender enabled" -ForegroundColor Green
} else {
    Write-Host "  [Vulnerable] Windows Defender disabled" -ForegroundColor Red
}

# PC-17: Firewall
Write-Host "`n[PC-17] Firewall Status"
$firewallEnabled = (Get-NetFirewallProfile | Where-Object {$_.Enabled -eq $true}).Count
if ($firewallEnabled -eq 3) {
    Write-Host "  [Good] All profiles enabled" -ForegroundColor Green
} else {
    Write-Host "  [Vulnerable] Some profiles disabled" -ForegroundColor Red
}

Write-Host "`n===== Assessment Complete =====" -ForegroundColor Cyan
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Unnecessary accounts, screen saver | High |
| Access Management | Shared folders, removable media | High |
| Patch Management | OS patches | Highest |
| Security Management | Antivirus, firewall | Highest |

---

*Next Chapter: Chapter 12. Control System (OT) Assessment*


---

# Chapter 12. Control System (OT) Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Control systems (OT, Operational Technology) control physical processes in power plants, factories, transportation, etc. They have unique characteristics different from IT systems and require separate assessment methods. This chapter covers 45 assessment items (C-01 ~ C-45).

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | C-01 ~ C-08 | 8 |
| Service Management | C-09 ~ C-14 | 6 |
| Patch Management | C-15 ~ C-18 | 4 |
| Network Access Control | C-19 ~ C-24 | 6 |
| Physical Access Control | C-25 ~ C-27 | 3 |
| Security Threat Detection | C-28 ~ C-30 | 3 |
| Recovery Response | C-31 ~ C-38 | 8 |
| Security Management | C-39 ~ C-44 | 6 |
| Education/Training | C-45 | 1 |

---

## 12-1. Control System Characteristics

### IT vs OT Comparison

| Item | IT System | OT/Control System |
|------|-----------|-------------------|
| **Priority** | Confidentiality > Integrity > Availability | **Availability** > Integrity > Confidentiality |
| **Uptime** | Reboot possible | 24/7 continuous operation |
| **Patching** | Regular patches | Maintenance windows only |
| **Lifespan** | 3-5 years | 15-20 years |
| **Protocols** | TCP/IP | Modbus, DNP3, OPC, etc. |

> **WARNING**
> When assessing control systems, **availability** must be the top priority. System downtime can lead to physical damage.

---

## 12-2. Account/Service Management (C-01 ~ C-14)

### C-01. Change Default Account Password

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | HMI, PLC, SCADA Server |
| **Special Note** | Change vendor default passwords |

#### Key Control System Default Accounts

| System | Default Account | Action |
|--------|-----------------|--------|
| Siemens S7 | (none) | Set password |
| Allen Bradley | (default) | Change required |
| Schneider | admin | Change required |

---

### C-09. Disable Unnecessary Services

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Minimize attack surface |

#### Recommended to Disable

- Remote Desktop (restrict if needed)
- File sharing
- Web server (except HMI)
- USB auto-run

---

## 12-3. Network/Physical Access Control (C-19 ~ C-27)

### C-19. Network Segregation

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | IT/OT network separation |

#### Recommended Architecture (Purdue Model)

```
┌─────────────────────────────────────────────────────────────────┐
│              Purdue Model-Based IT/OT Separation                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Level 5: Enterprise Network (Internet, ERP, Email)     │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            │ ← DMZ / Firewall                   │
│  ┌─────────────────────────┴───────────────────────────────┐   │
│  │  Level 4: Business Systems (Production Planning, Inv)   │   │
│  └─────────────────────────┬───────────────────────────────┘   │
│                            │ ← Firewall (IT/OT Boundary)        │
│  ╔═════════════════════════╧═══════════════════════════════╗   │
│  ║                  OT Zone (Control Systems)              ║   │
│  ╠═════════════════════════════════════════════════════════╣   │
│  ║  ┌───────────────────────────────────────────────────┐  ║   │
│  ║  │  Level 3: Manufacturing Operations (MES, Historian)│  ║   │
│  ║  └───────────────────────┬───────────────────────────┘  ║   │
│  ║                          │                               ║   │
│  ║  ┌───────────────────────┴───────────────────────────┐  ║   │
│  ║  │  Level 2: Supervisory Control (SCADA Server, HMI) │  ║   │
│  ║  └───────────────────────┬───────────────────────────┘  ║   │
│  ║                          │                               ║   │
│  ║  ┌───────────────────────┴───────────────────────────┐  ║   │
│  ║  │  Level 1: Basic Control (PLC, RTU, DCS)           │  ║   │
│  ║  └───────────────────────┬───────────────────────────┘  ║   │
│  ║                          │                               ║   │
│  ║  ┌───────────────────────┴───────────────────────────┐  ║   │
│  ║  │  Level 0: Physical Process (Sensors, Actuators)   │  ║   │
│  ║  └───────────────────────────────────────────────────┘  ║   │
│  ╚═════════════════════════════════════════════════════════╝   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### C-25. Physical Access Restriction

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Physical security of control room/equipment room |

#### Check Points

- Control room access control
- CCTV installation
- Access log management
- Locking devices (cabinets, terminals)

---

## 12-4. Security Threat Detection and Recovery (C-28 ~ C-38)

### C-28. Abnormal Traffic Detection

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | OT environment IDS operation |

#### Recommendations

- Deploy OT-specific IDS (Claroty, Nozomi, etc.)
- Detect abnormal protocols
- Configure alarm thresholds

---

### C-31. Backup and Recovery Procedures

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Rapid recovery in case of failure |

#### Backup Targets

| Target | Backup Frequency | Storage Location |
|--------|:----------------:|------------------|
| PLC programs | On change | Offline |
| HMI configuration | Weekly | Separate server |
| SCADA DB | Daily | Backup server |
| Network configuration | On change | Documentation |

---

## Control System Assessment Precautions

> **WARNING**
> The following must be observed when assessing control systems.

1. **Prior coordination**: Coordinate assessment schedule with operations staff
2. **Minimize live testing**: Test during maintenance windows when possible
3. **Simulation environment**: Verify in test environment first when possible
4. **Emergency contacts**: Have immediate response capability for issues
5. **Rollback plan**: Establish recovery plan before changes

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account/Service | Default password, unnecessary services | High |
| Network | IT/OT separation | Highest |
| Physical Security | Access control | High |
| Detection/Recovery | IDS, backups | High |

---

## Part II Complete

Systems covered in Part II (Technical Vulnerability Assessment):

- Chapter 3: Unix/Linux Server
- Chapter 4: Windows Server
- Chapter 5: Web Service
- Chapter 6: Web Application
- Chapter 7: DBMS
- Chapter 8: Network Equipment
- Chapter 9: Security Equipment
- Chapter 10: Virtualization/Cloud
- Chapter 11: PC/Endpoint
- Chapter 12: Control System (OT)

---

*Next Chapter: Chapter 13. Information Security Policy and Organization (Part III Start)*


---

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


---

# Chapter 14. Asset Management and Risk Management

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Asset management and risk management form the foundation of information security. You need to identify assets to protect and assess risks to establish appropriate protection measures. This chapter covers Asset Classification (A-10 ~ A-14), Risk Management (A-15 ~ A-17), and Audit (A-18 ~ A-20).

| Domain | Items | Count |
|--------|-------|:-----:|
| Asset Classification | A-10 ~ A-14 | 5 |
| Risk Management | A-15 ~ A-17 | 3 |
| Audit | A-18 ~ A-20 | 3 |

---

## 14-1. Asset Classification (A-10 ~ A-14)

### A-10. Establish Asset Classification Criteria

| Item | Content |
|------|---------|
| **Assessment Item** | Identify all assets (personnel, facilities, equipment, etc.) within critical information infrastructure and establish documented asset classification criteria |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Asset Types

| Type | Examples |
|------|----------|
| Information Assets | Databases, documents, software |
| Physical Assets | Servers, network equipment, PCs |
| Human Assets | System administrators, developers |
| Facility Assets | Data center, communications room, protected areas |

#### Classification Criteria Example

| Level | Confidentiality | Integrity | Availability |
|:-----:|-----------------|-----------|--------------|
| Level 1 | Secret | Operations impossible if damaged | Immediate recovery required |
| Level 2 | Confidential | Operations impaired if damaged | Recovery within 4 hours |
| Level 3 | General | Recoverable | Recovery within 1 day |

---

### A-11. Security Level Classification Management

| Item | Content |
|------|---------|
| **Assessment Item** | Classify and manage information assets according to security level and importance |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Security Level Classification

| Level | Definition | Examples |
|:-----:|------------|----------|
| Top Secret | Disclosure affects national security | Encryption keys, core designs |
| Secret | Disclosure causes severe organizational damage | Personal information, financial data |
| Confidential | Disclosure causes organizational damage | Internal business documents |
| General | Can be disclosed | Marketing materials, public documents |

---

### A-12. Asset Inventory Management

| Item | Content |
|------|---------|
| **Assessment Item** | Create and maintain an up-to-date asset inventory reflecting regular asset status surveys and changes (acquisition, disposal, transfer, etc.) |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Required Asset Inventory Fields

| Field | Description |
|-------|-------------|
| Asset ID | Unique identifier |
| Asset Name | Equipment/system name |
| Category | Server/network/endpoint, etc. |
| Location | Installation location |
| Administrator | Responsible person/department |
| Security Level | Level 1/2/3 |
| Acquisition Date | Purchase date |
| Change History | Transfer/replacement/disposal history |

---

### A-13. Asset Handling Procedures

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement handling procedures (creation/acquisition, storage, use, disposal) and protection measures according to asset classification |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Lifecycle-based Protection Measures

| Stage | Level 1 | Level 2 | Level 3 |
|-------|---------|---------|---------|
| Acquisition | Approval required | Approval required | Registration |
| Storage | Encryption + isolation | Encryption | Standard storage |
| Use | Access log + approval | Access log | Basic control |
| Disposal | Secure deletion + certificate | Secure deletion | Format/delete |

---

### A-14. Asset Manager Designation

| Item | Content |
|------|---------|
| **Assessment Item** | Designate administrators and management owners for each information asset and maintain an up-to-date list |
| **Related Dept.** | Information Security Department, All Departments |

#### Role Definitions

| Role | Responsibility |
|------|----------------|
| Asset Owner | Ultimate responsibility for the asset |
| Asset Administrator | Day-to-day management and operations |
| Asset User | Use within authorized scope |

---

## 14-2. Risk Management (A-15 ~ A-17)

### A-15. Service Status Identification

| Item | Content |
|------|---------|
| **Assessment Item** | Identify service status of critical information infrastructure, understand business processes and flows, and document them |
| **Related Dept.** | Information Security Department, System Operations Department |

#### Service Status Documentation Content

- Service list and descriptions
- Business flow diagrams (Data Flow Diagram)
- System architecture diagrams
- Network topology
- Connected systems status

---

### A-16. Risk Assessment Execution

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct risk assessment at least annually on a regular basis |
| **Related Dept.** | Information Security Department |

#### Risk Assessment Process

```
┌─────────────────────────────────────────────────────────────────┐
│                     Risk Assessment Process                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐            │
│   │ 1. Asset  │────▶│ 2. Threat │────▶│3. Vuln.   │            │
│   │   Ident.  │     │   Ident.  │     │  Ident.   │            │
│   └───────────┘     └───────────┘     └─────┬─────┘            │
│                                             │                    │
│                                             ▼                    │
│                                   ┌─────────────────┐           │
│                                   │  4. Risk Level  │           │
│                                   │   Calculation   │           │
│                                   │                 │           │
│                                   │ Risk = Asset    │           │
│                                   │    × Threat     │           │
│                                   │    × Vuln.      │           │
│                                   └────────┬────────┘           │
│                                            │                     │
│                                            ▼                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              5. Risk Treatment Decision                  │   │
│   ├─────────────┬─────────────┬─────────────┬───────────────┤   │
│   │   Reduce    │  Transfer   │    Avoid    │    Accept     │   │
│   │ (Controls)  │ (Insurance) │(Discontinue)│(Mgmt Approval)│   │
│   └─────────────┴─────────────┴─────────────┴───────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Risk Treatment Options

| Option | Description | Example |
|--------|-------------|---------|
| Risk Reduction | Apply protection measures | Deploy firewall, encryption |
| Risk Transfer | Transfer through insurance, etc. | Cyber insurance |
| Risk Avoidance | Eliminate risk source | Service discontinuation |
| Risk Acceptance | Accept residual risk | Accept with executive approval |

---

### A-17. Protection Measure Implementation Plan

| Item | Content |
|------|---------|
| **Assessment Item** | Establish annual protection measure implementation plan based on risk assessment and report to executive management |
| **Related Dept.** | Information Security Department, Executive Management |

#### Implementation Plan Components

| Item | Content |
|------|---------|
| Measure Name | Specific protection measure |
| Owner | Implementation responsibility |
| Schedule | Start date/completion date |
| Budget | Required cost |
| Effect | Risk reduction level |

---

## 14-3. Audit (A-18 ~ A-20)

### A-18. Legal Requirements Compliance Review

| Item | Content |
|------|---------|
| **Assessment Item** | Review compliance with legal requirements at least annually on a regular basis |
| **Related Dept.** | Information Security Department, Legal Department |

#### Key Legal Requirements

| Regulation | Key Content |
|------------|-------------|
| Act on Protection of Information and Communications Infrastructure | Vulnerability analysis and assessment, protection measure establishment |
| Personal Information Protection Act | Security measures, access control |
| Electronic Financial Transactions Act | Electronic financial transaction security |
| Information and Communications Network Act | Technical and administrative protection measures |

---

### A-19. Information Security Audit

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement periodic information security audit plan |
| **Related Dept.** | Audit Department, Information Security Department |

#### Audit Types

| Type | Frequency | Performed By |
|------|:---------:|--------------|
| Regular Audit | At least annually | Internal audit team |
| Ad-hoc Audit | As needed | Internal audit team |
| External Audit | As needed | External professional organization |

---

### A-20. Audit Results Reporting and Follow-up

| Item | Content |
|------|---------|
| **Assessment Item** | Report audit results to executive management and implement appropriate follow-up actions |
| **Related Dept.** | Audit Department, Executive Management |

#### Audit Follow-up Actions

1. Prepare audit result report
2. Report to executive management
3. Develop corrective action plan
4. Implement corrective actions
5. Verify implementation

---

## 14-4. Asset Inventory Management Automation

### Asset Inventory Template (Excel/CSV)

```csv
AssetID,AssetName,Type,Location,Administrator,SecurityLevel,AcquisitionDate,Status,Notes
A001,DBServer01,Server,DataCenterA,Kim,Level1,2024-01-15,Operational,Oracle DB
A002,WebServer01,Server,DataCenterA,Kim,Level2,2024-02-20,Operational,Apache
A003,Switch01,Network,CommRoom,Park,Level2,2023-05-10,Operational,Cisco
```

### Asset Collection Script (PowerShell)

```powershell
#===============================================
# KESE KIT - Asset Information Collection Script
#===============================================

$report = @()

# Collect server information
Get-ADComputer -Filter * -Properties * | ForEach-Object {
    $report += [PSCustomObject]@{
        AssetName = $_.Name
        Type = "Server"
        OS = $_.OperatingSystem
        IPAddress = $_.IPv4Address
        LastLogon = $_.LastLogonDate
    }
}

# Export to CSV
$report | Export-Csv -Path "asset_inventory.csv" -Encoding UTF8 -NoTypeInformation

Write-Host "Asset inventory generated: asset_inventory.csv"
```

### Asset Change Monitoring (Python)

```python
"""
KESE KIT - Asset Change Monitoring
Compares with previous snapshot to detect changes
"""
import pandas as pd
from datetime import datetime

def compare_assets(old_file, new_file):
    """Compare asset inventories"""
    old_df = pd.read_csv(old_file)
    new_df = pd.read_csv(new_file)

    # New assets
    new_assets = new_df[~new_df['AssetID'].isin(old_df['AssetID'])]

    # Removed assets
    removed_assets = old_df[~old_df['AssetID'].isin(new_df['AssetID'])]

    # Changed assets
    merged = old_df.merge(new_df, on='AssetID', suffixes=('_old', '_new'))
    changed = merged[merged['Status_old'] != merged['Status_new']]

    return {
        'new': new_assets,
        'removed': removed_assets,
        'changed': changed
    }

if __name__ == "__main__":
    result = compare_assets("assets_old.csv", "assets_new.csv")
    print(f"New: {len(result['new'])} items")
    print(f"Removed: {len(result['removed'])} items")
    print(f"Changed: {len(result['changed'])} items")
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Asset Classification | Asset inventory + classification criteria | Highest |
| Asset Management | Administrator designation + currency | High |
| Risk Management | Annual risk assessment | Highest |
| Audit | Annual audit + result reporting | High |

---

*Next Chapter: Chapter 15. Human Resource Security and External Party Security*


---

# Chapter 15. Human Resource Security and External Party Security

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Human resource security addresses security for internal employees, while external party security addresses security for contractors and outsourced personnel. Human factors can be the weakest security link, requiring systematic management.

```
┌─────────────────────────────────────────────────────────────────┐
│               HR Security Lifecycle Management                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              Internal Employees (A-21~A-26)              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐  │
│   │  Hiring │────▶│  Active │────▶│ Transfer│────▶│  Term.  │  │
│   │         │     │         │     │         │     │         │  │
│   │•Screen- │     │•Job     │     │•Access  │     │•Revoke  │  │
│   │ ing     │     │ defined │     │ adjust  │     │ access  │  │
│   │•Security│     │•Training│     │•Handover│     │•Asset   │  │
│   │ pledge  │     │•Monitor │     │         │     │ return  │  │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘  │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              External Parties (A-27~A-33)                │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐  │
│   │Contract │────▶│Execute  │────▶│  Audit  │────▶│  Close  │  │
│   │         │     │         │     │         │     │         │  │
│   │•Security│     │•Status  │     │•Compli- │     │•Delete  │  │
│   │ clauses │     │ mgmt    │     │ ance    │     │ accounts│  │
│   │•NDA     │     │•Visit   │     │•Violation│    │•Return  │  │
│   │         │     │ proced. │     │ action  │     │ data    │  │
│   └─────────┘     └─────────┘     └─────────┘     └─────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Human Resource Security | A-21 ~ A-26 | 6 |
| External Party Security | A-27 ~ A-33 | 7 |

---

## 15-1. Human Resource Security (A-21 ~ A-26)

### A-21. Define Job Responsibilities and Roles

| Item | Content |
|------|---------|
| **Assessment Item** | Clearly define and document responsibilities and roles for information security-related positions |
| **Related Dept.** | Information Security Department, HR Department |

#### Job Description Components

| Item | Description |
|------|-------------|
| Job Title | Information Security Officer, System Administrator, etc. |
| Role | Tasks to be performed |
| Responsibility | Scope of responsibility and authority |
| Reporting Line | Superior reporting structure |
| Qualifications | Required certifications, experience, etc. |

---

### A-22. Pre-employment Screening

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct pre-employment screening covering identity, capability, education, and experience when designating critical infrastructure personnel |
| **Related Dept.** | Information Security Department, HR Department |

#### Screening Items

| Item | Verification Content |
|------|----------------------|
| Identity Verification | ID card, military service records, etc. |
| Education Verification | Diploma certificate |
| Experience Verification | Employment certificates, career verification |
| Qualification Verification | Certification copies |
| Credit Check | Credit inquiry (if necessary) |

> **TIP**
> Public organizations may require background investigations according to "Security Work Regulations."

---

### A-23. Pre-employment Security Pledge

| Item | Content |
|------|---------|
| **Assessment Item** | Obtain security pledge or non-disclosure agreement when designating critical infrastructure personnel |
| **Related Dept.** | Information Security Department, HR Department |

#### Security Pledge Content

- Confidentiality obligation
- Information security policy compliance obligation
- Disciplinary provisions for violations
- Post-termination confidentiality obligation
- Signature and date

---

### A-24. Termination Confidentiality Agreement

| Item | Content |
|------|---------|
| **Assessment Item** | Obtain separate confidentiality agreement when removing critical infrastructure personnel designation |
| **Related Dept.** | Information Security Department, HR Department |

#### Termination Confidentiality Agreement Content

- Obligation to maintain secrets acquired during employment
- Confidentiality period (e.g., 3 years after termination)
- Legal liability for violations
- Damage compensation clause

---

### A-25. Termination Access Revocation

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement procedures for prompt asset return, access revocation/adjustment, and result verification when removing critical infrastructure personnel designation |
| **Related Dept.** | Information Security Department, HR Department, IT Department |

#### Termination Processing Checklist

| Item | Responsible | Check |
|------|-------------|:-----:|
| Access card collection | Security Team | ☐ |
| PC/laptop return | IT Team | ☐ |
| System account deletion | IT Team | ☐ |
| Email account deactivation | IT Team | ☐ |
| VPN access removal | Security Team | ☐ |
| Security pledge collection | HR Team | ☐ |
| Portable storage media return | IT Team | ☐ |

---

### A-26. Security Violation Discipline

| Item | Content |
|------|---------|
| **Assessment Item** | Clearly specify disciplinary measures for information security policy violations by critical infrastructure personnel in regulations |
| **Related Dept.** | Information Security Department, HR Department, Legal Department |

#### Disciplinary Levels

| Violation Type | Disciplinary Level |
|----------------|-------------------|
| Minor violation (1st offense) | Warning, caution |
| Repeated violation | Pay reduction, suspension |
| Serious violation | Termination, legal action |
| Intentional leakage | Termination + civil/criminal action |

---

## 15-2. External Party Security (A-27 ~ A-33)

### A-27. External Party Security Pledge

| Item | Content |
|------|---------|
| **Assessment Item** | Obtain security pledge from new external parties for external service use and business outsourcing |
| **Related Dept.** | Information Security Department, Contract Department |

#### External Party Scope

- Contractor employees
- Dispatched personnel
- Maintenance vendors
- Partner company personnel
- Outsourced developers

---

### A-28. External Party Status Management

| Item | Content |
|------|---------|
| **Assessment Item** | Identify and manage external service use and business outsourcing status within critical infrastructure scope |
| **Related Dept.** | Information Security Department, Contract Department |

#### External Party Status Management Items

| Item | Content |
|------|---------|
| Company Name | Contracted company name |
| Contract Period | Start date ~ end date |
| Scope of Work | Outsourced work content |
| Point of Contact | Vendor contact information |
| Access Rights | Granted system/area access |
| Pledge Status | Security pledge obtained |

---

### A-29. Security Requirements in Contracts

| Item | Content |
|------|---------|
| **Assessment Item** | Identify information security requirements for external service use and business outsourcing and specify in contracts or agreements |
| **Related Dept.** | Information Security Department, Contract Department, Legal Department |

#### Contract Security Clause Examples

- Confidentiality obligation
- Prohibition or approval conditions for subcontracting
- Security incident notification obligation
- Security audit acceptance obligation
- Data return/deletion upon contract termination
- Damage compensation for security violations

---

### A-30. Temporary Visitor Security Notification

| Item | Content |
|------|---------|
| **Assessment Item** | Provide advance notification of security regulations regarding information and asset access for temporary visitors (e.g., maintenance personnel) |
| **Related Dept.** | Information Security Department, Facilities Management Department |

#### Temporary Visitor Procedure

```
1. Submit visit request in advance (Requester → Security Team)
     ↓
2. Visit approval
     ↓
3. Identity verification + visitor badge issuance upon arrival
     ↓
4. Security regulation notification (signature required)
     ↓
5. Work performed with escort
     ↓
6. Badge return + belongings check upon departure
```

---

### A-31. External Party Security Audit

| Item | Content |
|------|---------|
| **Assessment Item** | Periodically audit or inspect whether external parties comply with information security requirements specified in contracts, agreements, and internal policies |
| **Related Dept.** | Information Security Department, Audit Department |

#### External Party Audit Items

| Area | Audit Items |
|------|-------------|
| Account Management | Existence of unnecessary accounts |
| Access Control | Compliance with authorized scope |
| Work Records | Work log maintenance |
| Data Management | Data leakage status |
| Security Training | Training completion status |

---

### A-32. External Party Security Violation Actions

| Item | Content |
|------|---------|
| **Assessment Item** | Take appropriate action when external parties violate security requirements or cause security incidents |
| **Related Dept.** | Information Security Department, Legal Department, Contract Department |

#### Violation Response Steps

| Step | Action |
|:----:|--------|
| Step 1 | Warning and corrective action request |
| Step 2 | Penalty imposition |
| Step 3 | Contract termination |
| Step 4 | Legal action (damage compensation) |

---

### A-33. External Party Contract Termination Processing

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement security measures for asset return, access deletion, and confidentiality agreement upon external party contract expiration, work completion, or personnel change |
| **Related Dept.** | Information Security Department, Contract Department, IT Department |

#### External Party Termination Checklist

| Item | Responsible | Check |
|------|-------------|:-----:|
| Account deletion | IT Team | ☐ |
| Access authorization removal | Security Team | ☐ |
| Equipment/data return | IT Team | ☐ |
| Confidentiality pledge | Contract Team | ☐ |
| Data deletion verification | IT Team | ☐ |
| Handover completion | Responsible Dept. | ☐ |

---

## 15-3. Security Pledge Templates

### Employee Security Pledge

```markdown
Security Pledge

I hereby pledge to comply with the following in performing duties
related to critical information infrastructure at [Organization Name]:

1. I will not disclose secrets and important information
   acquired through my duties to external parties.
2. I will faithfully comply with information security laws
   and internal regulations.
3. I will not access information assets beyond my authorized
   work purposes.
4. I will not copy, remove, or leak information without
   authorization.
5. I will immediately report any security incident occurrence
   or discovery.
6. I will maintain secrets acquired during employment even
   after resignation.
7. I confirm that I will bear civil and criminal liability
   according to relevant laws if I violate the above.

Date: YYYY/MM/DD

Department: _______________
Name: _______________ (Signature)
```

### Termination Confidentiality Agreement

```markdown
Confidentiality Agreement

Upon leaving [Organization Name], I hereby confirm the following:

1. I will not disclose any secrets and important information
   acquired during my employment to external parties even
   after termination.
2. I have returned all work-related materials and confirm
   that I do not retain any personal copies.
3. I will comply with this agreement for 3 years after
   termination.
4. I confirm that I will bear civil and criminal liability
   according to relevant laws if I violate the above.

Date: YYYY/MM/DD

Department: _______________
Name: _______________ (Signature)
```

### External Party Security Pledge

```markdown
External Party Security Pledge

I hereby pledge to comply with the following in performing
information system-related work for [Organization Name]:

1. I will not disclose information acquired through work
   to external parties.
2. I will not access information assets beyond my authorized
   work purposes.
3. I will comply with security regulations including
   prohibition of personal storage media use.
4. I will delete/return all materials after work completion.
5. I will not retain acquired information even after
   contract termination.
6. I confirm that I will bear contract termination and
   legal liability if I violate the above.

Date: YYYY/MM/DD

Company: _______________
Name: _______________ (Signature)
Supervisor Verification: _______________ (Signature)
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| HR Security | Job definition + security pledge | Highest |
| HR Security | Termination access revocation | Highest |
| External Party | Security requirements in contracts | Highest |
| External Party | External party status management | High |
| External Party | Contract termination processing | Highest |

---

*Next Chapter: Chapter 16. Training, Authentication, and Access Control*


---

# Chapter 16. Training, Authentication, and Access Control

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Training is essential for human resource security, while authentication and access control form the foundation of system security. This chapter covers Training (A-34 ~ A-38), Authentication and Authorization Management (A-39 ~ A-42), and Access Control (A-43 ~ A-55).

```
┌─────────────────────────────────────────────────────────────────┐
│      Training, Authentication, Access Control Assessment (22)    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                      ┌─────────────┐                            │
│                      │  Personnel  │                            │
│                      │   (Human)   │                            │
│                      └──────┬──────┘                            │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  Training   │     │   Auth &    │     │   Access    │       │
│  │ A-34 ~ A-38 │     │   AuthZ     │     │   Control   │       │
│  │    (5)      │     │ A-39 ~ A-42 │     │ A-43 ~ A-55 │       │
│  ├─────────────┤     │    (4)      │     │    (13)     │       │
│  │• Training   │     ├─────────────┤     ├─────────────┤       │
│  │  plan       │     │• Account/   │     │• Network    │       │
│  │• All-staff  │     │  permission │     │  separation │       │
│  │• Role-based │     │• Auth method│     │• Remote work│       │
│  │• Measure    │     │• Password   │     │• Air-gap    │       │
│  │• Alerts     │     │• Review     │     │• Wireless   │       │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘       │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             │                                    │
│                             ▼                                    │
│              ┌───────────────────────────┐                      │
│              │   Integrated Security     │                      │
│              │  (Who + How + Where)      │                      │
│              └───────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Training | A-34 ~ A-38 | 5 |
| Authentication and Authorization | A-39 ~ A-42 | 4 |
| Access Control | A-43 ~ A-55 | 13 |

---

## 16-1. Training (A-34 ~ A-38)

### A-34. Establish Training Plan

| Item | Content |
|------|---------|
| **Assessment Item** | Develop comprehensive training plan for information security awareness and conduct regularly |
| **Related Dept.** | Information Security Department, HR Department |

#### Annual Training Plan Example

| Quarter | Target | Training Content | Duration |
|:-------:|--------|-----------------|:--------:|
| Q1 | All staff | Information security basics | 2H |
| Q2 | IT staff | Latest security threats | 4H |
| Q3 | All staff | Personal information protection | 2H |
| Q4 | Managers | Incident response exercises | 4H |

---

### A-35. All-Staff Training

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct information security training for all employees and external parties |
| **Related Dept.** | Information Security Department, HR Department |

#### Training Content by Audience

| Audience | Required Content |
|----------|------------------|
| All staff | Security policy, password management, phishing response |
| New hires | Security orientation (within 1 week) |
| IT staff | Technical security, vulnerability management |
| External parties | Security regulations, pledge education |

---

### A-36. Role-Based Differentiated Training

| Item | Content |
|------|---------|
| **Assessment Item** | Differentiate training based on position and job characteristics |
| **Related Dept.** | Information Security Department |

#### Differentiated Training Framework

| Position/Role | Training Level | Annual Hours |
|---------------|----------------|:------------:|
| Executives | Security governance | 2H |
| Middle managers | Departmental security | 4H |
| General staff | Basic security rules | 4H |
| IT personnel | Technical advanced training | 8H+ |
| Security personnel | Professional training + certification | 16H+ |

---

### A-37. Training Effectiveness Measurement

| Item | Content |
|------|---------|
| **Assessment Item** | Measure and analyze training effectiveness and reflect in future training |
| **Related Dept.** | Information Security Department |

#### Effectiveness Measurement Methods

| Method | Description |
|--------|-------------|
| Pre/Post test | Compare knowledge levels before and after |
| Satisfaction survey | Evaluate content and instructor |
| Behavior observation | Monitor security incident frequency changes |
| Simulation exercises | Measure phishing response rate |

---

### A-38. Security Advisory Sharing

| Item | Content |
|------|---------|
| **Assessment Item** | Share security advisories from relevant agencies with employees and external parties and provide action guidance |
| **Related Dept.** | Information Security Department |

#### Key Security Information Sources

| Agency | URL | Content |
|--------|-----|---------|
| KISA | boho.or.kr | Security advisories, vulnerability information |
| NCSC | ncsc.go.kr | Cyber threat intelligence |
| CVE | cve.mitre.org | Vulnerability database |

---

## 16-2. Authentication and Authorization (A-39 ~ A-42)

### A-39. Account and Access Policy

| Item | Content |
|------|---------|
| **Assessment Item** | Define and implement user account and access authorization methods and scope based on job responsibilities |
| **Related Dept.** | Information Security Department, IT Department |

#### Authorization Principles

| Principle | Description |
|-----------|-------------|
| Least privilege | Grant only minimum permissions needed for job |
| Separation of duties | Separate conflicting roles (dev/ops) |
| Approval process | Grant permissions after manager approval |
| Regular review | Periodically review permission appropriateness |

#### Account Request Procedure

```
1. Complete account request form (User)
     ↓
2. Department head approval
     ↓
3. Information security officer review
     ↓
4. IT department creates account
     ↓
5. Initial password delivered to user
     ↓
6. Password change at first login
```

---

### A-40. Secure Authentication Methods

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement secure authentication methods and procedures for internal and external system access |
| **Related Dept.** | Information Security Department, IT Department |

#### Authentication Methods by Access Type

| Access Type | Authentication Method |
|-------------|----------------------|
| Regular work | ID/PW + 2FA (OTP) |
| Remote access | VPN + certificate + OTP |
| Critical systems | MFA required |
| Admin access | Certificate + OTP + IP restriction |

---

### A-41. Password Management

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement secure password management procedures and composition rules for system access |
| **Related Dept.** | Information Security Department, IT Department |

#### Password Policy

| Item | Requirement |
|------|-------------|
| Minimum length | 8+ characters (admin 10+) |
| Complexity | Combination of letters + numbers + special characters |
| Change frequency | 90 days (admin 60 days) |
| History | Prohibit reuse of last 5 passwords |
| Lockout | Lock for 15 minutes after 5 failed attempts |

---

### A-42. Permission Appropriateness Review

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement review criteria, responsible parties, methods, and frequency for user account and access permission appropriateness |
| **Related Dept.** | Information Security Department, IT Department |

#### Regular Review Items

| Item | Frequency | Responsible |
|------|:---------:|-------------|
| Dormant accounts | Monthly | IT Team |
| Permission appropriateness | Quarterly | Security Team |
| Privileged accounts | Monthly | Security Team |
| Terminated employee accounts | Real-time | HR + IT Team |

---

## 16-3. Access Control (A-43 ~ A-55)

### A-43. Network Security Policy

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement network security policy including access authorization control, remote access management, network segregation |
| **Related Dept.** | Information Security Department, Network Operations |

---

### A-44. Network Segregation

| Item | Content |
|------|---------|
| **Assessment Item** | Segregate networks based on system purpose and sensitivity, apply access control between zones |
| **Related Dept.** | Information Security Department, Network Operations |

#### Network Segregation Structure

```
[Internet]
    ↓
[DMZ] ─── Web servers, mail servers
    ↓ Firewall
[Work Network] ─── Business systems
    ↓ Firewall
[DB Zone] ─── Databases
    ↓ Firewall
[Management Network] ─── Management systems
```

---

### A-45. Access Control Rule Approval

| Item | Content |
|------|---------|
| **Assessment Item** | Access control rules must be set or changed with administrator approval |
| **Related Dept.** | Information Security Department |

---

### A-46. Access Control Policy Review

| Item | Content |
|------|---------|
| **Assessment Item** | Periodically review access control policy appropriateness |
| **Review Frequency** | At least quarterly |

---

### A-47. Firewall and IDS Deployment

| Item | Content |
|------|---------|
| **Assessment Item** | Deploy firewalls, intrusion detection systems for secure network |
| **Related Dept.** | Information Security Department, Network Operations |

---

### A-48. Remote Work Policy

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement policy for remote work (telework, incident response) including manager approval, work scope, duration, access log recording/review |
| **Related Dept.** | Information Security Department, IT Department |

#### Remote Work Procedure

1. Complete remote work request form
2. Department head + CISO approval
3. VPN account issuance (time-limited)
4. Work execution (log recording)
5. VPN account deactivation after completion
6. Log review

---

### A-49. Internal Management Terminal Restriction

| Item | Content |
|------|---------|
| **Assessment Item** | When operating systems over network, restrict management to specific internal terminals only |
| **Related Dept.** | Information Security Department, IT Department |

---

### A-50. VPN and Secure Access

| Item | Content |
|------|---------|
| **Assessment Item** | Apply VPN or other secure access methods when accessing internal systems from external locations |
| **Related Dept.** | Information Security Department, IT Department |

---

### A-51. Network Air-Gap

| Item | Content |
|------|---------|
| **Assessment Item** | Separate internal network (work network) from internet network |
| **Related Dept.** | Information Security Department, IT Department |

#### Air-Gap Types

| Type | Description | Pros/Cons |
|------|-------------|-----------|
| Physical separation | Separate network infrastructure | Security↑, Cost↑ |
| Logical separation | VLAN, VDI utilization | Cost↓, Requires management |

---

### A-52. Data Transfer System

| Item | Content |
|------|---------|
| **Assessment Item** | Deploy and use secure data transfer system after network segregation |
| **Related Dept.** | Information Security Department, IT Department |

---

### A-53. VoIP Network Separation

| Item | Content |
|------|---------|
| **Assessment Item** | Separate VoIP network from general IT network |
| **Related Dept.** | Information Security Department, Communications Department |

---

### A-54. External Party Network Separation

| Item | Content |
|------|---------|
| **Assessment Item** | Separate network for external parties stationed internally |
| **Related Dept.** | Information Security Department, IT Department |

---

### A-55. Wireless Network Security

| Item | Content |
|------|---------|
| **Assessment Item** | Apply appropriate security measures including security review approval, secure encryption algorithms, and encryption key settings for wireless network use |
| **Related Dept.** | Information Security Department, IT Department |

#### Wireless Network Security Requirements

| Item | Requirement |
|------|-------------|
| Encryption | WPA3 or WPA2-Enterprise |
| Authentication | 802.1X + RADIUS |
| SSID | Hidden setting recommended |
| Access control | MAC address filtering |
| Monitoring | Rogue AP detection |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Training | Annual training plan + differentiated training | High |
| Authentication | Password policy + MFA | Highest |
| Authorization | Least privilege + regular review | Highest |
| Access Control | Network segregation + VPN | Highest |
| Wireless | WPA2/3 + 802.1X | High |

---

*Next Chapter: Chapter 17. Operations Management and Security Management*


---

# Chapter 17. Operations Management and Security Management

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Operations management ensures stable system operation, while security management provides protection from security threats. This chapter covers Operations Management (A-56 ~ A-93) and Security Management (A-94 ~ A-103).

```
┌─────────────────────────────────────────────────────────────────┐
│        Operations and Security Management Assessment (48)        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Operations Management (A-56 ~ A-93) 38 items    │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │  │
│  │  │ Wireless │  │ System  │  │Mainten- │  │   Log   │     │  │
│  │  │  Network │  │ Deploy/ │  │ ance/   │  │  Mgmt   │     │  │
│  │  │ A-56~57  │  │ Change  │  │ Backup  │  │ A-73~75 │     │  │
│  │  │   (2)    │  │ A-58~66 │  │ A-67~72 │  │   (3)   │     │  │
│  │  │          │  │   (9)   │  │   (6)   │  │         │     │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘     │  │
│  │       │            │            │            │           │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │  │
│  │  │  Data   │  │ Security│  │ Mobile  │                  │  │
│  │  │ Protect │  │  Sys Ops│  │ Device  │                  │  │
│  │  │ A-76~85 │  │ A-86~88 │  │ A-89~93 │                  │  │
│  │  │  (10)   │  │   (3)   │  │   (5)   │                  │  │
│  │  └─────────┘  └─────────┘  └─────────┘                  │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │          Security Management (A-94 ~ A-103) 10 items      │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │  │
│  │  │Patch/EOS│  │ Malware │  │Personal │  │  Vuln/  │     │  │
│  │  │  Mgmt   │  │/Security│  │ Info    │  │ Pentest │     │  │
│  │  │ A-94~95 │  │ A-96~97 │  │  A-100  │  │A-101~103│     │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Operations Management | A-56 ~ A-93 | 38 |
| Security Management | A-94 ~ A-103 | 10 |

---

## 17-1. Operations Management (A-56 ~ A-93)

### Wireless Network Management (A-56 ~ A-57)

#### A-56. Wireless Network Usage Procedure

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement procedures for wireless network usage application and termination so only authorized personnel can use authorized devices |
| **Related Dept.** | Information Security Department, IT Department |

#### A-57. Wireless Network Inspection

| Item | Content |
|------|---------|
| **Assessment Item** | Periodically inspect for unauthorized wireless use, unauthorized APs, and bypass network blocking |
| **Inspection Frequency** | At least monthly |

#### Wireless AP Inspection Items

| Item | Content |
|------|---------|
| Authorization | Verify if registered AP |
| Encryption | WPA2/WPA3 applied |
| SSID | Organization name exposure |
| Location | Installation location appropriateness |

---

### System Deployment/Change Management (A-58 ~ A-67)

#### A-58. Legal Requirements Documentation

| Item | Content |
|------|---------|
| **Assessment Item** | When deploying, developing, or changing assets and systems, define and document legal, regulatory, and contractual requirements |
| **Related Dept.** | Information Security Department, Legal Department |

#### A-59. Security Review

| Item | Content |
|------|---------|
| **Assessment Item** | When deploying, developing, or changing assets and systems, conduct security and compatibility review with security officer confirmation and approval |
| **Related Dept.** | Information Security Department |

#### Security Review Checklist

| Item | Verification Content |
|------|----------------------|
| Account management | Default account change, password policy |
| Access control | Unnecessary port blocking, permission settings |
| Encryption | Transmission/storage data encryption |
| Logging | Audit log configuration |
| Patching | Latest patch application |

---

#### A-60. Change Management Procedure

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement system change management procedures |
| **Related Dept.** | Information Security Department, IT Department |

#### Change Management Process

```
1. Submit change request
     ↓
2. Impact analysis (including security impact)
     ↓
3. Change Advisory Board approval
     ↓
4. Develop change plan (including rollback plan)
     ↓
5. Verify in test environment
     ↓
6. Execute change
     ↓
7. Confirm results and document
```

---

#### A-61. CC Certification and Security Validation

| Item | Content |
|------|---------|
| **Assessment Item** | Security products must have domestic CC certification or security validation |
| **Related Dept.** | Information Security Department, Procurement Department |

> **TIP**
> Public organizations must deploy CC-certified or security-validated products. The IT Security Certification Office (www.itscc.kr) provides certified product lists.

---

#### A-63 ~ A-66. Development/Operations Environment Management

| Item | Assessment Content |
|------|-------------------|
| A-63 | Separate development/test and production environments |
| A-64 | Separate developer and operator access permissions |
| A-65 | Differentiate source code access, store separately |
| A-66 | Analyze security vulnerabilities when changing source code |

#### Environment Separation Principles

| Environment | Purpose | Access |
|-------------|---------|--------|
| Development | Code writing, unit testing | Developers |
| Test | Integration/performance testing | Developers, QA |
| Staging | Pre-production verification | Operations, QA |
| Production | Live service | Operations only |

---

### Maintenance, Incident, Backup Management (A-67 ~ A-72)

#### A-67. Change Procedures

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement formal procedures for changes to major systems and security products |

---

#### A-68. Maintenance Work Management

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement formal work request and execution procedures for maintenance, regularly review work records |
| **Related Dept.** | Information Security Department, IT Department |

#### Maintenance Procedure

| Step | Content |
|:----:|---------|
| 1 | Complete work request (content, date, personnel) |
| 2 | Manager approval |
| 3 | Pre-work backup |
| 4 | Execute work (with escort) |
| 5 | Verify work results |
| 6 | Document work record |

---

#### A-69. Incident Management

| Item | Content |
|------|---------|
| **Assessment Item** | Document system incident management guidelines including detection, recording, analysis, recovery, and reporting |
| **Related Dept.** | IT Department |

---

#### A-70. Backup Procedures

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement backup procedures including targets, frequency, methods, storage location, retention period, offsite storage |
| **Related Dept.** | IT Department |

#### Backup Policy Example

| Target | Type | Frequency | Retention |
|--------|------|:---------:|:---------:|
| DB | Full | Weekly | 1 year |
| DB | Incremental | Daily | 1 month |
| System config | Full | Monthly | 1 year |
| Logs | Archive | Daily | 2 years |

---

#### A-71. Recovery Testing

| Item | Content |
|------|---------|
| **Assessment Item** | Regularly conduct recovery tests to verify backup completeness, accuracy, and procedure appropriateness |
| **Test Frequency** | At least annually |

---

### Log Management (A-73 ~ A-75)

#### A-73. Access Record Generation and Retention

| Item | Content |
|------|---------|
| **Assessment Item** | Generate and retain access records (logs) for systems and security systems, implement protective measures against unauthorized viewing and tampering |
| **Retention Period** | Minimum 6 months (1 year for personal information) |

#### Log Management Requirements

| Item | Requirement |
|------|-------------|
| Collection | Access time, accessor, IP address, performed action |
| Storage | Separate log server, tamper protection |
| Retention | Minimum 6 months |
| Review | Regular anomaly analysis |

---

#### A-74. Log Review and Monitoring

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement log review and monitoring procedures including review frequency, targets, and methods to detect anomalies such as errors, abuse, and fraud |

---

#### A-75. Log Review Result Reporting

| Item | Content |
|------|---------|
| **Assessment Item** | Report log and monitoring results to responsible manager at least monthly |
| **Reporting Frequency** | At least monthly |

---

### Data Protection (A-76 ~ A-85)

#### A-76. Information/Media Disposal

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement disposal methods for information and media |

#### Storage Media Deletion Methods

| Media Type | Deletion Method |
|------------|-----------------|
| HDD | Secure erase (DoD 5220.22-M) or physical destruction |
| SSD | Secure Erase or physical destruction |
| Optical media | Physical destruction |
| Documents | Cross-cut shredder (DIN Level 4+) |

---

#### A-77. Security Inspection

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct periodic and unscheduled security inspections to verify compliance with security regulations |

---

#### A-78 ~ A-81. Confidential Information Management

| Item | Assessment Content |
|------|-------------------|
| A-78 | Register and manage confidential documents in registry |
| A-79 | Store printed confidential documents in locked cabinets |
| A-80 | Deploy protection measures/systems for sensitive information handling |
| A-81 | Manage network configuration (IP info) as confidential or higher |

---

#### A-82 ~ A-85. Data Protection

| Item | Assessment Content |
|------|-------------------|
| A-82 | Store critical and general data on separate servers |
| A-83 | Establish posting procedures for website content |
| A-84 | Establish encryption policy including targets, strength, key management |
| A-85 | Establish encryption key recovery procedures and review recovery records |

---

### Security System Operations (A-86 ~ A-93)

#### A-86. Firewall/IDS Operations

| Item | Content |
|------|---------|
| **Assessment Item** | Install and operate intrusion prevention and detection tools according to organizational security policy and rules |

---

#### A-88. Unauthorized Device Blocking

| Item | Content |
|------|---------|
| **Assessment Item** | Block unauthorized PCs, laptops when connected to network and periodically review blocking records |

---

#### A-89 ~ A-93. Mobile Device Management

| Item | Assessment Content |
|------|-------------------|
| A-89 | Mobile device (laptop, tablet, USB) usage/removal control procedures |
| A-90 | Record removal history and periodic inspection |
| A-91 | Protection measures for sensitive information on smartphones |
| A-92 | Periodic inspection of portable storage media, current status updates |
| A-93 | Countermeasures for mobile device loss |

---

## 17-2. Security Management (A-94 ~ A-103)

### A-94. Patch Management Policy

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement OS and software patch management policy and procedures based on asset characteristics and criticality |
| **Related Dept.** | Information Security Department, IT Department |

#### Patch Management Process

```
1. Collect patch information (KISA, vendors, etc.)
     ↓
2. Impact analysis
     ↓
3. Apply to test environment
     ↓
4. Develop deployment plan (prioritization)
     ↓
5. Apply to production
     ↓
6. Verify deployment results
```

---

### A-95. End of Security Support Response

| Item | Content |
|------|---------|
| **Assessment Item** | When OS or software is no longer supported by vendor, replace product or implement security measures |

#### EOS/EOL Response Options

| Option | Description |
|--------|-------------|
| Upgrade | Upgrade to supported version |
| Replace | Replace with new product |
| Isolate | Network isolation + additional security |
| Virtual patching | Block vulnerabilities with WAF, IPS |

---

### A-96. Malware Response

| Item | Content |
|------|---------|
| **Assessment Item** | Deploy and operate security programs to protect against viruses and other malware |

---

### A-97. Monthly Security Inspection Day

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct monthly security inspection and remediation activities on focus items |
| **Frequency** | Monthly (third Wednesday of each month) |

> **TIP**
> Public organizations designate the third Wednesday of each month as "Cyber Security Inspection Day" for PC security checks.

---

### A-100. Personal Information Security Measures

| Item | Content |
|------|---------|
| **Assessment Item** | Implement measures for personal information security including access authorization management, access control, encryption, access record retention and inspection |

#### Personal Information Security Requirements

| Measure | Content |
|---------|---------|
| Access authorization | Grant to minimum personnel only, regular review |
| Access control | IP restriction, unauthorized access blocking |
| Encryption | Encrypt passwords, SSN, etc. in storage/transmission |
| Access records | Retain minimum 1 year, review monthly |

---

### A-101. DDoS Response

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and operate DDoS attack prevention measures |

#### DDoS Response Options

| Option | Description |
|--------|-------------|
| DDoS protection service | KISA Cyber Shelter, CDN, etc. |
| Bandwidth capacity | Sufficient network bandwidth |
| Detection system | Abnormal traffic detection |
| Response plan | Attack response procedures |

---

### A-102. Penetration Testing

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct penetration testing on systems directly or indirectly connected to critical infrastructure and establish security measures |
| **Frequency** | At least annually |

---

### A-103. Vulnerability Assessment

| Item | Content |
|------|---------|
| **Assessment Item** | Operate periodic security vulnerability review and remediation process for systems and equipment |
| **Frequency** | At least annually (per Article 9, Act on Protection of Information and Communications Infrastructure) |

---

## 17-3. Network Air-Gap Configuration

### Air-Gap Type Comparison

| Type | Physical Separation | Logical Separation |
|------|--------------------|--------------------|
| Implementation | Separate network, PCs | VDI, CBC, etc. |
| Cost | High | Relatively low |
| Security | High | Depends on management |
| Usability | Less convenient | Relatively convenient |

### Air-Gap Architecture Example

```
[Internet Network]            [Work Network]
    │                           │
[Internet PC]──[Data Transfer]──[Work PC]
    │           System            │
    ↓                            ↓
[Internet Server]            [Work Server]
```

### Data Transfer System Security

| Item | Requirement |
|------|-------------|
| Approval | Approval procedure for data transfer |
| Scanning | Malware scanning |
| Logging | Transfer history recording |
| Capacity | Transfer size limits |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Operations | Change management + backup/recovery | Highest |
| Operations | Log management + regular review | Highest |
| Security | Patch management + malware response | Highest |
| Security | Vulnerability assessment + penetration testing | High |
| Air-Gap | Physical/logical separation + data transfer | Highest |

---

*Next Chapter: Chapter 18. Incident Response and Business Continuity*


---

# Chapter 18. Incident Response and Business Continuity

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Rapid incident response and ensuring business continuity are critical to organizational survival. This chapter covers Incident Response (A-104 ~ A-113) and Business Continuity (A-114 ~ A-118).

```
┌─────────────────────────────────────────────────────────────────┐
│          Incident Response and Business Continuity (15)         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Incident Response (A-104 ~ A-113) 10 items      │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │    ┌──────────┐                                          │  │
│  │    │ Detection │                                          │  │
│  │    │(Monitoring)│                                         │  │
│  │    └─────┬────┘                                          │  │
│  │          ▼                                                │  │
│  │    ┌──────────┐    ┌──────────┐    ┌──────────┐         │  │
│  │    │  Initial │───▶│ Analysis │───▶│Containmnt│         │  │
│  │    │ Response │    │(Root Cause)│   │(Isolate) │         │  │
│  │    └──────────┘    └──────────┘    └─────┬────┘         │  │
│  │                                          ▼               │  │
│  │    ┌──────────┐    ┌──────────┐    ┌──────────┐         │  │
│  │    │Prevention│◀───│ Evidence │◀───│ Recovery │         │  │
│  │    │(Lessons) │    │(Forensics)│   │(Eradicate)│         │  │
│  │    └──────────┘    └──────────┘    └──────────┘         │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         Business Continuity (A-114 ~ A-118) 5 items       │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │                                                           │  │
│  │   ┌─────────┐    ┌─────────┐    ┌─────────┐             │  │
│  │   │ Disaster│───▶│ RTO/RPO │───▶│   DR    │             │  │
│  │   │ Types   │    │  Define │    │  Plan   │             │  │
│  │   └─────────┘    └─────────┘    └────┬────┘             │  │
│  │                                       │                   │  │
│  │                  ┌────────────────────┼─────────────┐    │  │
│  │                  ▼                    ▼             │    │  │
│  │            ┌─────────┐          ┌─────────┐        │    │  │
│  │            │Redundancy│         │ DR Drill │       │    │  │
│  │            │  Setup   │         │ Execute  │       │    │  │
│  │            └─────────┘          └─────────┘        │    │  │
│  │                                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Incident Response | A-104 ~ A-113 | 10 |
| Business Continuity | A-114 ~ A-118 | 5 |

---

## 18-1. Incident Response (A-104 ~ A-113)

### A-104. Establish Incident Response Framework

| Item | Content |
|------|---------|
| **Assessment Item** | Establish framework and procedures for preventing security incidents and personal information breaches, and for rapid effective response when incidents occur |
| **Related Dept.** | Information Security Department, All Departments |

#### Incident Response Framework Components

| Component | Content |
|-----------|---------|
| Response Team | Computer Emergency Response Team (CERT) composition |
| Response Procedures | Detect→Analyze→Contain→Eradicate→Recover→Post-incident |
| Contact System | Internal/external emergency contact lists |
| Roles/Responsibilities | Define roles for each team member |

---

### A-105. Incident Reporting Procedure

| Item | Content |
|------|---------|
| **Assessment Item** | Document procedures for rapid security incident reporting and execute prompt reporting |
| **Related Dept.** | Information Security Department, All Departments |

#### Incident Reporting Chain

```
[Incident Discoverer]
     ↓ Immediate report
[Department Head]
     ↓ Within 1 hour
[Chief Information Security Officer (CISO)]
     ↓ If necessary
[CEO/Executive Director]
     ↓ If legally required
[KISA/Relevant Agencies]
```

---

### A-106. External Coordination Framework

| Item | Content |
|------|---------|
| **Assessment Item** | Establish coordination framework with external agencies and experts for incident response |
| **Related Dept.** | Information Security Department |

#### External Coordination Agencies

| Agency | Contact | Role |
|--------|---------|------|
| KISA Internet Incident Response Center | 118 | Incident reporting, technical support |
| Cyber Safety Center (NCSC) | - | Public organization incident response |
| Police Cyber Bureau | 182 | Cybercrime investigation |
| External specialists | - | Forensics, recovery support |

---

### A-107. Emergency Response Team

| Item | Content |
|------|---------|
| **Assessment Item** | Establish Emergency Response Team that can be activated when cyber crisis level reaches "Caution" or higher, or when damage occurs |
| **Related Dept.** | Information Security Department, Executive Management |

#### Cyber Crisis Alert Levels

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cyber Crisis Alert Levels                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────┐                                                   │
│   │ Severe  │ ← Large-scale damage, full emergency response     │
│   │  (Red)  │                                                    │
│   ├─────────┤                                                   │
│   │  Alert  │ ← Damage occurring, emergency response mode       │
│   │(Orange) │                                                    │
│   ├─────────┤                                                   │
│   │ Caution │ ← Potential damage, activate emergency team       │
│   │(Yellow) │                                                    │
│   ├─────────┤                                                   │
│   │ Interest│ ← Increased threat indicators, enhanced monitoring│
│   │ (Blue)  │                                                    │
│   ├─────────┤                                                   │
│   │ Normal  │ ← Normal monitoring operations                    │
│   │ (Green) │                                                    │
│   └─────────┘                                                   │
│                                                                  │
│   ※ Based on NCSC (National Cyber Security Center) criteria     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Level | Situation | Response |
|:-----:|-----------|----------|
| Normal | Normal | Regular monitoring |
| Interest | Increased threats | Enhanced monitoring |
| Caution | Potential damage | Activate emergency team |
| Alert | Damage occurring | Emergency response mode |
| Severe | Large-scale damage | Full emergency response |

---

### A-108. Incident Monitoring

| Item | Content |
|------|---------|
| **Assessment Item** | Continuously monitor for unauthorized access and security incidents |
| **Related Dept.** | Information Security Department, Security Operations Center |

---

### A-109. Response Training

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct periodic training to familiarize personnel with incident response procedures and methods |
| **Frequency** | At least annually |

#### Training Types

| Type | Content | Frequency |
|------|---------|:---------:|
| Tabletop exercise | Scenario-based discussion | Annually |
| Simulation | Actual response simulation | Annually |
| Phishing drill | Simulated phishing emails | Quarterly |

---

### A-110. Incident Record Management

| Item | Content |
|------|---------|
| **Assessment Item** | Record and manage security incident analysis results including type, scope, and impact |
| **Related Dept.** | Information Security Department |

#### Incident Record Items

| Item | Content |
|------|---------|
| Incident time | Occurrence/detection/closure times |
| Incident type | Malware, hacking, data breach, etc. |
| Impact scope | Systems, data, operations |
| Damage extent | Data loss, service downtime |
| Root cause | Root cause analysis |
| Response actions | Actions taken |
| Lessons learned | Improvement items |

---

### A-111. Remediation Procedures

| Item | Content |
|------|---------|
| **Assessment Item** | Establish remediation procedures for security vulnerabilities and incidents |
| **Related Dept.** | Information Security Department, IT Department |

---

### A-112. Recurrence Prevention Measures

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement recurrence prevention measures after cyber security incidents |
| **Related Dept.** | Information Security Department |

#### Recurrence Prevention Process

```
1. Root Cause Analysis
     ↓
2. Identify similar risk factors
     ↓
3. Develop prevention measures
     ↓
4. Implement measures
     ↓
5. Verify effectiveness
     ↓
6. Update policies/procedures
```

---

### A-113. Evidence Collection

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement guidelines for collecting appropriate evidence for incident handling, contract verification, and litigation |
| **Related Dept.** | Information Security Department, Legal Department |

#### Evidence Collection Principles

| Principle | Description |
|-----------|-------------|
| Integrity | Prevent evidence tampering (record hash values) |
| Chain of custody | Document collection→storage→analysis process |
| Timeliness | Collect volatile data first |
| Legality | Collect in legally valid manner |

---

## 18-2. Business Continuity (A-114 ~ A-118)

### A-114. IT Disaster Type Identification

| Item | Content |
|------|---------|
| **Assessment Item** | Identify IT disaster types that could threaten service continuity, analyze damage extent and business impact, identify critical IT services and systems |
| **Related Dept.** | Information Security Department, IT Department, Business Departments |

#### IT Disaster Types

| Type | Examples |
|------|----------|
| Natural disasters | Earthquake, fire, flood |
| Technical failures | Hardware failure, software errors |
| Human errors | Operational mistakes, data deletion |
| Cyber attacks | Ransomware, DDoS, hacking |
| Infrastructure failures | Power, communications, HVAC |

---

### A-115. Recovery Objectives Definition

| Item | Content |
|------|---------|
| **Assessment Item** | Define recovery time objectives and recovery point objectives based on characteristics of critical IT services and systems |
| **Related Dept.** | Information Security Department, IT Department, Business Departments |

#### Recovery Objective Metrics

| Metric | Definition | Example |
|--------|------------|---------|
| RTO | Recovery Time Objective | 4 hours |
| RPO | Recovery Point Objective | 1 hour |
| MTPD | Maximum Tolerable Period of Disruption | 24 hours |

#### System Recovery Objectives Example

| System | RTO | RPO | Tier |
|--------|:---:|:---:|:----:|
| Mission-critical systems | 2H | 0 (real-time) | Tier 1 |
| Critical business systems | 4H | 1H | Tier 2 |
| General business systems | 24H | 4H | Tier 3 |

---

### A-116. Disaster Recovery Plan

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement disaster recovery plan including recovery strategy, emergency recovery organization, emergency contact system, and recovery procedures to ensure service and system continuity during disasters |
| **Related Dept.** | Information Security Department, IT Department, Executive Management |

#### Disaster Recovery Plan (DRP) Components

| Component | Content |
|-----------|---------|
| Recovery strategy | Hot/Warm/Cold Site |
| Recovery organization | Roles, responsibilities, contacts |
| Recovery procedures | Step-by-step recovery procedures |
| Resource inventory | Required resources (HW, SW, personnel) |
| Test plan | Annual drill plan |

---

### A-117. System Redundancy

| Item | Content |
|------|---------|
| **Assessment Item** | Implement redundancy for high security importance systems |
| **Related Dept.** | IT Department |

#### Redundancy Types

| Type | Description | RTO |
|------|-------------|:---:|
| Active-Active | Both systems running simultaneously | ~0 |
| Active-Standby | Automatic failover to standby | Minutes |
| Cold Standby | Manual failover to standby | Hours |

---

### A-118. Continuity Review and Training

| Item | Content |
|------|---------|
| **Assessment Item** | Continuously review and manage business continuity through drills, reflect organizational changes |
| **Frequency** | At least annually |

#### DR Drill Types

| Type | Description | Frequency |
|------|-------------|:---------:|
| Walkthrough | Procedure review | Semi-annually |
| Simulation | Virtual scenario | Annually |
| Failover test | Actual failover execution | Annually |

---

## 18-3. Incident Reporting Procedures

### Legal Reporting Requirements

| Regulation | Subject | Report To | Deadline |
|------------|---------|-----------|----------|
| Act on Protection of CII | Critical infrastructure | KISA, relevant agency | Without delay |
| Personal Information Protection Act | Personal information processors | PIPC | Within 72 hours |
| Information and Communications Network Act | IT service providers | KISA | Within 24 hours |

### Incident Report Form

```markdown
Security Incident Report

1. Reporting Organization Information
   - Organization name:
   - Contact person:
   - Phone number:

2. Incident Overview
   - Occurrence time:
   - Discovery time:
   - Incident type: [ ]Malware [ ]Hacking [ ]DDoS [ ]Data breach [ ]Other
   - Affected systems:
   - Damage extent:

3. Incident Details
   - How discovered:
   - Cause (suspected):
   - Damage details:

4. Response Status
   - Initial response:
   - Future plans:

5. Attachments
   - Relevant logs
   - Screenshots

Date: YYYY/MM/DD
Prepared by:             (Signature)
```

### KISA Reporting Methods

| Method | Contact |
|--------|---------|
| Phone | 118 (Internet Incident Response Center) |
| Web | boho.or.kr |
| Email | cert@krcert.or.kr |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Incident Response | Response framework + reporting procedures | Highest |
| Incident Response | External coordination + emergency team | High |
| Incident Response | Evidence collection + recurrence prevention | High |
| Business Continuity | RTO/RPO definition | Highest |
| Business Continuity | DR plan + training | Highest |

---

*Next Chapter: Chapter 19. Physical Security*


---

# Chapter 19. Physical Security

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Physical security protects information assets from physical threats. No matter how strong technical security is, all security can be compromised if physical access is possible. This chapter covers Physical Security assessment items (B-1 ~ B-9).

```
┌─────────────────────────────────────────────────────────────────┐
│                 Physical Security Assessment (9)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────────┐                      │
│                    │   External Boundary  │                      │
│                    │  (Building Perimeter) │                     │
│                    └──────────┬──────────┘                      │
│                               │                                  │
│                               ▼                                  │
│           ┌─────────────────────────────────────┐               │
│           │            General Zone             │               │
│           │     (Lobby, Meeting rooms -         │               │
│           │      General access)                │               │
│           │         B-5: Visitor control        │               │
│           └──────────────────┬──────────────────┘               │
│                              │                                   │
│                              ▼                                   │
│           ┌─────────────────────────────────────┐               │
│           │           Restricted Zone           │               │
│           │     (Offices, Dev rooms -           │               │
│           │      Authorized access)             │               │
│           │   B-2: Access control │ B-3: Records│               │
│           │   B-9: Document sec.  │ B-6: Removal│               │
│           └──────────────────┬──────────────────┘               │
│                              │                                   │
│                              ▼                                   │
│           ╔═════════════════════════════════════╗               │
│           ║           Controlled Zone           ║               │
│           ║     (Data center, Server room -     ║               │
│           ║      Strict control)                ║               │
│           ║                                     ║               │
│           ║   B-1: Protected area  B-4: CCTV   ║               │
│           ║   B-7: Environmental   B-8: Cable  ║               │
│           ║                                     ║               │
│           ║    ┌─────────────────────────┐     ║               │
│           ║    │    Information Assets   │     ║               │
│           ║    │  (Servers, Network, DB) │     ║               │
│           ║    └─────────────────────────┘     ║               │
│           ╚═════════════════════════════════════╝               │
│                                                                  │
│           ※ Higher security levels toward center               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Physical Security | B-1 ~ B-9 | 9 |

---

## 19-1. Physical Security Assessment (B-1 ~ B-9)

### B-1. Protected Area Designation

| Item | Content |
|------|---------|
| **Assessment Item** | Designate and manage locations requiring physical protection (data center, communications room, etc.) as protected areas |
| **Related Dept.** | Information Security Department, Facilities Management |

#### Protected Area Classification

| Zone | Definition | Examples |
|------|------------|----------|
| Controlled | Unauthorized access prohibited | Data center, server room |
| Restricted | Authorized personnel only | Offices, development room |
| General | General access allowed | Lobby, meeting rooms |

#### Protected Area Marking

- Zone signage installation
- Floor color/line differentiation
- Security level indication

---

### B-2. Access Control Procedures

| Item | Content |
|------|---------|
| **Assessment Item** | Establish access control procedures for protected areas and maintain access records |
| **Related Dept.** | Information Security Department, Facilities Management |

#### Access Control Methods

| Method | Description | Security Level |
|--------|-------------|:--------------:|
| Key card | RFID/smart card | Medium |
| Biometrics | Fingerprint, iris, facial | High |
| PIN + Card | Dual authentication | High |
| Key | Physical key | Low |

#### Access Record Management

| Item | Content |
|------|---------|
| Record items | Date/time, accessor, purpose, escort |
| Retention period | Minimum 1 year |
| Review frequency | Monthly |

---

### B-3. Access Record Retention

| Item | Content |
|------|---------|
| **Assessment Item** | Retain and manage access records for protected areas (data center, etc.) for minimum 1 year |
| **Retention Period** | Minimum 1 year |

---

### B-4. CCTV Installation and Operation

| Item | Content |
|------|---------|
| **Assessment Item** | Install and operate CCTV for monitoring access to protected areas |
| **Related Dept.** | Facilities Management, Information Security Department |

#### CCTV Installation Requirements

| Item | Requirement |
|------|-------------|
| Location | Entrances, corridors, data center interior |
| Recording quality | Face-identifiable resolution |
| Retention period | Minimum 30 days |
| Monitoring | Real-time monitoring or regular review |

> **WARNING**
> CCTV operation must comply with privacy laws. Notice signs and purpose disclosure are required.

---

### B-5. Visitor Access Control

| Item | Content |
|------|---------|
| **Assessment Item** | Control access for external visitors (including maintenance vendors) to protected areas |
| **Related Dept.** | Facilities Management, Information Security Department |

#### Visitor Access Procedure

```
1. Pre-visit request (Requester → Security Team)
     ↓
2. Visit approval
     ↓
3. Identity verification on visit day
     ↓
4. Visitor badge issuance (photo recommended)
     ↓
5. Security regulation briefing/signature
     ↓
6. Escort by responsible party
     ↓
7. Badge return upon departure
     ↓
8. Belongings inspection (if necessary)
```

---

### B-6. Asset Removal Control

| Item | Content |
|------|---------|
| **Assessment Item** | Control removal of information systems and protected assets |
| **Related Dept.** | Information Security Department, Facilities Management |

#### Asset Removal Control Targets

| Category | Targets |
|----------|---------|
| Incoming | External equipment, storage media, laptops |
| Outgoing | Servers, storage media, documents |

#### Removal Procedure

1. Complete removal request form
2. Manager/security officer approval
3. Data deletion verification (for media)
4. Create removal record
5. Inspection upon return

---

### B-7. Environmental Protection Equipment

| Item | Content |
|------|---------|
| **Assessment Item** | Operate and manage equipment to protect information systems in protected areas from natural disasters and environmental risks |
| **Related Dept.** | Facilities Management |

#### Environmental Protection Equipment

| Equipment | Purpose | Inspection Frequency |
|-----------|---------|:--------------------:|
| HVAC | Temperature/humidity control | Daily |
| Fire suppression | Fire response | Monthly |
| UPS | Power outage protection | Monthly |
| Generator | Extended outage protection | Quarterly |
| Water leak detection | Flood prevention | Daily |
| Grounding | Lightning/static protection | Annually |

#### Data Center Environmental Standards

| Item | Standard |
|------|----------|
| Temperature | 18~27°C |
| Humidity | 40~60% |
| Dust | Class 100,000 or below |

---

### B-8. Cable Security

| Item | Content |
|------|---------|
| **Assessment Item** | Safely install and manage cables in protected areas |
| **Related Dept.** | Facilities Management, IT Department |

#### Cable Security Requirements

| Item | Requirement |
|------|-------------|
| Routing | Under-floor/ceiling routing (minimize exposure) |
| Identification | Cable labeling |
| Separation | Separate power/data/communications cables |
| Protection | Use cable trays, ducts |

---

### B-9. Document Security

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement secure storage and disposal procedures for important documents |
| **Related Dept.** | Information Security Department, All Departments |

#### Document Security Requirements

| Item | Requirement |
|------|-------------|
| Storage | Store in locked cabinets |
| Disposal | Use cross-cut shredder (DIN Level 4+) |
| Copying | Approval procedure for copying |
| Removal | Approval and logging for removal |

---

## 19-2. Protected Area Management

### Protected Area Registry Form

| Zone Name | Location | Level | Manager | Access Method | Notes |
|-----------|----------|:-----:|---------|---------------|-------|
| Data Center | 1F Bldg A | Controlled | Kim | Card+Biometric | 24hr CCTV |
| Comm Room | 2F Bldg B | Controlled | Park | Card+PIN | 24hr CCTV |
| Dev Room | 3F Bldg C | Restricted | Lee | Card | - |

### Access Log Form

| Date | Visitor | Affiliation | Purpose | Escort | In | Out | Notes |
|------|---------|-------------|---------|--------|:--:|:---:|-------|
| 3/15 | Hong | Company A | Server maintenance | Kim | 09:00 | 12:00 | |
| 3/15 | Lee | Company B | Network inspection | Park | 14:00 | 16:00 | |

### Physical Security Inspection Checklist

| Inspection Item | Content | Good | Vulnerable |
|-----------------|---------|:----:|:----------:|
| Access control | Card/biometric operation | ☐ | ☐ |
| CCTV | Recording status, angle appropriateness | ☐ | ☐ |
| Access records | Record retention | ☐ | ☐ |
| Locking devices | Cabinet lock status | ☐ | ☐ |
| Environmental equipment | Temperature/humidity, fire suppression status | ☐ | ☐ |
| Cabling | Cable organization | ☐ | ☐ |
| Visitor control | Badge issuance/collection | ☐ | ☐ |

---

## Physical Security Related Regulations

### Act on Protection of Information and Communications Infrastructure

- Article 10 (Protection Guidelines): Includes physical protection measures

### Personal Information Protection Act

- Article 29 (Security Measures): Physical access blocking

### National Information Security Basic Guidelines

- Article 42 (Physical Protected Area Designation)
- Article 43 (Access Control)

---

## Summary

| Item | Key Assessment Content | Priority |
|------|------------------------|:--------:|
| B-1 | Protected area designation | Highest |
| B-2 | Access control procedures + records | Highest |
| B-4 | CCTV installation and operation | High |
| B-5 | Visitor access control | Highest |
| B-6 | Asset removal control | High |
| B-7 | Environmental protection equipment | High |

---

## Part III Complete

Content covered in Part III (Administrative and Physical Vulnerability Assessment):

- Chapter 13: Information Security Policy and Organization
- Chapter 14: Asset Management and Risk Management
- Chapter 15: Human Resource Security and External Party Security
- Chapter 16: Training, Authentication, and Access Control
- Chapter 17: Operations Management and Security Management
- Chapter 18: Incident Response and Business Continuity
- Chapter 19: Physical Security

---

*Next Chapter: Chapter 20. Government Project Environment Application (Part IV Start)*


---

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


---

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


---

# Chapter 22. Automation Tool Development

> Part IV. Practical Application

---

## Overview

Automating vulnerability assessments significantly improves efficiency. This chapter covers assessment script architecture, result collection and reporting, and CI/CD pipeline integration.

```
┌─────────────────────────────────────────────────────────────────┐
│                  KESE-KIT Automation Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Target Systems                        │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │
│  │  │ Unix/   │  │ Windows │  │ Network │  │ Database│   │    │
│  │  │ Linux   │  │ Server  │  │ Device  │  │  (DBMS) │   │    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │    │
│  └───────┼────────────┼────────────┼────────────┼────────┘    │
│          │            │            │            │              │
│          └────────────┴────────────┴────────────┘              │
│                            │                                    │
│                            ▼ Execute assessment scripts         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Assessment Engine (Scripts)             │    │
│  │  ┌───────────────┐  ┌────────────────┐                  │    │
│  │  │ Item Defs     │  │ Target Defs    │                  │    │
│  │  │ (items.yaml)  │  │ (targets.yaml) │                  │    │
│  │  └───────────────┘  └────────────────┘                  │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                    │
│                            ▼ JSON results transmission          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Collector Server                        │    │
│  │              REST API (Flask/FastAPI)                    │    │
│  │  ┌───────────────────────────────────────────────────┐  │    │
│  │  │  /api/v1/results  │  /api/v1/summary             │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                    │
│           ┌────────────────┼────────────────┐                   │
│           ▼                ▼                ▼                   │
│    ┌───────────┐    ┌───────────┐    ┌───────────┐             │
│    │ Reporting │    │   Web     │    │  CI/CD    │             │
│    │ (HTML/PDF)│    │ Dashboard │    │Integration│             │
│    └───────────┘    └───────────┘    └───────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 22-1. Assessment Script Architecture

### Overall Structure

```
KESE-KIT/
├── scripts/
│   ├── unix/           # Unix/Linux assessment scripts
│   │   ├── account.sh  # Account management
│   │   ├── file.sh     # File/directory
│   │   ├── service.sh  # Service management
│   │   └── run_all.sh  # Execute all
│   ├── windows/        # Windows assessment scripts
│   │   ├── account.ps1
│   │   ├── service.ps1
│   │   └── run_all.ps1
│   ├── network/        # Network device assessment
│   └── database/       # Database assessment
├── collector/          # Result collection module
│   ├── agent.py        # Agent
│   └── server.py       # Collection server
├── reporter/           # Reporting module
│   ├── templates/      # Report templates
│   └── generator.py    # Report generator
├── config/             # Configuration files
│   ├── items.yaml      # Assessment item definitions
│   └── targets.yaml    # Assessment target definitions
└── web/                # Web dashboard
    └── dashboard/
```

### Assessment Item Definition (YAML)

```yaml
# config/items.yaml
unix:
  - id: U-01
    name: Restrict root remote login
    category: Account Management
    severity: High
    check:
      type: grep
      target: /etc/ssh/sshd_config
      pattern: "^PermitRootLogin"
      expected: "no"
    remediation: "Set PermitRootLogin no in sshd_config"

  - id: U-02
    name: Password complexity settings
    category: Account Management
    severity: High
    check:
      type: file_exists
      target: /etc/security/pwquality.conf
    remediation: "Configure pwquality.conf file"

windows:
  - id: W-01
    name: Rename Administrator account
    category: Account Management
    severity: High
    check:
      type: powershell
      script: "(Get-LocalUser | Where-Object {$_.SID -like '*-500'}).Name"
      expected_not: "Administrator"
    remediation: "Rename Administrator account to different name"
```

### Assessment Target Definition (YAML)

```yaml
# config/targets.yaml
groups:
  - name: Web Servers
    targets:
      - hostname: web01
        ip: 192.168.1.10
        os: linux
        credentials:
          type: ssh_key
          user: admin
          key_file: ~/.ssh/id_rsa
      - hostname: web02
        ip: 192.168.1.11
        os: linux

  - name: DB Servers
    targets:
      - hostname: db01
        ip: 192.168.1.20
        os: linux
        db_type: mysql
```

---

## 22-2. Integrated Assessment Scripts

### Unix/Linux Integrated Script

```bash
#!/bin/bash
#===============================================
# KESE KIT - Unix/Linux Integrated Assessment Script
# Version: 1.0
#===============================================

# Configuration
REPORT_DIR="/var/log/kese_kit"
REPORT_FILE="$REPORT_DIR/$(hostname)_$(date +%Y%m%d).json"
RESULT=()

# Create log directory
mkdir -p "$REPORT_DIR"

# Assessment function
check_item() {
    local id="$1"
    local name="$2"
    local result="$3"  # GOOD, VULN, N/A
    local detail="$4"

    RESULT+=("{\"id\":\"$id\",\"name\":\"$name\",\"result\":\"$result\",\"detail\":\"$detail\"}")

    if [ "$result" == "GOOD" ]; then
        echo -e "[\e[32mGOOD\e[0m] $id: $name"
    elif [ "$result" == "VULN" ]; then
        echo -e "[\e[31mVULN\e[0m] $id: $name - $detail"
    else
        echo -e "[\e[33mN/A\e[0m] $id: $name"
    fi
}

# U-01: Restrict root remote login
check_u01() {
    local id="U-01"
    local name="Restrict root remote login"

    if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config 2>/dev/null; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "PermitRootLogin is not set to no"
    fi
}

# U-02: Password complexity
check_u02() {
    local id="U-02"
    local name="Password complexity settings"

    if [ -f /etc/security/pwquality.conf ]; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "pwquality.conf does not exist"
    fi
}

# U-04: Password file protection
check_u04() {
    local id="U-04"
    local name="Password file protection"

    if [ ! -r /etc/shadow ] || [ "$(stat -c %a /etc/shadow)" -le "400" ]; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "/etc/shadow has excessive permissions"
    fi
}

# Main execution
echo "============================================="
echo "KESE KIT - Unix/Linux Vulnerability Assessment"
echo "Host: $(hostname)"
echo "Date: $(date)"
echo "============================================="

check_u01
check_u02
check_u04
# ... additional assessment items

# Save JSON results
echo "[" > "$REPORT_FILE"
echo "${RESULT[*]}" | sed 's/} {/},\n{/g' >> "$REPORT_FILE"
echo "]" >> "$REPORT_FILE"

echo ""
echo "Results saved: $REPORT_FILE"
```

### Windows Integrated Script

```powershell
#===============================================
# KESE KIT - Windows Integrated Assessment Script
# Version: 1.0
#===============================================

param(
    [string]$ReportPath = "C:\KESE_KIT\Reports"
)

# Configuration
$ReportFile = Join-Path $ReportPath "$($env:COMPUTERNAME)_$(Get-Date -Format 'yyyyMMdd').json"
$Results = @()

# Create directory
New-Item -ItemType Directory -Path $ReportPath -Force | Out-Null

# Assessment function
function Test-Item {
    param(
        [string]$Id,
        [string]$Name,
        [string]$Result,
        [string]$Detail = ""
    )

    $script:Results += @{
        id = $Id
        name = $Name
        result = $Result
        detail = $Detail
    }

    $color = switch ($Result) {
        "GOOD" { "Green" }
        "VULN" { "Red" }
        default { "Yellow" }
    }

    Write-Host "[$Result] $Id`: $Name" -ForegroundColor $color
    if ($Detail) { Write-Host "  -> $Detail" -ForegroundColor Gray }
}

# W-01: Administrator account rename
function Test-W01 {
    $id = "W-01"
    $name = "Rename Administrator account"

    $admin = Get-LocalUser | Where-Object { $_.SID -like "*-500" }
    if ($admin.Name -ne "Administrator") {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        Test-Item -Id $id -Name $name -Result "VULN" -Detail "Using default account name"
    }
}

# W-02: Guest account disabled
function Test-W02 {
    $id = "W-02"
    $name = "Disable Guest account"

    $guest = Get-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
    if (-not $guest.Enabled) {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        Test-Item -Id $id -Name $name -Result "VULN" -Detail "Guest account is enabled"
    }
}

# W-03: Password complexity
function Test-W03 {
    $id = "W-03"
    $name = "Password complexity settings"

    $policy = Get-Content C:\Windows\System32\GroupPolicy\Machine\Microsoft\Windows` NT\SecEdit\GptTmpl.inf -ErrorAction SilentlyContinue
    if ($policy -match "PasswordComplexity\s*=\s*1") {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        # Check with secedit
        secedit /export /cfg "$env:TEMP\secpol.cfg" | Out-Null
        $cfg = Get-Content "$env:TEMP\secpol.cfg"
        if ($cfg -match "PasswordComplexity\s*=\s*1") {
            Test-Item -Id $id -Name $name -Result "GOOD"
        } else {
            Test-Item -Id $id -Name $name -Result "VULN" -Detail "Complexity not configured"
        }
    }
}

# Main execution
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "KESE KIT - Windows Vulnerability Assessment" -ForegroundColor Cyan
Write-Host "Host: $($env:COMPUTERNAME)"
Write-Host "Date: $(Get-Date)"
Write-Host "=============================================" -ForegroundColor Cyan

Test-W01
Test-W02
Test-W03
# ... additional assessment items

# Save JSON results
$Results | ConvertTo-Json | Out-File $ReportFile -Encoding UTF8

Write-Host ""
Write-Host "Results saved: $ReportFile" -ForegroundColor Green
```

---

## 22-3. Result Collection and Reporting

### Result Collection Server (Python)

```python
"""
KESE KIT - Result Collection Server
Flask-based REST API
"""
from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
RESULT_DIR = "./results"

@app.route('/api/v1/results', methods=['POST'])
def receive_result():
    """Receive assessment results"""
    data = request.json

    hostname = data.get('hostname', 'unknown')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{hostname}_{timestamp}.json"

    os.makedirs(RESULT_DIR, exist_ok=True)
    with open(os.path.join(RESULT_DIR, filename), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({'status': 'success', 'filename': filename})

@app.route('/api/v1/results', methods=['GET'])
def get_results():
    """Get assessment result list"""
    files = os.listdir(RESULT_DIR) if os.path.exists(RESULT_DIR) else []
    return jsonify({'results': files})

@app.route('/api/v1/results/<filename>', methods=['GET'])
def get_result(filename):
    """Get specific assessment result"""
    filepath = os.path.join(RESULT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/v1/summary', methods=['GET'])
def get_summary():
    """Get overall status summary"""
    if not os.path.exists(RESULT_DIR):
        return jsonify({'total': 0, 'good': 0, 'vuln': 0})

    total, good, vuln = 0, 0, 0
    for filename in os.listdir(RESULT_DIR):
        with open(os.path.join(RESULT_DIR, filename), 'r') as f:
            data = json.load(f)
            for item in data.get('results', []):
                total += 1
                if item.get('result') == 'GOOD':
                    good += 1
                elif item.get('result') == 'VULN':
                    vuln += 1

    return jsonify({
        'total': total,
        'good': good,
        'vuln': vuln,
        'compliance_rate': round(good / total * 100, 1) if total > 0 else 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Report Generator (Python)

```python
"""
KESE KIT - Report Generator
Generate HTML/PDF reports from vulnerability assessment results
"""
from jinja2 import Template
import json
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Vulnerability Assessment Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; border-bottom: 2px solid #333; }
        .summary { background: #f5f5f5; padding: 20px; margin: 20px 0; }
        .good { color: green; }
        .vuln { color: red; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #333; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Critical Information Infrastructure Vulnerability Assessment Report</h1>

    <div class="summary">
        <h2>Assessment Overview</h2>
        <p>Assessment Date: {{ date }}</p>
        <p>Target: {{ hostname }}</p>
        <p>Total Items: {{ total }}</p>
        <p>Good: <span class="good">{{ good }}</span> /
           Vulnerable: <span class="vuln">{{ vuln }}</span></p>
        <p>Compliance Rate: {{ compliance_rate }}%</p>
    </div>

    <h2>Detailed Results</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Assessment Item</th>
            <th>Result</th>
            <th>Details</th>
        </tr>
        {% for item in results %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td class="{{ 'good' if item.result == 'GOOD' else 'vuln' }}">
                {{ 'Good' if item.result == 'GOOD' else 'Vulnerable' }}
            </td>
            <td>{{ item.detail }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def generate_report(result_file, output_file):
    """Generate HTML report from assessment results"""
    with open(result_file, 'r') as f:
        data = json.load(f)

    results = data.get('results', [])
    good = sum(1 for r in results if r.get('result') == 'GOOD')
    vuln = sum(1 for r in results if r.get('result') == 'VULN')
    total = len(results)

    template = Template(HTML_TEMPLATE)
    html = template.render(
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        hostname=data.get('hostname', 'Unknown'),
        total=total,
        good=good,
        vuln=vuln,
        compliance_rate=round(good / total * 100, 1) if total > 0 else 0,
        results=results
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Report generated: {output_file}")

if __name__ == '__main__':
    generate_report('result.json', 'report.html')
```

---

## 22-4. CI/CD Pipeline Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                CI/CD Security Assessment Pipeline                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────┐                                                 │
│    │  Code    │                                                 │
│    │  Push    │                                                 │
│    └────┬─────┘                                                 │
│         │                                                        │
│         ▼                                                        │
│    ╔══════════════════════════════════════════════════════╗     │
│    ║            CI/CD Pipeline (Automated)                ║     │
│    ╠══════════════════════════════════════════════════════╣     │
│    ║                                                      ║     │
│    ║  ┌─────────┐  ┌─────────┐  ┌─────────┐             ║     │
│    ║  │  SAST   │  │ Depend- │  │KESE-KIT │             ║     │
│    ║  │(Bandit) │  │  ency   │  │ Check   │             ║     │
│    ║  │         │  │(Safety) │  │         │             ║     │
│    ║  └────┬────┘  └────┬────┘  └────┬────┘             ║     │
│    ║       │            │            │                   ║     │
│    ║       └────────────┴────────────┘                   ║     │
│    ║                    │                                 ║     │
│    ║                    ▼                                 ║     │
│    ║            ┌───────────────┐                        ║     │
│    ║            │ Report Gen.   │                        ║     │
│    ║            │ (HTML/JSON)   │                        ║     │
│    ║            └───────┬───────┘                        ║     │
│    ║                    │                                 ║     │
│    ╚════════════════════╪════════════════════════════════╝     │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐                   │
│    │ Artifact│    │  Alert  │    │ Report  │                   │
│    │ Storage │    │ (Email) │    │ Publish │                   │
│    └─────────┘    └─────────┘    └─────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### GitHub Actions Integration

```yaml
# .github/workflows/security-check.yml
name: Security Vulnerability Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Every Monday

jobs:
  security-check:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install bandit safety

    - name: Run SAST (Bandit)
      run: |
        bandit -r . -f json -o bandit-report.json || true

    - name: Run dependency check (Safety)
      run: |
        safety check --json > safety-report.json || true

    - name: Run KESE-KIT checks
      run: |
        ./scripts/unix/run_all.sh

    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json
          /var/log/kese_kit/*.json

    - name: Check for critical vulnerabilities
      run: |
        python scripts/check_critical.py
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Security Scan') {
            parallel {
                stage('SAST') {
                    steps {
                        sh 'bandit -r . -f json -o bandit-report.json || true'
                    }
                }

                stage('Dependency Check') {
                    steps {
                        sh 'safety check --json > safety-report.json || true'
                    }
                }

                stage('KESE-KIT') {
                    steps {
                        sh './scripts/unix/run_all.sh'
                    }
                }
            }
        }

        stage('Generate Report') {
            steps {
                sh 'python reporter/generator.py'
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: '*.json,*.html', fingerprint: true
            }
        }
    }

    post {
        always {
            publishHTML([
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Security Report'
            ])
        }
        failure {
            emailext(
                subject: "Security Check Failed: ${env.JOB_NAME}",
                body: "Check the results: ${env.BUILD_URL}",
                to: 'security@company.com'
            )
        }
    }
}
```

---

## Summary

| Item | Key Content |
|------|-------------|
| Architecture | Modular script structure |
| Item Definition | YAML-based item/target definitions |
| Result Collection | REST API-based collection server |
| Reporting | Automated HTML/PDF generation |
| CI/CD | GitHub Actions, Jenkins integration |

---

## Part IV Complete

Content covered in Part IV (Practical Application):

- Chapter 20: Government Project Environment Application
- Chapter 21: Public Procurement Market Response
- Chapter 22: Automation Tool Development

---

*Next: Appendix*


---
