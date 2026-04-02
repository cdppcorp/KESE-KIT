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
