---
name: kesekit-fix
description: Auto-fix security vulnerabilities found in CII, AI, robot, and space systems. Generates hardening scripts for Unix/Linux, Windows, web servers, databases, AI, robot, and space infrastructure (satellite/GSaaS/ground station). Use when "fix vulnerabilities", "apply hardening", "server hardening", "AI security fix", "robot security fix", "space security fix", "satellite hardening", "GSaaS hardening".
---

# KESE Vulnerability Auto-Fix

Generate and apply fixes based on vulnerability assessment results. Auto-selects guideline.

## Guideline Selection

| # | Guideline | Description |
|---|-----------|-------------|
| 1 | **CII Hardening** | Platform-specific hardening scripts |
| 2 | **AI Security Fixes** | AI system security hardening |
| 3 | **Robot Security Fixes** | Robot system hardening (IEC 62443, CRA, RED) |
| 4 | **Space Security Fixes** | Space system hardening (CMMC, K-RMF, NIS2, NIST IR 8401) |
| 5 | **Secure Coding Fixes** | Auto-fix vulnerable code patterns (JS/Python, 46 CWE) |
| 6 | **Zero Trust Fixes** | Zero Trust gap remediation (8 elements, 4 maturity levels, ~396 items) |

Zero Trust, ZTA, ZTNA, 제로트러스트, 마이크로세그멘테이션, microsegmentation, SDP, SASE, PEP/PDP, never trust always verify → **Zero Trust**

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

## Notes
- Always backup before applying fixes
- Test in non-production first
- Document all changes for compliance audit
