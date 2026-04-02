# Chapter 7. Database (DBMS) Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

DBMS is a critical asset that stores organizational core data. This chapter covers 32 assessment items (D-01 ~ D-32).

```
┌─────────────────────────────────────────────────────────────────┐
│            DBMS Vulnerability Assessment Domains (32 items)      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│       ┌─────────────────────────────────────────────────┐       │
│       │              Supported DBMS Platforms           │       │
│       │  Oracle | MySQL | MSSQL | PostgreSQL | MariaDB  │       │
│       └───────────────────────┬─────────────────────────┘       │
│                               │                                  │
│       ┌───────────────────────┼───────────────────────┐         │
│       │                       │                       │         │
│       ▼                       ▼                       ▼         │
│ ┌───────────┐          ┌───────────┐          ┌───────────┐    │
│ │  Account  │          │  Access   │          │  Option   │    │
│ │ Management│          │ Management│          │ Management│    │
│ │ D-01~D-16 │          │ D-17~D-23 │          │ D-24~D-30 │    │
│ │   (16)    │          │   (7)     │          │   (7)     │    │
│ │           │          │           │          │           │    │
│ │• Default  │          │• Remote   │          │• Security │    │
│ │  accounts │          │  access   │          │  params   │    │
│ │• Password │          │  restrict │          │• Audit    │    │
│ │  policy   │          │• Least    │          │  settings │    │
│ │• Unused   │          │  privilege│          │           │    │
│ │  accounts │          │           │          │           │    │
│ └─────┬─────┘          └─────┬─────┘          └─────┬─────┘    │
│       │                      │                      │           │
│       └──────────────────────┼──────────────────────┘           │
│                              ▼                                   │
│                       ┌───────────┐                             │
│                       │   Patch   │                             │
│                       │ Management│                             │
│                       │ D-31~D-32 │                             │
│                       │   (2)     │                             │
│                       │• Security │                             │
│                       │  patches  │                             │
│                       └───────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | D-01 ~ D-16 | 16 |
| Access Management | D-17 ~ D-23 | 7 |
| Option Management | D-24 ~ D-30 | 7 |
| Patch Management | D-31 ~ D-32 | 2 |

---

## 7-1. Account Management (D-01 ~ D-16)

### D-01. Change Default Account Password

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target DB** | Oracle, MySQL, MSSQL, PostgreSQL |
| **Criteria** | Good: Default password changed / Vulnerable: Default used |

#### Default Account List

| DBMS | Default Account | Default Password |
|------|-----------------|------------------|
| Oracle | SYS, SYSTEM | change_on_install, manager |
| MySQL | root | (empty string) |
| MSSQL | sa | (set during installation) |
| PostgreSQL | postgres | (set during installation) |

#### Assessment Method (MySQL)

```sql
-- Check accounts without password
SELECT user, host FROM mysql.user WHERE authentication_string = '';
```

#### Assessment Method (Oracle)

```sql
-- Check accounts using default password
SELECT username, account_status FROM dba_users
WHERE username IN ('SYS', 'SYSTEM', 'DBSNMP', 'SCOTT');
```

---

### D-02. Remove Unnecessary Accounts

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent unauthorized access through unused accounts |

#### Assessment Method (MySQL)

```sql
-- Check all accounts
SELECT user, host, account_locked FROM mysql.user;
```

#### Assessment Method (Oracle)

```sql
-- Check account status
SELECT username, account_status, expiry_date, lock_date
FROM dba_users
ORDER BY username;
```

---

### D-05. Configure Password Policy

| Item | Content |
|------|---------|
| **Severity** | High |
| **Recommended** | Complexity, length, expiration period |

#### MySQL Password Policy

```sql
-- Check password policy
SHOW VARIABLES LIKE 'validate_password%';

-- Configure policy
SET GLOBAL validate_password.length = 8;
SET GLOBAL validate_password.policy = MEDIUM;
```

#### Oracle Password Policy (Profile)

```sql
-- Create profile
CREATE PROFILE secure_profile LIMIT
    PASSWORD_LIFE_TIME 90
    PASSWORD_GRACE_TIME 7
    PASSWORD_REUSE_TIME 365
    PASSWORD_REUSE_MAX 12
    FAILED_LOGIN_ATTEMPTS 5
    PASSWORD_LOCK_TIME 1/24;

-- Apply profile
ALTER USER username PROFILE secure_profile;
```

---

## 7-2. Access Management (D-17 ~ D-23)

### D-17. Restrict Remote Access

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block unauthorized remote access |

#### MySQL Remote Access Restriction

```sql
-- Check accounts with remote access
SELECT user, host FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1');

-- Allow specific IP only
CREATE USER 'user'@'192.168.1.%' IDENTIFIED BY 'password';
```

#### PostgreSQL Access Control (pg_hba.conf)

```
# Allow local connections only
local   all   all                 md5
host    all   all   127.0.0.1/32  md5
# Allow specific network
host    all   all   192.168.1.0/24  md5
```

---

### D-19. Principle of Least Privilege

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Grant only minimum required privileges |

#### MySQL Permission Check

```sql
-- Check user privileges
SHOW GRANTS FOR 'username'@'host';

-- Full privilege status
SELECT * FROM mysql.user WHERE user = 'username'\G
```

> **WARNING**
> `GRANT ALL PRIVILEGES` violates least privilege principle. Grant only necessary permissions individually.

---

## 7-3. Option Management (D-24 ~ D-30)

### D-24. Configure Security-Related Parameters

#### Oracle Security Parameters

| Parameter | Recommended | Description |
|-----------|:-----------:|-------------|
| REMOTE_LOGIN_PASSWORDFILE | EXCLUSIVE | Remote password file |
| REMOTE_OS_AUTHENT | FALSE | Disable OS authentication |
| O7_DICTIONARY_ACCESSIBILITY | FALSE | Restrict data dictionary access |
| AUDIT_TRAIL | DB | Enable auditing |

#### MySQL Security Parameters

| Parameter | Recommended | Description |
|-----------|:-----------:|-------------|
| local_infile | OFF | Disable local file load |
| skip_symbolic_links | ON | Disable symbolic links |
| secure_file_priv | Specified path | Restrict file operations path |

---

## 7-4. Patch Management (D-31 ~ D-32)

### D-31. Apply Latest Security Patches

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Patch known vulnerabilities |

#### Version Check Methods

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

## 7-5. DB Assessment Scripts

### MySQL Assessment Script

```bash
#!/bin/bash
# KESE KIT - MySQL Assessment Script

MYSQL_USER="root"
MYSQL_PASS="your_password"

echo "===== MySQL Security Assessment ====="

# D-01: Accounts with empty password
echo -e "\n[D-01] Accounts with Empty Password"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host FROM mysql.user WHERE authentication_string = '';" 2>/dev/null

# D-02: All accounts list
echo -e "\n[D-02] All Accounts List"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host, account_locked FROM mysql.user;" 2>/dev/null

# D-17: Accounts with remote access
echo -e "\n[D-17] Accounts with Remote Access"
mysql -u$MYSQL_USER -p$MYSQL_PASS -e "SELECT user, host FROM mysql.user WHERE host NOT IN ('localhost', '127.0.0.1', '::1');" 2>/dev/null

echo -e "\n===== Assessment Complete ====="
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Default password change, remove unused accounts | Highest |
| Access Management | Remote access restriction, least privilege | Highest |
| Option Management | Security parameter settings | High |
| Patch Management | Apply latest patches | Highest |

---

*Next Chapter: Chapter 8. Network Equipment Assessment*
