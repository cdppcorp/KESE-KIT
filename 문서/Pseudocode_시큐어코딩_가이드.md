# 시큐어코딩 가이드 — Pseudo Code (범용)

> **기반 문서**: KISA JavaScript/Python 시큐어코딩 가이드 (2023년 개정본)
> **목적**: 언어에 무관한 범용 보안약점 패턴 제공
> **항목 수**: 46개 (7개 카테고리, 49 CWE)
> **활용**: AI 도구(Claude, Cursor, Copilot) 시큐어코딩 프롬프트, 코드 리뷰 기준

---

## 목차

- [1. 입력데이터 검증 및 표현 (Input Data Validation)](#1-입력데이터-검증-및-표현-input-data-validation) — 16개 항목
- [2. 보안기능 (Security Features)](#2-보안기능-security-features) — 16개 항목
- [3. 시간 및 상태 (Time and State)](#3-시간-및-상태-time-and-state) — 2개 항목
- [4. 에러처리 (Error Handling)](#4-에러처리-error-handling) — 3개 항목
- [5. 코드오류 (Code Quality)](#5-코드오류-code-quality) — 3개 항목
- [6. 캡슐화 (Encapsulation)](#6-캡슐화-encapsulation) — 4개 항목
- [7. API 오용 (API Misuse)](#7-api-오용-api-misuse) — 2개 항목
- [부록 A. CWE 매핑 전체 테이블](#부록-a-cwe-매핑-전체-테이블)
- [부록 B. 카테고리별 우선순위 요약](#부록-b-카테고리별-우선순위-요약)

---

## 1. 입력데이터 검증 및 표현 (Input Data Validation)

외부로부터 수신하는 모든 입력값(HTTP 파라미터, 파일, URL, XML 등)에 대해 유효성을 검증하고, 안전한 형태로 변환한 후 사용해야 합니다. 이 카테고리는 웹 애플리케이션에서 가장 빈번하게 발생하는 보안약점을 다루며, 원격 코드 실행, 데이터 유출, 서비스 거부 등 치명적 결과로 이어질 수 있습니다.

---

### 1-1. SQL 삽입 (CWE-89)

#### 가. 개요

SQL 삽입(SQL Injection)은 외부 입력값을 SQL 쿼리 문자열에 직접 결합할 때 발생합니다. 공격자가 입력값에 SQL 구문을 삽입하면 인증 우회, 데이터 유출, 데이터 변조, 심지어 운영체제 명령 실행까지 가능합니다. OWASP Top 10에서 지속적으로 상위를 차지하는 대표적인 인젝션 취약점입니다.

#### 나. 안전한 코딩기법

- 모든 SQL 쿼리에 파라미터 바인딩(Parameterized Query)을 사용합니다.
- ORM을 사용하더라도 raw query를 작성할 경우 반드시 바인딩 변수를 적용합니다.
- 입력값에 대해 화이트리스트 기반 검증을 수행하고, SQL 특수문자를 이스케이프합니다.
- 데이터베이스 계정에 최소 권한 원칙을 적용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 입력값을 쿼리에 직접 결합
userInput = request.getParameter("id")
query = "SELECT * FROM users WHERE id = " + userInput
db.execute(query)

// SAFE — 파라미터 바인딩 (인자화된 쿼리)
userInput = request.getParameter("id")
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, [userInput])
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Sequelize, Mongoose 등 ORM 사용 시에도 `literal()`, raw query에서 바인딩 필수 |
| Python | O | Django ORM의 `extra()`, `raw()` 및 SQLAlchemy `text()` 사용 시 바인딩 필수 |

---

### 1-2. 코드 삽입 (CWE-94, CWE-95)

#### 가. 개요

동적 코드 실행 함수(eval, exec, Function 생성자 등)에 외부 입력값을 전달하면 공격자가 서버에서 임의 코드를 실행할 수 있습니다. 이 취약점은 원격 코드 실행(RCE)으로 직결되며, 시스템 전체가 장악될 수 있는 가장 위험한 보안약점 중 하나입니다.

#### 나. 안전한 코딩기법

- eval(), exec(), Function() 등 동적 코드 실행 함수는 외부 입력값과 함께 사용하지 않습니다.
- 동적 계산이 필요한 경우 안전한 파서(수식 파서, JSON 파서 등)를 사용합니다.
- 허용된 연산만 화이트리스트로 정의하여 실행합니다.
- 코드 실행이 불가피한 경우 샌드박스 환경에서 격리하여 실행합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 외부 입력값을 동적 코드 실행에 사용
userInput = request.getParameter("expr")
result = eval(userInput)

// SAFE — 동적 코드 실행 대신 안전한 파서 사용
userInput = request.getParameter("expr")
result = safeParser.parse(userInput)
// 또는 허용된 연산만 화이트리스트로 실행
if userInput in ALLOWED_OPERATIONS:
    result = ALLOWED_OPERATIONS[userInput]()
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `eval()`, `Function()`, `setTimeout(string)` 등 문자열 기반 코드 실행 금지 |
| Python | O | `eval()`, `exec()`, `compile()` 및 `__import__()` 동적 호출 금지 |

---

### 1-3. 경로 조작 및 자원 삽입 (CWE-22, CWE-99)

#### 가. 개요

파일 경로에 외부 입력값을 직접 사용하면 `../` 등의 상대 경로를 통해 의도하지 않은 디렉터리에 접근할 수 있습니다. 공격자는 시스템 설정 파일, 인증 정보 파일 등 민감한 자원을 읽거나 덮어쓸 수 있으며, 자원 식별자(포트, IP 등)에 대한 삽입도 동일한 원리로 발생합니다.

#### 나. 안전한 코딩기법

- 파일 경로를 정규화(resolve/normalize)한 후 기본 디렉터리(base path) 내에 위치하는지 검증합니다.
- `../`, `..\\`, `%2e%2e` 등 경로 조작 문자열을 필터링합니다.
- 파일명에 화이트리스트 기반 검증(영숫자, 허용 확장자만)을 적용합니다.
- chroot 또는 컨테이너 격리를 통해 접근 가능 범위를 제한합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 입력값을 경로에 직접 사용
filename = request.getParameter("file")
content = file.read("/data/uploads/" + filename)
// 공격: filename = "../../etc/passwd"

// SAFE — 경로 정규화 후 기본 디렉터리 내 위치 검증
filename = request.getParameter("file")
basePath = resolve("/data/uploads/")
fullPath = resolve(basePath + "/" + filename)
if not fullPath.startsWith(basePath):
    return error("Invalid path")
content = file.read(fullPath)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `path.resolve()`, `path.normalize()` 사용 후 `startsWith()` 검증 필수 |
| Python | O | `os.path.realpath()`, `pathlib.resolve()` 사용 후 기본 경로 포함 여부 확인 |

---

### 1-4. 크로스사이트 스크립트 — XSS (CWE-79)

#### 가. 개요

크로스사이트 스크립팅(XSS)은 외부 입력값이 HTML 응답에 이스케이프 없이 포함될 때 발생합니다. 공격자가 악성 JavaScript를 삽입하면 사용자의 세션 쿠키 탈취, 키로깅, 피싱 페이지 표시 등이 가능합니다. 저장형(Stored), 반사형(Reflected), DOM 기반 XSS의 세 가지 유형이 있습니다.

#### 나. 안전한 코딩기법

- 출력 시점에 HTML 엔티티 이스케이프(`<` -> `&lt;`, `>` -> `&gt;`, `"` -> `&quot;` 등)를 적용합니다.
- 템플릿 엔진의 자동 이스케이프 기능을 활성화합니다.
- Content-Security-Policy(CSP) 헤더를 설정하여 인라인 스크립트 실행을 제한합니다.
- 클라이언트와 서버 양쪽 모두에서 입력값 검증과 출력값 이스케이프를 적용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 입력값을 HTML에 직접 삽입
userInput = request.getParameter("name")
response.write("<h1>Hello " + userInput + "</h1>")
// 공격: name = "<script>alert('xss')</script>"

// SAFE — HTML 엔티티 이스케이프 적용
userInput = request.getParameter("name")
safeInput = htmlEscape(userInput)  // < → &lt;  > → &gt;  " → &quot;
response.write("<h1>Hello " + safeInput + "</h1>")
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Express에서 EJS/Pug 등 템플릿 엔진 자동 이스케이프 확인, `innerHTML` 직접 할당 금지 |
| Python | O | Django는 기본 자동 이스케이프, Flask/Jinja2는 `|safe` 필터 사용에 주의 |

---

### 1-5. 운영체제 명령어 삽입 (CWE-78)

#### 가. 개요

시스템 명령어(shell command)에 외부 입력값을 직접 전달하면 공격자가 세미콜론(`;`), 파이프(`|`), 백틱 등의 메타문자를 이용하여 임의 명령을 실행할 수 있습니다. 서버 장악, 데이터 삭제, 악성코드 설치 등 치명적 결과를 초래합니다.

#### 나. 안전한 코딩기법

- 가능한 한 시스템 명령 호출 대신 언어 내장 라이브러리/API를 사용합니다.
- 부득이하게 명령을 실행해야 할 경우 인자를 배열로 전달하여 쉘 해석을 방지합니다.
- 입력값에 대해 화이트리스트 기반 검증을 수행합니다.
- 쉘 메타문자(`;`, `|`, `&`, `$`, 백틱 등)를 필터링합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 입력값을 쉘 명령에 직접 결합
filename = request.getParameter("file")
os.execute("cat /var/log/" + filename)
// 공격: file = "access.log; rm -rf /"

// SAFE — 쉘 호출 대신 라이브러리 API 사용
filename = request.getParameter("file")
if not isValidFilename(filename):
    return error("Invalid filename")
content = file.read("/var/log/" + filename)

// 부득이한 경우: 인자 배열로 전달 (쉘 해석 방지)
process.exec(["cat", "/var/log/" + filename])
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `child_process.exec()` 대신 `execFile()` 또는 `spawn()` 사용, `shell: false` 옵션 적용 |
| Python | O | `os.system()`, `subprocess.call(shell=True)` 금지, `subprocess.run(args_list)` 사용 |

---

### 1-6. 위험한 형식 파일 업로드 (CWE-434)

#### 가. 개요

파일 업로드 시 확장자, 크기, MIME 타입, 파일 내용을 검증하지 않으면 웹셸, 실행 파일, 악성 스크립트 등이 업로드될 수 있습니다. 업로드된 악성 파일이 웹 서버에서 실행되면 서버 전체가 장악됩니다.

#### 나. 안전한 코딩기법

- 허용된 확장자를 화이트리스트로 관리합니다(블랙리스트 방식은 우회 가능).
- 파일명을 랜덤 생성하여 원본 파일명을 사용하지 않습니다.
- 업로드 디렉터리에 실행 권한을 제거합니다.
- 파일 크기 제한을 설정합니다.
- MIME 타입과 매직 바이트(파일 헤더)를 함께 검증합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 파일 확장자 검증 없이 저장
uploadedFile = request.getFile("attachment")
uploadedFile.saveTo("/uploads/" + uploadedFile.name)

// SAFE — 화이트리스트 확장자 + 저장 경로 분리
uploadedFile = request.getFile("attachment")
extension = getExtension(uploadedFile.name).toLowerCase()
if extension not in [".jpg", ".png", ".pdf", ".docx"]:
    return error("Disallowed file type")
safeName = generateRandomName() + extension
uploadedFile.saveTo(UPLOAD_DIR + "/" + safeName)
// 업로드 디렉터리는 실행 권한 제거
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Multer 등 미들웨어에서 `fileFilter`, `limits` 설정 필수 |
| Python | O | Django `FileExtensionValidator`, Flask에서 `secure_filename()` 사용 |

---

### 1-7. 신뢰되지 않은 URL 주소로 자동접속 연결 — Open Redirect (CWE-601)

#### 가. 개요

리다이렉트 URL을 외부 입력으로 받아 검증 없이 사용하면 공격자가 사용자를 피싱 사이트나 악성 사이트로 유도할 수 있습니다. 정상 도메인의 URL로 시작하기 때문에 사용자가 의심하기 어렵습니다.

#### 나. 안전한 코딩기법

- 리다이렉트 URL을 허용된 도메인/경로의 화이트리스트와 대조합니다.
- 상대 경로만 허용하고 절대 URL을 차단합니다.
- 리다이렉트 대상을 인덱스 번호로 관리하여 직접 URL을 받지 않습니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 외부 입력 URL로 직접 리다이렉트
redirectUrl = request.getParameter("next")
response.redirect(redirectUrl)

// SAFE — 허용된 도메인/경로만 리다이렉트
redirectUrl = request.getParameter("next")
if not isInternalUrl(redirectUrl):
    redirectUrl = "/default"
response.redirect(redirectUrl)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Express `res.redirect()` 사용 전 URL 검증 필수, `//untrusted-origin.example.com` 형태의 프로토콜 상대 URL 주의 |
| Python | O | Django `is_safe_url()` (deprecated), `url_has_allowed_host_and_scheme()` 사용 |

---

### 1-8. 부적절한 XML 외부 개체 참조 — XXE (CWE-611)

#### 가. 개요

XML 파서가 외부 엔티티(External Entity)를 처리하도록 설정되어 있으면, 공격자가 DTD를 통해 서버의 로컬 파일을 읽거나 내부 네트워크에 요청(SSRF)을 보내거나 서비스 거부(Billion Laughs 공격)를 유발할 수 있습니다.

#### 나. 안전한 코딩기법

- XML 파서의 외부 엔티티 처리 기능을 비활성화합니다.
- DTD(Document Type Definition) 처리를 비활성화합니다.
- 가능하면 XML 대신 JSON 등 더 단순한 데이터 형식을 사용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 외부 엔티티 처리 허용
parser = XMLParser()
doc = parser.parse(request.body)
// 공격: <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>

// SAFE — 외부 엔티티 비활성화
parser = XMLParser()
parser.setFeature("EXTERNAL_ENTITIES", false)
parser.setFeature("DTD", false)
doc = parser.parse(request.body)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `libxmljs`는 기본 외부 엔티티 허용, `noent: false` 명시 필요 |
| Python | O | `lxml`의 `resolve_entities=False`, `defusedxml` 라이브러리 사용 권장 |

---

### 1-9. XPath / XML 삽입 (CWE-643)

#### 가. 개요

XPath 쿼리에 외부 입력값을 직접 삽입하면 공격자가 XPath 구문을 조작하여 인증을 우회하거나 XML 문서 전체의 데이터를 추출할 수 있습니다. SQL 삽입과 유사한 원리로 동작합니다.

#### 나. 안전한 코딩기법

- XPath 쿼리에 파라미터 바인딩을 사용합니다.
- 파라미터 바인딩이 불가능한 경우 XPath 특수문자(`'`, `"`, `[`, `]`, `=` 등)를 이스케이프합니다.
- 입력값에 대해 화이트리스트 기반 검증을 수행합니다.

#### 다. 코드예제

```pseudo
// UNSAFE
username = request.getParameter("user")
query = "//users/user[name='" + username + "']"
result = xmlDoc.xpath(query)

// SAFE — 파라미터 바인딩 또는 입력값 이스케이프
username = request.getParameter("user")
username = escapeXPathValue(username)
query = "//users/user[name='" + username + "']"
result = xmlDoc.xpath(query)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `xpath` 모듈에서 파라미터 바인딩 미지원 시 수동 이스케이프 필수 |
| Python | O | `lxml.etree.XPath`에서 변수 바인딩 지원, `defusedxml` 병행 사용 권장 |

---

### 1-10. LDAP 삽입 (CWE-90)

#### 가. 개요

LDAP 필터에 외부 입력값을 직접 삽입하면 공격자가 LDAP 쿼리를 조작하여 디렉터리 서비스의 전체 데이터를 조회하거나 인증을 우회할 수 있습니다. 기업 환경에서 Active Directory 등과 연동된 인증 시스템에서 주로 발생합니다.

#### 나. 안전한 코딩기법

- LDAP 특수문자(`*`, `(`, `)`, `\`, NUL 등)를 이스케이프합니다.
- 입력값에 대해 화이트리스트 기반 검증(영숫자만 허용 등)을 수행합니다.
- LDAP 쿼리 구성에 파라미터 바인딩이 가능한 라이브러리를 사용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE
username = request.getParameter("user")
filter = "(uid=" + username + ")"
results = ldap.search(baseDN, filter)

// SAFE — 특수문자 이스케이프
username = request.getParameter("user")
username = escapeLDAP(username)  // *, (, ), \, NUL 이스케이프
filter = "(uid=" + username + ")"
results = ldap.search(baseDN, filter)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `ldapjs` 등에서 `filter.escape()` 또는 수동 이스케이프 적용 |
| Python | O | `ldap3` 라이브러리의 `escape_filter_chars()` 사용 |

---

### 1-11. 크로스사이트 요청 위조 — CSRF (CWE-352)

#### 가. 개요

상태 변경(데이터 수정, 삭제, 결제 등) 요청에 CSRF 토큰 검증이 없으면, 공격자가 사용자의 브라우저를 통해 사용자의 의지와 무관한 요청을 실행할 수 있습니다. 사용자가 로그인 상태에서 악성 페이지를 방문하는 것만으로 공격이 성립합니다.

#### 나. 안전한 코딩기법

- 모든 상태 변경 요청에 CSRF 토큰을 포함하고 서버에서 검증합니다.
- SameSite 쿠키 속성을 `Strict` 또는 `Lax`로 설정하여 추가 방어를 적용합니다.
- Referer/Origin 헤더를 검증하여 요청 출처를 확인합니다.
- GET 요청으로 상태 변경을 수행하지 않습니다.

#### 다. 코드예제

```pseudo
// UNSAFE — CSRF 토큰 없이 상태 변경
router.POST("/transfer", handler(req):
    amount = req.getParameter("amount")
    toAccount = req.getParameter("to")
    transferMoney(req.user, toAccount, amount)
)

// SAFE — CSRF 토큰 검증
router.POST("/transfer", handler(req):
    if not csrfToken.verify(req.getHeader("X-CSRF-Token")):
        return error(403, "Invalid CSRF token")
    amount = req.getParameter("amount")
    toAccount = req.getParameter("to")
    transferMoney(req.user, toAccount, amount)
)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Express에서 `csurf` 미들웨어 또는 커스텀 토큰 검증 적용 |
| Python | O | Django는 CSRF 미들웨어 기본 활성화, Flask에서 `Flask-WTF` 사용 |

---

### 1-12. 서버사이드 요청 위조 — SSRF (CWE-918)

#### 가. 개요

서버가 외부 입력으로 받은 URL로 HTTP 요청을 보내면, 공격자가 내부 네트워크의 서비스(메타데이터 서버, 관리 인터페이스 등)에 접근할 수 있습니다. 클라우드 환경에서는 인스턴스 메타데이터 API(169.254.169.254)를 통해 인증 정보가 유출될 수 있어 특히 위험합니다.

#### 나. 안전한 코딩기법

- 요청 대상 URL을 화이트리스트로 관리합니다.
- 내부 IP 대역(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16)을 차단합니다.
- 허용된 프로토콜(http, https)만 허용합니다.
- DNS 재바인딩 공격을 방지하기 위해 요청 전 DNS를 미리 해석하고 IP를 검증합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 입력 URL로 서버가 직접 요청
targetUrl = request.getParameter("url")
response = http.fetch(targetUrl)
// 공격: url = "http://169.254.169.254/latest/meta-data/"

// SAFE — URL 화이트리스트 + 내부 IP 차단
targetUrl = request.getParameter("url")
parsed = parseUrl(targetUrl)
if parsed.host in BLOCKED_HOSTS or isPrivateIP(parsed.host):
    return error("Blocked URL")
if parsed.scheme not in ["http", "https"]:
    return error("Invalid scheme")
response = http.fetch(targetUrl)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `axios`, `node-fetch` 등에서 요청 전 URL 파싱 및 IP 검증 필수 |
| Python | O | `requests` 라이브러리 사용 시 URL 검증 로직을 별도 구현, `ssrf-guard` 활용 가능 |

---

### 1-13. 보안기능 결정에 사용되는 부적절한 입력값 (CWE-807)

#### 가. 개요

보안 결정(인증, 인가, 접근 제어 등)에 클라이언트가 조작할 수 있는 값(쿠키, 히든 필드, HTTP 헤더 등)을 사용하면 공격자가 해당 값을 변조하여 권한을 우회할 수 있습니다. 클라이언트 측 데이터는 항상 위변조 가능성을 전제해야 합니다.

#### 나. 안전한 코딩기법

- 보안 결정에 필요한 정보는 서버 세션에서 관리합니다.
- 클라이언트로부터 받은 역할, 권한 정보를 신뢰하지 않습니다.
- 중요 값은 서버 측에서 재검증합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 클라이언트 쿠키로 관리자 판단
isAdmin = request.getCookie("isAdmin")
if isAdmin == "true":
    showAdminPanel()

// SAFE — 서버 세션에서 권한 확인
user = session.getUser(request.sessionId)
if user.role == "admin":
    showAdminPanel()
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Express 세션(`express-session`)에서 역할 관리, 클라이언트 쿠키 값 불신 |
| Python | O | Django `request.user`, Flask `flask-login`의 서버 측 세션 사용 |

---

### 1-14. HTTP 응답분할 (CWE-113) — Python 고유

#### 가. 개요

HTTP 응답 헤더에 외부 입력값이 개행 문자(`\r\n`)와 함께 삽입되면 HTTP 응답이 분리됩니다. 공격자는 임의의 응답 헤더나 본문을 삽입하여 캐시 오염, 세션 하이재킹, XSS 등을 유발할 수 있습니다.

#### 나. 안전한 코딩기법

- HTTP 헤더 값에서 개행 문자(`\r`, `\n`)를 제거합니다.
- 헤더 값에 대해 화이트리스트 기반 검증을 수행합니다.
- 최신 프레임워크는 대부분 자동으로 개행을 차단하므로 프레임워크 버전을 최신으로 유지합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 입력값을 HTTP 헤더에 직접 삽입
location = request.getParameter("redirect")
response.setHeader("Location", location)
// 공격: redirect = "http://safe.com\r\nSet-Cookie: session=hijacked"

// SAFE — 헤더 값에서 개행 문자 제거
location = request.getParameter("redirect")
location = location.replace("\r", "").replace("\n", "")
response.setHeader("Location", location)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | - | Node.js 최신 버전에서 헤더 개행 자동 차단 (별도 항목 없음) |
| Python | O | Django/Flask 최신 버전은 자동 차단, 직접 응답 생성 시 주의 필요 |

---

### 1-15. 정수형 오버플로우 (CWE-190) — Python 고유

#### 가. 개요

정수 연산 결과가 해당 자료형의 표현 범위를 초과하면 값이 뒤집히거나 예상치 못한 동작이 발생합니다. 가격 계산, 배열 인덱스, 메모리 할당 크기 등에서 오버플로우가 발생하면 보안 검사 우회나 서비스 거부로 이어질 수 있습니다.

#### 나. 안전한 코딩기법

- 연산 전에 입력값의 범위를 검증합니다.
- 비즈니스 로직에 맞는 최솟값/최댓값 제한을 설정합니다.
- C 확장 모듈이나 외부 라이브러리 호출 시 정수 범위를 확인합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 정수 범위 검증 없이 사용
quantity = parseInt(request.getParameter("qty"))
totalPrice = quantity * unitPrice
// 공격: qty = 2147483647 → 오버플로우

// SAFE — 범위 검증 후 사용
quantity = parseInt(request.getParameter("qty"))
if quantity < 0 or quantity > MAX_QUANTITY:
    return error("Invalid quantity")
totalPrice = quantity * unitPrice
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | - | JS의 Number는 IEEE 754 부동소수점, BigInt 사용 시 주의 (별도 항목 없음) |
| Python | O | Python int는 무한 정밀도이나, C 확장/`ctypes`/`struct` 사용 시 오버플로우 발생 가능 |

---

### 1-16. 포맷 스트링 삽입 (CWE-134) — Python 고유

#### 가. 개요

포맷 스트링에 외부 입력값을 직접 사용하면 공격자가 포맷 지시자를 삽입하여 메모리 정보를 유출하거나 프로그램 동작을 변조할 수 있습니다. Python의 `format()` 메서드나 f-string에서도 객체의 속성 접근을 통한 정보 유출이 가능합니다.

#### 나. 안전한 코딩기법

- 포맷 스트링과 인자를 분리합니다.
- 외부 입력값을 포맷 스트링 자체로 사용하지 않습니다.
- 로깅 시 `logger.info("%s", user_input)` 형태로 인자를 분리합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 입력값을 포맷 스트링으로 사용
userInput = request.getParameter("msg")
log(userInput)  // Python: userInput.format() 또는 % 연산자

// SAFE — 포맷 스트링과 인자를 분리
userInput = request.getParameter("msg")
log("%s", userInput)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | - | JS에는 C 스타일 포맷 스트링이 없어 해당 취약점 미해당 (별도 항목 없음) |
| Python | O | `str.format()`, `%` 연산자에서 `{0.__class__}` 등 속성 접근 공격 주의 |

---

## 2. 보안기능 (Security Features)

인증, 인가, 암호화, 키 관리, 세션 관리 등 소프트웨어의 보안 기능과 관련된 보안약점을 다룹니다. 보안 기능이 올바르게 구현되지 않으면 인증 우회, 데이터 유출, 중간자 공격 등이 발생할 수 있습니다.

---

### 2-1. 적절한 인증 없는 중요 기능 허용 (CWE-306)

#### 가. 개요

관리자 기능, 데이터 삭제, 설정 변경 등 중요 기능에 인증 검사가 누락되면 비인가자가 해당 기능에 직접 접근할 수 있습니다. URL을 추측하거나 API 엔드포인트를 직접 호출하는 방식으로 쉽게 악용됩니다.

#### 나. 안전한 코딩기법

- 모든 중요 기능에 인증 미들웨어/데코레이터를 적용합니다.
- 인증 후 추가로 해당 기능에 대한 권한(인가) 검증을 수행합니다.
- 인증이 필요 없는 경로를 화이트리스트로 관리하고, 나머지는 기본적으로 인증을 요구합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 인증 없이 관리 기능 노출
router.POST("/admin/delete-user", handler(req):
    userId = req.getParameter("id")
    deleteUser(userId)
)

// SAFE — 인증 미들웨어 적용
router.POST("/admin/delete-user", authRequired, handler(req):
    if not req.user.hasPermission("admin"):
        return error(403)
    userId = req.getParameter("id")
    deleteUser(userId)
)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Express 미들웨어 체인에서 인증 미들웨어를 라우트 앞에 배치 |
| Python | O | Django `@login_required`, Flask `@login_required` 데코레이터 적용 |

---

### 2-2. 부적절한 인가 (CWE-285)

#### 가. 개요

인증된 사용자라도 권한 검증 없이 타인의 리소스에 접근할 수 있으면 수평적 권한 상승(Horizontal Privilege Escalation)이 발생합니다. 예를 들어, 로그인한 사용자가 URL의 ID 값만 변경하여 다른 사용자의 주문 내역이나 개인정보를 열람할 수 있습니다.

#### 나. 안전한 코딩기법

- 리소스 접근 시 요청자와 소유자의 일치 여부를 반드시 확인합니다.
- 역할 기반 접근 제어(RBAC) 또는 속성 기반 접근 제어(ABAC)를 적용합니다.
- 리소스 조회 쿼리에 현재 사용자 ID를 조건으로 포함합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 소유자 검증 없이 리소스 반환
router.GET("/orders/:id", handler(req):
    order = db.findOrder(req.params.id)
    return order
)

// SAFE — 요청자와 소유자 일치 확인
router.GET("/orders/:id", handler(req):
    order = db.findOrder(req.params.id)
    if order.userId != req.user.id:
        return error(403, "Forbidden")
    return order
)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | ORM 쿼리에 `where: { userId: req.user.id }` 조건 필수 |
| Python | O | Django `get_object_or_404(Model, pk=id, user=request.user)` 패턴 사용 |

---

### 2-3. 중요한 자원에 대한 잘못된 권한 설정 (CWE-732)

#### 가. 개요

파일, 디렉터리, 데이터베이스, API 엔드포인트 등 중요 자원에 과도한 권한을 부여하면 비인가자가 해당 자원에 접근하거나 변조할 수 있습니다. 특히 설정 파일, 키 파일, 로그 파일 등에 0777 등 과도한 권한을 부여하는 것은 위험합니다.

#### 나. 안전한 코딩기법

- 최소 권한 원칙(Principle of Least Privilege)을 적용합니다.
- 중요 파일은 소유자만 읽기/쓰기 가능하도록 설정합니다(0600).
- 디렉터리는 소유자만 접근 가능하도록 설정합니다(0700).

#### 다. 코드예제

```pseudo
// UNSAFE — 모든 사용자에게 읽기/쓰기 권한
file.setPermissions("/config/secrets.yml", "0777")

// SAFE — 소유자만 읽기/쓰기, 그룹/기타 접근 차단
file.setPermissions("/config/secrets.yml", "0600")
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `fs.chmod()`, `fs.writeFile()` 시 `mode` 옵션 명시 |
| Python | O | `os.chmod()`, `open()` 시 파일 모드 명시, `umask` 설정 확인 |

---

### 2-4. 취약한 암호화 알고리즘 사용 (CWE-327)

#### 가. 개요

DES, RC4, MD5, SHA-1 등 이미 취약성이 증명된 암호화/해시 알고리즘을 사용하면 암호화된 데이터가 해독되거나 해시 충돌이 발생할 수 있습니다. 공격자는 비교적 적은 계산 비용으로 데이터를 복호화하거나 위변조할 수 있습니다.

#### 나. 안전한 코딩기법

- 대칭 암호화: AES-256-GCM 이상을 사용합니다.
- 해시: SHA-256 이상을 사용합니다.
- 패스워드 해싱: bcrypt, scrypt, argon2 등 전용 알고리즘을 사용합니다.
- DES, 3DES, RC4, MD5, SHA-1은 사용하지 않습니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 취약한 알고리즘 사용
encrypted = crypto.encrypt("DES", data, key)
hashed = crypto.hash("MD5", password)
hashed = crypto.hash("SHA1", password)

// SAFE — 강력한 알고리즘 사용
encrypted = crypto.encrypt("AES-256-GCM", data, key)
hashed = crypto.hash("SHA-256", password)
// 패스워드는 bcrypt, scrypt, argon2 등 사용
hashed = bcrypt.hash(password, saltRounds=12)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `crypto.createCipheriv('aes-256-gcm')` 사용, `createCipher()` (deprecated) 금지 |
| Python | O | `cryptography` 라이브러리의 Fernet 또는 AES-GCM 사용, `hashlib.md5()` 보안 용도 금지 |

---

### 2-5. 암호화되지 않은 중요정보 (CWE-312, CWE-319)

#### 가. 개요

비밀번호, 개인정보, 금융정보 등 중요 정보를 평문으로 저장하거나 암호화되지 않은 채널(HTTP)로 전송하면 데이터 유출 위험이 있습니다. 네트워크 스니핑, 데이터베이스 유출 등을 통해 즉시 악용될 수 있습니다.

#### 나. 안전한 코딩기법

- 비밀번호는 bcrypt, argon2 등으로 해싱하여 저장합니다(복호화 불가 방식).
- 중요 데이터는 AES-256 등으로 암호화하여 저장합니다.
- 네트워크 전송 시 반드시 TLS/HTTPS를 사용합니다.
- HSTS 헤더를 설정하여 HTTP 다운그레이드를 방지합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 평문 저장 및 HTTP 전송
db.save("users", {password: userPassword})
http.post("http://api.example.com/login", {password: userPassword})

// SAFE — 해싱 후 저장, HTTPS 전송
hashedPassword = bcrypt.hash(userPassword, saltRounds=12)
db.save("users", {password: hashedPassword})
https.post("https://api.example.com/login", {password: userPassword})
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `bcryptjs` 또는 `argon2` 패키지 사용, Express에서 HTTPS 강제 리다이렉트 설정 |
| Python | O | `bcrypt`, `passlib` 사용, Django `SECURE_SSL_REDIRECT = True` 설정 |

---

### 2-6. 하드코드된 중요정보 (CWE-259, CWE-321)

#### 가. 개요

소스코드에 비밀번호, API 키, 암호화 키 등을 직접 기재하면, 소스코드가 유출되거나 버전 관리 시스템에 기록되어 즉시 악용됩니다. 특히 공개 저장소에 커밋된 비밀키는 자동 스캔 봇에 의해 수 분 내에 탈취될 수 있습니다.

#### 나. 안전한 코딩기법

- 환경변수(`process.env`, `os.environ`)를 통해 비밀정보를 주입합니다.
- AWS Secrets Manager, HashiCorp Vault 등 비밀 관리 도구를 사용합니다.
- `.env` 파일은 반드시 `.gitignore`에 추가합니다.
- CI/CD 파이프라인에서 시크릿 스캐닝을 적용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 소스코드에 비밀번호/키 하드코딩
DB_PASSWORD = "super_secret_123"
API_KEY = "sk-abcdef1234567890"

// SAFE — 환경변수 또는 비밀 관리 도구 사용
DB_PASSWORD = env.get("DB_PASSWORD")
API_KEY = secretManager.get("API_KEY")
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `dotenv` 패키지 사용, `process.env`에서 로드 |
| Python | O | `python-dotenv` 사용, `os.environ.get()` 또는 Django `django-environ` 사용 |

---

### 2-7. 충분하지 않은 키 길이 사용 (CWE-326)

#### 가. 개요

암호화 키의 길이가 짧으면 무차별 대입(Brute Force) 공격으로 키를 추측할 수 있습니다. 컴퓨팅 성능의 향상에 따라 이전에 안전하다고 여겨졌던 키 길이도 현재는 취약할 수 있습니다.

#### 나. 안전한 코딩기법

- RSA: 최소 2048비트, 권장 4096비트를 사용합니다.
- AES: 256비트를 사용합니다.
- ECDSA: 256비트 이상 곡선(P-256 이상)을 사용합니다.
- 1024비트 이하의 RSA 키, 128비트 미만의 대칭키는 사용하지 않습니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 짧은 키 사용
key = crypto.generateKey("RSA", 1024)
key = crypto.generateKey("AES", 64)

// SAFE — 충분한 키 길이
key = crypto.generateKey("RSA", 2048)  // 최소 2048, 권장 4096
key = crypto.generateKey("AES", 256)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `crypto.generateKeyPairSync('rsa', { modulusLength: 2048 })` 사용 |
| Python | O | `cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(key_size=2048)` |

---

### 2-8. 적절하지 않은 난수 값 사용 (CWE-330)

#### 가. 개요

세션 ID, 토큰, 비밀번호 초기화 링크 등 보안 목적으로 사용하는 값을 일반 난수 생성기(`Math.random()`, `random.random()` 등)로 생성하면 값이 예측 가능합니다. 공격자가 난수를 예측하면 세션 하이재킹, 토큰 위조 등이 가능합니다.

#### 나. 안전한 코딩기법

- 보안 목적의 난수는 반드시 암호학적 보안 난수 생성기(CSPRNG)를 사용합니다.
- JavaScript: `crypto.randomBytes()`, `crypto.getRandomValues()`
- Python: `secrets` 모듈, `os.urandom()`

#### 다. 코드예제

```pseudo
// UNSAFE — 일반 난수 사용
token = random.nextInt()
sessionId = Math.random().toString()

// SAFE — 암호학적 보안 난수 사용
token = crypto.randomBytes(32).toHex()
sessionId = crypto.secureRandom(32)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `crypto.randomBytes()` 또는 `crypto.randomUUID()` 사용, `Math.random()` 보안 용도 금지 |
| Python | O | `secrets.token_hex()`, `secrets.token_urlsafe()` 사용, `random` 모듈 보안 용도 금지 |

---

### 2-9. 취약한 패스워드 허용 (CWE-521)

#### 가. 개요

패스워드 복잡도 정책이 없거나 약하면 무차별 대입(Brute Force), 사전 공격(Dictionary Attack) 등으로 패스워드가 쉽게 추측됩니다. "123456", "password" 등 흔한 패스워드를 허용하면 계정 탈취 위험이 급격히 증가합니다.

#### 나. 안전한 코딩기법

- 최소 8자 이상의 길이를 요구합니다.
- 대문자, 소문자, 숫자, 특수문자 조합을 요구합니다.
- 흔한 패스워드 목록(breached password list)과 대조합니다.
- 패스워드 저장 시 반드시 bcrypt, argon2 등으로 해싱합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 패스워드 정책 없음
if password.length > 0:
    createAccount(username, password)

// SAFE — 복잡도 검증
if password.length < 8:
    return error("8자 이상 입력하세요")
if not regex.match("[A-Z]", password):
    return error("대문자를 포함하세요")
if not regex.match("[0-9]", password):
    return error("숫자를 포함하세요")
if not regex.match("[!@#$%]", password):
    return error("특수문자를 포함하세요")
createAccount(username, bcrypt.hash(password))
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `zxcvbn` 라이브러리로 강도 측정, 서버 측 검증 필수 (클라이언트 검증만으로 불충분) |
| Python | O | Django `AUTH_PASSWORD_VALIDATORS` 설정, `django.contrib.auth.password_validation` 활용 |

---

### 2-10. 부적절한 전자서명 확인 (CWE-347)

#### 가. 개요

JWT, XML 서명, 코드 서명 등 전자서명을 검증하지 않고 디코딩만 수행하면 공격자가 위변조된 데이터를 신뢰하게 됩니다. 특히 JWT에서 `alg: none` 공격이나 키 혼동 공격을 통해 인증을 우회할 수 있습니다.

#### 나. 안전한 코딩기법

- JWT는 반드시 서명을 검증(`verify`)한 후 페이로드를 사용합니다.
- `algorithms` 옵션을 명시하여 허용 알고리즘을 제한합니다.
- `alg: none`을 허용하지 않습니다.
- 비밀키 관리에 주의하고 주기적으로 키를 교체합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 서명 검증 없이 디코딩만 수행
payload = jwt.decode(token)  // 서명 검증 안 함
userId = payload.userId

// SAFE — 서명 검증 후 사용
payload = jwt.verify(token, SECRET_KEY)
userId = payload.userId
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `jsonwebtoken`의 `jwt.verify()` 사용, `algorithms` 옵션 명시 필수 |
| Python | O | `PyJWT`의 `jwt.decode(token, key, algorithms=["HS256"])` 사용, `options` 설정 확인 |

---

### 2-11. 부적절한 인증서 유효성 검증 (CWE-295)

#### 가. 개요

HTTPS 통신에서 SSL/TLS 인증서 검증을 비활성화하면 중간자 공격(MITM)에 노출됩니다. 공격자가 통신을 가로채 데이터를 도청하거나 변조할 수 있으며, 사용자는 이를 인지할 수 없습니다.

#### 나. 안전한 코딩기법

- 인증서 검증을 비활성화하지 않습니다(프로덕션 환경에서는 절대 금지).
- 자체 서명 인증서가 필요한 경우 CA 번들을 직접 지정합니다.
- 인증서 만료, 호스트명 불일치 등의 경고를 무시하지 않습니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 인증서 검증 비활성화
http.get("https://api.example.com", {verifySSL: false})

// SAFE — 인증서 검증 유지 (기본값)
http.get("https://api.example.com", {verifySSL: true})
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `rejectUnauthorized: false` 설정 금지, `NODE_TLS_REJECT_UNAUTHORIZED=0` 환경변수 사용 금지 |
| Python | O | `requests.get(url, verify=False)` 금지, `urllib3.disable_warnings()` 사용 금지 |

---

### 2-12. 사용자 하드디스크에 저장되는 쿠키를 통한 정보 노출 (CWE-539)

#### 가. 개요

민감 정보(역할, 인증 토큰, 개인정보 등)를 영속 쿠키에 평문으로 저장하면 브라우저 저장소를 통해 탈취될 수 있습니다. XSS 공격과 결합되면 쿠키에 저장된 모든 정보가 유출됩니다.

#### 나. 안전한 코딩기법

- 쿠키에는 세션 ID만 저장하고 실제 데이터는 서버 세션에 보관합니다.
- 쿠키에 `httpOnly`, `secure`, `sameSite` 속성을 설정합니다.
- 민감 정보는 쿠키에 저장하지 않습니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 민감 정보를 쿠키에 저장
response.setCookie("user_role", "admin")
response.setCookie("session_data", serializedUserInfo)

// SAFE — 서버 세션에 저장, 쿠키는 세션 ID만
response.setCookie("sessionId", secureSessionId, {
    httpOnly: true,
    secure: true,
    sameSite: "Strict"
})
session.set(secureSessionId, {role: "admin"})
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `express-session`의 `cookie` 옵션에 `httpOnly`, `secure`, `sameSite` 필수 설정 |
| Python | O | Django `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`, Flask `session.permanent` 관리 |

---

### 2-13. 주석문 안에 포함된 시스템 주요정보 (CWE-615)

#### 가. 개요

소스코드 주석에 비밀번호, API 키, 내부 서버 정보 등을 기재하면 소스코드 유출, 클라이언트 측 HTML/JS 주석 노출 등을 통해 민감 정보가 유출됩니다. 개발 중 임시로 기재한 정보가 삭제되지 않고 프로덕션에 배포되는 경우가 많습니다.

#### 나. 안전한 코딩기법

- 주석에 비밀번호, API 키, 서버 주소 등 민감 정보를 기재하지 않습니다.
- 접속 정보 등은 환경변수 또는 비밀 관리 도구를 통해 관리합니다.
- 배포 전 코드 리뷰에서 주석 내 민감 정보를 점검합니다.
- 시크릿 스캐닝 도구(GitGuardian, truffleHog 등)를 CI/CD에 적용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE
// TODO: 운영 DB 비밀번호는 "Passw0rd!" 입니다
// API Key: sk-1234567890abcdef

// SAFE — 주석에 민감 정보 절대 기재 금지
// DB 접속 정보는 환경변수에서 로드 (설정 가이드: wiki/db-setup 참조)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | 클라이언트 측 JS 주석은 브라우저에서 직접 열람 가능, 빌드 시 주석 제거 권장 |
| Python | O | docstring에도 민감 정보 기재 금지, `help()` 함수로 노출 가능 |

---

### 2-14. 솔트 없이 일방향 해시 함수 사용 (CWE-759)

#### 가. 개요

패스워드를 솔트(Salt) 없이 해싱하면 동일한 패스워드가 동일한 해시값을 생성합니다. 공격자는 사전에 계산된 레인보우 테이블(Rainbow Table)을 이용하여 해시값으로부터 원래 패스워드를 역추적할 수 있습니다.

#### 나. 안전한 코딩기법

- 각 패스워드마다 고유한 솔트를 생성하여 해싱합니다.
- bcrypt, scrypt, argon2 등 솔트가 내장된 알고리즘을 사용합니다.
- 솔트는 충분한 길이(최소 16바이트)의 암호학적 보안 난수를 사용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 솔트 없이 해싱
hashed = sha256(password)

// SAFE — 솔트 적용
salt = crypto.randomBytes(16)
hashed = sha256(salt + password)
// 또는 bcrypt 등 솔트 내장 알고리즘 사용
hashed = bcrypt.hash(password, saltRounds=12)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `bcryptjs`는 솔트 자동 생성, `crypto.pbkdf2Sync()` 사용 시 솔트 별도 관리 |
| Python | O | `bcrypt.gensalt()` 자동 생성, `hashlib.pbkdf2_hmac()` 사용 시 솔트 별도 생성 |

---

### 2-15. 무결성 검사 없는 코드 다운로드 (CWE-494)

#### 가. 개요

외부에서 코드, 라이브러리, 바이너리를 다운로드할 때 무결성(해시, 서명)을 검증하지 않으면 변조된 파일이 설치되어 악성코드가 실행될 수 있습니다. 공급망 공격(Supply Chain Attack)의 대표적인 경로입니다.

#### 나. 안전한 코딩기법

- 다운로드한 파일의 해시(SHA-256 이상)를 사전에 알려진 값과 비교합니다.
- 가능하면 디지털 서명을 검증합니다.
- 패키지 매니저의 무결성 검사 기능(npm `integrity`, pip `--require-hashes`)을 활용합니다.
- 신뢰할 수 있는 소스(공식 레지스트리, HTTPS)에서만 다운로드합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 체크섬 없이 다운로드
binary = http.download("https://cdn.example.com/lib.tar.gz")
install(binary)

// SAFE — 해시 검증 후 설치
binary = http.download("https://cdn.example.com/lib.tar.gz")
if sha256(binary) != EXPECTED_HASH:
    return error("Integrity check failed")
install(binary)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `package-lock.json`의 `integrity` 필드 확인, `npm audit` 정기 실행 |
| Python | O | `pip install --require-hashes`, `pipenv`/`poetry`의 lock 파일 무결성 확인 |

---

### 2-16. 반복된 인증시도 제한 기능 부재 (CWE-307)

#### 가. 개요

로그인 시도 횟수에 제한이 없으면 공격자가 자동화 도구로 무차별 대입 공격을 수행하여 패스워드를 추측할 수 있습니다. 계정 잠금이나 지연 메커니즘이 없으면 초당 수천 회의 시도가 가능합니다.

#### 나. 안전한 코딩기법

- 일정 횟수(5~10회) 이상 실패 시 계정을 임시 잠금합니다.
- 점진적 지연(Progressive Delay)을 적용합니다.
- IP 기반 또는 계정 기반 Rate Limiting을 적용합니다.
- CAPTCHA를 도입하여 자동화 공격을 방지합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 시도 횟수 무제한
router.POST("/login", handler(req):
    if authenticate(req.username, req.password):
        return success()
    return error("Invalid credentials")
)

// SAFE — 시도 횟수 제한 + 잠금
router.POST("/login", rateLimiter(maxAttempts=5, window=15min), handler(req):
    attempts = getLoginAttempts(req.username)
    if attempts >= 5:
        return error(429, "계정이 잠겼습니다. 15분 후 재시도하세요.")
    if authenticate(req.username, req.password):
        resetLoginAttempts(req.username)
        return success()
    incrementLoginAttempts(req.username)
    return error("Invalid credentials")
)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `express-rate-limit`, `rate-limiter-flexible` 미들웨어 사용 |
| Python | O | Django `django-axes`, Flask `flask-limiter` 사용 |

---

## 3. 시간 및 상태 (Time and State)

동시 실행, 경쟁 조건, 무한 루프 등 프로그램의 실행 흐름과 상태 관리에서 발생하는 보안약점을 다룹니다. 멀티스레드/멀티프로세스 환경에서 자원 접근 순서가 보장되지 않으면 보안 검사가 무효화될 수 있습니다.

---

### 3-1. 경쟁조건: 검사시점과 사용시점 — TOCTOU (CWE-367)

#### 가. 개요

리소스의 상태를 검사(Time of Check)한 후 사용(Time of Use)하기까지의 시간 차이에서 상태가 변경되면 보안 검사가 무효화됩니다. 예를 들어 파일 존재 여부를 확인한 후 읽기 전에 해당 파일이 심볼릭 링크로 교체될 수 있습니다.

#### 나. 안전한 코딩기법

- 검사와 사용을 원자적(atomic) 연산으로 수행합니다.
- 파일 핸들 기반으로 작업하여 검사와 사용 사이의 갭을 제거합니다.
- 임시 파일 생성 시 안전한 API(`mkstemp` 등)를 사용합니다.
- 잠금(lock) 메커니즘을 활용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 검사 후 사용 사이에 갭 존재
if file.exists(path) and file.isReadable(path):
    // 이 사이에 파일이 심볼릭 링크로 교체될 수 있음
    content = file.read(path)

// SAFE — 원자적 연산 또는 파일 핸들 기반 검사
try:
    handle = file.open(path, "r")
    content = handle.read()
catch FileNotFoundError:
    return error("File not found")
finally:
    handle.close()
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | - | Node.js의 비동기 특성상 TOCTOU 발생 가능성이 낮아 별도 항목 없음 |
| Python | O | `os.path.exists()` 후 `open()` 패턴 대신 직접 `open()` 시도 + 예외 처리 |

---

### 3-2. 종료되지 않는 반복문 또는 재귀 함수 (CWE-835, CWE-674)

#### 가. 개요

종료 조건이 누락되거나 도달할 수 없는 반복문/재귀 함수는 CPU와 메모리를 지속적으로 소비하여 서비스 거부(DoS)를 유발합니다. 외부 입력에 따라 반복 횟수가 결정되는 경우 공격자가 의도적으로 무한 루프를 유발할 수 있습니다.

#### 나. 안전한 코딩기법

- 모든 반복문과 재귀 함수에 명확한 종료 조건을 설정합니다.
- 재귀 깊이에 상한을 두어 스택 오버플로우를 방지합니다.
- 반복 횟수의 최댓값을 설정합니다.
- 타임아웃을 적용하여 일정 시간 이상 실행되면 강제 종료합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 종료 조건 누락
function processTree(node):
    processTree(node.left)   // 종료 조건 없음
    processTree(node.right)

// SAFE — 종료 조건 + 깊이 제한
function processTree(node, depth=0):
    if node == null or depth > MAX_DEPTH:
        return
    processTree(node.left, depth + 1)
    processTree(node.right, depth + 1)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Node.js에서 이벤트 루프 블로킹 주의, `setImmediate()`로 분할 처리 고려 |
| Python | O | `sys.setrecursionlimit()` 설정 확인, 깊은 재귀 대신 반복문 변환 권장 |

---

## 4. 에러처리 (Error Handling)

에러 메시지 노출, 예외 무시, 부적절한 예외 처리 등 오류 상황에서 발생하는 보안약점을 다룹니다. 올바르지 않은 에러 처리는 시스템 정보 유출, 후속 장애 발생, 보안 검사 우회 등으로 이어질 수 있습니다.

---

### 4-1. 오류 메시지 정보노출 (CWE-209)

#### 가. 개요

에러 발생 시 스택 트레이스, SQL 쿼리, 파일 경로, 서버 버전 등 상세 정보가 사용자에게 노출되면 공격자에게 시스템 구조와 취약점 정보를 제공하게 됩니다. 이 정보는 후속 공격(SQL 삽입, 경로 조작 등)을 위한 정찰에 활용됩니다.

#### 나. 안전한 코딩기법

- 사용자에게는 일반적인 오류 메시지만 반환합니다.
- 상세 오류 정보는 서버 측 로그에만 기록합니다.
- 프로덕션 환경에서 디버그 모드를 비활성화합니다.
- 에러 응답에 일관된 형식을 사용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 스택 트레이스를 그대로 반환
try:
    result = db.query(sql)
catch error:
    response.send(500, error.stackTrace)

// SAFE — 일반 메시지만 반환, 상세 로그는 서버에 기록
try:
    result = db.query(sql)
catch error:
    logger.error(error.stackTrace)
    response.send(500, "서버 오류가 발생했습니다.")
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Express `app.use(errorHandler)` 에서 `stack` 속성 제거, `NODE_ENV=production` 설정 |
| Python | O | Django `DEBUG = False`, Flask `app.debug = False` 프로덕션 필수 설정 |

---

### 4-2. 오류상황 대응 부재 (CWE-390)

#### 가. 개요

예외를 포착한 후 아무런 처리를 하지 않으면(빈 catch 블록) 오류가 무시되어 프로그램이 비정상 상태에서 계속 실행됩니다. 설정 파일 로드 실패, 인증 검증 실패 등이 무시되면 보안 검사가 건너뛰어지는 결과를 초래합니다.

#### 나. 안전한 코딩기법

- 모든 catch 블록에서 최소한 로깅을 수행합니다.
- 복구 가능한 오류는 기본값 적용 또는 재시도를 수행합니다.
- 복구 불가능한 오류는 예외를 재발생(re-throw)시킵니다.
- 빈 catch 블록은 코드 리뷰에서 반드시 지적합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 예외를 무시
try:
    config = file.read("config.yml")
catch error:
    pass  // 아무 처리 없음

// SAFE — 적절한 처리 또는 기본값 적용
try:
    config = file.read("config.yml")
catch FileNotFoundError:
    logger.warn("Config not found, using defaults")
    config = DEFAULT_CONFIG
catch error:
    logger.error("Config load failed: " + error.message)
    throw error  // 재발생
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | ESLint `no-empty` 규칙으로 빈 catch 블록 탐지, Promise `.catch()` 누락 주의 |
| Python | O | `except: pass` 패턴 금지, `pylint` / `flake8`으로 빈 except 탐지 |

---

### 4-3. 부적절한 예외 처리 (CWE-754)

#### 가. 개요

지나치게 넓은 예외 처리(catch-all)는 예기치 않은 오류를 숨겨 디버깅을 어렵게 하고 보안 문제를 은폐합니다. 반대로 필요한 예외를 처리하지 않으면 프로그램이 비정상 종료됩니다. 예외는 구체적으로 분리하여 각각 적절히 처리해야 합니다.

#### 나. 안전한 코딩기법

- 예외를 구체적인 타입별로 분리하여 처리합니다.
- 범용 예외(`Exception`, `Error`)는 최상위 핸들러에서만 사용합니다.
- 각 예외 타입에 맞는 복구 전략을 적용합니다.
- 예상치 못한 예외는 로깅 후 안전하게 종료합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 모든 예외를 한꺼번에 처리
try:
    data = parse(input)
    result = process(data)
    save(result)
catch Exception:
    return error("Something went wrong")

// SAFE — 예외를 구체적으로 분리 처리
try:
    data = parse(input)
catch ParseError as e:
    return error("Invalid input format")
try:
    result = process(data)
    save(result)
catch DatabaseError as e:
    logger.error("DB error: " + e.message)
    return error("Processing failed")
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `catch(e)` 에서 `e instanceof TypeError` 등으로 구체적 분기, `async/await` 예외 전파 주의 |
| Python | O | `except Exception` 대신 `except (ValueError, KeyError)` 등 구체적 예외 지정 |

---

## 5. 코드오류 (Code Quality)

null 참조, 자원 미해제, 안전하지 않은 역직렬화 등 코드 품질과 관련된 보안약점을 다룹니다. 코드 오류는 프로그램 비정상 종료, 리소스 고갈, 원격 코드 실행 등의 보안 문제로 이어질 수 있습니다.

---

### 5-1. Null Pointer 역참조 (CWE-476)

#### 가. 개요

null 또는 undefined 값을 참조하면 프로그램이 비정상 종료됩니다. 웹 서비스에서는 서비스 거부(DoS)로 이어지며, 공격자가 의도적으로 null이 반환되는 조건을 유발하여 서비스를 중단시킬 수 있습니다.

#### 나. 안전한 코딩기법

- 외부 입력이나 데이터베이스 조회 결과를 사용하기 전에 null 체크를 수행합니다.
- Optional Chaining(`?.`), Null Coalescing(`??`) 등 안전한 접근 연산자를 활용합니다.
- 함수 반환값의 null 가능성을 문서화하고 호출부에서 처리합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — null 체크 없이 사용
user = db.findUser(userId)
name = user.name  // user가 null이면 크래시

// SAFE — null 체크 후 사용
user = db.findUser(userId)
if user == null:
    return error(404, "User not found")
name = user.name
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `?.` (Optional Chaining), `??` (Nullish Coalescing) 활용, TypeScript strict null checks 권장 |
| Python | O | `if obj is None:` 체크, `getattr(obj, 'attr', default)` 안전 접근 패턴 |

---

### 5-2. 부적절한 자원 해제 (CWE-404)

#### 가. 개요

파일 핸들, 데이터베이스 연결, 네트워크 소켓 등의 리소스를 사용 후 해제하지 않으면 리소스 고갈(Resource Exhaustion)이 발생합니다. 커넥션 풀이 고갈되면 서비스 전체가 중단될 수 있으며, 파일 디스크립터 부족은 시스템 전반에 영향을 줍니다.

#### 나. 안전한 코딩기법

- `finally` 블록에서 리소스를 해제합니다.
- 언어별 자동 해제 구문을 사용합니다(Python: `with`, JS: `try-finally`, Java: `try-with-resources`).
- 커넥션 풀을 사용하여 리소스 관리를 자동화합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 리소스 해제 누락
connection = db.connect()
result = connection.query(sql)
// connection.close() 누락 → 커넥션 풀 고갈

// SAFE — finally 또는 컨텍스트 매니저로 확실히 해제
connection = db.connect()
try:
    result = connection.query(sql)
finally:
    connection.close()

// 또는 언어별 자동 해제 구문 사용
// Python: with db.connect() as conn:
// JS: using 또는 try-finally
// Java: try-with-resources
// C#: using statement
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `try-finally` 패턴 사용, `stream.destroy()`, DB 풀의 `release()` 호출 확인 |
| Python | O | `with` 구문(Context Manager) 사용, `__enter__`/`__exit__` 프로토콜 활용 |

---

### 5-3. 신뢰할 수 없는 데이터의 역직렬화 (CWE-502)

#### 가. 개요

신뢰할 수 없는 출처의 데이터를 역직렬화하면 공격자가 조작된 직렬화 데이터를 통해 임의 코드를 실행할 수 있습니다. Python의 `pickle`, Java의 `ObjectInputStream`, JS의 `node-serialize` 등은 역직렬화 과정에서 코드를 실행할 수 있어 매우 위험합니다.

#### 나. 안전한 코딩기법

- 외부 입력에 대해 `pickle`, `node-serialize` 등 코드 실행 가능한 역직렬화를 사용하지 않습니다.
- JSON 등 코드 실행이 불가능한 데이터 형식을 사용합니다.
- 역직렬화 후 스키마 검증을 수행합니다.
- 부득이하게 역직렬화가 필요한 경우 허용 클래스를 화이트리스트로 제한합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 외부 데이터를 직접 역직렬화
data = request.body
obj = deserialize(data)  // Python: pickle.loads(), JS: node-serialize

// SAFE — JSON 등 안전한 포맷만 사용
data = request.body
obj = JSON.parse(data)  // 코드 실행 불가능한 포맷
// 스키마 검증 추가
if not schema.validate(obj):
    return error("Invalid data format")
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `node-serialize` 사용 금지, `JSON.parse()` 사용, 입력 크기 제한 설정 |
| Python | O | `pickle.loads()` 외부 입력에 사용 금지, `json.loads()` 사용, `yaml.safe_load()` 사용 |

---

## 6. 캡슐화 (Encapsulation)

세션 데이터 보호, 디버그 코드 관리, 내부 데이터 접근 제어 등 정보 은닉과 관련된 보안약점을 다룹니다. 캡슐화가 제대로 이루어지지 않으면 내부 정보가 외부에 노출되거나 의도치 않은 데이터 변조가 발생합니다.

---

### 6-1. 잘못된 세션에 의한 데이터 정보 노출 (CWE-488, CWE-543)

#### 가. 개요

사용자별 데이터를 전역 변수나 정적 변수에 저장하면, 동시 요청 처리 시 다른 사용자의 데이터가 덮어씌워져 데이터가 교차 노출됩니다. 멀티스레드/멀티프로세스 웹 서버 환경에서 특히 위험합니다.

#### 나. 안전한 코딩기법

- 사용자 데이터는 요청(request) 스코프 또는 세션 스코프의 변수에 저장합니다.
- 전역/정적 변수에 사용자별 데이터를 저장하지 않습니다.
- 스레드 로컬 저장소(Thread Local Storage)를 활용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 전역/정적 변수에 사용자 데이터 저장
global currentUser = null

handler(req):
    currentUser = req.user  // 동시 요청 시 다른 사용자 데이터로 덮어씌워짐
    return "Hello " + currentUser.name

// SAFE — 요청/세션 스코프 변수 사용
handler(req):
    currentUser = req.user  // 요청별 로컬 변수
    return "Hello " + currentUser.name
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | Node.js는 단일 스레드이나 모듈 스코프 변수 공유 주의, `AsyncLocalStorage` 활용 |
| Python | O | Flask의 `g` 객체, Django의 `request` 객체 활용, 전역 변수에 사용자 데이터 저장 금지 |

---

### 6-2. 제거되지 않고 남은 디버그 코드 (CWE-489)

#### 가. 개요

개발 중 사용한 디버그 코드(console.log, print, 디버그 모드 활성화 등)가 프로덕션에 남으면 비밀번호, 토큰, 내부 구조 등 민감 정보가 로그를 통해 노출됩니다. 디버그 엔드포인트가 남아 있으면 공격 표면이 확대됩니다.

#### 나. 안전한 코딩기법

- 배포 전 코드 리뷰에서 디버그 코드를 점검합니다.
- 로그 레벨을 환경에 따라 분기합니다(개발: DEBUG, 프로덕션: WARN 이상).
- 린트 규칙(`no-console` 등)을 적용하여 디버그 코드를 탐지합니다.
- 프로덕션 빌드에서 디버그 코드를 자동 제거합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 디버그 코드 잔존
console.log("DEBUG: user password = " + password)
app.config.DEBUG = true

// SAFE — 디버그 코드 제거 또는 환경 분기
if env.isDevelopment():
    logger.debug("User login attempt: " + username)
// 프로덕션에서는 DEBUG 모드 비활성화
app.config.DEBUG = env.get("DEBUG", false)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | ESLint `no-console` 규칙 적용, webpack/Terser의 `drop_console` 옵션 사용 |
| Python | O | `logging` 모듈 사용, `print()` 대신 `logger.debug()` 사용, 프로덕션 로그 레벨 설정 |

---

### 6-3. Public 메소드로부터 반환된 Private 배열 (CWE-495)

#### 가. 개요

클래스 내부의 배열이나 객체의 참조를 public 메서드에서 직접 반환하면, 외부 코드가 반환된 참조를 통해 내부 데이터를 직접 수정할 수 있습니다. 이로 인해 캡슐화가 깨지고 데이터 무결성이 훼손됩니다.

#### 나. 안전한 코딩기법

- 내부 데이터를 반환할 때 깊은 복사(Deep Copy)를 수행합니다.
- 불변(Immutable) 객체로 래핑하여 반환합니다.
- 방어적 복사(Defensive Copy) 패턴을 적용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 내부 배열의 참조를 직접 반환
class UserService:
    private users = [...]
    
    function getUsers():
        return this.users  // 외부에서 수정 가능

// SAFE — 복사본 반환
class UserService:
    private users = [...]
    
    function getUsers():
        return copy(this.users)  // 깊은 복사
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `structuredClone()`, `JSON.parse(JSON.stringify())`, 스프레드 연산자(`[...arr]`) 사용 |
| Python | O | `copy.deepcopy()`, 리스트 슬라이싱(`list[:]`), `dataclasses.field(default_factory)` 사용 |

---

### 6-4. Private 배열에 Public 데이터 할당 (CWE-496)

#### 가. 개요

외부에서 전달받은 배열이나 객체를 내부 필드에 직접 할당하면, 외부에서 원본 참조를 통해 내부 데이터를 변경할 수 있습니다. 이는 6-3(Private 배열 반환)의 반대 방향 문제입니다.

#### 나. 안전한 코딩기법

- 외부 데이터를 내부에 할당할 때 깊은 복사를 수행합니다.
- setter 메서드에서 방어적 복사를 적용합니다.
- 입력 데이터의 유효성을 검증한 후 복사본을 저장합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 외부 참조를 그대로 내부에 할당
class Config:
    private settings = {}
    
    function setSettings(newSettings):
        this.settings = newSettings  // 외부에서 변경 시 내부도 변경

// SAFE — 복사본을 할당
class Config:
    private settings = {}
    
    function setSettings(newSettings):
        this.settings = copy(newSettings)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `structuredClone(newSettings)` 또는 `Object.freeze()` 적용 |
| Python | O | `copy.deepcopy(new_settings)` 사용, `@dataclass(frozen=True)` 불변 객체 활용 |

---

## 7. API 오용 (API Misuse)

API를 의도와 다르게 사용하거나, 보안상 취약한 API를 사용하여 발생하는 보안약점을 다룹니다. DNS 기반 보안 결정, deprecated/취약 함수 사용 등이 해당됩니다.

---

### 7-1. DNS lookup에 의존한 보안결정 (CWE-350)

#### 가. 개요

접근 제어나 인증에 DNS 역방향 조회 결과(호스트명)를 사용하면, 공격자가 DNS 스푸핑을 통해 보안 검사를 우회할 수 있습니다. DNS 레코드는 공격자가 조작할 수 있으므로 신뢰할 수 없는 정보입니다.

#### 나. 안전한 코딩기법

- 접근 제어에 DNS 호스트명 대신 IP 주소를 직접 사용합니다.
- IP 기반 화이트리스트를 관리합니다.
- 가능하면 인증서 기반 상호 인증(mTLS)을 적용합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — 역방향 DNS로 접근 제어
hostname = dns.reverseLookup(request.remoteIP)
if hostname == "trusted.internal.com":
    allowAccess()

// SAFE — IP 주소 직접 비교
clientIP = request.remoteIP
if clientIP in TRUSTED_IP_LIST:
    allowAccess()
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `dns.reverse()` 결과를 보안 결정에 사용 금지, `req.ip` 또는 `req.socket.remoteAddress` 사용 |
| Python | O | `socket.gethostbyaddr()` 결과를 보안 결정에 사용 금지, `request.META['REMOTE_ADDR']` 사용 |

---

### 7-2. 취약한 API 사용

#### 가. 개요

보안 취약점이 알려져 있거나 deprecated된 API/함수를 사용하면 공격자가 해당 취약점을 악용할 수 있습니다. 라이브러리의 구 버전에 존재하는 취약점(CVE)이 패치되지 않은 채 사용되는 경우가 대표적입니다.

#### 나. 안전한 코딩기법

- deprecated된 API를 최신 대체 API로 교체합니다.
- 사용 중인 라이브러리의 보안 권고(Security Advisory)를 정기적으로 확인합니다.
- 의존성 취약점 스캐닝 도구(`npm audit`, `pip-audit`, `safety`)를 CI/CD에 적용합니다.
- 알려진 취약점이 있는 라이브러리 버전을 즉시 업데이트합니다.

#### 다. 코드예제

```pseudo
// UNSAFE — deprecated 또는 취약 API 사용
result = dangerousFunction(data)  // 알려진 취약점 존재
// 예: strcpy, gets (C), md5 (해싱), http (비암호화)

// SAFE — 보안이 강화된 대체 API 사용
result = safeAlternative(data)
// 예: strncpy, fgets (C), sha256/bcrypt (해싱), https (암호화)
```

#### 라. 적용 언어

| 언어 | 대응 | 주의점 |
|------|:----:|--------|
| JavaScript | O | `npm audit fix`, `npx ncu` (npm-check-updates)로 의존성 관리, Node.js LTS 버전 사용 |
| Python | O | `pip-audit`, `safety check`로 취약 패키지 탐지, `pyup.io` 자동 업데이트 활용 |

---

## 부록 A. CWE 매핑 전체 테이블

### 1. 입력데이터 검증 및 표현

| # | 보안약점 | CWE | JS | Py | 우선순위 |
|---|---------|-----|:--:|:--:|:-------:|
| 1 | SQL 삽입 | CWE-89 | O | O | Critical |
| 2 | 코드 삽입 | CWE-94, 95 | O | O | Critical |
| 3 | 경로 조작 및 자원 삽입 | CWE-22, 99 | O | O | High |
| 4 | 크로스사이트 스크립트 (XSS) | CWE-79 | O | O | Critical |
| 5 | 운영체제 명령어 삽입 | CWE-78 | O | O | Critical |
| 6 | 위험한 형식 파일 업로드 | CWE-434 | O | O | High |
| 7 | 신뢰되지 않은 URL 주소로 자동접속 연결 | CWE-601 | O | O | Medium |
| 8 | 부적절한 XML 외부 개체 참조 (XXE) | CWE-611 | O | O | High |
| 9 | XPath/XML 삽입 | CWE-643 | O | O | Medium |
| 10 | LDAP 삽입 | CWE-90 | O | O | Medium |
| 11 | 크로스사이트 요청 위조 (CSRF) | CWE-352 | O | O | High |
| 12 | 서버사이드 요청 위조 (SSRF) | CWE-918 | O | O | High |
| 13 | 보안기능 결정에 사용되는 부적절한 입력값 | CWE-807 | O | O | Medium |
| 14 | HTTP 응답분할 | CWE-113 | - | O | Medium |
| 15 | 정수형 오버플로우 | CWE-190 | - | O | Medium |
| 16 | 포맷 스트링 삽입 | CWE-134 | - | O | Medium |

### 2. 보안기능

| # | 보안약점 | CWE | JS | Py | 우선순위 |
|---|---------|-----|:--:|:--:|:-------:|
| 1 | 적절한 인증 없는 중요 기능 허용 | CWE-306 | O | O | Critical |
| 2 | 부적절한 인가 | CWE-285 | O | O | Critical |
| 3 | 중요한 자원에 대한 잘못된 권한 설정 | CWE-732 | O | O | High |
| 4 | 취약한 암호화 알고리즘 사용 | CWE-327 | O | O | High |
| 5 | 암호화되지 않은 중요정보 | CWE-312, 319 | O | O | High |
| 6 | 하드코드된 중요정보 | CWE-259, 321 | O | O | Critical |
| 7 | 충분하지 않은 키 길이 사용 | CWE-326 | O | O | Medium |
| 8 | 적절하지 않은 난수 값 사용 | CWE-330 | O | O | High |
| 9 | 취약한 패스워드 허용 | CWE-521 | O | O | Medium |
| 10 | 부적절한 전자서명 확인 | CWE-347 | O | O | High |
| 11 | 부적절한 인증서 유효성 검증 | CWE-295 | O | O | High |
| 12 | 사용자 하드디스크에 저장되는 쿠키를 통한 정보 노출 | CWE-539 | O | O | Medium |
| 13 | 주석문 안에 포함된 시스템 주요정보 | CWE-615 | O | O | Medium |
| 14 | 솔트 없이 일방향 해시 함수 사용 | CWE-759 | O | O | Medium |
| 15 | 무결성 검사 없는 코드 다운로드 | CWE-494 | O | O | Medium |
| 16 | 반복된 인증시도 제한 기능 부재 | CWE-307 | O | O | High |

### 3. 시간 및 상태

| # | 보안약점 | CWE | JS | Py | 우선순위 |
|---|---------|-----|:--:|:--:|:-------:|
| 1 | 경쟁조건: 검사시점과 사용시점 (TOCTOU) | CWE-367 | - | O | Medium |
| 2 | 종료되지 않는 반복문 또는 재귀 함수 | CWE-835, 674 | O | O | Medium |

### 4. 에러처리

| # | 보안약점 | CWE | JS | Py | 우선순위 |
|---|---------|-----|:--:|:--:|:-------:|
| 1 | 오류 메시지 정보노출 | CWE-209 | O | O | Medium |
| 2 | 오류상황 대응 부재 | CWE-390 | O | O | Medium |
| 3 | 부적절한 예외 처리 | CWE-754 | O | O | Medium |

### 5. 코드오류

| # | 보안약점 | CWE | JS | Py | 우선순위 |
|---|---------|-----|:--:|:--:|:-------:|
| 1 | Null Pointer 역참조 | CWE-476 | O | O | Medium |
| 2 | 부적절한 자원 해제 | CWE-404 | O | O | Medium |
| 3 | 신뢰할 수 없는 데이터의 역직렬화 | CWE-502 | O | O | Critical |

### 6. 캡슐화

| # | 보안약점 | CWE | JS | Py | 우선순위 |
|---|---------|-----|:--:|:--:|:-------:|
| 1 | 잘못된 세션에 의한 데이터 정보 노출 | CWE-488, 543 | O | O | High |
| 2 | 제거되지 않고 남은 디버그 코드 | CWE-489 | O | O | Medium |
| 3 | Public 메소드로부터 반환된 Private 배열 | CWE-495 | O | O | Medium |
| 4 | Private 배열에 Public 데이터 할당 | CWE-496 | O | O | Medium |

### 7. API 오용

| # | 보안약점 | CWE | JS | Py | 우선순위 |
|---|---------|-----|:--:|:--:|:-------:|
| 1 | DNS lookup에 의존한 보안결정 | CWE-350 | O | O | Medium |
| 2 | 취약한 API 사용 | - | O | O | Medium |

---

## 부록 B. 카테고리별 우선순위 요약

| 카테고리 | 항목 수 | Critical | High | Medium |
|---------|:------:|:--------:|:----:|:------:|
| 1. 입력데이터 검증 및 표현 | 16 | 4 | 5 | 7 |
| 2. 보안기능 | 16 | 3 | 7 | 6 |
| 3. 시간 및 상태 | 2 | 0 | 0 | 2 |
| 4. 에러처리 | 3 | 0 | 0 | 3 |
| 5. 코드오류 | 3 | 1 | 0 | 2 |
| 6. 캡슐화 | 4 | 0 | 1 | 3 |
| 7. API 오용 | 2 | 0 | 0 | 2 |
| **합계** | **46** | **8** | **13** | **25** |

### 우선순위별 대응 기준

| 등급 | 설명 | 대응 시점 |
|------|------|----------|
| **Critical** | 원격 코드 실행, 인증 우회, 대규모 데이터 유출이 가능합니다. | 즉시 수정합니다. |
| **High** | 중요 정보 노출, 권한 상승, 서비스 거부가 가능합니다. | 배포 전에 수정합니다. |
| **Medium** | 제한적 영향이며, 특정 조건에서 악용 가능합니다. | 계획을 수립하여 수정합니다. |

### 언어별 적용 범위

| 언어 | 기반 가이드 | 항목 수 | 주요 프레임워크 |
|------|-----------|:------:|--------------|
| JavaScript | KISA JS 시큐어코딩 가이드 (2023) | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | KISA Python 시큐어코딩 가이드 (2023) | 46 | Django, Flask, SQLAlchemy, cryptography, hashlib |
| Pseudo Code (본 문서) | JS + Python 통합 | 46 | 언어 무관 범용 패턴 |

### Python 고유 항목 (4개)

JavaScript 가이드에는 없고 Python 가이드에만 포함된 항목입니다.

1. **HTTP 응답분할** (CWE-113) -- Node.js 최신 버전에서 자동 차단
2. **정수형 오버플로우** (CWE-190) -- Python int는 무한 정밀도이나 C 확장에서 발생 가능
3. **포맷 스트링 삽입** (CWE-134) -- Python의 `str.format()`, `%` 연산자 고유 취약점
4. **경쟁조건 TOCTOU** (CWE-367) -- Node.js 비동기 특성상 발생 가능성 낮음

---

> 본 문서는 KISA(한국인터넷진흥원) JavaScript/Python 시큐어코딩 가이드 (2023년 개정본)를 기반으로 작성되었습니다. 언어별 상세 코드 예시는 원본 가이드를 참조하시기 바랍니다.
