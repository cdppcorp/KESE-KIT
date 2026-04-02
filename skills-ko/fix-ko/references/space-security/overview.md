# Space Security Overview

> Source: KISA "Space Security Model" Part1 (2024.12) + Part2 (2025.12) + Explanation Guide (2025.12)

## 1. Overview

| Item | Content |
|------|---------|
| Publisher | KISA (Korea Internet & Security Agency) / MSIT |
| Target | Space industry operators, satellite service providers, GSaaS providers, supply chain participants |
| Scope | Space segment, Ground segment, Satellite service segment, GSaaS, Supply chain |
| Standards | CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, NIST CSF, CCSDS |

## 2. Space Architecture Layers

| Layer | Components |
|-------|-----------|
| Space Segment | GEO/MEO/LEO satellites, LEO constellations, satellite bus, payload, OBC |
| Ground Segment | Satellite control, payload data processing, antenna, satellite modem, mission control |
| GSaaS | Antenna zone, ground station-cloud zone, reservation/scheduling, API/DB servers |
| Satellite Services | Navigation (GNSS), Communication (VSAT/LEO), Broadcasting |
| Supply Chain | Satellite/launch vehicle manufacturers, ground station operators, satellite operators |

## 3. Satellite Service Types

| Service | Description | Key Components |
|---------|-------------|----------------|
| Navigation (GNSS) | Position/navigation/timing via GNSS satellites | Smart ships, autonomous vehicles, UAM |
| Communication | Satellite-based data/voice communication | VSAT, LEO mobile, LEO internet |
| Broadcasting | Satellite TV/radio relay | Broadcasting centers, set-top boxes |
| GSaaS | Ground Station as a Service (cloud-based shared infrastructure) | Shared antennas, cloud scheduling, API |

## 4. Security Objectives

| Objective | Description |
|-----------|-------------|
| Confidentiality | Prevent unauthorized access to satellite data and communications |
| Integrity | Prevent unauthorized modification of commands, telemetry, and operational data |
| Availability | Ensure continuous satellite service operation |
| Authentication | Verify identity of users, processes, devices, and satellites |
| Non-repudiation | Ensure accountability for satellite operations |
| Resilience | Maintain operations during and after security incidents |

## 5. Threat Categories (3 Major Types)

| Type | Description | Attack Vectors |
|------|-------------|----------------|
| Data Corruption | Unauthorized data modification/deletion | MITM, spoofing, malware, insider threat |
| Service Disruption | Service interruption/degradation | Jamming, DDoS, physical destruction, SW vulnerabilities |
| Information Leakage | Sensitive data exfiltration | Eavesdropping, sniffing, session hijacking, data theft |

## 6. Checklist Structure (12 Domains, 53 Items)

| # | Code | Domain | Items | Reference File |
|---|------|--------|:-----:|----------------|
| 1 | AC | Access Control | 12 | `access-control.md` |
| 2 | IA | Identification & Authentication | 2 | `access-control.md` |
| 3 | SC | System & Communication Security | 7 | `system-security.md` |
| 4 | SI | System & Information Integrity | 4 | `system-security.md` |
| 5 | SO | System/Service Operations Management | 9 | `operations.md` |
| 6 | IR | Incident Response | 2 | `operations.md` |
| 7 | PS | Personnel Security | 2 | `governance.md` |
| 8 | PE | Physical & Environmental Security | 3 | `governance.md` |
| 9 | RA | Risk Assessment & Security Evaluation | 2 | `governance.md` |
| 10 | SG | Security Governance | 4 | `governance.md` |
| 11 | CP | Contingency Planning | 2 | `governance.md` |
| 12 | SM | Supply Chain Management | 4 | `supply-chain.md` |

## 7. Compliance Standards

| Standard | Description |
|----------|-------------|
| CMMC | Cybersecurity Maturity Model Certification (US DoD, Level 1-3) |
| K-RMF | Korea Risk Management Framework |
| NIS2 | EU Network and Information Security Directive (includes space) |
| ISMS-P | Korea Information Security Management System |
| NIST IR 8401 | Satellite Ground Segment Cybersecurity |
| NIST IR 8270 | Commercial Satellite Operations Cybersecurity |
| NIST CSF | Cybersecurity Framework (Identify/Protect/Detect/Respond/Recover) |
| NIST SP 800-171 | CUI Protection (110 requirements) |
| CCSDS 352.0-B-2 | Space System Cryptographic Algorithm Recommendation |
| ENISA Space Threat Landscape | Space system threat analysis |
