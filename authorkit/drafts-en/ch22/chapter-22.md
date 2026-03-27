# Chapter 22. Automation Tool Development

> Part IV. Practical Application

---

## Overview

Automating vulnerability assessments significantly improves efficiency. This chapter covers assessment script architecture, result collection and reporting, and CI/CD pipeline integration.

```
┌─────────────────────────────────────────────────────────────────┐
│                  KESE-KIT Automation Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Target Systems                        │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │
│  │  │ Unix/   │  │ Windows │  │ Network │  │ Database│   │    │
│  │  │ Linux   │  │ Server  │  │ Device  │  │  (DBMS) │   │    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │    │
│  └───────┼────────────┼────────────┼────────────┼────────┘    │
│          │            │            │            │              │
│          └────────────┴────────────┴────────────┘              │
│                            │                                    │
│                            ▼ Execute assessment scripts         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Assessment Engine (Scripts)             │    │
│  │  ┌───────────────┐  ┌────────────────┐                  │    │
│  │  │ Item Defs     │  │ Target Defs    │                  │    │
│  │  │ (items.yaml)  │  │ (targets.yaml) │                  │    │
│  │  └───────────────┘  └────────────────┘                  │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                    │
│                            ▼ JSON results transmission          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                  Collector Server                        │    │
│  │              REST API (Flask/FastAPI)                    │    │
│  │  ┌───────────────────────────────────────────────────┐  │    │
│  │  │  /api/v1/results  │  /api/v1/summary             │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                    │
│           ┌────────────────┼────────────────┐                   │
│           ▼                ▼                ▼                   │
│    ┌───────────┐    ┌───────────┐    ┌───────────┐             │
│    │ Reporting │    │   Web     │    │  CI/CD    │             │
│    │ (HTML/PDF)│    │ Dashboard │    │Integration│             │
│    └───────────┘    └───────────┘    └───────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 22-1. Assessment Script Architecture

### Overall Structure

```
KESE-KIT/
├── scripts/
│   ├── unix/           # Unix/Linux assessment scripts
│   │   ├── account.sh  # Account management
│   │   ├── file.sh     # File/directory
│   │   ├── service.sh  # Service management
│   │   └── run_all.sh  # Execute all
│   ├── windows/        # Windows assessment scripts
│   │   ├── account.ps1
│   │   ├── service.ps1
│   │   └── run_all.ps1
│   ├── network/        # Network device assessment
│   └── database/       # Database assessment
├── collector/          # Result collection module
│   ├── agent.py        # Agent
│   └── server.py       # Collection server
├── reporter/           # Reporting module
│   ├── templates/      # Report templates
│   └── generator.py    # Report generator
├── config/             # Configuration files
│   ├── items.yaml      # Assessment item definitions
│   └── targets.yaml    # Assessment target definitions
└── web/                # Web dashboard
    └── dashboard/
```

### Assessment Item Definition (YAML)

```yaml
# config/items.yaml
unix:
  - id: U-01
    name: Restrict root remote login
    category: Account Management
    severity: High
    check:
      type: grep
      target: /etc/ssh/sshd_config
      pattern: "^PermitRootLogin"
      expected: "no"
    remediation: "Set PermitRootLogin no in sshd_config"

  - id: U-02
    name: Password complexity settings
    category: Account Management
    severity: High
    check:
      type: file_exists
      target: /etc/security/pwquality.conf
    remediation: "Configure pwquality.conf file"

windows:
  - id: W-01
    name: Rename Administrator account
    category: Account Management
    severity: High
    check:
      type: powershell
      script: "(Get-LocalUser | Where-Object {$_.SID -like '*-500'}).Name"
      expected_not: "Administrator"
    remediation: "Rename Administrator account to different name"
```

### Assessment Target Definition (YAML)

```yaml
# config/targets.yaml
groups:
  - name: Web Servers
    targets:
      - hostname: web01
        ip: 192.168.1.10
        os: linux
        credentials:
          type: ssh_key
          user: admin
          key_file: ~/.ssh/id_rsa
      - hostname: web02
        ip: 192.168.1.11
        os: linux

  - name: DB Servers
    targets:
      - hostname: db01
        ip: 192.168.1.20
        os: linux
        db_type: mysql
```

---

## 22-2. Integrated Assessment Scripts

### Unix/Linux Integrated Script

```bash
#!/bin/bash
#===============================================
# KESE KIT - Unix/Linux Integrated Assessment Script
# Version: 1.0
#===============================================

# Configuration
REPORT_DIR="/var/log/kese_kit"
REPORT_FILE="$REPORT_DIR/$(hostname)_$(date +%Y%m%d).json"
RESULT=()

# Create log directory
mkdir -p "$REPORT_DIR"

# Assessment function
check_item() {
    local id="$1"
    local name="$2"
    local result="$3"  # GOOD, VULN, N/A
    local detail="$4"

    RESULT+=("{\"id\":\"$id\",\"name\":\"$name\",\"result\":\"$result\",\"detail\":\"$detail\"}")

    if [ "$result" == "GOOD" ]; then
        echo -e "[\e[32mGOOD\e[0m] $id: $name"
    elif [ "$result" == "VULN" ]; then
        echo -e "[\e[31mVULN\e[0m] $id: $name - $detail"
    else
        echo -e "[\e[33mN/A\e[0m] $id: $name"
    fi
}

# U-01: Restrict root remote login
check_u01() {
    local id="U-01"
    local name="Restrict root remote login"

    if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config 2>/dev/null; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "PermitRootLogin is not set to no"
    fi
}

# U-02: Password complexity
check_u02() {
    local id="U-02"
    local name="Password complexity settings"

    if [ -f /etc/security/pwquality.conf ]; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "pwquality.conf does not exist"
    fi
}

# U-04: Password file protection
check_u04() {
    local id="U-04"
    local name="Password file protection"

    if [ ! -r /etc/shadow ] || [ "$(stat -c %a /etc/shadow)" -le "400" ]; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "/etc/shadow has excessive permissions"
    fi
}

# Main execution
echo "============================================="
echo "KESE KIT - Unix/Linux Vulnerability Assessment"
echo "Host: $(hostname)"
echo "Date: $(date)"
echo "============================================="

check_u01
check_u02
check_u04
# ... additional assessment items

# Save JSON results
echo "[" > "$REPORT_FILE"
echo "${RESULT[*]}" | sed 's/} {/},\n{/g' >> "$REPORT_FILE"
echo "]" >> "$REPORT_FILE"

echo ""
echo "Results saved: $REPORT_FILE"
```

### Windows Integrated Script

```powershell
#===============================================
# KESE KIT - Windows Integrated Assessment Script
# Version: 1.0
#===============================================

param(
    [string]$ReportPath = "C:\KESE_KIT\Reports"
)

# Configuration
$ReportFile = Join-Path $ReportPath "$($env:COMPUTERNAME)_$(Get-Date -Format 'yyyyMMdd').json"
$Results = @()

# Create directory
New-Item -ItemType Directory -Path $ReportPath -Force | Out-Null

# Assessment function
function Test-Item {
    param(
        [string]$Id,
        [string]$Name,
        [string]$Result,
        [string]$Detail = ""
    )

    $script:Results += @{
        id = $Id
        name = $Name
        result = $Result
        detail = $Detail
    }

    $color = switch ($Result) {
        "GOOD" { "Green" }
        "VULN" { "Red" }
        default { "Yellow" }
    }

    Write-Host "[$Result] $Id`: $Name" -ForegroundColor $color
    if ($Detail) { Write-Host "  -> $Detail" -ForegroundColor Gray }
}

# W-01: Administrator account rename
function Test-W01 {
    $id = "W-01"
    $name = "Rename Administrator account"

    $admin = Get-LocalUser | Where-Object { $_.SID -like "*-500" }
    if ($admin.Name -ne "Administrator") {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        Test-Item -Id $id -Name $name -Result "VULN" -Detail "Using default account name"
    }
}

# W-02: Guest account disabled
function Test-W02 {
    $id = "W-02"
    $name = "Disable Guest account"

    $guest = Get-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
    if (-not $guest.Enabled) {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        Test-Item -Id $id -Name $name -Result "VULN" -Detail "Guest account is enabled"
    }
}

# W-03: Password complexity
function Test-W03 {
    $id = "W-03"
    $name = "Password complexity settings"

    $policy = Get-Content C:\Windows\System32\GroupPolicy\Machine\Microsoft\Windows` NT\SecEdit\GptTmpl.inf -ErrorAction SilentlyContinue
    if ($policy -match "PasswordComplexity\s*=\s*1") {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        # Check with secedit
        secedit /export /cfg "$env:TEMP\secpol.cfg" | Out-Null
        $cfg = Get-Content "$env:TEMP\secpol.cfg"
        if ($cfg -match "PasswordComplexity\s*=\s*1") {
            Test-Item -Id $id -Name $name -Result "GOOD"
        } else {
            Test-Item -Id $id -Name $name -Result "VULN" -Detail "Complexity not configured"
        }
    }
}

# Main execution
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "KESE KIT - Windows Vulnerability Assessment" -ForegroundColor Cyan
Write-Host "Host: $($env:COMPUTERNAME)"
Write-Host "Date: $(Get-Date)"
Write-Host "=============================================" -ForegroundColor Cyan

Test-W01
Test-W02
Test-W03
# ... additional assessment items

# Save JSON results
$Results | ConvertTo-Json | Out-File $ReportFile -Encoding UTF8

Write-Host ""
Write-Host "Results saved: $ReportFile" -ForegroundColor Green
```

---

## 22-3. Result Collection and Reporting

### Result Collection Server (Python)

```python
"""
KESE KIT - Result Collection Server
Flask-based REST API
"""
from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
RESULT_DIR = "./results"

@app.route('/api/v1/results', methods=['POST'])
def receive_result():
    """Receive assessment results"""
    data = request.json

    hostname = data.get('hostname', 'unknown')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{hostname}_{timestamp}.json"

    os.makedirs(RESULT_DIR, exist_ok=True)
    with open(os.path.join(RESULT_DIR, filename), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return jsonify({'status': 'success', 'filename': filename})

@app.route('/api/v1/results', methods=['GET'])
def get_results():
    """Get assessment result list"""
    files = os.listdir(RESULT_DIR) if os.path.exists(RESULT_DIR) else []
    return jsonify({'results': files})

@app.route('/api/v1/results/<filename>', methods=['GET'])
def get_result(filename):
    """Get specific assessment result"""
    filepath = os.path.join(RESULT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/v1/summary', methods=['GET'])
def get_summary():
    """Get overall status summary"""
    if not os.path.exists(RESULT_DIR):
        return jsonify({'total': 0, 'good': 0, 'vuln': 0})

    total, good, vuln = 0, 0, 0
    for filename in os.listdir(RESULT_DIR):
        with open(os.path.join(RESULT_DIR, filename), 'r') as f:
            data = json.load(f)
            for item in data.get('results', []):
                total += 1
                if item.get('result') == 'GOOD':
                    good += 1
                elif item.get('result') == 'VULN':
                    vuln += 1

    return jsonify({
        'total': total,
        'good': good,
        'vuln': vuln,
        'compliance_rate': round(good / total * 100, 1) if total > 0 else 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Report Generator (Python)

```python
"""
KESE KIT - Report Generator
Generate HTML/PDF reports from vulnerability assessment results
"""
from jinja2 import Template
import json
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Vulnerability Assessment Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; border-bottom: 2px solid #333; }
        .summary { background: #f5f5f5; padding: 20px; margin: 20px 0; }
        .good { color: green; }
        .vuln { color: red; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #333; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
    </style>
</head>
<body>
    <h1>Critical Information Infrastructure Vulnerability Assessment Report</h1>

    <div class="summary">
        <h2>Assessment Overview</h2>
        <p>Assessment Date: {{ date }}</p>
        <p>Target: {{ hostname }}</p>
        <p>Total Items: {{ total }}</p>
        <p>Good: <span class="good">{{ good }}</span> /
           Vulnerable: <span class="vuln">{{ vuln }}</span></p>
        <p>Compliance Rate: {{ compliance_rate }}%</p>
    </div>

    <h2>Detailed Results</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>Assessment Item</th>
            <th>Result</th>
            <th>Details</th>
        </tr>
        {% for item in results %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td class="{{ 'good' if item.result == 'GOOD' else 'vuln' }}">
                {{ 'Good' if item.result == 'GOOD' else 'Vulnerable' }}
            </td>
            <td>{{ item.detail }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def generate_report(result_file, output_file):
    """Generate HTML report from assessment results"""
    with open(result_file, 'r') as f:
        data = json.load(f)

    results = data.get('results', [])
    good = sum(1 for r in results if r.get('result') == 'GOOD')
    vuln = sum(1 for r in results if r.get('result') == 'VULN')
    total = len(results)

    template = Template(HTML_TEMPLATE)
    html = template.render(
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        hostname=data.get('hostname', 'Unknown'),
        total=total,
        good=good,
        vuln=vuln,
        compliance_rate=round(good / total * 100, 1) if total > 0 else 0,
        results=results
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Report generated: {output_file}")

if __name__ == '__main__':
    generate_report('result.json', 'report.html')
```

---

## 22-4. CI/CD Pipeline Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                CI/CD Security Assessment Pipeline                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────┐                                                 │
│    │  Code    │                                                 │
│    │  Push    │                                                 │
│    └────┬─────┘                                                 │
│         │                                                        │
│         ▼                                                        │
│    ╔══════════════════════════════════════════════════════╗     │
│    ║            CI/CD Pipeline (Automated)                ║     │
│    ╠══════════════════════════════════════════════════════╣     │
│    ║                                                      ║     │
│    ║  ┌─────────┐  ┌─────────┐  ┌─────────┐             ║     │
│    ║  │  SAST   │  │ Depend- │  │KESE-KIT │             ║     │
│    ║  │(Bandit) │  │  ency   │  │ Check   │             ║     │
│    ║  │         │  │(Safety) │  │         │             ║     │
│    ║  └────┬────┘  └────┬────┘  └────┬────┘             ║     │
│    ║       │            │            │                   ║     │
│    ║       └────────────┴────────────┘                   ║     │
│    ║                    │                                 ║     │
│    ║                    ▼                                 ║     │
│    ║            ┌───────────────┐                        ║     │
│    ║            │ Report Gen.   │                        ║     │
│    ║            │ (HTML/JSON)   │                        ║     │
│    ║            └───────┬───────┘                        ║     │
│    ║                    │                                 ║     │
│    ╚════════════════════╪════════════════════════════════╝     │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐                   │
│    │ Artifact│    │  Alert  │    │ Report  │                   │
│    │ Storage │    │ (Email) │    │ Publish │                   │
│    └─────────┘    └─────────┘    └─────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### GitHub Actions Integration

```yaml
# .github/workflows/security-check.yml
name: Security Vulnerability Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Every Monday

jobs:
  security-check:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install bandit safety

    - name: Run SAST (Bandit)
      run: |
        bandit -r . -f json -o bandit-report.json || true

    - name: Run dependency check (Safety)
      run: |
        safety check --json > safety-report.json || true

    - name: Run KESE-KIT checks
      run: |
        ./scripts/unix/run_all.sh

    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json
          /var/log/kese_kit/*.json

    - name: Check for critical vulnerabilities
      run: |
        python scripts/check_critical.py
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Security Scan') {
            parallel {
                stage('SAST') {
                    steps {
                        sh 'bandit -r . -f json -o bandit-report.json || true'
                    }
                }

                stage('Dependency Check') {
                    steps {
                        sh 'safety check --json > safety-report.json || true'
                    }
                }

                stage('KESE-KIT') {
                    steps {
                        sh './scripts/unix/run_all.sh'
                    }
                }
            }
        }

        stage('Generate Report') {
            steps {
                sh 'python reporter/generator.py'
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: '*.json,*.html', fingerprint: true
            }
        }
    }

    post {
        always {
            publishHTML([
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Security Report'
            ])
        }
        failure {
            emailext(
                subject: "Security Check Failed: ${env.JOB_NAME}",
                body: "Check the results: ${env.BUILD_URL}",
                to: 'security@company.com'
            )
        }
    }
}
```

---

## Summary

| Item | Key Content |
|------|-------------|
| Architecture | Modular script structure |
| Item Definition | YAML-based item/target definitions |
| Result Collection | REST API-based collection server |
| Reporting | Automated HTML/PDF generation |
| CI/CD | GitHub Actions, Jenkins integration |

---

## Part IV Complete

Content covered in Part IV (Practical Application):

- Chapter 20: Government Project Environment Application
- Chapter 21: Public Procurement Market Response
- Chapter 22: Automation Tool Development

---

*Next: Appendix*
