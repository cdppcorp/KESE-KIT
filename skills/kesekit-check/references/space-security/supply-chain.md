# Supply Chain Threat Scenarios

> Domain: GSaaS/Supply Chain Threat Scenarios (with code-block illustrations)

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
