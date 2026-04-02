# DBMS 점검 스크립트 (D-01 ~ D-26)

## 1. 계정 관리

### D-01: 기본 계정의 비밀번호, 정책 등을 변경하여 사용
**점검:**
```sql
-- Oracle: 기본 계정 사용 여부 및 정책 확인
SELECT USERNAME, ACCOUNT_STATUS, PROFILE FROM DBA_USERS;
SELECT username, account_status, lock_date, expiry_date, profile FROM dba_users WHERE account_status = 'OPEN';

-- MSSQL: sa 계정 확인
SELECT name, is_disabled FROM sys.server_principals WHERE name = 'sa';

-- MySQL: root 계정 확인
SELECT User, Host FROM mysql.user;
SHOW VARIABLES LIKE 'validate_password%';

-- PostgreSQL: 역할 확인
SELECT rolname, rolsuper FROM pg_roles;

-- Altibase
SELECT * FROM system_.sys_users_;

-- Tibero
SELECT * FROM dba_users;

-- Cubrid
SELECT name, password FROM db_user;
SELECT * FROM db_password;
```
**조치:**
```sql
-- Oracle: 비밀번호 변경 / 잠금
ALTER USER <기본계정명> IDENTIFIED BY <신규비밀번호>;
ALTER USER <기본계정명> ACCOUNT LOCK;

-- MSSQL: sa 비밀번호 변경
ALTER LOGIN sa WITH PASSWORD = '신규비밀번호';

-- MySQL 5.7
UPDATE user SET authentication_string = PASSWORD('신규비밀번호') WHERE User = 'root';
FLUSH PRIVILEGES;
-- MySQL 8.0
ALTER USER 'root'@'localhost' IDENTIFIED BY '신규비밀번호';
FLUSH PRIVILEGES;

-- Altibase
ALTER USER sys IDENTIFIED BY [신규비밀번호];

-- Tibero
ALTER USER sys IDENTIFIED BY [신규비밀번호];

-- PostgreSQL
ALTER USER postgres WITH PASSWORD '신규비밀번호';

-- Cubrid
ALTER USER "사용자계정명" PASSWORD '신규비밀번호';
```

### D-02: 불필요 계정 제거 또는 잠금설정
**점검:**
```sql
-- Oracle
SELECT USERNAME, ACCOUNT_STATUS FROM DBA_USERS;

-- MSSQL
SELECT name, is_disabled FROM sys.server_principals;

-- MySQL
SELECT User, Host FROM mysql.user;

-- Altibase
SELECT * FROM system_.sys_users_;

-- Tibero
SELECT * FROM all_users;
SELECT * FROM dba_users;

-- PostgreSQL
SELECT * FROM pg_roles;
-- 또는 명령어: \du

-- Cubrid
SELECT name, password FROM db_user;
```
**조치:**
```sql
-- Oracle
DROP USER [삭제할 계정];

-- MSSQL
EXEC sp_droplogin '삭제할 계정';

-- MySQL
DROP USER '삭제할 계정'@'호스트명';
FLUSH PRIVILEGES;

-- Altibase / Tibero
DROP USER user_name CASCADE;

-- PostgreSQL
DROP ROLE '삭제할 계정';

-- Cubrid
DROP USER [삭제할 계정];
```

### D-03: 비밀번호 사용 기간 및 복잡도 설정
**점검:**
```sql
-- Oracle
SELECT profile, resource_name, limit FROM DBA_PROFILES WHERE resource_name LIKE 'PASSWORD%';

-- MySQL
SHOW VARIABLES LIKE 'validate_password%';
SHOW VARIABLES LIKE 'default_password_lifetime';

-- Altibase
SELECT * FROM system_.sys_users_;

-- Tibero
SELECT * FROM dba_users;
SELECT * FROM dba_profiles;
```
**조치:**
```sql
-- Oracle: 비밀번호 정책 설정
ALTER PROFILE <프로파일명> LIMIT
  FAILED_LOGIN_ATTEMPTS 3
  PASSWORD_LIFE_TIME 30
  PASSWORD_REUSE_TIME 30
  PASSWORD_VERIFY_FUNCTION verify_function
  PASSWORD_GRACE_TIME 5;
ALTER USER <계정명> PROFILE <프로파일명>;

-- MSSQL: 암호 만료 강제 적용 (SSMS GUI)
-- 보안 > 로그인 > 속성 > "암호 만료 강제 적용" 설정
-- OS 암호 정책: [로컬 보안 정책] > [암호 정책] > 최대 암호 사용 기간: 60일

-- MySQL: 복잡도 정책
INSTALL COMPONENT 'file://component_validate_password';
SET GLOBAL validate_password.policy = 'MEDIUM';
SET GLOBAL validate_password.length = 8;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.number_count = 1;
SET GLOBAL validate_password.special_char_count = 1;
-- LifeTime 정책
SET GLOBAL default_password_lifetime = 90;
ALTER USER '<계정명>'@'<호스트>' PASSWORD EXPIRE INTERVAL 91 DAY;

-- Altibase
ALTER USER 계정명 LIMIT (FAILED_LOGIN_ATTEMPTS 7, PASSWORD_LOCK_TIME 7);

-- Tibero
CREATE PROFILE prof LIMIT
  failed_login_attempts 3
  password_lock_time 1/1440
  password_life_time 90
  password_reuse_time unlimited
  password_reuse_max 10
  password_grace_time 10
  password_verify_function verify_function;
```

### D-04: 관리자 권한을 필요한 계정에만 허용
**점검:**
```sql
-- Oracle: SYSDBA 권한 점검
SELECT username FROM v$pwfile_users WHERE username NOT IN (
  SELECT grantee FROM dba_role_privs WHERE granted_role='DBA'
) AND username != 'INTERNAL' AND SYSDBA = 'TRUE';
-- Admin 부적합 계정 점검
SELECT grantee, privilege FROM dba_sys_privs WHERE grantee NOT IN (
  'SYS','SYSTEM','AQ_ADMINISTRATOR_ROLE','DBA','DSYS','BACSYS','SCHEDULER_ADMIN','MSYS'
) AND admin_option = 'YES' AND grantee NOT IN (
  SELECT grantee FROM dba_role_privs WHERE granted_role='DBA'
);

-- MySQL: SUPER 권한 확인
SELECT GRANTEE FROM INFORMATION_SCHEMA.USER_PRIVILEGES WHERE PRIVILEGE_TYPE = 'SUPER';

-- PostgreSQL
SELECT * FROM pg_user;
SELECT username, usesuper FROM pg_shadow;

-- Cubrid: DBA 권한 사용자 확인
SELECT a.name FROM db_user a, table(direct_groups) AS t(roles) WHERE roles.name = 'DBA';
```
**조치:**
```sql
-- Oracle: 불필요 권한 제거
SELECT * FROM DBA_SYS_PRIVS WHERE GRANTEE = '계정명';
REVOKE <권한> FROM <계정명>;
GRANT <권한> ON <테이블명> TO <계정명>;

-- MSSQL: sysadmin 역할에서 삭제
EXEC sp_dropsrvrolemember 'user01', 'sysadmin';

-- MySQL: SUPER 권한 회수
REVOKE SUPER ON *.* FROM '<계정명>';
FLUSH PRIVILEGES;

-- PostgreSQL: 불필요 관리자 권한 회수
ALTER ROLE <계정명> NOSUPERUSER;
ALTER ROLE <계정명> NOCREATEROLE;
ALTER ROLE <계정명> NOCREATEDB;
ALTER ROLE <계정명> NOREPLICATION;
ALTER ROLE <계정명> NOBYPASSRLS;

-- Cubrid: DBA 권한 회수
REVOKE ALL PRIVILEGES ON test FROM 'GRANT_TEST';
```

### D-05: 비밀번호 재사용 제약 설정
**점검:**
```sql
-- Oracle
SELECT profile FROM DBA_PROFILES WHERE resource_name = 'PASSWORD_REUSE_MAX'
  AND limit IN ('UNLIMITED', 'NULL');
SELECT profile FROM DBA_PROFILES WHERE resource_name = 'PASSWORD_REUSE_TIME'
  AND limit IN ('UNLIMITED', 'NULL');

-- Altibase
SELECT * FROM system_.sys_users_;

-- Tibero
SELECT * FROM dba_profiles;
```
**조치:**
```sql
-- Oracle
ALTER PROFILE default LIMIT password_reuse_time 365 password_reuse_max 10;

-- Altibase
ALTER USER [계정명] LIMIT (PASSWORD_REUSE_TIME 365, PASSWORD_REUSE_MAX 10);

-- Tibero
CREATE PROFILE prof LIMIT
  password_reuse_time unlimited
  password_reuse_max 10;
```

### D-06: DB 사용자 계정 개별 부여
**점검:**
```sql
-- Oracle
SELECT username FROM dba_users ORDER BY username;

-- MySQL
SELECT User, Host FROM mysql.user;

-- PostgreSQL
SELECT * FROM pg_shadow;

-- Altibase
SELECT * FROM system_.sys_users_;
```
**조치:**
```sql
-- Oracle: 공용 계정 삭제 후 개별 계정 생성
DROP USER '공용계정';
CREATE USER '<계정명>' IDENTIFIED BY '<비밀번호>';
GRANT connect, resource TO [계정명];

-- MSSQL
EXEC sp_droplogin '공용계정';
CREATE LOGIN '생성계정' WITH PASSWORD = '비밀번호';
CREATE USER '생성계정' FOR LOGIN '생성계정';

-- MySQL
DROP USER <계정명>@<호스트>;
CREATE USER '<계정명>'@'<호스트>' IDENTIFIED BY '비밀번호';
GRANT SELECT, INSERT ON DB이름.테이블명 TO '<계정명>'@'<호스트>';
FLUSH PRIVILEGES;

-- PostgreSQL
DROP ROLE '삭제할 계정';
CREATE USER '생성할 계정';
ALTER ROLE '계정명' <권한명>;
```

### D-07: root 권한으로 서비스 구동 제한
**점검:**
```bash
# Oracle
ps -ef | grep pmon
ps -ef | grep tnslsnr

# MySQL
ps -ef | grep mysqld
cat /etc/my.cnf | grep user

# Altibase
ps -ef | grep altibase | grep -v grep
```
**조치:**
```bash
# Oracle: oracle 계정으로 전환 후 구동
su - oracle
lsnrctl start
sqlplus / as sysdba
startup

# MySQL: my.cnf [mysqld] 섹션에 user 지정
# vi /etc/my.cnf
# [mysqld]
# user = mysql

# Altibase: 전용 계정으로 소유자 변경
chown -R [계정명]:[그룹명] '[Altibase 디렉터리]'
```

### D-08: 안전한 암호화 알고리즘 사용
**점검:**
```sql
-- Oracle: 암호화 알고리즘 확인
SELECT * FROM v$parameter WHERE name LIKE '%crypto%';

-- MySQL
SHOW VARIABLES LIKE '%ssl%';
```
**조치:**
```sql
-- 안전한 암호화 알고리즘(AES-256, SHA-256 등) 사용 설정
-- DBMS별 암호화 설정은 벤더 문서 참조
```

### D-09: 로그인 실패 시 잠금정책 설정
**점검:**
```sql
-- Oracle
SELECT profile, resource_name, limit FROM DBA_PROFILES
  WHERE resource_name = 'FAILED_LOGIN_ATTEMPTS';

-- MySQL
SHOW VARIABLES LIKE 'max_connect_errors';
```
**조치:**
```sql
-- Oracle
ALTER PROFILE <프로파일명> LIMIT FAILED_LOGIN_ATTEMPTS 5;

-- MySQL
SET GLOBAL max_connect_errors = 5;
```

## 2. 접근 관리

### D-10: 원격에서 DB 서버 접속 제한
**점검:**
```sql
-- Oracle: listener.ora에서 접근 IP 제한 확인
-- MySQL
SELECT User, Host FROM mysql.user;

-- PostgreSQL: pg_hba.conf 확인
```
**조치:**
```sql
-- MySQL: 원격 접속 제한
-- 특정 IP에서만 접속 가능하도록 계정 생성
CREATE USER '<계정명>'@'<허용IP>' IDENTIFIED BY '비밀번호';
-- 모든 호스트 접근 가능 계정 삭제
DROP USER '<계정명>'@'%';
FLUSH PRIVILEGES;
```
```bash
# Oracle: $ORACLE_HOME/network/admin/sqlnet.ora
# tcp.validnode_checking = YES
# tcp.invited_nodes = (허용IP1, 허용IP2)

# PostgreSQL: pg_hba.conf에서 접근 IP 제한
# host all all <허용IP>/32 md5
```

### D-11: 시스템 테이블 접근 제한
**점검:**
```sql
-- Oracle: DBA 이외 시스템 테이블 접근 권한 확인
SELECT grantee, privilege, table_name FROM dba_tab_privs
  WHERE table_name IN (SELECT table_name FROM dba_tables WHERE owner = 'SYS');
```
**조치:**
```sql
-- Oracle: 불필요 권한 회수
REVOKE SELECT ON SYS.<테이블명> FROM <계정명>;
```

### D-12: 리스너 비밀번호 설정
**점검:**
```bash
# Oracle: listener.ora 파일 확인
cat $ORACLE_HOME/network/admin/listener.ora
```
**조치:**
```bash
# Oracle: 리스너 비밀번호 설정
lsnrctl
LSNRCTL> set current_listener <리스너명>
LSNRCTL> change_password
# Old password: (빈칸)
# New password: <비밀번호>
LSNRCTL> save_config
```

### D-13: 불필요한 ODBC/OLE-DB 데이터 소스 제거
**점검:**
```powershell
# Windows: ODBC 데이터 소스 확인
Get-OdbcDsn
```
**조치:**
```powershell
# Windows: 불필요한 ODBC 데이터 소스 제거
Remove-OdbcDsn -Name "<데이터소스명>" -DsnType "System"
```

### D-14: 주요 파일 접근 권한 설정
**점검:**
```bash
# Oracle
ls -la $ORACLE_HOME/dbs/*.ora
ls -la $ORACLE_HOME/network/admin/*.ora

# MySQL
ls -la /etc/my.cnf
ls -la /var/lib/mysql/

# PostgreSQL
ls -la /var/lib/pgsql/data/pg_hba.conf
ls -la /var/lib/pgsql/data/postgresql.conf
```
**조치:**
```bash
# Oracle: 640 이하 권한 설정
chmod 640 $ORACLE_HOME/dbs/*.ora
chmod 640 $ORACLE_HOME/network/admin/*.ora
chown oracle:dba $ORACLE_HOME/dbs/*.ora

# MySQL
chmod 640 /etc/my.cnf
chown mysql:mysql /etc/my.cnf

# PostgreSQL
chmod 600 /var/lib/pgsql/data/pg_hba.conf
chown postgres:postgres /var/lib/pgsql/data/pg_hba.conf
```

### D-15: 리스너 로그 및 trace 파일 변경 제한
**점검:**
```bash
# Oracle: listener.ora에서 ADMIN_RESTRICTIONS 확인
grep ADMIN_RESTRICTIONS $ORACLE_HOME/network/admin/listener.ora
```
**조치:**
```bash
# Oracle: listener.ora에 추가
# ADMIN_RESTRICTIONS_<리스너명> = ON
```

### D-16: Windows 인증 모드 사용
**점검:**
```sql
-- MSSQL: 인증 모드 확인
SELECT SERVERPROPERTY('IsIntegratedSecurityOnly');
-- 1: Windows 인증 모드, 0: 혼합 모드
```
**조치:**
```
-- MSSQL: SSMS > 서버 속성 > 보안 > "Windows 인증 모드" 선택
```

## 3. 옵션 관리

### D-17: Audit Table 접근 제한
**점검:**
```sql
-- Oracle: Audit 테이블 접근 권한 확인
SELECT grantee, privilege FROM dba_tab_privs WHERE table_name LIKE '%AUDIT%';
```
**조치:**
```sql
-- Oracle: 불필요 권한 회수
REVOKE SELECT ON SYS.AUD$ FROM <계정명>;
```

### D-18: DBA 계정 Role이 Public으로 설정되지 않도록 조정
**점검:**
```sql
-- Oracle: PUBLIC에 부여된 권한 확인
SELECT grantee, granted_role FROM dba_role_privs WHERE grantee = 'PUBLIC';
SELECT grantee, privilege FROM dba_sys_privs WHERE grantee = 'PUBLIC';
```
**조치:**
```sql
-- Oracle: PUBLIC에서 불필요 Role/권한 회수
REVOKE <Role명> FROM PUBLIC;
REVOKE EXECUTE ON <패키지명> FROM PUBLIC;
```

### D-19: OS_ROLES 등 FALSE 설정
**점검:**
```sql
-- Oracle
SHOW PARAMETER OS_ROLES;
SHOW PARAMETER REMOTE_OS_AUTHENTICATION;
SHOW PARAMETER REMOTE_OS_ROLES;
```
**조치:**
```sql
-- Oracle: init.ora 또는 spfile 수정
ALTER SYSTEM SET OS_ROLES = FALSE SCOPE=SPFILE;
ALTER SYSTEM SET REMOTE_OS_AUTHENTICATION = FALSE SCOPE=SPFILE;
ALTER SYSTEM SET REMOTE_OS_ROLES = FALSE SCOPE=SPFILE;
-- DB 재시작 필요
```

### D-20: 인가되지 않은 Object Owner 제한
**점검:**
```sql
-- Oracle: Object Owner 확인
SELECT owner, object_type, count(*) FROM dba_objects GROUP BY owner, object_type ORDER BY owner;
```
**조치:**
```sql
-- 불필요한 Object Owner의 객체를 적절한 스키마로 이전 또는 삭제
```

### D-21: 인가되지 않은 GRANT OPTION 사용 제한
**점검:**
```sql
-- Oracle
SELECT grantee, privilege, admin_option FROM dba_sys_privs WHERE admin_option = 'YES';
SELECT grantee, table_name, privilege, grantable FROM dba_tab_privs WHERE grantable = 'YES';
```
**조치:**
```sql
-- Oracle: ADMIN OPTION 제거 후 재부여
REVOKE <권한> FROM <계정명>;
GRANT <권한> TO <계정명>;
```

### D-22: 자원 제한 기능 TRUE 설정
**점검:**
```sql
-- Oracle
SHOW PARAMETER RESOURCE_LIMIT;
```
**조치:**
```sql
-- Oracle
ALTER SYSTEM SET RESOURCE_LIMIT = TRUE;
```

### D-23: xp_cmdshell 사용 제한
**점검:**
```sql
-- MSSQL
EXEC sp_configure 'xp_cmdshell';
```
**조치:**
```sql
-- MSSQL: xp_cmdshell 비활성화
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 0;
RECONFIGURE;
```

### D-24: Registry Procedure 권한 제한
**점검:**
```sql
-- MSSQL: 레지스트리 관련 확장 저장 프로시저 확인
SELECT name FROM sys.objects WHERE name LIKE 'xp_reg%';
```
**조치:**
```sql
-- MSSQL: public에서 실행 권한 제거
DENY EXECUTE ON xp_regread TO public;
DENY EXECUTE ON xp_regwrite TO public;
DENY EXECUTE ON xp_regdeletekey TO public;
DENY EXECUTE ON xp_regdeletevalue TO public;
DENY EXECUTE ON xp_regenumvalues TO public;
```

## 4. 패치 관리

### D-25: 주기적 보안 패치 및 벤더 권고 사항 적용
**점검:**
```sql
-- Oracle: 버전 확인
SELECT * FROM v$version;

-- MSSQL: 버전 확인
SELECT @@VERSION;

-- MySQL: 버전 확인
SELECT VERSION();

-- PostgreSQL: 버전 확인
SELECT version();
```
**조치:**
```
-- 공통: 벤더 보안 패치 사이트에서 최신 패치 확인 및 적용
-- Oracle: https://www.oracle.com/security-alerts/
-- MSSQL: https://learn.microsoft.com/ko-kr/sql/
-- MySQL: https://dev.mysql.com/downloads/
-- PostgreSQL: https://www.postgresql.org/support/security/
```

### D-26: 감사 기록 정책 설정
**점검:**
```sql
-- Oracle: Audit 설정 확인
SHOW PARAMETER AUDIT_TRAIL;
SELECT * FROM dba_stmt_audit_opts;
SELECT * FROM dba_priv_audit_opts;

-- MSSQL: 감사 설정 확인
SELECT * FROM sys.server_audits;

-- MySQL: 로그 설정 확인
SHOW VARIABLES LIKE 'general_log%';
SHOW VARIABLES LIKE 'log_bin%';

-- PostgreSQL
SHOW log_statement;
SHOW log_connections;
SHOW log_disconnections;
```
**조치:**
```sql
-- Oracle: Audit 활성화
ALTER SYSTEM SET AUDIT_TRAIL = DB SCOPE=SPFILE;
AUDIT SELECT TABLE, INSERT TABLE, UPDATE TABLE, DELETE TABLE BY ACCESS;
AUDIT CREATE SESSION;

-- MySQL: 일반 로그 활성화
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = '/var/log/mysql/general.log';

-- PostgreSQL: postgresql.conf
-- log_statement = 'all'
-- log_connections = on
-- log_disconnections = on
-- logging_collector = on
```
