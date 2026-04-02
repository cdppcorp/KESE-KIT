# Secure Coding Guide — Pseudo Code

KISA 시큐어코딩 가이드(JavaScript/Python) 기반, 언어에 무관한 범용 보안약점 패턴입니다.
모든 항목은 UNSAFE(취약) / SAFE(안전) 쌍으로 구성됩니다.

---

## 1. Input Data Validation (입력데이터 검증 및 표현)

### 1-1. SQL Injection (CWE-89)

외부 입력값을 쿼리 문자열에 직접 삽입하면 공격자가 임의 SQL을 실행할 수 있습니다.

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

> **TIP** ORM 사용 시에도 raw query를 쓸 경우 반드시 바인딩 변수를 사용하세요.

---

### 1-2. Code Injection (CWE-94, CWE-95)

동적 코드 실행 함수(eval, exec 등)에 외부 입력값을 전달하면 임의 코드가 실행됩니다.

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

> **WARNING** eval(), exec(), Function() 등 동적 코드 실행 함수는 절대 외부 입력값과 함께 사용하지 마세요.

---

### 1-3. Path Traversal / Resource Injection (CWE-22, CWE-99)

파일 경로에 외부 입력값을 직접 사용하면 상위 디렉터리 접근이 가능합니다.

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

---

### 1-4. Cross-Site Scripting — XSS (CWE-79)

외부 입력값이 HTML 응답에 그대로 포함되면 악성 스크립트가 실행됩니다.

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

> **TIP** 템플릿 엔진의 자동 이스케이프 기능을 활성화하세요. 클라이언트와 서버 양쪽 모두 적용해야 합니다.

---

### 1-5. OS Command Injection (CWE-78)

시스템 명령어에 외부 입력값을 직접 전달하면 임의 명령 실행이 가능합니다.

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

---

### 1-6. Unrestricted File Upload (CWE-434)

파일 업로드 시 확장자/크기/내용을 검증하지 않으면 웹셸 등 악성 파일이 업로드됩니다.

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

---

### 1-7. Open Redirect (CWE-601)

리다이렉트 URL을 외부 입력으로 받으면 피싱 사이트로 유도될 수 있습니다.

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

---

### 1-8. XML External Entity — XXE (CWE-611)

XML 파서가 외부 엔티티를 처리하면 서버 파일 읽기, SSRF가 가능합니다.

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

---

### 1-9. XPath / XML Injection (CWE-643)

XPath 쿼리에 외부 입력값을 직접 삽입하면 인증 우회 등이 가능합니다.

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

---

### 1-10. LDAP Injection (CWE-90)

LDAP 필터에 외부 입력값을 직접 삽입하면 디렉터리 데이터 유출이 가능합니다.

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

---

### 1-11. Cross-Site Request Forgery — CSRF (CWE-352)

상태 변경 요청에 CSRF 토큰이 없으면 사용자 의지와 무관한 요청이 실행됩니다.

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

> **TIP** SameSite 쿠키 속성을 Strict 또는 Lax로 설정하면 추가 방어가 됩니다.

---

### 1-12. Server-Side Request Forgery — SSRF (CWE-918)

서버가 외부 입력 URL로 요청을 보내면 내부 네트워크 접근이 가능합니다.

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

---

### 1-13. Untrusted Input for Security Decision (CWE-807)

보안 결정에 클라이언트 조작 가능한 값(쿠키, 히든필드 등)을 사용하면 권한 우회가 가능합니다.

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

---

### 1-14. HTTP Response Splitting (CWE-113) — Python 고유

HTTP 응답 헤더에 개행 문자가 포함되면 응답이 분리되어 캐시 오염 등이 가능합니다.

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

---

### 1-15. Integer Overflow (CWE-190) — Python 고유

정수 연산 결과가 표현 범위를 초과하면 예상치 못한 동작이 발생합니다.

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

---

### 1-16. Format String Injection (CWE-134) — Python 고유

포맷 스트링에 외부 입력값을 직접 사용하면 메모리 정보 유출이 가능합니다.

```pseudo
// UNSAFE — 입력값을 포맷 스트링으로 사용
userInput = request.getParameter("msg")
log(userInput)  // Python: userInput.format() 또는 % 연산자

// SAFE — 포맷 스트링과 인자를 분리
userInput = request.getParameter("msg")
log("%s", userInput)
```

---

## 2. Security Features (보안기능)

### 2-1. Missing Authentication (CWE-306)

중요 기능에 인증 검사가 없으면 비인가자가 접근할 수 있습니다.

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

---

### 2-2. Improper Authorization (CWE-285)

인증된 사용자라도 권한 검증 없이 타인의 리소스에 접근할 수 있습니다.

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

---

### 2-3. Incorrect Permission Assignment (CWE-732)

파일/자원에 과도한 권한을 부여하면 비인가 접근이 가능합니다.

```pseudo
// UNSAFE — 모든 사용자에게 읽기/쓰기 권한
file.setPermissions("/config/secrets.yml", "0777")

// SAFE — 소유자만 읽기/쓰기, 그룹/기타 접근 차단
file.setPermissions("/config/secrets.yml", "0600")
```

---

### 2-4. Broken Crypto Algorithm (CWE-327)

취약한 암호화 알고리즘을 사용하면 암호화된 데이터가 해독될 수 있습니다.

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

---

### 2-5. Cleartext Storage / Transmission (CWE-312, CWE-319)

중요 정보를 평문으로 저장/전송하면 유출 위험이 있습니다.

```pseudo
// UNSAFE — 평문 저장 및 HTTP 전송
db.save("users", {password: userPassword})
http.post("http://api.example.com/login", {password: userPassword})

// SAFE — 해싱 후 저장, HTTPS 전송
hashedPassword = bcrypt.hash(userPassword, saltRounds=12)
db.save("users", {password: hashedPassword})
https.post("https://api.example.com/login", {password: userPassword})
```

---

### 2-6. Hard-coded Credentials (CWE-259, CWE-321)

소스코드에 비밀번호/키를 직접 기재하면 유출 시 즉시 악용됩니다.

```pseudo
// UNSAFE — 소스코드에 비밀번호/키 하드코딩
DB_PASSWORD = "super_secret_123"
API_KEY = "sk-abcdef1234567890"

// SAFE — 환경변수 또는 비밀 관리 도구 사용
DB_PASSWORD = env.get("DB_PASSWORD")
API_KEY = secretManager.get("API_KEY")
```

> **WARNING** .env 파일은 반드시 .gitignore에 추가하세요.

---

### 2-7. Inadequate Key Size (CWE-326)

짧은 키를 사용하면 무차별 대입으로 해독이 가능합니다.

```pseudo
// UNSAFE — 짧은 키 사용
key = crypto.generateKey("RSA", 1024)
key = crypto.generateKey("AES", 64)

// SAFE — 충분한 키 길이
key = crypto.generateKey("RSA", 2048)  // 최소 2048, 권장 4096
key = crypto.generateKey("AES", 256)
```

---

### 2-8. Insufficient Randomness (CWE-330)

보안 목적에 일반 난수 생성기를 사용하면 예측 가능합니다.

```pseudo
// UNSAFE — 일반 난수 사용
token = random.nextInt()
sessionId = Math.random().toString()

// SAFE — 암호학적 보안 난수 사용
token = crypto.randomBytes(32).toHex()
sessionId = crypto.secureRandom(32)
```

---

### 2-9. Weak Password Requirements (CWE-521)

약한 패스워드 정책은 무차별 대입 공격에 취약합니다.

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

---

### 2-10. Improper Signature Verification (CWE-347)

전자서명/JWT를 검증하지 않으면 위변조된 데이터를 신뢰하게 됩니다.

```pseudo
// UNSAFE — 서명 검증 없이 디코딩만 수행
payload = jwt.decode(token)  // 서명 검증 안 함
userId = payload.userId

// SAFE — 서명 검증 후 사용
payload = jwt.verify(token, SECRET_KEY)
userId = payload.userId
```

---

### 2-11. Improper Certificate Validation (CWE-295)

SSL/TLS 인증서 검증을 비활성화하면 중간자 공격에 노출됩니다.

```pseudo
// UNSAFE — 인증서 검증 비활성화
http.get("https://api.example.com", {verifySSL: false})

// SAFE — 인증서 검증 유지 (기본값)
http.get("https://api.example.com", {verifySSL: true})
```

> **WARNING** 개발 환경에서만 비활성화하고, 프로덕션에서는 절대 비활성화하지 마세요.

---

### 2-12. Sensitive Info in Persistent Cookie (CWE-539)

민감 정보를 쿠키에 평문 저장하면 탈취 위험이 있습니다.

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

---

### 2-13. Sensitive Info in Comments (CWE-615)

주석에 비밀번호/키를 남기면 소스코드 노출 시 즉시 악용됩니다.

```pseudo
// UNSAFE
// TODO: 운영 DB 비밀번호는 "Passw0rd!" 입니다
// API Key: sk-1234567890abcdef

// SAFE — 주석에 민감 정보 절대 기재 금지
// DB 접속 정보는 환경변수에서 로드 (설정 가이드: wiki/db-setup 참조)
```

---

### 2-14. Unsalted One-Way Hash (CWE-759)

솔트 없이 해싱하면 레인보우 테이블 공격에 취약합니다.

```pseudo
// UNSAFE — 솔트 없이 해싱
hashed = sha256(password)

// SAFE — 솔트 적용
salt = crypto.randomBytes(16)
hashed = sha256(salt + password)
// 또는 bcrypt 등 솔트 내장 알고리즘 사용
hashed = bcrypt.hash(password, saltRounds=12)
```

---

### 2-15. Download Without Integrity Check (CWE-494)

코드/라이브러리 다운로드 시 무결성을 검증하지 않으면 변조된 파일이 실행됩니다.

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

---

### 2-16. Missing Brute Force Protection (CWE-307)

인증 시도 횟수 제한이 없으면 무차별 대입 공격이 가능합니다.

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

---

## 3. Time and State (시간 및 상태)

### 3-1. TOCTOU Race Condition (CWE-367)

검사 시점과 사용 시점 사이에 상태가 변경되면 보안 검사가 무효화됩니다.

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

---

### 3-2. Infinite Loop / Uncontrolled Recursion (CWE-835, CWE-674)

종료 조건이 없는 반복문/재귀는 서비스 거부를 유발합니다.

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

---

## 4. Error Handling (에러처리)

### 4-1. Error Message Information Exposure (CWE-209)

상세 에러 메시지가 사용자에게 노출되면 시스템 정보가 유출됩니다.

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

---

### 4-2. Error Condition Without Action (CWE-390)

예외를 포착하고도 아무 처리를 하지 않으면 오류가 무시되어 후속 장애가 발생합니다.

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

---

### 4-3. Improper Exception Handling (CWE-754)

지나치게 넓은 예외 처리는 예기치 않은 오류를 숨깁니다.

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

---

## 5. Code Quality (코드오류)

### 5-1. NULL Pointer Dereference (CWE-476)

null/undefined 값을 참조하면 프로그램이 비정상 종료됩니다.

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

---

### 5-2. Improper Resource Shutdown (CWE-404)

사용 후 리소스(파일, DB 연결, 소켓)를 해제하지 않으면 리소스 고갈이 발생합니다.

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

---

### 5-3. Deserialization of Untrusted Data (CWE-502)

신뢰할 수 없는 데이터를 역직렬화하면 임의 코드가 실행될 수 있습니다.

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

> **WARNING** Python의 pickle, JS의 node-serialize는 원격 코드 실행이 가능합니다. 외부 입력에 절대 사용하지 마세요.

---

## 6. Encapsulation (캡슐화)

### 6-1. Data Leak Between Sessions (CWE-488, CWE-543)

사용자별 데이터가 공유 변수에 저장되면 세션 간 데이터가 유출됩니다.

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

---

### 6-2. Active Debug Code (CWE-489)

디버그 코드가 프로덕션에 남으면 시스템 내부 정보가 노출됩니다.

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

---

### 6-3. Private Data Returned from Public Method (CWE-495)

내부 배열/객체의 참조를 직접 반환하면 외부에서 수정이 가능합니다.

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

---

### 6-4. Public Data Assigned to Private Field (CWE-496)

외부 배열/객체를 내부 필드에 직접 할당하면 외부 변경이 내부에 반영됩니다.

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

---

## 7. API Misuse (API 오용)

### 7-1. Reliance on DNS Lookup (CWE-350)

DNS 기반 보안 결정은 DNS 스푸핑으로 우회될 수 있습니다.

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

---

### 7-2. Use of Vulnerable API

취약한 API/함수를 사용하면 보안 위협에 노출됩니다.

```pseudo
// UNSAFE — deprecated 또는 취약 API 사용
result = dangerousFunction(data)  // 알려진 취약점 존재
// 예: strcpy, gets (C), md5 (해싱), http (비암호화)

// SAFE — 보안이 강화된 대체 API 사용
result = safeAlternative(data)
// 예: strncpy, fgets (C), sha256/bcrypt (해싱), https (암호화)
```

> **TIP** 사용 중인 라이브러리의 보안 권고(advisory)를 정기적으로 확인하세요.
