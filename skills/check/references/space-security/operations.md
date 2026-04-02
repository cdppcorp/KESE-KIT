# Operations & Incident Response Checklist

> Domains: SO (System/Service Operations Management, 9 items) + IR (Incident Response, 2 items)

## SO — System/Service Operations Management (9 Items)

| ID | Item | Purpose | Key Verification Points |
|----|------|---------|------------------------|
| SO-01 | Maintenance Control | Control maintenance personnel, tools, and remote access | Work request/approval/logging, NDA, media sanitization, VPN+MFA for remote maintenance |
| SO-02 | System Audit & Log Analysis | Detect unauthorized/abnormal activities, ensure accountability | Audit log generation/retention, tamper protection, restricted admin access, integrated analysis/reporting |
| SO-03 | Time Synchronization | Ensure audit log accuracy and reliability | NTP standard time sync, internal NTP server, periodic verification |
| SO-04 | Portable Storage Security | Protect storage media confidentiality/integrity | Classification marking, encrypted transfer, unauthorized media control, secure disposal |
| SO-05 | Configuration Management | Establish configuration baselines, maintain integrity | HW/SW/FW baseline identification, security configuration documentation, periodic monitoring |
| SO-06 | Security Requirements Definition | Define security requirements from planning phase | Authentication/access control/encryption/logging requirements in RFP, secure coding standards |
| SO-07 | Change Management | Ensure integrity during system/application changes | Change review/approval/recording, pre-change security impact analysis, access restrictions |
| SO-08 | Development Testing & Evaluation | Verify security requirement implementation | Acceptance testing, source code verification, vulnerability scanning in production-equivalent environment |
| SO-09 | Function Minimization & SW Control | Remove unnecessary features, control unauthorized software | Essential functions only, blacklist/whitelist policies, disable DHCP/Print Spooler etc., block P2P/webhard |

### SO Protection Measures Summary

| Category | Key Actions |
|----------|-------------|
| Maintenance | Approved personnel only, clean PC with AV scan, media control, session recording |
| Logging | All systems generate audit logs, tamper-proof storage, min 1-year retention, weekly review |
| Media Control | USB port lock, media control solution, encrypted transport, overwrite-based disposal |
| Configuration | Baseline registry/account/network settings, monthly drift detection, rollback capability |
| Secure Development | Security requirements in RFP, secure coding per language (Java/PHP/ASP/C), code review |
| Change Control | Formal approval process, security impact analysis, revision history, pre/post testing |

## IR — Incident Response (2 Items)

| ID | Item | Purpose | Key Verification Points |
|----|------|---------|------------------------|
| IR-01 | Incident Handling & Testing | Minimize damage and enable rapid recovery | Incident classification, detection/response/recovery procedures, post-incident review, periodic drills |
| IR-02 | Incident Reporting | Enable consistent response through timely reporting | Internal reporting chain, regulatory notification, stakeholder communication |

### IR Protection Measures

| Measure | Detail |
|---------|--------|
| Incident Types | Malware, unauthorized access, service disruption, data breach, physical compromise |
| Response Phases | Preparation > Detection > Investigation > Analysis > Containment > Eradication > Recovery |
| Reporting Timeline | Internal: immediate; KISA: within 24 hours (per ICT Infrastructure Act Art.48-3); NIS2: 24h/72h/1month staged |
| Emergency Contacts | Quarterly review, 24/7 contact chain, regulatory liaison designated |
| Testing | Annual tabletop exercise, biannual red team drill, post-exercise lessons learned |

## Total: 11 Items (SO: 9 + IR: 2)
