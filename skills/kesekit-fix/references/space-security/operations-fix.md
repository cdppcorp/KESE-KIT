# Operations & Incident Response — Fix Scripts

> Hardening for SO-01~SO-09, IR-01~IR-02

## SO-02: Audit Logging

### Log Types (all required)
| Type | Content |
|------|---------|
| System event | Start/stop, status, error codes |
| Network event | IP assignment, traffic on key segments |
| Security system | Admin access, policy create/change/delete |
| Audit | Login/logout, auth success/failure, file access |

### Log Protection
```bash
# rsyslog — forward to central SIEM
*.* @@siem-server:514

# Append-only log files
chattr +a /var/log/secure
chattr +a /var/log/audit/audit.log

# Minimum retention: 1 year
```

### Tamper-Proof Storage
- CD-ROM, DVD-R, WORM media for critical audit logs
- If writable media: store MAC value / digital signature separately
- Real-time collection to SIEM / central log server

---

## SO-03: Time Synchronization

### Linux NTP
```bash
# /etc/ntp.conf or /etc/chrony.conf
server <INTERNAL_NTP_SERVER> iburst
driftfile /var/lib/chrony/drift

# Verify sync
chronyc tracking
chronyc sources -v
```

### Windows NTP
```cmd
REM Check current sync
w32tm /dumpreg /subkey:parameters

REM Set internal NTP server
w32tm /config /syncfromflags:manual /manualpeerlist:<NTP_SERVER_IP> /update

REM Force resync
w32tm /resync

REM Check time difference
w32tm /stripchart /dataonly /computer:<NTP_SERVER_IP>
```

---

## SO-04: Portable Storage Security

### USB Control
```bash
# Disable USB storage (Linux)
echo "install usb-storage /bin/true" >> /etc/modprobe.d/disable-usb.conf
echo "blacklist usb-storage" >> /etc/modprobe.d/disable-usb.conf
```

### Secure Disposal Methods
| Method | Description | Recommended |
|--------|-------------|:-----------:|
| Physical destruction | Shredder, melting, incineration | For classified |
| Degausser | Magnetic field erasure | For HDD |
| Overwrite | Random/0/1 values, **3+ passes** | For reusable media |
| Crypto-erase | Encrypt → delete key → overwrite | For SSD |

### Backup Encryption
| Type | Algorithms |
|------|-----------|
| Symmetric | SEED, ARIA-128/192/256, AES-128/192/256, HIGHT, LEA |
| Asymmetric | RSAES-OAEP |
| Hash | SHA-256/384/512 |

---

## SO-05: Configuration Management

### Baseline Items
```
Hardware: Model, serial, firmware version, physical location
Software: OS version, installed packages, patch level
Firmware: Version, checksum, update history
Settings: Registry values, account permissions, file/directory permissions, network config
```

### Drift Detection
```bash
# AIDE (Advanced Intrusion Detection Environment)
aide --init
aide --check

# Monthly baseline comparison
```

---

## IR-02: Incident Reporting

### Korea (ICT Infrastructure Protection Act Art.48-3)
```
Deadline: Within 24 hours of discovery
Contact:
  Phone: 118 (24/7)
  Online: KrCERT → "침해사고 신고"
  Email: certgen@krcert.or.kr
```

### EU NIS2 Reporting Timeline
| Stage | Deadline | Content |
|-------|----------|---------|
| Early warning | **24 hours** | Indicate if unlawful/malicious |
| Incident notification | **72 hours** | Initial assessment, IoC |
| Interim report | On CSIRT request | Status update |
| Final report | **1 month** after 72h notification | Root cause, mitigation |

### NIS2 Significant Incident Criteria
- Direct damage > **EUR 500,000** or **5%** of prior year revenue
- Cloud: service unavailable > **30 minutes**
- Data center: availability limited > **1 hour**

### NIS2 Penalties
| Entity Type | Maximum Fine |
|-------------|-------------|
| Essential | **2%** annual revenue or **EUR 10,000,000** (whichever higher) |
| Important | **1.4%** annual revenue or **EUR 7,000,000** (whichever higher) |

### US DFARS 252.204-7012
- Report within **72 hours** to DC3 DCISE
- Preserve system images and network data for **90 days**
- Require DoD **Medium Assurance Certificate**

---

## Supply Chain Fix — SBOM & Integrity

### SBOM Standards
```
Formats: SPDX, CycloneDX
Content: All open-source/commercial SW components, versions, licenses
CVE Scanning: Periodic (at least quarterly)
On new vulnerability: SBOM-based impact identification
```

### Integrity Verification
```bash
# Hash verification for SW updates
sha256sum firmware-update.bin > firmware-update.sha256
sha256sum -c firmware-update.sha256

# Digital signature verification
gpg --verify firmware-update.bin.sig firmware-update.bin
```

### CI/CD Pipeline Security
- Verify all IDE plugins and CI/CD tools before use
- Scan build artifacts for malware before deployment
- Maintain internal library repository behind firewall
- Block unverified Docker Hub images
- Remove test/debug accounts before production deployment
- Check for hardcoded credentials (MASTER_KEY, API keys, passwords)
