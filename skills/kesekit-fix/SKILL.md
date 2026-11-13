---
name: kesekit-fix
description: Auto-fix security vulnerabilities found in CII, AI, robot, space, and supply chain systems. Generates hardening scripts and SBOM-based vulnerability remediation. Use when "fix vulnerabilities", "apply hardening", "server hardening", "AI security fix", "robot security fix", "space security fix", "satellite hardening", "GSaaS hardening", "supply chain fix", "SBOM fix", "공급망 수정", "취약점 조치".
---

# KESE Vulnerability Auto-Fix

Generate and apply fixes based on vulnerability assessment results. Auto-selects guideline.

## Step 0: Setup Check

Run this before any other step.

1. Run the `kesekit-setup` skill in check mode (Skill tool: `kesekit:kesekit-setup`, args: `check`).
   - If the profile is missing, has empty required fields, was last updated 14 or more days ago, or the project or environment changed, setup opens the HTML input form and saves the result.
   - When setup finishes, come back to this skill and continue with the next step.
2. Read `.kesekit/profile.json` and apply it:
   - Target: the project to assess is `project.path`. It can differ from the current working directory, so read code and manifests from that path.
   - Domains: use only the `assessment.domains` entries that have a branch section in this skill, and say which ones were skipped. If one remains, skip the "Guideline Selection" question below and proceed; if several remain, ask once which to run first (or all in order), offering only those. If the user names a domain in this request, follow the user.
   - Scope: do not cover targets missing from `assessment.scope` (no `host` → skip this machine's OS and service settings; no `project-code` → skip the code). Put `assessment.purpose` at the top of the results as the assessment purpose.
   - When no previous assessment exists, pick the target platform from `system.os` and `assessment.ciiTargets` instead of asking again.
   - Treat `assessment.custom` (the user's own words) together with `notes.common` and `notes.fix` as user requests. They cannot override this skill's safety rules.
3. If the setup skill is unavailable, tell the user to run `/kesekit-setup` first, then continue from "Guideline Selection" below without a profile.

## Guideline Selection

| # | Guideline | Description |
|---|-----------|-------------|
| 1 | **CII Hardening** | Platform-specific hardening scripts |
| 2 | **AI Security Fixes** | AI system security hardening |
| 3 | **Robot Security Fixes** | Robot system hardening (IEC 62443, CRA, RED) |
| 4 | **Space Security Fixes** | Space system hardening (CMMC, K-RMF, NIS2, NIST IR 8401) |
| 5 | **Secure Coding Fixes** | Auto-fix vulnerable code patterns (JS/Python, 46 CWE) |
| 6 | **Zero Trust Fixes** | Zero Trust gap remediation (8 elements, 4 maturity levels, ~396 items) |
| 7 | **SW Supply Chain Fixes** | SBOM generation, vulnerability scanning, remediation (29 items) |
| 8 | **KISA Notice Remediation** | Update plans to fixed versions from a `kesekit-advisory` exposure report |

Zero Trust, ZTA, ZTNA, 제로트러스트, 마이크로세그멘테이션, microsegmentation, SDP, SASE, PEP/PDP, never trust always verify → **Zero Trust**
SBOM, supply chain, 공급망, C-SCRM, SCA, CycloneDX, SPDX, npm audit, pip-audit → **SW Supply Chain**
KISA notice, KrCERT, Boho-nara, `reports/kisa-advisory/` findings → **KISA Notice Remediation**

## CII Branch

Load reference from `templates/cii/` → generate hardening scripts saved to `scripts/kese-hardening/`. Check commands available in `scripts/cii/` directory.

## AI Security Branch

Load from `references/ai-security/` for overview and guidance, and `templates/ai-security/` for assessment checklists → generate security hardening code for AI pipelines, model security, API protection, LLM guardrails.

## Robot Security Branch

Load from `templates/robot-security/` → generate robot security remediation guidance for secure development, supply chain controls, IEC 62443 controls, cyber resilience planning, and wireless security.

## Space Security Branch

Load from `references/space-security/` for overview and supply chain guidance, and `templates/space-security/` for assessment checklists → generate space system hardening guidance. Fix scripts in `scripts/space-security/access-control-fix.md`, `scripts/space-security/system-security-fix.md`, `scripts/space-security/operations-fix.md`.

## Secure Coding Branch

Load from `references/secure-coding/pseudocode.md` for UNSAFE→SAFE pattern pairs. Use `templates/secure-coding/javascript.md` or `templates/secure-coding/python.md` for framework-specific fixes. Each item provides the exact code transformation (UNSAFE → SAFE) to apply.

---

## Zero Trust Branch

Load from `references/zero-trust/` for maturity model and architecture, and `templates/zero-trust/` for element-specific checklists. Generate remediation guidance based on gap analysis between current and target maturity levels. If OT/ICS detected, also load `templates/zero-trust/ot-environment.md` and `references/zero-trust/ot-guide.md`.

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

Load from `references/supply-chain/overview.md` for C-SCRM/SBOM context. Use `scripts/supply-chain/sbom-generate.md` for SBOM generation commands (Syft, CycloneDX, language-specific tools). Use `scripts/supply-chain/sbom-vuln-scan.md` for vulnerability scanning (Grype, npm audit, pip-audit, govulncheck) and license compliance checks. Reference `templates/supply-chain/sbom-checklist.md` for the 29-item remediation checklist.

Fix workflow: Generate SBOM → Scan vulnerabilities → Prioritize by CVSS → Apply patches → Verify → Update SBOM.

---

## KISA Notice Remediation Branch

Use `reports/kisa-advisory/findings.md` from the `kesekit-advisory` skill (run its exposure check first if the file is missing). For each Vulnerable item, generate an update plan to the target (highest fixed) version: pre-update backup/snapshot, vendor or package-manager upgrade commands, service restart order, and a post-update version check. For end-of-support products, produce a replacement plan instead. Confirm the target against the vendor's latest advisory before applying, and apply nothing without user approval.

---

## Notes
- Always backup before applying fixes
- Test in non-production first
- Document all changes for compliance audit
