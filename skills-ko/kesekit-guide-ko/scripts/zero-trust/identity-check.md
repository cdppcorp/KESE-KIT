# Zero Trust Identity & Access Check

> Source: 제로트러스트 가이드라인 2.0 (KISA), NIST SP 800-207
> Checklist refs: ZT-ID-01~ZT-ID-53, ZT-DV-01~ZT-DV-36

---

## 1. MFA Configuration Audit (ZT-ID-11~16)

```bash
# Check PAM MFA configuration (Linux)
grep -n "pam_google_authenticator\|pam_duo\|pam_u2f\|pam_oath" /etc/pam.d/* 2>/dev/null

# Check SSH MFA enforcement
grep -n "AuthenticationMethods\|ChallengeResponseAuthentication\|KbdInteractiveAuthentication" /etc/ssh/sshd_config

# Verify MFA is required (not optional)
# Expected: AuthenticationMethods publickey,keyboard-interactive
```

### Windows MFA Check
```powershell
# Check Azure AD MFA status (requires AzureAD module)
# Get-MsolUser -All | Where-Object {$_.StrongAuthenticationRequirements.Count -eq 0} |
#   Select-Object DisplayName, UserPrincipalName

# Check Windows Hello for Business status
dsregcmd /status | findstr /i "NgcSet\|DeviceAuthStatus"
```

---

## 2. Session Timeout & Continuous Authentication (ZT-ID-17~21)

```bash
# Check SSH session timeout
grep -n "ClientAliveInterval\|ClientAliveCountMax" /etc/ssh/sshd_config

# Check shell timeout
echo "TMOUT=$TMOUT"
grep "TMOUT" /etc/profile /etc/bashrc /etc/profile.d/*.sh 2>/dev/null

# Check web session timeout in application configs
grep -rn "session.*timeout\|session.*expire\|maxInactiveInterval" \
  --include="*.yaml" --include="*.yml" --include="*.xml" --include="*.conf" \
  /etc/ /opt/ 2>/dev/null | head -20
```

---

## 3. Least Privilege Access Audit (ZT-ID-46~53)

```bash
# List users with sudo/root access
grep -v "^#" /etc/sudoers 2>/dev/null | grep -v "^$"
cat /etc/sudoers.d/* 2>/dev/null

# Find accounts with UID 0 (root equivalent)
awk -F: '$3==0{print $1}' /etc/passwd

# List users with login shell
awk -F: '$7!="/sbin/nologin" && $7!="/usr/sbin/nologin" && $7!="/bin/false"{print $1, $7}' /etc/passwd

# Check for dormant accounts (no login >90 days)
lastlog | awk '$NF!="in" && NR>1{print $1}' | head -20
```

---

## 4. Device Compliance Check (ZT-DV-01~08)

```bash
# Check OS patch level
uname -r
cat /etc/os-release

# Check pending security updates
# Debian/Ubuntu
apt list --upgradable 2>/dev/null | grep -i security

# RHEL/CentOS
yum check-update --security 2>/dev/null

# Check firewall status
systemctl status firewalld 2>/dev/null || ufw status 2>/dev/null || iptables -L -n 2>/dev/null | head -20

# Check antivirus/EDR status
systemctl status clamav-daemon 2>/dev/null
systemctl status falcon-sensor 2>/dev/null
```

---

## 5. User Inventory & Identity Federation (ZT-ID-01~10)

```bash
# Count total system accounts
echo "Total accounts: $(wc -l < /etc/passwd)"
echo "Login-capable accounts: $(awk -F: '$7!="/sbin/nologin" && $7!="/usr/sbin/nologin" && $7!="/bin/false"' /etc/passwd | wc -l)"

# Check LDAP/SSO integration
grep -rn "ldap\|sssd\|krb5\|oauth\|saml\|oidc" /etc/nsswitch.conf /etc/sssd/ /etc/pam.d/ 2>/dev/null | head -10

# Check for local-only accounts (not federated)
grep -v "^#" /etc/passwd | awk -F: '$3>=1000 && $3<65534{print $1, $3}'
```

---

## 6. Endpoint Management Check (ZT-DV-20~25)

```bash
# Check if endpoint management agent is running
systemctl status intune 2>/dev/null
systemctl status jamf 2>/dev/null
systemctl status qualys-cloud-agent 2>/dev/null

# Check disk encryption
lsblk -o NAME,FSTYPE,MOUNTPOINT,SIZE | grep -i crypt
# macOS: fdesetup status

# Check screen lock policy
gsettings get org.gnome.desktop.session idle-delay 2>/dev/null
gsettings get org.gnome.desktop.screensaver lock-enabled 2>/dev/null
```

---

## Verification Checklist

| Item | Check | Expected |
|------|-------|----------|
| MFA enabled | PAM/SSH config | MFA required for all users |
| Session timeout | `TMOUT` / SSH config | ≤ 600 seconds |
| No extra root users | `awk UID==0` | Only `root` |
| Dormant accounts | `lastlog` | None > 90 days |
| OS patched | Security updates | No critical pending |
| Firewall active | `systemctl status` | Running and configured |
| Identity federation | SSO/LDAP check | Centralized auth |
| Disk encryption | `lsblk` / fdesetup | Encrypted |
