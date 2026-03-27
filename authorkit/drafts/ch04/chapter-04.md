# 4장. Windows 서버 점검

> Part II. 기술적 취약점 점검

---

## 개요

Windows 서버는 기업 환경에서 Active Directory, 파일 서버, 웹 서버 등 다양한 역할로 활용됩니다. 이 장에서는 73개의 점검 항목(W-01 ~ W-73)을 5개 영역으로 나누어 설명합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│               Windows 서버 취약점 점검 영역 (73개)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      보안 관리 (W-48~W-73, 26개)             │ │
│  │   방화벽 | 백신 | 화면보호기 | 레지스트리 | 권한 설정        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▲                                   │
│        ┌─────────────────────┼─────────────────────┐            │
│        │                     │                     │            │
│  ┌─────┴─────┐        ┌─────┴─────┐        ┌─────┴─────┐       │
│  │  계정 관리 │        │ 서비스 관리│        │  로그 관리 │       │
│  │ W-01~W-14 │        │ W-15~W-39 │        │ W-42~W-47 │       │
│  │  (14개)   │        │  (25개)   │        │  (6개)    │       │
│  │           │        │           │        │           │       │
│  │• Admin   │        │• 불필요   │        │• 감사정책 │       │
│  │  이름변경 │        │  서비스   │        │• 로그크기 │       │
│  │• Guest   │        │• IIS 점검 │        │• 이벤트   │       │
│  │  비활성화 │        │• 공유폴더 │        │  로그     │       │
│  │• 잠금정책│        │           │        │           │       │
│  └───────────┘        └───────────┘        └───────────┘       │
│                              │                                   │
│                       ┌─────┴─────┐                             │
│                       │  패치 관리 │                             │
│                       │ W-40~W-41 │                             │
│                       │  (2개)    │                             │
│                       │           │                             │
│                       │• 서비스팩 │                             │
│                       │• 보안패치 │                             │
│                       └───────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 영역 | 항목 | 항목 수 |
|------|------|:------:|
| 계정 관리 | W-01 ~ W-14 | 14 |
| 서비스 관리 | W-15 ~ W-39 | 25 |
| 패치 관리 | W-40 ~ W-41 | 2 |
| 로그 관리 | W-42 ~ W-47 | 6 |
| 보안 관리 | W-48 ~ W-73 | 26 |

---

## 4-1. 계정 관리 (W-01 ~ W-14)

### W-01. Administrator 계정 이름 변경

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 기본 관리자 계정명 노출로 인한 공격 방지 |
| **판단 기준** | 양호: 이름 변경됨 / 취약: 기본값 사용 |

#### 점검 방법 (PowerShell)

```powershell
# Administrator 계정 확인
Get-LocalUser | Where-Object {$_.SID -like "*-500"}

# 또는 명령 프롬프트
net user administrator
```

#### 조치 방법

```powershell
# PowerShell로 계정 이름 변경
Rename-LocalUser -Name "Administrator" -NewName "새로운관리자명"

# 또는 로컬 보안 정책
# secpol.msc > 로컬 정책 > 보안 옵션 > 계정: Administrator 계정 이름 바꾸기
```

> **TIP**
> 계정 이름은 예측하기 어려운 이름으로 변경하되, 관리 편의를 위해 문서화하세요.

---

### W-02. Guest 계정 비활성화

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 익명 접근 차단 |
| **판단 기준** | 양호: 비활성화 / 취약: 활성화 |

#### 점검 방법

```powershell
# Guest 계정 상태 확인
Get-LocalUser -Name "Guest" | Select-Object Name, Enabled
```

#### 조치 방법

```powershell
# Guest 계정 비활성화
Disable-LocalUser -Name "Guest"
```

---

### W-03. 불필요한 계정 제거

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 미사용 계정을 통한 비인가 접근 방지 |

#### 점검 방법

```powershell
# 모든 로컬 계정 확인
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# 90일 이상 미접속 계정 확인
$threshold = (Get-Date).AddDays(-90)
Get-LocalUser | Where-Object {$_.LastLogon -lt $threshold}
```

---

### W-04. 비밀번호 정책 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 강력한 비밀번호 사용 강제 |

#### 점검 방법

```powershell
# 비밀번호 정책 확인
net accounts

# 또는 PowerShell
Get-ADDefaultDomainPasswordPolicy  # 도메인 환경
```

#### 권장 설정값

| 정책 | 권장값 |
|------|:------:|
| 최소 비밀번호 길이 | 8자 이상 |
| 비밀번호 복잡성 | 사용 |
| 최대 비밀번호 사용 기간 | 90일 |
| 최소 비밀번호 사용 기간 | 1일 |
| 비밀번호 기억 | 12개 |

#### 조치 방법

```powershell
# 로컬 보안 정책 (secpol.msc) 또는 그룹 정책(gpedit.msc)에서 설정
# 컴퓨터 구성 > Windows 설정 > 보안 설정 > 계정 정책 > 암호 정책
```

---

### W-05. 계정 잠금 정책 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 무차별 대입 공격 방지 |

#### 점검 방법

```powershell
# 계정 잠금 정책 확인
net accounts
```

#### 권장 설정값

| 정책 | 권장값 |
|------|:------:|
| 계정 잠금 임계값 | 5회 |
| 계정 잠금 기간 | 30분 |
| 다음 시간 후 계정 잠금 수를 원래대로 설정 | 30분 |

---

### W-06 ~ W-14. 기타 계정 관리 항목

| 코드 | 항목 | 중요도 | 핵심 점검 |
|------|------|:------:|----------|
| W-06 | 관리자 그룹에 최소한의 사용자 포함 | 상 | Administrators 그룹 구성원 |
| W-07 | 로컬 계정 관리 | 중 | 불필요 로컬 계정 |
| W-08 | 비밀번호 저장을 위한 해독 가능한 암호화 사용 안 함 | 중 | 정책 설정 |
| W-09 | 로컬 계정의 원격 접속 제한 | 중 | UAC 원격 제한 |
| W-10 | 세션 타임아웃 설정 | 하 | 화면 잠금 |
| W-11 | 마지막 로그온 사용자 이름 표시 안 함 | 하 | 로그온 화면 |
| W-12 | 로그온 시 경고 메시지 표시 | 하 | 법적 고지 |
| W-13 | SAM 계정과 공유의 익명 열거 허용 안 함 | 상 | 익명 열거 차단 |
| W-14 | 원격 레지스트리 서비스 비활성화 | 상 | 원격 레지스트리 |

---

## 4-2. 서비스 관리 (W-15 ~ W-39)

### W-15. 불필요한 서비스 비활성화

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 공격 표면 최소화 |

#### 비활성화 권장 서비스

| 서비스 | 설명 | 비활성화 권장 |
|--------|------|:------------:|
| Telnet | 원격 접속 (평문) | O |
| TFTP | 파일 전송 (비인증) | O |
| FTP Publishing | FTP 서버 | 검토 |
| Remote Registry | 원격 레지스트리 | O |
| Simple TCP/IP Services | Echo, Daytime 등 | O |

#### 점검 방법

```powershell
# 실행 중인 서비스 확인
Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, DisplayName

# 특정 서비스 상태 확인
Get-Service -Name "RemoteRegistry" | Select-Object Name, Status, StartType
```

#### 조치 방법

```powershell
# 서비스 중지 및 비활성화
Stop-Service -Name "RemoteRegistry"
Set-Service -Name "RemoteRegistry" -StartupType Disabled
```

---

### W-20. IIS 서비스 구동 점검

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 불필요한 웹 서버 비활성화 |

#### 점검 방법

```powershell
# IIS 설치 여부 확인
Get-WindowsFeature -Name Web-Server

# IIS 서비스 상태
Get-Service -Name "W3SVC"
```

---

### W-25. 공유 폴더 점검

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 불필요한 공유 제거, 권한 점검 |

#### 점검 방법

```powershell
# 공유 폴더 목록
Get-SmbShare

# 관리 공유 확인
Get-SmbShare | Where-Object {$_.Name -match '\$$'}

# 공유 권한 확인
Get-SmbShareAccess -Name "공유명"
```

> **WARNING**
> 관리 공유(C$, ADMIN$ 등)는 관리 목적으로 기본 생성됩니다. 불필요 시 제거하되, 영향도를 검토하세요.

---

## 4-3. 패치 관리 (W-40 ~ W-41)

### W-40. 최신 서비스팩 적용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 알려진 취약점 패치 적용 |

#### 점검 방법

```powershell
# OS 버전 및 빌드 확인
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber

# 설치된 핫픽스 확인
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

---

### W-41. 최신 보안 패치 적용

#### 점검 방법

```powershell
# Windows Update 기록 확인
Get-WindowsUpdateLog  # Windows 10/Server 2016 이상

# 또는 업데이트 확인
$UpdateSession = New-Object -ComObject Microsoft.Update.Session
$UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
$Updates = $UpdateSearcher.Search("IsInstalled=0")
$Updates.Updates | Select-Object Title
```

---

## 4-4. 로그 관리 (W-42 ~ W-47)

### W-42. 로그 정책 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 적절한 감사 로그 기록 |

#### 권장 감사 정책

| 정책 | 성공 | 실패 |
|------|:----:|:----:|
| 계정 로그온 이벤트 감사 | O | O |
| 계정 관리 감사 | O | O |
| 로그온 이벤트 감사 | O | O |
| 개체 액세스 감사 | O | O |
| 정책 변경 감사 | O | O |
| 시스템 이벤트 감사 | O | O |

#### 점검 방법

```powershell
# 감사 정책 확인
auditpol /get /category:*
```

---

### W-43. 로그 파일 크기 설정

#### 권장 설정

| 로그 | 최대 크기 | 보존 정책 |
|------|:--------:|----------|
| 응용 프로그램 | 64MB 이상 | 필요한 경우 덮어쓰기 |
| 보안 | 128MB 이상 | 보관 후 덮어쓰기 |
| 시스템 | 64MB 이상 | 필요한 경우 덮어쓰기 |

#### 점검 방법

```powershell
# 이벤트 로그 설정 확인
Get-EventLog -List | Select-Object Log, MaximumKilobytes
```

---

## 4-5. 보안 관리 (W-48 ~ W-73)

### W-48. 화면 보호기 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 중 |
| **점검 목적** | 무인 터미널 보호 |

#### 권장 설정

- 대기 시간: 10분 이내
- 다시 시작 시 암호 보호: 사용

---

### W-56. Windows 방화벽 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 네트워크 접근 통제 |

#### 점검 방법

```powershell
# 방화벽 상태 확인
Get-NetFirewallProfile | Select-Object Name, Enabled

# 인바운드 규칙 확인
Get-NetFirewallRule -Direction Inbound -Enabled True | Select-Object Name, Action
```

---

### W-67. 최신 백신 프로그램 사용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 악성코드 방어 |

#### 점검 방법

```powershell
# Windows Defender 상태 확인
Get-MpComputerStatus | Select-Object AntivirusEnabled, AntispywareEnabled, RealTimeProtectionEnabled

# 최신 정의 업데이트 확인
Get-MpComputerStatus | Select-Object AntivirusSignatureLastUpdated
```

---

## 4-6. PowerShell 점검 스크립트

### 통합 점검 스크립트

```powershell
#===============================================
# KESE KIT - Windows 서버 취약점 자동 점검
# Version: 1.0
#===============================================

$ReportFile = "windows_check_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

function Write-Report {
    param([string]$Message)
    Write-Host $Message
    Add-Content -Path $ReportFile -Value $Message
}

Write-Report "============================================="
Write-Report "KESE KIT Windows 취약점 점검 결과"
Write-Report "점검 일시: $(Get-Date)"
Write-Report "호스트명: $env:COMPUTERNAME"
Write-Report "============================================="

# W-01: Administrator 계정 이름 변경
Write-Report "`n[W-01] Administrator 계정 이름 변경"
$AdminUser = Get-LocalUser | Where-Object {$_.SID -like "*-500"}
if ($AdminUser.Name -ne "Administrator") {
    Write-Report "  [양호] 계정명 변경됨: $($AdminUser.Name)"
} else {
    Write-Report "  [취약] 기본 계정명 사용 중"
}

# W-02: Guest 계정 비활성화
Write-Report "`n[W-02] Guest 계정 비활성화"
$GuestUser = Get-LocalUser -Name "Guest"
if ($GuestUser.Enabled -eq $false) {
    Write-Report "  [양호] Guest 계정 비활성화됨"
} else {
    Write-Report "  [취약] Guest 계정 활성화됨"
}

# W-05: 계정 잠금 정책
Write-Report "`n[W-05] 계정 잠금 정책"
$NetAccounts = net accounts
$LockoutThreshold = ($NetAccounts | Select-String "Lockout threshold").ToString().Split(":")[1].Trim()
if ($LockoutThreshold -ne "Never" -and [int]$LockoutThreshold -le 5) {
    Write-Report "  [양호] 잠금 임계값: $LockoutThreshold"
} else {
    Write-Report "  [취약] 잠금 임계값: $LockoutThreshold (5회 이하 권장)"
}

# W-14: 원격 레지스트리 서비스
Write-Report "`n[W-14] 원격 레지스트리 서비스"
$RemoteReg = Get-Service -Name "RemoteRegistry" -ErrorAction SilentlyContinue
if ($RemoteReg.Status -ne "Running") {
    Write-Report "  [양호] 원격 레지스트리 비활성화"
} else {
    Write-Report "  [취약] 원격 레지스트리 실행 중"
}

# W-56: Windows 방화벽
Write-Report "`n[W-56] Windows 방화벽"
$Firewall = Get-NetFirewallProfile
$AllEnabled = ($Firewall | Where-Object {$_.Enabled -eq $true}).Count -eq 3
if ($AllEnabled) {
    Write-Report "  [양호] 모든 프로필 방화벽 활성화"
} else {
    Write-Report "  [취약] 일부 방화벽 프로필 비활성화"
}

# W-67: 백신 프로그램
Write-Report "`n[W-67] 백신 프로그램"
try {
    $Defender = Get-MpComputerStatus
    if ($Defender.AntivirusEnabled) {
        Write-Report "  [양호] Windows Defender 활성화"
    } else {
        Write-Report "  [취약] Windows Defender 비활성화"
    }
} catch {
    Write-Report "  [정보] Windows Defender 상태 확인 불가"
}

Write-Report "`n============================================="
Write-Report "점검 완료. 결과 파일: $ReportFile"
```

### 스크립트 사용 방법

```powershell
# 관리자 권한으로 PowerShell 실행
# 실행 정책 설정 (필요 시)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 스크립트 실행
.\windows_check.ps1

# 결과 확인
Get-Content .\windows_check_*.txt
```

---

## 요약

| 영역 | 핵심 점검 항목 | 우선순위 |
|------|---------------|:--------:|
| 계정 관리 | Administrator 변경, Guest 비활성화, 잠금 정책 | 최우선 |
| 서비스 관리 | 불필요 서비스 비활성화, 공유 폴더 점검 | 높음 |
| 패치 관리 | 최신 보안 패치 적용 | 최우선 |
| 로그 관리 | 감사 정책 설정, 로그 크기 | 중간 |
| 보안 관리 | 방화벽, 백신, 화면 보호기 | 높음 |

---

*다음 장: 5장. 웹 서비스 점검*
