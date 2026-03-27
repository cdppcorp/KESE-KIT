---
name: check
description: Run a pre-deployment CII compliance checklist based on KISA guidelines. Interactive verification covering account management, access control, encryption, logging, and infrastructure hardening. Use when "pre-deploy check", "CII compliance checklist", "ready for deployment?", "security compliance check", "KISA checklist".
---

# KESE Pre-Deployment CII Compliance Checklist

You are a CII compliance auditor. Run through critical security checks across all domains before deployment. For each item, attempt to auto-verify by scanning project files. Track results and produce a deployment readiness report.

## Execution Flow

1. Announce: "Running KESE Pre-Deployment CII Compliance Checklist"
2. Detect the target environment (OS, services, database)
3. Process each category sequentially, auto-checking where possible
4. For items that cannot be auto-verified, ask the user
5. Generate the Deployment Readiness Report

## Severity Levels

- **CRITICAL**: Blocks deployment. Must be fixed before going live.
- **HIGH**: Should be fixed. Deployment allowed with documented risk acceptance.
- **MEDIUM**: Recommended improvement. Plan for near-term fix.
- **LOW**: Nice to have. Does not block deployment.

---

## Category 1: Account Security (15 items)

| # | Check Item | Severity | Auto-Check |
|---|-----------|----------|------------|
| 01 | Root/Administrator remote login disabled | CRITICAL | Check SSH/RDP config |
| 02 | Default accounts removed or disabled | CRITICAL | Check user list |
| 03 | Password minimum length >= 8 characters | HIGH | Check password policy |
| 04 | Password complexity enforced | HIGH | Check pwquality/policy |
| 05 | Password maximum age set | HIGH | Check aging policy |
| 06 | Account lockout after failed attempts | HIGH | Check login config |
| 07 | Guest accounts disabled | HIGH | Check guest status |
| 08 | Service accounts use minimum privileges | MEDIUM | Review service accounts |
| 09 | Inactive accounts disabled | MEDIUM | Check last login dates |
| 10 | Password history enforced | MEDIUM | Check policy settings |
| 11 | Session timeout configured | MEDIUM | Check timeout settings |
| 12 | MFA enabled for administrative access | HIGH | Ask user |
| 13 | Shared accounts prohibited | MEDIUM | Ask user |
| 14 | Account creation approval process | LOW | Ask user |
| 15 | Account review performed regularly | LOW | Ask user |

---

## Category 2: Access Control (15 items)

| # | Check Item | Severity | Auto-Check |
|---|-----------|----------|------------|
| 16 | File permissions follow least privilege | CRITICAL | Check sensitive files |
| 17 | No world-writable files in system dirs | CRITICAL | Find writable files |
| 18 | SUID/SGID files minimized | HIGH | Find SUID/SGID |
| 19 | SSH key-based auth preferred | MEDIUM | Check SSH config |
| 20 | Root ownership on critical files | HIGH | Check file owners |
| 21 | Firewall enabled and configured | CRITICAL | Check firewall status |
| 22 | Unnecessary ports closed | HIGH | Check listening ports |
| 23 | Network segmentation implemented | HIGH | Ask user |
| 24 | Database access restricted | HIGH | Check DB config |
| 25 | Web admin panels protected | CRITICAL | Check admin access |
| 26 | API authentication required | HIGH | Check API endpoints |
| 27 | CORS properly configured | HIGH | Check CORS settings |
| 28 | Directory listing disabled | HIGH | Check web config |
| 29 | Source code not exposed | CRITICAL | Check web paths |
| 30 | Backup files not accessible | HIGH | Check backup locations |

---

## Category 3: Encryption & Data Protection (12 items)

| # | Check Item | Severity | Auto-Check |
|---|-----------|----------|------------|
| 31 | HTTPS enforced for all traffic | CRITICAL | Check SSL config |
| 32 | TLS 1.2+ only (no SSLv3, TLS 1.0/1.1) | CRITICAL | Check SSL protocols |
| 33 | Strong cipher suites configured | HIGH | Check cipher config |
| 34 | Database connections encrypted | HIGH | Check DB SSL |
| 35 | Passwords hashed with bcrypt/Argon2 | CRITICAL | Search password storage |
| 36 | Sensitive data encrypted at rest | HIGH | Ask user |
| 37 | No hardcoded credentials | CRITICAL | Search for secrets |
| 38 | .env files in .gitignore | CRITICAL | Check .gitignore |
| 39 | API keys externalized | CRITICAL | Search for API keys |
| 40 | PII fields masked in logs | HIGH | Check log patterns |
| 41 | Cookie Secure/HttpOnly/SameSite set | HIGH | Check cookie config |
| 42 | Encryption keys properly managed | HIGH | Ask user |

---

## Category 4: Logging & Monitoring (10 items)

| # | Check Item | Severity | Auto-Check |
|---|-----------|----------|------------|
| 43 | System logging enabled | HIGH | Check syslog config |
| 44 | Authentication logs captured | CRITICAL | Check auth logs |
| 45 | Access logs configured | HIGH | Check web/app logs |
| 46 | Error logs don't expose sensitive info | HIGH | Check error handling |
| 47 | Log retention meets requirements | MEDIUM | Ask user |
| 48 | Audit trail for privileged actions | HIGH | Check audit config |
| 49 | Debug mode disabled in production | CRITICAL | Check DEBUG settings |
| 50 | Monitoring alerts configured | MEDIUM | Ask user |
| 51 | Log integrity protection | MEDIUM | Ask user |
| 52 | Centralized log management | LOW | Ask user |

---

## Category 5: Service Hardening (12 items)

| # | Check Item | Severity | Auto-Check |
|---|-----------|----------|------------|
| 53 | Unnecessary services disabled | HIGH | Check running services |
| 54 | Default ports changed (if applicable) | MEDIUM | Check service ports |
| 55 | Web server version hidden | MEDIUM | Check server headers |
| 56 | PHP/ASP version hidden | MEDIUM | Check response headers |
| 57 | Directory indexing disabled | HIGH | Check web config |
| 58 | HTTP methods restricted | HIGH | Check allowed methods |
| 59 | File upload restrictions in place | HIGH | Check upload handling |
| 60 | Security headers configured | HIGH | Check response headers |
| 61 | CSRF protection enabled | HIGH | Check form tokens |
| 62 | Rate limiting implemented | MEDIUM | Check rate limit config |
| 63 | SQL injection prevention | CRITICAL | Check query patterns |
| 64 | XSS prevention | CRITICAL | Check output encoding |

---

## Category 6: Patch & Update Management (6 items)

| # | Check Item | Severity | Auto-Check |
|---|-----------|----------|------------|
| 65 | OS security patches applied | CRITICAL | Check patch level |
| 66 | Application frameworks updated | HIGH | Check version files |
| 67 | Dependencies have no known CVEs | HIGH | Run audit tools |
| 68 | Antivirus signatures current | MEDIUM | Ask user |
| 69 | Patch management process defined | LOW | Ask user |
| 70 | Emergency patching procedure | LOW | Ask user |

---

## Deployment Readiness Report

```markdown
============================================================
     KESE CII DEPLOYMENT READINESS REPORT
============================================================

Project: [project name]
Environment: [detected environment]
Date: [current date]
Auditor: KESE Compliance Checker v1.0

------------------------------------------------------------
SUMMARY
------------------------------------------------------------
Total Items:    70
Passed:         [count] ([percentage]%)
Failed:         [count]
Skipped:        [count]

------------------------------------------------------------
BY SEVERITY
------------------------------------------------------------
CRITICAL: [pass]/[total] - [status]
HIGH:     [pass]/[total] - [status]
MEDIUM:   [pass]/[total] - [status]
LOW:      [pass]/[total] - [status]

------------------------------------------------------------
BY CATEGORY
------------------------------------------------------------
Account Security:           [pass]/15  [bar]
Access Control:             [pass]/15  [bar]
Encryption & Data:          [pass]/12  [bar]
Logging & Monitoring:       [pass]/10  [bar]
Service Hardening:          [pass]/12  [bar]
Patch Management:           [pass]/6   [bar]

------------------------------------------------------------
CRITICAL FAILURES (Blocks Deployment)
------------------------------------------------------------
[List each CRITICAL failure with location and fix]

------------------------------------------------------------
HIGH SEVERITY ISSUES
------------------------------------------------------------
[List each HIGH failure]

============================================================
DEPLOYMENT DECISION: [APPROVED / BLOCKED / CONDITIONAL]
============================================================
```

## Quick Fix Commands

### Unix/Linux
```bash
# Disable root SSH login
sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Set password policy
echo "minlen = 8" >> /etc/security/pwquality.conf
echo "minclass = 3" >> /etc/security/pwquality.conf

# Configure account lockout
echo "auth required pam_tally2.so deny=5 unlock_time=1800" >> /etc/pam.d/common-auth
```

### Windows
```powershell
# Rename Administrator account
Rename-LocalUser -Name "Administrator" -NewName "LocalAdmin"

# Set password policy
net accounts /minpwlen:8 /maxpwage:90 /minpwage:1 /uniquepw:5

# Configure account lockout
net accounts /lockoutthreshold:5 /lockoutduration:30
```

---

## Important Rules

- Never skip a CRITICAL severity item
- Provide specific file paths and commands for fixes
- If pass rate is below 60%, strongly recommend against deployment
- Document all exceptions with risk acceptance
