# OT/ICS Zero Trust Deployment Guide

> Reference: KISA 제로트러스트 가이드라인 2.0, NIST SP 800-82 Rev.3, IEC 62443
> Purpose: Guidance for deploying Zero Trust in OT/ICS environments

## Why OT/ICS Requires Special ZT Consideration

Traditional IT Zero Trust assumes:
- Modern endpoints capable of running agents
- Tolerance for additional authentication latency
- Ability to patch and update frequently
- Replaceable infrastructure components

OT/ICS reality:
- Legacy devices (PLCs, RTUs, HMIs) with 15-30 year lifecycles
- Real-time control loops with microsecond-level latency requirements
- Safety-critical functions where authentication delays can cause harm
- Proprietary protocols (Modbus, DNP3, OPC UA, PROFINET)
- Air-gapped or semi-isolated networks

## Phased Deployment Approach

### Phase 1: Visibility & Asset Discovery

**Objective**: Know what you have before you protect it.

- Conduct complete OT asset inventory (active + passive discovery)
- Map communication flows between OT devices, IT systems, and external connections
- Identify Purdue Model levels for each asset
- Baseline normal traffic patterns and protocol usage
- Document legacy devices that cannot support modern security controls

### Phase 2: IT-OT Boundary Segmentation

**Objective**: Establish strong boundary between IT and OT networks.

- Deploy industrial DMZ between IT and OT networks
- Implement data diodes or unidirectional gateways for critical flows
- Control all IT-OT data exchange through monitored jump servers
- Establish separate authentication domains for IT and OT

### Phase 3: OT Internal Segmentation

**Objective**: Apply zone/conduit model within OT network.

- Implement IEC 62443 zones and conduits
- Segment by safety level (SL), function, and criticality
- Deploy OT-aware firewalls between zones
- Establish conduit-level access policies

### Phase 4: Identity & Access Control

**Objective**: Enforce identity-based access in OT environment.

- Deploy MFA for all remote OT access (hardware tokens preferred)
- Implement privileged access management (PAM) for OT systems
- Apply least-privilege access for OT operators and engineers
- Manage shared/service accounts with rotation and monitoring
- Use jump servers with session recording for maintenance access

### Phase 5: Continuous Monitoring

**Objective**: Maintain visibility and detect anomalies.

- Deploy OT-specific IDS/IPS (passive monitoring preferred initially)
- Implement Deep Packet Inspection (DPI) for OT protocols
- Integrate OT security events with enterprise SIEM
- Establish OT-specific SOC or extend IT SOC with OT expertise
- Monitor for known OT malware signatures (Triton, Industroyer, etc.)

### Phase 6: Automated Response (with Safety Validation)

**Objective**: Enable automated response without compromising safety.

- Define automated response actions with safety impact assessment
- Implement fail-safe defaults (fail-open for safety-critical, fail-close for non-critical)
- Require human approval for actions affecting safety systems
- Test automated responses in simulation environment before deployment

## OT-Specific ZT Architecture

```
┌────────────────────────────────────────────┐
│              Enterprise Zone (IT)           │
│  ┌────────┐  ┌────────┐  ┌────────────┐   │
│  │  PDP   │  │ IdP/   │  │ Enterprise │   │
│  │        │  │ MFA    │  │ SIEM       │   │
│  └────────┘  └────────┘  └────────────┘   │
└──────────────────┬─────────────────────────┘
                   │ Industrial DMZ
┌──────────────────┴─────────────────────────┐
│  ┌────────────┐  ┌─────────┐  ┌────────┐  │
│  │ Jump Server│  │ Historian│  │ PEP    │  │
│  │ (PAM)     │  │ Mirror  │  │ (OT)   │  │
│  └────────────┘  └─────────┘  └────────┘  │
└──────────────────┬─────────────────────────┘
                   │
┌──────────────────┴─────────────────────────┐
│              OT Zone (ICS/SCADA)            │
│  ┌────────┐  ┌────────┐  ┌────────────┐   │
│  │  HMI   │  │  PLC   │  │    RTU     │   │
│  │        │  │        │  │            │   │
│  └────────┘  └────────┘  └────────────┘   │
│  ┌────────────────────────────────────┐    │
│  │   OT IDS (Passive Monitoring)     │    │
│  └────────────────────────────────────┘    │
└────────────────────────────────────────────┘
```

## Legacy Device Handling

For OT devices that cannot support modern ZT controls:

1. **Security Wrapper/Proxy**: Place a ZT-capable proxy in front of legacy devices
2. **Network-Level Protection**: Use OT-aware firewalls to enforce access policies
3. **Monitoring**: Deploy passive DPI sensors for visibility without device modification
4. **Compensating Controls**: Document risk acceptance with compensating controls per IEC 62443

## Standards Mapping

| OT-ZT Requirement | IEC 62443 | NIST SP 800-82 | KISA ZT 2.0 |
|-------------------|-----------|----------------|-------------|
| Network Segmentation | Zone/Conduit | Section 5.3 | NW Element |
| Access Control | FR 1 (AC) | Section 6.2 | ID Element |
| Device Management | FR 4 (DC) | Section 6.3 | DV Element |
| Communication Integrity | FR 3 (SI) | Section 5.4 | SY Element |
| Monitoring | FR 6 (RE) | Section 6.6 | VA Element |
| Incident Response | FR 7 (RA) | Section 6.7 | AU Element |
