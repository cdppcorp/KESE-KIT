# Chapter 14. Asset Management and Risk Management

> Part III. Administrative and Physical Vulnerability Assessment

---

## Overview

Asset management and risk management form the foundation of information security. You need to identify assets to protect and assess risks to establish appropriate protection measures. This chapter covers Asset Classification (A-10 ~ A-14), Risk Management (A-15 ~ A-17), and Audit (A-18 ~ A-20).

| Domain | Items | Count |
|--------|-------|:-----:|
| Asset Classification | A-10 ~ A-14 | 5 |
| Risk Management | A-15 ~ A-17 | 3 |
| Audit | A-18 ~ A-20 | 3 |

---

## 14-1. Asset Classification (A-10 ~ A-14)

### A-10. Establish Asset Classification Criteria

| Item | Content |
|------|---------|
| **Assessment Item** | Identify all assets (personnel, facilities, equipment, etc.) within critical information infrastructure and establish documented asset classification criteria |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Asset Types

| Type | Examples |
|------|----------|
| Information Assets | Databases, documents, software |
| Physical Assets | Servers, network equipment, PCs |
| Human Assets | System administrators, developers |
| Facility Assets | Data center, communications room, protected areas |

#### Classification Criteria Example

| Level | Confidentiality | Integrity | Availability |
|:-----:|-----------------|-----------|--------------|
| Level 1 | Secret | Operations impossible if damaged | Immediate recovery required |
| Level 2 | Confidential | Operations impaired if damaged | Recovery within 4 hours |
| Level 3 | General | Recoverable | Recovery within 1 day |

---

### A-11. Security Level Classification Management

| Item | Content |
|------|---------|
| **Assessment Item** | Classify and manage information assets according to security level and importance |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Security Level Classification

| Level | Definition | Examples |
|:-----:|------------|----------|
| Top Secret | Disclosure affects national security | Encryption keys, core designs |
| Secret | Disclosure causes severe organizational damage | Personal information, financial data |
| Confidential | Disclosure causes organizational damage | Internal business documents |
| General | Can be disclosed | Marketing materials, public documents |

---

### A-12. Asset Inventory Management

| Item | Content |
|------|---------|
| **Assessment Item** | Create and maintain an up-to-date asset inventory reflecting regular asset status surveys and changes (acquisition, disposal, transfer, etc.) |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Required Asset Inventory Fields

| Field | Description |
|-------|-------------|
| Asset ID | Unique identifier |
| Asset Name | Equipment/system name |
| Category | Server/network/endpoint, etc. |
| Location | Installation location |
| Administrator | Responsible person/department |
| Security Level | Level 1/2/3 |
| Acquisition Date | Purchase date |
| Change History | Transfer/replacement/disposal history |

---

### A-13. Asset Handling Procedures

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement handling procedures (creation/acquisition, storage, use, disposal) and protection measures according to asset classification |
| **Related Dept.** | Information Security Department, Asset Management Department |

#### Lifecycle-based Protection Measures

| Stage | Level 1 | Level 2 | Level 3 |
|-------|---------|---------|---------|
| Acquisition | Approval required | Approval required | Registration |
| Storage | Encryption + isolation | Encryption | Standard storage |
| Use | Access log + approval | Access log | Basic control |
| Disposal | Secure deletion + certificate | Secure deletion | Format/delete |

---

### A-14. Asset Manager Designation

| Item | Content |
|------|---------|
| **Assessment Item** | Designate administrators and management owners for each information asset and maintain an up-to-date list |
| **Related Dept.** | Information Security Department, All Departments |

#### Role Definitions

| Role | Responsibility |
|------|----------------|
| Asset Owner | Ultimate responsibility for the asset |
| Asset Administrator | Day-to-day management and operations |
| Asset User | Use within authorized scope |

---

## 14-2. Risk Management (A-15 ~ A-17)

### A-15. Service Status Identification

| Item | Content |
|------|---------|
| **Assessment Item** | Identify service status of critical information infrastructure, understand business processes and flows, and document them |
| **Related Dept.** | Information Security Department, System Operations Department |

#### Service Status Documentation Content

- Service list and descriptions
- Business flow diagrams (Data Flow Diagram)
- System architecture diagrams
- Network topology
- Connected systems status

---

### A-16. Risk Assessment Execution

| Item | Content |
|------|---------|
| **Assessment Item** | Conduct risk assessment at least annually on a regular basis |
| **Related Dept.** | Information Security Department |

#### Risk Assessment Process

```
┌─────────────────────────────────────────────────────────────────┐
│                     Risk Assessment Process                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌───────────┐     ┌───────────┐     ┌───────────┐            │
│   │ 1. Asset  │────▶│ 2. Threat │────▶│3. Vuln.   │            │
│   │   Ident.  │     │   Ident.  │     │  Ident.   │            │
│   └───────────┘     └───────────┘     └─────┬─────┘            │
│                                             │                    │
│                                             ▼                    │
│                                   ┌─────────────────┐           │
│                                   │  4. Risk Level  │           │
│                                   │   Calculation   │           │
│                                   │                 │           │
│                                   │ Risk = Asset    │           │
│                                   │    × Threat     │           │
│                                   │    × Vuln.      │           │
│                                   └────────┬────────┘           │
│                                            │                     │
│                                            ▼                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              5. Risk Treatment Decision                  │   │
│   ├─────────────┬─────────────┬─────────────┬───────────────┤   │
│   │   Reduce    │  Transfer   │    Avoid    │    Accept     │   │
│   │ (Controls)  │ (Insurance) │(Discontinue)│(Mgmt Approval)│   │
│   └─────────────┴─────────────┴─────────────┴───────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Risk Treatment Options

| Option | Description | Example |
|--------|-------------|---------|
| Risk Reduction | Apply protection measures | Deploy firewall, encryption |
| Risk Transfer | Transfer through insurance, etc. | Cyber insurance |
| Risk Avoidance | Eliminate risk source | Service discontinuation |
| Risk Acceptance | Accept residual risk | Accept with executive approval |

---

### A-17. Protection Measure Implementation Plan

| Item | Content |
|------|---------|
| **Assessment Item** | Establish annual protection measure implementation plan based on risk assessment and report to executive management |
| **Related Dept.** | Information Security Department, Executive Management |

#### Implementation Plan Components

| Item | Content |
|------|---------|
| Measure Name | Specific protection measure |
| Owner | Implementation responsibility |
| Schedule | Start date/completion date |
| Budget | Required cost |
| Effect | Risk reduction level |

---

## 14-3. Audit (A-18 ~ A-20)

### A-18. Legal Requirements Compliance Review

| Item | Content |
|------|---------|
| **Assessment Item** | Review compliance with legal requirements at least annually on a regular basis |
| **Related Dept.** | Information Security Department, Legal Department |

#### Key Legal Requirements

| Regulation | Key Content |
|------------|-------------|
| Act on Protection of Information and Communications Infrastructure | Vulnerability analysis and assessment, protection measure establishment |
| Personal Information Protection Act | Security measures, access control |
| Electronic Financial Transactions Act | Electronic financial transaction security |
| Information and Communications Network Act | Technical and administrative protection measures |

---

### A-19. Information Security Audit

| Item | Content |
|------|---------|
| **Assessment Item** | Establish and implement periodic information security audit plan |
| **Related Dept.** | Audit Department, Information Security Department |

#### Audit Types

| Type | Frequency | Performed By |
|------|:---------:|--------------|
| Regular Audit | At least annually | Internal audit team |
| Ad-hoc Audit | As needed | Internal audit team |
| External Audit | As needed | External professional organization |

---

### A-20. Audit Results Reporting and Follow-up

| Item | Content |
|------|---------|
| **Assessment Item** | Report audit results to executive management and implement appropriate follow-up actions |
| **Related Dept.** | Audit Department, Executive Management |

#### Audit Follow-up Actions

1. Prepare audit result report
2. Report to executive management
3. Develop corrective action plan
4. Implement corrective actions
5. Verify implementation

---

## 14-4. Asset Inventory Management Automation

### Asset Inventory Template (Excel/CSV)

```csv
AssetID,AssetName,Type,Location,Administrator,SecurityLevel,AcquisitionDate,Status,Notes
A001,DBServer01,Server,DataCenterA,Kim,Level1,2024-01-15,Operational,Oracle DB
A002,WebServer01,Server,DataCenterA,Kim,Level2,2024-02-20,Operational,Apache
A003,Switch01,Network,CommRoom,Park,Level2,2023-05-10,Operational,Cisco
```

### Asset Collection Script (PowerShell)

```powershell
#===============================================
# KESE KIT - Asset Information Collection Script
#===============================================

$report = @()

# Collect server information
Get-ADComputer -Filter * -Properties * | ForEach-Object {
    $report += [PSCustomObject]@{
        AssetName = $_.Name
        Type = "Server"
        OS = $_.OperatingSystem
        IPAddress = $_.IPv4Address
        LastLogon = $_.LastLogonDate
    }
}

# Export to CSV
$report | Export-Csv -Path "asset_inventory.csv" -Encoding UTF8 -NoTypeInformation

Write-Host "Asset inventory generated: asset_inventory.csv"
```

### Asset Change Monitoring (Python)

```python
"""
KESE KIT - Asset Change Monitoring
Compares with previous snapshot to detect changes
"""
import pandas as pd
from datetime import datetime

def compare_assets(old_file, new_file):
    """Compare asset inventories"""
    old_df = pd.read_csv(old_file)
    new_df = pd.read_csv(new_file)

    # New assets
    new_assets = new_df[~new_df['AssetID'].isin(old_df['AssetID'])]

    # Removed assets
    removed_assets = old_df[~old_df['AssetID'].isin(new_df['AssetID'])]

    # Changed assets
    merged = old_df.merge(new_df, on='AssetID', suffixes=('_old', '_new'))
    changed = merged[merged['Status_old'] != merged['Status_new']]

    return {
        'new': new_assets,
        'removed': removed_assets,
        'changed': changed
    }

if __name__ == "__main__":
    result = compare_assets("assets_old.csv", "assets_new.csv")
    print(f"New: {len(result['new'])} items")
    print(f"Removed: {len(result['removed'])} items")
    print(f"Changed: {len(result['changed'])} items")
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Asset Classification | Asset inventory + classification criteria | Highest |
| Asset Management | Administrator designation + currency | High |
| Risk Management | Annual risk assessment | Highest |
| Audit | Annual audit + result reporting | High |

---

*Next Chapter: Chapter 15. Human Resource Security and External Party Security*
