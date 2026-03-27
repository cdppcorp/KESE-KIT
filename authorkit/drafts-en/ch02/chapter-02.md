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
