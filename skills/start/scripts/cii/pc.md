# PC 점검 스크립트 (PC-01 ~ PC-18)

## 1. 계정 관리

### PC-01: 비밀번호의 주기적 변경
**점검:**
```powershell
# 최대 암호 사용 기간 확인
net accounts | findstr "최대"
# 로컬 보안 정책 확인
secedit /export /cfg C:\secpol.cfg
findstr "MaximumPasswordAge" C:\secpol.cfg
findstr "MinimumPasswordAge" C:\secpol.cfg
findstr "PasswordHistorySize" C:\secpol.cfg
```
**조치:**
```powershell
# 최대 암호 사용 기간 90일 설정
net accounts /maxpwage:90
# 최소 암호 사용 기간 1일
net accounts /minpwage:1

# GPO: 시작 > 로컬 보안 정책 > 계정 정책 > 암호 정책
#   "최대 암호 사용 기간": 90일
#   "최소 암호 사용 기간": 1일
#   "최근 암호 기억": 24개

# 계정별 비밀번호 기간 설정
# LUSRMGR.MSC > 사용자 > 계정 속성 > "암호 사용 기간 제한 없음" 해제
```

### PC-02: 비밀번호 관리정책 설정
**점검:**
```powershell
# 암호 복잡성 및 최소 길이 확인
net accounts
secedit /export /cfg C:\secpol.cfg
findstr "MinimumPasswordLength" C:\secpol.cfg
findstr "PasswordComplexity" C:\secpol.cfg
```
**조치:**
```powershell
# GPO: 시작 > 로컬 보안 정책 > 계정 정책 > 암호 정책
#   "최소 암호 길이": 8문자 이상
#   "암호는 복잡성을 만족해야 함": 사용함

# 복잡성 기준: 영문 대/소문자, 숫자, 특수문자 중
#   2종류 조합 시 최소 10자리 이상
#   3종류 조합 시 최소 8자리 이상
```

### PC-03: 복구 콘솔에서 자동 로그온 금지
**점검:**
```powershell
# 복구 콘솔 자동 로그온 설정 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole" /v SecurityLevel
```
**조치:**
```powershell
# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
#   "복구 콘솔: 자동 관리 로그온 허용" -> "사용 안 함"

# 레지스트리 직접 설정
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole" /v SecurityLevel /t REG_DWORD /d 0 /f
```

## 2. 서비스 관리

### PC-04: 공유 폴더 제거
**점검:**
```powershell
# 공유 폴더 목록 확인
net share
# 기본 공유 폴더 확인 (C$, D$, Admin$, IPC$)
Get-SmbShare
# AutoShareWks 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoShareWks
```
**조치:**
```powershell
# 기본 공유 폴더 삭제
net share C$ /delete
net share D$ /delete
net share Admin$ /delete

# 재부팅 시 자동 공유 방지 레지스트리 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoShareWks /t REG_DWORD /d 0 /f

# 일반 공유 폴더 삭제
net share <공유폴더명> /delete

# 공유 폴더 접근에 "Everyone" 제거 (GUI)
# 컴퓨터 관리 > 공유 폴더 > 공유 > 속성 > 공유 사용 권한 > Everyone 제거

# 암호로 보호된 공유 설정
# 설정 > 네트워크 > 고급 공유 설정 > 모든 네트워크 > "암호로 보호된 공유" 켬
```

### PC-05: 불필요한 서비스 제거
**점검:**
```powershell
# 실행 중인 서비스 목록 확인
Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, DisplayName, StartType
# 특정 불필요 서비스 확인
Get-Service -Name "RemoteRegistry","Messenger","Clipbook","Alerter" -ErrorAction SilentlyContinue
```
**조치:**
```powershell
# 불필요 서비스 중지 및 시작 유형 변경
# GUI: services.msc > 해당 서비스 > 속성 > 시작 유형: 사용 안 함

# PowerShell로 서비스 비활성화
Stop-Service -Name "<서비스명>" -Force
Set-Service -Name "<서비스명>" -StartupType Disabled

# 일반적으로 불필요한 서비스 예시:
#   Alerter, Clipbook, Computer Browser, DHCP Client (고정IP 사용 시)
#   Distributed Link Tracking Client, Error Reporting Service
#   Messenger, NetMeeting Remote Desktop Sharing
#   Print Spooler (프린터 미사용 시), Remote Registry
#   Simple TCP/IP Services, Universal Plug and Play Device Host
```

### PC-06: 비인가 상용 메신저 사용 금지
**점검:**
```powershell
# 설치된 메신저 프로그램 확인
Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -match "카카오톡|Skype|NateOn|Telegram"} | Select-Object Name
# 실행 중인 메신저 프로세스 확인
Get-Process | Where-Object {$_.ProcessName -match "kakaotalk|skype|nateon"} | Select-Object ProcessName
```
**조치:**
```powershell
# GPO: gpedit.msc > 컴퓨터 구성 > 관리 템플릿 > Windows 구성 요소 > Windows Messenger
#   "Windows Messenger를 실행 허용 안 함": 사용

# 상용 메신저 제거
# 설정 > 앱 > 앱 및 기능 > 해당 메신저 제거
```

### PC-07: 파일 시스템이 NTFS 포맷으로 설정
**점검:**
```powershell
# 디스크 볼륨 파일 시스템 확인
Get-Volume | Select-Object DriveLetter, FileSystemType, Size
# 또는
fsutil fsinfo volumeinfo C:
```
**조치:**
```powershell
# FAT32 -> NTFS 변환 (비파괴 변환)
convert C: /fs:ntfs

# 변환 후 폴더/파일에 적합한 ACL 적용
# 속성 > 보안 > 편집 > 그룹/계정별 권한 설정
```

### PC-08: 멀티 부팅 방지
**점검:**
```powershell
# 설치된 OS 확인
bcdedit /enum
# 또는
msconfig
# 부팅 탭에서 2개 이상 OS 확인
```
**조치:**
```powershell
# msconfig > 부팅 탭 > 사용하지 않는 OS 선택 후 삭제
# 또는
bcdedit /delete {identifier}
```

### PC-09: 브라우저 종료 시 임시 인터넷 파일 삭제
**점검:**
```powershell
# GPO 설정 확인
reg query "HKLM\SOFTWARE\Policies\Microsoft\Internet Explorer\Privacy" /v ClearBrowsingHistoryOnExit
```
**조치:**
```powershell
# GPO: gpedit.msc > 컴퓨터 구성 > 관리 템플릿 > Windows 구성 요소
#   > Internet Explorer > 인터넷 제어판 > 고급 페이지
#   "브라우저를 닫을 때 임시 인터넷 파일 폴더 비우기": 사용

# 레지스트리 직접 설정
reg add "HKLM\SOFTWARE\Policies\Microsoft\Internet Explorer\Privacy" /v ClearBrowsingHistoryOnExit /t REG_DWORD /d 1 /f
```

## 3. 패치 관리

### PC-10: 주기적 보안 패치 및 벤더 권고사항 적용
**점검:**
```powershell
# 설치된 HOT FIX 확인
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
# Windows Update 설정 확인
Get-WindowsUpdateLog
# 자동 업데이트 설정 확인
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
```
**조치:**
```powershell
# 설정 > Windows Update > 업데이트 확인
# PowerShell로 업데이트 확인 및 설치
Install-Module PSWindowsUpdate -Force
Get-WindowsUpdate
Install-WindowsUpdate -AcceptAll -AutoReboot
```

### PC-11: 지원이 종료되지 않은 Windows OS Build 적용
**점검:**
```powershell
# 현재 OS 빌드 버전 확인
[System.Environment]::OSVersion.Version
Get-ComputerInfo | Select-Object WindowsVersion, OsBuildNumber, WindowsProductName
winver
```
**조치:**
```powershell
# Windows Update를 통한 최신 빌드 적용
# 설정 > Windows Update > 업데이트 확인
# 수동 업데이트: https://www.microsoft.com/ko-kr/software-download/
```

## 4. 보안 관리

### PC-12: Windows 자동 로그인 점검
**점검:**
```powershell
# 자동 로그인 레지스트리 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword
```
**조치:**
```powershell
# 자동 로그인 비활성화
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 0 /f
# DefaultPassword 값 삭제
reg delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /f
```

### PC-13: 바이러스 백신 프로그램 설치 및 주기적 업데이트
**점검:**
```powershell
# Windows Defender 상태 확인
Get-MpComputerStatus | Select-Object AntivirusEnabled, AntivirusSignatureLastUpdated, AntispywareEnabled
# 백신 설치 여부 확인
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | Select-Object displayName, productState
```
**조치:**
```powershell
# Windows Defender 업데이트
Update-MpSignature
# 설정 > Windows 보안 > 바이러스 및 위협 방지 > 보호 업데이트 > 업데이트 확인
```

### PC-14: 백신 실시간 감시 기능 활성화
**점검:**
```powershell
# 실시간 보호 상태 확인
Get-MpPreference | Select-Object DisableRealtimeMonitoring
Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled
```
**조치:**
```powershell
# 실시간 보호 활성화
Set-MpPreference -DisableRealtimeMonitoring $false
# GUI: Windows 보안 > 바이러스 및 위협 방지 > 설정 관리 > 실시간 보호 켬
```

### PC-15: OS에서 제공하는 침입차단 기능 활성화
**점검:**
```powershell
# 방화벽 상태 확인
Get-NetFirewallProfile | Select-Object Name, Enabled
netsh advfirewall show allprofiles state
```
**조치:**
```powershell
# 방화벽 활성화 (모든 프로필)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
# 또는
netsh advfirewall set allprofiles state on

# GUI: 제어판 > Windows Defender 방화벽 > 설정/해제 > "사용" 설정
```

### PC-16: 화면보호기 대기 시간 설정 및 재시작 시 암호 보호
**점검:**
```powershell
# 화면보호기 설정 확인
reg query "HKCU\Control Panel\Desktop" /v ScreenSaveTimeOut
reg query "HKCU\Control Panel\Desktop" /v ScreenSaverIsSecure
reg query "HKCU\Control Panel\Desktop" /v ScreenSaveActive
```
**조치:**
```powershell
# 화면보호기 활성화
reg add "HKCU\Control Panel\Desktop" /v ScreenSaveActive /t REG_SZ /d 1 /f
# 대기 시간 설정 (600초 = 10분 이하)
reg add "HKCU\Control Panel\Desktop" /v ScreenSaveTimeOut /t REG_SZ /d 600 /f
# 재시작 시 암호 보호
reg add "HKCU\Control Panel\Desktop" /v ScreenSaverIsSecure /t REG_SZ /d 1 /f

# GUI: 설정 > 개인설정 > 잠금화면 > 화면보호기
#   대기: 10분 이하 / "다시 시작 시 로그온 화면 표시" 체크
```

### PC-17: 이동식 미디어 자동 실행 방지
**점검:**
```powershell
# 자동 실행 정책 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoDriveTypeAutoRun
# GPO 확인
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\Explorer" /v NoAutorun
```
**조치:**
```powershell
# 모든 드라이브 자동 실행 끄기
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f

# GPO: gpedit.msc > 컴퓨터 구성 > 관리 템플릿 > Windows 구성 요소 > 자동 실행 정책
#   "자동 실행 끄기": 사용 - 모든 드라이브

# 제어판: 하드웨어 및 소리 > 자동 실행
#   "모든 미디어 및 장치에 자동 실행 사용" 체크 해제
```

### PC-18: 원격 지원 금지
**점검:**
```powershell
# 원격 지원 설정 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Remote Assistance" /v fAllowToGetHelp
# 원격 데스크톱 설정 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections
```
**조치:**
```powershell
# 원격 지원 비활성화
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Remote Assistance" /v fAllowToGetHelp /t REG_DWORD /d 0 /f

# GPO: gpedit.msc > 컴퓨터 구성 > 관리 템플릿 > 시스템 > 원격 지원
#   "원격 지원 제공 구성": 사용 안 함

# 원격 데스크톱 비활성화 (필요 시)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f
```
