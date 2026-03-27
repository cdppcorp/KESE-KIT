---
name: fix
description: CII 시스템에서 발견된 보안 취약점을 자동 수정합니다. Unix/Linux, Windows, 웹 서버, 데이터베이스용 하드닝 스크립트를 생성합니다. KISA 가이드라인에 따른 보안 설정을 적용합니다. "취약점 수정", "시스템 보안", "보안 수정 적용", "서버 하드닝", "KISA 하드닝" 시 사용하세요.
---

# KESE 취약점 자동 수정

CII 보안 하드닝 전문가로서 취약점 분석 결과를 기반으로 적절한 수정을 생성하고 적용합니다. KISA 가이드라인을 따르는 플랫폼별 하드닝 스크립트를 생성합니다.

## 실행 흐름

1. `reports/kese/`에서 이전 평가 결과 읽기 (있는 경우)
2. 이전 평가가 없으면 사용자에게 대상 플랫폼 확인
3. 식별된 플랫폼에 대한 하드닝 스크립트 생성
4. 단계별 조치 가이드 제공
5. 스크립트를 `scripts/kese-hardening/`에 저장

## 출력 구조

```
scripts/kese-hardening/
├── unix/
│   ├── account-hardening.sh
│   ├── file-permissions.sh
│   ├── service-hardening.sh
│   └── full-hardening.sh
├── windows/
│   ├── account-hardening.ps1
│   ├── service-hardening.ps1
│   └── full-hardening.ps1
├── web/
│   ├── apache-hardening.conf
│   ├── nginx-hardening.conf
│   └── tomcat-hardening.xml
├── database/
│   ├── mysql-hardening.sql
│   ├── postgresql-hardening.sql
│   └── oracle-hardening.sql
└── README.md
```

---

## Unix/Linux 하드닝 스크립트

### 계정 하드닝 (U-01 ~ U-09)

```bash
#!/bin/bash
# KESE Unix 계정 하드닝 스크립트
# KISA 주요정보통신기반시설 취약점 분석평가 가이드라인 기반

echo "=== KESE 계정 하드닝 ==="

# U-01: root 원격 접속 제한
echo "[U-01] SSH root 로그인 제한 설정 중..."
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config 2>/dev/null

# U-02: 패스워드 복잡성
echo "[U-02] 패스워드 복잡성 설정 중..."
cat > /etc/security/pwquality.conf << 'EOF'
minlen = 8
minclass = 3
maxrepeat = 3
lcredit = -1
ucredit = -1
dcredit = -1
ocredit = -1
EOF

# U-03: 계정 잠금 정책
echo "[U-03] 계정 잠금 설정 중..."
cat >> /etc/pam.d/common-auth << 'EOF'
auth required pam_tally2.so deny=5 unlock_time=1800
EOF

# U-04: 패스워드 에이징
echo "[U-04] 패스워드 에이징 정책 설정 중..."
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   1/' /etc/login.defs
sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE   7/' /etc/login.defs

# U-05: Shadow 파일 권한
echo "[U-05] shadow 파일 권한 설정 중..."
chmod 400 /etc/shadow
chown root:root /etc/shadow

# U-06: 세션 타임아웃
echo "[U-06] 세션 타임아웃 설정 중..."
echo "TMOUT=300" >> /etc/profile
echo "readonly TMOUT" >> /etc/profile
echo "export TMOUT" >> /etc/profile

# U-07: 불필요한 계정 제거
echo "[U-07] 불필요한 계정 검토 중..."
# 삭제하지 않고 잠금 - 수동 검토 필요
for user in games gopher ftp; do
    if id "$user" &>/dev/null; then
        usermod -L $user 2>/dev/null
        echo "  잠금된 계정: $user"
    fi
done

echo "=== 계정 하드닝 완료 ==="
```

### 파일 권한 하드닝 (U-10 ~ U-24)

```bash
#!/bin/bash
# KESE Unix 파일 권한 하드닝 스크립트

echo "=== KESE 파일 권한 하드닝 ==="

# U-10: SUID/SGID 파일 점검
echo "[U-10] SUID/SGID 파일 검토 중..."
find / -perm -4000 -o -perm -2000 2>/dev/null > /tmp/suid_sgid_files.txt
echo "  $(wc -l < /tmp/suid_sgid_files.txt)개의 SUID/SGID 파일 발견"
echo "  불필요한 권한은 /tmp/suid_sgid_files.txt를 검토하세요"

# U-11: World-writable 파일
echo "[U-11] World-writable 권한 제거 중..."
find / -type f -perm -002 -exec chmod o-w {} \; 2>/dev/null

# U-12: Umask 설정
echo "[U-12] 기본 umask 설정 중..."
echo "umask 022" >> /etc/profile
echo "umask 022" >> /etc/bashrc

# U-13: 중요 파일 권한
echo "[U-13] 중요 파일 권한 설정 중..."
chmod 644 /etc/passwd
chmod 400 /etc/shadow
chmod 644 /etc/group
chmod 600 /etc/hosts.allow
chmod 600 /etc/hosts.deny

# U-14: 홈 디렉터리 권한
echo "[U-14] 홈 디렉터리 보안 설정 중..."
for dir in /home/*; do
    if [ -d "$dir" ]; then
        chmod 700 "$dir"
    fi
done

# U-15: /tmp 디렉터리 sticky bit
echo "[U-15] /tmp sticky bit 설정 중..."
chmod 1777 /tmp
chmod 1777 /var/tmp

echo "=== 파일 권한 하드닝 완료 ==="
```

### 서비스 하드닝 (U-25 ~ U-43)

```bash
#!/bin/bash
# KESE Unix 서비스 하드닝 스크립트

echo "=== KESE 서비스 하드닝 ==="

# U-25~U-30: 불필요한 서비스 비활성화
UNNECESSARY_SERVICES=(
    "telnet"
    "rsh"
    "rlogin"
    "rexec"
    "finger"
    "tftp"
    "talk"
    "ntalk"
    "chargen"
    "daytime"
    "echo"
    "discard"
    "nfs"
    "rpc.cmsd"
    "rpc.ttdbserverd"
)

echo "[U-25~U-30] 불필요한 서비스 비활성화 중..."
for service in "${UNNECESSARY_SERVICES[@]}"; do
    systemctl disable $service 2>/dev/null
    systemctl stop $service 2>/dev/null
    echo "  비활성화됨: $service"
done

# U-31: SSH 설정 하드닝
echo "[U-31] SSH 설정 하드닝 중..."
cat >> /etc/ssh/sshd_config << 'EOF'
# KESE SSH 하드닝
Protocol 2
PermitRootLogin no
PasswordAuthentication yes
PermitEmptyPasswords no
MaxAuthTries 5
ClientAliveInterval 300
ClientAliveCountMax 0
X11Forwarding no
AllowTcpForwarding no
EOF

# U-32: FTP 설정 (필요 시)
echo "[U-32] FTP 설정 하드닝 중..."
if [ -f /etc/vsftpd.conf ]; then
    sed -i 's/^anonymous_enable=.*/anonymous_enable=NO/' /etc/vsftpd.conf
    echo "ftpd_banner=인가된 접근만 허용됩니다" >> /etc/vsftpd.conf
fi

# U-33: Apache 하드닝 (있는 경우)
echo "[U-33] Apache 설정 하드닝 중..."
if [ -d /etc/apache2 ] || [ -d /etc/httpd ]; then
    cat > /etc/apache2/conf-available/security-kese.conf << 'EOF'
ServerTokens Prod
ServerSignature Off
TraceEnable Off
Header always set X-Frame-Options SAMEORIGIN
Header always set X-Content-Type-Options nosniff
Header always set X-XSS-Protection "1; mode=block"
EOF
fi

# 서비스 재시작
echo "SSH 서비스 재시작 중..."
systemctl restart sshd

echo "=== 서비스 하드닝 완료 ==="
```

---

## Windows 하드닝 스크립트

### 계정 하드닝 (W-01 ~ W-15)

```powershell
# KESE Windows 계정 하드닝 스크립트
# KISA 주요정보통신기반시설 취약점 분석평가 가이드라인 기반

Write-Host "=== KESE Windows 계정 하드닝 ===" -ForegroundColor Green

# W-01: Administrator 계정명 변경
Write-Host "[W-01] Administrator 계정명 변경 중..."
$admin = Get-LocalUser | Where-Object {$_.SID -like "*-500"}
if ($admin.Name -eq "Administrator") {
    Rename-LocalUser -Name "Administrator" -NewName "LocalAdmin"
    Write-Host "  Administrator가 LocalAdmin으로 변경됨"
}

# W-02: Guest 계정 비활성화
Write-Host "[W-02] Guest 계정 비활성화 중..."
Disable-LocalUser -Name "Guest" -ErrorAction SilentlyContinue
Write-Host "  Guest 계정 비활성화됨"

# W-03~W-04: 패스워드 정책
Write-Host "[W-03~W-04] 패스워드 정책 설정 중..."
net accounts /minpwlen:8 /maxpwage:90 /minpwage:1 /uniquepw:5

# W-05: 계정 잠금 정책
Write-Host "[W-05] 계정 잠금 설정 중..."
net accounts /lockoutthreshold:5 /lockoutduration:30 /lockoutwindow:30

# W-06: 세션 타임아웃
Write-Host "[W-06] 세션 타임아웃 설정 중..."
# 화면보호기 타임아웃 10분, 암호 필요
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name ScreenSaveTimeOut -Value 600
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name ScreenSaverIsSecure -Value 1

# W-07: 불필요한 계정 제거
Write-Host "[W-07] 불필요한 계정 검토 중..."
$unusedAccounts = Get-LocalUser | Where-Object {$_.Enabled -eq $true -and $_.LastLogon -lt (Get-Date).AddDays(-90)}
foreach ($account in $unusedAccounts) {
    Write-Host "  계정 검토 필요: $($account.Name) - 마지막 로그온: $($account.LastLogon)"
}

Write-Host "=== 계정 하드닝 완료 ===" -ForegroundColor Green
```

### 서비스 하드닝 (W-16 ~ W-35)

```powershell
# KESE Windows 서비스 하드닝 스크립트

Write-Host "=== KESE Windows 서비스 하드닝 ===" -ForegroundColor Green

# W-16~W-20: 불필요한 서비스 비활성화
$unnecessaryServices = @(
    "RemoteRegistry",
    "Telnet",
    "TFTP",
    "SNMPTRAP",
    "WinRM"
)

Write-Host "[W-16~W-20] 불필요한 서비스 비활성화 중..."
foreach ($service in $unnecessaryServices) {
    $svc = Get-Service -Name $service -ErrorAction SilentlyContinue
    if ($svc) {
        Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
        Set-Service -Name $service -StartupType Disabled
        Write-Host "  비활성화됨: $service"
    }
}

# W-21: 기본 공유 비활성화
Write-Host "[W-21] 기본 공유 설정 중..."
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -Name "AutoShareServer" -Value 0
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" -Name "AutoShareWks" -Value 0

# W-22~W-25: 방화벽 설정
Write-Host "[W-22~W-25] Windows 방화벽 설정 중..."
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
Set-NetFirewallProfile -DefaultInboundAction Block -DefaultOutboundAction Allow

# W-26: 원격 데스크톱 하드닝
Write-Host "[W-26] 원격 데스크톱 하드닝 중..."
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "UserAuthentication" -Value 1

# W-27~W-30: IIS 하드닝 (설치된 경우)
if (Get-Service -Name W3SVC -ErrorAction SilentlyContinue) {
    Write-Host "[W-27~W-30] IIS 하드닝 중..."
    Import-Module WebAdministration -ErrorAction SilentlyContinue

    # 서버 헤더 제거
    Set-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering" -Name "removeServerHeader" -Value "True"

    # 디렉터리 브라우징 비활성화
    Set-WebConfigurationProperty -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "False"
}

Write-Host "=== 서비스 하드닝 완료 ===" -ForegroundColor Green
```

---

## 웹 서버 하드닝

### Apache 설정

```apache
# KESE Apache 하드닝 설정
# httpd.conf 또는 apache2.conf에 포함

# 서버 버전 숨김
ServerTokens Prod
ServerSignature Off

# TRACE 메서드 비활성화
TraceEnable Off

# 보안 헤더
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set Content-Security-Policy "default-src 'self'"

# 디렉터리 리스팅 비활성화
<Directory />
    Options -Indexes
    AllowOverride None
    Require all denied
</Directory>

# HTTP 메서드 제한
<Directory "/var/www/html">
    <LimitExcept GET POST HEAD>
        Require all denied
    </LimitExcept>
</Directory>

# SSL/TLS 설정
SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder on
```

### Nginx 설정

```nginx
# KESE Nginx 하드닝 설정

# 서버 버전 숨김
server_tokens off;

# 보안 헤더
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# 디렉터리 리스팅 비활성화
autoindex off;

# 요청 메서드 제한
if ($request_method !~ ^(GET|HEAD|POST)$) {
    return 405;
}

# SSL/TLS 설정
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers on;

# 요청 본문 크기 제한
client_max_body_size 10m;

# 요청 제한
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
```

---

## 데이터베이스 하드닝

### MySQL/MariaDB

```sql
-- KESE MySQL 하드닝 스크립트

-- D-01: 익명 사용자 제거
DELETE FROM mysql.user WHERE User='';

-- D-02: 원격 root 접근 제거
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');

-- D-03: test 데이터베이스 제거
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';

-- D-04: root 패스워드 설정
-- ALTER USER 'root'@'localhost' IDENTIFIED BY 'StrongPassword123!';

-- D-05: 원격 연결 SSL 필수
-- 민감한 사용자에 대해 REQUIRE SSL

-- 변경사항 적용
FLUSH PRIVILEGES;
```

### PostgreSQL

```sql
-- KESE PostgreSQL 하드닝 스크립트

-- D-01: public 권한 회수
REVOKE ALL ON DATABASE postgres FROM PUBLIC;

-- D-02: 새 데이터베이스 기본 권한 제거
ALTER DEFAULT PRIVILEGES REVOKE ALL ON TABLES FROM PUBLIC;

-- D-03: 로깅 활성화
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;

-- D-04: 패스워드 암호화 설정
ALTER SYSTEM SET password_encryption = 'scram-sha-256';

-- 변경사항 적용
SELECT pg_reload_conf();
```

---

## 수정 적용 시 주의사항

- 수정 전 항상 설정 백업
- 비운영 환경에서 먼저 테스트
- 각 스크립트를 검토하고 환경에 맞게 커스터마이징
- 일부 수정은 서비스 재시작 필요
- 컴플라이언스 감사를 위해 모든 변경사항 문서화
