# Certificate & Protocol Security

> Source: 로봇 보안취약점 점검 체크리스트 해설서 (KISA)
> Checklist refs: IA-04, ER-01

---

## 1. OpenSSL Certificate Inspection (IA-04)

```bash
# 인증서 내용 확인 명령어
openssl x509 -in server.crt -text -noout
```

---

## 2. Key File Permission Hardening (IA-04)

```bash
# 개인키 접근 권한 설정
chown robot-service:robot-service /etc/robot/keys/device.key
chmod 600 /etc/robot/keys/device.key  # 파일 소유자만 접근 가능
```

---

## 3. OPC UA Security Configuration (IA-04)

### 3.1 Certificate Validation

```ini
# server.conf (OPC UA 서버 인증서 검증 활성화 설정)
ValidateCertificates = True        # 인증서 검증 수행
RejectUnknownCertificates = True   # 검증 실패 시 차단
```

### 3.2 Certificate Revocation Check

```ini
# server.conf (OPC UA 서버 인증서 폐지 검증 활성화 설정)
ValidateCertificates = True          # 인증서 검증 수행
RevocationCheck = True               # 인증서 폐지 상태 확인 활성화
RejectUnknownCertificates = True     # 검증 실패 시 차단
```

---

## 4. TLS Client Certificate Verification - Python (IA-04)

```python
import ssl, socket

context = ssl.create_default_context()
context.verify_mode = ssl.CERT_REQUIRED       # 인증서 검증
context.check_hostname = True                 # 인증서 CN/SAN 검증

with socket.create_connection(("server.com", 443)) as sock:
    with context.wrap_socket(sock, server_hostname="server.com") as ssock:
        print("TLS Established:", ssock.version())
```

---

## 5. Crypto Algorithm Requirements (IA-04)

| Category | Recommended | Insufficient |
|---|---|---|
| Key algorithm | RSA >= 2048bit or ECC P-256+ | RSA 1024bit or below, ECC P-192 or below |
| Hash algorithm | SHA-256+ (SHA-2/SHA-3 family) | SHA-1, MD5 |
| TLS protocol | TLS 1.2+ (recommended: TLS 1.3) | TLS 1.0 / 1.1 |

---

## 6. Audit Log API Access (ER-01)

```http
GET /api/audit/logs
Authorization: Bearer <AdminToken>

HTTP/1.1 200 OK
{
    "entries": [...],
    "integrity": "sha256:f45a..."
}
```

---

## 7. Platform-specific Certificate ACL Examples (IA-04)

| Platform | Certificate Store |
|---|---|
| General server / cloud | DB table |
| OPC UA | /pki/trusted, /pki/rejected folders |
| MQTT mTLS | CA DB, allowed client certificate list |
| Robot PKI | KV DB, HSM integration |
