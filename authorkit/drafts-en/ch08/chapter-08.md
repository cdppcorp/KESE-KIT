# Chapter 8. Network Equipment Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Network equipment (routers, switches) is the core of infrastructure. This chapter covers 40 assessment items (N-01 ~ N-40).

```
┌─────────────────────────────────────────────────────────────────┐
│        Network Equipment Vulnerability Assessment Domains (40)   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │Network Equipment│                          │
│                    │ Router | Switch │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│     ┌───────────────────────┼───────────────────────┐           │
│     │           │           │           │           │           │
│     ▼           ▼           ▼           ▼           ▼           │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐         │
│ │Account│  │ Access│  │ Patch │  │  Log  │  │Feature│         │
│ │ Mgmt  │  │ Mgmt  │  │ Mgmt  │  │ Mgmt  │  │ Mgmt  │         │
│ │N-01~10│  │N-11~18│  │ N-19  │  │N-20~24│  │N-25~40│         │
│ │ (10)  │  │  (8)  │  │  (1)  │  │  (5)  │  │ (16)  │         │
│ │       │  │       │  │       │  │       │  │       │         │
│ │•Default│ │• ACL  │  │• Firm-│  │• Sys- │  │• SNMP │         │
│ │ acct  │  │• SSH  │  │  ware │  │  log  │  │• CDP  │         │
│ │•Encrypt│ │•Telnet│  │       │  │• NTP  │  │•Unnec-│         │
│ │       │  │ block │  │       │  │       │  │ essary│         │
│ │       │  │       │  │       │  │       │  │ svc   │         │
│ └───────┘  └───────┘  └───────┘  └───────┘  └───────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | N-01 ~ N-10 | 10 |
| Access Management | N-11 ~ N-18 | 8 |
| Patch Management | N-19 | 1 |
| Log Management | N-20 ~ N-24 | 5 |
| Feature Management | N-25 ~ N-40 | 16 |

---

## 8-1. Account Management (N-01 ~ N-10)

### N-01. Change Default Account Password

| Item | Content |
|------|---------|
| **Severity** | High |
| **Criteria** | Good: Default password changed / Vulnerable: Default used |

#### Cisco Equipment Default Accounts

| Account | Default Password | Action |
|---------|------------------|--------|
| cisco | cisco | Change required |
| admin | admin | Change required |
| enable | (none) | Configuration required |

#### Remediation (Cisco IOS)

```
enable
configure terminal
username admin privilege 15 secret [strong_password]
enable secret [strong_password]
```

---

### N-04. Encrypt Stored Passwords

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent plaintext passwords in config files |

#### Assessment Method (Cisco)

```
show running-config | include password
# "password 7" or plaintext indicates vulnerability
```

#### Remediation

```
configure terminal
service password-encryption
# Use enable secret instead of enable password
enable secret [password]
```

---

## 8-2. Access Management (N-11 ~ N-18)

### N-11. Restrict Remote Access (ACL)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Allow access only from management networks |

#### Remediation (Cisco)

```
! Create management ACL
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 deny any log

! Apply to VTY lines
line vty 0 4
 access-class 10 in
 transport input ssh
```

---

### N-12. Use SSH (Disable Telnet)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Use encrypted management access |

#### Remediation (Cisco)

```
! Enable SSH
hostname Router1
ip domain-name example.com
crypto key generate rsa modulus 2048
ip ssh version 2

! Disable Telnet
line vty 0 4
 transport input ssh
```

---

## 8-3. Patch Management (N-19)

### N-19. Apply Latest Firmware

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Patch known vulnerabilities |

#### Version Check (Cisco)

```
show version
```

> **WARNING**
> Always backup current configuration before firmware upgrade.

---

## 8-4. Log Management (N-20 ~ N-24)

### N-20. Configure Logging

#### Remediation (Cisco)

```
! Syslog server configuration
logging host 192.168.1.100
logging trap informational
logging facility local7

! Add timestamps
service timestamps log datetime msec
```

---

## 8-5. Feature Management (N-25 ~ N-40)

### N-25. SNMP Security Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access via SNMP |

#### Remediation

```
! Delete default communities
no snmp-server community public
no snmp-server community private

! Use complex community or SNMPv3
snmp-server community [complex_string] RO 10
snmp-server group v3group v3 priv
snmp-server user v3user v3group v3 auth sha [auth_password] priv aes 256 [priv_password]
```

---

### N-30. Disable Unnecessary Services

#### Recommended to Disable

```
no ip http server
no ip http secure-server
no cdp run
no ip source-route
no service tcp-small-servers
no service udp-small-servers
no ip finger
no ip bootp server
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password, encrypted storage | Highest |
| Access Management | SSH usage, ACL configuration | Highest |
| Patch Management | Latest firmware | High |
| Log Management | Syslog configuration | Medium |
| Feature Management | SNMP security, disable unnecessary services | High |

---

*Next Chapter: Chapter 9. Security Equipment Assessment*
