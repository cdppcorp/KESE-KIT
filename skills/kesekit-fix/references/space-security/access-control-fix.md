# Access Control & Authentication — Fix Scripts

> Hardening scripts and configurations for AC-01~AC-12, IA-01~IA-02

## AC-01: Access Control Policy

### Network ACL
```bash
# Allow only Jump Server IP for SSH access
iptables -A INPUT -s <JUMP_SERVER_IP> -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP

# Block plaintext protocols (Telnet, FTP)
iptables -A INPUT -p tcp --dport 23 -j DROP   # Telnet
iptables -A INPUT -p tcp --dport 21 -j DROP   # FTP
iptables -A OUTPUT -p tcp --dport 23 -j DROP
iptables -A OUTPUT -p tcp --dport 21 -j DROP
```

### Account Cleanup
```bash
# Find and disable default accounts
for user in admin guest test demo; do
  id "$user" 2>/dev/null && usermod -L "$user" && echo "Locked: $user"
done

# List accounts with no password expiry
chage -l <username> | grep "Password expires"

# Force password change for all users
for user in $(awk -F: '$3>=1000{print $1}' /etc/passwd); do
  chage -M 90 "$user"  # Max 90 days
done
```

### Thresholds
| Item | Value | Standard |
|------|-------|----------|
| Account deletion on termination | Same day | KISA |
| Full access review cycle | Annual (minimum) | CMMC |
| Allowed protocols | SSH, SFTP, VPN only | K-RMF |

---

## AC-03: Privileged Access

### Linux — SELinux/AppArmor
```bash
# Check SELinux status
getenforce

# Enable SELinux enforcing mode
setenforce 1
sed -i 's/SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config

# Restrict admin to system management paths only (AppArmor)
# /etc/apparmor.d/usr.sbin.admin-profile
# deny /usr/bin/firefox rx,
# deny /usr/bin/chrome rx,
```

### Windows — AppLocker
```powershell
# Enable AppLocker via GPO
# Computer Configuration > Windows Settings > Security Settings > Application Control Policies > AppLocker
# Create rule: Allow only management tools (MMC, PowerShell) for admin profiles
# Block all other EXE, DLL for privileged accounts
```

### PAM (Privileged Access Management)
```bash
# Restrict admin IP + MAC address access
# /etc/hosts.allow
sshd: 10.0.1.0/24
# /etc/hosts.deny
sshd: ALL
```

---

## AC-06: Failed Login Attempts

### Linux — PAM
```bash
# /etc/pam.d/system-auth (or common-auth)
auth required pam_tally2.so deny=5 unlock_time=1800 onerr=fail

# Check locked accounts
pam_tally2 --user=<username>

# Reset failed count
pam_tally2 --user=<username> --reset
```

### Windows
```
secpol.msc → Account Policies → Account Lockout Policy
→ Account lockout threshold: 5
→ Account lockout duration: 30 minutes
→ Reset account lockout counter after: 30 minutes
```

### Thresholds
| Target | Max Attempts | Lockout Duration | Standard |
|--------|:-----------:|:----------------:|----------|
| Server | 3 | 30 min | K-RMF |
| User account | 5 | 15-60 min | CMMC |
| Mobile device | 5-10 (then wipe) | - | KISA |
| Login delay | 5-10 sec after failure | - | Best practice |

---

## AC-07: Session Lock & Termination

### Linux
```bash
# Auto-logout after 10 min inactivity
echo "TMOUT=600" >> /etc/profile
echo "readonly TMOUT" >> /etc/profile
echo "export TMOUT" >> /etc/profile
```

### Windows
```
# Screen saver with password after 10 min
GPO: User Configuration > Administrative Templates > Control Panel > Personalization
→ Enable screen saver: Enabled
→ Screen saver timeout: 600 seconds
→ Password protect the screen saver: Enabled
```

### Web Application (JSP)
```xml
<!-- web.xml -->
<session-config>
  <session-timeout>10</session-timeout> <!-- minutes -->
</session-config>

<!-- weblogic.xml -->
<session-descriptor>
  <timeout-secs>600</timeout-secs>
</session-descriptor>
```

### Session Timeout by Risk
| Risk Level | Timeout | Example |
|-----------|:-------:|---------|
| Critical functions | 2-5 min | Satellite command, orbit control |
| Standard operations | 10-15 min | Ground station monitoring |
| Low-risk | 15-30 min | Reporting, documentation |
| Exception | No timeout (approved) | 24/7 NOC/SOC dashboards |

---

## AC-08: Remote Access Control

### VPN + MFA
```bash
# OpenVPN with MFA (TOTP)
# /etc/openvpn/server.conf
plugin /usr/lib/openvpn/plugins/openvpn-plugin-auth-pam.so openvpn
verify-client-cert require

# Require all traffic through VPN (no split tunneling)
push "redirect-gateway def1"
```

---

## AC-09: Wireless Access

### Wi-Fi Hardening
```bash
# hostapd.conf — WPA2-Enterprise
wpa=2
wpa_key_mgmt=WPA-EAP
rsn_pairwise=CCMP
ieee8021x=1

# Hide SSID
ignore_broadcast_ssid=1

# MAC filtering
macaddr_acl=1
accept_mac_file=/etc/hostapd/accept
```

### WIPS Deployment
- Deploy Wireless IPS sensors in antenna zones and ground station facilities
- Monitor for rogue APs and unauthorized wireless connections
- Disable unused Bluetooth/Wi-Fi on all operational devices

---

## IA-01: Identification & Authentication

### Password Policy
```bash
# /etc/security/pwquality.conf
minlen = 8
minclass = 2          # At least 2 character types
maxrepeat = 3
dcredit = -1          # Require digit
ucredit = -1          # Require uppercase
lcredit = -1          # Require lowercase
ocredit = -1          # Require special char

# /etc/login.defs
PASS_MAX_DAYS 90
PASS_MIN_DAYS 1
PASS_WARN_AGE 14
```

### Windows
```
secpol.msc → Account Policies → Password Policy
→ Minimum password length: 8
→ Password must meet complexity requirements: Enabled
→ Maximum password age: 90 days
→ Enforce password history: 5 passwords remembered
```

### Password Storage
- **NEVER** store plaintext or reversibly encrypted passwords
- Use one-way hash: **SHA-256+** with salt
- Transmit via **TLS encrypted channel** only

---

## IA-02: Multi-Factor Authentication

### MFA Methods (combine 2+)
| Factor | Methods |
|--------|---------|
| Knowledge | Password |
| Possession | PKI certificate, OTP (TOTP 30s/60s), smart card, hardware token |
| Biometric | Fingerprint, iris, face |
| Supplemental | IP address, MAC address, device serial, geolocation |

### Anti-Replay
```
# TOTP configuration
- Token validity: 30 or 60 seconds
- Use Kerberos ticket-based authentication
- Include Nonce (random number) per request
- One-time-use tokens (discard after use)
- High-risk accounts: U2F/FIDO2, smart card, OTP hardware token
```
