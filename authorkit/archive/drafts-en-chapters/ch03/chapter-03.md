# Chapter 3. Unix/Linux Server Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Unix/Linux servers are core infrastructure for Critical Information Infrastructure. This chapter covers 68 assessment items (U-01 ~ U-68) divided into 5 domains.

```
┌─────────────────────────────────────────────────────────────────┐
│           Unix/Linux Server Vulnerability Assessment Domains     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │   Account   │   │  File/Dir   │   │   Service   │          │
│   │ Management  │   │ Management  │   │ Management  │          │
│   │  U-01~U-13  │   │  U-14~U-33  │   │  U-34~U-63  │          │
│   │   (13)      │   │   (20)      │   │   (30)      │          │
│   │             │   │             │   │             │          │
│   │ • root      │   │ • Permissions│  │ • Unnecessary│         │
│   │   access    │   │ • SUID/SGID │   │   services  │          │
│   │ • Password  │   │ • Ownership │   │ • SNMP      │          │
│   │ • Lockout   │   │             │   │   security  │          │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘          │
│          │                 │                 │                  │
│          └────────────────┬┴─────────────────┘                  │
│                           │                                      │
│          ┌────────────────┴────────────────┐                    │
│          ▼                                 ▼                    │
│   ┌─────────────┐                   ┌─────────────┐            │
│   │   Patch     │                   │    Log      │            │
│   │ Management  │                   │ Management  │            │
│   │    U-64     │                   │  U-65~U-68  │            │
│   │    (1)      │                   │    (4)      │            │
│   │             │                   │             │            │
│   │ • Security  │                   │ • Log config│            │
│   │   patches   │                   │ • Retention │            │
│   └─────────────┘                   └─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | U-01 ~ U-13 | 13 |
| File and Directory Management | U-14 ~ U-33 | 20 |
| Service Management | U-34 ~ U-63 | 30 |
| Patch Management | U-64 | 1 |
| Log Management | U-65 ~ U-68 | 4 |

---

## 3-1. Account Management (U-01 ~ U-13)

Account management is the first line of defense for server security. Improper account management is a major cause of unauthorized access.

### U-01. Restrict Remote Access to root Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access by restricting direct remote access to root account |
| **Criteria** | Good: Direct root access blocked / Vulnerable: Direct root access allowed |

#### Assessment Method

```bash
# Check SSH configuration
cat /etc/ssh/sshd_config | grep -i "PermitRootLogin"

# Check Telnet usage (not recommended)
cat /etc/securetty
```

#### Remediation

```bash
# Edit /etc/ssh/sshd_config
PermitRootLogin no

# Restart SSH service
systemctl restart sshd
```

> **TIP**
> When root access is needed, connect with a regular account first and use `su -` or `sudo`.

---

### U-02. Configure Password Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Enforce password complexity and periodic changes |
| **Criteria** | Good: Policy configured / Vulnerable: Policy not configured |

#### Assessment Method

```bash
# Check password policy
cat /etc/login.defs | grep -E "PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_MIN_LEN|PASS_WARN_AGE"

# Check PAM configuration (RHEL/CentOS)
cat /etc/pam.d/system-auth | grep pam_pwquality
```

#### Recommended Settings

| Item | Recommended | Description |
|------|:-----------:|-------------|
| PASS_MAX_DAYS | 90 | Maximum password age |
| PASS_MIN_DAYS | 1 | Minimum password age |
| PASS_MIN_LEN | 8 | Minimum length |
| PASS_WARN_AGE | 7 | Warning days before expiry |

#### Remediation

```bash
# Edit /etc/login.defs
PASS_MAX_DAYS   90
PASS_MIN_DAYS   1
PASS_MIN_LEN    8
PASS_WARN_AGE   7
```

---

### U-03. Configure Account Lockout Threshold

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent brute force attacks |
| **Criteria** | Good: Set to 5 or less / Vulnerable: Not configured or exceeded |

#### Assessment Method

```bash
# Check PAM configuration
cat /etc/pam.d/system-auth | grep pam_tally2
# or
cat /etc/pam.d/system-auth | grep pam_faillock
```

#### Remediation

```bash
# /etc/pam.d/system-auth (RHEL 7 and later)
auth required pam_faillock.so preauth silent deny=5 unlock_time=600
auth required pam_faillock.so authfail deny=5 unlock_time=600
```

> **WARNING**
> Be careful with `even_deny_root` option to prevent locking out the root account.

---

### U-04. Password File Protection

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Protect password hashes using Shadow passwords |
| **Criteria** | Good: Shadow used / Vulnerable: Passwords stored in passwd |

#### Assessment Method

```bash
# Check second field in /etc/passwd
cat /etc/passwd | awk -F: '{print $1":"$2}'
# 'x' indicates shadow is in use
```

---

### U-05. Prohibit UID '0' for Non-root Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Detect unauthorized accounts with root privileges |
| **Criteria** | Good: Only root has UID 0 / Vulnerable: Other accounts have UID 0 |

#### Assessment Method

```bash
# Check accounts with UID 0
awk -F: '$3==0 {print $1}' /etc/passwd
```

#### Remediation

Delete or change UID for any non-root accounts with UID 0.

---

### U-06. Restrict su Command Access

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Restrict su command usage to specific groups |
| **Criteria** | Good: Only wheel group can use su / Vulnerable: No restrictions |

#### Assessment Method

```bash
# Check PAM configuration
cat /etc/pam.d/su | grep pam_wheel
```

#### Remediation

```bash
# Edit /etc/pam.d/su (uncomment)
auth required pam_wheel.so use_uid

# Add user to wheel group
usermod -aG wheel [username]
```

---

### U-07 ~ U-13. Other Account Management Items

| Code | Item | Severity | Key Check |
|------|------|:--------:|-----------|
| U-07 | Remove unnecessary accounts | Low | Unused accounts in `/etc/passwd` |
| U-08 | Minimize admin group members | Medium | wheel/root group members |
| U-09 | Prohibit GID without accounts | Low | `/etc/group` integrity |
| U-10 | Prohibit duplicate UIDs | Medium | Check for duplicate UIDs |
| U-11 | User shell verification | Low | Unnecessary accounts `/sbin/nologin` |
| U-12 | Session timeout configuration | Low | TMOUT environment variable |
| U-13 | Secure password encryption algorithm | Medium | SHA-512 recommended |

---

## 3-2. File and Directory Management (U-14 ~ U-33)

File permission management is key to protecting system integrity.

### U-14. root Home and PATH Directory Permissions

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent '.' in PATH environment variable |
| **Criteria** | Good: PATH without '.' / Vulnerable: '.' included |

#### Assessment Method

```bash
# Check PATH environment variable
echo $PATH | grep -E "^\.|:\.|:$"

# Check root profile
cat /root/.bash_profile | grep PATH
```

> **WARNING**
> Including current directory (`.`) in PATH risks executing malicious programs.

---

### U-16 ~ U-22. Key System File Permissions

| Code | Target File | Recommended | Owner |
|------|------------|:-----------:|:-----:|
| U-16 | /etc/passwd | 644 | root |
| U-18 | /etc/shadow | 400 | root |
| U-19 | /etc/hosts | 600 | root |
| U-20 | /etc/(x)inetd.conf | 600 | root |
| U-21 | /etc/(r)syslog.conf | 640 | root |
| U-22 | /etc/services | 644 | root |

#### Batch Assessment Script

```bash
#!/bin/bash
# Key file permission check

FILES=(
    "/etc/passwd:644:root"
    "/etc/shadow:400:root"
    "/etc/hosts:600:root"
    "/etc/services:644:root"
)

for item in "${FILES[@]}"; do
    IFS=':' read -r file perm owner <<< "$item"
    if [ -f "$file" ]; then
        actual_perm=$(stat -c "%a" "$file")
        actual_owner=$(stat -c "%U" "$file")
        if [ "$actual_perm" -le "$perm" ] && [ "$actual_owner" == "$owner" ]; then
            echo "[Good] $file (Permission: $actual_perm, Owner: $actual_owner)"
        else
            echo "[Vulnerable] $file (Permission: $actual_perm, Owner: $actual_owner)"
        fi
    fi
done
```

---

### U-23. SUID, SGID, Sticky Bit File Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent privilege escalation through unnecessary SUID/SGID files |

#### Assessment Method

```bash
# Find SUID files
find / -perm -4000 -type f 2>/dev/null

# Find SGID files
find / -perm -2000 -type f 2>/dev/null

# Find SUID + SGID files
find / -perm -6000 -type f 2>/dev/null
```

#### Key SUID Files to Check

| File | Required | Action |
|------|:--------:|--------|
| /usr/bin/passwd | Yes | Maintain |
| /usr/bin/su | Yes | Maintain |
| /usr/bin/chsh | Review | Remove if unnecessary |
| /usr/bin/newgrp | Review | Remove if unnecessary |

---

### U-25. World Writable File Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Detect files writable by all users |

#### Assessment Method

```bash
# Find world writable files
find / -perm -2 -type f 2>/dev/null

# Find world writable directories (without sticky bit)
find / -perm -2 -type d ! -perm -1000 2>/dev/null
```

---

## 3-3. Service Management (U-34 ~ U-63)

Unnecessary services increase the attack surface. Run only essential services.

### U-34. Disable Finger Service

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent user information disclosure |
| **Criteria** | Good: Disabled / Vulnerable: Enabled |

#### Assessment Method

```bash
# Check Finger service
systemctl status finger 2>/dev/null
# or
chkconfig --list finger 2>/dev/null
```

---

### U-36. Disable r-series Services

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block remote access without authentication |
| **Target Services** | rsh, rlogin, rexec |

#### Assessment Method

```bash
# Check r-series services
systemctl status rsh.socket rlogin.socket rexec.socket 2>/dev/null

# Check inetd/xinetd configuration
cat /etc/xinetd.d/rsh 2>/dev/null | grep disable
```

> **WARNING**
> r-series services use unencrypted communication. Replace with SSH.

---

### U-52. Disable Telnet Service

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Block plaintext communication services |
| **Criteria** | Good: Disabled or SSH used / Vulnerable: Telnet enabled |

#### Assessment Method

```bash
# Check Telnet service
systemctl status telnet.socket 2>/dev/null

# Check port
netstat -tlnp | grep :23
```

---

### U-58 ~ U-61. SNMP Security

| Code | Item | Severity |
|------|------|:--------:|
| U-58 | Check unnecessary SNMP service | Medium |
| U-59 | Use secure SNMP version | High |
| U-60 | SNMP Community String complexity | Medium |
| U-61 | SNMP Access Control configuration | High |

#### Assessment Method

```bash
# Check SNMP service
systemctl status snmpd

# Check Community String
cat /etc/snmp/snmpd.conf | grep -i community
```

> **TIP**
> Use SNMP v3 and always change default Community Strings (public, private).

---

## 3-4. Patch Management (U-64)

### U-64. Apply Regular Security Patches and Vendor Recommendations

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Apply patches for known vulnerabilities |
| **Criteria** | Good: Latest patches applied / Vulnerable: Not applied |

#### Assessment Method

```bash
# RHEL/CentOS
yum check-update

# Ubuntu/Debian
apt list --upgradable

# Check kernel version
uname -r
```

#### Remediation

```bash
# RHEL/CentOS
yum update -y

# Ubuntu/Debian
apt update && apt upgrade -y
```

> **WARNING**
> In production environments, verify patches in test environments before applying.

---

## 3-5. Log Management (U-65 ~ U-68)

### U-65. Log Policy Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Appropriate log recording and retention |

#### Assessment Method

```bash
# Check syslog configuration
cat /etc/rsyslog.conf

# Check key log file existence
ls -la /var/log/messages /var/log/secure /var/log/wtmp
```

### U-66. Log Management per Policy

| Log File | Content | Recommended Retention |
|----------|---------|:--------------------:|
| /var/log/messages | System messages | 6 months |
| /var/log/secure | Authentication logs | 6 months |
| /var/log/wtmp | Login records | 6 months |
| /var/log/btmp | Failed logins | 6 months |

---

## 3-6. Automation Scripts

### Integrated Assessment Script

Below is a Bash script that automatically checks key items.

```bash
#!/bin/bash
#===============================================
# KESE KIT - Unix/Linux Server Vulnerability Auto-Check
# Version: 1.0
#===============================================

REPORT_FILE="unix_check_$(date +%Y%m%d_%H%M%S).txt"

echo "=============================================" | tee $REPORT_FILE
echo "KESE KIT Unix/Linux Vulnerability Check Results" | tee -a $REPORT_FILE
echo "Check Date: $(date)" | tee -a $REPORT_FILE
echo "Hostname: $(hostname)" | tee -a $REPORT_FILE
echo "=============================================" | tee -a $REPORT_FILE

# U-01: root remote access restriction
echo -e "\n[U-01] root Remote Access Restriction" | tee -a $REPORT_FILE
SSH_ROOT=$(grep -i "^PermitRootLogin" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
if [ "$SSH_ROOT" == "no" ]; then
    echo "  [Good] PermitRootLogin = no" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] PermitRootLogin = $SSH_ROOT" | tee -a $REPORT_FILE
fi

# U-04: Password file protection
echo -e "\n[U-04] Password File Protection (Shadow Usage)" | tee -a $REPORT_FILE
SHADOW_CHECK=$(awk -F: '$2!="x" && $2!="*" && $2!="!!" {print $1}' /etc/passwd)
if [ -z "$SHADOW_CHECK" ]; then
    echo "  [Good] Shadow password in use" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Accounts not using Shadow: $SHADOW_CHECK" | tee -a $REPORT_FILE
fi

# U-05: Non-root UID 0 accounts
echo -e "\n[U-05] Non-root UID 0 Accounts" | tee -a $REPORT_FILE
UID_ZERO=$(awk -F: '$3==0 && $1!="root" {print $1}' /etc/passwd)
if [ -z "$UID_ZERO" ]; then
    echo "  [Good] Only root has UID 0" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] UID 0 accounts: $UID_ZERO" | tee -a $REPORT_FILE
fi

# U-16: /etc/passwd permission
echo -e "\n[U-16] /etc/passwd Permission" | tee -a $REPORT_FILE
PASSWD_PERM=$(stat -c "%a" /etc/passwd)
if [ "$PASSWD_PERM" -le "644" ]; then
    echo "  [Good] Permission: $PASSWD_PERM" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Permission: $PASSWD_PERM (644 or less recommended)" | tee -a $REPORT_FILE
fi

# U-18: /etc/shadow permission
echo -e "\n[U-18] /etc/shadow Permission" | tee -a $REPORT_FILE
SHADOW_PERM=$(stat -c "%a" /etc/shadow)
if [ "$SHADOW_PERM" -le "400" ]; then
    echo "  [Good] Permission: $SHADOW_PERM" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Permission: $SHADOW_PERM (400 or less recommended)" | tee -a $REPORT_FILE
fi

# U-52: Telnet service
echo -e "\n[U-52] Telnet Service" | tee -a $REPORT_FILE
TELNET_CHECK=$(systemctl is-active telnet.socket 2>/dev/null)
if [ "$TELNET_CHECK" != "active" ]; then
    echo "  [Good] Telnet disabled" | tee -a $REPORT_FILE
else
    echo "  [Vulnerable] Telnet enabled" | tee -a $REPORT_FILE
fi

echo -e "\n=============================================" | tee -a $REPORT_FILE
echo "Check complete. Results file: $REPORT_FILE" | tee -a $REPORT_FILE
```

### Script Usage

```bash
# Grant execution permission
chmod +x unix_check.sh

# Execute (root privileges required)
sudo ./unix_check.sh

# View results
cat unix_check_*.txt
```

> **TIP**
> Register this script in cron for periodic checks.
> ```
> # Run every Monday at 2 AM
> 0 2 * * 1 /path/to/unix_check.sh
> ```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | root remote access, password policy, account lockout | Highest |
| File Permissions | Key config file permissions, SUID/SGID | High |
| Service Management | Disable unnecessary services, SNMP security | High |
| Patch Management | Apply latest security patches | Highest |
| Log Management | Log configuration and retention | Medium |

---

*Next Chapter: Chapter 4. Windows Server Assessment*
