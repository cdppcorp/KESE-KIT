# Chapter 4. Windows Server Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Windows servers are used in enterprise environments for various roles including Active Directory, file servers, and web servers. This chapter covers 73 assessment items (W-01 ~ W-73) divided into 5 domains.

```
┌─────────────────────────────────────────────────────────────────┐
│           Windows Server Vulnerability Assessment Domains (73)   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                Security Management (W-48~W-73, 26)          │ │
│  │   Firewall | Antivirus | Screen Saver | Registry | Perms   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▲                                   │
│        ┌─────────────────────┼─────────────────────┐            │
│        │                     │                     │            │
│  ┌─────┴─────┐        ┌─────┴─────┐        ┌─────┴─────┐       │
│  │  Account  │        │  Service  │        │    Log    │       │
│  │ Management│        │ Management│        │ Management│       │
│  │ W-01~W-14 │        │ W-15~W-39 │        │ W-42~W-47 │       │
│  │   (14)    │        │   (25)    │        │    (6)    │       │
│  │           │        │           │        │           │       │
│  │• Admin   │        │• Unnecessary│       │• Audit    │       │
│  │  rename  │        │  services │        │  policy   │       │
│  │• Guest   │        │• IIS check│        │• Log size │       │
│  │  disable │        │• Shared   │        │• Event    │       │
│  │• Lockout │        │  folders  │        │  logs     │       │
│  └───────────┘        └───────────┘        └───────────┘       │
│                              │                                   │
│                       ┌─────┴─────┐                             │
│                       │   Patch   │                             │
│                       │ Management│                             │
│                       │ W-40~W-41 │                             │
│                       │    (2)    │                             │
│                       │           │                             │
│                       │• Service  │                             │
│                       │  Pack     │                             │
│                       │• Security │                             │
│                       │  patches  │                             │
│                       └───────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | W-01 ~ W-14 | 14 |
| Service Management | W-15 ~ W-39 | 25 |
| Patch Management | W-40 ~ W-41 | 2 |
| Log Management | W-42 ~ W-47 | 6 |
| Security Management | W-48 ~ W-73 | 26 |

---

## 4-1. Account Management (W-01 ~ W-14)

### W-01. Rename Administrator Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent attacks targeting default admin account name |
| **Criteria** | Good: Name changed / Vulnerable: Default name used |

#### Assessment Method (PowerShell)

```powershell
# Check Administrator account
Get-LocalUser | Where-Object {$_.SID -like "*-500"}

# Or Command Prompt
net user administrator
```

#### Remediation

```powershell
# Rename account with PowerShell
Rename-LocalUser -Name "Administrator" -NewName "NewAdminName"

# Or via Local Security Policy
# secpol.msc > Local Policies > Security Options > Accounts: Rename administrator account
```

> **TIP**
> Choose an unpredictable name, but document it for management convenience.

---

### W-02. Disable Guest Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block anonymous access |
| **Criteria** | Good: Disabled / Vulnerable: Enabled |

#### Assessment Method

```powershell
# Check Guest account status
Get-LocalUser -Name "Guest" | Select-Object Name, Enabled
```

#### Remediation

```powershell
# Disable Guest account
Disable-LocalUser -Name "Guest"
```

---

### W-03. Remove Unnecessary Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access through unused accounts |

#### Assessment Method

```powershell
# List all local accounts
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Find accounts not logged in for 90+ days
$threshold = (Get-Date).AddDays(-90)
Get-LocalUser | Where-Object {$_.LastLogon -lt $threshold}
```

---

### W-04. Configure Password Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Enforce strong password usage |

#### Assessment Method

```powershell
# Check password policy
net accounts

# Or PowerShell
Get-ADDefaultDomainPasswordPolicy  # Domain environment
```

#### Recommended Settings

| Policy | Recommended |
|--------|:-----------:|
| Minimum password length | 8+ characters |
| Password complexity | Enabled |
| Maximum password age | 90 days |
| Minimum password age | 1 day |
| Password history | 12 |

#### Remediation

```powershell
# Configure via Local Security Policy (secpol.msc) or Group Policy (gpedit.msc)
# Computer Configuration > Windows Settings > Security Settings > Account Policies > Password Policy
```

---

### W-05. Configure Account Lockout Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent brute force attacks |

#### Assessment Method

```powershell
# Check account lockout policy
net accounts
```

#### Recommended Settings

| Policy | Recommended |
|--------|:-----------:|
| Account lockout threshold | 5 attempts |
| Account lockout duration | 30 minutes |
| Reset account lockout counter after | 30 minutes |

---

### W-06 ~ W-14. Other Account Management Items

| Code | Item | Severity | Key Check |
|------|------|:--------:|-----------|
| W-06 | Minimize admin group members | High | Administrators group members |
| W-07 | Local account management | Medium | Unnecessary local accounts |
| W-08 | Disable reversible encryption for passwords | Medium | Policy setting |
| W-09 | Restrict remote access for local accounts | Medium | UAC remote restriction |
| W-10 | Session timeout configuration | Low | Screen lock |
| W-11 | Don't display last logged on user | Low | Logon screen |
| W-12 | Display legal notice at logon | Low | Legal warning |
| W-13 | Don't allow anonymous enumeration of SAM accounts | High | Block anonymous enumeration |
| W-14 | Disable Remote Registry service | High | Remote Registry |

---

## 4-2. Service Management (W-15 ~ W-39)

### W-15. Disable Unnecessary Services

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Minimize attack surface |

#### Services Recommended for Disabling

| Service | Description | Disable |
|---------|-------------|:-------:|
| Telnet | Remote access (plaintext) | Yes |
| TFTP | File transfer (no auth) | Yes |
| FTP Publishing | FTP server | Review |
| Remote Registry | Remote registry access | Yes |
| Simple TCP/IP Services | Echo, Daytime, etc. | Yes |

#### Assessment Method

```powershell
# List running services
Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, DisplayName

# Check specific service status
Get-Service -Name "RemoteRegistry" | Select-Object Name, Status, StartType
```

#### Remediation

```powershell
# Stop and disable service
Stop-Service -Name "RemoteRegistry"
Set-Service -Name "RemoteRegistry" -StartupType Disabled
```

---

### W-20. IIS Service Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Disable unnecessary web server |

#### Assessment Method

```powershell
# Check if IIS is installed
Get-WindowsFeature -Name Web-Server

# IIS service status
Get-Service -Name "W3SVC"
```

---

### W-25. Shared Folder Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Remove unnecessary shares, verify permissions |

#### Assessment Method

```powershell
# List shared folders
Get-SmbShare

# Check administrative shares
Get-SmbShare | Where-Object {$_.Name -match '\$$'}

# Check share permissions
Get-SmbShareAccess -Name "ShareName"
```

> **WARNING**
> Administrative shares (C$, ADMIN$, etc.) are created by default for management. Remove if unnecessary, but review impact first.

---

## 4-3. Patch Management (W-40 ~ W-41)

### W-40. Apply Latest Service Pack

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Apply patches for known vulnerabilities |

#### Assessment Method

```powershell
# Check OS version and build
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber

# Check installed hotfixes
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

---

### W-41. Apply Latest Security Patches

#### Assessment Method

```powershell
# Check Windows Update history
Get-WindowsUpdateLog  # Windows 10/Server 2016 and later

# Or check for updates
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$Updates = $UpdateSearcher.Search("IsInstalled=0")
$Updates.Updates | Select-Object Title
```

---

## 4-4. Log Management (W-42 ~ W-47)

### W-42. Configure Log Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Record appropriate audit logs |

#### Recommended Audit Policies

| Policy | Success | Failure |
|--------|:-------:|:-------:|
| Audit account logon events | Yes | Yes |
| Audit account management | Yes | Yes |
| Audit logon events | Yes | Yes |
| Audit object access | Yes | Yes |
| Audit policy change | Yes | Yes |
| Audit system events | Yes | Yes |

#### Assessment Method

```powershell
# Check audit policy
auditpol /get /category:*
```

---

### W-43. Configure Log File Size

#### Recommended Settings

| Log | Max Size | Retention Policy |
|-----|:--------:|------------------|
| Application | 64MB+ | Overwrite as needed |
| Security | 128MB+ | Archive then overwrite |
| System | 64MB+ | Overwrite as needed |

#### Assessment Method

```powershell
# Check event log settings
Get-EventLog -List | Select-Object Log, MaximumKilobytes
```

---

## 4-5. Security Management (W-48 ~ W-73)

### W-48. Screen Saver Configuration

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Protect unattended terminals |

#### Recommended Settings

- Wait time: 10 minutes or less
- Password protect on resume: Enabled

---

### W-56. Windows Firewall Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Network access control |

#### Assessment Method

```powershell
# Check firewall status
Get-NetFirewallProfile | Select-Object Name, Enabled

# Check inbound rules
Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object Name, Action
```

---

### W-67. Use Updated Antivirus Software

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Malware defense |

#### Assessment Method

```powershell
# Check Windows Defender status
Get-MpComputerStatus | Select-Object AntivirusEnabled, AntispywareEnabled, RealTimeProtectionEnabled

# Check latest definition update
Get-MpComputerStatus | Select-Object AntivirusSignatureLastUpdated
```

---

## 4-6. PowerShell Assessment Script

### Integrated Assessment Script

```powershell
#===============================================
# KESE KIT - Windows Server Vulnerability Auto-Check
# Version: 1.0
#===============================================

$ReportFile = "windows_check_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

function Write-Report {
    param([string]$Message)
    Write-Host $Message
    Add-Content -Path $ReportFile -Value $Message
}

Write-Report "============================================="
Write-Report "KESE KIT Windows Vulnerability Check Results"
Write-Report "Check Date: $(Get-Date)"
Write-Report "Hostname: $env:COMPUTERNAME"
Write-Report "============================================="

# W-01: Administrator account name change
Write-Report "`n[W-01] Administrator Account Name Change"
$AdminUser = Get-LocalUser | Where-Object {$_.SID -like "*-500"}
if ($AdminUser.Name -ne "Administrator") {
    Write-Report "  [Good] Account renamed: $($AdminUser.Name)"
} else {
    Write-Report "  [Vulnerable] Using default account name"
}

# W-02: Guest account disabled
Write-Report "`n[W-02] Guest Account Disabled"
$GuestUser = Get-LocalUser -Name "Guest"
if ($GuestUser.Enabled -eq $false) {
    Write-Report "  [Good] Guest account disabled"
} else {
    Write-Report "  [Vulnerable] Guest account enabled"
}

# W-05: Account lockout policy
Write-Report "`n[W-05] Account Lockout Policy"
$NetAccounts = net accounts
$LockoutThreshold = ($NetAccounts | Select-String "Lockout threshold").ToString().Split(":")[1].Trim()
if ($LockoutThreshold -ne "Never" -and [int]$LockoutThreshold -le 5) {
    Write-Report "  [Good] Lockout threshold: $LockoutThreshold"
} else {
    Write-Report "  [Vulnerable] Lockout threshold: $LockoutThreshold (5 or less recommended)"
}

# W-14: Remote Registry service
Write-Report "`n[W-14] Remote Registry Service"
$RemoteReg = Get-Service -Name "RemoteRegistry" -ErrorAction SilentlyContinue
if ($RemoteReg.Status -ne "Running") {
    Write-Report "  [Good] Remote Registry disabled"
} else {
    Write-Report "  [Vulnerable] Remote Registry running"
}

# W-56: Windows Firewall
Write-Report "`n[W-56] Windows Firewall"
$Firewall = Get-NetFirewallProfile
$AllEnabled = ($Firewall | Where-Object {$_.Enabled -eq $true}).Count -eq 3
if ($AllEnabled) {
    Write-Report "  [Good] All firewall profiles enabled"
} else {
    Write-Report "  [Vulnerable] Some firewall profiles disabled"
}

# W-67: Antivirus software
Write-Report "`n[W-67] Antivirus Software"
try {
    $Defender = Get-MpComputerStatus
    if ($Defender.AntivirusEnabled) {
        Write-Report "  [Good] Windows Defender enabled"
    } else {
        Write-Report "  [Vulnerable] Windows Defender disabled"
    }
} catch {
    Write-Report "  [Info] Unable to check Windows Defender status"
}

Write-Report "`n============================================="
Write-Report "Check complete. Results file: $ReportFile"
```

### Script Usage

```powershell
# Run PowerShell as Administrator
# Set execution policy (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run script
.\windows_check.ps1

# View results
Get-Content .\windows_check_*.txt
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Administrator rename, Guest disable, lockout policy | Highest |
| Service Management | Disable unnecessary services, shared folder check | High |
| Patch Management | Apply latest security patches | Highest |
| Log Management | Audit policy configuration, log size | Medium |
| Security Management | Firewall, antivirus, screen saver | High |

---

*Next Chapter: Chapter 5. Web Service Assessment*
