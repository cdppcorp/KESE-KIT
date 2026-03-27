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
