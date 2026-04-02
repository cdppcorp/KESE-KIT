# Secure Coding Guide — Overview

KISA 시큐어코딩 가이드 기반 보안약점 분류 체계입니다. 언어에 무관하게 적용 가능한 7개 카테고리, 49개 고유 CWE 매핑을 제공합니다.

## 7 Categories

| # | Category | Description | Items | CWE Count |
|---|----------|-------------|:-----:|:---------:|
| 1 | **Input Data Validation** | 외부 입력값의 검증 및 필터링 | 16 | 18 |
| 2 | **Security Features** | 인증, 암호화, 접근제어 등 보안 기능 | 16 | 16 |
| 3 | **Time and State** | 동시성, 경쟁조건, 무한루프 | 2 | 3 |
| 4 | **Error Handling** | 에러 메시지 노출, 예외 처리 | 3 | 3 |
| 5 | **Code Quality** | 널 포인터, 자원 해제, 역직렬화 | 3 | 3 |
| 6 | **Encapsulation** | 세션 데이터 보호, 디버그 코드, 접근 제어 | 4 | 5 |
| 7 | **API Misuse** | DNS 의존, 취약 API 사용 | 2 | 1 |
| | **Total** | | **46** | **49** |

## CWE Mapping Table

### 1. Input Data Validation (입력데이터 검증 및 표현)

| # | Weakness | CWE | JS | Py | Priority |
|---|----------|-----|:--:|:--:|:--------:|
| 1 | SQL Injection | CWE-89 | O | O | Critical |
| 2 | Code Injection | CWE-94, 95 | O | O | Critical |
| 3 | Path Traversal / Resource Injection | CWE-22, 99 | O | O | High |
| 4 | Cross-Site Scripting (XSS) | CWE-79 | O | O | Critical |
| 5 | OS Command Injection | CWE-78 | O | O | Critical |
| 6 | Unrestricted File Upload | CWE-434 | O | O | High |
| 7 | Open Redirect | CWE-601 | O | O | Medium |
| 8 | XML External Entity (XXE) | CWE-611 | O | O | High |
| 9 | XPath/XML Injection | CWE-643 | O | O | Medium |
| 10 | LDAP Injection | CWE-90 | O | O | Medium |
| 11 | Cross-Site Request Forgery (CSRF) | CWE-352 | O | O | High |
| 12 | Server-Side Request Forgery (SSRF) | CWE-918 | O | O | High |
| 13 | Untrusted Input for Security Decision | CWE-807 | O | O | Medium |
| 14 | HTTP Response Splitting | CWE-113 | - | O | Medium |
| 15 | Integer Overflow | CWE-190 | - | O | Medium |
| 16 | Format String Injection | CWE-134 | - | O | Medium |

### 2. Security Features (보안기능)

| # | Weakness | CWE | JS | Py | Priority |
|---|----------|-----|:--:|:--:|:--------:|
| 1 | Missing Authentication | CWE-306 | O | O | Critical |
| 2 | Improper Authorization | CWE-285 | O | O | Critical |
| 3 | Incorrect Permission Assignment | CWE-732 | O | O | High |
| 4 | Broken Crypto Algorithm | CWE-327 | O | O | High |
| 5 | Cleartext Storage / Transmission | CWE-312, 319 | O | O | High |
| 6 | Hard-coded Credentials | CWE-259, 321 | O | O | Critical |
| 7 | Inadequate Key Size | CWE-326 | O | O | Medium |
| 8 | Insufficient Randomness | CWE-330 | O | O | High |
| 9 | Weak Password Requirements | CWE-521 | O | O | Medium |
| 10 | Improper Signature Verification | CWE-347 | O | O | High |
| 11 | Improper Certificate Validation | CWE-295 | O | O | High |
| 12 | Sensitive Info in Persistent Cookie | CWE-539 | O | O | Medium |
| 13 | Sensitive Info in Comments | CWE-615 | O | O | Medium |
| 14 | Unsalted One-Way Hash | CWE-759 | O | O | Medium |
| 15 | Download Without Integrity Check | CWE-494 | O | O | Medium |
| 16 | Missing Brute Force Protection | CWE-307 | O | O | High |

### 3. Time and State (시간 및 상태)

| # | Weakness | CWE | JS | Py | Priority |
|---|----------|-----|:--:|:--:|:--------:|
| 1 | TOCTOU Race Condition | CWE-367 | - | O | Medium |
| 2 | Infinite Loop / Uncontrolled Recursion | CWE-835, 674 | O | O | Medium |

### 4. Error Handling (에러처리)

| # | Weakness | CWE | JS | Py | Priority |
|---|----------|-----|:--:|:--:|:--------:|
| 1 | Error Message Information Exposure | CWE-209 | O | O | Medium |
| 2 | Error Condition Without Action | CWE-390 | O | O | Medium |
| 3 | Improper Exception Handling | CWE-754 | O | O | Medium |

### 5. Code Quality (코드오류)

| # | Weakness | CWE | JS | Py | Priority |
|---|----------|-----|:--:|:--:|:--------:|
| 1 | NULL Pointer Dereference | CWE-476 | O | O | Medium |
| 2 | Improper Resource Shutdown | CWE-404 | O | O | Medium |
| 3 | Deserialization of Untrusted Data | CWE-502 | O | O | Critical |

### 6. Encapsulation (캡슐화)

| # | Weakness | CWE | JS | Py | Priority |
|---|----------|-----|:--:|:--:|:--------:|
| 1 | Data Leak Between Sessions | CWE-488, 543 | O | O | High |
| 2 | Active Debug Code | CWE-489 | O | O | Medium |
| 3 | Private Data Returned from Public Method | CWE-495 | O | O | Medium |
| 4 | Public Data Assigned to Private Field | CWE-496 | O | O | Medium |

### 7. API Misuse (API 오용)

| # | Weakness | CWE | JS | Py | Priority |
|---|----------|-----|:--:|:--:|:--------:|
| 1 | Reliance on DNS Lookup | CWE-350 | O | O | Medium |
| 2 | Use of Vulnerable API | - | O | O | Medium |

## Language Coverage

| Language | Source | Items | Frameworks |
|----------|--------|:-----:|------------|
| **Pseudo Code** | JS+Py merged | 46 | Language-agnostic patterns |
| JavaScript | ref-011 (KISA 2023) | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | ref-012 (KISA 2023) | 46 | Django, Flask, SQLAlchemy, cryptography, hashlib |

## Priority Legend

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | 원격 코드 실행, 인증 우회, 데이터 유출 가능 | 즉시 수정 |
| **High** | 중요 정보 노출, 권한 상승 가능 | 배포 전 수정 |
| **Medium** | 제한적 영향, 특정 조건에서 악용 가능 | 계획 수정 |
