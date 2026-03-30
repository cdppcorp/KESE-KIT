---
name: fix
description: Auto-fix security vulnerabilities found in CII, AI, and robot systems. Generates hardening guidance for Unix/Linux, Windows, web servers, databases, AI systems, and robot platforms. Applies secure configurations based on KISA guidelines and related standards. Use when "fix vulnerabilities", "secure the system", "apply hardening", "server hardening", "AI security fix", "robot security fix".
---

# KESE Vulnerability Auto-Fix

Generate and apply fixes based on vulnerability assessment results. Auto-selects guideline.

## Guideline Selection

| # | Guideline | Description |
|---|-----------|-------------|
| 1 | **CII Hardening** | Platform-specific hardening scripts |
| 2 | **AI Security Fixes** | AI system security hardening |
| 3 | **Robot Security Fixes** | Robot system hardening (IEC 62443, CRA, RED) |

## CII Branch

Load reference from `references/cii/` → generate hardening scripts saved to `scripts/kese-hardening/`.

## AI Security Branch

Load from `references/ai-security/` → generate security hardening code for AI pipelines, model security, API protection, LLM guardrails.

## Robot Security Branch

Load from `references/robot-security/` → generate robot security remediation guidance for secure development, supply chain controls, IEC 62443 controls, cyber resilience planning, and wireless security.

## Notes
- Always backup before applying fixes
- Test in non-production first
- Document all changes for compliance audit
