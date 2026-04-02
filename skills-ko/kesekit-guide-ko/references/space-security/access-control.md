# Access Control & Authentication Checklist

> Domains: AC (Access Control, 12 items) + IA (Identification & Authentication, 2 items)

## AC — Access Control (12 Items)

| ID | Item | Purpose | Key Verification Points |
|----|------|---------|------------------------|
| AC-01 | Access Control Policy | Restrict access to authorized users/processes/devices only | Access control policy established, authorized entities identified, per-system access rules defined |
| AC-02 | Least Privilege | Grant minimum necessary permissions | Least privilege procedures, management approval, periodic review |
| AC-03 | Privileged Access Use | Restrict and audit privileged account usage | Privileged account types defined/limited, audit logs stored/reviewed |
| AC-04 | Information Flow Control | Control information flow within and between systems | Flow control policy, source/destination identification, change approval |
| AC-05 | Separation of Duties | Prevent authority abuse through role separation | Duty separation policy, critical duties separated, compensating controls |
| AC-06 | Failed Login Attempts | Protect accounts from brute-force attacks | Max attempt limits, auto-lockout policy, alert/notification on failures |
| AC-07 | Session Lock & Termination | Prevent unauthorized access during idle sessions | Auto-lock on inactivity, re-authentication required, session termination conditions |
| AC-08 | Remote Access Control | Prevent unauthorized remote access | Remote access policy, device security check/MFA/encryption, monitoring/logging |
| AC-09 | Wireless Access | Prevent unauthorized wireless connections | Wireless policy, authentication/encryption, unauthorized AP prevention |
| AC-10 | Mobile Device Control | Control mobile device connections | Mobile device policy, data encryption, loss/theft protection |
| AC-11 | External Connection Control | Protect system boundaries from external systems | External systems identified, approved methods only, continuous monitoring |
| AC-12 | Public Information Control | Prevent sensitive information disclosure | Pre-publication review/approval, designated reviewers, periodic content review |

### AC Protection Measures Summary

| Category | Measures |
|----------|----------|
| Account Management | 1-person-1-account, default account deletion, immediate revocation on termination, annual full review |
| Authentication | MFA for privileged access, SSH/SFTP/VPN only, 8+ char passwords with 2+ character types |
| Network | ACL-based deny-all, IP/port whitelisting, WPA3/WPA2-Enterprise, WIPS deployment |
| Session | 10-min inactivity lock, screensaver with password, session timeout enforcement |
| Remote Access | 3-step procedure (request/approve/monitor), VPN+MFA, high-risk assets remote-access-denied by default |
| Monitoring | Failed login alerts to SOC, audit log analysis, access log review |

## IA — Identification & Authentication (2 Items)

| ID | Item | Purpose | Key Verification Points |
|----|------|---------|------------------------|
| IA-01 | Identification & Authentication | Prevent unauthorized access and credential theft | Unique identifiers for users/processes/devices, password complexity (upper+lower+special+number, 8+ chars), cryptographic protection, reuse prevention |
| IA-02 | Multi-Factor Authentication | Strengthen privileged account authentication, prevent replay attacks | MFA for privileged network access, replay attack prevention (challenge-response/timestamp) |

### IA Protection Measures

| Measure | Detail |
|---------|--------|
| Password Policy | Min 8 chars, 3+ character types, 90-day rotation, history check (last 5) |
| MFA Methods | OTP, certificate, biometric — at least 2 factors required |
| Replay Prevention | Challenge-response protocol, timestamp-based token validation |
| Credential Storage | Hashed (SHA-256+), no plaintext storage, encrypted transmission |

## Total: 14 Items (AC: 12 + IA: 2)
