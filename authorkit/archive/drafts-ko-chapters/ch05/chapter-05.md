# 5장. 웹 서비스 점검

> Part II. 기술적 취약점 점검

---

## 개요

웹 서비스는 Apache, Nginx 등의 웹 서버 소프트웨어 설정에 대한 점검입니다. 이 장에서는 47개의 점검 항목(WS-01 ~ WS-47)을 4개 영역으로 나누어 설명합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│              웹 서비스 취약점 점검 영역 (47개 항목)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│               ┌─────────────────────────────┐                   │
│               │        웹 서버 (Apache/Nginx)         │                   │
│               └──────────────┬──────────────┘                   │
│                              │                                   │
│      ┌───────────────────────┼───────────────────────┐          │
│      │                       │                       │          │
│      ▼                       ▼                       ▼          │
│ ┌─────────┐           ┌─────────┐           ┌─────────┐        │
│ │ 계정    │           │ 서비스  │           │ 보안    │        │
│ │ 관리    │           │ 관리    │           │ 설정    │        │
│ │WS-01~05 │           │WS-06~30 │           │WS-31~43 │        │
│ │ (5개)   │           │ (25개)  │           │ (13개)  │        │
│ │         │           │         │           │         │        │
│ │• 전용   │           │• 디렉터 │           │• SSL/TLS│        │
│ │  계정   │           │  리 리스│           │• 보안   │        │
│ │• 쉘제한 │           │  팅 제거│           │  헤더   │        │
│ │• 권한   │           │• 버전   │           │• 에러   │        │
│ │  설정   │           │  숨김   │           │  페이지 │        │
│ └────┬────┘           └────┬────┘           └────┬────┘        │
│      │                     │                     │              │
│      └─────────────────────┼─────────────────────┘              │
│                            ▼                                     │
│                    ┌─────────────┐                              │
│                    │ 패치/로그   │                              │
│                    │   관리      │                              │
│                    │ WS-44~47   │                              │
│                    │  (4개)     │                              │
│                    │            │                              │
│                    │• 최신버전  │                              │
│                    │• 로그설정  │                              │
│                    └─────────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| 영역 | 항목 | 항목 수 |
|------|------|:------:|
| 계정 관리 | WS-01 ~ WS-05 | 5 |
| 서비스 관리 | WS-06 ~ WS-30 | 25 |
| 보안 설정 | WS-31 ~ WS-43 | 13 |
| 패치 및 로그 관리 | WS-44 ~ WS-47 | 4 |

---

## 5-1. 계정 관리 (WS-01 ~ WS-05)

### WS-01. 웹 서비스 전용 계정 사용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 웹 서비스가 최소 권한 계정으로 실행되는지 확인 |
| **판단 기준** | 양호: 전용 계정(www-data, apache 등) 사용 / 취약: root로 실행 |

#### 점검 방법

```bash
# Apache 실행 계정 확인
ps aux | grep httpd | grep -v grep
ps aux | grep apache2 | grep -v grep

# Nginx 실행 계정 확인
ps aux | grep nginx | grep -v grep
```

#### 조치 방법 (Apache)

```bash
# /etc/httpd/conf/httpd.conf 또는 /etc/apache2/envvars
User www-data
Group www-data
```

#### 조치 방법 (Nginx)

```bash
# /etc/nginx/nginx.conf
user www-data;
```

> **WARNING**
> 웹 서버를 root 계정으로 실행하면 취약점 발생 시 시스템 전체가 위험해집니다.

---

### WS-02. 웹 서비스 계정 쉘 제한

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 웹 서비스 계정의 대화형 로그인 차단 |

#### 점검 방법

```bash
# 웹 서비스 계정 쉘 확인
grep -E "www-data|apache|nginx" /etc/passwd
```

#### 권장 설정

```bash
# 쉘을 nologin으로 설정
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

---

### WS-03 ~ WS-05. 기타 계정 관리

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| WS-03 | 웹 서비스 계정 홈 디렉터리 권한 | 중 |
| WS-04 | 웹 서비스 설정 파일 권한 | 상 |
| WS-05 | 웹 서비스 로그 파일 권한 | 중 |

---

## 5-2. 서비스 관리 (WS-06 ~ WS-30)

### WS-06. 디렉터리 리스팅 제거

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 디렉터리 내용 노출 방지 |
| **판단 기준** | 양호: 비활성화 / 취약: 활성화 |

#### 점검 방법 (Apache)

```bash
# httpd.conf에서 Indexes 옵션 확인
grep -r "Options.*Indexes" /etc/httpd/
grep -r "Options.*Indexes" /etc/apache2/
```

#### 조치 방법 (Apache)

```apache
# Indexes 옵션 제거
<Directory /var/www/html>
    Options -Indexes +FollowSymLinks
</Directory>
```

#### 조치 방법 (Nginx)

```nginx
# autoindex off 설정
location / {
    autoindex off;
}
```

---

### WS-07. 웹 서비스 버전 정보 숨김

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 서버 버전 정보 노출로 인한 표적 공격 방지 |

#### 점검 방법

```bash
# HTTP 헤더 확인
curl -I http://localhost

# 응답에서 Server 헤더 확인
# 예: Server: Apache/2.4.41 (Ubuntu)
```

#### 조치 방법 (Apache)

```apache
# /etc/httpd/conf/httpd.conf
ServerTokens Prod
ServerSignature Off
```

#### 조치 방법 (Nginx)

```nginx
# /etc/nginx/nginx.conf
server_tokens off;
```

---

### WS-10. 불필요한 HTTP 메소드 제한

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | PUT, DELETE 등 위험한 메소드 차단 |

#### 점검 방법

```bash
# OPTIONS 메소드로 허용된 메소드 확인
curl -X OPTIONS -I http://localhost
```

#### 조치 방법 (Apache)

```apache
<Directory /var/www/html>
    <LimitExcept GET POST>
        Require all denied
    </LimitExcept>
</Directory>
```

#### 조치 방법 (Nginx)

```nginx
if ($request_method !~ ^(GET|POST|HEAD)$ ) {
    return 405;
}
```

---

### WS-15. 웹 서버 심볼릭 링크 사용 제한

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 심볼릭 링크를 통한 파일 시스템 접근 방지 |

#### 조치 방법 (Apache)

```apache
<Directory /var/www/html>
    Options -FollowSymLinks
    # 또는 SymLinksIfOwnerMatch 사용
    Options +SymLinksIfOwnerMatch
</Directory>
```

---

### WS-20. 기본 페이지/문서 제거

| 항목 | 내용 |
|------|------|
| **중요도** | 중 |
| **점검 목적** | 기본 설치 페이지로 인한 정보 노출 방지 |

#### 점검 대상

- Apache 기본 페이지 (/var/www/html/index.html)
- Nginx 기본 페이지
- 샘플 애플리케이션
- 매뉴얼 디렉터리 (/manual/)

---

## 5-3. 보안 설정 (WS-31 ~ WS-43)

### WS-31. 에러 페이지 커스터마이징

| 항목 | 내용 |
|------|------|
| **중요도** | 중 |
| **점검 목적** | 에러 메시지를 통한 시스템 정보 노출 방지 |

#### 조치 방법 (Apache)

```apache
# 커스텀 에러 페이지 설정
ErrorDocument 400 /error/400.html
ErrorDocument 401 /error/401.html
ErrorDocument 403 /error/403.html
ErrorDocument 404 /error/404.html
ErrorDocument 500 /error/500.html
```

#### 조치 방법 (Nginx)

```nginx
error_page 404 /404.html;
error_page 500 502 503 504 /50x.html;

location = /404.html {
    root /var/www/error;
    internal;
}
```

---

### WS-35. SSL/TLS 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 안전한 암호화 통신 보장 |

#### 권장 설정 (Apache)

```apache
# 최신 프로토콜만 허용
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1

# 안전한 암호화 스위트
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384

# 서버 암호화 스위트 우선
SSLHonorCipherOrder on
```

#### 권장 설정 (Nginx)

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
```

> **TIP**
> SSL Labs (https://www.ssllabs.com/ssltest/)에서 SSL 설정을 테스트할 수 있습니다.

---

### WS-40. HTTP 보안 헤더 설정

| 헤더 | 용도 | 권장 값 |
|------|------|---------|
| X-Content-Type-Options | MIME 스니핑 방지 | nosniff |
| X-Frame-Options | 클릭재킹 방지 | DENY 또는 SAMEORIGIN |
| X-XSS-Protection | XSS 필터 | 1; mode=block |
| Strict-Transport-Security | HTTPS 강제 | max-age=31536000 |
| Content-Security-Policy | 콘텐츠 출처 제한 | 정책에 맞게 설정 |

#### 조치 방법 (Apache)

```apache
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

#### 조치 방법 (Nginx)

```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## 5-4. 패치 및 로그 관리 (WS-44 ~ WS-47)

### WS-44. 웹 서버 최신 버전 사용

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 알려진 취약점 패치 |

#### 점검 방법

```bash
# Apache 버전 확인
httpd -v
apache2 -v

# Nginx 버전 확인
nginx -v
```

---

### WS-46. 로그 설정

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 접근 및 에러 로그 기록 |

#### 권장 로그 형식 (Apache)

```apache
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
CustomLog /var/log/httpd/access_log combined
ErrorLog /var/log/httpd/error_log
LogLevel warn
```

#### 권장 로그 형식 (Nginx)

```nginx
log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_x_forwarded_for"';

access_log /var/log/nginx/access.log main;
error_log /var/log/nginx/error.log warn;
```

---

## 웹 서비스 점검 스크립트

### Apache 점검 스크립트

```bash
#!/bin/bash
#===============================================
# KESE KIT - Apache 웹 서버 취약점 점검
#===============================================

echo "===== Apache 웹 서버 점검 ====="
echo "점검 일시: $(date)"

# WS-01: 실행 계정 확인
echo -e "\n[WS-01] 웹 서비스 실행 계정"
APACHE_USER=$(ps aux | grep -E "httpd|apache2" | grep -v grep | head -1 | awk '{print $1}')
if [ "$APACHE_USER" != "root" ]; then
    echo "  [양호] 실행 계정: $APACHE_USER"
else
    echo "  [취약] root 계정으로 실행 중"
fi

# WS-06: 디렉터리 리스팅
echo -e "\n[WS-06] 디렉터리 리스팅"
if grep -rq "Options.*Indexes" /etc/httpd/ /etc/apache2/ 2>/dev/null; then
    echo "  [취약] Indexes 옵션 발견"
else
    echo "  [양호] 디렉터리 리스팅 비활성화"
fi

# WS-07: 버전 정보
echo -e "\n[WS-07] 서버 버전 정보"
SERVER_HEADER=$(curl -sI http://localhost 2>/dev/null | grep -i "^Server:")
if echo "$SERVER_HEADER" | grep -qE "[0-9]+\.[0-9]+"; then
    echo "  [취약] 버전 노출: $SERVER_HEADER"
else
    echo "  [양호] 버전 정보 숨김"
fi

echo -e "\n===== 점검 완료 ====="
```

---

## 요약

| 영역 | 핵심 점검 항목 | 우선순위 |
|------|---------------|:--------:|
| 계정 관리 | 전용 계정 사용, 쉘 제한 | 최우선 |
| 서비스 관리 | 디렉터리 리스팅, 버전 숨김, 메소드 제한 | 최우선 |
| 보안 설정 | SSL/TLS, 보안 헤더 | 높음 |
| 패치/로그 | 최신 버전, 로그 설정 | 높음 |

---

*다음 장: 6장. 웹 애플리케이션 점검*
