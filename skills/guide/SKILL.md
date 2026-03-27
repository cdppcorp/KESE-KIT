---
name: guide
description: Generate secure coding prompts and guides for AI tools (Claude, ChatGPT, Cursor, Copilot). Creates copy-paste ready prompts that instruct AI to write secure code following KISA CII guidelines and CWE-mapped vulnerability patterns. Use when "generate secure guide", "AI prompt for security", "secure coding guide", "how to ask AI for secure code".
---

# KESE Secure Coding Prompt Generator

Generate secure coding prompts for AI tools based on KISA CII guidelines and international standards (OWASP, CWE). Create copy-paste ready prompts that instruct AI assistants to write secure code.

## Execution Flow

1. Ask user for target context (language, framework, feature type)
2. Generate customized secure coding prompt
3. Include relevant CWE patterns and KISA guidelines
4. Provide the prompt in copy-paste format

---

## Universal Secure Coding Prompt

```markdown
# Secure Coding Requirements

When writing code, follow these security requirements:

## Input Validation
- Validate all user inputs (type, length, format, range)
- Use parameterized queries for database operations
- Sanitize inputs before use in commands or file paths
- Implement allowlist validation over blocklist

## Authentication & Session
- Use strong password hashing (bcrypt, Argon2, PBKDF2)
- Implement session timeout (max 30 minutes idle)
- Regenerate session ID after login
- Use secure, HttpOnly, SameSite cookies

## Data Protection
- Use HTTPS/TLS 1.2+ for all data transmission
- Encrypt sensitive data at rest (AES-256)
- Never hardcode credentials (use environment variables)
- Mask PII in logs

## Error Handling
- Never expose stack traces to users
- Log errors server-side only
- Use generic error messages for users
- Implement proper exception handling

## Access Control
- Apply least privilege principle
- Verify authorization on every request
- Use RBAC or ABAC patterns
- Validate resource ownership

## Code Quality
- Avoid deprecated/dangerous functions
- Close resources properly (files, connections)
- Handle null/undefined values
- Avoid infinite loops and recursion without limits
```

---

## Language-Specific Prompts

### Python Secure Coding

```markdown
# Python Secure Coding Requirements

When writing Python code, follow these patterns:

## SQL Injection Prevention (CWE-89)
```python
# VULNERABLE - Never do this
query = f"SELECT * FROM users WHERE id = {user_id}"

# SECURE - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# SECURE - Use ORM
User.objects.filter(id=user_id)
```

## Command Injection Prevention (CWE-78)
```python
# VULNERABLE - Never use shell=True with user input
subprocess.run(f"ls {user_path}", shell=True)

# SECURE - Use argument list
subprocess.run(["ls", user_path], shell=False)

# SECURE - Use shlex.quote
import shlex
subprocess.run(f"ls {shlex.quote(user_path)}", shell=True)
```

## Path Traversal Prevention (CWE-22)
```python
# VULNERABLE
open(f"/uploads/{filename}")

# SECURE - Validate path
import os
base_dir = "/uploads"
full_path = os.path.realpath(os.path.join(base_dir, filename))
if not full_path.startswith(base_dir):
    raise ValueError("Invalid path")
```

## Secure Deserialization (CWE-502)
```python
# VULNERABLE - Never unpickle user data
import pickle
data = pickle.loads(user_input)

# SECURE - Use JSON
import json
data = json.loads(user_input)

# SECURE - Use yaml.safe_load
import yaml
data = yaml.safe_load(user_input)
```

## Password Hashing (CWE-916)
```python
# VULNERABLE
import hashlib
hashed = hashlib.sha256(password.encode()).hexdigest()

# SECURE - Use bcrypt
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```
```

### JavaScript/Node.js Secure Coding

```markdown
# JavaScript Secure Coding Requirements

When writing JavaScript/Node.js code, follow these patterns:

## XSS Prevention (CWE-79)
```javascript
// VULNERABLE - Never insert user input directly
element.innerHTML = userInput;

// SECURE - Use textContent
element.textContent = userInput;

// SECURE - Use DOMPurify for HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// React - Avoid dangerouslySetInnerHTML
// VULNERABLE
<div dangerouslySetInnerHTML={{__html: userInput}} />

// SECURE - Let React escape automatically
<div>{userInput}</div>
```

## SQL Injection Prevention (CWE-89)
```javascript
// VULNERABLE
const query = `SELECT * FROM users WHERE id = ${userId}`;

// SECURE - Use parameterized queries
const query = 'SELECT * FROM users WHERE id = $1';
await client.query(query, [userId]);

// SECURE - Use ORM
await User.findOne({ where: { id: userId } });
```

## Command Injection Prevention (CWE-78)
```javascript
// VULNERABLE
const { exec } = require('child_process');
exec(`ls ${userPath}`);

// SECURE - Use execFile with arguments
const { execFile } = require('child_process');
execFile('ls', [userPath]);
```

## Path Traversal Prevention (CWE-22)
```javascript
// VULNERABLE
const filePath = path.join('/uploads', userFilename);

// SECURE - Validate path
const path = require('path');
const baseDir = '/uploads';
const filePath = path.resolve(baseDir, userFilename);
if (!filePath.startsWith(baseDir)) {
  throw new Error('Invalid path');
}
```

## Secure Random Generation (CWE-330)
```javascript
// VULNERABLE - Predictable
const token = Math.random().toString(36);

// SECURE - Cryptographic
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');
```
```

### Java Secure Coding

```markdown
# Java Secure Coding Requirements

When writing Java code, follow these patterns:

## SQL Injection Prevention (CWE-89)
```java
// VULNERABLE
String query = "SELECT * FROM users WHERE id = " + userId;

// SECURE - Use PreparedStatement
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ?"
);
stmt.setString(1, userId);

// SECURE - Use JPA/Hibernate
User user = entityManager.find(User.class, userId);
```

## XXE Prevention (CWE-611)
```java
// VULNERABLE
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

// SECURE - Disable external entities
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
```

## Path Traversal Prevention (CWE-22)
```java
// VULNERABLE
File file = new File("/uploads/" + filename);

// SECURE - Validate canonical path
File baseDir = new File("/uploads");
File file = new File(baseDir, filename);
if (!file.getCanonicalPath().startsWith(baseDir.getCanonicalPath())) {
    throw new SecurityException("Invalid path");
}
```

## Secure Deserialization (CWE-502)
```java
// VULNERABLE - Never deserialize untrusted data
ObjectInputStream ois = new ObjectInputStream(input);
Object obj = ois.readObject();

// SECURE - Use allowlist
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "java.base/*;!*"
);
ois.setObjectInputFilter(filter);
```
```

---

## Feature-Specific Prompts

### Authentication Implementation

```markdown
# Secure Authentication Requirements

When implementing authentication:

1. **Password Storage**
   - Use bcrypt/Argon2/PBKDF2 with cost factor >= 10
   - Never store plaintext or weak hashes (MD5, SHA1)

2. **Login Process**
   - Implement account lockout (5 attempts, 30-min lock)
   - Use constant-time comparison for passwords
   - Regenerate session ID after successful login
   - Log all authentication attempts

3. **Session Management**
   - Set session timeout (15-30 minutes idle)
   - Use secure, HttpOnly, SameSite=Strict cookies
   - Implement proper logout (destroy server session)

4. **MFA**
   - Implement TOTP or WebAuthn for sensitive operations
   - Rate limit MFA attempts

5. **Password Reset**
   - Use time-limited tokens (15-60 minutes)
   - Send via secure channel (HTTPS link)
   - Invalidate token after use
   - Don't reveal if email exists
```

### File Upload Implementation

```markdown
# Secure File Upload Requirements

When implementing file uploads:

1. **Validation**
   - Check file extension (allowlist: .jpg, .png, .pdf, etc.)
   - Validate MIME type (don't trust Content-Type header alone)
   - Limit file size (e.g., max 10MB)
   - Scan for malware if possible

2. **Storage**
   - Store outside web root
   - Generate random filenames (UUID)
   - Don't preserve original extension for execution risk
   - Set restrictive permissions (0644)

3. **Serving**
   - Use Content-Disposition: attachment
   - Set correct Content-Type
   - Consider CDN with signed URLs

4. **Processing**
   - Reprocess images (strip metadata, resize)
   - Don't execute uploaded files
   - Quarantine before processing
```

### API Security Implementation

```markdown
# Secure API Requirements

When implementing APIs:

1. **Authentication**
   - Use JWT with proper validation (algorithm, expiry, issuer)
   - Implement API key rotation
   - Use OAuth 2.0 for third-party access

2. **Authorization**
   - Verify permissions on every endpoint
   - Implement rate limiting (per user/IP)
   - Use API gateway for centralized control

3. **Input/Output**
   - Validate all inputs (type, length, format)
   - Sanitize outputs (prevent injection)
   - Use appropriate HTTP methods

4. **Transport**
   - HTTPS only (TLS 1.2+)
   - Set security headers (CORS, HSTS)
   - Implement request signing for sensitive operations

5. **Logging**
   - Log all API access (who, what, when)
   - Don't log sensitive data
   - Monitor for anomalies
```

---

## CWE Quick Reference

| CWE | Name | Prevention |
|-----|------|------------|
| CWE-20 | Improper Input Validation | Validate all inputs |
| CWE-22 | Path Traversal | Canonicalize and validate paths |
| CWE-78 | OS Command Injection | Avoid shell, use argument lists |
| CWE-79 | XSS | Encode output, use CSP |
| CWE-89 | SQL Injection | Use parameterized queries |
| CWE-94 | Code Injection | Avoid eval(), exec() |
| CWE-287 | Improper Authentication | Use proven auth frameworks |
| CWE-327 | Weak Crypto | Use AES-256, RSA-2048+ |
| CWE-352 | CSRF | Use CSRF tokens |
| CWE-434 | Unrestricted Upload | Validate type, size, name |
| CWE-502 | Insecure Deserialization | Use safe formats (JSON) |
| CWE-611 | XXE | Disable external entities |
| CWE-798 | Hardcoded Credentials | Use environment variables |
| CWE-918 | SSRF | Validate URLs, block private IPs |

---

## Usage

Copy the relevant prompt and paste it into your AI assistant conversation before asking it to write code. This primes the AI to follow secure coding practices.

Example:
```
[Paste secure coding requirements here]

Now, please implement a user registration endpoint in Python/FastAPI that accepts username, email, and password.
```
