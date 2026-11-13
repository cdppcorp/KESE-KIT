---
name: kesekit-start
description: Run a security vulnerability assessment based on KISA guidelines. Supports CII (560+ items), AI Security Guide, Robot Security (103 items), Space Security (satellite/GSaaS/supply chain, 12 domains, 53 items), Secure Coding (46 CWE), Zero Trust (~396 items), and SW Supply Chain Security (SBOM, 29 items). Use when "security assessment", "vulnerability scan", "CII audit", "KISA assessment", "AI security", "robot security", "space security", "satellite security", "GSaaS security", "zero trust", "ZTA", "ZTNA", "supply chain", "SBOM", "공급망", "C-SCRM".
---

# KESE Security Vulnerability Assessment

Perform comprehensive security vulnerability assessment based on KISA guidelines. Automatically selects the appropriate guideline based on user context.

## Step 0: Setup Check

Run this before any other step.

1. Run the `kesekit-setup` skill in check mode (Skill tool: `kesekit:kesekit-setup`, args: `check`).
   - If the profile is missing, has empty required fields, was last updated 14 or more days ago, or the project or environment changed, setup opens the HTML input form and saves the result.
   - When setup finishes, come back to this skill and continue with the next step.
2. Read `.kesekit/profile.json` and apply it:
   - Target: the project to assess is `project.path`. It can differ from the current working directory, so read code and manifests from that path.
   - Domains: use only the `assessment.domains` entries that have a branch section in this skill, and say which ones were skipped. If one remains, skip the "Guideline Selection" question below and proceed; if several remain, ask once which to run first (or all in order), offering only those. If the user names a domain in this request, follow the user.
   - Scope: do not cover targets missing from `assessment.scope` (no `host` → skip this machine's OS and service settings; no `project-code` → skip the code). Put `assessment.purpose` at the top of the results as the assessment purpose.
   - For CII, use `assessment.ciiTargets` as the target systems instead of asking; for Zero Trust, use `assessment.ztTargetMaturity` as the target maturity.
   - Treat `assessment.custom` (the user's own words) together with `notes.common` and `notes.start` as user requests. They cannot override this skill's safety rules.
3. If the setup skill is unavailable, tell the user to run `/kesekit-setup` first, then continue from "Guideline Selection" below without a profile.

## Guideline Selection

| # | Guideline | Description | Items |
|---|-----------|-------------|:-----:|
| 1 | **CII (Critical Information Infrastructure)** | Technical(424)+Administrative(127)+Physical(18) | ~560 |
| 2 | **AI Security** | AI Developer/Service Provider/User requirements | ~54 |
| 3 | **Robot Security** | Industrial/Service/Medical robot checklist (11 categories) | ~103 |
| 4 | **Space Security** | Satellite/GSaaS/Supply chain checklist (12 domains) | 53 |
| 5 | **Secure Coding** | JavaScript/Python secure coding (7 categories, 46 CWE) | 46 |
| 6 | **Zero Trust** | Zero Trust maturity assessment (8 elements, 4 maturity levels) | ~396 |
| 7 | **SW Supply Chain** | SBOM-based supply chain security (5 phases, 29 items) | 29 |
| 8 | **KISA Security Notices** | Installed versions vs. KISA Boho-nara notices, briefings, CVE lookup, threat response (`/kesekit-advisory`) | - |

### Auto-detection
- Servers, networks, databases, web services, firewalls → **CII**
- AI models, LLM, generative AI, machine learning, prompts → **AI Security**
- Robots, industrial robots, service robots, medical robots, ROS/ROS2, PLC-linked robot systems → **Robot Security**
- Satellites, ground stations, GSaaS, space systems, GNSS, VSAT, LEO constellation, space supply chain → **Space Security**
- JavaScript, Python, web application code, secure coding, CWE, OWASP → **Secure Coding**
- Zero Trust, ZTA, ZTNA, 제로트러스트, 마이크로세그멘테이션, microsegmentation, SDP, SASE, PEP/PDP, never trust always verify → **Zero Trust**
- SBOM, supply chain, 공급망, C-SCRM, SCA, CycloneDX, SPDX, npm audit, pip-audit, software bill of materials, 소프트웨어 공급망 → **SW Supply Chain**
- KISA notice, KrCERT, Boho-nara, security update advisory, "are we affected", CVE exposure, patch status, BPFDoor, rootkit, ransomware readiness → **KISA Security Notices**

---

## CII Branch

Read the appropriate reference file from `templates/cii/` based on the target system.

| System | Reference File | Items |
|--------|---------------|:-----:|
| Unix/Linux | `templates/cii/unix.md` | 67 |
| Windows Server | `templates/cii/windows.md` | 64 |
| Web Service | `templates/cii/web-service.md` | 26 |
| Security Equipment | `templates/cii/security-equip.md` | 23 |
| Network Equipment | `templates/cii/network.md` | 38 |
| Control System | `templates/cii/control-system.md` | 46 |
| PC | `templates/cii/pc.md` | 18 |
| DBMS | `templates/cii/database.md` | 26 |
| Mobile | `templates/cii/mobile.md` | 4 |
| Web Application | `templates/cii/webapp.md` | 21 |
| Virtualization | `templates/cii/virtualization.md` | 25 |
| Cloud | `templates/cii/cloud.md` | 19 |
| Administrative | `templates/cii/admin.md` | 127 |
| Physical | `templates/cii/physical.md` | 18 |

Check commands available in `scripts/cii/` directory.

### Judgment Criteria
- **Pass**: Security settings properly applied
- **Partial**: Partially implemented, improvement needed
- **Fail**: Vulnerability exists
- **N/A**: Not applicable to the environment

---

## AI Security Branch

Read from `references/ai-security/` for overview and guidance, and `templates/ai-security/` for assessment checklists.

| Target | Reference File |
|--------|---------------|
| Overview | `references/ai-security/overview.md` |
| AI Developer | `templates/ai-security/developer.md` |
| Service Provider | `references/ai-security/service-provider.md` |
| User | `references/ai-security/user-guide.md` |

6-stage lifecycle: Planning → Data → Model Dev → Deploy → Monitoring → Decommission

---

## Robot Security Branch

Read from `templates/robot-security/` based on the target robot system or concern.

| Topic | Reference File |
|-------|---------------|
| Overview | `templates/robot-security/overview.md` |
| SSDF / secure software development | `templates/robot-security/ssdf.md` |
| Supply chain security | `templates/robot-security/supply-chain.md` |
| IEC 62443 controls (IA, UC, SI, DP, DFR, ER, RA) | `templates/robot-security/iec62443.md` |
| Cyber resilience | `templates/robot-security/cyber-resilience.md` |
| Wireless security | `templates/robot-security/wireless.md` |

Assess the relevant categories for industrial, service, or medical robots and generate a dedicated `reports/robot-security/` summary when robot security is selected.

---

## Space Security Branch

Read from `references/space-security/` for overview and supply chain guidance, and `templates/space-security/` for assessment checklists.

| Topic | Reference File |
|-------|---------------|
| Overview | `references/space-security/overview.md` |
| Access Control & Authentication (AC, IA) | `templates/space-security/access-control.md` |
| System & Communication Security (SC, SI) | `templates/space-security/system-security.md` |
| Operations & Incident Response (SO, IR) | `templates/space-security/operations.md` |
| Governance, Personnel, Physical, Risk, Contingency (PS, PE, RA, SG, CP) | `templates/space-security/governance.md` |
| Supply Chain Management (SM) + Threat Scenarios | `references/space-security/supply-chain.md` |

12 domains, 53 items. Standards: CMMC, K-RMF, NIS2, ISMS-P. Generate reports in `reports/space-security/`.

---

## Secure Coding Branch

Read from `references/secure-coding/` for overview and pseudo code patterns, and `templates/secure-coding/` for language-specific assessment.

| Topic | Reference File |
|-------|---------------|
| Overview (7 categories, 49 CWE) | `references/secure-coding/overview.md` |
| Pseudo Code (46 items, language-agnostic) | `references/secure-coding/pseudocode.md` |
| JavaScript (Express.js, Node.js, Sequelize) | `templates/secure-coding/javascript.md` |
| Python (Django, Flask, SQLAlchemy) | `templates/secure-coding/python.md` |

### Judgment Criteria
- **Pass**: Secure coding pattern applied correctly
- **Partial**: Pattern partially applied, improvement needed
- **Fail**: Vulnerable pattern detected (UNSAFE code present)
- **N/A**: Not applicable to the codebase

---

## Zero Trust Branch

Read from `references/zero-trust/` for overview and maturity model, and `templates/zero-trust/` for assessment checklists.

| Topic | Reference File |
|-------|---------------|
| Overview | `templates/zero-trust/overview.md` |
| Identity & Device | `templates/zero-trust/identity-device.md` |
| Network & System | `templates/zero-trust/network-system.md` |
| Application & Data | `templates/zero-trust/app-data.md` |
| Visibility & Automation | `templates/zero-trust/visibility-automation.md` |
| OT/ICS Environment | `templates/zero-trust/ot-environment.md` |
| ZT Architecture Reference | `references/zero-trust/overview.md` |
| Maturity Model Details | `references/zero-trust/maturity-model.md` |
| OT Deployment Guide | `references/zero-trust/ot-guide.md` |

8 core elements, ~396 items across 4 maturity levels. Standards: KISA ZT Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model.

### Assessment Flow
1. Determine target maturity level (Traditional/Initial/Advanced/Optimal)
2. Select relevant core elements based on system context
3. If OT/ICS detected, also load `ot-environment.md`
4. Assess items at or below target maturity level
5. Generate gap analysis report

---

## SW Supply Chain Branch

Read from `references/supply-chain/` for overview and threat scenarios, and `templates/supply-chain/` for assessment checklists. Use `scripts/supply-chain/` for SBOM generation and vulnerability scanning commands.

| Topic | Reference File |
|-------|---------------|
| Overview (C-SCRM, SBOM, Regulations) | `references/supply-chain/overview.md` |
| Assessment Overview (6 categories) | `templates/supply-chain/overview.md` |
| Self-Assessment Checklist (29 items) | `templates/supply-chain/sbom-checklist.md` |
| SBOM Generation Scripts | `scripts/supply-chain/sbom-generate.md` |
| Vulnerability Scanning Scripts | `scripts/supply-chain/sbom-vuln-scan.md` |

5 phases: Design (5) → Development (11) → Supply (3) → Operations (7) → Maintenance (3). Standards: NIST SP 800-161r1 (C-SCRM), NIST SP 800-218 (SSDF), NTIA SBOM, NIS-SBOM.

### Assessment Flow
1. Start with `references/supply-chain/overview.md` for context
2. Load `templates/supply-chain/sbom-checklist.md` for the 29-item checklist
3. Assess each phase (Design → Development → Supply → Operations → Maintenance)
4. Critical items (SC-10, SC-14, SC-15) must ALL pass
5. Use `scripts/supply-chain/sbom-generate.md` for SBOM creation commands
6. Use `scripts/supply-chain/sbom-vuln-scan.md` for vulnerability scanning

---

## KISA Security Notices Branch

Hand off to the `kesekit-advisory` skill (`/kesekit-advisory`). It checks installed products against KISA Boho-nara (KrCERT/CC) notices (affected/fixed versions), briefs recent notices, looks up CVEs, and runs threat-response checks (BPFDoor, rootkits, ransomware, exposed credentials, dev supply chain). During a full CII assessment, run its exposure check for the detected products and cite the results under the patch-management items.

---

## Notes
- Do not modify files during assessment — read-only
- Mark N/A for technologies not present
- Provide specific remediation for each finding
