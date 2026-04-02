# 8장. 네트워크 장비 점검

> Part II. 기술적 취약점 점검

---

## 개요

네트워크 장비(라우터, 스위치)는 인프라의 핵심입니다. 이 장에서는 40개의 점검 항목(N-01 ~ N-40)을 다룹니다.

```
┌─────────────────────────────────────────────────────────────────┐
│              네트워크 장비 취약점 점검 영역 (40개)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │  네트워크 장비   │                          │
│                    │ 라우터 | 스위치  │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│     ┌───────────────────────┼───────────────────────┐           │
│     │           │           │           │           │           │
│     ▼           ▼           ▼           ▼           ▼           │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐         │
│ │ 계정  │  │ 접근  │  │ 패치  │  │ 로그  │  │ 기능  │         │
│ │ 관리  │  │ 관리  │  │ 관리  │  │ 관리  │  │ 관리  │         │
│ │N-01~10│  │N-11~18│  │ N-19  │  │N-20~24│  │N-25~40│         │
│ │(10개) │  │(8개)  │  │(1개)  │  │(5개)  │  │(16개) │         │
│ │       │  │       │  │       │  │       │  │       │         │
│ │• 기본 │  │• ACL  │  │• 펌웨 │  │• Sys- │  │• SNMP │         │
│ │  계정 │  │• SSH  │  │  어   │  │  log  │  │• CDP  │         │
│ │• 암호 │  │• Telnet│ │       │  │• NTP  │  │• 불필 │         │
│ │  화   │  │  차단 │  │       │  │       │  │  요   │         │
│ │       │  │       │  │       │  │       │  │  서비 │         │
│ └───────┘  └───────┘  └───────┘  └───────┘  │  스   │         │
│                                             └───────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 영역 | 항목 | 항목 수 |
|------|------|:------:|
| 계정 관리 | N-01 ~ N-10 | 10 |
| 접근 관리 | N-11 ~ N-18 | 8 |
| 패치 관리 | N-19 | 1 |
| 로그 관리 | N-20 ~ N-24 | 5 |
| 기능 관리 | N-25 ~ N-40 | 16 |

---

## 8-1. 계정 관리 (N-01 ~ N-10)

### N-01. 기본 계정 비밀번호 변경

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **판단 기준** | 양호: 기본 비밀번호 변경됨 / 취약: 기본값 사용 |

#### Cisco 장비 기본 계정

| 계정 | 기본 비밀번호 | 조치 |
|------|-------------|------|
| cisco | cisco | 변경 필수 |
| admin | admin | 변경 필수 |
| enable | (없음) | 설정 필수 |

#### 조치 방법 (Cisco IOS)

```
enable
configure terminal
username admin privilege 15 secret [강력한비밀번호]
enable secret [강력한비밀번호]
```

---

### N-04. 비밀번호 암호화 저장

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 설정 파일 내 평문 비밀번호 방지 |

#### 점검 방법 (Cisco)

```
show running-config | include password
# "password 7" 또는 평문이 보이면 취약
```

#### 조치 방법

```
configure terminal
service password-encryption
# enable password 대신 enable secret 사용
enable secret [비밀번호]
```

---

## 8-2. 접근 관리 (N-11 ~ N-18)

### N-11. 원격 접속 제한 (ACL)

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 관리 네트워크에서만 접속 허용 |

#### 조치 방법 (Cisco)

```
! 관리용 ACL 생성
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 deny any log

! VTY 라인에 적용
line vty 0 4
 access-class 10 in
 transport input ssh
```

---

### N-12. SSH 사용 (Telnet 비활성화)

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 암호화된 관리 접속 사용 |

#### 조치 방법 (Cisco)

```
! SSH 활성화
hostname Router1
ip domain-name example.com
crypto key generate rsa modulus 2048
ip ssh version 2

! Telnet 비활성화
line vty 0 4
 transport input ssh
```

---

## 8-3. 패치 관리 (N-19)

### N-19. 최신 펌웨어 적용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 알려진 취약점 패치 |

#### 버전 확인 (Cisco)

```
show version
```

> **WARNING**
> 펌웨어 업그레이드 전 반드시 현재 설정을 백업하세요.

---

## 8-4. 로그 관리 (N-20 ~ N-24)

### N-20. 로깅 설정

#### 조치 방법 (Cisco)

```
! Syslog 서버 설정
logging host 192.168.1.100
logging trap informational
logging facility local7

! 타임스탬프 추가
service timestamps log datetime msec
```

---

## 8-5. 기능 관리 (N-25 ~ N-40)

### N-25. SNMP 보안 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | SNMP를 통한 비인가 접근 방지 |

#### 조치 방법

```
! 기본 커뮤니티 삭제
no snmp-server community public
no snmp-server community private

! 복잡한 커뮤니티 설정 또는 SNMPv3 사용
snmp-server community [복잡한문자열] RO 10
snmp-server group v3group v3 priv
snmp-server user v3user v3group v3 auth sha [인증비밀번호] priv aes 256 [암호화비밀번호]
```

---

### N-30. 불필요한 서비스 비활성화

#### 비활성화 권장 서비스

```
no ip http server
no ip http secure-server
no cdp run
no ip source-route
no service tcp-small-servers
no service udp-small-servers
no ip finger
no ip bootp server
```

---

## 요약

| 영역 | 핵심 점검 항목 | 우선순위 |
|------|---------------|:--------:|
| 계정 관리 | 기본 비밀번호, 암호화 저장 | 최우선 |
| 접근 관리 | SSH 사용, ACL 설정 | 최우선 |
| 패치 관리 | 최신 펌웨어 | 높음 |
| 로그 관리 | Syslog 설정 | 중간 |
| 기능 관리 | SNMP 보안, 불필요 서비스 비활성화 | 높음 |

---

*다음 장: 9장. 보안 장비 점검*
