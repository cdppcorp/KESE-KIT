# Windows 서버 취약점 분석·평가 항목

> KISA 주요정보통신기반시설 기술적 취약점 분석·평가 방법 상세가이드 (2026)

## 1. 계정 관리 (14항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| W-01 | Administrator 계정 이름 변경 등 보안성 강화 | 상 |
| W-02 | Guest 계정 비활성화 | 상 |
| W-03 | 불필요한 계정 제거 | 상 |
| W-04 | 계정 잠금 임계값 설정 | 상 |
| W-05 | 해독 가능한 암호화를 사용하여 암호 저장 해제 | 상 |
| W-06 | 관리자 그룹에 최소한의 사용자 포함 | 상 |
| W-07 | Everyone 사용 권한을 익명 사용자에게 적용 | 중 |
| W-08 | 계정 잠금 기간 설정 | 중 |
| W-09 | 비밀번호 관리정책 설정 | 상 |
| W-10 | 마지막 사용자 이름 표시 안 함 | 중 |
| W-11 | 로컬 로그온 허용 | 중 |
| W-12 | 익명 SID/이름 변환 허용 해제 | 중 |
| W-13 | 콘솔 로그온 시 로컬 계정에서 빈 암호 사용 제한 | 중 |
| W-14 | 원격터미널 접속 가능한 사용자 그룹 제한 | 중 |

### 주요 점검 명령어
```powershell
# W-01: Administrator 계정명
Get-LocalUser | Where-Object {$_.SID -like "*-500"} | Select Name

# W-02: Guest 비활성화
Get-LocalUser -Name "Guest" | Select Enabled

# W-04: 계정 잠금
net accounts

# W-06: 관리자 그룹
net localgroup Administrators

# W-09: 패스워드 정책
net accounts
```

---

## 2. 서비스 관리 (23항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| W-15 | 사용자 개인키 사용 시 암호 입력 | 상 |
| W-16 | 공유 권한 및 사용자 그룹 설정 | 상 |
| W-17 | 하드디스크 기본 공유 제거 | 상 |
| W-18 | 불필요한 서비스 제거 | 상 |
| W-19 | 불필요한 IIS 서비스 구동 점검 | 상 |
| W-20 | NetBIOS 바인딩 서비스 구동 점검 | 상 |
| W-21 | 암호화되지 않는 FTP 서비스 비활성화 | 상 |
| W-22 | FTP 디렉토리 접근권한 설정 | 상 |
| W-23 | 공유 서비스에 대한 익명 접근 제한 설정 | 상 |
| W-24 | FTP 접근 제어 설정 | 상 |
| W-25 | DNS Zone Transfer 설정 | 상 |
| W-26 | RDS(Remote Data Services) 제거 | 상 |
| W-27 | 최신 Windows OS Build 버전 적용 | 상 |
| W-28 | 터미널 서비스 암호화 수준 설정 | 중 |
| W-29 | 불필요한 SNMP 서비스 구동 점검 | 중 |
| W-30 | SNMP Community String 복잡성 설정 | 중 |
| W-31 | SNMP Access Control 설정 | 중 |
| W-32 | DNS 서비스 구동 점검 | 중 |
| W-33 | HTTP/FTP/SMTP 배너 차단 | 하 |
| W-34 | Telnet 서비스 비활성화 | 중 |
| W-35 | 불필요한 ODBC/OLE-DB 데이터 소스와 드라이브 제거 | 중 |
| W-36 | 원격터미널 접속 타임아웃 설정 | 중 |
| W-37 | 예약된 작업에 의심스러운 명령이 등록되어 있는지 점검 | 중 |

### 주요 점검 명령어
```powershell
# W-17: 기본 공유
net share
Get-SmbShare

# W-18: 서비스 목록
Get-Service | Where-Object {$_.Status -eq "Running"}

# W-19: IIS
Get-Service W3SVC

# W-29~31: SNMP
Get-Service SNMP
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities"
```

---

## 3. 패치 관리 (2항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| W-38 | 주기적 보안 패치 및 벤더 권고사항 적용 | 상 |
| W-39 | 백신 프로그램 업데이트 | 상 |

```powershell
# W-38: 패치 현황
Get-HotFix | Sort-Object InstalledOn -Descending | Select -First 10
systeminfo | findstr "KB"

# W-39: 백신
Get-MpComputerStatus  # Windows Defender
```

---

## 4. 로그 관리 (4항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| W-40 | 정책에 따른 시스템 로깅 설정 | 중 |
| W-41 | NTP 및 시각 동기화 설정 | 중 |
| W-42 | 이벤트 로그 관리 설정 | 하 |
| W-43 | 이벤트 로그 파일 접근 통제 설정 | 중 |

```powershell
# W-40: 감사 정책
auditpol /get /category:*

# W-41: NTP
w32tm /query /status

# W-42: 이벤트 로그 설정
Get-EventLog -List
```

---

## 5. 보안 관리 (21항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| W-44 | 원격으로 액세스할 수 있는 레지스트리 경로 | 상 |
| W-45 | 백신 프로그램 설치 | 상 |
| W-46 | SAM 파일 접근 통제 설정 | 상 |
| W-47 | 화면보호기 설정 | 상 |
| W-48 | 로그온하지 않고 시스템 종료 허용 | 상 |
| W-49 | 원격 시스템에서 강제로 시스템 종료 | 상 |
| W-50 | 보안 감사를 로그할 수 없는 경우 즉시 시스템 종료 | 상 |
| W-51 | SAM 계정과 공유의 익명 열거 허용 안 함 | 상 |
| W-52 | Autologon 기능 제어 | 상 |
| W-53 | 이동식 미디어 포맷 및 꺼내기 허용 | 상 |
| W-54 | DoS 공격 방어 레지스트리 설정 | 중 |
| W-55 | 사용자가 프린터 드라이버를 설치할 수 없게 함 | 중 |
| W-56 | SMB 세션 중단 관리 설정 | 중 |
| W-57 | 로그온 시 경고 메시지 설정 | 하 |
| W-58 | 사용자별 홈 디렉터리 권한 설정 | 중 |
| W-59 | LAN Manager 인증 수준 | 중 |
| W-60 | 보안 채널 데이터 디지털 암호화 또는 서명 | 중 |
| W-61 | 파일 및 디렉토리 보호 | 중 |
| W-62 | 시작프로그램 목록 분석 | 중 |
| W-63 | 도메인 컨트롤러-사용자의 시간 동기화 | 중 |
| W-64 | 윈도우 방화벽 설정 | 중 |

### 주요 점검 명령어
```powershell
# W-44: 원격 레지스트리
Get-Service RemoteRegistry | Select Status

# W-46: SAM 파일
icacls C:\Windows\System32\config\SAM

# W-47: 화면보호기
reg query "HKCU\Control Panel\Desktop" /v ScreenSaveTimeOut
reg query "HKCU\Control Panel\Desktop" /v ScreenSaverIsSecure

# W-52: Autologon
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon

# W-59: LAN Manager
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LmCompatibilityLevel

# W-64: 방화벽
Get-NetFirewallProfile | Select Name, Enabled
```

---

## 통계

| 분류 | 항목 수 | 상 | 중 | 하 |
|------|:------:|:--:|:--:|:--:|
| 계정 관리 | 14 | 7 | 7 | 0 |
| 서비스 관리 | 23 | 13 | 9 | 1 |
| 패치 관리 | 2 | 2 | 0 | 0 |
| 로그 관리 | 4 | 0 | 3 | 1 |
| 보안 관리 | 21 | 10 | 10 | 1 |
| **합계** | **64** | **32** | **29** | **3** |
