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
