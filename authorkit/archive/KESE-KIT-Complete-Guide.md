# KESE KIT - Critical Information Infrastructure Vulnerability Analysis and Assessment Practical Guide

---

## Preface

This guide provides comprehensive, practical guidance for conducting vulnerability analysis and assessment of Critical Information Infrastructure (CII) in accordance with the Act on the Protection of Information and Communications Infrastructure. KESE KIT (Korea Enhanced Security Evaluation - KISA Infrastructure Toolkit) is designed to help security practitioners, system administrators, and government project managers systematically assess and remediate security vulnerabilities across technical, administrative, and physical domains.

The guide covers approximately 560 assessment items across all domains:
- **Technical Vulnerabilities** (~424 items): Unix/Linux, Windows, Web, DBMS, Network, Security Equipment, Virtualization/Cloud, PC/Endpoint, and Control Systems
- **Administrative Vulnerabilities** (127 items): Policy, Organization, Asset Management, Risk Management, HR Security, Access Control, Operations, Incident Response, and Business Continuity
- **Physical Vulnerabilities** (9 items): Protected areas, access control, environmental protection

Whether you are conducting self-assessments, preparing for external audits, or developing automation tools for security assessments, this guide provides the practical knowledge and ready-to-use scripts needed to protect critical infrastructure.

---

## Table of Contents

### Part I. Fundamentals
- [Chapter 1. Introduction](#chapter-1-introduction)
- [Chapter 2. Legal Framework and Assessment Framework](#chapter-2-legal-framework-and-assessment-framework)

### Part II. Technical Vulnerability Assessment
- [Chapter 3. Unix/Linux Server Assessment](#chapter-3-unixlinux-server-assessment)
- [Chapter 4. Windows Server Assessment](#chapter-4-windows-server-assessment)
- [Chapter 5. Web Service Assessment](#chapter-5-web-service-assessment)
- [Chapter 6. Web Application Assessment](#chapter-6-web-application-assessment)
- [Chapter 7. Database (DBMS) Assessment](#chapter-7-database-dbms-assessment)
- [Chapter 8. Network Equipment Assessment](#chapter-8-network-equipment-assessment)
- [Chapter 9. Security Equipment Assessment](#chapter-9-security-equipment-assessment)
- [Chapter 10. Virtualization and Cloud Assessment](#chapter-10-virtualization-and-cloud-assessment)
- [Chapter 11. PC and Endpoint Assessment](#chapter-11-pc-and-endpoint-assessment)
- [Chapter 12. Control System (OT) Assessment](#chapter-12-control-system-ot-assessment)

### Part III. Administrative and Physical Vulnerability Assessment
- [Chapter 13. Information Security Policy and Organization](#chapter-13-information-security-policy-and-organization)
- [Chapter 14. Asset Management and Risk Management](#chapter-14-asset-management-and-risk-management)
- [Chapter 15. Human Resource Security and External Party Security](#chapter-15-human-resource-security-and-external-party-security)
- [Chapter 16. Training, Authentication, and Access Control](#chapter-16-training-authentication-and-access-control)
- [Chapter 17. Operations Management and Security Management](#chapter-17-operations-management-and-security-management)
- [Chapter 18. Incident Response and Business Continuity](#chapter-18-incident-response-and-business-continuity)
- [Chapter 19. Physical Security](#chapter-19-physical-security)

### Part IV. Practical Application
- [Chapter 20. Government Project Environment Application](#chapter-20-government-project-environment-application)
- [Chapter 21. Public Procurement Market Response](#chapter-21-public-procurement-market-response)
- [Chapter 22. Automation Tool Development](#chapter-22-automation-tool-development)

---

# Part I. Fundamentals

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

# Part II. Technical Vulnerability Assessment

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

# Chapter 5. Web Service Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Web service assessment covers configuration checks for web server software like Apache and Nginx. This chapter covers 47 assessment items (WS-01 ~ WS-47) divided into 4 domains.

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

## 5-2. Service Management (WS-06 ~ WS-30)

### WS-06. Disable Directory Listing

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent directory content disclosure |
| **Criteria** | Good: Disabled / Vulnerable: Enabled |

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

## 5-3. Security Settings (WS-31 ~ WS-43)

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

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Dedicated account, shell restriction | Highest |
| Service Management | Directory listing, version hiding, method restriction | Highest |
| Security Settings | SSL/TLS, security headers | High |
| Patch/Log | Latest version, log configuration | High |

---

# Chapter 6. Web Application Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Web application vulnerabilities are assessed based on OWASP Top 10. This chapter is especially important for those developing in **Vibe Coding** environments.

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

---

### XSS (Cross-Site Scripting)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Risk Level** | OWASP Top 10 A03:2021 |
| **Types** | Stored XSS, Reflected XSS, DOM XSS |

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

---

## 6-2. Authentication and Session Management

### Secure Session Management

| Item | Recommended Setting |
|------|---------------------|
| Session ID length | 128 bits or more |
| Session ID generation | Use cryptographic random |
| Session timeout | Within 30 minutes (critical systems) |
| Session regeneration after login | Required |

### Password Storage

| Method | Security | Recommended |
|--------|:--------:|:-----------:|
| Plaintext storage | Very vulnerable | No |
| MD5/SHA-1 | Vulnerable | No |
| SHA-256 (no salt) | Vulnerable | No |
| bcrypt/scrypt/Argon2 | Secure | Yes |

---

## 6-3. Access Control and Authorization Verification

### Vertical Privilege Escalation

| Item | Content |
|------|---------|
| **Description** | Regular user accessing admin functions |
| **Defense** | Server-side authorization verification required |

### Horizontal Privilege Escalation

| Item | Content |
|------|---------|
| **Description** | Accessing another user's data |
| **Defense** | Resource ownership verification |

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

> **TIP**
> Never deploy AI-generated code to production without security review.

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

# Chapter 7. Database (DBMS) Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

DBMS is a critical asset that stores organizational core data. This chapter covers 32 assessment items (D-01 ~ D-32).

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

### D-19. Principle of Least Privilege

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Grant only minimum required privileges |

> **WARNING**
> `GRANT ALL PRIVILEGES` violates least privilege principle. Grant only necessary permissions individually.

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password change, remove unused accounts | Highest |
| Access Management | Remote access restriction, least privilege | Highest |
| Option Management | Security parameter settings | High |
| Patch Management | Apply latest patches | Highest |

---

# Chapter 8. Network Equipment Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Network equipment (routers, switches) is the core of infrastructure. This chapter covers 40 assessment items (N-01 ~ N-40).

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

### N-04. Encrypt Stored Passwords

#### Remediation (Cisco)

```
configure terminal
service password-encryption
# Use enable secret instead of enable password
enable secret [password]
```

---

## 8-2. Access Management (N-11 ~ N-18)

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

## 8-5. Feature Management (N-25 ~ N-40)

### N-25. SNMP Security Configuration

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

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password, encrypted storage | Highest |
| Access Management | SSH usage, ACL configuration | Highest |
| Patch Management | Latest firmware | High |
| Log Management | Syslog configuration | Medium |
| Feature Management | SNMP security, disable unnecessary services | High |

---

# Chapter 9. Security Equipment Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Security equipment (Firewall, IDS/IPS, WAF) is a core element of security. This chapter covers 19 assessment items (S-01 ~ S-19).

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | S-01 ~ S-05 | 5 |
| Access Management | S-06 ~ S-08 | 3 |
| Patch Management | S-09 | 1 |
| Log Management | S-10 ~ S-12 | 3 |
| Feature Management | S-13 ~ S-19 | 7 |

---

## 9-1. Firewall Assessment (S-01 ~ S-19)

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

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password change | Highest |
| Access Management | Management interface restriction | Highest |
| Feature Management | Policy optimization, signature updates | High |

---

# Chapter 10. Virtualization and Cloud Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Virtualization and cloud environments are core to modern infrastructure. This chapter covers Virtualization equipment (V-01 ~ V-36) and Cloud (CL-01 ~ CL-14) assessments.

---

## 10-1. Virtualization Equipment (V-01 ~ V-36)

### V-01. Hypervisor Account Management

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | VMware vSphere, Hyper-V, KVM |
| **Purpose** | Hypervisor admin account security |

### V-12. Virtual Network Segregation

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Network isolation between VMs |

---

## 10-2. Cloud Environment (CL-01 ~ CL-14)

### CL-01. IAM Account Management

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | AWS, Azure, GCP |
| **Purpose** | Cloud account and permission management |

### CL-04. Principle of Least Privilege

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent excessive permission grants |

> **WARNING**
> Minimize AdministratorAccess and *:* permissions.

---

## 10-3. Container Security (Docker, K8s)

### Docker Security Assessment

| Item | Check For |
|------|-----------|
| Image vulnerabilities | Base image vulnerability scan |
| Privileged execution | Prohibit --privileged flag |
| root execution | Use non-root user in container |
| Network | Prohibit unnecessary port exposure |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Virtualization | Hypervisor accounts, network segregation | Highest |
| Cloud | IAM, least privilege, storage security | Highest |
| Container | Image vulnerabilities, privilege restriction | High |

---

# Chapter 11. PC and Endpoint Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

PCs and endpoints are the points of direct contact with users. This chapter covers 18 assessment items (PC-01 ~ PC-18).

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | PC-01 ~ PC-04 | 4 |
| Access Management | PC-05 ~ PC-11 | 7 |
| Patch Management | PC-12 ~ PC-13 | 2 |
| Security Management | PC-14 ~ PC-18 | 5 |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Unnecessary accounts, screen saver | High |
| Access Management | Shared folders, removable media | High |
| Patch Management | OS patches | Highest |
| Security Management | Antivirus, firewall | Highest |

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

# Part III. Administrative and Physical Vulnerability Assessment

---

# Chapter 13. Information Security Policy and Organization

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Administrative vulnerability assessment, unlike technical assessment, involves reviewing policies, guidelines, and procedures, along with conducting interviews with relevant personnel. This chapter covers Information Security Policy (A-1 ~ A-7) and Information Security Organization (A-8 ~ A-9).

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

#### Judgment Criteria

| Judgment | Criteria |
|:--------:|----------|
| Good | Top-level information security policy established with executive approval |
| Partial | Policy exists but approval history unclear |
| Vulnerable | No information security policy established |

---

## 13-2. Information Security Organization (A-8 ~ A-9)

### A-8. Dedicated Information Security Team

| Item | Content |
|------|---------|
| **Assessment Item** | Establish a dedicated team and personnel to plan, execute, and review information security activities |
| **Related Dept.** | Information Security Department, HR Department |

### A-9. Information Security Committee

| Item | Content |
|------|---------|
| **Assessment Item** | Information Security Committee is established with documented roles and responsibilities |
| **Related Dept.** | Information Security Department, Executive Management |

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

## 14-2. Risk Management (A-15 ~ A-17)

### A-16. Risk Assessment Execution

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct risk assessment at least annually on a regular basis |
| **Related Dept.** | Information Security Department |

#### Risk Treatment Options

| Option | Description | Example |
|--------|-------------|---------|
| Risk Reduction | Apply protection measures | Deploy firewall, encryption |
| Risk Transfer | Transfer through insurance, etc. | Cyber insurance |
| Risk Avoidance | Eliminate risk source | Service discontinuation |
| Risk Acceptance | Accept residual risk | Accept with executive approval |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Asset Classification | Asset inventory + classification criteria | Highest |
| Asset Management | Administrator designation + currency | High |
| Risk Management | Annual risk assessment | Highest |
| Audit | Annual audit + result reporting | High |

---

# Chapter 15. Human Resource Security and External Party Security

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Human resource security addresses security for internal employees, while external party security addresses security for contractors and outsourced personnel. Human factors can be the weakest security link, requiring systematic management.

| Domain | Items | Count |
|--------|-------|:-----:|
| Human Resource Security | A-21 ~ A-26 | 6 |
| External Party Security | A-27 ~ A-33 | 7 |

---

## 15-1. Human Resource Security (A-21 ~ A-26)

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

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| HR Security | Job definition + security pledge | Highest |
| HR Security | Termination access revocation | Highest |
| External Party | Security requirements in contracts | Highest |
| External Party | External party status management | High |
| External Party | Contract termination processing | Highest |

---

# Chapter 16. Training, Authentication, and Access Control

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Training is essential for human resource security, while authentication and access control form the foundation of system security. This chapter covers Training (A-34 ~ A-38), Authentication and Authorization Management (A-39 ~ A-42), and Access Control (A-43 ~ A-55).

| Domain | Items | Count |
|--------|-------|:-----:|
| Training | A-34 ~ A-38 | 5 |
| Authentication and Authorization | A-39 ~ A-42 | 4 |
| Access Control | A-43 ~ A-55 | 13 |

---

## 16-2. Authentication and Authorization (A-39 ~ A-42)

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

## 16-3. Access Control (A-43 ~ A-55)

### A-44. Network Segregation

| Item | Content |
|------|---------|
| **Assessment Item** | Segregate networks based on system purpose and sensitivity, apply access control between zones |
| **Related Dept.** | Information Security Department, Network Operations |

### A-55. Wireless Network Security

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

# Chapter 17. Operations Management and Security Management

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Operations management ensures stable system operation, while security management provides protection from security threats. This chapter covers Operations Management (A-56 ~ A-93) and Security Management (A-94 ~ A-103).

| Domain | Items | Count |
|--------|-------|:-----:|
| Operations Management | A-56 ~ A-93 | 38 |
| Security Management | A-94 ~ A-103 | 10 |

---

## 17-1. Operations Management (A-56 ~ A-93)

### A-60. Change Management Procedure

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

### A-70. Backup Procedures

#### Backup Policy Example

| Target | Type | Frequency | Retention |
|--------|------|:---------:|:---------:|
| DB | Full | Weekly | 1 year |
| DB | Incremental | Daily | 1 month |
| System config | Full | Monthly | 1 year |
| Logs | Archive | Daily | 2 years |

---

## 17-2. Security Management (A-94 ~ A-103)

### A-94. Patch Management Policy

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement OS and software patch management policy and procedures based on asset characteristics and criticality |
| **Related Dept.** | Information Security Department, IT Department |

### A-102. Penetration Testing

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct penetration testing on systems directly or indirectly connected to critical infrastructure and establish security measures |
| **Frequency** | At least annually |

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

# Chapter 18. Incident Response and Business Continuity

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Rapid incident response and ensuring business continuity are critical to organizational survival. This chapter covers Incident Response (A-104 ~ A-113) and Business Continuity (A-114 ~ A-118).

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

## 18-2. Business Continuity (A-114 ~ A-118)

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

# Chapter 19. Physical Security

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Physical security protects information assets from physical threats. No matter how strong technical security is, all security can be compromised if physical access is possible. This chapter covers Physical Security assessment items (B-1 ~ B-9).

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

### B-7. Environmental Protection Equipment

#### Environmental Protection Equipment

| Equipment | Purpose | Inspection Frequency |
|-----------|---------|:--------------------:|
| HVAC | Temperature/humidity control | Daily |
| Fire suppression | Fire response | Monthly |
| UPS | Power outage protection | Monthly |
| Generator | Extended outage protection | Quarterly |
| Water leak detection | Flood prevention | Daily |
| Grounding | Lightning/static protection | Annually |

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

# Part IV. Practical Application

---

# Chapter 20. Government Project Environment Application

> Part IV. Practical Application

---

## Overview

Government and public sector projects have different security requirements from private sector projects. This chapter covers public organization security requirements, information security budget guidelines, and pre-certified product utilization methods.

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

---

## 20-2. Information Security Budget Guidelines

### Information Security Budget Guidelines

Information security budget ratio within public organization IT project budgets:

| Category | Recommended Ratio | Notes |
|----------|:-----------------:|-------|
| General IT projects | 5% or more | Baseline |
| Personal information systems | 7% or more | Recommended |
| Critical information infrastructure | 10% or more | Required |

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

# Chapter 21. Public Procurement Market Response

> Part IV. Practical Application

---

## Overview

To enter the public procurement market, security requirements must be met. This chapter covers procurement agency security requirements, proposal writing guide, and security review response methods.

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

---

## 21-2. Proposal Writing Guide

### Proposal Differentiation Points

| Area | Differentiation Points |
|------|----------------------|
| Certification | ISMS/ISO 27001 holder |
| Experience | Similar public project track record |
| Tools | Proprietary security assessment tools |
| Personnel | Information security professionals |
| Methodology | Security development methodology |

---

## 21-3. Security Review Response

### What is Security Review?

A procedure to review whether security requirements are met when deploying or developing information systems in administrative agencies

| Item | Content |
|------|---------|
| Legal Basis | e-Government Act Article 56 |
| Target | Public organization information systems |
| Review Agency | NIS (national/public) or self-review |

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

---

## Summary

| Item | Key Content |
|------|-------------|
| Procurement Requirements | CC certification, secure coding, vulnerability assessment |
| Proposal | Detailed security plan, methodology presentation |
| Security Review | Advance preparation, checklist utilization |
| Preparation | ISMS certification, track record, personnel |

---

# Chapter 22. Automation Tool Development

> Part IV. Practical Application

---

## Overview

Automating vulnerability assessments significantly improves efficiency. This chapter covers assessment script architecture, result collection and reporting, and CI/CD pipeline integration.

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

# Main execution
echo "============================================="
echo "KESE KIT - Unix/Linux Vulnerability Assessment"
echo "Host: $(hostname)"
echo "Date: $(date)"
echo "============================================="

check_u01
# ... additional assessment items

# Save JSON results
echo "[" > "$REPORT_FILE"
echo "${RESULT[*]}" | sed 's/} {/},\n{/g' >> "$REPORT_FILE"
echo "]" >> "$REPORT_FILE"

echo ""
echo "Results saved: $REPORT_FILE"
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

---

## 22-4. CI/CD Pipeline Integration

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

# End of Document

This comprehensive guide covers all aspects of vulnerability analysis and assessment for Critical Information Infrastructure. For the latest updates to assessment items and methodologies, refer to the official KISA guidelines and the Act on the Protection of Information and Communications Infrastructure.

---

*KESE KIT - Critical Information Infrastructure Vulnerability Analysis and Assessment Practical Guide*

*Version 1.0*
