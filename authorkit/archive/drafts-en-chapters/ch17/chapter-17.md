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
