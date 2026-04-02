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

## Notes
- Always backup before applying fixes
- Test in non-production first
- Document all changes for compliance audit
