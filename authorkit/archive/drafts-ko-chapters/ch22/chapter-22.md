# 22장. 자동화 도구 구축

> Part IV. 실무 적용

---

## 개요

취약점 점검을 자동화하면 효율성이 크게 향상됩니다. 이 장에서는 점검 스크립트 아키텍처, 결과 수집 및 리포팅, CI/CD 파이프라인 연동 방법을 다룹니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                   KESE-KIT 자동화 아키텍처                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     점검 대상 시스템                     │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │
│  │  │ Unix/   │  │ Windows │  │ Network │  │ Database│   │    │
│  │  │ Linux   │  │ Server  │  │ Device  │  │  (DBMS) │   │    │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │    │
│  └───────┼────────────┼────────────┼────────────┼────────┘    │
│          │            │            │            │              │
│          └────────────┴────────────┴────────────┘              │
│                            │                                    │
│                            ▼ 점검 스크립트 실행                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     점검 엔진 (Scripts)                   │    │
│  │  ┌───────────────┐  ┌────────────────┐                  │    │
│  │  │ 항목 정의     │  │ 대상 정의       │                  │    │
│  │  │ (items.yaml) │  │ (targets.yaml) │                  │    │
│  │  └───────────────┘  └────────────────┘                  │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                    │
│                            ▼ JSON 결과 전송                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     수집 서버 (Collector)                 │    │
│  │              REST API (Flask/FastAPI)                    │    │
│  │  ┌───────────────────────────────────────────────────┐  │    │
│  │  │  /api/v1/results  │  /api/v1/summary             │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  └─────────────────────────┬───────────────────────────────┘    │
│                            │                                    │
│           ┌────────────────┼────────────────┐                   │
│           ▼                ▼                ▼                   │
│    ┌───────────┐    ┌───────────┐    ┌───────────┐             │
│    │ 리포팅    │    │   웹      │    │  CI/CD    │             │
│    │ (HTML/PDF)│    │ 대시보드  │    │  연동     │             │
│    └───────────┘    └───────────┘    └───────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 22-1. 점검 스크립트 아키텍처

### 전체 구조

```
KESE-KIT/
├── scripts/
│   ├── unix/           # Unix/Linux 점검 스크립트
│   │   ├── account.sh  # 계정 관리
│   │   ├── file.sh     # 파일/디렉터리
│   │   ├── service.sh  # 서비스 관리
│   │   └── run_all.sh  # 전체 실행
│   ├── windows/        # Windows 점검 스크립트
│   │   ├── account.ps1
│   │   ├── service.ps1
│   │   └── run_all.ps1
│   ├── network/        # 네트워크 장비 점검
│   └── database/       # 데이터베이스 점검
├── collector/          # 결과 수집 모듈
│   ├── agent.py        # 에이전트
│   └── server.py       # 수집 서버
├── reporter/           # 리포팅 모듈
│   ├── templates/      # 보고서 템플릿
│   └── generator.py    # 보고서 생성기
├── config/             # 설정 파일
│   ├── items.yaml      # 점검 항목 정의
│   └── targets.yaml    # 점검 대상 정의
└── web/                # 웹 대시보드
    └── dashboard/
```

### 점검 항목 정의 (YAML)

```yaml
# config/items.yaml
unix:
  - id: U-01
    name: root 계정 원격접속 제한
    category: 계정관리
    severity: 상
    check:
      type: grep
      target: /etc/ssh/sshd_config
      pattern: "^PermitRootLogin"
      expected: "no"
    remediation: "sshd_config에서 PermitRootLogin no 설정"

  - id: U-02
    name: 패스워드 복잡성 설정
    category: 계정관리
    severity: 상
    check:
      type: file_exists
      target: /etc/security/pwquality.conf
    remediation: "pwquality.conf 파일 설정"

windows:
  - id: W-01
    name: Administrator 계정 이름 변경
    category: 계정관리
    severity: 상
    check:
      type: powershell
      script: "(Get-LocalUser | Where-Object {$_.SID -like '*-500'}).Name"
      expected_not: "Administrator"
    remediation: "Administrator 계정명을 다른 이름으로 변경"
```

### 점검 대상 정의 (YAML)

```yaml
# config/targets.yaml
groups:
  - name: 웹서버
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

  - name: DB서버
    targets:
      - hostname: db01
        ip: 192.168.1.20
        os: linux
        db_type: mysql
```

---

## 22-2. 통합 점검 스크립트

### Unix/Linux 통합 스크립트

```bash
#!/bin/bash
#===============================================
# KESE KIT - Unix/Linux 통합 점검 스크립트
# Version: 1.0
#===============================================

# 설정
REPORT_DIR="/var/log/kese_kit"
REPORT_FILE="$REPORT_DIR/$(hostname)_$(date +%Y%m%d).json"
RESULT=()

# 로그 디렉터리 생성
mkdir -p "$REPORT_DIR"

# 점검 함수
check_item() {
    local id="$1"
    local name="$2"
    local result="$3"  # GOOD, VULN, N/A
    local detail="$4"

    RESULT+=("{\"id\":\"$id\",\"name\":\"$name\",\"result\":\"$result\",\"detail\":\"$detail\"}")

    if [ "$result" == "GOOD" ]; then
        echo -e "[\e[32m양호\e[0m] $id: $name"
    elif [ "$result" == "VULN" ]; then
        echo -e "[\e[31m취약\e[0m] $id: $name - $detail"
    else
        echo -e "[\e[33mN/A\e[0m] $id: $name"
    fi
}

# U-01: root 원격접속 제한
check_u01() {
    local id="U-01"
    local name="root 계정 원격접속 제한"

    if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config 2>/dev/null; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "PermitRootLogin이 no가 아님"
    fi
}

# U-02: 패스워드 복잡성
check_u02() {
    local id="U-02"
    local name="패스워드 복잡성 설정"

    if [ -f /etc/security/pwquality.conf ]; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "pwquality.conf 미존재"
    fi
}

# U-04: 패스워드 파일 보호
check_u04() {
    local id="U-04"
    local name="패스워드 파일 보호"

    if [ ! -r /etc/shadow ] || [ "$(stat -c %a /etc/shadow)" -le "400" ]; then
        check_item "$id" "$name" "GOOD" ""
    else
        check_item "$id" "$name" "VULN" "/etc/shadow 권한 과다"
    fi
}

# 메인 실행
echo "============================================="
echo "KESE KIT - Unix/Linux 취약점 점검"
echo "Host: $(hostname)"
echo "Date: $(date)"
echo "============================================="

check_u01
check_u02
check_u04
# ... 추가 점검 항목

# JSON 결과 저장
echo "[" > "$REPORT_FILE"
echo "${RESULT[*]}" | sed 's/} {/},\n{/g' >> "$REPORT_FILE"
echo "]" >> "$REPORT_FILE"

echo ""
echo "결과 저장: $REPORT_FILE"
```

### Windows 통합 스크립트

```powershell
#===============================================
# KESE KIT - Windows 통합 점검 스크립트
# Version: 1.0
#===============================================

param(
    [string]$ReportPath = "C:\KESE_KIT\Reports"
)

# 설정
$ReportFile = Join-Path $ReportPath "$($env:COMPUTERNAME)_$(Get-Date -Format 'yyyyMMdd').json"
$Results = @()

# 디렉터리 생성
New-Item -ItemType Directory -Path $ReportPath -Force | Out-Null

# 점검 함수
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

# W-01: Administrator 계정명 변경
function Test-W01 {
    $id = "W-01"
    $name = "Administrator 계정 이름 변경"

    $admin = Get-LocalUser | Where-Object { $_.SID -like "*-500" }
    if ($admin.Name -ne "Administrator") {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        Test-Item -Id $id -Name $name -Result "VULN" -Detail "기본 계정명 사용 중"
    }
}

# W-02: Guest 계정 비활성화
function Test-W02 {
    $id = "W-02"
    $name = "Guest 계정 비활성화"

    $guest = Get-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
    if (-not $guest.Enabled) {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        Test-Item -Id $id -Name $name -Result "VULN" -Detail "Guest 계정 활성화됨"
    }
}

# W-03: 패스워드 복잡성
function Test-W03 {
    $id = "W-03"
    $name = "패스워드 복잡성 설정"

    $policy = Get-Content C:\Windows\System32\GroupPolicy\Machine\Microsoft\Windows NT\SecEdit\GptTmpl.inf -ErrorAction SilentlyContinue
    if ($policy -match "PasswordComplexity\s*=\s*1") {
        Test-Item -Id $id -Name $name -Result "GOOD"
    } else {
        # secedit로 확인
        secedit /export /cfg "$env:TEMP\secpol.cfg" | Out-Null
        $cfg = Get-Content "$env:TEMP\secpol.cfg"
        if ($cfg -match "PasswordComplexity\s*=\s*1") {
            Test-Item -Id $id -Name $name -Result "GOOD"
        } else {
            Test-Item -Id $id -Name $name -Result "VULN" -Detail "복잡성 미설정"
        }
    }
}

# 메인 실행
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "KESE KIT - Windows 취약점 점검" -ForegroundColor Cyan
Write-Host "Host: $($env:COMPUTERNAME)"
Write-Host "Date: $(Get-Date)"
Write-Host "=============================================" -ForegroundColor Cyan

Test-W01
Test-W02
Test-W03
# ... 추가 점검 항목

# JSON 결과 저장
$Results | ConvertTo-Json | Out-File $ReportFile -Encoding UTF8

Write-Host ""
Write-Host "결과 저장: $ReportFile" -ForegroundColor Green
```

---

## 22-3. 결과 수집 및 리포팅

### 결과 수집 서버 (Python)

```python
"""
KESE KIT - 결과 수집 서버
Flask 기반 REST API
"""
from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
RESULT_DIR = "./results"

@app.route('/api/v1/results', methods=['POST'])
def receive_result():
    """점검 결과 수신"""
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
    """점검 결과 목록 조회"""
    files = os.listdir(RESULT_DIR) if os.path.exists(RESULT_DIR) else []
    return jsonify({'results': files})

@app.route('/api/v1/results/<filename>', methods=['GET'])
def get_result(filename):
    """특정 점검 결과 조회"""
    filepath = os.path.join(RESULT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/v1/summary', methods=['GET'])
def get_summary():
    """전체 현황 요약"""
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

### 보고서 생성기 (Python)

```python
"""
KESE KIT - 보고서 생성기
취약점 점검 결과를 HTML/PDF 보고서로 생성
"""
from jinja2 import Template
import json
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>취약점 점검 보고서</title>
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; margin: 40px; }
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
    <h1>주요정보통신기반시설 취약점 점검 보고서</h1>

    <div class="summary">
        <h2>점검 개요</h2>
        <p>점검 일시: {{ date }}</p>
        <p>점검 대상: {{ hostname }}</p>
        <p>총 점검 항목: {{ total }}개</p>
        <p>양호: <span class="good">{{ good }}개</span> /
           취약: <span class="vuln">{{ vuln }}개</span></p>
        <p>준수율: {{ compliance_rate }}%</p>
    </div>

    <h2>점검 결과 상세</h2>
    <table>
        <tr>
            <th>ID</th>
            <th>점검 항목</th>
            <th>결과</th>
            <th>세부 내용</th>
        </tr>
        {% for item in results %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td class="{{ 'good' if item.result == 'GOOD' else 'vuln' }}">
                {{ '양호' if item.result == 'GOOD' else '취약' }}
            </td>
            <td>{{ item.detail }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def generate_report(result_file, output_file):
    """점검 결과로부터 HTML 보고서 생성"""
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

    print(f"보고서 생성: {output_file}")

if __name__ == '__main__':
    generate_report('result.json', 'report.html')
```

---

## 22-4. CI/CD 파이프라인 연동

```
┌─────────────────────────────────────────────────────────────────┐
│                   CI/CD 보안 점검 파이프라인                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────┐                                                 │
│    │  코드    │                                                 │
│    │  Push    │                                                 │
│    └────┬─────┘                                                 │
│         │                                                        │
│         ▼                                                        │
│    ╔══════════════════════════════════════════════════════╗     │
│    ║              CI/CD Pipeline (자동 실행)               ║     │
│    ╠══════════════════════════════════════════════════════╣     │
│    ║                                                      ║     │
│    ║  ┌─────────┐  ┌─────────┐  ┌─────────┐             ║     │
│    ║  │  SAST   │  │의존성   │  │KESE-KIT │             ║     │
│    ║  │(Bandit) │  │검사     │  │ 점검    │             ║     │
│    ║  │         │  │(Safety) │  │         │             ║     │
│    ║  └────┬────┘  └────┬────┘  └────┬────┘             ║     │
│    ║       │            │            │                   ║     │
│    ║       └────────────┴────────────┘                   ║     │
│    ║                    │                                 ║     │
│    ║                    ▼                                 ║     │
│    ║            ┌───────────────┐                        ║     │
│    ║            │  보고서 생성   │                        ║     │
│    ║            │ (HTML/JSON)  │                        ║     │
│    ║            └───────┬───────┘                        ║     │
│    ║                    │                                 ║     │
│    ╚════════════════════╪════════════════════════════════╝     │
│                         │                                        │
│         ┌───────────────┼───────────────┐                       │
│         ▼               ▼               ▼                       │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐                   │
│    │ 아티팩트 │    │  알림   │    │ 리포트  │                   │
│    │  저장   │    │ (이메일) │    │ 게시    │                   │
│    └─────────┘    └─────────┘    └─────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### GitHub Actions 연동

```yaml
# .github/workflows/security-check.yml
name: Security Vulnerability Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # 매주 월요일

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

### Jenkins 파이프라인

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
                subject: "보안 점검 실패: ${env.JOB_NAME}",
                body: "점검 결과를 확인하세요: ${env.BUILD_URL}",
                to: 'security@company.com'
            )
        }
    }
}
```

---

## 요약

| 항목 | 핵심 내용 |
|------|----------|
| 아키텍처 | 모듈화된 스크립트 구조 |
| 점검 정의 | YAML 기반 항목/대상 정의 |
| 결과 수집 | REST API 기반 수집 서버 |
| 리포팅 | HTML/PDF 자동 생성 |
| CI/CD | GitHub Actions, Jenkins 연동 |

---

## Part IV 완료

Part IV (실무 적용)에서 다룬 내용:

- 20장: 정부과제 환경 적용
- 21장: 공공조달시장 대응
- 22장: 자동화 도구 구축

---

*다음: 부록*
