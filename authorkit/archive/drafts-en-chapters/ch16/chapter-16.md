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
