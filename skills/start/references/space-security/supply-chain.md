# Supply Chain Management Checklist

> Domain: SM (Supply Chain Management, 4 items) + GSaaS/Supply Chain Threat Scenarios

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

## Threat Scenarios (Supply Chain)

### Scenario 1: Vulnerable Open-Source Causing Ground Station Failure
```
Backdoor inserted into open-source community
  -> Library used without verification
  -> Backdoor enables system takeover
  -> Ground station service disruption
```

### Scenario 2: Malicious Code in Payload Update File
```
Developer PC compromised via phishing
  -> Ransomware inserted into SW update
  -> Update uploaded to satellite without verification
  -> Payload malfunction
```

### Scenario 3: Tampered IDE Plugin Causing Satellite Malfunction
```
Malicious code in IDE/CI-CD plugin
  -> Firmware developed/loaded without verification
  -> Component inspection skipped
  -> Satellite bus malfunction
```

## GSaaS Threat Scenarios

### Scenario 1: Satellite Control Hijacking via Weak Authentication
```
Plaintext communication sniffing
  -> IAM credential theft
  -> Web shell upload
  -> Ground station infiltration
  -> Orbit control system takeover
  -> Satellite hijacking
```

### Scenario 2: Data Tampering via Unauthorized Device Backdoor
```
No media control
  -> USB/single-board-computer backdoor
  -> Internal network access
  -> Satellite access credential collection
  -> Data tampering malware injection
```

### Scenario 3: Physical Attack via Drone Disrupting Satellite Communication
```
Plaintext communication sniffing
  -> Antenna location identified
  -> Drone with jamming device/explosives
  -> Antenna-satellite communication disrupted
```

## Total: 4 Checklist Items + 6 Threat Scenarios
