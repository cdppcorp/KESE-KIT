# 3장. Unix/Linux 서버 점검

> Part II. 기술적 취약점 점검

---

## 개요

Unix/Linux 서버는 주요정보통신기반시설의 핵심 인프라입니다. 이 장에서는 68개의 점검 항목(U-01 ~ U-68)을 5개 영역으로 나누어 설명합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                Unix/Linux 서버 취약점 점검 영역                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │   계정 관리  │   │  파일/디렉  │   │  서비스     │          │
│   │  U-01~U-13  │   │  터리 관리   │   │   관리      │          │
│   │   (13개)    │   │  U-14~U-33  │   │  U-34~U-63  │          │
│   │             │   │   (20개)    │   │   (30개)    │          │
│   │ • root 접속 │   │ • 권한 설정 │   │ • 불필요    │          │
│   │ • 비밀번호  │   │ • SUID/SGID│   │   서비스    │          │
│   │ • 계정 잠금 │   │ • 소유자   │   │ • SNMP 보안 │          │
│   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘          │
│          │                 │                 │                  │
│          └────────────────┬┴─────────────────┘                  │
│                           │                                      │
│          ┌────────────────┴────────────────┐                    │
│          ▼                                 ▼                    │
│   ┌─────────────┐                   ┌─────────────┐            │
│   │  패치 관리   │                   │  로그 관리   │            │
│   │    U-64     │                   │  U-65~U-68  │            │
│   │   (1개)     │                   │   (4개)     │            │
│   │             │                   │             │            │
│   │ • 보안 패치 │                   │ • 로그 설정 │            │
│   │   적용      │                   │ • 로그 보관 │            │
│   └─────────────┘                   └─────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 영역 | 항목 | 항목 수 |
|------|------|:------:|
| 계정 관리 | U-01 ~ U-13 | 13 |
| 파일 및 디렉터리 관리 | U-14 ~ U-33 | 20 |
| 서비스 관리 | U-34 ~ U-63 | 30 |
| 패치 관리 | U-64 | 1 |
| 로그 관리 | U-65 ~ U-68 | 4 |

---

## 3-1. 계정 관리 (U-01 ~ U-13)

계정 관리는 서버 보안의 첫 번째 방어선입니다. 부적절한 계정 관리는 비인가 접근의 주요 원인이 됩니다.

### U-01. root 계정 원격 접속 제한

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | root 계정의 직접 원격 접속을 제한하여 비인가 접근 방지 |
| **판단 기준** | 양호: root 직접 접속 차단 / 취약: root 직접 접속 허용 |

#### 점검 방법

```bash
# SSH 설정 확인
cat /etc/ssh/sshd_config | grep -i "PermitRootLogin"

# Telnet 사용 여부 확인 (사용하지 않는 것이 권장)
cat /etc/securetty
```

#### 조치 방법

```bash
# /etc/ssh/sshd_config 수정
PermitRootLogin no

# SSH 서비스 재시작
systemctl restart sshd
```

> **TIP**
> root 접속이 필요한 경우, 일반 계정으로 접속 후 `su -` 또는 `sudo`를 사용하세요.

---

### U-02. 비밀번호 관리정책 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 비밀번호 복잡성 및 주기적 변경 강제 |
| **판단 기준** | 양호: 정책 설정됨 / 취약: 정책 미설정 |

#### 점검 방법

```bash
# 비밀번호 정책 확인
cat /etc/login.defs | grep -E "PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_MIN_LEN|PASS_WARN_AGE"

# PAM 설정 확인 (RHEL/CentOS)
cat /etc/pam.d/system-auth | grep pam_pwquality
```

#### 권장 설정값

| 항목 | 권장값 | 설명 |
|------|:------:|------|
| PASS_MAX_DAYS | 90 | 최대 사용 기간 |
| PASS_MIN_DAYS | 1 | 최소 사용 기간 |
| PASS_MIN_LEN | 8 | 최소 길이 |
| PASS_WARN_AGE | 7 | 만료 경고 일수 |

#### 조치 방법

```bash
# /etc/login.defs 수정
PASS_MAX_DAYS   90
PASS_MIN_DAYS   1
PASS_MIN_LEN    8
PASS_WARN_AGE   7
```

---

### U-03. 계정 잠금 임계값 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 무차별 대입 공격(Brute Force) 방지 |
| **판단 기준** | 양호: 5회 이하 설정 / 취약: 미설정 또는 초과 |

#### 점검 방법

```bash
# PAM 설정 확인
cat /etc/pam.d/system-auth | grep pam_tally2
# 또는
cat /etc/pam.d/system-auth | grep pam_faillock
```

#### 조치 방법

```bash
# /etc/pam.d/system-auth (RHEL 7 이상)
auth required pam_faillock.so preauth silent deny=5 unlock_time=600
auth required pam_faillock.so authfail deny=5 unlock_time=600
```

> **WARNING**
> 계정 잠금 설정 시 root 계정이 잠기지 않도록 `even_deny_root` 옵션 사용에 주의하세요.

---

### U-04. 비밀번호 파일 보호

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | Shadow 패스워드 사용으로 암호 해시 보호 |
| **판단 기준** | 양호: shadow 사용 / 취약: passwd에 암호 저장 |

#### 점검 방법

```bash
# /etc/passwd에서 두 번째 필드 확인
cat /etc/passwd | awk -F: '{print $1":"$2}'
# 'x'로 표시되면 shadow 사용 중
```

---

### U-05. root 이외의 UID가 '0' 금지

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | root 권한을 가진 비인가 계정 탐지 |
| **판단 기준** | 양호: root만 UID 0 / 취약: 다른 계정이 UID 0 |

#### 점검 방법

```bash
# UID가 0인 계정 확인
awk -F: '$3==0 {print $1}' /etc/passwd
```

#### 조치 방법

root 외에 UID가 0인 계정이 있다면 삭제하거나 UID를 변경합니다.

---

### U-06. 사용자 계정 su 기능 제한

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | su 명령어 사용을 특정 그룹으로 제한 |
| **판단 기준** | 양호: wheel 그룹만 su 사용 가능 / 취약: 제한 없음 |

#### 점검 방법

```bash
# PAM 설정 확인
cat /etc/pam.d/su | grep pam_wheel
```

#### 조치 방법

```bash
# /etc/pam.d/su 수정 (주석 해제)
auth required pam_wheel.so use_uid

# wheel 그룹에 사용자 추가
usermod -aG wheel [사용자명]
```

---

### U-07 ~ U-13. 기타 계정 관리 항목

| 코드 | 항목 | 중요도 | 핵심 점검 |
|------|------|:------:|----------|
| U-07 | 불필요한 계정 제거 | 하 | `/etc/passwd` 미사용 계정 |
| U-08 | 관리자 그룹에 최소한의 계정 포함 | 중 | wheel/root 그룹 구성원 |
| U-09 | 계정이 존재하지 않는 GID 금지 | 하 | `/etc/group` 정합성 |
| U-10 | 동일한 UID 금지 | 중 | 중복 UID 확인 |
| U-11 | 사용자 Shell 점검 | 하 | 불필요 계정 `/sbin/nologin` |
| U-12 | 세션 종료 시간 설정 | 하 | TMOUT 환경변수 |
| U-13 | 안전한 비밀번호 암호화 알고리즘 | 중 | SHA-512 사용 권장 |

---

## 3-2. 파일 및 디렉터리 관리 (U-14 ~ U-33)

파일 권한 관리는 시스템 무결성 보호의 핵심입니다.

### U-14. root 홈, 패스 디렉터리 권한 및 패스 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | PATH 환경변수에 '.' 포함 방지 |
| **판단 기준** | 양호: PATH에 '.' 미포함 / 취약: '.' 포함 |

#### 점검 방법

```bash
# PATH 환경변수 확인
echo $PATH | grep -E "^\.|:\.|:$"

# root 프로파일 확인
cat /root/.bash_profile | grep PATH
```

> **WARNING**
> PATH에 현재 디렉터리(`.`)가 포함되면 악성 프로그램 실행 위험이 있습니다.

---

### U-16 ~ U-22. 주요 시스템 파일 권한

| 코드 | 대상 파일 | 권장 권한 | 소유자 |
|------|----------|:--------:|:------:|
| U-16 | /etc/passwd | 644 | root |
| U-18 | /etc/shadow | 400 | root |
| U-19 | /etc/hosts | 600 | root |
| U-20 | /etc/(x)inetd.conf | 600 | root |
| U-21 | /etc/(r)syslog.conf | 640 | root |
| U-22 | /etc/services | 644 | root |

#### 일괄 점검 스크립트

```bash
#!/bin/bash
# 주요 파일 권한 점검

FILES=(
    "/etc/passwd:644:root"
    "/etc/shadow:400:root"
    "/etc/hosts:600:root"
    "/etc/services:644:root"
)

for item in "${FILES[@]}"; do
    IFS=':' read -r file perm owner <<< "$item"
    if [ -f "$file" ]; then
        actual_perm=$(stat -c "%a" "$file")
        actual_owner=$(stat -c "%U" "$file")
        if [ "$actual_perm" -le "$perm" ] && [ "$actual_owner" == "$owner" ]; then
            echo "[양호] $file (권한: $actual_perm, 소유자: $actual_owner)"
        else
            echo "[취약] $file (권한: $actual_perm, 소유자: $actual_owner)"
        fi
    fi
done
```

---

### U-23. SUID, SGID, Sticky bit 설정 파일 점검

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 불필요한 SUID/SGID 파일로 인한 권한 상승 방지 |

#### 점검 방법

```bash
# SUID 파일 검색
find / -perm -4000 -type f 2>/dev/null

# SGID 파일 검색
find / -perm -2000 -type f 2>/dev/null

# SUID + SGID 동시 검색
find / -perm -6000 -type f 2>/dev/null
```

#### 주요 점검 대상 SUID 파일

| 파일 | 필요 여부 | 조치 |
|------|:--------:|------|
| /usr/bin/passwd | 필요 | 유지 |
| /usr/bin/su | 필요 | 유지 |
| /usr/bin/chsh | 검토 | 불필요 시 제거 |
| /usr/bin/newgrp | 검토 | 불필요 시 제거 |

---

### U-25. world writable 파일 점검

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 모든 사용자가 쓰기 가능한 파일 탐지 |

#### 점검 방법

```bash
# world writable 파일 검색
find / -perm -2 -type f 2>/dev/null

# world writable 디렉터리 검색 (sticky bit 없는)
find / -perm -2 -type d ! -perm -1000 2>/dev/null
```

---

## 3-3. 서비스 관리 (U-34 ~ U-63)

불필요한 서비스는 공격 표면을 증가시킵니다. 최소한의 서비스만 운영해야 합니다.

### U-34. Finger 서비스 비활성화

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 사용자 정보 노출 방지 |
| **판단 기준** | 양호: 비활성화 / 취약: 활성화 |

#### 점검 방법

```bash
# Finger 서비스 확인
systemctl status finger 2>/dev/null
# 또는
chkconfig --list finger 2>/dev/null
```

---

### U-36. r 계열 서비스 비활성화

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 인증 없는 원격 접속 차단 |
| **대상 서비스** | rsh, rlogin, rexec |

#### 점검 방법

```bash
# r 계열 서비스 확인
systemctl status rsh.socket rlogin.socket rexec.socket 2>/dev/null

# inetd/xinetd 설정 확인
cat /etc/xinetd.d/rsh 2>/dev/null | grep disable
```

> **WARNING**
> r 계열 서비스는 암호화되지 않은 통신을 사용합니다. SSH로 대체하세요.

---

### U-52. Telnet 서비스 비활성화

| 항목 | 내용 |
|------|------|
| **중요도** | 중 |
| **점검 목적** | 평문 통신 서비스 차단 |
| **판단 기준** | 양호: 비활성화 또는 SSH 사용 / 취약: Telnet 활성화 |

#### 점검 방법

```bash
# Telnet 서비스 확인
systemctl status telnet.socket 2>/dev/null

# 포트 확인
netstat -tlnp | grep :23
```

---

### U-58 ~ U-61. SNMP 보안

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| U-58 | 불필요한 SNMP 서비스 구동 점검 | 중 |
| U-59 | 안전한 SNMP 버전 사용 | 상 |
| U-60 | SNMP Community String 복잡성 | 중 |
| U-61 | SNMP Access Control 설정 | 상 |

#### 점검 방법

```bash
# SNMP 서비스 확인
systemctl status snmpd

# Community String 확인
cat /etc/snmp/snmpd.conf | grep -i community
```

> **TIP**
> SNMP v3를 사용하고, 기본 Community String(public, private)은 반드시 변경하세요.

---

## 3-4. 패치 관리 (U-64)

### U-64. 주기적 보안 패치 및 벤더 권고사항 적용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 알려진 취약점에 대한 패치 적용 |
| **판단 기준** | 양호: 최신 패치 적용 / 취약: 미적용 |

#### 점검 방법

```bash
# RHEL/CentOS
yum check-update

# Ubuntu/Debian
apt list --upgradable

# 커널 버전 확인
uname -r
```

#### 조치 방법

```bash
# RHEL/CentOS
yum update -y

# Ubuntu/Debian
apt update && apt upgrade -y
```

> **WARNING**
> 프로덕션 환경에서는 패치 전 테스트 환경에서 검증 후 적용하세요.

---

## 3-5. 로그 관리 (U-65 ~ U-68)

### U-65. 로그 정책 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 적절한 로그 기록 및 보관 |

#### 점검 방법

```bash
# syslog 설정 확인
cat /etc/rsyslog.conf

# 주요 로그 파일 존재 확인
ls -la /var/log/messages /var/log/secure /var/log/wtmp
```

### U-66. 정책에 따른 로그 관리

| 로그 파일 | 내용 | 권장 보관 기간 |
|----------|------|:-------------:|
| /var/log/messages | 시스템 메시지 | 6개월 |
| /var/log/secure | 인증 로그 | 6개월 |
| /var/log/wtmp | 로그인 기록 | 6개월 |
| /var/log/btmp | 실패한 로그인 | 6개월 |

---

## 3-6. 자동화 스크립트 작성

### 통합 점검 스크립트

아래는 주요 항목을 자동으로 점검하는 Bash 스크립트입니다.

```bash
#!/bin/bash
#===============================================
# KESE KIT - Unix/Linux 서버 취약점 자동 점검
# Version: 1.0
#===============================================

REPORT_FILE="unix_check_$(date +%Y%m%d_%H%M%S).txt"

echo "=============================================" | tee $REPORT_FILE
echo "KESE KIT Unix/Linux 취약점 점검 결과" | tee -a $REPORT_FILE
echo "점검 일시: $(date)" | tee -a $REPORT_FILE
echo "호스트명: $(hostname)" | tee -a $REPORT_FILE
echo "=============================================" | tee -a $REPORT_FILE

# U-01: root 원격 접속 제한
echo -e "\n[U-01] root 원격 접속 제한" | tee -a $REPORT_FILE
SSH_ROOT=$(grep -i "^PermitRootLogin" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
if [ "$SSH_ROOT" == "no" ]; then
    echo "  [양호] PermitRootLogin = no" | tee -a $REPORT_FILE
else
    echo "  [취약] PermitRootLogin = $SSH_ROOT" | tee -a $REPORT_FILE
fi

# U-04: 비밀번호 파일 보호
echo -e "\n[U-04] 비밀번호 파일 보호 (Shadow 사용)" | tee -a $REPORT_FILE
SHADOW_CHECK=$(awk -F: '$2!="x" && $2!="*" && $2!="!!" {print $1}' /etc/passwd)
if [ -z "$SHADOW_CHECK" ]; then
    echo "  [양호] Shadow 패스워드 사용 중" | tee -a $REPORT_FILE
else
    echo "  [취약] Shadow 미사용 계정: $SHADOW_CHECK" | tee -a $REPORT_FILE
fi

# U-05: root 외 UID 0 계정
echo -e "\n[U-05] root 외 UID 0 계정" | tee -a $REPORT_FILE
UID_ZERO=$(awk -F: '$3==0 && $1!="root" {print $1}' /etc/passwd)
if [ -z "$UID_ZERO" ]; then
    echo "  [양호] root만 UID 0" | tee -a $REPORT_FILE
else
    echo "  [취약] UID 0 계정: $UID_ZERO" | tee -a $REPORT_FILE
fi

# U-16: /etc/passwd 권한
echo -e "\n[U-16] /etc/passwd 권한" | tee -a $REPORT_FILE
PASSWD_PERM=$(stat -c "%a" /etc/passwd)
if [ "$PASSWD_PERM" -le "644" ]; then
    echo "  [양호] 권한: $PASSWD_PERM" | tee -a $REPORT_FILE
else
    echo "  [취약] 권한: $PASSWD_PERM (644 이하 권장)" | tee -a $REPORT_FILE
fi

# U-18: /etc/shadow 권한
echo -e "\n[U-18] /etc/shadow 권한" | tee -a $REPORT_FILE
SHADOW_PERM=$(stat -c "%a" /etc/shadow)
if [ "$SHADOW_PERM" -le "400" ]; then
    echo "  [양호] 권한: $SHADOW_PERM" | tee -a $REPORT_FILE
else
    echo "  [취약] 권한: $SHADOW_PERM (400 이하 권장)" | tee -a $REPORT_FILE
fi

# U-52: Telnet 서비스
echo -e "\n[U-52] Telnet 서비스" | tee -a $REPORT_FILE
TELNET_CHECK=$(systemctl is-active telnet.socket 2>/dev/null)
if [ "$TELNET_CHECK" != "active" ]; then
    echo "  [양호] Telnet 비활성화" | tee -a $REPORT_FILE
else
    echo "  [취약] Telnet 활성화됨" | tee -a $REPORT_FILE
fi

echo -e "\n=============================================" | tee -a $REPORT_FILE
echo "점검 완료. 결과 파일: $REPORT_FILE" | tee -a $REPORT_FILE
```

### 스크립트 사용 방법

```bash
# 실행 권한 부여
chmod +x unix_check.sh

# 실행 (root 권한 필요)
sudo ./unix_check.sh

# 결과 확인
cat unix_check_*.txt
```

> **TIP**
> 이 스크립트를 cron에 등록하여 주기적으로 점검할 수 있습니다.
> ```
> # 매주 월요일 오전 2시 실행
> 0 2 * * 1 /path/to/unix_check.sh
> ```

---

## 요약

| 영역 | 핵심 점검 항목 | 우선순위 |
|------|---------------|:--------:|
| 계정 관리 | root 원격접속, 비밀번호 정책, 계정 잠금 | 최우선 |
| 파일 권한 | 주요 설정 파일 권한, SUID/SGID | 높음 |
| 서비스 관리 | 불필요 서비스 비활성화, SNMP 보안 | 높음 |
| 패치 관리 | 최신 보안 패치 적용 | 최우선 |
| 로그 관리 | 로그 설정 및 보관 | 중간 |

---

*다음 장: 4장. Windows 서버 점검*
