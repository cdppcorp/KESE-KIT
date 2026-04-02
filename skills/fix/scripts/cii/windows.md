# Windows 서버 취약점 점검/조치 스크립트
> KISA 주요정보통신기반시설 기술적 취약점 분석평가 가이드 (W-01 ~ W-64)

---

## 1. 계정 관리

### W-01: Administrator 계정 이름 변경 등 보안성 강화 (상)
**점검:**
```powershell
# Administrator(SID-500) 계정명 확인
Get-LocalUser | Where-Object {$_.SID -like "*-500"} | Select-Object Name, Enabled, SID

# 로컬 보안 정책에서 확인
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "NewAdministratorName" C:\secpol_tmp.cfg
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# Administrator 계정명을 유추 불가능한 이름으로 변경
Rename-LocalUser -Name "Administrator" -NewName "yourCustomAdmin"

# 또는 wmic 사용
wmic useraccount where "SID like '%-500'" rename "yourCustomAdmin"

# GPO 방식: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "계정: Administrator 계정 이름 바꾸기" 설정
```

---

### W-02: Guest 계정 비활성화 (상)
**점검:**
```powershell
# Guest 계정 활성화 여부 확인
Get-LocalUser -Name "Guest" | Select-Object Name, Enabled

# net 명령으로 확인
net user Guest
```
**조치:**
```powershell
# Guest 계정 비활성화
Disable-LocalUser -Name "Guest"

# 또는 net 명령
net user Guest /active:no
```

---

### W-03: 불필요한 계정 제거 (상)
**점검:**
```powershell
# 전체 로컬 사용자 계정 목록 확인
Get-LocalUser | Select-Object Name, Enabled, LastLogon, PasswordLastSet | Format-Table

# 장기 미사용 계정 확인 (90일 이상 미로그인)
Get-LocalUser | Where-Object {
    $_.Enabled -eq $true -and
    $_.LastLogon -lt (Get-Date).AddDays(-90)
} | Select-Object Name, LastLogon
```
**조치:**
```powershell
# 불필요한 계정 비활성화
Disable-LocalUser -Name "<불필요한계정명>"

# 불필요한 계정 삭제
Remove-LocalUser -Name "<불필요한계정명>"
```

---

### W-04: 계정 잠금 임계값 설정 (상)
**점검:**
```powershell
# 계정 잠금 정책 확인
net accounts

# 상세 확인 (secedit)
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "LockoutBadCount" C:\secpol_tmp.cfg
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# 계정 잠금 임계값 5회로 설정
net accounts /lockoutthreshold:5

# GPO 방식: 로컬 보안 정책 > 계정 정책 > 계정 잠금 정책
# "계정 잠금 임계값" = 5
```

---

### W-05: 해독 가능한 암호화를 사용하여 암호 저장 해제 (상)
**점검:**
```powershell
# 정책 확인
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "ClearTextPassword" C:\secpol_tmp.cfg
# 값이 0이면 양호
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# 로컬 보안 정책 > 계정 정책 > 암호 정책
# "해독 가능한 암호화를 사용하여 암호 저장" = 사용 안 함
# secedit 인라인 설정
secedit /export /cfg C:\secpol_tmp.cfg
(Get-Content C:\secpol_tmp.cfg) -replace "ClearTextPassword = 1","ClearTextPassword = 0" | Set-Content C:\secpol_tmp.cfg
secedit /configure /db C:\Windows\security\local.sdb /cfg C:\secpol_tmp.cfg /areas SECURITYPOLICY
Remove-Item C:\secpol_tmp.cfg -Force
```

---

### W-06: 관리자 그룹에 최소한의 사용자 포함 (상)
**점검:**
```powershell
# Administrators 그룹 구성원 확인
Get-LocalGroupMember -Group "Administrators" | Select-Object Name, ObjectClass, PrincipalSource

# net 명령
net localgroup Administrators
```
**조치:**
```powershell
# 불필요한 계정을 Administrators 그룹에서 제거
Remove-LocalGroupMember -Group "Administrators" -Member "<불필요한계정>"

# 관리 업무용 계정과 일반 업무용 계정을 분리하여 운용
```

---

### W-07: Everyone 사용 권한을 익명 사용자에 적용 해제 (중)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v EveryoneIncludesAnonymous
# 값이 0이면 양호

# 로컬 보안 정책 내보내기로 확인
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "EveryoneIncludesAnonymous" C:\secpol_tmp.cfg
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# 레지스트리 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v EveryoneIncludesAnonymous /t REG_DWORD /d 0 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "네트워크 액세스: Everyone 사용 권한을 익명 사용자에게 적용" = 사용 안 함
```

---

### W-08: 계정 잠금 기간 설정 (중)
**점검:**
```powershell
# 계정 잠금 정책 확인
net accounts
# "잠금 기간(분)"과 "잠금 관찰 창(분)" 확인

secedit /export /cfg C:\secpol_tmp.cfg
Select-String "LockoutDuration|ResetLockoutCount" C:\secpol_tmp.cfg
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# 계정 잠금 기간 60분, 잠금 수 원래대로 설정 기간 60분
net accounts /lockoutduration:60
net accounts /lockoutwindow:60

# GPO: 로컬 보안 정책 > 계정 정책 > 계정 잠금 정책
# "계정 잠금 기간" = 60분
# "다음 시간 후 계정 잠금 수를 원래대로 설정" = 60분
```

---

### W-09: 비밀번호 관리 정책 설정 (상)
**점검:**
```powershell
# 암호 정책 확인
net accounts

secedit /export /cfg C:\secpol_tmp.cfg
Select-String "MinimumPasswordLength|PasswordComplexity|MaximumPasswordAge|MinimumPasswordAge|PasswordHistorySize" C:\secpol_tmp.cfg
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# 암호 정책 설정
net accounts /minpwlen:8 /maxpwage:90 /minpwage:1 /uniquepw:4

# GPO: 로컬 보안 정책 > 계정 정책 > 암호 정책
# "암호는 복잡성을 만족해야 함" = 사용
# "최소 암호 길이" = 8문자
# "최대 암호 사용 기간" = 90일
# "최소 암호 사용 기간" = 1일
# "최근 암호 기억" = 4개 암호 기억됨
```

---

### W-10: 마지막 사용자 이름 표시 안 함 (중)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v DontDisplayLastUserName
# 값이 1이면 양호
```
**조치:**
```powershell
# 레지스트리 설정
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v DontDisplayLastUserName /t REG_DWORD /d 1 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "대화형 로그온: 마지막 사용자 이름 표시 안 함" = 사용
```

---

### W-11: 로컬 로그온 허용 (중)
**점검:**
```powershell
# 로컬 로그온 허용 정책 확인
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "SeInteractiveLogonRight" C:\secpol_tmp.cfg
Remove-Item C:\secpol_tmp.cfg -Force

# Administrators, IUSR_ 외 다른 계정이 있으면 취약
```
**조치:**
```powershell
# GPO: 로컬 보안 정책 > 로컬 정책 > 사용자 권한 할당
# "로컬 로그온 허용" 정책에 Administrators, IUSR_ 외 다른 계정 및 그룹 제거

# ntrights 유틸리티 사용 (Windows Resource Kit)
# ntrights -u "<제거할계정>" -r SeInteractiveLogonRight
```

---

### W-12: 익명 SID/이름 변환 허용 해제 (중)
**점검:**
```powershell
# 레지스트리 확인 (Windows 2003 이상)
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "LSAAnonymousNameLookup" C:\secpol_tmp.cfg
# 값이 0이면 양호
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "네트워크 액세스: 익명 SID/이름 변환 허용" = 사용 안 함
```

---

### W-13: 콘솔 로그온 시 로컬 계정에서 빈 암호 사용 제한 (중)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LimitBlankPasswordUse
# 값이 1이면 양호
```
**조치:**
```powershell
# 레지스트리 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LimitBlankPasswordUse /t REG_DWORD /d 1 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "계정: 콘솔 로그온 시 로컬 계정에서 빈 암호 사용 제한" = 사용
```

---

### W-14: 원격터미널 접속 가능한 사용자 그룹 제한 (중)
**점검:**
```powershell
# Remote Desktop Users 그룹 구성원 확인
Get-LocalGroupMember -Group "Remote Desktop Users" | Select-Object Name, ObjectClass

# 원격 데스크톱 설정 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections
# 0이면 원격 데스크톱 허용 상태
```
**조치:**
```powershell
# 관리자 외 별도 원격 접속 계정 생성
New-LocalUser -Name "rdpUser" -Password (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force) -FullName "RDP 전용 사용자"
Add-LocalGroupMember -Group "Remote Desktop Users" -Member "rdpUser"

# 불필요한 계정 제거
Remove-LocalGroupMember -Group "Remote Desktop Users" -Member "<불필요한계정>"
```

---

## 2. 서비스 관리

### W-15: 사용자 개인키 사용 시 암호 입력 (상)
**점검:**
```powershell
# 로컬 보안 정책 확인
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "ForceKeyProtection" C:\secpol_tmp.cfg
# 값이 2이면 양호 (키를 사용할 때마다 암호 입력)
Remove-Item C:\secpol_tmp.cfg -Force

# 레지스트리 직접 확인
reg query "HKLM\SOFTWARE\Policies\Microsoft\Cryptography" /v ForceKeyProtection
```
**조치:**
```powershell
# 레지스트리 설정 (2 = 키를 사용할 때마다 암호 매번 입력)
reg add "HKLM\SOFTWARE\Policies\Microsoft\Cryptography" /v ForceKeyProtection /t REG_DWORD /d 2 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "시스템 암호화: 컴퓨터에 저장된 사용자 키에 대해 강력한 키 보호 사용"
# = "키를 사용할 때마다 암호를 매 번 입력해야 함"
```

---

### W-16: 공유 권한 및 사용자 그룹 설정 (상)
**점검:**
```powershell
# 공유 폴더 목록 확인
Get-SmbShare | Select-Object Name, Path, Description | Format-Table

# 공유 폴더 권한에서 Everyone 확인
Get-SmbShare | ForEach-Object {
    $share = $_.Name
    Get-SmbShareAccess -Name $share | Where-Object { $_.AccountName -like "*Everyone*" } |
    Select-Object @{N='Share';E={$share}}, AccountName, AccessControlType, AccessRight
}
```
**조치:**
```powershell
# 공유 폴더에서 Everyone 권한 제거
Revoke-SmbShareAccess -Name "<공유명>" -AccountName "Everyone" -Force

# 필요한 계정에 적절한 권한 추가
Grant-SmbShareAccess -Name "<공유명>" -AccountName "<계정명>" -AccessRight Read -Force
```

---

### W-17: 하드디스크 기본 공유 제거 (상)
**점검:**
```powershell
# 기본 공유 확인
net share
Get-SmbShare | Where-Object { $_.Name -match '^\w\$|^ADMIN\$' } | Select-Object Name, Path

# AutoShareServer 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoShareServer 2>$null
reg query "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoShareWks 2>$null
```
**조치:**
```powershell
# 기본 공유 중지
net share C$ /delete
net share D$ /delete
net share ADMIN$ /delete

# 재부팅 후 재생성 방지 (레지스트리)
reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoShareServer /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoShareWks /t REG_DWORD /d 0 /f

# 참고: 방화벽에서 135~139(TCP/UDP) 포트 차단 권장
```

---

### W-18: 불필요한 서비스 제거 (상)
**점검:**
```powershell
# 실행 중인 서비스 목록
Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, DisplayName, StartType | Format-Table

# 불필요한 서비스 존재 여부 확인
$unnecessaryServices = @("Alerter","ClipSrv","Browser","CryptSvc","DHCPClient",
    "TrkWks","TrkSvr","ERSvc","HidServ","IMAPICD","Messenger","mnmsrvc",
    "WmdmPmSN","Spooler","RemoteRegistry","simptcp","upnphost","WZCSVC")
Get-Service | Where-Object { $unnecessaryServices -contains $_.Name -and $_.Status -eq "Running" } |
    Select-Object Name, DisplayName, Status
```
**조치:**
```powershell
# 불필요한 서비스 중지 및 비활성화
Stop-Service -Name "<서비스명>" -Force
Set-Service -Name "<서비스명>" -StartupType Disabled

# 예시: Remote Registry 비활성화
Stop-Service -Name "RemoteRegistry" -Force
Set-Service -Name "RemoteRegistry" -StartupType Disabled

# 예시: Print Spooler 비활성화 (프린터 미사용 시)
Stop-Service -Name "Spooler" -Force
Set-Service -Name "Spooler" -StartupType Disabled
```

---

### W-19: 불필요한 IIS 서비스 구동 점검 (상)
**점검:**
```powershell
# IIS 서비스 상태 확인
Get-Service -Name "W3SVC" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType
Get-Service -Name "IISADMIN" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType

# IIS 설치 여부
Get-WindowsFeature -Name Web-Server 2>$null | Select-Object Name, Installed
```
**조치:**
```powershell
# IIS 서비스 중지 및 비활성화 (불필요 시)
Stop-Service -Name "W3SVC" -Force -ErrorAction SilentlyContinue
Set-Service -Name "W3SVC" -StartupType Disabled -ErrorAction SilentlyContinue
Stop-Service -Name "IISADMIN" -Force -ErrorAction SilentlyContinue
Set-Service -Name "IISADMIN" -StartupType Disabled -ErrorAction SilentlyContinue

# IIS 기능 제거
Uninstall-WindowsFeature -Name Web-Server
```

---

### W-20: NetBIOS 바인딩 서비스 구동 점검 (상)
**점검:**
```powershell
# NetBIOS over TCP/IP 설정 확인
Get-WmiObject Win32_NetworkAdapterConfiguration -Filter "IPEnabled=true" |
    Select-Object Description, TcpipNetbiosOptions
# TcpipNetbiosOptions: 0=DHCP기본, 1=사용, 2=사용안함

# 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\NetBT\Parameters\Interfaces" /s /v NetbiosOptions
```
**조치:**
```powershell
# NetBIOS over TCP/IP 비활성화 (WMI)
$adapters = Get-WmiObject Win32_NetworkAdapterConfiguration -Filter "IPEnabled=true"
foreach ($adapter in $adapters) {
    $adapter.SetTcpipNetbios(2)  # 2 = NetBIOS 사용 안 함
}

# GUI: 네트워크 연결 > 속성 > TCP/IPv4 > 고급 > WINS 탭
# "NetBIOS over TCP/IP 사용 안 함" 선택
```

---

### W-21: 암호화되지 않는 FTP 서비스 비활성화 (상)
**점검:**
```powershell
# FTP 서비스 상태 확인
Get-Service -Name "FTPSVC" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType
Get-Service -Name "MSFTPSVC" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType
```
**조치:**
```powershell
# FTP 서비스 중지 및 비활성화
Stop-Service -Name "FTPSVC" -Force -ErrorAction SilentlyContinue
Set-Service -Name "FTPSVC" -StartupType Disabled -ErrorAction SilentlyContinue

# SFTP 또는 FTPS 대안 사용 권장
```

---

### W-22: FTP 디렉토리 접근권한 설정 (상)
**점검:**
```powershell
# FTP 홈 디렉터리 경로 확인 (IIS 기반)
Import-Module WebAdministration -ErrorAction SilentlyContinue
Get-WebConfiguration -Filter "/system.ftpServer/sites/site" -PSPath "IIS:\" -ErrorAction SilentlyContinue

# FTP 홈 디렉터리 권한 확인
icacls "C:\inetpub\ftproot" 2>$null
# Everyone 권한이 있으면 취약
```
**조치:**
```powershell
# FTP 홈 디렉터리에서 Everyone 권한 제거
icacls "C:\inetpub\ftproot" /remove Everyone /T

# 필요한 사용자에게만 권한 부여
icacls "C:\inetpub\ftproot" /grant "ftpUser:(OI)(CI)RX"
```

---

### W-23: 공유 서비스에 대한 익명 접근 제한 설정 (상)
**점검:**
```powershell
# FTP 익명 인증 설정 확인 (IIS)
Import-Module WebAdministration -ErrorAction SilentlyContinue
Get-WebConfigurationProperty -PSPath "IIS:\Sites\Default FTP Site" -Filter "/system.ftpServer/security/authentication/anonymousAuthentication" -Name "enabled" -ErrorAction SilentlyContinue
```
**조치:**
```powershell
# IIS FTP 익명 인증 비활성화
Import-Module WebAdministration
Set-WebConfigurationProperty -PSPath "IIS:\Sites\Default FTP Site" -Filter "/system.ftpServer/security/authentication/anonymousAuthentication" -Name "enabled" -Value $false

# 또는 IIS 관리자에서:
# FTP 사이트 > FTP 인증 > 익명 인증 = 사용 안 함
```

---

### W-24: FTP 접근 제어 설정 (상)
**점검:**
```powershell
# IIS FTP IP 제한 설정 확인
Import-Module WebAdministration -ErrorAction SilentlyContinue
Get-WebConfiguration -Filter "/system.ftpServer/security/ipSecurity" -PSPath "IIS:\Sites\Default FTP Site" -ErrorAction SilentlyContinue
```
**조치:**
```powershell
# IIS 관리자에서 FTP 사이트 > FTP IPv4 주소 및 도메인 제한
# 1) 허용 항목 추가 (접속 허용 IP)
# 2) 기능 설정 편집 > 지정되지 않은 클라이언트 액세스 = 거부

# PowerShell (IIS 모듈)
Import-Module WebAdministration
# 특정 IP 허용 추가
Add-WebConfigurationProperty -PSPath "IIS:\Sites\Default FTP Site" -Filter "/system.ftpServer/security/ipSecurity" -Name "." -Value @{ipAddress="192.168.1.100";allowed="true"}
```

---

### W-25: DNS Zone Transfer 설정 (상)
**점검:**
```powershell
# DNS 서비스 상태 확인
Get-Service -Name "DNS" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType

# DNS 영역 전송 설정 확인 (DNS 서버 설치 시)
Get-DnsServerZone -ErrorAction SilentlyContinue | Select-Object ZoneName, ZoneType
Get-DnsServerZone -ErrorAction SilentlyContinue | ForEach-Object {
    Get-DnsServerZoneTransferPolicy -ZoneName $_.ZoneName -ErrorAction SilentlyContinue
}
```
**조치:**
```powershell
# DNS 영역 전송을 특정 서버로만 제한
# dnscmd /zoneresetsecondaries <영역이름> /securens
Set-DnsServerPrimaryZone -Name "<영역이름>" -SecureSecondaries TransferToSecureServers -ErrorAction SilentlyContinue

# 불필요 시 DNS 서비스 중지
Stop-Service -Name "DNS" -Force -ErrorAction SilentlyContinue
Set-Service -Name "DNS" -StartupType Disabled -ErrorAction SilentlyContinue
```

---

### W-26: RDS(Remote Data Services) 제거 (상)
**점검:**
```powershell
# MSADC 가상 디렉터리 존재 확인 (IIS 기반)
Import-Module WebAdministration -ErrorAction SilentlyContinue
Get-WebVirtualDirectory -Site "Default Web Site" -Name "MSADC" -ErrorAction SilentlyContinue

# RDS 관련 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\W3SVC\Parameters\ADCLaunch" 2>$null
```
**조치:**
```powershell
# MSADC 가상 디렉터리 제거
Import-Module WebAdministration -ErrorAction SilentlyContinue
Remove-WebVirtualDirectory -Site "Default Web Site" -Name "MSADC" -ErrorAction SilentlyContinue

# RDS 관련 레지스트리 키 제거
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\W3SVC\Parameters\ADCLaunch\RDSServer.DataFactory" /f 2>$null
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\W3SVC\Parameters\ADCLaunch\AdvancedDataFactory" /f 2>$null
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\W3SVC\Parameters\ADCLaunch\VbBusObj.VbBusObjCls" /f 2>$null

# 참고: Windows 2008 이상은 해당 없음
```

---

### W-27: 최신 Windows OS Build 버전 적용 (상)
**점검:**
```powershell
# Windows 빌드 버전 확인
[System.Environment]::OSVersion.Version
(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").CurrentBuild
(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").UBR

# winver 실행
winver

# systeminfo로 상세 정보
systeminfo | Select-String "OS 이름|OS 버전|OS Name|OS Version"
```
**조치:**
```powershell
# Windows Update 확인 및 설치
# 자동 업데이트:
# 제어판 > Windows Update

# PowerShell로 업데이트 확인 (PSWindowsUpdate 모듈)
Install-Module PSWindowsUpdate -Force -ErrorAction SilentlyContinue
Get-WindowsUpdate
Install-WindowsUpdate -AcceptAll -AutoReboot

# 수동 패치: https://msrc.microsoft.com/update-guide
```

---

### W-28: 터미널 서비스 암호화 수준 설정 (중)
**점검:**
```powershell
# RDP 암호화 수준 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MinEncryptionLevel
# 2=중간(클라이언트 호환 가능), 3=높음, 4=FIPS

# GPO 설정 확인
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services" /v MinEncryptionLevel 2>$null
```
**조치:**
```powershell
# 레지스트리에서 암호화 수준 설정 (2 이상)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MinEncryptionLevel /t REG_DWORD /d 3 /f

# GPO: 컴퓨터 구성 > 관리 템플릿 > Windows 구성 요소 > 원격 데스크톱 서비스
#       > 원격 데스크톱 세션 호스트 > 보안
# "클라이언트 연결 암호화 수준 설정" = 사용 (높음)
```

---

### W-29: 불필요한 SNMP 서비스 구동 점검 (중)
**점검:**
```powershell
# SNMP 서비스 상태 확인
Get-Service -Name "SNMP" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType
```
**조치:**
```powershell
# SNMP 서비스 중지 및 비활성화 (불필요 시)
Stop-Service -Name "SNMP" -Force -ErrorAction SilentlyContinue
Set-Service -Name "SNMP" -StartupType Disabled -ErrorAction SilentlyContinue
```

---

### W-30: SNMP Community String 복잡성 설정 (중)
**점검:**
```powershell
# SNMP Community String 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities" 2>$null
# public, private이 있으면 취약
```
**조치:**
```powershell
# 기본 Community String 제거
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities" /v public /f 2>$null
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities" /v private /f 2>$null

# 복잡한 Community String 추가 (읽기전용 = 4)
reg add "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities" /v "C0mpl3x$tr1ng!" /t REG_DWORD /d 4 /f

# SNMP 서비스 재시작
Restart-Service -Name "SNMP" -ErrorAction SilentlyContinue
```

---

### W-31: SNMP Access Control 설정 (중)
**점검:**
```powershell
# SNMP 허용 호스트 설정 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\PermittedManagers" 2>$null
# 값이 없으면 모든 호스트 허용 (취약)
```
**조치:**
```powershell
# 특정 호스트로부터만 SNMP 패킷 수신 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\PermittedManagers" /v 1 /t REG_SZ /d "192.168.1.100" /f

# GUI: 서비스 > SNMP Service > 속성 > 보안 탭
# "다음 호스트로부터 SNMP 패킷 받아들이기" 선택 후 호스트 등록
Restart-Service -Name "SNMP" -ErrorAction SilentlyContinue
```

---

### W-32: DNS 서비스 구동 점검 (중)
**점검:**
```powershell
# DNS 서비스 상태 확인
Get-Service -Name "DNS" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType

# DNS 동적 업데이트 설정 확인
Get-DnsServerZone -ErrorAction SilentlyContinue | Select-Object ZoneName, DynamicUpdate
```
**조치:**
```powershell
# DNS 동적 업데이트 비활성화
Set-DnsServerPrimaryZone -Name "<영역이름>" -DynamicUpdate None -ErrorAction SilentlyContinue

# 불필요 시 DNS 서비스 중지
Stop-Service -Name "DNS" -Force -ErrorAction SilentlyContinue
Set-Service -Name "DNS" -StartupType Disabled -ErrorAction SilentlyContinue
```

---

### W-33: HTTP/FTP/SMTP 배너 차단 (하)
**점검:**
```powershell
# IIS Server 헤더 확인 (HTTP 응답)
# (Invoke-WebRequest -Uri "http://localhost" -UseBasicParsing).Headers["Server"]

# IIS X-Powered-By 헤더 확인
Import-Module WebAdministration -ErrorAction SilentlyContinue
Get-WebConfigurationProperty -PSPath "IIS:\Sites\Default Web Site" -Filter "system.webServer/httpProtocol/customHeaders" -Name "." -ErrorAction SilentlyContinue

# SMTP 배너 확인
# telnet localhost 25 으로 접속 시 배너 확인
```
**조치:**
```powershell
# [HTTP] IIS Server 헤더 제거 - URL Rewrite 모듈 필요
# 1) URL Rewrite 설치: https://www.iis.net/downloads/microsoft/url-rewrite
# 2) 아웃바운드 규칙 추가: 서버 변수 RESPONSE_SERVER 비우기

# [HTTP] X-Powered-By 헤더 제거
Import-Module WebAdministration -ErrorAction SilentlyContinue
Remove-WebConfigurationProperty -PSPath "IIS:\Sites\Default Web Site" -Filter "system.webServer/httpProtocol/customHeaders" -Name "." -AtElement @{name="X-Powered-By"} -ErrorAction SilentlyContinue

# [FTP] 기본 배너 숨기기
# IIS 관리자 > FTP 사이트 > FTP 메시지 > "기본 배너 숨기기" 체크

# [SMTP] 배너 변경
# cd C:\inetpub\AdminScripts
# cscript adsutil.vbs set smtpsvc/1/connectresponse "Authorized Access Only"
# net stop smtpsvc && net start smtpsvc
```

---

### W-34: Telnet 서비스 비활성화 (중)
**점검:**
```powershell
# Telnet 서비스 상태 확인
Get-Service -Name "TlntSvr" -ErrorAction SilentlyContinue | Select-Object Name, Status, StartType

# Telnet 인증 방식 확인 (Windows 2003~2012)
# tlntadmn config 명령으로 확인
```
**조치:**
```powershell
# Telnet 서비스 중지 및 비활성화
Stop-Service -Name "TlntSvr" -Force -ErrorAction SilentlyContinue
Set-Service -Name "TlntSvr" -StartupType Disabled -ErrorAction SilentlyContinue

# 부득이 사용 시 NTLM 인증만 사용
# tlntadmn config sec = +NTLM -passwd

# 참고: Windows 2016 이상에서는 Telnet 서버 제공하지 않음
```

---

### W-35: 불필요한 ODBC/OLE-DB 데이터 소스와 드라이브 제거 (중)
**점검:**
```powershell
# 시스템 DSN 확인
Get-OdbcDsn -DsnType System -ErrorAction SilentlyContinue | Select-Object Name, DriverName, Platform

# 레지스트리에서 ODBC 데이터 소스 확인
reg query "HKLM\SOFTWARE\ODBC\ODBC.INI\ODBC Data Sources" 2>$null
```
**조치:**
```powershell
# 불필요한 ODBC 데이터 소스 제거
Remove-OdbcDsn -Name "<데이터소스명>" -DsnType System -ErrorAction SilentlyContinue

# GUI: 제어판 > 관리 도구 > ODBC 데이터 원본 > 시스템 DSN
# 불필요한 데이터 소스 선택 후 제거
```

---

### W-36: 원격터미널 접속 타임아웃 설정 (중)
**점검:**
```powershell
# RDP 세션 유휴 타임아웃 레지스트리 확인
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services" /v MaxIdleTime 2>$null
# 밀리초 단위: 1800000 = 30분

# 현재 설정 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxIdleTime 2>$null
```
**조치:**
```powershell
# 유휴 세션 타임아웃 30분(1800000ms) 설정
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services" /v MaxIdleTime /t REG_DWORD /d 1800000 /f

# GPO: 컴퓨터 구성 > 관리 템플릿 > Windows 구성 요소 > 원격 데스크톱 서비스
#       > 원격 데스크톱 세션 호스트 > 세션 시간 제한
# "활성 상태지만 유휴 터미널 서비스 세션에 시간 제한 설정" = 사용 (30분)
```

---

### W-37: 예약된 작업에 의심스러운 명령이 등록되어 있는지 점검 (중)
**점검:**
```powershell
# 예약된 작업 목록 확인
Get-ScheduledTask | Where-Object {$_.State -ne "Disabled"} |
    Select-Object TaskName, TaskPath, State |
    Format-Table -AutoSize

# 예약된 작업 상세 정보 (실행 명령 포함)
Get-ScheduledTask | ForEach-Object {
    $task = $_
    $actions = $task.Actions
    foreach ($action in $actions) {
        [PSCustomObject]@{
            TaskName = $task.TaskName
            Execute  = $action.Execute
            Arguments = $action.Arguments
            State    = $task.State
        }
    }
} | Format-Table -AutoSize

# schtasks 명령
schtasks /query /fo LIST /v
```
**조치:**
```powershell
# 의심스러운 예약 작업 비활성화
Disable-ScheduledTask -TaskName "<작업이름>"

# 의심스러운 예약 작업 삭제
Unregister-ScheduledTask -TaskName "<작업이름>" -Confirm:$false

# schtasks 명령
schtasks /delete /tn "<작업이름>" /f
```

---

## 3. 패치 관리

### W-38: 주기적 보안 패치 및 벤더 권고사항 적용 (상)
**점검:**
```powershell
# 설치된 핫픽스 목록 확인
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object HotFixID, InstalledOn, Description -First 20

# 시스템 정보에서 KB 목록
systeminfo | findstr "KB"

# 마지막 패치 설치 날짜 확인
(Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 1).InstalledOn

# Windows Update 이력 확인
$session = New-Object -ComObject Microsoft.Update.Session
$searcher = $session.CreateUpdateSearcher()
$history = $searcher.QueryHistory(0, 20)
$history | Select-Object Title, Date, ResultCode | Format-Table
```
**조치:**
```powershell
# Windows Update 실행
# 수동: https://msrc.microsoft.com/update-guide
# 자동: 제어판 > Windows Update

# PowerShell 모듈 사용
Install-Module PSWindowsUpdate -Force -ErrorAction SilentlyContinue
Get-WindowsUpdate
Install-WindowsUpdate -AcceptAll
```

---

### W-39: 백신 프로그램 업데이트 (상)
**점검:**
```powershell
# Windows Defender 상태 확인
Get-MpComputerStatus | Select-Object AMServiceEnabled, AntispywareEnabled, AntivirusEnabled,
    AntivirusSignatureLastUpdated, AntispywareSignatureLastUpdated

# 백신 엔진 버전 확인
Get-MpComputerStatus | Select-Object AMEngineVersion, AMProductVersion, AntivirusSignatureVersion

# 3rd party 백신 확인
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct -ErrorAction SilentlyContinue |
    Select-Object displayName, productState, pathToSignedProductExe
```
**조치:**
```powershell
# Windows Defender 정의 업데이트
Update-MpSignature

# Windows Defender 수동 빠른 검사
Start-MpScan -ScanType QuickScan

# 3rd party 백신의 경우 해당 제조사 업데이트 절차 참조
```

---

## 4. 로그 관리

### W-40: 정책에 따른 시스템 로깅 설정 (중)
**점검:**
```powershell
# 감사 정책 확인
auditpol /get /category:*

# 주요 감사 정책 확인
auditpol /get /subcategory:"로그온","로그오프","계정 관리","정책 변경","권한 사용","디렉터리 서비스 액세스"
```
**조치:**
```powershell
# 감사 정책 설정 (KISA 권고 기준)
auditpol /set /subcategory:"계정 관리" /failure:enable
auditpol /set /subcategory:"계정 로그온 이벤트" /success:enable /failure:enable
auditpol /set /subcategory:"권한 사용" /success:enable /failure:enable
auditpol /set /subcategory:"디렉터리 서비스 액세스" /failure:enable
auditpol /set /subcategory:"로그온" /success:enable /failure:enable
auditpol /set /subcategory:"로그오프" /success:enable /failure:enable
auditpol /set /subcategory:"정책 변경" /success:enable /failure:enable

# GPO: 로컬 보안 정책 > 로컬 정책 > 감사 정책
```

---

### W-41: NTP 및 시각 동기화 설정 (중)
**점검:**
```powershell
# NTP 동기화 상태 확인
w32tm /query /status
w32tm /query /configuration

# NTP 서버 설정 확인
w32tm /dumpreg /subkey:parameters

# 시간 서비스 상태
Get-Service -Name "W32Time" | Select-Object Name, Status, StartType
```
**조치:**
```powershell
# Windows Time 서비스 활성화
Set-Service -Name "W32Time" -StartupType Automatic
Start-Service -Name "W32Time"

# 내부 NTP 서버와 동기화 설정
w32tm /config /syncfromflags:manual /manualpeerlist:"ntp.server.ip" /update
w32tm /resync

# 동기화 시간차 확인
w32tm /stripchart /dataonly /computer:"ntp.server.ip"
```

---

### W-42: 이벤트 로그 관리 설정 (하)
**점검:**
```powershell
# 이벤트 로그 설정 확인
Get-EventLog -List | Select-Object Log, MaximumKilobytes, OverflowAction, MinimumRetentionDays | Format-Table

# 레지스트리에서 직접 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\EventLog\Application" /v MaxSize
reg query "HKLM\SYSTEM\CurrentControlSet\Services\EventLog\Security" /v MaxSize
reg query "HKLM\SYSTEM\CurrentControlSet\Services\EventLog\System" /v MaxSize
```
**조치:**
```powershell
# 이벤트 로그 최대 크기 10240KB(10MB) 이상 설정
Limit-EventLog -LogName Application -MaximumSize 10240KB -OverflowAction OverwriteOlder -RetentionDays 90
Limit-EventLog -LogName Security -MaximumSize 10240KB -OverflowAction OverwriteOlder -RetentionDays 90
Limit-EventLog -LogName System -MaximumSize 10240KB -OverflowAction OverwriteOlder -RetentionDays 90

# 레지스트리 직접 설정 (바이트 단위: 10485760 = 10MB)
reg add "HKLM\SYSTEM\CurrentControlSet\Services\EventLog\Security" /v MaxSize /t REG_DWORD /d 10485760 /f
```

---

### W-43: 이벤트 로그 파일 접근 통제 설정 (중)
**점검:**
```powershell
# 시스템 로그 디렉터리 권한 확인
icacls "%SystemRoot%\System32\config"
# Everyone 권한이 있으면 취약

# IIS 로그 디렉터리 권한 확인
icacls "%SystemRoot%\System32\LogFiles" 2>$null
```
**조치:**
```powershell
# 로그 디렉터리에서 Everyone 권한 제거
icacls "C:\Windows\System32\config" /remove Everyone /T
icacls "C:\Windows\System32\LogFiles" /remove Everyone /T

# Administrators, SYSTEM만 접근 가능하도록 설정
```

---

## 5. 보안 관리

### W-44: 원격으로 액세스할 수 있는 레지스트리 경로 (상)
**점검:**
```powershell
# Remote Registry 서비스 상태 확인
Get-Service -Name "RemoteRegistry" | Select-Object Name, Status, StartType
```
**조치:**
```powershell
# Remote Registry 서비스 중지 및 비활성화
Stop-Service -Name "RemoteRegistry" -Force
Set-Service -Name "RemoteRegistry" -StartupType Disabled
```

---

### W-45: 백신 프로그램 설치 (상)
**점검:**
```powershell
# Windows Defender 설치 및 활성화 확인
Get-MpComputerStatus | Select-Object AMServiceEnabled, AntivirusEnabled, RealTimeProtectionEnabled

# 설치된 백신 프로그램 확인
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct -ErrorAction SilentlyContinue |
    Select-Object displayName, productState

# 프로그램 목록에서 백신 확인
Get-WmiObject -Class Win32_Product | Where-Object { $_.Name -match "antivirus|백신|V3|알약|Kaspersky|Norton|McAfee|Symantec" } |
    Select-Object Name, Version
```
**조치:**
```powershell
# Windows Defender 활성화 (비활성화된 경우)
Set-MpPreference -DisableRealtimeMonitoring $false

# 백신이 설치되지 않은 경우 조직 정책에 따라 백신 프로그램 설치
# Windows Defender는 Windows Server 2016 이상 기본 탑재
Install-WindowsFeature -Name Windows-Defender -ErrorAction SilentlyContinue
```

---

### W-46: SAM 파일 접근 통제 설정 (상)
**점검:**
```powershell
# SAM 파일 접근 권한 확인
icacls "C:\Windows\System32\config\SAM"
# Administrator, SYSTEM 외 다른 그룹/사용자 권한이 있으면 취약
```
**조치:**
```powershell
# SAM 파일 권한 설정 (Administrator, SYSTEM만 접근)
icacls "C:\Windows\System32\config\SAM" /inheritance:r
icacls "C:\Windows\System32\config\SAM" /grant "BUILTIN\Administrators:(F)"
icacls "C:\Windows\System32\config\SAM" /grant "NT AUTHORITY\SYSTEM:(F)"
```

---

### W-47: 화면보호기 설정 (하)
**점검:**
```powershell
# 화면보호기 설정 확인
reg query "HKCU\Control Panel\Desktop" /v ScreenSaveActive
reg query "HKCU\Control Panel\Desktop" /v ScreenSaveTimeOut
reg query "HKCU\Control Panel\Desktop" /v ScreenSaverIsSecure
# ScreenSaveActive=1, ScreenSaveTimeOut<=600(10분), ScreenSaverIsSecure=1 이면 양호
```
**조치:**
```powershell
# 화면보호기 활성화 (대기 시간 10분, 암호 사용)
reg add "HKCU\Control Panel\Desktop" /v ScreenSaveActive /t REG_SZ /d 1 /f
reg add "HKCU\Control Panel\Desktop" /v ScreenSaveTimeOut /t REG_SZ /d 600 /f
reg add "HKCU\Control Panel\Desktop" /v ScreenSaverIsSecure /t REG_SZ /d 1 /f
reg add "HKCU\Control Panel\Desktop" /v SCRNSAVE.EXE /t REG_SZ /d "C:\Windows\System32\scrnsave.scr" /f

# GPO 일괄 적용:
# 사용자 구성 > 관리 템플릿 > 제어판 > 개인 설정
# "화면 보호기 사용" = 사용
# "화면 보호기 시간 제한" = 600초
# "화면 보호기 암호로 보호" = 사용
```

---

### W-48: 로그온하지 않고 시스템 종료 허용 (상)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v ShutdownWithoutLogon
# 값이 0이면 양호
```
**조치:**
```powershell
# 로그온 없이 시스템 종료 차단
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v ShutdownWithoutLogon /t REG_SZ /d 0 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "시스템 종료: 로그온하지 않고 시스템 종료 허용" = 사용 안 함
```

---

### W-49: 원격 시스템에서 강제로 시스템 종료 (상)
**점검:**
```powershell
# 원격 시스템 종료 권한 확인
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "SeRemoteShutdownPrivilege" C:\secpol_tmp.cfg
# Administrators만 있으면 양호
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# GPO: 로컬 보안 정책 > 로컬 정책 > 사용자 권한 할당
# "원격 시스템에서 강제로 시스템 종료" 정책에 Administrators 외 다른 계정/그룹 제거
```

---

### W-50: 보안 감사를 로그할 수 없는 경우 즉시 시스템 종료 (상)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v CrashOnAuditFail
# 값이 0이면 양호 (사용 안 함), 1이면 취약

# 로컬 보안 정책 확인
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "CrashOnAuditFail" C:\secpol_tmp.cfg
Remove-Item C:\secpol_tmp.cfg -Force
```
**조치:**
```powershell
# 레지스트리 설정 (사용 안 함)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v CrashOnAuditFail /t REG_DWORD /d 0 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "감사: 보안 감사를 로그할 수 없는 경우 즉시 시스템 종료" = 사용 안 함
```

---

### W-51: SAM 계정과 공유의 익명 열거 허용 안 함 (상)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RestrictAnonymous
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RestrictAnonymousSAM
# RestrictAnonymous=1, RestrictAnonymousSAM=1 이면 양호
```
**조치:**
```powershell
# 레지스트리 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RestrictAnonymous /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RestrictAnonymousSAM /t REG_DWORD /d 1 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "네트워크 액세스: SAM 계정과 공유의 익명 열거 허용 안 함" = 사용
# "네트워크 액세스: SAM 계정의 익명 열거 허용 안 함" = 사용

# 참고: 방화벽에서 135~139(TCP/UDP) 포트 차단 권장
```

---

### W-52: Autologon 기능 제어 (상)
**점검:**
```powershell
# AutoAdminLogon 레지스트리 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon
# 값이 0이거나 존재하지 않으면 양호

# DefaultPassword 존재 여부 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword 2>$null
```
**조치:**
```powershell
# Autologon 비활성화
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 0 /f

# DefaultPassword 제거
reg delete "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /f 2>$null
```

---

### W-53: 이동식 미디어 포맷 및 꺼내기 허용 (상)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AllocateDASD
# 값이 0(Administrators만)이면 양호
```
**조치:**
```powershell
# Administrators에게만 이동식 미디어 포맷/꺼내기 허용
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AllocateDASD /t REG_SZ /d 0 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "장치: 이동식 미디어 포맷 및 꺼내기 허용" = Administrators
```

---

### W-54: DoS 공격 방어 레지스트리 설정 (중)
**점검:**
```powershell
# TCP/IP 스택 강화 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v SynAttackProtect 2>$null
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v EnableDeadGWDetect 2>$null
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v KeepAliveTime 2>$null
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v NoNameReleaseOnDemand 2>$null
# SynAttackProtect>=1, EnableDeadGWDetect=0, KeepAliveTime=300000, NoNameReleaseOnDemand=1 이면 양호
```
**조치:**
```powershell
# DoS 방어 레지스트리 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v SynAttackProtect /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v EnableDeadGWDetect /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v KeepAliveTime /t REG_DWORD /d 300000 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v NoNameReleaseOnDemand /t REG_DWORD /d 1 /f

# 주의: 잘못된 값 설정 시 OS 재설치 필요할 수 있음
```

---

### W-55: 사용자가 프린터 드라이버를 설치할 수 없게 함 (중)
**점검:**
```powershell
# 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Print\Providers\LanMan Print Services\Servers" /v AddPrinterDrivers 2>$null
# 값이 1이면 양호 (사용자 설치 차단)
```
**조치:**
```powershell
# 레지스트리 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Print\Providers\LanMan Print Services\Servers" /v AddPrinterDrivers /t REG_DWORD /d 1 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "장치: 사용자가 프린터 드라이버를 설치할 수 없게 함" = 사용
```

---

### W-56: SMB 세션 중단 관리 설정 (중)
**점검:**
```powershell
# SMB 세션 유휴 시간 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoDisconnect 2>$null
# 값이 15 이하이면 양호

# 로그온 시간 만료 시 연결 끊기 설정 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v EnableForcedLogoff 2>$null
# 값이 1이면 양호
```
**조치:**
```powershell
# SMB 유휴 세션 타임아웃 15분 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v AutoDisconnect /t REG_DWORD /d 15 /f

# 로그온 시간 만료 시 연결 끊기 활성화
reg add "HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" /v EnableForcedLogoff /t REG_DWORD /d 1 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "Microsoft 네트워크 서버: 로그온 시간이 만료되면 클라이언트 연결 끊기" = 사용
# "Microsoft 네트워크 서버: 세션 연결을 중단하기 전에 필요한 유휴 시간" = 15분
```

---

### W-57: 로그온 시 경고 메시지 설정 (하)
**점검:**
```powershell
# 로그온 경고 메시지 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v LegalNoticeCaption
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v LegalNoticeText
# 둘 다 값이 설정되어 있으면 양호
```
**조치:**
```powershell
# 로그온 경고 메시지 설정
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v LegalNoticeCaption /t REG_SZ /d "경고" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v LegalNoticeText /t REG_SZ /d "이 시스템은 인가된 사용자만 접근할 수 있습니다. 비인가 접근 시도 시 법적 처벌을 받을 수 있습니다." /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "대화형 로그온: 로그온 시도하는 사용자에 대한 메시지 제목" = 경고 제목
# "대화형 로그온: 로그온 시도하는 사용자에 대한 메시지 텍스트" = 경고 내용
```

---

### W-58: 사용자별 홈 디렉터리 권한 설정 (중)
**점검:**
```powershell
# 사용자 홈 디렉터리 권한 확인
Get-ChildItem "C:\Users" -Directory | ForEach-Object {
    $acl = Get-Acl $_.FullName
    $everyoneAccess = $acl.Access | Where-Object { $_.IdentityReference -like "*Everyone*" }
    if ($everyoneAccess) {
        [PSCustomObject]@{
            Directory = $_.Name
            Everyone = ($everyoneAccess | ForEach-Object { $_.FileSystemRights }) -join ", "
        }
    }
}
```
**조치:**
```powershell
# 홈 디렉터리에서 Everyone 권한 제거 (All Users, Default User 제외)
Get-ChildItem "C:\Users" -Directory | Where-Object {
    $_.Name -notin @("All Users","Default User","Default","Public")
} | ForEach-Object {
    icacls $_.FullName /remove Everyone /T
}
```

---

### W-59: LAN Manager 인증 수준 (중)
**점검:**
```powershell
# LAN Manager 인증 수준 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LmCompatibilityLevel
# 값이 5이면 양호 (NTLMv2 응답만 보냄, LM 및 NTLM 거부)
# 최소 3 이상 권장
```
**조치:**
```powershell
# NTLMv2 응답만 보내도록 설정
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LmCompatibilityLevel /t REG_DWORD /d 5 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "네트워크 보안: LAN Manager 인증 수준" = "NTLMv2 응답만 보내기/LM 및 NTLM 거부"
```

---

### W-60: 보안 채널 데이터 디지털 암호화 또는 서명 (중)
**점검:**
```powershell
# 보안 채널 관련 레지스트리 확인
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters" /v RequireSignOrSeal 2>$null
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters" /v SealSecureChannel 2>$null
reg query "HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters" /v SignSecureChannel 2>$null
# 세 값 모두 1이면 양호
```
**조치:**
```powershell
# 보안 채널 데이터 암호화/서명 활성화
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters" /v RequireSignOrSeal /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters" /v SealSecureChannel /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters" /v SignSecureChannel /t REG_DWORD /d 1 /f

# GPO: 로컬 보안 정책 > 로컬 정책 > 보안 옵션
# "도메인 구성원: 보안 채널 데이터를 디지털 암호화 또는 서명(항상)" = 사용
# "도메인 구성원: 보안 채널 데이터를 디지털 암호화(가능한 경우)" = 사용
# "도메인 구성원: 보안 채널 데이터 디지털 서명(가능한 경우)" = 사용
```

---

### W-61: 파일 및 디렉토리 보호 (중)
**점검:**
```powershell
# 파일 시스템 유형 확인
Get-Volume | Select-Object DriveLetter, FileSystemType, Size | Format-Table

# CMD 확인
fsutil fsinfo volumeinfo C:
```
**조치:**
```powershell
# FAT 파일 시스템을 NTFS로 변환
# convert <드라이브명>: /fs:ntfs
# 예: convert F: /fs:ntfs

# 주의: 변환은 비가역적이며 초기 설치 시 NTFS 선택 권장
# 기존 FAT에서 변환 시 Default ACL이 적용되지 않을 수 있음
```

---

### W-62: 시작 프로그램 목록 분석 (중)
**점검:**
```powershell
# 시작 프로그램 레지스트리 확인
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce" 2>$null

# 시작 폴더 확인
Get-ChildItem "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Startup" -ErrorAction SilentlyContinue
Get-ChildItem "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup" -ErrorAction SilentlyContinue

# WMI 시작 프로그램 목록
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location | Format-Table -AutoSize
```
**조치:**
```powershell
# 불필요한 시작 프로그램 제거 (레지스트리)
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "<프로그램명>" /f
reg delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "<프로그램명>" /f

# msconfig 실행 (Windows 2008 이하)
# 시작 프로그램 탭에서 불필요한 항목 체크 해제
```

---

### W-63: 도메인 컨트롤러-사용자의 시간 동기화 (중)
**점검:**
```powershell
# Kerberos 최대 허용 오차 확인 (도메인 컨트롤러)
secedit /export /cfg C:\secpol_tmp.cfg
Select-String "MaxClockSkew" C:\secpol_tmp.cfg
# 값이 5 이하이면 양호
Remove-Item C:\secpol_tmp.cfg -Force

# 현재 시간 동기화 상태
w32tm /query /status
```
**조치:**
```powershell
# GPO: 로컬 보안 정책 > 계정 정책 > Kerberos 정책
# "컴퓨터 시계 동기화 최대 허용 오차" = 5분

# 시간 동기화 강제 수행
w32tm /resync /force
```

---

### W-64: 윈도우 방화벽 설정 (중)
**점검:**
```powershell
# Windows 방화벽 프로필 상태 확인
Get-NetFirewallProfile | Select-Object Name, Enabled | Format-Table

# 방화벽 규칙 요약
Get-NetFirewallProfile | ForEach-Object {
    $profile = $_.Name
    $enabled = $_.Enabled
    [PSCustomObject]@{
        Profile = $profile
        Enabled = $enabled
        InboundDefault = $_.DefaultInboundAction
        OutboundDefault = $_.DefaultOutboundAction
    }
} | Format-Table

# netsh 명령
netsh advfirewall show allprofiles
```
**조치:**
```powershell
# Windows 방화벽 활성화 (모든 프로필)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# netsh 명령
netsh advfirewall set allprofiles state on

# GUI: 제어판 > Windows Defender 방화벽 > 설정 또는 해제
# 모든 프로필에 대해 "사용" 설정
```
