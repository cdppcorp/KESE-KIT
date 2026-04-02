# 네트워크 장비 점검 스크립트 (N-01 ~ N-38)

## 1. 계정 관리

### N-01: 비밀번호 설정
**점검:**
```
! Cisco IOS
Router> enable
Router# show running-config
! VTY, 콘솔, AUX 포트의 login/password 설정 확인

! Juniper Junos
user@host> configure
user@host# show

! Piolink PLOS
switch# show running-config
```
**조치:**
```
! Cisco IOS - enable 비밀번호
Router(config)# enable secret <비밀번호>
! VTY 비밀번호
Router(config)# line vty 0 4
Router(config-line)# login
Router(config-line)# password <비밀번호>
! 콘솔 비밀번호
Router(config)# line console 0
Router(config-line)# login
Router(config-line)# password <비밀번호>
! AUX 비밀번호
Router(config)# line aux 0
Router(config-line)# login
Router(config-line)# password <비밀번호>

! Radware Alteon
Main# /cfg/sys/access/user/admpw
Main# apply
Main# save

! Juniper Junos
user@host# set system root-authentication plain-test-passwd

! Piolink PLOS
(config)# password
```

### N-02: 비밀번호 복잡성 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! security passwords min-length 설정 확인
```
**조치:**
```
! Cisco IOS - 비밀번호 최소 길이 설정
Router(config)# security passwords min-length <길이>
```

### N-03: 암호화된 비밀번호 사용
**점검:**
```
! Cisco IOS
Router# show running-config
! enable secret / username secret / service password-encryption 확인

! Juniper Junos
user@host# show
! encrypted-password 설정 확인
```
**조치:**
```
! Cisco IOS
Router(config)# enable secret <비밀번호>
Router(config)# username <사용자> secret <비밀번호>
Router(config)# service password-encryption

! Juniper Junos
user@host# set system root-authentication encrypted-password <암호화된 비밀번호>
```

### N-04: 계정 잠금 임계값 설정
**점검:**
```
! Cisco IOS
Router# show running-config
Router# show login

! Juniper Junos
user@host# show version
```
**조치:**
```
! Cisco IOS
Router(config)# login block-for <잠금시간> attempts <실패횟수> within <허용시간>

! Juniper Junos
[edit system login retry-options]
user@host# set tries-before-disconnect <실패횟수>
user@host# set lockout-period <잠금시간>
```

### N-05: 사용자/명령어별 권한 설정
**점검:**
```
! Cisco IOS
Router# show privilege

! Juniper Junos
! [edit system login] 에서 superuser, read-only 클래스 분리 확인
```
**조치:**
```
! Cisco IOS - 사용자별 권한 수준 지정
Router(config)# username [ID] privilege [1-15] secret [PASS]
! 명령어별 권한 수준 지정 (중요 명령어 레벨 15 적용)
Router(config)# privilege exec level 15 connect
Router(config)# privilege exec level 15 telnet
Router(config)# privilege exec level 15 rlogin
Router(config)# privilege exec level 15 show ip access-list
Router(config)# privilege exec level 15 show logging

! Juniper Junos
[edit system login]
login {
  class class-name {
    allow-commands "regular-expression";
    deny-commands "regular-expression";
    idle-timeout minutes;
    permissions [ permissions ];
  }
}

! Piolink PLOS
! 슈퍼 유저(root)와 일반 유저로 권한 분리 관리
```

## 2. 접근 관리

### N-06: VTY 접근(ACL) 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! access-list 및 access-class 설정 확인

! Juniper Junos
user@host# show
! firewall filter + 루프백 인터페이스 적용 확인
```
**조치:**
```
! Cisco IOS
Router(config)# access-list <ACL번호> permit <IP주소>
Router(config)# access-list <ACL번호> deny any log
Router(config)# line vty 0 4
Router(config-line)# access-class <ACL번호> in

! Radware Alteon
# cfg > sys > access > mgmt > add
Enter Management Network Address: <IP주소>
Enter Management Network Mask: <서브넷마스크>
# apply > save

! Juniper Junos
user@host# set policy-options prefix-list <prefix-name> <IP주소>
user@host# edit firewall family inet filter <filter-name>
user@host# edit term <term-name-1>
user@host# set from source-address 0.0.0.0/0
user@host# set from source-prefix-list <prefix-name> except
user@host# set from protocol tcp
user@host# set from destination-port ssh
user@host# set then discard
! 기본 허용 종료
user@host# set term <term-name-2> then accept
! 루프백에 적용
user@host# set interfaces lo0 unit 0 family inet filter input <filter-name>

! Piolink PLOS
(config-security-system-access)# rule <rule-id>
(config-security-system-access-rule[id])# protocol tcp
(config-security-system-access-rule[id])# source-ip <IP주소>
(config-security-system-access-rule[id])# dest-port 22
(config-security-system-access-rule[id])# policy accept
(config-security-system-access-rule[id])# apply
(config-security-system-access)# default-policy deny
```

### N-07: Session Timeout 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! exec-timeout 설정 확인
```
**조치:**
```
! Cisco IOS (10분 이하 권고, 예: 5분)
Router(config)# line con 0
Router(config-line)# exec-timeout 5 0
Router(config)# line vty 0 4
Router(config-line)# exec-timeout 5 0
Router(config)# line aux 0
Router(config-line)# exec-timeout 5 0

! Radware Alteon
# cfg > sys > idle <분> > apply > save

! Juniper Junos
[edit login]
user@host# set class <클래스> idle-timeout <분>

! Piolink PLOS
(config)# terminal timeout <분>
```

### N-08: VTY 접속 시 안전한 프로토콜 사용
**점검:**
```
! Cisco IOS
Router# show ip ssh
Router# show version

! Juniper Junos
user@host# set ssh
```
**조치:**
```
! Cisco IOS - SSH 설정
Router(config)# hostname <호스트명>
Router(config)# ip domain-name <도메인명>
Router(config)# crypto key generate rsa
Router(config)# ip ssh version 2
Router(config)# ip ssh time-out <초>
Router(config)# ip ssh authentication-retries <횟수>
Router(config)# line vty 0 4
Router(config-line)# transport input ssh

! Radware Alteon
# cfg > /sys/sshd ena > /sys/sshd on > apply > save

! Juniper Junos
root# set system services ssh
root# delete system services telnet
root# commit

! Piolink PLOS
(config-management-access)# ssh status enable
(config-management-access)# telnet status disable
(config-management-access)# apply
```

### N-09: 불필요한 보조 입출력 포트 사용 금지
**점검:**
```
! Cisco IOS
Router# show running
! 불필요 포트 Up/Down 확인
```
**조치:**
```
! Cisco IOS - AUX 포트 차단
Router(config)# line aux 0
Router(config-line)# no password
Router(config-line)# transport input none
Router(config-line)# no exec
Router(config-line)# exec-timeout 0 1

! Juniper Junos
[edit system ports]
root# set auxiliary disable
root# commit
```

### N-10: 로그인 시 경고 메시지 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! banner 설정 확인
```
**조치:**
```
! Cisco IOS
Router(config)# banner motd # <경고 문구> #
Router(config)# banner login # <경고 문구> #
Router(config)# banner exec # <경고 문구> #

! Radware Alteon
# cfg > sys > banner <string> > apply > save

! Juniper Junos
[edit system login]
message "경고 문구"
```

### N-11: 원격로그 서버 사용
**점검:**
```
! Cisco IOS
Router# show running-config
Router# show logging
```
**조치:**
```
! Cisco IOS
Router(config)# logging on
Router(config)# logging trap informational
Router(config)# logging <syslog서버IP>
Router(config)# logging facility local6
Router(config)# logging source-interface serial 0

! Radware Alteon
# cfg > sys > /syslog/host <IP주소> > apply > save

! Juniper Junos
user@host# edit system syslog
user@host# set system syslog file message any error
user@host# set system syslog host <syslog서버IP> any any
user@host# set archive files 5 sizes 5m world-readable

! Piolink PLOS
# logging server enable
# logging server <IP주소> <event> <level>
```

## 3. 패치 관리

### N-12: 주기적 보안 패치 및 벤더 권고사항 적용
**점검:**
```
! Cisco IOS
Router# show version

! Juniper Junos
user@host# show version
```
**조치:**
```
! 공통
! 1. 하드웨어/소프트웨어/EOL/패치 현황 문서화
! 2. 벤더 보안 패치 및 권고사항 입수
! 3. 취약점 영향도/발생 가능성 분석 후 패치 우선순위 결정
! 4. 테스트베드(GNS3 등)에서 패치 검증
! 5. 패치 적용 전 이미지/설정 백업 후 적용
! 벤더별 패치 사이트:
!   Cisco: https://software.cisco.com
!   Juniper: https://support.juniper.net/support/downloads
!   공통: https://www.krcert.or.kr
```

## 4. 로그 관리

### N-13: 로깅 버퍼 크기 설정
**점검:**
```
! Cisco IOS
Router# show logging
```
**조치:**
```
! Cisco IOS
Router(config)# logging on
Router(config)# logging buffered 16000
Router(config)# logging buffered informational

! Piolink PLOS
(config)# logging buffer <size>
(config)# logging priority <event> <level>
```

### N-14: 정책에 따른 로깅 설정
**점검:**
```
! Cisco IOS
Router# show logging

! Juniper Junos
user@host# show log messages
```
**조치:**
```
! 공통 - 6가지 로깅 방법 활용
! 1. 콘솔 로깅: 콘솔 포트에서만 확인
! 2. Buffered 로깅: RAM에 저장 (버퍼 가득 차면 오래된 로그 대체)
! 3. Terminal 로깅: terminal monitor로 VTY에 전송
! 4. Syslog: 외부 syslog 서버에 저장
! 5. SNMP traps: 외부 SNMP 서버에 전송
! 6. ACL 침입 로깅: ACL 룰에 log/log-input 추가
```

### N-15: NTP 및 시각 동기화 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! ntp server 설정 확인
```
**조치:**
```
! Cisco IOS
Router(config)# ntp server <NTP서버IP>

! Radware Alteon
# cfg > /sys/ntp > on
# prisrvr <NTP서버IP>
# intrval <동기화주기>
# tzone +9:00
# apply > save

! Juniper Junos
[edit system ntp]
user@host# set server <NTP서버IP>
user@host# set boot-server <NTP부트서버IP>
```

### N-16: Timestamp 로그 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! service timestamps 확인
```
**조치:**
```
! Cisco IOS - UTC 시간 밀리초 단위
Router(config)# service timestamps log datetime msec show-timezone
! 로컬 시간(KST) 밀리초 단위
Router(config)# clock timezone KST 9
Router(config)# service timestamps log datetime msec localtime show-timezone
```

## 5. 기능 관리

### N-17: SNMP 서비스 확인
**점검:**
```
! Cisco IOS
Router# show running-config
Router# show snmp

! Juniper Junos
user@host# show snmp

! Piolink PLOS
switch# show running-config
```
**조치:**
```
! Cisco IOS - SNMP 비활성화
Router(config)# no snmp-server

! Radware Alteon
>> Main# /cfg/sys/access/snmp
Enter new SNMP access [d/r/w]: d

! Juniper Junos
user@host# no set snmp community public
```

### N-18: SNMP Community String 복잡성 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! snmp-server community 설정 확인 (public/private 사용 여부)
```
**조치:**
```
! Cisco IOS
Router(config)# snmp-server community <복잡한String>

! Radware Alteon
# cfg/sys/ssnmp
# rcomm <복잡한String>
# wcomm <복잡한String>
# apply > save

! Juniper Junos
user@host# set snmp community <복잡한String> authorization read-only

! Piolink PLOS
switch(config-snmp)# community <복잡한String>
switch(config-snmp)# status enable
switch(config-snmp)# apply
```

### N-19: SNMP ACL 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! snmp-server community + ACL 적용 확인
```
**조치:**
```
! Cisco IOS
Router(config)# access-list <ACL번호> permit <IP주소>
Router(config)# access-list <ACL번호> deny any log
Router(config)# snmp-server community <String> RO <ACL번호>

! Juniper Junos
[edit snmp]
user@host# edit client-list <client-list-name>
user@host# set default restrict
user@host# set <ip-address/range>
user@host# up
user@host# edit community <community-name>
user@host# set client-list-name <client-list-name>

! Piolink PLOS
(config-security-system-access)# rule <rule-id>
(config-security-system-access-rule[id])# protocol udp
(config-security-system-access-rule[id])# source-ip <IP주소>
(config-security-system-access-rule[id])# dest-port 161
(config-security-system-access-rule[id])# policy accept
(config-security-system-access-rule[id])# apply
(config-security-system-access)# default-policy deny
```

### N-20: SNMP Community 권한 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! snmp-server community RO/RW 확인
```
**조치:**
```
! Cisco IOS - RO 권한만 설정
Router(config)# snmp-server community <String> RO

! Radware Alteon
>> Main# /cfg/sys/access/snmp
Enter new SNMP access [d/r/w]: r
>> Main# apply

! Juniper Junos
[edit snmp]
user@host# delete community <Community>
user@host# set community <Community> authorization read-only
! SNMPv3 그룹 RW 권한 제거
[edit snmp v3 vacm access]
user@host# delete group <그룹> default-context-prefix security-model <모델> security-level <레벨> write-view

! Piolink PLOS
switch(config-snmp)# policy read-only
switch(config-snmp)# apply
```

### N-21: TFTP 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config
```
**조치:**
```
! Cisco IOS
Router(config)# no service tftp
```

### N-22: Spoofing 방지 필터링 적용
**점검:**
```
! Cisco IOS
Router# show running-config
! access-list deny 설정 확인

! Juniper Junos
! Configure/Apply Firewall Filters 확인
```
**조치:**
```
! Cisco IOS - Anti-Spoofing ACL (Extended ACL 100-199)
Router(config)# access-list <ACL번호> deny ip 0.0.0.0 0.255.255.255 any
Router(config)# access-list <ACL번호> deny ip 10.0.0.0 0.255.255.255 any
Router(config)# access-list <ACL번호> deny ip 127.0.0.0 0.255.255.255 any
Router(config)# access-list <ACL번호> deny ip 169.254.0.0 0.0.255.255 any
Router(config)# access-list <ACL번호> deny ip 172.16.0.0 0.15.255.255 any
Router(config)# access-list <ACL번호> deny ip 192.0.2.0 0.0.0.255 any
Router(config)# access-list <ACL번호> deny ip 192.168.0.0 0.0.255.255 any
Router(config)# access-list <ACL번호> deny ip 224.0.0.0 15.255.255.255 any
Router(config)# access-list <ACL번호> permit ip any any
Router(config)# interface serial <인터페이스>
Router(config-if)# ip access-group <ACL번호> in

! Juniper Junos
[edit policy-options]
user@host# set prefix-list <name> 0.0.0.0/8
user@host# set prefix-list <name> 10.0.0.0/8
user@host# set prefix-list <name> 127.0.0.0/8
user@host# set prefix-list <name> 169.254.0.0/16
user@host# set prefix-list <name> 172.16.0.0/12
user@host# set prefix-list <name> 192.0.2.0/24
user@host# set prefix-list <name> 192.168.0.0/16
user@host# set prefix-list <name> 224.0.0.0/4
[edit firewall family inet filter <filter-name> term <term-1>]
user@host# set from source-address <prefix-name>
user@host# set then discard
[edit firewall family inet filter <filter-name>]
user@host# set term <term-2> then accept
user@host# set interfaces <인터페이스> unit <유닛> family inet filter input <filter-name>
```

### N-23: DDoS 공격 방어 설정 또는 DDoS 장비 사용
**점검:**
```
! Cisco IOS
Router# show running-config

! Juniper Junos
user@host# show configuration
```
**조치:**
```
! 공통 - DDoS 방어 3가지 방법
! 1. ACL: 스푸핑 방지 필터링 사전 적용, 공격 유형별 IP/프로토콜/포트 임시 차단
! 2. Rate Limiting: UDP, ICMP, TCP SYN 패킷 대역폭 제한
! 3. TCP Intercept: SYN Flooding 방어
!   - Intercept 모드: 라우터가 SYN-ACK 대신 응답
!   - Watch 모드: SYN 전달 후 30초 미완료 시 RST 전송
```

### N-24: 사용하지 않는 인터페이스 비활성화
**점검:**
```
! Cisco IOS
Router# show interface
! Administratively down 확인

! Juniper Junos
user@host# show interface terse
```
**조치:**
```
! Cisco IOS
Router(config)# interface <인터페이스>
Router(config-if)# shutdown

! Radware Alteon
>> Main# /cfg/port <포트>/dis
>> Main# apply

! Juniper Junos
[edit interfaces]
user@host# set <인터페이스> disable

! Piolink PLOS
switch(config)# port <포트> status disable
switch(config)# apply
```

### N-25: TCP Keepalive 서비스 설정
**점검:**
```
! Cisco IOS
Router# show running-config
! service tcp-keepalives 확인
```
**조치:**
```
! Cisco IOS
Router(config)# service tcp-keepalives-in
Router(config)# service tcp-keepalives-out
```

### N-26: Finger 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config

! Juniper Junos
user@host# show
```
**조치:**
```
! Cisco IOS
Router(config)# no ip finger

! Juniper Junos
[edit system services]
user@host# delete finger
user@host# commit
```

### N-27: 웹 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config
! ip http server 확인
```
**조치:**
```
! Cisco IOS
Router(config)# no ip http server
Router(config)# no ip http secure-server

! Radware Alteon
>> Main# /cfg/sys/access/https/https dis
>> Main# apply

! Juniper Junos
user@host# delete system services web-management

! Piolink PLOS
(config-management-access)# http status disable
(config-management-access)# https status disable
```

### N-28: TCP/UDP Small 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config
```
**조치:**
```
! Cisco IOS
Router(config)# no service tcp-small-servers
Router(config)# no service udp-small-servers
```

### N-29: Bootp 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config
! ip bootp server 확인
```
**조치:**
```
! Cisco IOS
Router(config)# no ip bootp server
! DHCP 유지하고 BOOTP만 차단 시
Router(config)# ip dhcp bootp ignore

! Radware Alteon
>> Main# /cfg/sys/bootp dis
>> Main# apply

! Juniper Junos
[edit forwarding-options helpers bootp]
user@switch# no set interface <인터페이스> server <주소>
```

### N-30: CDP 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config
Router# show cdp
```
**조치:**
```
! Cisco IOS - 전체 비활성화
Router(config)# no cdp run
! 특정 인터페이스 비활성화
Router(config)# interface FastEthernet0/1
Router(config-if)# no cdp enable
```

### N-31: Directed-broadcast 차단
**점검:**
```
! Cisco IOS
Router# show running-config
```
**조치:**
```
! Cisco IOS
Router(config)# interface <인터페이스>
Router(config-if)# no ip directed-broadcast

! Radware Alteon
# cfg/l3/frwd > dirbr disable > apply > save

! Passport
# config vlan <vid> ip directed-broadcast > disable
```

### N-32: Source Routing 차단
**점검:**
```
! Cisco IOS / Juniper Junos
Router# show running-config
```
**조치:**
```
! Cisco IOS
Router(config)# no ip source-route

! Juniper Junos
user@host# set chassis no-source-route
```

### N-33: Proxy ARP 차단
**점검:**
```
! Cisco IOS
Router# show running-config

! Juniper Junos
user@host# show
```
**조치:**
```
! Cisco IOS
Router(config)# interface <인터페이스>
Router(config-if)# no ip proxy-arp

! Juniper Junos
[edit interfaces <인터페이스> unit <유닛>]
user@host# delete proxy-arp
```

### N-34: ICMP unreachable, redirect 차단
**점검:**
```
! Cisco IOS
Router# show running-config
! 각 인터페이스 no ip unreachables / no ip redirects 확인
```
**조치:**
```
! Cisco IOS
Router(config)# interface <인터페이스>
Router(config-if)# no ip unreachables
Router(config-if)# no ip redirects

! Juniper Junos - 전체 장비
[edit system]
user@host# set no-redirects
! 특정 인터페이스
[edit interfaces]
user@host# set <인터페이스> unit <유닛> family <패밀리> no-redirects
```

### N-35: identd 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config
```
**조치:**
```
! Cisco IOS
Router(config)# no ip identd
```

### N-36: Domain Lookup 차단
**점검:**
```
! Cisco IOS
Router# show running-config
```
**조치:**
```
! Cisco IOS
Router(config)# no ip domain lookup
```

### N-37: PAD 서비스 차단
**점검:**
```
! Cisco IOS
Router# show running-config
```
**조치:**
```
! Cisco IOS
Router(config)# no service pad
```

### N-38: mask-reply 차단
**점검:**
```
! Cisco IOS
Router# show running-config
Router# show ip interface
! "ICMP mask replies are never sent" 확인
```
**조치:**
```
! Cisco IOS
Router(config)# interface <인터페이스>
Router(config-if)# no ip mask-reply
```
