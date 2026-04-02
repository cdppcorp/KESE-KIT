# System & Communication Security Checklist

> Domains: SC (System & Communication Security, 7 items) + SI (System & Information Integrity, 4 items)

## SC — System & Communication Security (7 Items)

| ID | Item | Purpose | Key Verification Points |
|----|------|---------|------------------------|
| SC-01 | Boundary Protection | Block unauthorized communications at boundaries | Network segmentation, DMZ deployment, communication encryption/monitoring, deny-all ACL |
| SC-02 | Security Engineering & Function Separation | Defense-in-depth, eliminate single points of failure | Security engineering principles, admin/user function separation, Secure by Design |
| SC-03 | Stored & Transmitted Information Security | Protect command/telemetry/log confidentiality and integrity | Storage encryption, uplink/downlink encryption, shared resource protection |
| SC-04 | Communication Security | Establish/maintain/terminate secure sessions | Default deny policy, authenticated/integrity-checked channels, session timeout |
| SC-05 | Encryption | Apply cryptographic algorithms and manage keys | Approved algorithms, key lifecycle management (create/distribute/store/retire) |
| SC-06 | Collaborative Computing Devices | Prevent remote camera/mic activation, prevent leaks | Device inventory, remote activation blocked, LED indicator required |
| SC-07 | Mobile Code & VoIP Control | Prevent malicious code execution and unauthorized VoIP | Mobile code execution control, VoIP usage restriction, monitoring |

### SC Protection Measures

| Category | Measures |
|----------|----------|
| Network Segmentation | Physical/logical separation, DMZ for public servers, satellite-control/operations/internet isolation |
| Encryption Standards | AES-256/ARIA-256, TLS 1.2+, IPsec VPN, CCSDS 352.0-B-2 for space systems |
| Integrity Verification | Digital signatures, HMAC, memory/buffer initialization |
| Session Management | mTLS, split-tunneling blocked, session ID rotation, 2-30 min timeout |
| Cryptographic Keys | AES-256, SHA-256+, RSA-4096+; PROHIBIT TDEA/MD5/SHA-1; full key lifecycle management |
| Code Control | ActiveX/Java Runtime disabled, script whitelisting, signed code only, SRTP for VoIP |

## SI — System & Information Integrity (4 Items)

| ID | Item | Purpose | Key Verification Points |
|----|------|---------|------------------------|
| SI-01 | Vulnerability Scanning & Flaw Remediation | Identify and fix system/application vulnerabilities | Periodic scanning, immediate scan on new vulnerabilities, flaw identification/remediation/reporting |
| SI-02 | Malicious Code Prevention | Prevent virus/worm/ransomware infiltration | Anti-malware on all systems, periodic/real-time scanning, signature updates |
| SI-03 | Security Alerts & Advisories | Monitor and respond to security alerts | Continuous monitoring of KISA/NCSC/CISA/NIST NVD, impact analysis, patch/hardening |
| SI-04 | System & Communication Traffic Monitoring | Detect abnormal traffic in real-time | Monitoring policy, inbound/outbound monitoring, result analysis/response |

### SI Protection Measures

| Measure | Detail |
|---------|--------|
| Vulnerability Management | Network/server/security/app/web scanning, CWE/CVE-based, prioritized remediation |
| Anti-Malware | Enterprise AV on all assets, daily+ updates, P2P/webhard blocked, central management |
| Alert Monitoring | RSS/email subscription to KISA/CISA/NVD, internal notification chain, patch within SLA |
| Traffic Monitoring | IDS/IPS at boundaries, access/security/network log integration, automated alerting |

## Total: 11 Items (SC: 7 + SI: 4)
