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
