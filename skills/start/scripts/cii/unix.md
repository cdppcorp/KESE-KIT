# Unix 서버 점검 및 조치 스크립트

## 1. 계정 관리

### U-01: root 계정 원격 접속 제한
**판단기준:** 원격터미널 서비스 사용 시 root 직접 접속을 차단한 경우 양호
**점검:**
```bash
# SSH root 접속 설정 확인
grep -i "PermitRootLogin" /etc/ssh/sshd_config

# Telnet root 접속 설정 확인 (SOLARIS)
grep "CONSOLE" /etc/default/login

# Telnet pts 설정 확인 (LINUX)
cat /etc/securetty | grep pts

# Telnet rlogin 설정 확인 (AIX)
grep "rlogin" /etc/security/user
```
**조치:**
```bash
# SSH - 모든 OS 공통
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd

# Telnet - SOLARIS
# /etc/default/login 파일에 설정
echo "CONSOLE=/dev/console" >> /etc/default/login

# Telnet - LINUX (/etc/securetty에서 pts 제거)
sed -i '/^pts\//d' /etc/securetty
# /etc/pam.d/login에 모듈 추가
# auth required /lib/security/pam_securetty.so

# Telnet - AIX (/etc/security/user)
chsec -f /etc/security/user -s root -a rlogin=false

# HP-UX SSH
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' /opt/ssh/etc/sshd_config
```

### U-02: 비밀번호 관리정책 설정
**판단기준:** 영문+숫자+특수문자 8자리 이상, 최소사용 1일, 최대사용 90일, 이력 4회 이상 양호
**점검:**
```bash
# LINUX - 비밀번호 정책 확인
grep -E "PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_MIN_LEN|PASS_WARN_AGE" /etc/login.defs
cat /etc/security/pwquality.conf 2>/dev/null
grep pam_pwquality /etc/pam.d/system-auth 2>/dev/null
grep pam_pwquality /etc/pam.d/common-password 2>/dev/null

# SOLARIS
cat /etc/default/passwd | grep -E "HISTORY|PASSLENGTH|MINDIGIT|MINUPPER|MINLOWER|MINSPECIAL"

# AIX
grep -E "minage|maxage|minalpha|minother|minlen|histsize" /etc/security/user
```
**조치:**
```bash
# LINUX (Redhat) - /etc/login.defs
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/' /etc/login.defs
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 1/' /etc/login.defs

# LINUX (Redhat) - /etc/security/pwquality.conf
cat > /etc/security/pwquality.conf <<'CONF'
minlen = 8
dcredit = -1
ucredit = -1
lcredit = -1
ocredit = -1
enforce_for_root
CONF

# SOLARIS - /etc/default/passwd
cat >> /etc/default/passwd <<'CONF'
HISTORY=4
PASSLENGTH=8
MINDIGIT=1
MINUPPER=1
MINLOWER=1
MINSPECIAL=1
WHITESPACE=NO
CONF

# AIX - /etc/security/user
chsec -f /etc/security/user -s default -a minage=1
chsec -f /etc/security/user -s default -a maxage=12
chsec -f /etc/security/user -s default -a minalpha=2
chsec -f /etc/security/user -s default -a minother=2
chsec -f /etc/security/user -s default -a minlen=8
chsec -f /etc/security/user -s default -a histsize=4

# HP-UX - /etc/default/security
cat >> /etc/default/security <<'CONF'
MIN_PASSWORD_LENGTH=8
PASSWORD_MIN_UPPER_CASE_CHARS=1
PASSWORD_MIN_LOWER_CASE_CHARS=1
PASSWORD_MIN_DIGIT_CASE_CHARS=1
PASSWORD_MIN_SPECIAL_CASE_CHARS=1
PASSWORD_MAXDAYS=90
PASSWORD_MINDAYS=1
HISTORY=4
CONF
```

### U-03: 계정 잠금 임계값 설정
**판단기준:** 계정 잠금 임계값이 10회 이하로 설정된 경우 양호
**점검:**
```bash
# LINUX - PAM 계정잠금 설정 확인
grep pam_tally /etc/pam.d/system-auth 2>/dev/null
grep pam_faillock /etc/pam.d/system-auth 2>/dev/null
grep -E "deny|unlock_time" /etc/security/faillock.conf 2>/dev/null
authselect current 2>/dev/null

# SOLARIS
grep "RETRIES" /etc/default/login
grep "LOCK_AFTER_RETRIES" /etc/security/policy.conf 2>/dev/null

# AIX
grep "loginretries" /etc/security/user

# HP-UX
grep "AUTH_MAXTRIES" /etc/default/security 2>/dev/null
```
**조치:**
```bash
# LINUX (Redhat - authselect 방식, RHEL 8+)
authselect enable-feature with-faillock
# /etc/security/faillock.conf 수정
cat >> /etc/security/faillock.conf <<'CONF'
silent
deny = 10
unlock_time = 120
CONF

# LINUX (Redhat - pam_faillock 방식)
# /etc/pam.d/system-auth에 추가
# auth required pam_faillock.so preauth silent audit deny=10 unlock_time=120
# /etc/pam.d/password-auth에 추가
# auth required pam_faillock.so preauth silent audit deny=10 unlock_time=120

# LINUX (Debian - pam_faillock 방식)
# /etc/pam.d/common-auth에 추가
# auth required pam_faillock.so preauth silent audit deny=10 unlock_time=120

# SOLARIS (5.9+)
# /etc/security/policy.conf
echo "LOCK_AFTER_RETRIES=YES" >> /etc/security/policy.conf

# AIX
chsec -f /etc/security/user -s default -a loginretries=10

# HP-UX (11.v3+)
echo "AUTH_MAXTRIES=10" >> /etc/default/security
```

### U-04: 비밀번호 파일 보호
**판단기준:** 쉐도우 비밀번호를 사용하거나 비밀번호를 암호화하여 저장하는 경우 양호
**점검:**
```bash
# /etc/passwd 두 번째 필드가 'x'인지 확인 (x이면 shadow 사용 중)
awk -F: '$2 != "x" {print $1" : 비밀번호 평문 저장 의심"}' /etc/passwd
```
**조치:**
```bash
# SOLARIS, LINUX - 쉐도우 비밀번호 적용
pwconv

# HP-UX - Trusted Mode 전환
/etc/tsconvert
```

### U-05: root 이외의 UID가 '0' 금지
**판단기준:** root 계정과 동일한 UID(0)를 갖는 계정이 존재하지 않는 경우 양호
**점검:**
```bash
awk -F: '$3==0 && $1!="root" {print $1" has UID 0"}' /etc/passwd
```
**조치:**
```bash
# UID 변경
usermod -u <변경할_UID> <사용자_이름>
# AIX의 경우
# chuser id=<변경할_UID> <사용자_이름>
```

### U-06: 사용자 계정 su 기능 제한
**판단기준:** su 명령어를 특정 그룹에 속한 사용자만 사용하도록 제한된 경우 양호
**점검:**
```bash
# wheel 그룹 확인
grep wheel /etc/group
# su 명령어 권한 확인
ls -l /usr/bin/su
# PAM 설정 확인 (LINUX)
grep pam_wheel /etc/pam.d/su
```
**조치:**
```bash
# wheel 그룹 생성 (없는 경우)
groupadd wheel
# su 명령 그룹 변경 및 권한 설정
chgrp wheel /usr/bin/su
chmod 4750 /usr/bin/su
# 허용 계정 등록
usermod -G wheel <username>

# LINUX PAM 설정 - /etc/pam.d/su
# auth required pam_wheel.so use_uid
```

### U-07: 불필요한 계정 제거
**판단기준:** 불필요한 계정이 존재하지 않는 경우 양호
**점검:**
```bash
# 시스템 계정 확인
cat /etc/passwd
# 마지막 로그인 기록 확인
last | head -30
# 로그인 불가 계정 확인
awk -F: '$7 !~ /nologin|false/ {print $1}' /etc/passwd
```
**조치:**
```bash
userdel <사용자_이름>
# AIX의 경우
# rmuser <사용자_이름>
```

### U-08: 관리자 그룹에 최소한의 계정 포함
**판단기준:** 관리자 그룹에 불필요한 계정이 등록되어 있지 않은 경우 양호
**점검:**
```bash
grep "^root:" /etc/group
```
**조치:**
```bash
gpasswd -d <사용자_이름> root
# AIX의 경우
# chgrpmem -m - <사용자_이름> root
```

### U-09: 계정이 존재하지 않는 GID 금지
**판단기준:** 시스템 관리나 운용에 불필요한 그룹이 제거된 경우 양호
**점검:**
```bash
# /etc/group과 /etc/passwd 비교
cat /etc/group
cat /etc/gshadow 2>/dev/null
```
**조치:**
```bash
groupdel <그룹_이름>
```

### U-10: 동일한 UID 금지
**판단기준:** 동일한 UID로 설정된 사용자 계정이 존재하지 않는 경우 양호
**점검:**
```bash
awk -F: '{print $3}' /etc/passwd | sort -n | uniq -d
# 중복 UID가 있다면 해당 계정 확인
awk -F: '{uid[$3]=uid[$3]" "$1} END{for(u in uid) if(split(uid[u],a," ")>2) print "UID "u":"uid[u]}' /etc/passwd
```
**조치:**
```bash
usermod -u <변경할_UID> <사용자_이름>
# AIX의 경우
# chuser id=<변경할_UID> <사용자_이름>
```

### U-11: 사용자 shell 점검
**판단기준:** 로그인이 필요하지 않은 계정에 /bin/false 또는 /sbin/nologin 쉘이 부여된 경우 양호
**점검:**
```bash
cat /etc/passwd | grep -E "^daemon|^bin|^sys|^adm|^listen|^nobody|^nobody4|^noaccess|^diag|^operator|^games|^gopher" | grep -v admin
```
**조치:**
```bash
# 불필요한 계정에 nologin 쉘 부여
usermod -s /bin/false <계정명>
usermod -s /sbin/nologin <계정명>
```

### U-12: 세션 종료 시간 설정
**판단기준:** Session Timeout이 600초(10분) 이하로 설정된 경우 양호
**점검:**
```bash
echo $TMOUT
grep -i tmout /etc/profile /etc/bashrc 2>/dev/null
grep autologout /etc/csh.cshrc /etc/csh.login 2>/dev/null
```
**조치:**
```bash
# sh, ksh, bash - /etc/profile에 추가
echo "TMOUT=600" >> /etc/profile
echo "export TMOUT" >> /etc/profile

# csh - /etc/csh.cshrc 또는 /etc/csh.login에 추가
echo "set autologout=10" >> /etc/csh.cshrc
```

### U-13: 안전한 비밀번호 암호화 알고리즘 사용
**판단기준:** SHA-2 이상의 안전한 비밀번호 암호화 알고리즘을 사용하는 경우 양호 ($5=SHA-256, $6=SHA-512)
**점검:**
```bash
# 암호화 알고리즘 확인 ($1=MD5, $5=SHA-256, $6=SHA-512)
awk -F: '$2 ~ /^\$/ {split($2,a,"$"); print $1" -> $"a[2]}' /etc/shadow 2>/dev/null

# LINUX
grep ENCRYPT_METHOD /etc/login.defs
```
**조치:**
```bash
# LINUX (Redhat)
sed -i 's/^ENCRYPT_METHOD.*/ENCRYPT_METHOD SHA512/' /etc/login.defs
# /etc/pam.d/system-auth
# password sufficient pam_unix.so sha512

# SOLARIS
# /etc/security/policy.conf
echo "CRYPT_DEFAULT=6" >> /etc/security/policy.conf

# AIX
chsec -f /etc/security/login.cfg -s usw -a pwd_algorithm=ssha512

# HP-UX
echo "CRYPT_DEFAULT=6" >> /etc/default/security
```

---

## 2. 파일 및 디렉터리 관리

### U-14: root 홈, 패스 디렉터리 권한 및 패스 설정
**판단기준:** PATH 환경변수에 "."이 맨 앞이나 중간에 포함되지 않은 경우 양호
**점검:**
```bash
echo $PATH | tr ':' '\n' | grep -n "^\.$"
echo $PATH | grep -E "(^\.:|:\.:|:\.$ )"
```
**조치:**
```bash
# 환경설정 파일에서 PATH 변숫값에서 "." 제거 또는 맨 마지막으로 이동
# ~/.profile, ~/.bashrc, /etc/profile 등에서 수정
# 예: PATH=$PATH:$HOME/bin (상대경로 "." 삭제)
```

### U-15: 파일 및 디렉터리 소유자 설정
**판단기준:** 소유자가 존재하지 않는 파일 및 디렉터리가 존재하지 않는 경우 양호
**점검:**
```bash
find / \( -nouser -o -nogroup \) -xdev -ls 2>/dev/null
```
**조치:**
```bash
# 불필요한 파일 제거
rm <파일_이름>
rm -r <디렉터리_이름>
# 사용 중인 파일의 소유자 변경
chown <사용자_이름> <파일명>
chgrp <그룹_이름> <파일명>
```

### U-16: /etc/passwd 파일 소유자 및 권한 설정
**판단기준:** 소유자가 root이고, 권한이 644 이하인 경우 양호
**점검:**
```bash
ls -l /etc/passwd
```
**조치:**
```bash
chown root /etc/passwd
chmod 644 /etc/passwd
```

### U-17: 시스템 시작 스크립트 권한 설정
**판단기준:** 소유자가 root이고, 일반 사용자의 쓰기 권한이 제거된 경우 양호
**점검:**
```bash
# LINUX (init)
ls -al /etc/rc.d/*/* 2>/dev/null
# LINUX (systemd)
ls -al /etc/systemd/system/* 2>/dev/null
# SOLARIS
ls -al /etc/rc*.d/* 2>/dev/null
```
**조치:**
```bash
chown root <파일_이름>
chmod o-w <파일_이름>
```

### U-18: /etc/shadow 파일 소유자 및 권한 설정
**판단기준:** 소유자가 root이고, 권한이 400 이하인 경우 양호
**점검:**
```bash
ls -l /etc/shadow
# AIX
ls -l /etc/security/passwd
```
**조치:**
```bash
# SOLARIS, LINUX
chown root /etc/shadow
chmod 400 /etc/shadow

# AIX
chown root /etc/security/passwd
chmod 400 /etc/security/passwd
```

### U-19: /etc/hosts 파일 소유자 및 권한 설정
**판단기준:** 소유자가 root이고, 권한이 644 이하인 경우 양호
**점검:**
```bash
ls -l /etc/hosts
```
**조치:**
```bash
chown root /etc/hosts
chmod 644 /etc/hosts
```

### U-20: /etc/(x)inetd.conf 파일 소유자 및 권한 설정
**판단기준:** 소유자가 root이고, 권한이 600 이하인 경우 양호
**점검:**
```bash
ls -l /etc/inetd.conf 2>/dev/null
ls -l /etc/xinetd.conf 2>/dev/null
ls -l /etc/xinetd.d/* 2>/dev/null
ls -l /etc/systemd/system.conf 2>/dev/null
```
**조치:**
```bash
# inetd
chown root /etc/inetd.conf
chmod 600 /etc/inetd.conf

# xinetd
chown root /etc/xinetd.conf
chmod 600 /etc/xinetd.conf
chown -R root /etc/xinetd.d/
chmod -R 600 /etc/xinetd.d/

# systemd
chown root /etc/systemd/system.conf
chmod 600 /etc/systemd/system.conf
```

### U-21: /etc/(r)syslog.conf 파일 소유자 및 권한 설정
**판단기준:** 소유자가 root(또는 bin, sys)이고, 권한이 640 이하인 경우 양호
**점검:**
```bash
ls -l /etc/syslog.conf /etc/rsyslog.conf 2>/dev/null
```
**조치:**
```bash
chown root /etc/rsyslog.conf
chmod 640 /etc/rsyslog.conf
```

### U-22: /etc/services 파일 소유자 및 권한 설정
**판단기준:** 소유자가 root(또는 bin, sys)이고, 권한이 644 이하인 경우 양호
**점검:**
```bash
ls -l /etc/services
```
**조치:**
```bash
chown root /etc/services
chmod 644 /etc/services
```

### U-23: SUID, SGID, Sticky bit 설정 파일 점검
**판단기준:** 주요 실행 파일의 권한에 불필요한 SUID/SGID가 부여되어 있지 않은 경우 양호
**점검:**
```bash
find / -user root -type f \( -perm -04000 -o -perm -02000 \) -xdev -exec ls -al {} \;
```
**조치:**
```bash
# 불필요한 특수 권한 제거
chmod -s <파일_이름>

# 특정 그룹에서만 사용하도록 제한
chgrp <그룹_이름> <SUID_파일>
chmod 4750 <SUID_파일>
```

### U-24: 사용자, 시스템 환경변수 파일 소유자 및 권한 설정
**판단기준:** 홈 디렉터리 환경변수 파일 소유자가 root 또는 해당 계정이고, 소유자 외 쓰기 권한이 없는 경우 양호
**점검:**
```bash
# 각 사용자 홈 디렉터리의 환경변수 파일 확인
ls -la ~/.profile ~/.kshrc ~/.cshrc ~/.bashrc ~/.bash_profile ~/.login ~/.exrc ~/.netrc 2>/dev/null
```
**조치:**
```bash
chown <root_또는_소유자> <환경변수_파일>
chmod o-w <환경변수_파일>
```

### U-25: world writable 파일 점검
**판단기준:** world writable 파일이 존재하지 않거나, 존재 시 설정 이유를 인지하고 있는 경우 양호
**점검:**
```bash
find / -type f -perm -2 -exec ls -l {} \; 2>/dev/null
```
**조치:**
```bash
# 일반 사용자 쓰기 권한 제거
chmod o-w <파일_이름>
# 불필요한 파일 제거
rm <파일_이름>
```

### U-26: /dev에 존재하지 않는 device 파일 점검
**판단기준:** /dev 디렉터리에 존재하지 않는 device 파일을 제거한 경우 양호
**점검:**
```bash
find /dev -type f -exec ls -l {} \;
```
**조치:**
```bash
rm <파일_이름>
```

### U-27: $HOME/.rhosts, hosts.equiv 사용 금지
**판단기준:** rlogin/rsh/rexec 미사용 또는 사용 시 소유자 root, 권한 600 이하, "+" 설정 없는 경우 양호
**점검:**
```bash
find / -name ".rhosts" -o -name "hosts.equiv" 2>/dev/null
cat /etc/hosts.equiv 2>/dev/null
ls -la /etc/hosts.equiv 2>/dev/null
```
**조치:**
```bash
chown root /etc/hosts.equiv
chmod 600 /etc/hosts.equiv
chown root $HOME/.rhosts
chmod 600 $HOME/.rhosts
# "+" 옵션 제거 후 허용 호스트 및 계정만 등록
```

### U-28: 접속 IP 및 포트 제한
**판단기준:** 접속을 허용할 특정 호스트에 대한 IP주소 및 포트 제한을 설정한 경우 양호
**점검:**
```bash
# TCP Wrapper
cat /etc/hosts.allow 2>/dev/null
cat /etc/hosts.deny 2>/dev/null

# iptables
iptables -L 2>/dev/null

# firewalld
firewall-cmd --list-all 2>/dev/null

# UFW
ufw status numbered 2>/dev/null
```
**조치:**
```bash
# TCP Wrapper
echo "ALL:ALL" > /etc/hosts.deny
echo "sshd : <허용_IP>" >> /etc/hosts.allow

# iptables
iptables -A INPUT -p tcp -s <IP주소> --dport <포트> -j ACCEPT
iptables-save

# firewalld
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="<IP>" port protocol="tcp" port="<포트>" accept'
firewall-cmd --reload

# UFW
ufw allow from <IP주소> to any port <포트>
ufw reload
```

### U-29: hosts.lpd 파일 소유자 및 권한 설정
**판단기준:** /etc/hosts.lpd 파일이 존재하지 않거나, 소유자 root이고 권한 600 이하인 경우 양호
**점검:**
```bash
ls -l /etc/hosts.lpd 2>/dev/null
```
**조치:**
```bash
chown root /etc/hosts.lpd
chmod 600 /etc/hosts.lpd
```

### U-30: UMASK 설정 관리
**판단기준:** UMASK 값이 022 이상으로 설정된 경우 양호
**점검:**
```bash
umask
grep -i umask /etc/profile /etc/bashrc /etc/login.defs 2>/dev/null
# SOLARIS
grep UMASK /etc/default/login 2>/dev/null
```
**조치:**
```bash
# /etc/profile에 추가
echo "umask 022" >> /etc/profile
echo "export umask" >> /etc/profile

# LINUX - /etc/login.defs
sed -i 's/^UMASK.*/UMASK 022/' /etc/login.defs

# SOLARIS - /etc/default/login
echo "UMASK=022" >> /etc/default/login

# FTP umask 설정
# vsFTP: vsftpd.conf -> local_umask=022
# ProFTP: proftpd.conf -> Umask 022
```

### U-31: 홈디렉토리 소유자 및 권한 설정
**판단기준:** 홈 디렉토리 소유자가 해당 계정이고, 타 사용자 쓰기 권한이 제거된 경우 양호
**점검:**
```bash
cat /etc/passwd | awk -F: '{print $1" "$6}' | while read user dir; do
  ls -ald "$dir" 2>/dev/null
done
```
**조치:**
```bash
chown <사용자_이름> <홈_디렉터리>
chmod o-w <홈_디렉터리>
```

### U-32: 홈 디렉토리로 지정한 디렉토리의 존재 관리
**판단기준:** 홈 디렉토리가 존재하지 않는 계정이 발견되지 않는 경우 양호
**점검:**
```bash
awk -F: '{print $1" "$6}' /etc/passwd | while read user dir; do
  [ ! -d "$dir" ] && echo "$user : $dir 존재하지 않음"
done
```
**조치:**
```bash
# 불필요한 계정 삭제
userdel <사용자_이름>
# 사용중인 계정의 홈 디렉터리 생성
mkdir -p /home/<사용자_이름>
chown <사용자_이름> /home/<사용자_이름>
```

### U-33: 숨겨진 파일 및 디렉토리 검색 및 제거
**판단기준:** 불필요하거나 의심스러운 숨겨진 파일 및 디렉토리를 제거한 경우 양호
**점검:**
```bash
find / -type f -name ".*" 2>/dev/null
find / -type d -name ".*" 2>/dev/null
```
**조치:**
```bash
rm <파일_이름>
rm -r <디렉터리_이름>
```

---

## 3. 서비스 관리

### U-34: Finger 서비스 비활성화
**판단기준:** Finger 서비스가 비활성화된 경우 양호
**점검:**
```bash
# LINUX (systemd)
systemctl list-units --type=service | grep finger
# SOLARIS (5.10+)
inetadm | grep finger 2>/dev/null
# inetd
grep finger /etc/inetd.conf 2>/dev/null
# xinetd
cat /etc/xinetd.d/finger 2>/dev/null
```
**조치:**
```bash
# LINUX (systemd)
systemctl stop finger.socket 2>/dev/null
systemctl disable finger.socket 2>/dev/null

# xinetd
# /etc/xinetd.d/finger -> disable = yes
systemctl restart xinetd

# inetd - finger 항목 주석 처리
# SOLARIS (5.10+)
inetadm -d svc:/network/finger:default
```

### U-35: 공유 서비스에 대한 익명 접근 제한 설정
**판단기준:** 공유 서비스에 대해 익명 접근을 제한한 경우 양호
**점검:**
```bash
# FTP 익명 계정 확인
grep -E "^ftp|^anonymous" /etc/passwd

# vsFTP
grep anonymous_enable /etc/vsftpd.conf /etc/vsftpd/vsftpd.conf 2>/dev/null

# ProFTP
sed -n '/<Anonymous ~ftp>/,/<\/Anonymous>/p' /etc/proftpd.conf /etc/proftpd/proftpd.conf 2>/dev/null

# NFS 익명 접근
grep -E "anonuid|anongid" /etc/exports 2>/dev/null

# Samba
grep "guest ok" /etc/samba/smb.conf 2>/dev/null
```
**조치:**
```bash
# FTP 익명 계정 제거
userdel ftp
userdel anonymous

# vsFTP - /etc/vsftpd/vsftpd.conf
# anonymous_enable=NO
systemctl restart vsftpd

# NFS - /etc/exports에서 anon 옵션 제거
exportfs -ra

# Samba - /etc/samba/smb.conf
# guest ok = no
smbcontrol all reload-config
```

### U-36: r 계열 서비스 비활성화
**판단기준:** 불필요한 r 계열 서비스(rlogin, rsh, rexec)가 비활성화된 경우 양호
**점검:**
```bash
# LINUX (systemd)
systemctl list-units --type=service | grep -E "rlogin|rsh|rexec"
# inetd
grep -E "rlogin|rsh|rexec|shell|login|exec" /etc/inetd.conf 2>/dev/null
# SOLARIS (5.10+)
inetadm | egrep "shell|rlogin|rexec" 2>/dev/null
```
**조치:**
```bash
# LINUX (systemd)
systemctl stop rlogin.socket rsh.socket rexec.socket 2>/dev/null
systemctl disable rlogin.socket rsh.socket rexec.socket 2>/dev/null

# inetd - 해당 서비스 항목 주석 처리
# SOLARIS (5.10+)
inetadm -d svc:/network/login:rlogin
inetadm -d svc:/network/shell:default
inetadm -d svc:/network/rexec:default
```

### U-37: crontab 설정파일 권한 설정 미흡
**판단기준:** crontab/at 명령어 권한 750 이하, cron/at 관련 파일 권한 640 이하인 경우 양호
**점검:**
```bash
ls -l /usr/bin/crontab
ls -l /usr/bin/at
ls -l /var/spool/cron/ 2>/dev/null
ls -l /var/spool/cron/crontabs/ 2>/dev/null
ls -l /etc/cron.allow /etc/cron.deny /etc/at.allow /etc/at.deny 2>/dev/null
```
**조치:**
```bash
# crontab/at 명령어 권한 설정
chown root /usr/bin/crontab
chmod 750 /usr/bin/crontab
chown root /usr/bin/at
chmod 750 /usr/bin/at

# cron 관련 파일 권한 설정
chmod 640 /etc/cron.allow /etc/cron.deny 2>/dev/null
chmod 640 /etc/at.allow /etc/at.deny 2>/dev/null
```

### U-38: DoS 공격에 취약한 서비스 비활성화
**판단기준:** echo, discard, daytime, chargen 서비스가 비활성화된 경우 양호
**점검:**
```bash
# LINUX (systemd)
systemctl list-units --type=service | grep -E "echo|discard|daytime|chargen"
# inetd
grep -E "echo|discard|daytime|chargen" /etc/inetd.conf 2>/dev/null
# SOLARIS
inetadm | grep enable | egrep "echo|discard|daytime|chargen" 2>/dev/null
```
**조치:**
```bash
# LINUX (systemd)
systemctl stop echo.socket discard.socket daytime.socket chargen.socket 2>/dev/null
systemctl disable echo.socket discard.socket daytime.socket chargen.socket 2>/dev/null

# inetd - 해당 서비스 항목 주석 처리
# SOLARIS
inetadm -d <서비스_데몬>
```

### U-39: 불필요한 NFS 서비스 비활성화
**판단기준:** 불필요한 NFS 서비스 관련 데몬이 비활성화된 경우 양호
**점검:**
```bash
# LINUX
systemctl list-units --type=service | grep nfs
# AIX
ps -ef | grep nfsd
lssrc -a | grep nfs 2>/dev/null
# SOLARIS
inetadm | egrep "nfs|statd|lockd" 2>/dev/null
```
**조치:**
```bash
# LINUX
systemctl stop nfs-server
systemctl disable nfs-server

# SOLARIS
inetadm -d <NFS_서비스_데몬>

# AIX
stopsrc -g nfs

# HP-UX
# /etc/rc.config.d/nfsconf -> NFS_SERVER=0
```

### U-40: NFS 접근 통제
**판단기준:** 접근 통제가 설정되어 있으며 NFS 설정 파일 접근 권한이 644 이하인 경우 양호
**점검:**
```bash
# LINUX
ls -l /etc/exports
cat /etc/exports
showmount -e 2>/dev/null

# SOLARIS
ls -l /etc/dfs/dfstab 2>/dev/null
cat /etc/dfs/dfstab 2>/dev/null
```
**조치:**
```bash
# LINUX
chown root /etc/exports
chmod 644 /etc/exports
# /etc/exports 예시: /home/share host1(ro,root_squash)
exportfs -ra

# SOLARIS
chown root /etc/dfs/dfstab
chmod 644 /etc/dfs/dfstab
# /etc/dfs/dfstab 예시: share -F nfs -o rw=client1:client2,ro=client1:client2 /export/home
shareall
```

### U-41: 불필요한 automountd 제거
**판단기준:** automountd 서비스가 비활성화된 경우 양호
**점검:**
```bash
# LINUX
systemctl list-units --type=service | grep -E "automount|autofs"
# SOLARIS
svcs -a | grep autofs 2>/dev/null
# AIX
ps -ef | grep automountd
```
**조치:**
```bash
# LINUX
systemctl stop autofs
systemctl disable autofs

# SOLARIS
svcadm disable svc:/system/filesystem/autofs:default

# HP-UX
# /etc/rc.config.d/nfsconf -> AUTOFS=0
```

### U-42: 불필요한 RPC 서비스 비활성화
**판단기준:** 불필요한 RPC 서비스(rpc.cmsd, rpc.ttdbserverd, sadmind, rusersd, walld, sprayd 등)가 비활성화된 경우 양호
**점검:**
```bash
# LINUX (systemd)
systemctl list-units --type=service | grep rpc
# inetd
grep -E "rpc\." /etc/inetd.conf 2>/dev/null
# SOLARIS
inetadm | grep rpc | grep enabled | egrep "ttdbserver|rex|rstart|rusers|spray|wall|rquota" 2>/dev/null
```
**조치:**
```bash
# LINUX (systemd)
systemctl stop <서비스명>
systemctl disable <서비스명>

# inetd - 해당 RPC 서비스 항목 주석 처리
# SOLARIS
svcadm disable <서비스_데몬>
```

### U-43: NIS, NIS+ 점검
**판단기준:** NIS 서비스가 비활성화되어 있거나, 불가피 시 NIS+ 서비스를 사용하는 경우 양호
**점검:**
```bash
# LINUX
systemctl list-units --type=service | grep -E "ypserv|ypbind|ypxfrd|rpc.yppasswdd|rpc.ypupdated"
# SOLARIS
svcs -a | grep nis 2>/dev/null
# AIX
lssrc -a | grep -E "ypserv|ypbind" 2>/dev/null
```
**조치:**
```bash
# LINUX
systemctl stop ypserv ypbind 2>/dev/null
systemctl disable ypserv ypbind 2>/dev/null

# SOLARIS
svcadm disable <NIS_서비스_데몬>

# HP-UX - /etc/rc.config.d/namesrvs
# NIS_MASTER_SERVER=0
# NIS_SLAVE_SERVER=0
# NIS_CLIENT_SERVER=0
```

### U-44: tftp, talk 서비스 비활성화
**판단기준:** tftp, talk, ntalk 서비스가 비활성화된 경우 양호
**점검:**
```bash
# LINUX (systemd)
systemctl list-units --type=service | grep -E "tftp|talk|ntalk"
# inetd
grep -E "tftp|talk|ntalk" /etc/inetd.conf 2>/dev/null
# SOLARIS
inetadm | egrep "tftp|talk" 2>/dev/null
```
**조치:**
```bash
# LINUX (systemd)
systemctl stop tftp.socket talk.socket ntalk.socket 2>/dev/null
systemctl disable tftp.socket talk.socket ntalk.socket 2>/dev/null

# inetd - 해당 서비스 항목 주석 처리
# SOLARIS
inetadm -d <서비스_데몬명>
```

### U-45: 메일 서비스 버전 점검
**판단기준:** 메일 서비스 버전이 최신 버전인 경우 양호
**점검:**
```bash
# Sendmail
sendmail -d0 -bt < /dev/null 2>&1 | grep Version
# Postfix
postconf mail_version 2>/dev/null
# Exim
exim -bV 2>/dev/null
```
**조치:**
```bash
# 미사용 시 비활성화
systemctl stop sendmail postfix 2>/dev/null
systemctl disable sendmail postfix 2>/dev/null

# 사용 시 최신 버전으로 패치 적용
# Sendmail: http://www.sendmail.org/
# Postfix: https://www.postfix.org/packages.html
# Exim: https://www.exim.org/
```

### U-46: 일반 사용자의 메일 서비스 실행 방지
**판단기준:** 일반 사용자의 메일 서비스 실행 방지가 설정된 경우 양호
**점검:**
```bash
# Sendmail
grep PrivacyOptions /etc/mail/sendmail.cf 2>/dev/null
# Postfix
ls -l /usr/sbin/postsuper 2>/dev/null
# Exim
ls -l /usr/sbin/exiqgrep 2>/dev/null
```
**조치:**
```bash
# Sendmail - /etc/mail/sendmail.cf
# PrivacyOptions = authwarnings, novrfy, noexpn, restrictqrun

# Postfix
chmod o-x /usr/sbin/postsuper

# Exim
chmod o-x /usr/sbin/exiqgrep
```

### U-47: 스팸 메일 릴레이 제한
**판단기준:** 릴레이 제한이 설정된 경우 양호
**점검:**
```bash
# Sendmail
grep "promiscuous_relay" /etc/mail/sendmail.mc 2>/dev/null
cat /etc/mail/access 2>/dev/null
# Postfix
grep -E "smtpd_recipient_restrictions|mynetworks" /etc/postfix/main.cf 2>/dev/null
# Exim
grep -E "relay_from_hosts|hosts =" /etc/exim/exim.conf /etc/exim4/exim4.conf 2>/dev/null
```
**조치:**
```bash
# Sendmail - /etc/mail/sendmail.mc에서 promiscuous_relay 제거
# FEATURE(`promiscuous_relay')dnl 삭제
m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf
# /etc/mail/access에 허용/차단 설정
makemap hash /etc/mail/access.db < /etc/mail/access
systemctl restart sendmail

# Postfix - /etc/postfix/main.cf
# mynetworks = <허용할_네트워크>
postfix reload

# Exim - /etc/exim/exim.conf
# hostlist relay_from_hosts = <허용할_네트워크>
systemctl restart exim
```

### U-48: expn, vrfy 명령어 제한
**판단기준:** noexpn, novrfy 옵션이 설정된 경우 양호
**점검:**
```bash
# Sendmail
grep PrivacyOptions /etc/mail/sendmail.cf
# Postfix
grep disable_vrfy_command /etc/postfix/main.cf 2>/dev/null
# Exim
grep -E "acl_smtp_vrfy|acl_smtp_expn" /etc/exim/exim.conf /etc/exim4/exim4.conf 2>/dev/null
```
**조치:**
```bash
# Sendmail - /etc/mail/sendmail.cf
# PrivacyOptions = authwarnings, novrfy, noexpn, restrictqrun
# 또는 PrivacyOptions = restrictqrun, goaway

# Postfix - /etc/postfix/main.cf
# disable_vrfy_command = yes
postfix reload

# Exim - acl_smtp_vrfy, acl_smtp_expn 설정 제거/주석 처리
```

### U-49: DNS 보안 버전 패치
**판단기준:** 주기적으로 패치를 관리하는 경우 양호
**점검:**
```bash
named -v 2>/dev/null
# LINUX
systemctl list-units --type=service | grep named
```
**조치:**
```bash
# 미사용 시 비활성화
systemctl stop named
systemctl disable named

# 사용 시 최신 버전 패치
# ISC BIND: https://www.isc.org/downloads/
# 취약점 정보: https://kb.isc.org/v1/docs/en/aa-00913
```

### U-50: DNS ZoneTransfer 설정
**판단기준:** Zone Transfer를 허가된 사용자에게만 허용한 경우 양호
**점검:**
```bash
grep allow-transfer /etc/named.conf /etc/bind/named.conf.options 2>/dev/null
grep xfrnets /etc/named.boot /etc/bind/named.boot 2>/dev/null
```
**조치:**
```bash
# /etc/named.conf (또는 /etc/bind/named.conf.options) 수정
# allow-transfer { <허용할_IP>; };
systemctl restart named
```

### U-51: DNS 서비스의 취약한 동적 업데이트 설정 금지
**판단기준:** 동적 업데이트 기능이 비활성화되었거나, 적절한 접근통제를 수행하는 경우 양호
**점검:**
```bash
grep allow-update /etc/named.conf /etc/bind/named.conf.options 2>/dev/null
```
**조치:**
```bash
# /etc/named.conf 수정
# 불필요 시: allow-update { none; };
# 필요 시: allow-update { <허용할_IP>; };
systemctl restart named
```

### U-52: Telnet 서비스 비활성화
**판단기준:** Telnet 프로토콜을 비활성화하고 있는 경우 양호
**점검:**
```bash
# LINUX (systemd)
systemctl list-units --type=socket | grep telnet
# inetd
grep telnet /etc/inetd.conf 2>/dev/null
# xinetd
cat /etc/xinetd.d/telnet 2>/dev/null
# SOLARIS
svcs -a | grep telnet 2>/dev/null
```
**조치:**
```bash
# LINUX (systemd)
systemctl stop telnet.socket
systemctl disable telnet.socket
systemctl start sshd

# xinetd - /etc/xinetd.d/telnet -> disable = yes
systemctl restart xinetd

# SOLARIS
svcadm disable svc:/network/telnet:default
svcadm enable ssh
```

### U-53: FTP 서비스 정보 노출 제한
**판단기준:** FTP 접속 배너에 노출되는 정보가 없는 경우 양호
**점검:**
```bash
# vsFTP
grep ftpd_banner /etc/vsftpd.conf /etc/vsftpd/vsftpd.conf 2>/dev/null
# ProFTP
grep ServerIdent /etc/proftpd.conf /etc/proftpd/proftpd.conf 2>/dev/null
```
**조치:**
```bash
# vsFTP - /etc/vsftpd/vsftpd.conf
# ftpd_banner=Authorized access only
systemctl restart vsftpd

# ProFTP - /etc/proftpd/proftpd.conf
# ServerIdent off
# 또는 ServerIdent on "Authorized access only"
systemctl restart proftpd
```

### U-54: 암호화되지 않는 FTP 서비스 비활성화
**판단기준:** 암호화되지 않은 FTP 서비스가 비활성화된 경우 양호 (SFTP 사용 권고)
**점검:**
```bash
# LINUX
systemctl list-units --type=service | grep -E "vsftpd|proftpd"
# inetd
grep "^ftp" /etc/inetd.conf 2>/dev/null
```
**조치:**
```bash
# LINUX
systemctl stop vsftpd proftpd 2>/dev/null
systemctl disable vsftpd proftpd 2>/dev/null

# inetd - ftp 항목 주석 처리
```

### U-55: FTP 계정 shell 제한
**판단기준:** FTP 계정에 /bin/false 또는 /sbin/nologin 쉘이 부여된 경우 양호
**점검:**
```bash
grep "^ftp" /etc/passwd
```
**조치:**
```bash
usermod -s /bin/false ftp
# 또는
usermod -s /sbin/nologin ftp
```

### U-56: FTP 서비스 접근 제어 설정
**판단기준:** 특정 IP주소/호스트에서만 FTP 서버에 접속할 수 있도록 접근 제어 설정을 적용한 경우 양호
**점검:**
```bash
# ftpusers 파일
cat /etc/ftpusers /etc/ftpd/ftpusers 2>/dev/null
ls -l /etc/ftpusers /etc/ftpd/ftpusers 2>/dev/null

# vsFTP
grep userlist_enable /etc/vsftpd.conf /etc/vsftpd/vsftpd.conf 2>/dev/null
cat /etc/vsftpd/ftpusers /etc/vsftpd/user_list 2>/dev/null

# ProFTP
grep UseFtpUsers /etc/proftpd.conf /etc/proftpd/proftpd.conf 2>/dev/null
```
**조치:**
```bash
# ftpusers 파일 권한 설정
chown root /etc/ftpusers
chmod 640 /etc/ftpusers

# vsFTP - user_list 방식
# /etc/vsftpd/vsftpd.conf
# userlist_enable=YES
# userlist_deny=YES (목록 사용자 차단) 또는 NO (목록 사용자만 허용)

# ProFTP - proftpd.conf 접근제한
# <Limit LOGIN>
#   Order Deny,Allow
#   AllowUser <사용자> 또는 Allow from <IP>
#   DenyUser <사용자> 또는 Deny from <IP>
# </Limit>
```

### U-57: Ftpusers 파일 설정 (root 계정 접근 제한)
**판단기준:** root 계정 접속을 차단한 경우 양호
**점검:**
```bash
# ftpusers 파일에 root가 등록되어 있는지 확인
grep "^root" /etc/ftpusers /etc/ftpd/ftpusers /etc/vsftpd/ftpusers /etc/vsftpd/user_list 2>/dev/null

# ProFTP
grep RootLogin /etc/proftpd.conf /etc/proftpd/proftpd.conf 2>/dev/null
```
**조치:**
```bash
# ftpusers 파일에 root 추가 (주석 해제)
# 해당 파일에서 #root -> root 로 변경

# ProFTP - /etc/proftpd/proftpd.conf
# RootLogin off
systemctl restart proftpd
```

### U-58: 불필요한 SNMP 서비스 구동 점검
**판단기준:** SNMP 서비스를 사용하지 않는 경우 양호
**점검:**
```bash
# LINUX
systemctl list-units --type=service | grep snmpd
# SOLARIS
svcs -a | grep snmp 2>/dev/null
# AIX
lssrc -a | grep snmp 2>/dev/null
# 프로세스 확인
ps -ef | grep snmp
```
**조치:**
```bash
# LINUX
systemctl stop snmpd
systemctl disable snmpd

# SOLARIS (5.10+)
svcadm disable svc:/application/management/snmpd:default

# AIX
stopsrc -s snmpd
# /etc/rc.tcpip에서 snmpd 주석 처리
```

### U-59: 안전한 SNMP 버전 사용
**판단기준:** SNMP 서비스를 v3 이상으로 사용하는 경우 양호
**점검:**
```bash
# SNMPv3 사용 여부 확인
snmpwalk -v3 -l authPriv -u <사용자> -a SHA -A <인증암호> -x AES -X <암호화암호> <서버IP> 2>/dev/null
grep -E "rouser|rwuser|createUser" /etc/snmp/snmpd.conf 2>/dev/null
```
**조치:**
```bash
# SNMPv3 사용자 생성
net-snmp-create-v3-user -ro -A myauthpass -X myprivpass -a SHA -x AES myuser

# /etc/snmp/snmpd.conf에 추가
# createUser myuser SHA myauthpass AES myprivpass
# rouser myuser

systemctl restart snmpd
```

### U-60: SNMP Community String 복잡성 설정
**판단기준:** Community String이 "public", "private"이 아니고 영숫자 10자리 이상 또는 영숫자+특수문자 8자리 이상인 경우 양호
**점검:**
```bash
grep -i community /etc/snmp/snmpd.conf 2>/dev/null
# AIX
grep -i community /etc/snmpdv3.conf 2>/dev/null
# HP-UX
grep -i community /etc/snmpd.conf 2>/dev/null
```
**조치:**
```bash
# LINUX (Redhat) - /etc/snmp/snmpd.conf
# com2sec notConfigUser default <복잡한_String값>
# LINUX (Debian) - /etc/snmp/snmpd.conf
# rocommunity <복잡한_String값> default
systemctl restart snmpd

# AIX - /etc/snmpdv3.conf
# COMMUNITY <새_String> <새_String> noAuthNoPriv 0.0.0.0 0.0.0.0 -
stopsrc -s snmpd && startsrc -s snmpd
```

### U-61: SNMP Access Control 설정
**판단기준:** SNMP 서비스에 접근 제어 설정이 되어 있는 경우 양호
**점검:**
```bash
# LINUX (Redhat)
grep "com2sec" /etc/snmp/snmpd.conf 2>/dev/null
# LINUX (Debian)
grep -E "rocommunity|rwcommunity" /etc/snmp/snmpd.conf 2>/dev/null
```
**조치:**
```bash
# LINUX (Redhat) - /etc/snmp/snmpd.conf
# com2sec notConfigUser <허용_네트워크> <String값>

# LINUX (Debian) - /etc/snmp/snmpd.conf
# rocommunity <String값> <허용_네트워크>

systemctl restart snmpd

# AIX - /etc/snmpdv3.conf
# COMMUNITY <String> <String> noAuthNoPriv <허용_IP> <넷마스크> -
stopsrc -s snmpd && startsrc -s snmpd
```

### U-62: 로그인 시 경고 메시지 설정
**판단기준:** 서버 및 Telnet, FTP, SMTP, DNS 서비스에 로그온 시 경고 메시지가 설정된 경우 양호
**점검:**
```bash
# 서버 로그온 배너
cat /etc/motd 2>/dev/null
cat /etc/issue 2>/dev/null
cat /etc/issue.net 2>/dev/null

# SSH 배너
grep "^Banner" /etc/ssh/sshd_config

# Sendmail
grep SmtpGreetingMessage /etc/mail/sendmail.cf 2>/dev/null

# Postfix
grep smtpd_banner /etc/postfix/main.cf 2>/dev/null

# vsFTP
grep ftpd_banner /etc/vsftpd.conf /etc/vsftpd/vsftpd.conf 2>/dev/null

# DNS
grep "version" /etc/named.conf /etc/bind/named.conf.options 2>/dev/null
```
**조치:**
```bash
# 서버 경고 메시지
echo "Authorized access only. All activity is monitored." > /etc/motd
echo "Authorized access only." > /etc/issue
echo "Authorized access only." > /etc/issue.net

# SSH - /etc/ssh/sshd_config
# Banner /etc/issue.net
systemctl restart sshd

# Sendmail - /etc/mail/sendmail.cf
# SmtpGreetingMessage=Authorized access only

# Postfix - /etc/postfix/main.cf
# smtpd_banner = Authorized access only

# vsFTP - /etc/vsftpd/vsftpd.conf
# ftpd_banner=Authorized access only

# DNS - /etc/named.conf
# version "Not disclosed";
```

### U-63: sudo 명령어 접근 관리
**판단기준:** /etc/sudoers 파일 소유자가 root이고, 파일 권한이 640인 경우 양호
**점검:**
```bash
ls -l /etc/sudoers
```
**조치:**
```bash
chown root /etc/sudoers
chmod 640 /etc/sudoers
```

---

## 4. 패치 관리

### U-64: 주기적 보안 패치 및 벤더 권고사항 적용
**판단기준:** 패치 적용 정책을 수립하여 주기적으로 패치 관리를 하고 있는 경우 양호
**점검:**
```bash
# OS 및 커널 버전 확인
uname -a
cat /etc/os-release 2>/dev/null
hostnamectl 2>/dev/null

# 패치 이력 확인 (LINUX)
rpm -qa --last | head -20 2>/dev/null
apt list --upgradable 2>/dev/null

# SOLARIS
pkg list -af entire@latest 2>/dev/null

# AIX
oslevel -s
instfix -i | grep ML 2>/dev/null
instfix -i | grep SP 2>/dev/null

# HP-UX
swlist -l product 2>/dev/null
```
**조치:**
```bash
# LINUX (Redhat/CentOS)
yum update -y
# LINUX (Debian/Ubuntu)
apt update && apt upgrade -y

# SOLARIS
pkg update --accept

# AIX - smitty installp를 통한 패치 설치

# HP-UX
# swinstall -s /tmp/patch.depot
```

---

## 5. 로그 관리

### U-65: NTP 및 시각 동기화 설정
**판단기준:** NTP 및 시각 동기화 설정이 기준에 따라 적용된 경우 양호
**점검:**
```bash
# NTP
ntpq -pn 2>/dev/null
cat /etc/ntp.conf 2>/dev/null

# Chrony (RHEL 8+)
chronyc sources 2>/dev/null
cat /etc/chrony.conf 2>/dev/null
```
**조치:**
```bash
# NTP - /etc/ntp.conf
# server <NTP_서버_주소>
systemctl restart ntp 2>/dev/null || systemctl restart ntpd 2>/dev/null

# Chrony - /etc/chrony.conf
# server <NTP_서버_주소>
systemctl restart chronyd
```

### U-66: 정책에 따른 시스템 로깅 설정
**판단기준:** 로그 기록 정책이 보안 정책에 따라 수립되어 있으며, 로그를 남기고 있는 경우 양호
**점검:**
```bash
# LINUX
cat /etc/rsyslog.conf 2>/dev/null
ls /etc/rsyslog.d/ 2>/dev/null

# SOLARIS
cat /etc/syslog.conf 2>/dev/null

# AIX
cat /etc/syslog.conf 2>/dev/null
```
**조치:**
```bash
# LINUX - /etc/rsyslog.conf 권장 설정
cat >> /etc/rsyslog.conf <<'CONF'
*.info;mail.none;authpriv.none;cron.none    /var/log/messages
authpriv.*                                   /var/log/secure
mail.*                                       /var/log/maillog
cron.*                                       /var/log/cron
*.emerg                                      *
CONF
systemctl restart rsyslog

# SOLARIS - /etc/syslog.conf 권장 설정
# mail.debug     /var/log/mail.log
# *.info         /var/log/syslog.log
# *.alert        /dev/console
# *.emerg        *

# AIX - /etc/syslog.conf 권장 설정
# *.emerg        *
# *.alert        /dev/console
# *.err          /var/adm/error.log
# mail.info      /var/adm/mail.log
# auth.info      /var/adm/auth.log
# refresh -s syslogd

# HP-UX - /etc/syslog.conf 권장 설정
# *.emerg        *
# *.alert        /dev/console
# *.err          /var/adm/syslog/error.log
# mail.info      /var/adm/syslog/mail.log
# auth.info      /var/adm/syslog/auth.log
```

### U-67: 로그 디렉터리 소유자 및 권한 설정
**판단기준:** 로그 파일의 소유자가 root이고, 권한이 644 이하인 경우 양호
**점검:**
```bash
# LINUX, SOLARIS
ls -la /var/log/
# AIX
ls -la /var/adm/ 2>/dev/null
# HP-UX
ls -la /var/adm/syslog/ 2>/dev/null
```
**조치:**
```bash
# LINUX, SOLARIS
chown root /var/log/*
chmod 644 /var/log/*

# AIX
chown root /var/adm/*
chmod 644 /var/adm/*

# HP-UX
chown root /var/adm/syslog/*
chmod 644 /var/adm/syslog/*
```
