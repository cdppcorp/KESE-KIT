---
name: check
description: Run a pre-deployment security compliance checklist based on KISA guidelines. Supports CII compliance (70 items), AI security checklists, Robot Security (103 items), and Space Security (12 domains, 53 items). Use when "pre-deploy check", "compliance checklist", "security checklist", "AI security check", "robot security check", "space security check", "satellite compliance", "GSaaS check".
---

# KESE Pre-Deployment Security Compliance Checklist

Run pre-deployment security checks. Auto-selects guideline based on user context.

## Guideline Selection

| # | Guideline | Description |
|---|-----------|-------------|
| 1 | **CII Compliance** | 70-item pre-deployment checklist |
| 2 | **AI Security Checklist** | AI developer/provider verification |
| 3 | **Robot Security Checklist** | Robot system 11 categories, 103 items |
| 4 | **Space Security Checklist** | Satellite/GSaaS/supply chain 12 domains, 53 items |

Servers, infrastructure → **CII** / AI models, LLM → **AI Security** / robots, ROS/ROS2 → **Robot Security** / satellites, ground stations, GSaaS, space supply chain → **Space Security**

---

## CII Branch

Load reference files from `references/cii/` based on detected environment. Check categories: Account Security (15), Access Control (15), Encryption (12), Logging (10), Service Hardening (12), Patch Management (6).

Severity: Critical (deployment blocker) → High → Medium → Low

## AI Security Branch

Load from `references/ai-security/`. Check developer (54 items), service provider, or user checklists by lifecycle phase.

## Robot Security Branch

Load from `references/robot-security/`. Start with `overview.md`, then select one or more category references (`ssdf.md`, `supply-chain.md`, `iec62443.md`, `cyber-resilience.md`, `wireless.md`) based on the robot type, interfaces, and regulatory context.

---

## Space Security Branch

Load from `references/space-security/`. Start with `overview.md`, then select domain references based on the space system type (GSaaS, satellite operator, ground station). Check against CMMC/K-RMF/NIS2/ISMS-P standards.

---

## Rules
- Never skip Critical severity items
- Provide specific file paths and commands for fixes
- Block deployment if pass rate < 60%
