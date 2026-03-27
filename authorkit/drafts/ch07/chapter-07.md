# 7장. 데이터베이스(DBMS) 점검

> Part II. 기술적 취약점 점검

---

## 개요

DBMS는 조직의 핵심 데이터를 저장하는 중요 자산입니다. 이 장에서는 32개의 점검 항목(D-01 ~ D-32)을 다룹니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                DBMS 취약점 점검 영역 (32개 항목)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│       ┌─────────────────────────────────────────────────┐       │
│       │              지원 DBMS 플랫폼                    │       │
│       │  Oracle | MySQL | MSSQL | PostgreSQL | MariaDB  │       │
│       └───────────────────────┬─────────────────────────┘       │
│                               │                                  │
│       ┌───────────────────────┼───────────────────────┐         │
│       │                       │                       │         │
│       ▼                       ▼                       ▼         │
│ ┌───────────┐          ┌───────────┐          ┌───────────┐    │
│ │  계정 관리 │          │  접근 관리 │          │  옵션 관리 │    │
│ │ D-01~D-16 │          │ D-17~D-23 │          │ D-24~D-30 │    │
│ │  (16개)   │          │  (7개)    │          │  (7개)    │    │
│ │           │          │           │          │           │    │
│ │• 기본계정 │          │• 원격접속 │          │• 보안     │    │
│ │• 비밀번호 │          │  제한     │          │  파라미터 │    │
│ │  정책     │          │• 최소권한 │          │• 감사     │    │
│ │• 불필요   │          │  원칙     │          │  설정     │    │
│ │  계정     │          │           │          │           │    │
│ └─────┬─────┘          └─────┬─────┘          └─────┬─────┘    │
│       │                      │                      │           │
│       └──────────────────────┼──────────────────────┘           │
│                              ▼                                   │
│                       ┌───────────┐                             │
│                       │  패치 관리 │                             │
│                       │ D-31~D-32 │                             │
│                       │  (2개)    │                             │
│                       │• 보안패치 │                             │
│                       └───────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 영역 | 항목 | 항목 수 |
|------|------|:------:|
| 계정 관리 | D-01 ~ D-16 | 16 |
| 접근 관리 | D-17 ~ D-23 | 7 |
| 옵션 관리 | D-24 ~ D-30 | 7 |
| 패치 관리 | D-31 ~ D-32 | 2 |

---

## 7-1. 계정 관리 (D-01 ~ D-16)

### D-01. 기본 계정 비밀번호 변경

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **대상 DB** | Oracle, MySQL, MSSQL, PostgreSQL |
| **판단 기준** | 양호: 기본 비밀번호 변경됨 / 취약: 기본값 사용 |

#### 기본 계정 목록

| DBMS | 기본 계정 | 기본 비밀번호 |
|------|----------|-------------|
| Oracle | SYS, SYSTEM | change_on_install, manager |
| MySQL | root | (빈 문자열) |
| MSSQL | sa | (설치 시 지정) |
| PostgreSQL | postgres | (설치 시 지정) |

#### 점검 방법 (MySQL)

```sql
-- 비밀번호 없는 계정 확인
SELECT user, host FROM mysql.user WHERE authentication_string = '';
```

#### 점검 방법 (Oracle)

```sql
-- 기본 비밀번호 사용 계정 확인
SELECT username, account_status FROM dba_users
WHERE username IN ('SYS', 'SYSTEM', 'DBSNMP', 'SCOTT');
```

---

### D-02. 불필요한 계정 제거

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 미사용 계정을 통한 비인가 접근 방지 |

#### 점검 방법 (MySQL)

```sql
-- 모든 계정 확인
SELECT user, host, account_locked FROM mysql.user;
```

#### 점검 방법 (Oracle)

```sql
-- 계정 상태 확인
SELECT username, account_status, expiry_date, lock_date
FROM dba_users
ORDER BY username;
```

---

### D-05. 비밀번호 정책 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **권장 설정** | 복잡성, 길이, 만료 기간 |

#### MySQL 비밀번호 정책

```sql
-- 비밀번호 정책 확인
SHOW VARIABLES LIKE 'validate_password%';

-- 정책 설정
SET GLOBAL validate_password.length = 8;
SET GLOBAL validate_password.policy = MEDIUM;
```

#### Oracle 비밀번호 정책 (프로파일)

```sql
-- 프로파일 생성
CREATE PROFILE secure_profile LIMIT
    PASSWORD_LIFE_TIME 90
    PASSWORD_GRACE_TIME 7
    PASSWORD_REUSE_TIME 365
    PASSWORD_REUSE_MAX 12
    FAILED_LOGIN_ATTEMPTS 5
    PASSWORD_LOCK_TIME 1/24;

-- 프로파일 적용
ALTER USER username PROFILE secure_profile;
```

---

## 7-2. 접근 관리 (D-17 ~ D-23)

### D-17. 원격 접속 제한

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 비인가 원격 접속 차단 |

#### MySQL 원격 접속 제한

```sql
-- 원격 접속 가능 계정 확인
SELECT user, host FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1');

-- 특정 IP만 허용
CREATE USER 'user'@'192.168.1.%' IDENTIFIED BY 'password';
```

#### PostgreSQL 접근 제어 (pg_hba.conf)

```
# 로컬 접속만 허용
local   all   all                 md5
host    all   all   127.0.0.1/32  md5
# 특정 네트워크 허용
host    all   all   192.168.1.0/24  md5
```

---

### D-19. 최소 권한 원칙

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 업무에 필요한 최소 권한만 부여 |

#### MySQL 권한 확인

```sql
-- 사용자별 권한 확인
SHOW GRANTS FOR 'username'@'host';

-- 전체 권한 현황
SELECT * FROM mysql.user WHERE user = 'username'\G
```

> **WARNING**
> `GRANT ALL PRIVILEGES`는 최소 권한 원칙에 위배됩니다. 필요한 권한만 개별 부여하세요.

---

## 7-3. 옵션 관리 (D-24 ~ D-30)

### D-24. 보안 관련 파라미터 설정

#### Oracle 보안 파라미터

| 파라미터 | 권장값 | 설명 |
|---------|:-----:|------|
| REMOTE_LOGIN_PASSWORDFILE | EXCLUSIVE | 원격 비밀번호 파일 |
| REMOTE_OS_AUTHENT | FALSE | OS 인증 비활성화 |
| O7_DICTIONARY_ACCESSIBILITY | FALSE | 데이터 딕셔너리 접근 제한 |
| AUDIT_TRAIL | DB | 감사 활성화 |

#### MySQL 보안 파라미터

| 파라미터 | 권장값 | 설명 |
|---------|:-----:|------|
| local_infile | OFF | 로컬 파일 로드 비활성화 |
| skip_symbolic_links | ON | 심볼릭 링크 비활성화 |
| secure_file_priv | 지정된 경로 | 파일 작업 경로 제한 |

---

## 7-4. 패치 관리 (D-31 ~ D-32)

### D-31. 최신 보안 패치 적용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 알려진 취약점 패치 |

#### 버전 확인 방법

```sql
-- MySQL
SELECT VERSION();

-- Oracle
SELECT * FROM V$VERSION;

-- PostgreSQL
SELECT version();

-- MSSQL
SELECT @@VERSION;
```

---

## 7-5. DB별 점검 스크립트

### MySQL 점검 스크립트

```bash
#!/bin/bash
# KESE KIT - MySQL 점검 스크립트

MYSQL_USER="root"
MYSQL_PASS="your_password"

echo "===== MySQL 보안 점검 ====="

# D-01: 빈 비밀번호 계정
echo -e "\n[D-01] 빈 비밀번호 계정"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host FROM mysql.user WHERE authentication_string = '';" 2>/dev/null

# D-02: 전체 계정 목록
echo -e "\n[D-02] 전체 계정 목록"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host, account_locked FROM mysql.user;" 2>/dev/null

# D-17: 원격 접속 가능 계정
echo -e "\n[D-17] 원격 접속 가능 계정"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1', '::1');" 2>/dev/null

echo -e "\n===== 점검 완료 ====="
```

---

## 요약

| 영역 | 핵심 점검 항목 | 우선순위 |
|------|---------------|:--------:|
| 계정 관리 | 기본 비밀번호 변경, 불필요 계정 제거 | 최우선 |
| 접근 관리 | 원격 접속 제한, 최소 권한 | 최우선 |
| 옵션 관리 | 보안 파라미터 설정 | 높음 |
| 패치 관리 | 최신 패치 적용 | 최우선 |

---

*다음 장: 8장. 네트워크 장비 점검*
