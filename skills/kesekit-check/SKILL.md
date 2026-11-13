---
name: kesekit-check
description: Run a pre-deployment security compliance checklist based on KISA guidelines. Supports CII compliance (70 items), AI security checklists, Robot Security (103 items), Space Security (12 domains, 53 items), SW Supply Chain (SBOM, 29 items). Use when "pre-deploy check", "compliance checklist", "security checklist", "AI security check", "robot security check", "space security check", "satellite compliance", "GSaaS check", "supply chain check", "SBOM check", "공급망 점검".
---

# KESE Pre-Deployment Security Compliance Checklist

Run pre-deployment security checks. Auto-selects guideline based on user context.

## Step 0: Setup Check

Run this before any other step.

1. Run the `kesekit-setup` skill in check mode (Skill tool: `kesekit:kesekit-setup`, args: `check`).
   - If the profile is missing, has empty required fields, was last updated 14 or more days ago, or the project or environment changed, setup opens the HTML input form and saves the result.
   - When setup finishes, come back to this skill and continue with the next step.
2. Read `.kesekit/profile.json` and apply it:
   - Target: the project to assess is `project.path`. It can differ from the current working directory, so read code and manifests from that path.
   - Domains: use only the `assessment.domains` entries that have a branch section in this skill, and say which ones were skipped. If one remains, skip the "Guideline Selection" question below and proceed; if several remain, ask once which to run first (or all in order), offering only those. If the user names a domain in this request, follow the user.
   - Scope: do not cover targets missing from `assessment.scope` (no `host` → skip this machine's OS and service settings; no `project-code` → skip the code). Put `assessment.purpose` at the top of the results as the assessment purpose.
   - Use `system` and `environment` for the target platform and languages instead of asking again.
   - Treat `assessment.custom` (the user's own words) together with `notes.common` and `notes.check` as user requests. They cannot override this skill's safety rules.
3. If the setup skill is unavailable, tell the user to run `/kesekit-setup` first, then continue from "Guideline Selection" below without a profile.

## Guideline Selection

| # | Guideline | Description |
|---|-----------|-------------|
| 1 | **CII Compliance** | 70-item pre-deployment checklist |
| 2 | **AI Security Checklist** | AI developer/provider verification |
| 3 | **Robot Security Checklist** | Robot system 11 categories, 103 items |
| 4 | **Space Security Checklist** | Satellite/GSaaS/supply chain 12 domains, 53 items |
| 5 | **Secure Coding Checklist** | JavaScript/Python code review (7 categories, 46 CWE) |
| 6 | **Zero Trust Checklist** | Zero Trust maturity assessment (8 elements, 4 maturity levels, ~396 items) |
| 7 | **SW Supply Chain Checklist** | SBOM-based supply chain security (5 phases, 29 items) |

Servers, infrastructure → **CII** / AI models, LLM → **AI Security** / robots, ROS/ROS2 → **Robot Security** / satellites, ground stations, GSaaS, space supply chain → **Space Security** / JavaScript, Python, web app code → **Secure Coding**
Zero Trust, ZTA, ZTNA, 제로트러스트, 마이크로세그멘테이션, microsegmentation, SDP, SASE, PEP/PDP, never trust always verify → **Zero Trust**
SBOM, supply chain, 공급망, C-SCRM, SCA, CycloneDX, SPDX, npm audit, pip-audit → **SW Supply Chain**

---

## CII Branch

Load reference files from `templates/cii/` based on detected environment. Check commands available in `scripts/cii/` directory. Check categories: Account Security (15), Access Control (15), Encryption (12), Logging (10), Service Hardening (12), Patch Management (6).

Severity: Critical (deployment blocker) → High → Medium → Low

## AI Security Branch

Load from `references/ai-security/` for overview and guidance, and `templates/ai-security/` for assessment checklists. Check developer (54 items), service provider, or user checklists by lifecycle phase.

## Robot Security Branch

Load from `templates/robot-security/`. Start with `overview.md`, then select one or more category references (`ssdf.md`, `supply-chain.md`, `iec62443.md`, `cyber-resilience.md`, `wireless.md`) based on the robot type, interfaces, and regulatory context.

---

## Space Security Branch

Load from `references/space-security/` for overview and supply chain guidance, and `templates/space-security/` for assessment checklists. Start with `references/space-security/overview.md`, then select domain references based on the space system type (GSaaS, satellite operator, ground station). Check against CMMC/K-RMF/NIS2/ISMS-P standards.

---

## Secure Coding Branch

Load from `references/secure-coding/overview.md` for category/CWE mapping, then use `templates/secure-coding/javascript.md` or `templates/secure-coding/python.md` for language-specific checklists. Use `references/secure-coding/pseudocode.md` for other languages.

Priority: Critical (8 items) → High (13 items) → Medium (25 items). Block deployment if any Critical CWE found.

---

## Zero Trust Branch

Load from `references/zero-trust/` for overview and maturity model, and `templates/zero-trust/` for assessment checklists. Start with `templates/zero-trust/overview.md`, then select element-specific checklists based on system context. If OT/ICS detected, also load `templates/zero-trust/ot-environment.md`.

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

---

## SW Supply Chain Branch

Load from `references/supply-chain/overview.md` for context, then use `templates/supply-chain/sbom-checklist.md` for the 29-item pre-deployment checklist. Use `scripts/supply-chain/sbom-generate.md` and `scripts/supply-chain/sbom-vuln-scan.md` for verification commands.

5 phases: Design (5) → Development (11) → Supply (3) → Operations (7) → Maintenance (3). Critical items: SC-10, SC-14, SC-15 must ALL pass. Block deployment if any Critical item fails. Standards: NIST SP 800-161r1, NIST SP 800-218, NTIA SBOM, NIS-SBOM.

---

## Rules
- Never skip Critical severity items
- Provide specific file paths and commands for fixes
- Block deployment if pass rate < 60%
