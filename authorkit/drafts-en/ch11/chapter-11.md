# Chapter 11. PC and Endpoint Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

PCs and endpoints are the points of direct contact with users. This chapter covers 18 assessment items (PC-01 ~ PC-18).

```
┌─────────────────────────────────────────────────────────────────┐
│           PC/Endpoint Vulnerability Assessment Domains (18)      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │     User PC     │                          │
│                    │   (Endpoint)    │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│     ┌───────────────────────┼───────────────────────┐           │
│     │           │           │           │           │           │
│     ▼           ▼           ▼           ▼           ▼           │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐         │
│ │Account│  │ Access│  │ Patch │  │Security│ │ Data  │         │
│ │ Mgmt  │  │ Mgmt  │  │ Mgmt  │  │ Mgmt   │ │Protect│         │
│ │PC-01~4│  │PC-05~11│ │PC-12~13│ │PC-14~18│ │(Integ)│         │
│ │  (4)  │  │  (7)  │  │  (2)  │  │  (5)   │ │       │         │
│ │       │  │       │  │       │  │        │ │       │         │
│ │•Unnec-│  │•Shared│  │• OS   │  │•Anti-  │ │•Encrypt│        │
│ │ essary│  │ folder│  │ patch │  │ virus  │ │•DLP   │         │
│ │ acct  │  │• USB  │  │• App  │  │•Fire-  │ │       │         │
│ │•Screen│  │ block │  │ patch │  │ wall   │ │       │         │
│ │ saver │  │       │  │       │  │        │ │       │         │
│ └───────┘  └───────┘  └───────┘  └────────┘ └───────┘         │
│                             │                                    │
│                             ▼                                    │
│              ┌───────────────────────────┐                      │
│              │ Unified Endpoint Security │                      │
│              │    (EDR / MDM / NAC)      │                      │
│              └───────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | PC-01 ~ PC-04 | 4 |
| Access Management | PC-05 ~ PC-11 | 7 |
| Patch Management | PC-12 ~ PC-13 | 2 |
| Security Management | PC-14 ~ PC-18 | 5 |

---

## 11-1. Account Management (PC-01 ~ PC-04)

### PC-01. Remove Unnecessary Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access through unused accounts |

#### Assessment Method (Windows)

```powershell
# Check local accounts
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Verify Guest account is disabled
Get-LocalUser -Name "Guest" | Select-Object Enabled
```

---

### PC-03. Screen Saver Configuration

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Recommended** | Within 10 minutes, password protected |

#### Assessment Method (Windows Registry)

```powershell
# Check registry
Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" | Select-Object ScreenSaveActive, ScreenSaverIsSecure, ScreenSaveTimeOut
```

---

## 11-2. Access Management (PC-05 ~ PC-11)

### PC-05. Shared Folder Assessment

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Remove unnecessary shares |

#### Assessment Method

```powershell
# Check shared folders
Get-SmbShare | Select-Object Name, Path, Description

# Check shares accessible by Everyone
Get-SmbShareAccess -Name "ShareName" | Where-Object {$_.AccountName -eq "Everyone"}
```

---

### PC-08. Restrict Removable Storage Media

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent data leakage via USB |

#### Group Policy Configuration

```
Computer Configuration > Administrative Templates > System > Removable Storage Access
- Removable Disks: Deny read access
- Removable Disks: Deny write access
```

---

## 11-3. Patch Management (PC-12 ~ PC-13)

### PC-12. Operating System Patches

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Apply latest security patches |

#### Assessment Method

```powershell
# Check recently installed updates
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5

# Check pending updates
(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0").Updates | Select-Object Title
```

---

## 11-4. Security Management (PC-14 ~ PC-18)

### PC-14. Antivirus Installation and Updates

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Malware defense |

#### Assessment Method (Windows Defender)

```powershell
# Windows Defender status
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated
```

---

### PC-17. Personal Firewall Usage

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Network attack defense |

#### Assessment Method

```powershell
# Windows Firewall status
Get-NetFirewallProfile | Select-Object Name, Enabled
```

---

## PC Assessment Script

```powershell
#===============================================
# KESE KIT - PC Security Assessment Script
#===============================================

Write-Host "===== PC Security Assessment =====" -ForegroundColor Cyan

# PC-01: Guest account
Write-Host "`n[PC-01] Guest Account Status"
$guest = Get-LocalUser -Name "Guest"
if ($guest.Enabled) { Write-Host "  [Vulnerable] Guest enabled" -ForegroundColor Red }
else { Write-Host "  [Good] Guest disabled" -ForegroundColor Green }

# PC-05: Shared folders
Write-Host "`n[PC-05] Shared Folders"
Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | ForEach-Object {
    Write-Host "  Share: $($_.Name) - $($_.Path)"
}

# PC-14: Antivirus status
Write-Host "`n[PC-14] Antivirus Status"
$defender = Get-MpComputerStatus
if ($defender.AntivirusEnabled -and $defender.RealTimeProtectionEnabled) {
    Write-Host "  [Good] Windows Defender enabled" -ForegroundColor Green
} else {
    Write-Host "  [Vulnerable] Windows Defender disabled" -ForegroundColor Red
}

# PC-17: Firewall
Write-Host "`n[PC-17] Firewall Status"
$firewallEnabled = (Get-NetFirewallProfile | Where-Object {$_.Enabled -eq $true}).Count
if ($firewallEnabled -eq 3) {
    Write-Host "  [Good] All profiles enabled" -ForegroundColor Green
} else {
    Write-Host "  [Vulnerable] Some profiles disabled" -ForegroundColor Red
}

Write-Host "`n===== Assessment Complete =====" -ForegroundColor Cyan
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Unnecessary accounts, screen saver | High |
| Access Management | Shared folders, removable media | High |
| Patch Management | OS patches | Highest |
| Security Management | Antivirus, firewall | Highest |

---

*Next Chapter: Chapter 12. Control System (OT) Assessment*
