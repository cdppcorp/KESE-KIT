# Secure Coding Guide — JavaScript

KISA JavaScript 시큐어코딩 가이드(ref-011, 159p, 42개 항목) 기반, JS 프레임워크별 구현 예시입니다.
Express.js, Sequelize, Mongoose, Node.js crypto, helmet, csurf 등 실무 프레임워크 코드를 사용합니다.
모든 항목은 UNSAFE(취약) / SAFE(안전) 쌍으로 구성됩니다.

---

## 1. Input Data Validation (입력데이터 검증 및 표현)

### 1-1. SQL Injection (CWE-89)

외부 입력값을 쿼리 문자열에 직접 삽입하면 공격자가 임의 SQL을 실행할 수 있습니다.

**Express.js + mysql 드라이버**

```javascript
// UNSAFE — 입력값을 쿼리에 직접 결합
const mysql = require("mysql");
const connection = mysql.createConnection(/* ... */);

router.get("/vuln/email", (req, res) => {
  const userInput = req.query.id;
  // 사용자 입력값을 검증 없이 쿼리에 삽입
  const query = `SELECT email FROM user WHERE user_id = ${userInput}`;
  connection.query(query, (err, result) => {
    if (err) return res.status(500).send("error");
    return res.send(result);
  });
});

// SAFE — 파라미터 바인딩 (? 플레이스홀더)
router.get("/safe/email", (req, res) => {
  const userInput = req.query.id;
  const query = "SELECT email FROM user WHERE user_id = ?";
  connection.query(query, [userInput], (err, result) => {
    if (err) return res.status(500).send("error");
    return res.send(result);
  });
});
```

**Sequelize ORM**

```javascript
// UNSAFE — ORM에서 raw query에 입력값 직접 삽입
const { QueryTypes } = require("sequelize");

router.get("/vuln/orm/email", (req, res) => {
  const userInput = req.query.id;
  const query = `SELECT email FROM user WHERE user_id = ${userInput}`;
  sequelize.query(query, { type: QueryTypes.SELECT })
    .then((result) => res.send(result))
    .catch((err) => res.status(500).send("error"));
});

// SAFE — 바인딩 변수 사용 ($1 플레이스홀더)
router.get("/safe/orm/email", (req, res) => {
  const userInput = req.query.id;
  const query = "SELECT email FROM user WHERE user_id = $1";
  sequelize.query(query, {
    bind: [userInput],
    type: QueryTypes.SELECT,
  })
    .then((result) => res.send(result))
    .catch((err) => res.status(500).send("error"));
});
```

**Mongoose (NoSQL Injection 방어)**

```javascript
// UNSAFE — 쿼리 객체에 외부 입력 직접 전달 (NoSQL Injection)
router.get("/vuln/user", async (req, res) => {
  const user = await User.findOne({ username: req.query.username });
  // 공격: ?username[$ne]=  → 모든 사용자 조회
  res.json(user);
});

// SAFE — mongo-sanitize로 연산자 제거
const sanitize = require("mongo-sanitize");

router.get("/safe/user", async (req, res) => {
  const username = sanitize(req.query.username);
  const user = await User.findOne({ username });
  res.json(user);
});
```

> **TIP** ORM 사용 시에도 raw query를 쓸 경우 반드시 바인딩 변수를 사용하세요.

---

### 1-2. Code Injection (CWE-94, CWE-95)

동적 코드 실행 함수(eval, Function 등)에 외부 입력값을 전달하면 임의 코드가 실행됩니다.

```javascript
// UNSAFE — 외부 입력값을 eval()에 직접 전달
router.post("/vuln/calc", (req, res) => {
  const data = eval(req.body.data);
  return res.send({ data });
});

// SAFE — 화이트리스트 검증 + 안전한 파서 사용
const { Parser } = require("expr-eval");
const parser = new Parser();

router.post("/safe/calc", (req, res) => {
  const input = req.body.expression;
  // 영문, 숫자, 기본 연산자만 허용
  if (!/^[0-9a-zA-Z+\-*/.() ]+$/.test(input)) {
    return res.status(400).send("Invalid expression");
  }
  try {
    const result = parser.evaluate(input);
    return res.send({ result });
  } catch (e) {
    return res.status(400).send("Parse error");
  }
});
```

> **WARNING** `eval()`, `Function()`, `setTimeout(string)`, `setInterval(string)` 등 동적 코드 실행 함수는 절대 외부 입력값과 함께 사용하지 마세요.

---

### 1-3. Path Traversal / Resource Injection (CWE-22, CWE-99)

파일 경로에 외부 입력값을 직접 사용하면 상위 디렉터리 접근이 가능합니다.

```javascript
// UNSAFE — 입력값을 경로에 직접 사용
const path = require("path");
const fs = require("fs");

router.get("/vuln/file", (req, res) => {
  const requestFile = req.query.file;
  // 공격: file=../../../../etc/passwd
  fs.readFile(path.resolve(__dirname, requestFile), "utf8", (err, data) => {
    if (err) return res.send("error");
    return res.send(data);
  });
});

// SAFE — 경로 정규화 후 기본 디렉터리 내 위치 검증
const UPLOAD_DIR = path.resolve(__dirname, "uploads");

router.get("/safe/file", (req, res) => {
  const requestFile = req.query.file;
  const fullPath = path.resolve(UPLOAD_DIR, requestFile);
  // 정규화된 경로가 허용된 디렉터리 내에 있는지 확인
  if (!fullPath.startsWith(UPLOAD_DIR)) {
    return res.status(403).send("Access denied");
  }
  fs.readFile(fullPath, "utf8", (err, data) => {
    if (err) return res.status(404).send("Not found");
    return res.send(data);
  });
});
```

**소켓 자원 삽입 방어**

```javascript
// UNSAFE — 외부 입력값으로 소켓 연결
const io = require("socket.io-client");

router.get("/vuln/socket", (req, res) => {
  const socket = io(req.query.url);
  return res.send("connected");
});

// SAFE — 화이트리스트 기반 연결
router.get("/safe/socket", (req, res) => {
  const whitelist = ["ws://localhost:3000", "ws://127.0.0.1:3000"];
  if (!whitelist.includes(req.query.url)) {
    return res.status(400).send("Blocked URL");
  }
  const socket = io(req.query.url);
  return res.send("connected");
});
```

---

### 1-4. Cross-Site Scripting — XSS (CWE-79)

외부 입력값이 HTML 응답에 그대로 포함되면 악성 스크립트가 실행됩니다.

**Express.js 서버측**

```javascript
// UNSAFE — 입력값을 HTML에 직접 삽입
router.get("/vuln/search", (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Results for: ${query}</h1>`);
  // 공격: q=<script>alert('xss')</script>
});

// SAFE — HTML 이스케이프 적용 + helmet 헤더 설정
const helmet = require("helmet");
const escapeHtml = require("escape-html");

app.use(helmet());  // X-XSS-Protection, CSP 등 보안 헤더 자동 설정

router.get("/safe/search", (req, res) => {
  const query = escapeHtml(req.query.q);
  res.send(`<h1>Results for: ${query}</h1>`);
});
```

**클라이언트측 (VanillaJS)**

```javascript
// UNSAFE — innerHTML로 외부 데이터 직접 삽입
document.getElementById("output").innerHTML = serverData;

// SAFE — textContent 사용 (HTML 파싱 방지)
document.getElementById("output").textContent = serverData;
```

**React (기본적으로 이스케이프)**

```javascript
// UNSAFE — dangerouslySetInnerHTML 사용
function Comment({ body }) {
  return <div dangerouslySetInnerHTML={{ __html: body }} />;
}

// SAFE — React의 기본 이스케이프 활용
function Comment({ body }) {
  return <div>{body}</div>;  // 자동 이스케이프
}

// 부득이한 경우 — DOMPurify로 sanitize 후 사용
import DOMPurify from "dompurify";

function Comment({ body }) {
  const clean = DOMPurify.sanitize(body);
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
}
```

> **TIP** `helmet` 미들웨어로 CSP(Content-Security-Policy) 헤더를 설정하고, 템플릿 엔진의 자동 이스케이프 기능을 활성화하세요.

---

### 1-5. OS Command Injection (CWE-78)

시스템 명령어에 외부 입력값을 직접 전달하면 임의 명령 실행이 가능합니다.

```javascript
// UNSAFE — 입력값을 쉘 명령에 직접 결합
const { exec } = require("child_process");

router.get("/vuln/ping", (req, res) => {
  const host = req.query.host;
  exec(`ping -c 4 ${host}`, (err, stdout) => {
    // 공격: host=127.0.0.1; rm -rf /
    res.send(stdout);
  });
});

// SAFE — execFile로 인자 배열 전달 (쉘 해석 방지)
const { execFile } = require("child_process");

router.get("/safe/ping", (req, res) => {
  const host = req.query.host;
  // 입력값 검증: IP/호스트명 패턴만 허용
  if (!/^[a-zA-Z0-9.\-]+$/.test(host)) {
    return res.status(400).send("Invalid host");
  }
  execFile("ping", ["-c", "4", host], (err, stdout) => {
    if (err) return res.status(500).send("error");
    res.send(stdout);
  });
});
```

> **TIP** `child_process.exec()` 대신 `child_process.execFile()` 또는 `child_process.spawn()`을 사용하면 쉘 해석 없이 명령을 실행합니다.

---

### 1-6. Unrestricted File Upload (CWE-434)

파일 업로드 시 확장자/크기/내용을 검증하지 않으면 웹셸 등 악성 파일이 업로드됩니다.

```javascript
// UNSAFE — 파일 확장자 검증 없이 저장
const multer = require("multer");
const upload = multer({ dest: "uploads/" });

router.post("/vuln/upload", upload.single("file"), (req, res) => {
  // 원본 파일명 그대로 저장, 확장자 무검증
  const destPath = `uploads/${req.file.originalname}`;
  fs.renameSync(req.file.path, destPath);
  res.send("Uploaded");
});

// SAFE — 화이트리스트 확장자 + 랜덤 파일명 + 크기 제한
const path = require("path");
const crypto = require("crypto");

const safeUpload = multer({
  limits: { fileSize: 5 * 1024 * 1024 },  // 5MB 제한
  fileFilter: (req, file, cb) => {
    const ALLOWED_EXTS = [".jpg", ".jpeg", ".png", ".pdf", ".docx"];
    const ext = path.extname(file.originalname).toLowerCase();
    if (!ALLOWED_EXTS.includes(ext)) {
      return cb(new Error("Disallowed file type"), false);
    }
    cb(null, true);
  },
});

router.post("/safe/upload", safeUpload.single("file"), (req, res) => {
  const ext = path.extname(req.file.originalname).toLowerCase();
  const safeName = crypto.randomUUID() + ext;
  const destPath = path.join("uploads/", safeName);
  fs.renameSync(req.file.path, destPath);
  res.send("Uploaded: " + safeName);
});
```

---

### 1-7. Open Redirect (CWE-601)

리다이렉트 URL을 외부 입력으로 받으면 피싱 사이트로 유도될 수 있습니다.

```javascript
// UNSAFE — 외부 입력 URL로 직접 리다이렉트
router.get("/vuln/redirect", (req, res) => {
  const next = req.query.next;
  res.redirect(next);
  // 공격: next=https://untrusted-origin.example.com
});

// SAFE — 허용된 도메인/경로만 리다이렉트
router.get("/safe/redirect", (req, res) => {
  const next = req.query.next;
  const ALLOWED_HOSTS = ["mysite.com", "www.mysite.com"];
  try {
    const parsed = new URL(next, `https://${req.hostname}`);
    if (!ALLOWED_HOSTS.includes(parsed.hostname)) {
      return res.redirect("/");
    }
    res.redirect(parsed.href);
  } catch {
    res.redirect("/");
  }
});
```

---

### 1-8. XML External Entity — XXE (CWE-611)

XML 파서가 외부 엔티티를 처리하면 서버 파일 읽기, SSRF가 가능합니다.

```javascript
// UNSAFE — 외부 엔티티 처리 허용
const libxmljs = require("libxmljs");

router.post("/vuln/xml", (req, res) => {
  // noent: true → 외부 엔티티 확장 허용 (위험)
  const doc = libxmljs.parseXml(req.body, { noent: true });
  res.send(doc.toString());
});

// SAFE — 외부 엔티티 비활성화
router.post("/safe/xml", (req, res) => {
  // noent 옵션을 비활성화 (기본값: false)
  const doc = libxmljs.parseXml(req.body, { noent: false, noblanks: true });
  res.send(doc.toString());
});

// 대안 — fast-xml-parser 사용 (DTD/엔티티 미지원으로 안전)
const { XMLParser } = require("fast-xml-parser");
const parser = new XMLParser();

router.post("/safe/xml2", (req, res) => {
  const result = parser.parse(req.body);
  res.json(result);
});
```

---

### 1-9. XPath / XML Injection (CWE-643)

XPath 쿼리에 외부 입력값을 직접 삽입하면 인증 우회 등이 가능합니다.

```javascript
// UNSAFE — 입력값을 XPath에 직접 삽입
const xpath = require("xpath");
const { DOMParser } = require("xmldom");

router.get("/vuln/xpath", (req, res) => {
  const username = req.query.user;
  const doc = new DOMParser().parseFromString(xmlData);
  // 공격: user=' or '1'='1
  const nodes = xpath.select(`//users/user[name='${username}']`, doc);
  res.json(nodes);
});

// SAFE — 입력값에서 XPath 특수문자 이스케이프
function escapeXPath(value) {
  if (!value.includes("'")) return `'${value}'`;
  if (!value.includes('"')) return `"${value}"`;
  return "concat(" + value.split("'").map(s => `'${s}'`).join(`,"'"`) + ")";
}

router.get("/safe/xpath", (req, res) => {
  const username = req.query.user;
  // 영숫자만 허용
  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    return res.status(400).send("Invalid input");
  }
  const doc = new DOMParser().parseFromString(xmlData);
  const nodes = xpath.select(`//users/user[name=${escapeXPath(username)}]`, doc);
  res.json(nodes);
});
```

---

### 1-10. LDAP Injection (CWE-90)

LDAP 필터에 외부 입력값을 직접 삽입하면 디렉터리 데이터 유출이 가능합니다.

```javascript
// UNSAFE — 입력값을 LDAP 필터에 직접 삽입
const ldap = require("ldapjs");
const client = ldap.createClient({ url: "ldap://localhost:389" });

router.get("/vuln/ldap", (req, res) => {
  const username = req.query.user;
  const filter = `(uid=${username})`;
  // 공격: user=*)(|(uid=*) → 모든 사용자 조회
  client.search("dc=example,dc=com", { filter }, (err, result) => {
    // ...
  });
});

// SAFE — LDAP 특수문자 이스케이프
function escapeLDAP(input) {
  return input.replace(/[\\*()&|!<>=~]/g, (ch) => {
    return "\\" + ch.charCodeAt(0).toString(16).padStart(2, "0");
  });
}

router.get("/safe/ldap", (req, res) => {
  const username = escapeLDAP(req.query.user);
  const filter = `(uid=${username})`;
  client.search("dc=example,dc=com", { filter }, (err, result) => {
    // ...
  });
});
```

---

### 1-11. Cross-Site Request Forgery — CSRF (CWE-352)

상태 변경 요청에 CSRF 토큰이 없으면 사용자 의지와 무관한 요청이 실행됩니다.

```javascript
// UNSAFE — CSRF 토큰 없이 상태 변경
router.post("/vuln/transfer", (req, res) => {
  const { amount, to } = req.body;
  transferMoney(req.user, to, amount);
  res.send("Transferred");
});

// SAFE — csurf 미들웨어로 CSRF 토큰 검증
const csrf = require("csurf");
const csrfProtection = csrf({ cookie: true });

// 토큰 발급 (폼 렌더링 시)
router.get("/safe/transfer", csrfProtection, (req, res) => {
  res.render("transfer", { csrfToken: req.csrfToken() });
});

// 토큰 검증 (상태 변경 시)
router.post("/safe/transfer", csrfProtection, (req, res) => {
  const { amount, to } = req.body;
  transferMoney(req.user, to, amount);
  res.send("Transferred");
});
```

> **TIP** SameSite 쿠키 속성을 `Strict` 또는 `Lax`로 설정하면 추가 방어가 됩니다. `csurf`가 deprecated된 경우 `csrf-csrf` 또는 `lusca` 패키지를 사용하세요.

---

### 1-12. Server-Side Request Forgery — SSRF (CWE-918)

서버가 외부 입력 URL로 요청을 보내면 내부 네트워크 접근이 가능합니다.

```javascript
// UNSAFE — 입력 URL로 서버가 직접 요청
const axios = require("axios");

router.get("/vuln/fetch", async (req, res) => {
  const targetUrl = req.query.url;
  // 공격: url=http://169.254.169.254/latest/meta-data/
  const response = await axios.get(targetUrl);
  res.send(response.data);
});

// SAFE — URL 화이트리스트 + 내부 IP 차단
const { URL } = require("url");
const ipaddr = require("ipaddr.js");
const dns = require("dns").promises;

async function isPrivateHost(hostname) {
  try {
    const { address } = await dns.lookup(hostname);
    const addr = ipaddr.parse(address);
    const range = addr.range();
    return ["private", "loopback", "linkLocal", "uniqueLocal"].includes(range);
  } catch {
    return true;  // DNS 실패 시 차단
  }
}

router.get("/safe/fetch", async (req, res) => {
  try {
    const parsed = new URL(req.query.url);
    if (!["http:", "https:"].includes(parsed.protocol)) {
      return res.status(400).send("Invalid scheme");
    }
    if (await isPrivateHost(parsed.hostname)) {
      return res.status(403).send("Blocked: internal address");
    }
    const response = await axios.get(parsed.href, { timeout: 5000 });
    res.send(response.data);
  } catch {
    res.status(400).send("Request failed");
  }
});
```

---

### 1-13. Untrusted Input for Security Decision (CWE-807)

보안 결정에 클라이언트 조작 가능한 값(쿠키, 히든필드 등)을 사용하면 권한 우회가 가능합니다.

```javascript
// UNSAFE — 클라이언트 쿠키로 관리자 판단
router.get("/vuln/admin", (req, res) => {
  const isAdmin = req.cookies.isAdmin;
  if (isAdmin === "true") {
    return res.send("Admin Panel");
  }
  res.status(403).send("Forbidden");
});

// SAFE — 서버 세션에서 권한 확인
router.get("/safe/admin", (req, res) => {
  const user = req.session.user;
  if (!user || user.role !== "admin") {
    return res.status(403).send("Forbidden");
  }
  res.send("Admin Panel");
});
```

---

### 1-14. HTTP Response Splitting (CWE-113)

> 해당 없음 (Python 고유 항목)

---

### 1-15. Integer Overflow (CWE-190)

> 해당 없음 (Python 고유 항목)

---

### 1-16. Format String Injection (CWE-134)

> 해당 없음 (Python 고유 항목)

---

## 2. Security Features (보안기능)

### 2-1. Missing Authentication (CWE-306)

중요 기능에 인증 검사가 없으면 비인가자가 접근할 수 있습니다.

```javascript
// UNSAFE — 인증 없이 관리 기능 노출
router.post("/vuln/admin/delete-user", (req, res) => {
  const userId = req.body.id;
  User.destroy({ where: { id: userId } });
  res.send("Deleted");
});

// SAFE — 인증 + 인가 미들웨어 적용
function authRequired(req, res, next) {
  if (!req.session || !req.session.user) {
    return res.status(401).json({ error: "Authentication required" });
  }
  next();
}

function adminOnly(req, res, next) {
  if (req.session.user.role !== "admin") {
    return res.status(403).json({ error: "Forbidden" });
  }
  next();
}

router.post("/safe/admin/delete-user", authRequired, adminOnly, (req, res) => {
  const userId = req.body.id;
  User.destroy({ where: { id: userId } });
  res.send("Deleted");
});
```

---

### 2-2. Improper Authorization (CWE-285)

인증된 사용자라도 권한 검증 없이 타인의 리소스에 접근할 수 있습니다.

```javascript
// UNSAFE — 소유자 검증 없이 리소스 반환
router.get("/vuln/orders/:id", authRequired, async (req, res) => {
  const order = await Order.findByPk(req.params.id);
  res.json(order);  // 다른 사용자의 주문도 열람 가능
});

// SAFE — 요청자와 소유자 일치 확인
router.get("/safe/orders/:id", authRequired, async (req, res) => {
  const order = await Order.findByPk(req.params.id);
  if (!order) return res.status(404).json({ error: "Not found" });
  if (order.userId !== req.session.user.id) {
    return res.status(403).json({ error: "Forbidden" });
  }
  res.json(order);
});
```

---

### 2-3. Incorrect Permission Assignment (CWE-732)

파일/자원에 과도한 권한을 부여하면 비인가 접근이 가능합니다.

```javascript
// UNSAFE — 모든 사용자에게 읽기/쓰기 권한
const fs = require("fs");

fs.writeFileSync("config/secrets.json", data);
fs.chmodSync("config/secrets.json", 0o777);

// SAFE — 소유자만 읽기/쓰기, 그룹/기타 접근 차단
fs.writeFileSync("config/secrets.json", data, { mode: 0o600 });
// 또는
fs.chmodSync("config/secrets.json", 0o600);
```

---

### 2-4. Broken Crypto Algorithm (CWE-327)

취약한 암호화 알고리즘을 사용하면 암호화된 데이터가 해독될 수 있습니다.

```javascript
// UNSAFE — 취약한 알고리즘 사용
const crypto = require("crypto");

const hash = crypto.createHash("md5").update(password).digest("hex");
const cipher = crypto.createCipheriv("des-ecb", key, null);

// SAFE — 강력한 알고리즘 사용
const hash = crypto.createHash("sha256").update(data).digest("hex");

// AES-256-GCM (인증된 암호화)
const iv = crypto.randomBytes(12);
const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
let encrypted = cipher.update(plaintext, "utf8", "hex");
encrypted += cipher.final("hex");
const authTag = cipher.getAuthTag();

// 패스워드는 bcrypt 사용
const bcrypt = require("bcrypt");
const hashed = await bcrypt.hash(password, 12);
const isMatch = await bcrypt.compare(inputPassword, hashed);
```

---

### 2-5. Cleartext Storage / Transmission (CWE-312, CWE-319)

중요 정보를 평문으로 저장/전송하면 유출 위험이 있습니다.

```javascript
// UNSAFE — 평문 저장 및 HTTP 전송
await User.create({ email, password: plainPassword });
await axios.post("http://api.example.com/login", { password: plainPassword });

// SAFE — 해싱 후 저장, HTTPS 전송
const bcrypt = require("bcrypt");
const hashedPassword = await bcrypt.hash(plainPassword, 12);
await User.create({ email, password: hashedPassword });

// HTTPS 강제 (helmet HSTS)
const helmet = require("helmet");
app.use(helmet.hsts({ maxAge: 31536000, includeSubDomains: true }));

// HTTP → HTTPS 리다이렉트
app.use((req, res, next) => {
  if (!req.secure) {
    return res.redirect(301, `https://${req.hostname}${req.url}`);
  }
  next();
});
```

---

### 2-6. Hard-coded Credentials (CWE-259, CWE-321)

소스코드에 비밀번호/키를 직접 기재하면 유출 시 즉시 악용됩니다.

```javascript
// UNSAFE — 소스코드에 비밀번호/키 하드코딩
const DB_PASSWORD = "super_secret_123";
const JWT_SECRET = "my-jwt-secret-key-12345";

// SAFE — 환경변수 또는 비밀 관리 도구 사용
require("dotenv").config();

const DB_PASSWORD = process.env.DB_PASSWORD;
const JWT_SECRET = process.env.JWT_SECRET;

if (!DB_PASSWORD || !JWT_SECRET) {
  throw new Error("Required environment variables are not set");
}
```

> **WARNING** `.env` 파일은 반드시 `.gitignore`에 추가하세요.

---

### 2-7. Inadequate Key Size (CWE-326)

짧은 키를 사용하면 무차별 대입으로 해독이 가능합니다.

```javascript
// UNSAFE — 짧은 키 사용
const crypto = require("crypto");

const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
  modulusLength: 1024,  // 1024비트는 취약
});

// SAFE — 충분한 키 길이
const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
  modulusLength: 2048,  // 최소 2048, 권장 4096
  publicKeyEncoding: { type: "spki", format: "pem" },
  privateKeyEncoding: { type: "pkcs8", format: "pem" },
});

// AES 키 — 최소 256비트
const aesKey = crypto.randomBytes(32);  // 256비트
```

---

### 2-8. Insufficient Randomness (CWE-330)

보안 목적에 일반 난수 생성기를 사용하면 예측 가능합니다.

```javascript
// UNSAFE — 일반 난수 사용
const token = Math.random().toString(36).substring(2);
const sessionId = Math.floor(Math.random() * 1000000).toString();

// SAFE — 암호학적 보안 난수 사용
const crypto = require("crypto");

const token = crypto.randomBytes(32).toString("hex");
const sessionId = crypto.randomUUID();
```

---

### 2-9. Weak Password Requirements (CWE-521)

약한 패스워드 정책은 무차별 대입 공격에 취약합니다.

```javascript
// UNSAFE — 패스워드 정책 없음
router.post("/vuln/register", async (req, res) => {
  const { username, password } = req.body;
  if (password.length > 0) {
    await User.create({ username, password });
    res.send("Registered");
  }
});

// SAFE — 복잡도 검증
function validatePassword(password) {
  const errors = [];
  if (password.length < 8) errors.push("8자 이상 입력하세요");
  if (password.length > 64) errors.push("64자 이하로 입력하세요");
  if (!/[A-Z]/.test(password)) errors.push("대문자를 포함하세요");
  if (!/[a-z]/.test(password)) errors.push("소문자를 포함하세요");
  if (!/[0-9]/.test(password)) errors.push("숫자를 포함하세요");
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) errors.push("특수문자를 포함하세요");
  return errors;
}

router.post("/safe/register", async (req, res) => {
  const { username, password } = req.body;
  const errors = validatePassword(password);
  if (errors.length > 0) {
    return res.status(400).json({ errors });
  }
  const hashed = await bcrypt.hash(password, 12);
  await User.create({ username, password: hashed });
  res.send("Registered");
});
```

---

### 2-10. Improper Signature Verification (CWE-347)

전자서명/JWT를 검증하지 않으면 위변조된 데이터를 신뢰하게 됩니다.

```javascript
// UNSAFE — 서명 검증 없이 디코딩만 수행
const jwt = require("jsonwebtoken");

router.get("/vuln/profile", (req, res) => {
  const token = req.headers.authorization?.split(" ")[1];
  const payload = jwt.decode(token);  // 서명 검증 안 함
  res.json({ userId: payload.userId });
});

// SAFE — 서명 검증 후 사용 + 알고리즘 고정
router.get("/safe/profile", (req, res) => {
  const token = req.headers.authorization?.split(" ")[1];
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ["HS256"],  // 알고리즘 명시 (none 공격 방지)
    });
    res.json({ userId: payload.userId });
  } catch (err) {
    res.status(401).json({ error: "Invalid token" });
  }
});
```

---

### 2-11. Improper Certificate Validation (CWE-295)

SSL/TLS 인증서 검증을 비활성화하면 중간자 공격에 노출됩니다.

```javascript
// UNSAFE — 인증서 검증 비활성화
const https = require("https");
const axios = require("axios");

// 전역 비활성화 (절대 사용 금지)
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

// 또는 요청별 비활성화
const response = await axios.get("https://api.example.com", {
  httpsAgent: new https.Agent({ rejectUnauthorized: false }),
});

// SAFE — 인증서 검증 유지 (기본값)
const response = await axios.get("https://api.example.com");
// rejectUnauthorized 기본값이 true이므로 별도 설정 불필요
```

> **WARNING** 개발 환경에서만 비활성화하고, 프로덕션에서는 절대 비활성화하지 마세요.

---

### 2-12. Sensitive Info in Persistent Cookie (CWE-539)

민감 정보를 쿠키에 평문 저장하면 탈취 위험이 있습니다.

```javascript
// UNSAFE — 민감 정보를 쿠키에 저장
router.post("/vuln/login", (req, res) => {
  res.cookie("user_role", "admin");
  res.cookie("user_email", user.email);
  res.send("Logged in");
});

// SAFE — 서버 세션에 저장, 쿠키는 세션 ID만
const session = require("express-session");

app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,    // JavaScript에서 접근 불가
    secure: true,      // HTTPS에서만 전송
    sameSite: "strict", // CSRF 방어
    maxAge: 3600000,   // 1시간
  },
}));

router.post("/safe/login", (req, res) => {
  req.session.user = { id: user.id, role: user.role };
  res.send("Logged in");
});
```

---

### 2-13. Sensitive Info in Comments (CWE-615)

주석에 비밀번호/키를 남기면 소스코드 노출 시 즉시 악용됩니다.

```javascript
// UNSAFE
// TODO: 운영 DB 비밀번호는 "Passw0rd!" 입니다
// API Key: sk-1234567890abcdef
// admin 계정 비번: admin123!

// SAFE — 주석에 민감 정보 절대 기재 금지
// DB 접속 정보는 환경변수에서 로드 (설정 가이드: wiki/db-setup 참조)
// API Key는 .env 또는 Vault에서 관리
```

---

### 2-14. Unsalted One-Way Hash (CWE-759)

솔트 없이 해싱하면 레인보우 테이블 공격에 취약합니다.

```javascript
// UNSAFE — 솔트 없이 해싱
const crypto = require("crypto");

const hashed = crypto.createHash("sha256").update(password).digest("hex");

// SAFE — 솔트 적용 (수동)
const salt = crypto.randomBytes(16).toString("hex");
const hashed = crypto.createHash("sha256").update(salt + password).digest("hex");
// salt와 hashed를 함께 저장: `${salt}:${hashed}`

// SAFE — bcrypt 사용 (솔트 내장)
const bcrypt = require("bcrypt");
const hashed = await bcrypt.hash(password, 12);
// 검증
const isValid = await bcrypt.compare(inputPassword, hashed);
```

---

### 2-15. Download Without Integrity Check (CWE-494)

코드/라이브러리 다운로드 시 무결성을 검증하지 않으면 변조된 파일이 실행됩니다.

```javascript
// UNSAFE — 체크섬 없이 다운로드
const axios = require("axios");
const fs = require("fs");

const response = await axios.get("https://cdn.example.com/lib.tar.gz", {
  responseType: "arraybuffer",
});
fs.writeFileSync("lib.tar.gz", response.data);

// SAFE — 해시 검증 후 저장
const crypto = require("crypto");

const EXPECTED_HASH = "a1b2c3d4e5f6...";  // 사전에 알려진 해시

const response = await axios.get("https://cdn.example.com/lib.tar.gz", {
  responseType: "arraybuffer",
});
const hash = crypto.createHash("sha256").update(Buffer.from(response.data)).digest("hex");
if (hash !== EXPECTED_HASH) {
  throw new Error("Integrity check failed: hash mismatch");
}
fs.writeFileSync("lib.tar.gz", response.data);
```

> **TIP** `npm install` 시 `package-lock.json`의 integrity 필드가 SRI(Subresource Integrity) 검증을 자동 수행합니다.

---

### 2-16. Missing Brute Force Protection (CWE-307)

인증 시도 횟수 제한이 없으면 무차별 대입 공격이 가능합니다.

```javascript
// UNSAFE — 시도 횟수 무제한
router.post("/vuln/login", async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ where: { username } });
  if (user && await bcrypt.compare(password, user.password)) {
    return res.send("Login success");
  }
  res.status(401).send("Invalid credentials");
});

// SAFE — express-rate-limit + 계정 잠금
const rateLimit = require("express-rate-limit");

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15분
  max: 5,                     // 최대 5회
  message: "Too many login attempts. Please try again after 15 minutes.",
  standardHeaders: true,
  legacyHeaders: false,
});

router.post("/safe/login", loginLimiter, async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ where: { username } });
  if (!user) return res.status(401).send("Invalid credentials");

  if (user.loginAttempts >= 5 && user.lockUntil > Date.now()) {
    return res.status(429).send("Account locked. Try again later.");
  }

  if (await bcrypt.compare(password, user.password)) {
    await user.update({ loginAttempts: 0, lockUntil: null });
    return res.send("Login success");
  }

  await user.update({
    loginAttempts: user.loginAttempts + 1,
    lockUntil: user.loginAttempts + 1 >= 5 ? Date.now() + 15 * 60 * 1000 : null,
  });
  res.status(401).send("Invalid credentials");
});
```

---

## 3. Time and State (시간 및 상태)

### 3-1. TOCTOU Race Condition (CWE-367)

> 해당 없음 (Python 고유 항목)

---

### 3-2. Infinite Loop / Uncontrolled Recursion (CWE-835, CWE-674)

종료 조건이 없는 반복문/재귀는 서비스 거부를 유발합니다.

```javascript
// UNSAFE — 종료 조건 누락
function processTree(node) {
  processTree(node.left);   // 종료 조건 없음 → 스택 오버플로우
  processTree(node.right);
}

// UNSAFE — 외부 입력으로 반복 횟수 결정
router.post("/vuln/repeat", (req, res) => {
  const count = parseInt(req.body.count);
  let result = "";
  for (let i = 0; i < count; i++) {  // count가 매우 크면 서비스 거부
    result += "x";
  }
  res.send(result);
});

// SAFE — 종료 조건 + 깊이 제한
const MAX_DEPTH = 100;

function processTree(node, depth = 0) {
  if (!node || depth > MAX_DEPTH) return;
  processTree(node.left, depth + 1);
  processTree(node.right, depth + 1);
}

// SAFE — 반복 횟수 상한 검증
const MAX_COUNT = 10000;

router.post("/safe/repeat", (req, res) => {
  const count = Math.min(parseInt(req.body.count) || 0, MAX_COUNT);
  if (count < 0) return res.status(400).send("Invalid count");
  const result = "x".repeat(count);
  res.send(result);
});
```

---

## 4. Error Handling (에러처리)

### 4-1. Error Message Information Exposure (CWE-209)

상세 에러 메시지가 사용자에게 노출되면 시스템 정보가 유출됩니다.

```javascript
// UNSAFE — 스택 트레이스를 그대로 반환
app.use((err, req, res, next) => {
  res.status(500).json({
    error: err.message,
    stack: err.stack,         // 내부 경로/라이브러리 버전 노출
    query: err.sql,           // SQL 쿼리 노출
  });
});

// SAFE — 일반 메시지만 반환, 상세 로그는 서버에 기록
const logger = require("winston");

app.use((err, req, res, next) => {
  logger.error("Unhandled error", {
    message: err.message,
    stack: err.stack,
    url: req.originalUrl,
    method: req.method,
  });
  res.status(500).json({
    error: "Internal server error. Please try again later.",
  });
});

// 프로덕션 환경에서 Express 기본 에러 페이지 비활성화
if (process.env.NODE_ENV === "production") {
  app.set("env", "production");  // 스택 트레이스 자동 숨김
}
```

---

### 4-2. Error Condition Without Action (CWE-390)

예외를 포착하고도 아무 처리를 하지 않으면 오류가 무시되어 후속 장애가 발생합니다.

```javascript
// UNSAFE — 예외를 무시
try {
  const config = JSON.parse(fs.readFileSync("config.json", "utf8"));
} catch (err) {
  // 아무 처리 없음 → config가 undefined인 채로 진행
}

// SAFE — 적절한 처리 또는 기본값 적용
const logger = require("winston");
const DEFAULT_CONFIG = { port: 3000, debug: false };

let config;
try {
  config = JSON.parse(fs.readFileSync("config.json", "utf8"));
} catch (err) {
  if (err.code === "ENOENT") {
    logger.warn("Config file not found, using defaults");
    config = DEFAULT_CONFIG;
  } else {
    logger.error("Config load failed", { error: err.message });
    throw err;  // 복구 불가능한 오류는 재발생
  }
}
```

---

### 4-3. Improper Exception Handling (CWE-754)

지나치게 넓은 예외 처리는 예기치 않은 오류를 숨깁니다.

```javascript
// UNSAFE — 모든 예외를 한꺼번에 처리
router.post("/vuln/process", async (req, res) => {
  try {
    const data = JSON.parse(req.body.data);
    const result = await processData(data);
    await saveResult(result);
    res.json(result);
  } catch (err) {
    res.status(500).send("Something went wrong");
    // 입력 오류, 비즈니스 로직 오류, DB 오류를 모두 동일하게 처리
  }
});

// SAFE — 예외를 구체적으로 분리 처리
router.post("/safe/process", async (req, res) => {
  let data;
  try {
    data = JSON.parse(req.body.data);
  } catch (err) {
    return res.status(400).json({ error: "Invalid JSON format" });
  }

  let result;
  try {
    result = await processData(data);
  } catch (err) {
    if (err instanceof ValidationError) {
      return res.status(422).json({ error: err.message });
    }
    logger.error("Processing failed", { error: err.message });
    return res.status(500).json({ error: "Processing failed" });
  }

  try {
    await saveResult(result);
  } catch (err) {
    logger.error("Save failed", { error: err.message });
    return res.status(500).json({ error: "Save failed" });
  }

  res.json(result);
});
```

---

## 5. Code Quality (코드오류)

### 5-1. NULL Pointer Dereference (CWE-476)

null/undefined 값을 참조하면 프로그램이 비정상 종료됩니다.

```javascript
// UNSAFE — null 체크 없이 사용
router.get("/vuln/user/:id", async (req, res) => {
  const user = await User.findByPk(req.params.id);
  res.json({ name: user.name });  // user가 null이면 TypeError
});

// SAFE — null 체크 후 사용
router.get("/safe/user/:id", async (req, res) => {
  const user = await User.findByPk(req.params.id);
  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }
  res.json({ name: user.name });
});

// Optional chaining 활용
const name = user?.profile?.name ?? "Unknown";
```

---

### 5-2. Improper Resource Shutdown (CWE-404)

사용 후 리소스(파일, DB 연결, 소켓)를 해제하지 않으면 리소스 고갈이 발생합니다.

```javascript
// UNSAFE — 리소스 해제 누락
const mysql = require("mysql2/promise");

router.get("/vuln/data", async (req, res) => {
  const connection = await mysql.createConnection(dbConfig);
  const [rows] = await connection.execute("SELECT * FROM data");
  // connection.end() 누락 → 커넥션 풀 고갈
  res.json(rows);
});

// SAFE — finally로 확실히 해제
router.get("/safe/data", async (req, res) => {
  let connection;
  try {
    connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute("SELECT * FROM data");
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: "Database error" });
  } finally {
    if (connection) await connection.end();
  }
});

// 커넥션 풀 사용 (권장)
const pool = mysql.createPool(dbConfig);

router.get("/safe/data2", async (req, res) => {
  const [rows] = await pool.execute("SELECT * FROM data");
  // 풀이 자동으로 커넥션 반환 관리
  res.json(rows);
});
```

---

### 5-3. Deserialization of Untrusted Data (CWE-502)

신뢰할 수 없는 데이터를 역직렬화하면 임의 코드가 실행될 수 있습니다.

```javascript
// UNSAFE — node-serialize로 외부 데이터 역직렬화
const serialize = require("node-serialize");

router.post("/vuln/data", (req, res) => {
  const obj = serialize.unserialize(req.body.data);
  // node-serialize는 함수 실행 가능 → 원격 코드 실행 (RCE)
  res.json(obj);
});

// SAFE — JSON.parse()만 사용 (코드 실행 불가)
const Joi = require("joi");

const dataSchema = Joi.object({
  name: Joi.string().max(100).required(),
  age: Joi.number().integer().min(0).max(150),
});

router.post("/safe/data", (req, res) => {
  let parsed;
  try {
    parsed = JSON.parse(req.body.data);
  } catch {
    return res.status(400).json({ error: "Invalid JSON" });
  }
  // 스키마 검증
  const { error, value } = dataSchema.validate(parsed);
  if (error) {
    return res.status(400).json({ error: error.message });
  }
  res.json(value);
});
```

> **WARNING** `node-serialize`, `serialize-javascript`(eval 포함)은 원격 코드 실행이 가능합니다. 외부 입력에 절대 사용하지 마세요.

---

## 6. Encapsulation (캡슐화)

### 6-1. Data Leak Between Sessions (CWE-488, CWE-543)

사용자별 데이터가 공유 변수에 저장되면 세션 간 데이터가 유출됩니다.

```javascript
// UNSAFE — 모듈 수준 변수에 사용자 데이터 저장
let currentUser = null;  // 모든 요청이 공유

router.get("/vuln/dashboard", (req, res) => {
  currentUser = req.session.user;  // 동시 요청 시 덮어씌워짐
  // ... 비동기 작업 후
  res.send(`Hello ${currentUser.name}`);  // 다른 사용자 데이터 반환 가능
});

// SAFE — 요청 스코프 변수 사용
router.get("/safe/dashboard", (req, res) => {
  const currentUser = req.session.user;  // 요청별 로컬 변수
  res.send(`Hello ${currentUser.name}`);
});
```

---

### 6-2. Active Debug Code (CWE-489)

디버그 코드가 프로덕션에 남으면 시스템 내부 정보가 노출됩니다.

```javascript
// UNSAFE — 디버그 코드 잔존
console.log("DEBUG: user password =", password);
console.log("DEBUG: SQL query =", query);
app.use(require("morgan")("dev"));  // 상세 요청 로그

// SAFE — 환경 분기 + 구조화된 로거
const logger = require("winston");

// 프로덕션에서는 디버그 로그 비활성화
const logLevel = process.env.NODE_ENV === "production" ? "warn" : "debug";
logger.configure({ level: logLevel });

// morgan은 프로덕션에서 최소화
if (process.env.NODE_ENV !== "production") {
  app.use(require("morgan")("dev"));
} else {
  app.use(require("morgan")("combined", {
    stream: { write: (msg) => logger.info(msg.trim()) },
  }));
}
```

---

### 6-3. Private Data Returned from Public Method (CWE-495)

내부 배열/객체의 참조를 직접 반환하면 외부에서 수정이 가능합니다.

```javascript
// UNSAFE — 내부 배열의 참조를 직접 반환
class UserService {
  #users = [];

  getUsers() {
    return this.#users;  // 외부에서 push/pop 가능
  }
}

// SAFE — 복사본 반환
class UserService {
  #users = [];

  getUsers() {
    return [...this.#users];  // 얕은 복사
  }

  getUsersDeep() {
    return structuredClone(this.#users);  // 깊은 복사 (Node 17+)
  }
}
```

---

### 6-4. Public Data Assigned to Private Field (CWE-496)

외부 배열/객체를 내부 필드에 직접 할당하면 외부 변경이 내부에 반영됩니다.

```javascript
// UNSAFE — 외부 참조를 그대로 내부에 할당
class Config {
  #settings = {};

  setSettings(newSettings) {
    this.#settings = newSettings;  // 외부에서 변경 시 내부도 변경
  }
}

// SAFE — 복사본을 할당
class Config {
  #settings = {};

  setSettings(newSettings) {
    this.#settings = structuredClone(newSettings);
  }

  // 또는 Object.freeze로 불변 처리
  setSettingsFrozen(newSettings) {
    this.#settings = Object.freeze({ ...newSettings });
  }
}
```

---

## 7. API Misuse (API 오용)

### 7-1. Reliance on DNS Lookup (CWE-350)

DNS 기반 보안 결정은 DNS 스푸핑으로 우회될 수 있습니다.

```javascript
// UNSAFE — 역방향 DNS로 접근 제어
const dns = require("dns");

router.get("/vuln/internal", (req, res) => {
  dns.reverse(req.ip, (err, hostnames) => {
    if (hostnames && hostnames.includes("trusted.internal.com")) {
      return res.send("Internal data");
    }
    res.status(403).send("Forbidden");
  });
});

// SAFE — IP 주소 직접 비교
const TRUSTED_IPS = ["10.0.1.100", "10.0.1.101", "192.168.1.50"];

router.get("/safe/internal", (req, res) => {
  const clientIP = req.ip;
  if (!TRUSTED_IPS.includes(clientIP)) {
    return res.status(403).send("Forbidden");
  }
  res.send("Internal data");
});
```

---

### 7-2. Use of Vulnerable API

취약한 API/함수를 사용하면 보안 위협에 노출됩니다.

```javascript
// UNSAFE — deprecated 또는 취약 API 사용
const escaped = escape(userInput);       // deprecated
const decoded = unescape(escaped);       // deprecated
const buf = new Buffer(data);            // deprecated (보안 취약)
const hash = crypto.createHash("md5");   // 취약한 해시
setTimeout("doSomething()", 1000);       // 문자열 인자 → eval과 동일

// SAFE — 보안이 강화된 대체 API 사용
const encoded = encodeURIComponent(userInput);
const decoded = decodeURIComponent(encoded);
const buf = Buffer.from(data);              // Buffer.from() 사용
const hash = crypto.createHash("sha256");   // SHA-256 이상 사용
setTimeout(doSomething, 1000);              // 함수 참조 전달
```

> **TIP** `npm audit`를 정기적으로 실행하여 의존성 패키지의 알려진 취약점을 점검하세요.
