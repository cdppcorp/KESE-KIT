# Chapter 6. Web Application Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Web application vulnerabilities are assessed based on OWASP Top 10. This chapter is especially important for those developing in **Vibe Coding** environments.

```
┌─────────────────────────────────────────────────────────────────┐
│              Web Application Security Vulnerability Domains      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │   User Input    │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Input     │    │   Auth/     │    │   Access    │         │
│  │ Validation  │    │  Session    │    │  Control    │         │
│  │             │    │ Management  │    │             │         │
│  │ ┌─────────┐│    │ ┌─────────┐│    │ ┌─────────┐│         │
│  │ │SQL Inj. ││    │ │ Session ││    │ │Vertical ││         │
│  │ └─────────┘│    │ └─────────┘│    │ │Privilege││         │
│  │ ┌─────────┐│    │ ┌─────────┐│    │ │Escalation│         │
│  │ │  XSS    ││    │ │Password ││    │ └─────────┘│         │
│  │ └─────────┘│    │ │Storage  ││    │ ┌─────────┐│         │
│  │ ┌─────────┐│    │ └─────────┘│    │ │Horizontal│         │
│  │ │  CSRF   ││    │ ┌─────────┐│    │ │Privilege││         │
│  │ └─────────┘│    │ │ Cookie  ││    │ │Escalation│         │
│  └─────────────┘    │ │Security ││    │ └─────────┘│         │
│         │           │ └─────────┘│    └─────────────┘         │
│         │           └─────────────┘           │               │
│         │                   │                 │               │
│         └───────────────────┼─────────────────┘               │
│                             ▼                                    │
│                    ┌─────────────────┐                          │
│                    │ Information     │                          │
│                    │ Disclosure      │                          │
│                    │                 │                          │
│                    │ • Error messages│                          │
│                    │ • Source comments│                         │
│                    │ • Version info  │                          │
│                    └─────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Key Vulnerabilities |
|--------|---------------------|
| Input Validation | SQL Injection, XSS, CSRF |
| Auth/Session Management | Session fixation, Cookie security |
| Access Control | Privilege bypass, Path manipulation |
| Information Disclosure | Error messages, Comments, Directories |

---

## 6-1. Input Validation (SQL Injection, XSS, CSRF)

### SQL Injection

| Item | Content |
|------|---------|
| **Severity** | High |
| **Risk Level** | OWASP Top 10 A03:2021 |
| **Impact** | Data leakage, modification, deletion, system compromise |

#### Vulnerable Code Example (Python)

```python
# Vulnerable: User input directly inserted into query
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# Attack example: username = "admin' OR '1'='1"
# Resulting query: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

#### Secure Code (Parameterized Query)

```python
# Secure: Using parameterized query
def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

#### Secure Methods by Framework

| Framework | Secure Method |
|-----------|---------------|
| Django | ORM usage, `filter()`, `get()` |
| Flask-SQLAlchemy | ORM usage, `query.filter_by()` |
| Node.js (mysql2) | Prepared Statements |
| Java (JDBC) | PreparedStatement |
| PHP (PDO) | Prepared Statements |

> **WARNING**
> Even when using ORM, be careful with `raw()` or direct SQL queries.

---

### XSS (Cross-Site Scripting)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Risk Level** | OWASP Top 10 A03:2021 |
| **Types** | Stored XSS, Reflected XSS, DOM XSS |

#### Vulnerable Code Example

```html
<!-- Vulnerable: User input directly output -->
<div>Welcome, <%= user.name %>!</div>

<!-- Attack example: name = "<script>alert('XSS')</script>" -->
```

#### Secure Code (HTML Escape)

```html
<!-- Secure: HTML escape applied -->
<div>Welcome, <%= escape(user.name) %>!</div>

<!-- Or use framework auto-escaping -->
<!-- Django: {{ user.name }} (auto-escape) -->
<!-- React: {user.name} (auto-escape) -->
```

#### XSS Defense Checklist

| Item | Defense Method |
|------|----------------|
| Escape on output | HTML Entity encoding |
| Content-Type setting | `text/html; charset=utf-8` |
| HttpOnly cookies | HttpOnly flag on session cookies |
| CSP header | Content-Security-Policy configuration |

---

### CSRF (Cross-Site Request Forgery)

| Item | Content |
|------|---------|
| **Severity** | High |
| **Risk Level** | OWASP Top 10 A01:2021 |
| **Impact** | Unauthorized actions using user privileges |

#### Vulnerable Scenario

```html
<!-- On attacker's site -->
<img src="https://bank.com/transfer?to=attacker&amount=1000000" />
<!-- Automatic transfer if victim visits while logged in -->
```

#### Defense Method: CSRF Token

```html
<!-- Include CSRF token in form -->
<form method="POST" action="/transfer">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <input type="text" name="to" />
    <input type="number" name="amount" />
    <button type="submit">Transfer</button>
</form>
```

#### CSRF Defense by Framework

| Framework | Method |
|-----------|--------|
| Django | `{% csrf_token %}` |
| Flask | Flask-WTF extension |
| Spring | `_csrf.token` |
| Express | csurf middleware |

---

## 6-2. Authentication and Session Management

### Secure Session Management

| Item | Recommended Setting |
|------|---------------------|
| Session ID length | 128 bits or more |
| Session ID generation | Use cryptographic random |
| Session timeout | Within 30 minutes (critical systems) |
| Session regeneration after login | Required |

#### Session Cookie Security Settings

```python
# Django settings.py
SESSION_COOKIE_SECURE = True      # HTTPS only
SESSION_COOKIE_HTTPONLY = True    # Block JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF defense
SESSION_COOKIE_AGE = 1800         # 30 minutes
```

---

### Password Storage

| Method | Security | Recommended |
|--------|:--------:|:-----------:|
| Plaintext storage | Very vulnerable | No |
| MD5/SHA-1 | Vulnerable | No |
| SHA-256 (no salt) | Vulnerable | No |
| bcrypt/scrypt/Argon2 | Secure | Yes |

#### Secure Password Hashing (Python)

```python
import bcrypt

# Hash password
password = "user_password".encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# Verify password
if bcrypt.checkpw(password, hashed):
    print("Password match")
```

---

## 6-3. Access Control and Authorization Verification

### Vertical Privilege Escalation

| Item | Content |
|------|---------|
| **Description** | Regular user accessing admin functions |
| **Defense** | Server-side authorization verification required |

#### Vulnerable Code

```python
# Vulnerable: Admin page accessible by URL only
@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html')
```

#### Secure Code

```python
# Secure: Authorization verification added
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    return render_template('admin_users.html')
```

---

### Horizontal Privilege Escalation

| Item | Content |
|------|---------|
| **Description** | Accessing another user's data |
| **Defense** | Resource ownership verification |

#### Vulnerable Code

```python
# Vulnerable: Only checks user ID
@app.route('/user/<int:user_id>/profile')
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
```

#### Secure Code

```python
# Secure: Compare current user with requested user
@app.route('/user/<int:user_id>/profile')
@login_required
def user_profile(user_id):
    if current_user.id != user_id:
        abort(403)
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
```

---

## 6-4. Information Disclosure Prevention

### Error Message Management

| Environment | Error Display |
|-------------|---------------|
| Development | Detailed errors (for debugging) |
| Production | Generic error messages only |

#### Secure Error Handling (Django)

```python
# settings.py
DEBUG = False  # Production environment

# Custom error handlers
handler404 = 'myapp.views.custom_404'
handler500 = 'myapp.views.custom_500'
```

---

### Remove Comments and Unnecessary Information

| Remove Target | Risk |
|---------------|------|
| Developer notes in HTML comments | Logic disclosure |
| Commented-out code | Feature disclosure |
| Version information | Vulnerability identification |
| Test account information | Unauthorized access |

---

## 6-5. Security in Vibe Coding Environments

### AI Code Generation Security Checklist

Code generated by Vibe Coding (AI-based coding) requires security review.

| Review Item | Check For |
|-------------|-----------|
| SQL queries | Parameterized query usage |
| User input | Validation/escaping |
| Auth/permissions | Server-side verification |
| Sensitive info | Hardcoding |
| Dependencies | Known vulnerabilities |

### AI Prompt Security Guide

```
# Secure prompt example
"Create a user login function.
Use parameterized queries to prevent SQL Injection,
hash passwords with bcrypt,
and apply CSRF tokens."
```

> **TIP**
> Never deploy AI-generated code to production without security review.

---

### Security Automation Tools

| Tool | Purpose | Type |
|------|---------|------|
| Bandit | Python static analysis | SAST |
| ESLint (security) | JavaScript static analysis | SAST |
| OWASP ZAP | Dynamic analysis | DAST |
| npm audit | Dependency vulnerabilities | SCA |
| pip-audit | Python dependencies | SCA |

#### Usage Examples

```bash
# Python code security analysis
pip install bandit
bandit -r ./src

# JavaScript dependency vulnerability check
npm audit

# Python dependency vulnerability check
pip install pip-audit
pip-audit
```

---

## Web Application Security Testing Script

### Basic Vulnerability Testing

```python
#!/usr/bin/env python3
"""
KESE KIT - Web Application Basic Security Test
"""

import requests
import sys

def test_sql_injection(url, param):
    """SQL Injection basic test"""
    payloads = ["'", "' OR '1'='1", "1; DROP TABLE users--"]

    for payload in payloads:
        try:
            response = requests.get(url, params={param: payload}, timeout=5)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                print(f"[Vulnerable] SQL Injection possible: {payload}")
                return True
        except:
            pass

    print("[Good] SQL Injection basic test passed")
    return False

def test_xss(url, param):
    """XSS basic test"""
    payload = "<script>alert('XSS')</script>"

    try:
        response = requests.get(url, params={param: payload}, timeout=5)
        if payload in response.text:
            print(f"[Vulnerable] XSS possible: Script reflected as-is")
            return True
    except:
        pass

    print("[Good] XSS basic test passed")
    return False

def test_security_headers(url):
    """Security headers test"""
    headers_to_check = [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "X-XSS-Protection",
        "Strict-Transport-Security",
        "Content-Security-Policy"
    ]

    try:
        response = requests.get(url, timeout=5)
        missing = []

        for header in headers_to_check:
            if header not in response.headers:
                missing.append(header)

        if missing:
            print(f"[Vulnerable] Missing security headers: {', '.join(missing)}")
        else:
            print("[Good] All security headers configured")

    except Exception as e:
        print(f"[Error] Test failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_security_test.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    print(f"===== Web Security Basic Test: {target_url} =====\n")

    test_security_headers(target_url)
```

---

## Summary

| Domain | Key Defense | Priority |
|--------|-------------|:--------:|
| SQL Injection | Parameterized queries, ORM | Highest |
| XSS | Output escaping, CSP | Highest |
| CSRF | CSRF tokens | High |
| Auth/Session | Secure session management, bcrypt | Highest |
| Access Control | Server-side authorization verification | High |
| Information Disclosure | Error message management | Medium |

---

## Vibe Coding Security Summary

1. **Review AI-generated code**: Always review from security perspective
2. **Input validation**: Never trust any user input
3. **Output encoding**: Context-specific encoding for HTML, SQL, JavaScript
4. **Dependency management**: Regular vulnerability scanning
5. **Automation tool usage**: Integrate SAST, DAST tools in CI/CD

---

*Next Chapter: Chapter 7. Database (DBMS) Assessment*
