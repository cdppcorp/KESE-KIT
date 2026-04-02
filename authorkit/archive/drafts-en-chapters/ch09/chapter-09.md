# Chapter 9. Security Equipment Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Security equipment (Firewall, IDS/IPS, WAF) is a core element of security. This chapter covers 19 assessment items (S-01 ~ S-19).

```
┌─────────────────────────────────────────────────────────────────┐
│        Security Equipment Vulnerability Assessment Domains (19)  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Security Equipment Types                  │ │
│  │                                                            │ │
│  │   ┌──────────┐    ┌──────────┐    ┌──────────┐           │ │
│  │   │ Firewall │    │ IDS/IPS  │    │   WAF    │           │ │
│  │   │          │    │Intrusion │    │   Web    │           │ │
│  │   │          │    │Detection/│    │Application│          │ │
│  │   │          │    │Prevention│    │ Firewall │           │ │
│  │   └────┬─────┘    └────┬─────┘    └────┬─────┘           │ │
│  │        │               │               │                  │ │
│  │        └───────────────┼───────────────┘                  │ │
│  │                        │                                  │ │
│  └────────────────────────┼──────────────────────────────────┘ │
│                           │                                     │
│           ┌───────────────┼───────────────┐                    │
│           │               │               │                    │
│           ▼               ▼               ▼                    │
│    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│    │Account/Access│ │ Patch/Log  │ │   Feature   │            │
│    │  Management │ │ Management │ │  Management │            │
│    │  S-01~S-08  │ │  S-09~S-12 │ │  S-13~S-19  │            │
│    │    (8)      │ │    (4)     │ │    (7)      │            │
│    │             │ │            │ │             │            │
│    │• Default    │ │• Firmware  │ │• Policy     │            │
│    │  accounts   │ │• Signature │ │  optimization│           │
│    │• Admin      │ │• Log       │ │• Ruleset    │            │
│    │  access     │ │  retention │ │  management │            │
│    └─────────────┘ └─────────────┘ └─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | S-01 ~ S-05 | 5 |
| Access Management | S-06 ~ S-08 | 3 |
| Patch Management | S-09 | 1 |
| Log Management | S-10 ~ S-12 | 3 |
| Feature Management | S-13 ~ S-19 | 7 |

---

## 9-1. Firewall Assessment (S-01 ~ S-19)

### S-01. Change Default Account Password

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | Firewall, IDS/IPS, UTM |
| **Criteria** | Good: Changed / Vulnerable: Default |

#### Key Security Equipment Default Accounts

| Equipment | Default Account | Action |
|-----------|-----------------|--------|
| Palo Alto | admin/admin | Change required |
| FortiGate | admin/(none) | Set password |
| Cisco ASA | - | Set enable password |

---

### S-06. Management Access Control

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Restrict management interface access |

#### Recommended Settings

- Separate management interface on isolated network
- Allow access only from specific IPs
- Use SSH or HTTPS (disable HTTP/Telnet)

---

### S-13. Policy Optimization

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Remove unnecessary allow policies |

#### Check Points

| Item | Check For |
|------|-----------|
| Any-Any policies | Source/destination is Any |
| Unused policies | Hit count is 0 |
| Duplicate policies | Same effect duplicated |
| Order issues | Broader policies above specific ones |

> **TIP**
> Regularly review policies and remove unused ones.

---

## 9-2. IDS/IPS Assessment

### Signature Updates

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Detect latest attack patterns |

#### Check Points

- Auto-update configuration
- Update frequency check (daily recommended)
- Last update date verification

---

## 9-3. WAF Assessment

### Web Attack Defense Settings

| Attack Type | Defense Setting |
|-------------|-----------------|
| SQL Injection | Detect/Block |
| XSS | Detect/Block |
| CSRF | Detect |
| File Inclusion | Detect/Block |
| Command Injection | Detect/Block |

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password change | Highest |
| Access Management | Management interface restriction | Highest |
| Feature Management | Policy optimization, signature updates | High |

---

*Next Chapter: Chapter 10. Virtualization and Cloud Assessment*
