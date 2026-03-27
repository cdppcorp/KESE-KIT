---
name: guide
description: AI 도구(Claude, ChatGPT, Cursor, Copilot)용 시큐어 코딩 프롬프트와 가이드를 생성합니다. KISA CII 가이드라인과 CWE 매핑 취약점 패턴을 따르는 보안 코드 작성을 위한 복사-붙여넣기 가능한 프롬프트를 생성합니다. "보안 가이드 생성", "AI 보안 프롬프트", "시큐어코딩 가이드", "AI에게 안전한 코드 요청" 시 사용하세요.
---

# KESE 시큐어 코딩 프롬프트 생성기

KISA CII 가이드라인과 국제 표준(OWASP, CWE)을 기반으로 AI 도구용 시큐어 코딩 프롬프트를 생성합니다. AI 어시스턴트가 보안 코드를 작성하도록 지시하는 복사-붙여넣기 가능한 프롬프트를 생성합니다.

## 실행 흐름

1. 사용자에게 대상 컨텍스트 확인 (언어, 프레임워크, 기능 유형)
2. 커스터마이징된 시큐어 코딩 프롬프트 생성
3. 관련 CWE 패턴 및 KISA 가이드라인 포함
4. 복사-붙여넣기 형식으로 프롬프트 제공

---

## 범용 시큐어 코딩 프롬프트

```markdown
# 시큐어 코딩 요구사항

코드 작성 시 다음 보안 요구사항을 따르세요:

## 입력값 검증
- 모든 사용자 입력 검증 (타입, 길이, 형식, 범위)
- 데이터베이스 작업에 매개변수화된 쿼리 사용
- 명령어 또는 파일 경로에 사용하기 전 입력값 소독
- 블랙리스트보다 화이트리스트 검증 구현

## 인증 및 세션
- 강력한 패스워드 해싱 사용 (bcrypt, Argon2, PBKDF2)
- 세션 타임아웃 구현 (최대 30분 유휴)
- 로그인 후 세션 ID 재생성
- secure, HttpOnly, SameSite 쿠키 사용

## 데이터 보호
- 모든 데이터 전송에 HTTPS/TLS 1.2+ 사용
- 저장 시 민감 데이터 암호화 (AES-256)
- 자격 증명 하드코딩 금지 (환경 변수 사용)
- 로그에서 PII 마스킹

## 에러 처리
- 사용자에게 스택 트레이스 노출 금지
- 에러는 서버 측에서만 로깅
- 사용자에게는 일반적인 에러 메시지 사용
- 적절한 예외 처리 구현

## 접근 제어
- 최소 권한 원칙 적용
- 모든 요청에서 권한 검증
- RBAC 또는 ABAC 패턴 사용
- 리소스 소유권 검증

## 코드 품질
- 더 이상 사용되지 않는/위험한 함수 피하기
- 리소스 적절히 닫기 (파일, 연결)
- null/undefined 값 처리
- 제한 없는 무한 루프와 재귀 피하기
```

---

## 언어별 프롬프트

### Python 시큐어 코딩

```markdown
# Python 시큐어 코딩 요구사항

Python 코드 작성 시 다음 패턴을 따르세요:

## SQL Injection 방지 (CWE-89)
```python
# 취약 - 절대 이렇게 하지 마세요
query = f"SELECT * FROM users WHERE id = {user_id}"

# 안전 - 매개변수화된 쿼리 사용
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# 안전 - ORM 사용
User.objects.filter(id=user_id)
```

## Command Injection 방지 (CWE-78)
```python
# 취약 - 사용자 입력과 shell=True 사용 금지
subprocess.run(f"ls {user_path}", shell=True)

# 안전 - 인자 리스트 사용
subprocess.run(["ls", user_path], shell=False)

# 안전 - shlex.quote 사용
import shlex
subprocess.run(f"ls {shlex.quote(user_path)}", shell=True)
```

## 경로 조작 방지 (CWE-22)
```python
# 취약
open(f"/uploads/{filename}")

# 안전 - 경로 검증
import os
base_dir = "/uploads"
full_path = os.path.realpath(os.path.join(base_dir, filename))
if not full_path.startswith(base_dir):
    raise ValueError("잘못된 경로")
```

## 안전한 역직렬화 (CWE-502)
```python
# 취약 - 사용자 데이터에 pickle 사용 금지
import pickle
data = pickle.loads(user_input)

# 안전 - JSON 사용
import json
data = json.loads(user_input)

# 안전 - yaml.safe_load 사용
import yaml
data = yaml.safe_load(user_input)
```

## 패스워드 해싱 (CWE-916)
```python
# 취약
import hashlib
hashed = hashlib.sha256(password.encode()).hexdigest()

# 안전 - bcrypt 사용
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```
```

### JavaScript/Node.js 시큐어 코딩

```markdown
# JavaScript 시큐어 코딩 요구사항

JavaScript/Node.js 코드 작성 시 다음 패턴을 따르세요:

## XSS 방지 (CWE-79)
```javascript
// 취약 - 사용자 입력 직접 삽입 금지
element.innerHTML = userInput;

// 안전 - textContent 사용
element.textContent = userInput;

// 안전 - HTML용 DOMPurify 사용
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// React - dangerouslySetInnerHTML 피하기
// 취약
<div dangerouslySetInnerHTML={{__html: userInput}} />

// 안전 - React 자동 이스케이프 허용
<div>{userInput}</div>
```

## SQL Injection 방지 (CWE-89)
```javascript
// 취약
const query = `SELECT * FROM users WHERE id = ${userId}`;

// 안전 - 매개변수화된 쿼리 사용
const query = 'SELECT * FROM users WHERE id = $1';
await client.query(query, [userId]);

// 안전 - ORM 사용
await User.findOne({ where: { id: userId } });
```

## Command Injection 방지 (CWE-78)
```javascript
// 취약
const { exec } = require('child_process');
exec(`ls ${userPath}`);

// 안전 - 인자와 함께 execFile 사용
const { execFile } = require('child_process');
execFile('ls', [userPath]);
```

## 경로 조작 방지 (CWE-22)
```javascript
// 취약
const filePath = path.join('/uploads', userFilename);

// 안전 - 경로 검증
const path = require('path');
const baseDir = '/uploads';
const filePath = path.resolve(baseDir, userFilename);
if (!filePath.startsWith(baseDir)) {
  throw new Error('잘못된 경로');
}
```

## 안전한 난수 생성 (CWE-330)
```javascript
// 취약 - 예측 가능
const token = Math.random().toString(36);

// 안전 - 암호화적 난수
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');
```
```

### Java 시큐어 코딩

```markdown
# Java 시큐어 코딩 요구사항

Java 코드 작성 시 다음 패턴을 따르세요:

## SQL Injection 방지 (CWE-89)
```java
// 취약
String query = "SELECT * FROM users WHERE id = " + userId;

// 안전 - PreparedStatement 사용
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ?"
);
stmt.setString(1, userId);

// 안전 - JPA/Hibernate 사용
User user = entityManager.find(User.class, userId);
```

## XXE 방지 (CWE-611)
```java
// 취약
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

// 안전 - 외부 엔티티 비활성화
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
```

## 경로 조작 방지 (CWE-22)
```java
// 취약
File file = new File("/uploads/" + filename);

// 안전 - 정규화된 경로 검증
File baseDir = new File("/uploads");
File file = new File(baseDir, filename);
if (!file.getCanonicalPath().startsWith(baseDir.getCanonicalPath())) {
    throw new SecurityException("잘못된 경로");
}
```

## 안전한 역직렬화 (CWE-502)
```java
// 취약 - 신뢰되지 않은 데이터 역직렬화 금지
ObjectInputStream ois = new ObjectInputStream(input);
Object obj = ois.readObject();

// 안전 - 화이트리스트 사용
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "java.base/*;!*"
);
ois.setObjectInputFilter(filter);
```
```

---

## 기능별 프롬프트

### 인증 구현

```markdown
# 안전한 인증 요구사항

인증 구현 시:

1. **패스워드 저장**
   - bcrypt/Argon2/PBKDF2 사용, cost factor >= 10
   - 평문 또는 약한 해시(MD5, SHA1) 저장 금지

2. **로그인 프로세스**
   - 계정 잠금 구현 (5회 시도, 30분 잠금)
   - 패스워드에 상수 시간 비교 사용
   - 로그인 성공 후 세션 ID 재생성
   - 모든 인증 시도 로깅

3. **세션 관리**
   - 세션 타임아웃 설정 (15-30분 유휴)
   - secure, HttpOnly, SameSite=Strict 쿠키 사용
   - 적절한 로그아웃 구현 (서버 세션 파기)

4. **MFA**
   - 민감한 작업에 TOTP 또는 WebAuthn 구현
   - MFA 시도 요청 제한

5. **패스워드 재설정**
   - 시간 제한 토큰 사용 (15-60분)
   - 보안 채널로 전송 (HTTPS 링크)
   - 사용 후 토큰 무효화
   - 이메일 존재 여부 노출 금지
```

### 파일 업로드 구현

```markdown
# 안전한 파일 업로드 요구사항

파일 업로드 구현 시:

1. **검증**
   - 파일 확장자 확인 (화이트리스트: .jpg, .png, .pdf 등)
   - MIME 타입 검증 (Content-Type 헤더만 신뢰 금지)
   - 파일 크기 제한 (예: 최대 10MB)
   - 가능하면 악성코드 스캔

2. **저장**
   - 웹 루트 외부에 저장
   - 랜덤 파일명 생성 (UUID)
   - 실행 위험 방지를 위해 원본 확장자 유지 금지
   - 제한적 권한 설정 (0644)

3. **제공**
   - Content-Disposition: attachment 사용
   - 올바른 Content-Type 설정
   - 서명된 URL이 있는 CDN 고려

4. **처리**
   - 이미지 재처리 (메타데이터 제거, 리사이즈)
   - 업로드된 파일 실행 금지
   - 처리 전 격리
```

### API 보안 구현

```markdown
# 안전한 API 요구사항

API 구현 시:

1. **인증**
   - 적절한 검증으로 JWT 사용 (알고리즘, 만료, 발급자)
   - API 키 순환 구현
   - 서드파티 접근에 OAuth 2.0 사용

2. **권한 부여**
   - 모든 엔드포인트에서 권한 검증
   - 요청 제한 구현 (사용자/IP별)
   - 중앙 집중 제어를 위한 API 게이트웨이 사용

3. **입출력**
   - 모든 입력 검증 (타입, 길이, 형식)
   - 출력 소독 (인젝션 방지)
   - 적절한 HTTP 메서드 사용

4. **전송**
   - HTTPS만 사용 (TLS 1.2+)
   - 보안 헤더 설정 (CORS, HSTS)
   - 민감한 작업에 요청 서명 구현

5. **로깅**
   - 모든 API 접근 로깅 (누가, 무엇을, 언제)
   - 민감 데이터 로깅 금지
   - 이상 징후 모니터링
```

---

## CWE 빠른 참조

| CWE | 이름 | 방지 방법 |
|-----|------|----------|
| CWE-20 | 부적절한 입력 검증 | 모든 입력 검증 |
| CWE-22 | 경로 조작 | 경로 정규화 및 검증 |
| CWE-78 | OS Command Injection | shell 피하기, 인자 리스트 사용 |
| CWE-79 | XSS | 출력 인코딩, CSP 사용 |
| CWE-89 | SQL Injection | 매개변수화된 쿼리 사용 |
| CWE-94 | Code Injection | eval(), exec() 피하기 |
| CWE-287 | 부적절한 인증 | 검증된 인증 프레임워크 사용 |
| CWE-327 | 약한 암호화 | AES-256, RSA-2048+ 사용 |
| CWE-352 | CSRF | CSRF 토큰 사용 |
| CWE-434 | 무제한 업로드 | 타입, 크기, 이름 검증 |
| CWE-502 | 안전하지 않은 역직렬화 | 안전한 형식 사용 (JSON) |
| CWE-611 | XXE | 외부 엔티티 비활성화 |
| CWE-798 | 하드코딩된 자격 증명 | 환경 변수 사용 |
| CWE-918 | SSRF | URL 검증, 사설 IP 차단 |

---

## 사용법

관련 프롬프트를 복사하여 AI 어시스턴트 대화에 붙여넣은 후 코드 작성을 요청하세요. 이렇게 하면 AI가 시큐어 코딩 관행을 따르도록 준비됩니다.

예시:
```
[여기에 시큐어 코딩 요구사항 붙여넣기]

이제 Python/FastAPI로 사용자명, 이메일, 패스워드를 받는 사용자 등록 엔드포인트를 구현해주세요.
```
