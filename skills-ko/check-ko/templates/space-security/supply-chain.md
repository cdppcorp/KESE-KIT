# Supply Chain Management Checklist

> Domain: SM (Supply Chain Management, 4 items)

## SM — Supply Chain Management (4 Items)

| ID | Item | Purpose | Key Verification Points |
|----|------|---------|------------------------|
| SM-01 | Supply Chain Protection | Identify and mitigate supply chain risks | Supply chain security policy, vendor selection criteria/contract security requirements, vendor registry updates |
| SM-02 | Pre-Acquisition Evaluation | Prevent vulnerable assets from entering operations | Pre-acquisition/update vulnerability scanning, acceptance testing, counterfeit inspection |
| SM-03 | All-Source Information Use | Achieve software transparency through SBOM | Require SBOM from suppliers, use SBOM for transparency/continuous management |
| SM-04 | Tampering/Counterfeiting Prevention & Detection | Detect and block supply chain tampering | Verify vendor development/distribution integrity, acceptance/operations integrity verification |

### SM Protection Measures

| Category | Measures |
|----------|----------|
| Contract Security | Training/incident notification/vulnerability remediation/audit rights/data disposal on termination in contracts |
| SBOM Management | SPDX/CycloneDX standard format, open-source/commercial SW identification, CVE periodic scanning |
| Integrity Verification | Hash value/digital signature verification, SBOM-based impact identification on new vulnerabilities |
| Vendor Management | Periodic vendor security audits, vendor registry maintenance, conditional acceptance criteria |

## Supply Chain Architecture (3 Zones)

### Satellite/Launch Vehicle Manufacturer
| Component | Security Focus |
|-----------|---------------|
| SW Development Server | IDE plugin verification, malware scanning |
| Library DB | Open-source library verification, vulnerability scanning |
| Code DB | Source code integrity, access control |
| Manufacturing Systems | Satellite bus, payload, launch vehicle manufacturing integrity |

### Ground Station Operator
| Component | Security Focus |
|-----------|---------------|
| Satellite Control System | Build pipeline security, backdoor prevention |
| SW Development Server | Secure development environment |
| SW Update Server | Update file integrity verification, secure transmission |
| Library/Code DB | Vulnerable open-source blocking, SBOM verification |

### Satellite Operator
| Component | Security Focus |
|-----------|---------------|
| Satellite Application System | Hard-coded credential prevention |
| SW Development Server | Remote work environment security |
| Data Processing System | Maintenance account management |
| Library/Code DB | Auto-build malicious open-source prevention |
