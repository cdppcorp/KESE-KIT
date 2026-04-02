---
name: kesekit-start
description: Run a security vulnerability assessment based on KISA guidelines. Supports CII (560+ items), AI Security Guide, Robot Security (103 items), and Space Security (satellite/GSaaS/supply chain, 12 domains, 53 items). Use when "security assessment", "vulnerability scan", "CII audit", "KISA assessment", "AI security", "robot security", "space security", "satellite security", "GSaaS security".
---

# KESE Security Vulnerability Assessment

Perform comprehensive security vulnerability assessment based on KISA guidelines. Automatically selects the appropriate guideline based on user context.

## Guideline Selection

| # | Guideline | Description | Items |
|---|-----------|-------------|:-----:|
| 1 | **CII (Critical Information Infrastructure)** | Technical(424)+Administrative(127)+Physical(18) | ~560 |
| 2 | **AI Security** | AI Developer/Service Provider/User requirements | ~54 |
| 3 | **Robot Security** | Industrial/Service/Medical robot checklist (11 categories) | ~103 |
| 4 | **Space Security** | Satellite/GSaaS/Supply chain checklist (12 domains) | 53 |

### Auto-detection
- Servers, networks, databases, web services, firewalls → **CII**
- AI models, LLM, generative AI, machine learning, prompts → **AI Security**
- Robots, industrial robots, service robots, medical robots, ROS/ROS2, PLC-linked robot systems → **Robot Security**
- Satellites, ground stations, GSaaS, space systems, GNSS, VSAT, LEO constellation, space supply chain → **Space Security**

---

## CII Branch

Read the appropriate reference file from `references/cii/` based on the target system.

| System | Reference File | Items |
|--------|---------------|:-----:|
| Unix/Linux | `references/cii/unix.md` | 67 |
| Windows Server | `references/cii/windows.md` | 64 |
| Web Service | `references/cii/web-service.md` | 26 |
| Security Equipment | `references/cii/security-equip.md` | 23 |
| Network Equipment | `references/cii/network.md` | 38 |
| Control System | `references/cii/control-system.md` | 46 |
| PC | `references/cii/pc.md` | 18 |
| DBMS | `references/cii/database.md` | 26 |
| Mobile | `references/cii/mobile.md` | 4 |
| Web Application | `references/cii/webapp.md` | 21 |
| Virtualization | `references/cii/virtualization.md` | 25 |
| Cloud | `references/cii/cloud.md` | 19 |
| Administrative | `references/cii/admin.md` | 127 |
| Physical | `references/cii/physical.md` | 18 |

### Judgment Criteria
- **Pass**: Security settings properly applied
- **Partial**: Partially implemented, improvement needed
- **Fail**: Vulnerability exists
- **N/A**: Not applicable to the environment

---

## AI Security Branch

Read from `references/ai-security/` based on target audience.

| Target | Reference File |
|--------|---------------|
| Overview | `references/ai-security/overview.md` |
| AI Developer | `references/ai-security/developer.md` |
| Service Provider | `references/ai-security/service-provider.md` |
| User | `references/ai-security/user-guide.md` |

6-stage lifecycle: Planning → Data → Model Dev → Deploy → Monitoring → Decommission

---

## Robot Security Branch

Read from `references/robot-security/` based on the target robot system or concern.

| Topic | Reference File |
|-------|---------------|
| Overview | `references/robot-security/overview.md` |
| SSDF / secure software development | `references/robot-security/ssdf.md` |
| Supply chain security | `references/robot-security/supply-chain.md` |
| IEC 62443 controls (IA, UC, SI, DP, DFR, ER, RA) | `references/robot-security/iec62443.md` |
| Cyber resilience | `references/robot-security/cyber-resilience.md` |
| Wireless security | `references/robot-security/wireless.md` |

Assess the relevant categories for industrial, service, or medical robots and generate a dedicated `reports/robot-security/` summary when robot security is selected.

---

## Space Security Branch

Read from `references/space-security/` based on target space system.

| Topic | Reference File |
|-------|---------------|
| Overview | `references/space-security/overview.md` |
| Access Control & Authentication (AC, IA) | `references/space-security/access-control.md` |
| System & Communication Security (SC, SI) | `references/space-security/system-security.md` |
| Operations & Incident Response (SO, IR) | `references/space-security/operations.md` |
| Governance, Personnel, Physical, Risk, Contingency (PS, PE, RA, SG, CP) | `references/space-security/governance.md` |
| Supply Chain Management (SM) + Threat Scenarios | `references/space-security/supply-chain.md` |

12 domains, 53 items. Standards: CMMC, K-RMF, NIS2, ISMS-P. Generate reports in `reports/space-security/`.

---

## Notes
- Do not modify files during assessment — read-only
- Mark N/A for technologies not present
- Provide specific remediation for each finding
