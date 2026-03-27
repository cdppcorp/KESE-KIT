---
name: fix
description: Auto-fix security vulnerabilities found in CII systems. Generates hardening scripts for Unix/Linux, Windows, web servers, and databases. Applies secure configurations based on KISA guidelines. Use when "fix vulnerabilities", "secure the system", "apply security fixes", "harden server", "KISA hardening".
---

# KESE Vulnerability Auto-Fix

You are a CII security hardening specialist. Based on vulnerability assessment results, generate and apply appropriate fixes. Create platform-specific hardening scripts following KISA guidelines.

## Execution Flow

1. Read previous assessment results (if available) from `reports/kese/`
2. If no previous assessment, ask user for target platform
3. Generate hardening scripts for the identified platform
4. Provide step-by-step remediation guidance
5. Save scripts to `scripts/kese-hardening/`

## Output Structure

```
scripts/kese-hardening/
├── unix/
│   ├── account-hardening.sh
│   ├── file-permissions.sh
│   ├── service-hardening.sh
│   └── full-hardening.sh
├── windows/
│   ├── account-hardening.ps1
│   ├── service-hardening.ps1
│   └── full-hardening.ps1
├── web/
│   ├── apache-hardening.conf
│   ├── nginx-hardening.conf
│   └── tomcat-hardening.xml
├── database/
│   ├── mysql-hardening.sql
│   ├── postgresql-hardening.sql
│   └── oracle-hardening.sql
└── README.md
```

---

## Unix/Linux Hardening Scripts

### Account Hardening (U-01 ~ U-09)

```bash
#!/bin/bash
# KESE Unix Account Hardening Script
# Based on KISA CII Vulnerability Assessment Guidelines

echo "=== KESE Account Hardening ==="

# U-01: Disable root remote login
echo "[U-01] Configuring SSH root login restriction..."
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config 2>/dev/null

# U-02: Password complexity
echo "[U-02] Configuring password complexity..."
cat > /etc/security/pwquality.conf << 'EOF'
minlen = 8
minclass = 3
maxrepeat = 3
lcredit = -1
ucredit = -1
dcredit = -1
ocredit = -1
EOF

# U-03: Account lockout policy
echo "[U-03] Configuring account lockout..."
cat >> /etc/pam.d/common-auth << 'EOF'
auth required pam_tally2.so deny=5 unlock_time=1800
EOF

# U-04: Password aging
echo "[U-04] Setting password aging policy..."
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   1/' /etc/login.defs
sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE   7/' /etc/login.defs

# U-05: Shadow file permissions
echo "[U-05] Setting shadow file permissions..."
chmod 400 /etc/shadow
chown root:root /etc/shadow

# U-06: Session timeout
echo "[U-06] Configuring session timeout..."
echo "TMOUT=300" >> /etc/profile
echo "readonly TMOUT" >> /etc/profile
echo "export TMOUT" >> /etc/profile

# U-07: Remove unnecessary accounts
echo "[U-07] Reviewing unnecessary accounts..."
# Locked but not deleted - review manually
for user in games gopher ftp; do
    if id "$user" &>/dev/null; then
        usermod -L $user 2>/dev/null
        echo "  Locked account: $user"
    fi
done

echo "=== Account Hardening Complete ==="
```

### File Permission Hardening (U-10 ~ U-24)

```bash
#!/bin/bash
# KESE Unix File Permission Hardening Script

echo "=== KESE File Permission Hardening ==="

# U-10: SUID/SGID file check
echo "[U-10] Reviewing SUID/SGID files..."
find / -perm -4000 -o -perm -2000 2>/dev/null > /tmp/suid_sgid_files.txt
echo "  Found $(wc -l < /tmp/suid_sgid_files.txt) SUID/SGID files"
echo "  Review /tmp/suid_sgid_files.txt for unnecessary permissions"

# U-11: World-writable files
echo "[U-11] Removing world-writable permissions..."
find / -type f -perm -002 -exec chmod o-w {} \; 2>/dev/null

# U-12: Umask setting
echo "[U-12] Configuring default umask..."
echo "umask 022" >> /etc/profile
echo "umask 022" >> /etc/bashrc

# U-13: Critical file permissions
echo "[U-13] Setting critical file permissions..."
chmod 644 /etc/passwd
chmod 400 /etc/shadow
chmod 644 /etc/group
chmod 600 /etc/hosts.allow
chmod 600 /etc/hosts.deny

# U-14: Home directory permissions
echo "[U-14] Securing home directories..."
for dir in /home/*; do
    if [ -d "$dir" ]; then
        chmod 700 "$dir"
    fi
done

# U-15: /tmp directory sticky bit
echo "[U-15] Setting sticky bit on /tmp..."
chmod 1777 /tmp
chmod 1777 /var/tmp

echo "=== File Permission Hardening Complete ==="
```

### Service Hardening (U-25 ~ U-43)

```bash
#!/bin/bash
# KESE Unix Service Hardening Script

echo "=== KESE Service Hardening ==="

# U-25~U-30: Disable unnecessary services
UNNECESSARY_SERVICES=(
    "telnet"
    "rsh"
    "rlogin"
    "rexec"
    "finger"
    "tftp"
    "talk"
    "ntalk"
    "chargen"
    "daytime"
    "echo"
    "discard"
    "nfs"
    "rpc.cmsd"
    "rpc.ttdbserverd"
)

echo "[U-25~U-30] Disabling unnecessary services..."
for service in "${UNNECESSARY_SERVICES[@]}"; do
    systemctl disable $service 2>/dev/null
    systemctl stop $service 2>/dev/null
    echo "  Disabled: $service"
done

# U-31: SSH configuration hardening
echo "[U-31] Hardening SSH configuration..."
cat >> /etc/ssh/sshd_config << 'EOF'
# KESE SSH Hardening
Protocol 2
PermitRootLogin no
PasswordAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 5
ClientAliveInterval 300
ClientAliveCountMax 0
X11Forwarding no
AllowTcpForwarding no
EOF

# U-32: FTP configuration (if needed)
echo "[U-32] Hardening FTP configuration..."
if [ -f /etc/vsftpd.conf ]; then
    sed -i 's/^anonymous_enable=.*/anonymous_enable=NO/' /etc/vsftpd.conf
    echo "ftpd_banner=Authorized access only" >> /etc/vsftpd.conf
fi

# U-33: Apache hardening (if present)
echo "[U-33] Hardening Apache configuration..."
if [ -d /etc/apache2 ] || [ -d /etc/httpd ]; then
    cat > /etc/apache2/conf-available/security-kese.conf << 'EOF'
ServerTokens Prod
ServerSignature Off
TraceEnable Off
Header always set X-Frame-Options SAMEORIGIN
Header always set X-Content-Type-Options nosniff
Header always set X-XSS-Protection "1; mode=block"
EOF
fi

# Restart services
echo "Restarting SSH service..."
systemctl restart sshd

echo "=== Service Hardening Complete ==="
```

---

## Windows Hardening Scripts

### Account Hardening (W-01 ~ W-15)

```powershell
# KESE Windows Account Hardening Script
# Based on KISA CII Vulnerability Assessment Guidelines

Write-Host "=== KESE Windows Account Hardening ===" -ForegroundColor Green

# W-01: Rename Administrator account
Write-Host "[W-01] Renaming Administrator account..."
$admin = Get-LocalUser | Where-Object {$_.SID -like "*-500"}
if ($admin.Name -eq "Administrator") {
    Rename-LocalUser -Name "Administrator" -NewName "LocalAdmin"
    Write-Host "  Administrator renamed to LocalAdmin"
}

# W-02: Disable Guest account
Write-Host "[W-02] Disabling Guest account..."
Disable-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
Write-Host "  Guest account disabled"

# W-03~W-04: Password policy
Write-Host "[W-03~W-04] Configuring password policy..."
net accounts /minpwlen:8 /maxpwage:90 /minpwage:1 /uniquepw:5

# W-05: Account lockout policy
Write-Host "[W-05] Configuring account lockout..."
net accounts /lockoutthreshold:5 /lockoutduration:30 /lockoutwindow:30

# W-06: Session timeout
Write-Host "[W-06] Configuring session timeout..."
# Set screen saver timeout to 10 minutes with password
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name ScreenSaveTimeOut -Value 600
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name ScreenSaverIsSecure -Value 1

# W-07: Remove unnecessary accounts
Write-Host "[W-07] Reviewing unnecessary accounts..."
$unusedAccounts = Get-LocalUser | Where-Object {$_.Enabled -eq $true -and $_.LastLogon -lt (Get-Date).AddDays(-90)}
foreach ($account in $unusedAccounts) {
    Write-Host "  Review account: $($account.Name) - Last logon: $($account.LastLogon)"
}

Write-Host "=== Account Hardening Complete ===" -ForegroundColor Green
```

### Service Hardening (W-16 ~ W-35)

```powershell
# KESE Windows Service Hardening Script

Write-Host "=== KESE Windows Service Hardening ===" -ForegroundColor Green

# W-16~W-20: Disable unnecessary services
$unnecessaryServices = @(
    "RemoteRegistry",
    "Telnet",
    "TFTP",
    "SNMPTRAP",
    "WinRM"
)

Write-Host "[W-16~W-20] Disabling unnecessary services..."
foreach ($service in $unnecessaryServices) {
    $svc = Get-Service -Name $service -ErrorAction SilentlyContinue
    if ($svc) {
        Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
        Set-Service -Name $service -StartupType Disabled
        Write-Host "  Disabled: $service"
    }
}

# W-21: Disable default shares
Write-Host "[W-21] Configuring default shares..."
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -Name "AutoShareServer" -Value 0
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -Name "AutoShareWks" -Value 0

# W-22~W-25: Firewall configuration
Write-Host "[W-22~W-25] Configuring Windows Firewall..."
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
Set-NetFirewallProfile -DefaultInboundAction Block -DefaultOutboundAction Allow

# W-26: Remote Desktop hardening
Write-Host "[W-26] Hardening Remote Desktop..."
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "UserAuthentication" -Value 1

# W-27~W-30: IIS hardening (if installed)
if (Get-Service -Name W3SVC -ErrorAction SilentlyContinue) {
    Write-Host "[W-27~W-30] Hardening IIS..."
    Import-Module WebAdministration -ErrorAction SilentlyContinue

    # Remove server header
    Set-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering" -Name "removeServerHeader" -Value "True"

    # Disable directory browsing
    Set-WebConfigurationProperty -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "False"
}

Write-Host "=== Service Hardening Complete ===" -ForegroundColor Green
```

---

## Web Server Hardening

### Apache Configuration

```apache
# KESE Apache Hardening Configuration
# Include this in httpd.conf or apache2.conf

# Hide server version
ServerTokens Prod
ServerSignature Off

# Disable TRACE method
TraceEnable Off

# Security headers
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set Content-Security-Policy "default-src 'self'"

# Disable directory listing
<Directory />
    Options -Indexes
    AllowOverride None
    Require all denied
</Directory>

# Limit HTTP methods
<Directory "/var/www/html">
    <LimitExcept GET POST HEAD>
        Require all denied
    </LimitExcept>
</Directory>

# SSL/TLS Configuration
SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder on
```

### Nginx Configuration

```nginx
# KESE Nginx Hardening Configuration

# Hide server version
server_tokens off;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Disable directory listing
autoindex off;

# Limit request methods
if ($request_method !~ ^(GET|HEAD|POST)$) {
    return 405;
}

# SSL/TLS Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers on;

# Limit request body size
client_max_body_size 10m;

# Rate limiting
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
```

---

## Database Hardening

### MySQL/MariaDB

```sql
-- KESE MySQL Hardening Script

-- D-01: Remove anonymous users
DELETE FROM mysql.user WHERE User='';

-- D-02: Remove remote root access
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');

-- D-03: Remove test database
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';

-- D-04: Set password for root
-- ALTER USER 'root'@'localhost' IDENTIFIED BY 'StrongPassword123!';

-- D-05: Require SSL for remote connections
-- REQUIRE SSL for sensitive users

-- Apply changes
FLUSH PRIVILEGES;
```

### PostgreSQL

```sql
-- KESE PostgreSQL Hardening Script

-- D-01: Revoke public permissions
REVOKE ALL ON DATABASE postgres FROM PUBLIC;

-- D-02: Remove default permissions on new databases
ALTER DEFAULT PRIVILEGES REVOKE ALL ON TABLES FROM PUBLIC;

-- D-03: Enable logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;

-- D-04: Set password encryption
ALTER SYSTEM SET password_encryption = 'scram-sha-256';

-- Apply changes
SELECT pg_reload_conf();
```

---

## Fix Application Notes

- Always backup configurations before applying fixes
- Test changes in non-production environment first
- Review each script and customize for your environment
- Some fixes require service restarts
- Document all changes for compliance audit trail
