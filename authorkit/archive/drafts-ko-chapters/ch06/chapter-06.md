# 6장. 웹 애플리케이션 점검

> Part II. 기술적 취약점 점검

---

## 개요

웹 애플리케이션 취약점은 OWASP Top 10을 기반으로 점검합니다. 이 장은 특히 **바이브코딩** 환경에서 개발하는 분들에게 중요합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│             웹 애플리케이션 보안 취약점 영역                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────┐                          │
│                    │  사용자 입력    │                          │
│                    └────────┬────────┘                          │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  입력값     │    │   인증/     │    │   접근      │         │
│  │  검증       │    │  세션 관리   │    │   제어      │         │
│  │             │    │             │    │             │         │
│  │ ┌─────────┐│    │ ┌─────────┐│    │ ┌─────────┐│         │
│  │ │SQL Inj. ││    │ │세션 관리││    │ │수직 권한││         │
│  │ └─────────┘│    │ └─────────┘│    │ │상승    ││         │
│  │ ┌─────────┐│    │ ┌─────────┐│    │ └─────────┘│         │
│  │ │  XSS    ││    │ │비밀번호 ││    │ ┌─────────┐│         │
│  │ └─────────┘│    │ │저장    ││    │ │수평 권한││         │
│  │ ┌─────────┐│    │ └─────────┘│    │ │상승    ││         │
│  │ │  CSRF   ││    │ ┌─────────┐│    │ └─────────┘│         │
│  │ └─────────┘│    │ │쿠키 보안││    │             │         │
│  └─────────────┘    │ └─────────┘│    └─────────────┘         │
│         │           └─────────────┘           │               │
│         │                   │                 │               │
│         └───────────────────┼─────────────────┘               │
│                             ▼                                    │
│                    ┌─────────────────┐                          │
│                    │   정보 노출     │                          │
│                    │                 │                          │
│                    │ • 에러 메시지  │                          │
│                    │ • 소스코드 주석│                          │
│                    │ • 버전 정보    │                          │
│                    └─────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 영역 | 주요 취약점 |
|------|------------|
| 입력값 검증 | SQL Injection, XSS, CSRF |
| 인증/세션 관리 | 세션 고정, 쿠키 보안 |
| 접근제어 | 권한 우회, 경로 조작 |
| 정보노출 | 에러 메시지, 주석, 디렉터리 |

---

## 6-1. 입력값 검증 (SQL Injection, XSS, CSRF)

### SQL Injection (SQL 삽입)

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **위험도** | OWASP Top 10 A03:2021 |
| **영향** | 데이터 유출, 변조, 삭제, 시스템 침해 |

#### 취약한 코드 예시 (Python)

```python
# 취약: 사용자 입력을 직접 쿼리에 삽입
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# 공격 예시: username = "admin' OR '1'='1"
# 결과 쿼리: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

#### 안전한 코드 (Parameterized Query)

```python
# 안전: 파라미터화된 쿼리 사용
def get_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone()
```

#### 프레임워크별 안전한 방법

| 프레임워크 | 안전한 방법 |
|-----------|------------|
| Django | ORM 사용, `filter()`, `get()` |
| Flask-SQLAlchemy | ORM 사용, `query.filter_by()` |
| Node.js (mysql2) | Prepared Statements |
| Java (JDBC) | PreparedStatement |
| PHP (PDO) | Prepared Statements |

> **WARNING**
> ORM을 사용하더라도 `raw()` 또는 직접 SQL 작성 시 주의가 필요합니다.

---

### XSS (Cross-Site Scripting, 크로스사이트 스크립팅)

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **위험도** | OWASP Top 10 A03:2021 |
| **유형** | Stored XSS, Reflected XSS, DOM XSS |

#### 취약한 코드 예시

```html
<!-- 취약: 사용자 입력을 직접 출력 -->
<div>환영합니다, <%= user.name %>!</div>

<!-- 공격 예시: name = "<script>alert('XSS')</script>" -->
```

#### 안전한 코드 (HTML Escape)

```html
<!-- 안전: HTML 이스케이프 적용 -->
<div>환영합니다, <%= escape(user.name) %>!</div>

<!-- 또는 프레임워크 기본 이스케이프 활용 -->
<!-- Django: {{ user.name }} (자동 이스케이프) -->
<!-- React: {user.name} (자동 이스케이프) -->
```

#### XSS 방어 체크리스트

| 항목 | 방어 방법 |
|------|----------|
| 출력 시 이스케이프 | HTML Entity 인코딩 |
| Content-Type 설정 | `text/html; charset=utf-8` |
| HttpOnly 쿠키 | 세션 쿠키에 HttpOnly 플래그 |
| CSP 헤더 | Content-Security-Policy 설정 |

---

### CSRF (Cross-Site Request Forgery, 크로스사이트 요청 위조)

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **위험도** | OWASP Top 10 A01:2021 |
| **영향** | 사용자 권한으로 비인가 작업 수행 |

#### 취약한 시나리오

```html
<!-- 공격자 사이트에서 -->
<img src="https://bank.com/transfer?to=attacker&amount=1000000" />
<!-- 피해자가 로그인 상태로 방문하면 자동 송금 -->
```

#### 방어 방법: CSRF 토큰

```html
<!-- 폼에 CSRF 토큰 포함 -->
<form method="POST" action="/transfer">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <input type="text" name="to" />
    <input type="number" name="amount" />
    <button type="submit">송금</button>
</form>
```

#### 프레임워크별 CSRF 방어

| 프레임워크 | 방법 |
|-----------|------|
| Django | `{% csrf_token %}` |
| Flask | Flask-WTF 확장 |
| Spring | `_csrf.token` |
| Express | csurf 미들웨어 |

---

## 6-2. 인증 및 세션 관리

### 안전한 세션 관리

| 항목 | 권장 설정 |
|------|----------|
| 세션 ID 길이 | 128비트 이상 |
| 세션 ID 생성 | 암호학적 난수 사용 |
| 세션 타임아웃 | 30분 이내 (중요 시스템) |
| 로그인 후 세션 재생성 | 필수 |

#### 세션 쿠키 보안 설정

```python
# Django settings.py
SESSION_COOKIE_SECURE = True      # HTTPS만 전송
SESSION_COOKIE_HTTPONLY = True    # JavaScript 접근 차단
SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF 방어
SESSION_COOKIE_AGE = 1800         # 30분
```

---

### 비밀번호 저장

| 방법 | 안전성 | 권장 |
|------|:------:|:----:|
| 평문 저장 | 매우 취약 | X |
| MD5/SHA-1 | 취약 | X |
| SHA-256 (salt 없음) | 취약 | X |
| bcrypt/scrypt/Argon2 | 안전 | O |

#### 안전한 비밀번호 해싱 (Python)

```python
import bcrypt

# 비밀번호 해싱
password = "user_password".encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# 비밀번호 검증
if bcrypt.checkpw(password, hashed):
    print("비밀번호 일치")
```

---

## 6-3. 접근제어 및 권한 검증

### 수직적 권한 상승 (Vertical Privilege Escalation)

| 항목 | 내용 |
|------|------|
| **설명** | 일반 사용자가 관리자 기능 접근 |
| **방어** | 서버 측 권한 검증 필수 |

#### 취약한 코드

```python
# 취약: URL만으로 관리자 페이지 접근
@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html')
```

#### 안전한 코드

```python
# 안전: 권한 검증 추가
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    return render_template('admin_users.html')
```

---

### 수평적 권한 상승 (Horizontal Privilege Escalation)

| 항목 | 내용 |
|------|------|
| **설명** | 다른 사용자의 데이터에 접근 |
| **방어** | 리소스 소유권 검증 |

#### 취약한 코드

```python
# 취약: 사용자 ID만 확인
@app.route('/user/<int:user_id>/profile')
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
```

#### 안전한 코드

```python
# 안전: 현재 사용자와 요청 사용자 비교
@app.route('/user/<int:user_id>/profile')
@login_required
def user_profile(user_id):
    if current_user.id != user_id:
        abort(403)
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
```

---

## 6-4. 정보노출 방지

### 에러 메시지 관리

| 환경 | 에러 표시 |
|------|----------|
| 개발 환경 | 상세 에러 (디버깅용) |
| 운영 환경 | 일반 에러 메시지만 |

#### 안전한 에러 처리 (Django)

```python
# settings.py
DEBUG = False  # 운영 환경

# 커스텀 에러 핸들러
handler404 = 'myapp.views.custom_404'
handler500 = 'myapp.views.custom_500'
```

---

### 주석 및 불필요한 정보 제거

| 제거 대상 | 위험 |
|----------|------|
| HTML 주석의 개발자 메모 | 로직 노출 |
| 주석 처리된 코드 | 기능 노출 |
| 버전 정보 | 취약점 식별 |
| 테스트 계정 정보 | 비인가 접근 |

---

## 6-5. 바이브코딩 환경에서의 보안

### AI 코드 생성 시 보안 체크리스트

바이브코딩(AI 기반 코딩)에서 생성된 코드는 반드시 보안 검토가 필요합니다.

| 검토 항목 | 확인 사항 |
|----------|----------|
| SQL 쿼리 | 파라미터화 사용 여부 |
| 사용자 입력 | 검증/이스케이프 여부 |
| 인증/권한 | 서버 측 검증 여부 |
| 민감 정보 | 하드코딩 여부 |
| 의존성 | 알려진 취약점 여부 |

### AI 프롬프트 보안 가이드

```
# 안전한 프롬프트 예시
"사용자 로그인 기능을 만들어줘.
SQL Injection 방지를 위해 파라미터화된 쿼리를 사용하고,
비밀번호는 bcrypt로 해싱해줘.
CSRF 토큰도 적용해줘."
```

> **TIP**
> AI가 생성한 코드라도 보안 검토 없이 프로덕션에 배포하지 마세요.

---

### 보안 자동화 도구

| 도구 | 용도 | 유형 |
|------|------|------|
| Bandit | Python 정적 분석 | SAST |
| ESLint (security) | JavaScript 정적 분석 | SAST |
| OWASP ZAP | 동적 분석 | DAST |
| npm audit | 의존성 취약점 | SCA |
| pip-audit | Python 의존성 | SCA |

#### 사용 예시

```bash
# Python 코드 보안 분석
pip install bandit
bandit -r ./src

# JavaScript 의존성 취약점 검사
npm audit

# Python 의존성 취약점 검사
pip install pip-audit
pip-audit
```

---

## 웹 애플리케이션 보안 테스트 스크립트

### 기본 취약점 테스트

```python
#!/usr/bin/env python3
"""
KESE KIT - 웹 애플리케이션 기본 보안 테스트
"""

import requests
import sys

def test_sql_injection(url, param):
    """SQL Injection 기본 테스트"""
    payloads = ["'", "' OR '1'='1", "1; DROP TABLE users--"]

    for payload in payloads:
        try:
            response = requests.get(url, params={param: payload}, timeout=5)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                print(f"[취약] SQL Injection 가능성: {payload}")
                return True
        except:
            pass

    print("[양호] SQL Injection 기본 테스트 통과")
    return False

def test_xss(url, param):
    """XSS 기본 테스트"""
    payload = "<script>alert('XSS')</script>"

    try:
        response = requests.get(url, params={param: payload}, timeout=5)
        if payload in response.text:
            print(f"[취약] XSS 가능성: 스크립트가 그대로 반영됨")
            return True
    except:
        pass

    print("[양호] XSS 기본 테스트 통과")
    return False

def test_security_headers(url):
    """보안 헤더 테스트"""
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
            print(f"[취약] 누락된 보안 헤더: {', '.join(missing)}")
        else:
            print("[양호] 모든 보안 헤더 설정됨")

    except Exception as e:
        print(f"[오류] 테스트 실패: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python web_security_test.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]
    print(f"===== 웹 보안 기본 테스트: {target_url} =====\n")

    test_security_headers(target_url)
```

---

## 요약

| 영역 | 핵심 방어 | 우선순위 |
|------|----------|:--------:|
| SQL Injection | 파라미터화된 쿼리, ORM | 최우선 |
| XSS | 출력 이스케이프, CSP | 최우선 |
| CSRF | CSRF 토큰 | 높음 |
| 인증/세션 | 안전한 세션 관리, bcrypt | 최우선 |
| 접근제어 | 서버 측 권한 검증 | 높음 |
| 정보노출 | 에러 메시지 관리 | 중간 |

---

## 바이브코딩 보안 요약

1. **AI 생성 코드 검토**: 항상 보안 관점에서 리뷰
2. **입력값 검증**: 모든 사용자 입력은 신뢰하지 않음
3. **출력값 인코딩**: HTML, SQL, JavaScript 컨텍스트별 인코딩
4. **의존성 관리**: 정기적인 취약점 검사
5. **자동화 도구 활용**: SAST, DAST 도구 CI/CD 연동

---

*다음 장: 7장. 데이터베이스(DBMS) 점검*
