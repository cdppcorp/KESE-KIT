---
name: kesekit-guide
description: Generate secure coding prompts and guides for AI tools (Claude, ChatGPT, Cursor, Copilot). Creates copy-paste ready prompts for KISA CII, AI security, robot security, and space security (CCSDS, satellite protocols, GSaaS, supply chain). Use when "security guide", "secure coding guide", "AI secure coding", "robot secure coding", "space secure coding", "satellite security guide".
---

# KESE Secure Coding Prompt Generator

Generate secure coding prompts based on KISA guidelines and international standards (OWASP, CWE).

## Guideline Selection

| # | Guideline | Description |
|---|-----------|-------------|
| 1 | **CII Secure Coding** | Traditional vulnerabilities (SQLi, XSS, etc.) |
| 2 | **AI Security Coding** | AI-specific (Prompt Injection, Data Poisoning, etc.) |
| 3 | **Robot Security Coding** | Robot-specific (IEC 62443, firmware, protocols) |
| 4 | **Space Security Coding** | Space-specific (CCSDS, satellite protocols, GSaaS, supply chain) |
| 5 | **Secure Coding (Language)** | Language-specific secure coding (JS, Python, pseudo code) |
| 6 | **Zero Trust Guide** | Zero Trust architecture and maturity assessment guide (8 elements, ~396 items) |

Zero Trust, ZTA, ZTNA, 제로트러스트, 마이크로세그멘테이션, microsegmentation, SDP, SASE, PEP/PDP, never trust always verify → **Zero Trust**

## CII Branch

Reference `templates/cii/webapp.md` for CWE-based patterns. Check commands available in `scripts/cii/` directory. Generate language-specific prompts (Python, JavaScript, Java, Go, etc.) and function-specific prompts (auth, file upload, API security).

## AI Security Branch

Reference `templates/ai-security/developer.md` and `references/ai-security/overview.md`. Generate prompts for: Prompt Injection defense, Data Poisoning prevention, Model Extraction protection, LLM security, RAG pipeline security.

## Robot Security Branch

Reference `templates/robot-security/overview.md` first, then use `ssdf.md`, `supply-chain.md`, `iec62443.md`, `cyber-resilience.md`, or `wireless.md` from `templates/robot-security/` depending on whether the user needs prompts for firmware, ROS/ROS2 nodes, robot APIs, field protocols, supply chain controls, or wireless interfaces.

## Space Security Branch

Reference `references/space-security/overview.md` first, then use domain-specific files from `templates/space-security/` for satellite communication encryption, ground station access control, GSaaS API security, and `references/space-security/supply-chain.md` for SBOM, anti-jamming/anti-spoofing, or CMMC/NIS2/K-RMF compliance.

## Secure Coding (Language) Branch

Reference `references/secure-coding/overview.md` for 7 categories and 49 CWE mappings. Use `references/secure-coding/pseudocode.md` for language-agnostic patterns (46 items, UNSAFE/SAFE pairs). For language-specific prompts, use `templates/secure-coding/javascript.md` (Express.js, Sequelize, Node.js) or `templates/secure-coding/python.md` (Django, Flask, SQLAlchemy).

### Auto-detection
- JavaScript, Node.js, Express, React, Vue → `templates/secure-coding/javascript.md`
- Python, Django, Flask, FastAPI → `templates/secure-coding/python.md`
- Other languages (Go, Java, Rust, C#) → `references/secure-coding/pseudocode.md` (AI adapts patterns)
- General / language-agnostic → `references/secure-coding/pseudocode.md`

## Zero Trust Branch

Reference `references/zero-trust/overview.md` for ZT architecture and `references/zero-trust/maturity-model.md` for maturity definitions. Use `templates/zero-trust/overview.md` for assessment guide. Generate ZT implementation prompts based on element-specific templates. For OT/ICS environments, reference `templates/zero-trust/ot-environment.md` and `references/zero-trust/ot-guide.md`.

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

## Usage

Copy the generated prompt into your AI assistant conversation, then request code.
