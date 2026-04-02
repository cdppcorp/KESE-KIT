# 11장. PC 및 단말기 점검

> Part II. 기술적 취약점 점검

---

## 개요

PC 및 단말기는 사용자와 직접 접촉하는 엔드포인트입니다. 이 장에서는 18개의 점검 항목(PC-01 ~ PC-18)을 다룹니다.

```
┌─────────────────────────────────────────────────────────────────┐
│              PC/단말기 취약점 점검 영역 (18개)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │    사용자 PC     │                          │
│                    │   (엔드포인트)    │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│     ┌───────────────────────┼───────────────────────┐           │
│     │           │           │           │           │           │
│     ▼           ▼           ▼           ▼           ▼           │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐         │
│ │ 계정  │  │ 접근  │  │ 패치  │  │ 보안  │  │ 데이터│         │
│ │ 관리  │  │ 관리  │  │ 관리  │  │ 관리  │  │ 보호  │         │
│ │PC-01~4│  │PC-05~11│ │PC-12~13│ │PC-14~18│ │ (통합)│         │
│ │(4개)  │  │(7개)  │  │(2개)  │  │(5개)  │  │       │         │
│ │       │  │       │  │       │  │       │  │       │         │
│ │• 불필 │  │• 공유 │  │• OS   │  │• 백신 │  │• 암호 │         │
│ │  요   │  │  폴더 │  │  패치 │  │• 방화 │  │  화   │         │
│ │  계정 │  │• USB  │  │• 앱   │  │  벽   │  │• DLP  │         │
│ │• 화면 │  │  제한 │  │  패치 │  │       │  │       │         │
│ │  보호 │  │       │  │       │  │       │  │       │         │
│ └───────┘  └───────┘  └───────┘  └───────┘  └───────┘         │
│                             │                                    │
│                             ▼                                    │
│              ┌───────────────────────────┐                      │
│              │   통합 엔드포인트 보안     │                      │
│              │   (EDR / MDM / NAC)       │                      │
│              └───────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 영역 | 항목 | 항목 수 |
|------|------|:------:|
| 계정 관리 | PC-01 ~ PC-04 | 4 |
| 접근 관리 | PC-05 ~ PC-11 | 7 |
| 패치 관리 | PC-12 ~ PC-13 | 2 |
| 보안 관리 | PC-14 ~ PC-18 | 5 |

---

## 11-1. 계정 관리 (PC-01 ~ PC-04)

### PC-01. 불필요한 계정 제거

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 미사용 계정을 통한 비인가 접근 방지 |

#### 점검 방법 (Windows)

```powershell
# 로컬 계정 확인
Get-LocalUser | Select-Object Name, Enabled, LastLogon

# Guest 계정 비활성화 확인
Get-LocalUser -Name "Guest" | Select-Object Enabled
```

---

### PC-03. 화면 보호기 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 중 |
| **권장 설정** | 10분 이내, 암호 보호 |

#### 점검 방법 (Windows 레지스트리)

```powershell
# 레지스트리 확인
Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" | Select-Object ScreenSaveActive, ScreenSaverIsSecure, ScreenSaveTimeOut
```

---

## 11-2. 접근 관리 (PC-05 ~ PC-11)

### PC-05. 공유 폴더 점검

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 불필요한 공유 제거 |

#### 점검 방법

```powershell
# 공유 폴더 확인
Get-SmbShare | Select-Object Name, Path, Description

# Everyone 접근 가능 공유 확인
Get-SmbShareAccess -Name "공유명" | Where-Object {$_.AccountName -eq "Everyone"}
```

---

### PC-08. 이동식 저장매체 사용 제한

| 항목 | 내용 |
|------|------|
| **중요도** | 중 |
| **점검 목적** | USB 등을 통한 데이터 유출 방지 |

#### 그룹 정책 설정

```
컴퓨터 구성 > 관리 템플릿 > 시스템 > 이동식 저장소 액세스
- 이동식 디스크: 읽기 권한 거부
- 이동식 디스크: 쓰기 권한 거부
```

---

## 11-3. 패치 관리 (PC-12 ~ PC-13)

### PC-12. 운영체제 패치

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 최신 보안 패치 적용 |

#### 점검 방법

```powershell
# 최근 설치된 업데이트 확인
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5

# 대기 중인 업데이트 확인
(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0").Updates | Select-Object Title
```

---

## 11-4. 보안 관리 (PC-14 ~ PC-18)

### PC-14. 백신 프로그램 설치 및 업데이트

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 악성코드 방어 |

#### 점검 방법 (Windows Defender)

```powershell
# Windows Defender 상태
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated
```

---

### PC-17. 개인 방화벽 사용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 네트워크 공격 방어 |

#### 점검 방법

```powershell
# Windows 방화벽 상태
Get-NetFirewallProfile | Select-Object Name, Enabled
```

---

## PC 점검 스크립트

```powershell
#===============================================
# KESE KIT - PC 보안 점검 스크립트
#===============================================

Write-Host "===== PC 보안 점검 =====" -ForegroundColor Cyan

# PC-01: Guest 계정
Write-Host "`n[PC-01] Guest 계정 상태"
$guest = Get-LocalUser -Name "Guest"
if ($guest.Enabled) { Write-Host "  [취약] Guest 활성화" -ForegroundColor Red }
else { Write-Host "  [양호] Guest 비활성화" -ForegroundColor Green }

# PC-05: 공유 폴더
Write-Host "`n[PC-05] 공유 폴더"
Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | ForEach-Object {
    Write-Host "  공유: $($_.Name) - $($_.Path)"
}

# PC-14: 백신 상태
Write-Host "`n[PC-14] 백신 상태"
$defender = Get-MpComputerStatus
if ($defender.AntivirusEnabled -and $defender.RealTimeProtectionEnabled) {
    Write-Host "  [양호] Windows Defender 활성화" -ForegroundColor Green
} else {
    Write-Host "  [취약] Windows Defender 비활성화" -ForegroundColor Red
}

# PC-17: 방화벽
Write-Host "`n[PC-17] 방화벽 상태"
$firewallEnabled = (Get-NetFirewallProfile | Where-Object {$_.Enabled -eq $true}).Count
if ($firewallEnabled -eq 3) {
    Write-Host "  [양호] 모든 프로필 활성화" -ForegroundColor Green
} else {
    Write-Host "  [취약] 일부 프로필 비활성화" -ForegroundColor Red
}

Write-Host "`n===== 점검 완료 =====" -ForegroundColor Cyan
```

---

## 요약

| 영역 | 핵심 점검 항목 | 우선순위 |
|------|---------------|:--------:|
| 계정 관리 | 불필요 계정, 화면 보호기 | 높음 |
| 접근 관리 | 공유 폴더, 이동식 매체 | 높음 |
| 패치 관리 | OS 패치 | 최우선 |
| 보안 관리 | 백신, 방화벽 | 최우선 |

---

*다음 장: 12장. 제어시스템(OT) 점검*
