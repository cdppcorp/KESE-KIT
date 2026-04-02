# System & Communication Security — Fix Scripts

> Hardening for SC-01~SC-07, SI-01~SI-04

## SC-01: Boundary Protection

### Network Segmentation
```
Zone Layout:
┌──────────────────────────────────────┐
│  DMZ          │ Web Server, Mail     │
├───────────────┼──────────────────────┤
│  Operations   │ Servers, Security    │
├───────────────┼──────────────────────┤
│  Development  │ Dev/Test servers     │
├───────────────┼──────────────────────┤
│  External     │ Contractors, Public  │
└──────────────────────────────────────┘

# Firewall default deny
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP
# Then add specific ALLOW rules
```

### Satellite Network Isolation
- Physically separate: satellite control network / operations network / internet network
- Use **one-way transfer device** for control → satellite communication path
- VDI virtualization for logical separation where physical not feasible

---

## SC-03: Stored & Transmitted Information Security

### Encryption Standards
| Use Case | Algorithm | Key Size | Standard |
|----------|-----------|:--------:|----------|
| Data at rest | AES-256 / ARIA-256 | 256-bit | CCSDS mandatory |
| Legacy systems | AES-128 (minimum) | 128-bit | CCSDS allowed |
| Integrity | HMAC-SHA-256 | - | CCSDS |
| Digital signature | RSA-4096+ | 4096-bit | CCSDS recommended |
| Hashing | SHA-256/384/512 | - | All standards |

### Prohibited Algorithms
```
BANNED: TDEA (3DES), MD5, SHA-1 (new systems)
```

### Korean Domestic Algorithms
```
Symmetric: SEED, HIGHT, ARIA-128/192/256, LEA-128/192/256
Public key: RSAES-OAEP (2048-bit minimum)
Hash: SHA-224/256/384/512
```

---

## SC-04: Communication Security

### Firewall Policy
```bash
# Default Deny → Exception Allow
iptables -P INPUT DROP
iptables -P FORWARD DROP

# Define allowed traffic (Source, Dest, Port, Protocol, Direction)
iptables -A INPUT -s 10.0.1.0/24 -d 10.0.2.0/24 -p tcp --dport 443 -j ACCEPT

# Block split tunneling on VPN
# OpenVPN: push "redirect-gateway def1"
# Block NAT/port forwarding from external to internal (principle)
```

### Session ID Security
| Requirement | Setting |
|-------------|---------|
| Session ID length | Minimum **128 bits** |
| Algorithm | Cryptographically secure PRNG |
| URL exposure | **Prohibited** (no URL rewrite) |
| On login | Destroy old session → issue new ID |
| Timeout (critical) | **2-5 minutes** |
| Timeout (standard) | **15-30 minutes** |

### TLS Configuration
```bash
# nginx.conf - enforce TLS 1.2+
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers on;

# New systems: TLS 1.3+ recommended
```

---

## SC-05: Encryption Key Lifecycle

### Key Management (4 phases)
```
Phase 1: Preparation  → Key generation (secure RNG), distribution
Phase 2: Operation     → Active use, rotation schedule
Phase 3: Suspension    → Inactive, archived, recoverable
Phase 4: Destruction   → Secure deletion, audit trail
```

### Rules
- **NEVER** store keys in source code as plaintext
- Minimum access, all access logged
- Use HSM (Hardware Security Module) for critical keys
- Satellite communication keys: follow CCSDS 352.0-B-2

---

## SC-07: Mobile Code & VoIP

### Mobile Code Control
```powershell
# Windows - Disable ActiveX, Java Runtime in operational environment
# GPO: Computer Configuration > Administrative Templates > Windows Components > Internet Explorer > Security
# → Disable "Run ActiveX controls and plug-ins": Enabled

# PowerShell execution logging
Set-ExecutionPolicy AllSigned
# Enable script block logging in GPO
```

### VoIP Control
```bash
# Block VoIP protocols by default
iptables -A INPUT -p udp --dport 5060 -j DROP   # SIP
iptables -A INPUT -p udp --dport 5004 -j DROP   # RTP
iptables -A INPUT -p udp --dport 5005 -j DROP   # RTCP

# If VoIP allowed (internal only): enforce SRTP
```

---

## SI-01: Vulnerability Scanning

### Scan Schedule
| Asset Criticality | Frequency |
|-------------------|-----------|
| Critical (satellite control) | Quarterly |
| High (ground station) | Semi-annual |
| Standard | Annual |
| On new vulnerability disclosure | Immediate |

### Reference Sources
| Source | URL/Description |
|--------|----------------|
| KISA KrCERT/CC | Korean vulnerability alerts |
| NCSC | National cyber threat analysis |
| CISA | US-CERT alerts, ICS advisories |
| NIST NVD | CVE database, CVSS scores |

---

## SI-02: Malicious Code Prevention
```bash
# Auto-update AV signatures (daily minimum)
# Disable USB autorun
echo "install usb-storage /bin/true" >> /etc/modprobe.d/disable-usb.conf

# Block P2P, webhard applications
iptables -A OUTPUT -p tcp --dport 6881:6889 -j DROP  # BitTorrent
```

---

## GSaaS-Specific Security Solutions

### Anti-Jamming
| Technique | Description |
|-----------|-------------|
| Frequency Hopping | Rapidly switch frequencies to avoid jamming |
| Spread Spectrum | Spread signal across wide bandwidth |
| LPI Waveform | Low Probability of Intercept |
| Antenna diversity | Redundant antenna systems |
| Frequency diversity | Redundant frequency channels |
| Drone countermeasures | Drone jammer, detection radar |

### GSaaS Network Architecture
```
[Satellite] ←→ [Antenna Zone] ←IPSec VPN→ [Ground Station] ←IPSec VPN→ [Cloud]
                                                                            ↑
                                                               [Satellite Operator]
                                                               (SSL VPN + MFA)
```

### Security Solutions by Zone
| Zone | Solutions |
|------|----------|
| Communication | Anti-jamming sensors, VPN (IPSec), encryption (asymmetric key exchange + symmetric data) |
| Antenna | Firewall, NAC, IDS/IPS, Anti-DDoS, DLP (media control), whitelist AV, CCTV, access control |
| Ground Station-Cloud | WAF, web shell detection, cloud DLP, DRM, PMS, vulnerability scanner |
| Operator | MFA, server access control, VPN (SSL), UPS/backup power |
