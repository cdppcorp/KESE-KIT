---
name: guide
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

## CII Branch

Reference `templates/cii/webapp.md` for CWE-based patterns. Check commands available in `scripts/cii/` directory. Generate language-specific prompts (Python, JavaScript, Java, Go, etc.) and function-specific prompts (auth, file upload, API security).

## AI Security Branch

Reference `templates/ai-security/developer.md` and `references/ai-security/overview.md`. Generate prompts for: Prompt Injection defense, Data Poisoning prevention, Model Extraction protection, LLM security, RAG pipeline security.

## Robot Security Branch

Reference `templates/robot-security/overview.md` first, then use `ssdf.md`, `supply-chain.md`, `iec62443.md`, `cyber-resilience.md`, or `wireless.md` from `templates/robot-security/` depending on whether the user needs prompts for firmware, ROS/ROS2 nodes, robot APIs, field protocols, supply chain controls, or wireless interfaces.

## Space Security Branch

Reference `references/space-security/overview.md` first, then use domain-specific files from `templates/space-security/` for satellite communication encryption, ground station access control, GSaaS API security, and `references/space-security/supply-chain.md` for SBOM, anti-jamming/anti-spoofing, or CMMC/NIS2/K-RMF compliance.

## Usage

Copy the generated prompt into your AI assistant conversation, then request code.
