# Chapter 5. Web Service Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Web service assessment covers configuration checks for web server software like Apache and Nginx. This chapter covers 47 assessment items (WS-01 ~ WS-47) divided into 4 domains.

```
┌─────────────────────────────────────────────────────────────────┐
│          Web Service Vulnerability Assessment Domains (47)       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│               ┌─────────────────────────────┐                   │
│               │    Web Server (Apache/Nginx)         │                   │
│               └──────────────┬──────────────┘                   │
│                              │                                   │
│      ┌───────────────────────┼───────────────────────┐          │
│      │                       │                       │          │
│      ▼                       ▼                       ▼          │
│ ┌─────────┐           ┌─────────┐           ┌─────────┐        │
│ │ Account │           │ Service │           │ Security│        │
│ │  Mgmt   │           │  Mgmt   │           │ Settings│        │
│ │WS-01~05 │           │WS-06~30 │           │WS-31~43 │        │
│ │  (5)    │           │  (25)   │           │  (13)   │        │
│ │         │           │         │           │         │        │
│ │• Dedicated│         │• Dir    │           │• SSL/TLS│        │
│ │  account │          │  listing│           │• Security│       │
│ │• Shell   │          │  remove │           │  headers│        │
│ │  restrict│          │• Version│           │• Error  │        │
│ │• Perms   │          │  hide   │           │  pages  │        │
│ └────┬────┘           └────┬────┘           └────┬────┘        │
│      │                     │                     │              │
│      └─────────────────────┼─────────────────────┘              │
│                            ▼                                     │
│                    ┌─────────────┐                              │
│                    │ Patch/Log   │                              │
│                    │   Mgmt      │                              │
│                    │ WS-44~47   │                              │
│                    │   (4)      │                              │
│                    │            │                              │
│                    │• Latest    │                              │
│                    │  version   │                              │
│                    │• Log config│                              │
│                    └─────────────┘                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Domain | Items | Count |
|--------|-------|:-----:|
| Account Management | WS-01 ~ WS-05 | 5 |
| Service Management | WS-06 ~ WS-30 | 25 |
| Security Settings | WS-31 ~ WS-43 | 13 |
| Patch and Log Management | WS-44 ~ WS-47 | 4 |

---

## 5-1. Account Management (WS-01 ~ WS-05)

### WS-01. Use Dedicated Web Service Account

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Verify web service runs with minimal privilege account |
| **Criteria** | Good: Dedicated account (www-data, apache, etc.) / Vulnerable: Running as root |

#### Assessment Method

```bash
# Check Apache process account
ps aux | grep httpd | grep -v grep
ps aux | grep apache2 | grep -v grep

# Check Nginx process account
ps aux | grep nginx | grep -v grep
```

#### Remediation (Apache)

```bash
# /etc/httpd/conf/httpd.conf or /etc/apache2/envvars
User www-data
Group www-data
```

#### Remediation (Nginx)

```bash
# /etc/nginx/nginx.conf
user www-data;
```

> **WARNING**
> Running a web server as root puts the entire system at risk if vulnerabilities are exploited.

---

### WS-02. Restrict Web Service Account Shell

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block interactive login for web service account |

#### Assessment Method

```bash
# Check web service account shell
grep -E "www-data|apache|nginx" /etc/passwd
```

#### Recommended Setting

```bash
# Set shell to nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

---

### WS-03 ~ WS-05. Other Account Management

| Code | Item | Severity |
|------|------|:--------:|
| WS-03 | Web service account home directory permissions | Medium |
| WS-04 | Web service configuration file permissions | High |
| WS-05 | Web service log file permissions | Medium |

---

## 5-2. Service Management (WS-06 ~ WS-30)

### WS-06. Disable Directory Listing

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent directory content disclosure |
| **Criteria** | Good: Disabled / Vulnerable: Enabled |

#### Assessment Method (Apache)

```bash
# Check for Indexes option in httpd.conf
grep -r "Options.*Indexes" /etc/httpd/
grep -r "Options.*Indexes" /etc/apache2/
```

#### Remediation (Apache)

```apache
# Remove Indexes option
<Directory /var/www/html>
    Options -Indexes +FollowSymLinks
</Directory>
```

#### Remediation (Nginx)

```nginx
# Set autoindex off
location / {
    autoindex off;
}
```

---

### WS-07. Hide Web Server Version Information

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent targeted attacks through server version disclosure |

#### Assessment Method

```bash
# Check HTTP headers
curl -I http://localhost

# Check Server header in response
# Example: Server: Apache/2.4.41 (Ubuntu)
```

#### Remediation (Apache)

```apache
# /etc/httpd/conf/httpd.conf
ServerTokens Prod
ServerSignature Off
```

#### Remediation (Nginx)

```nginx
# /etc/nginx/nginx.conf
server_tokens off;
```

---

### WS-10. Restrict Unnecessary HTTP Methods

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block dangerous methods like PUT, DELETE |

#### Assessment Method

```bash
# Check allowed methods with OPTIONS
curl -X OPTIONS -I http://localhost
```

#### Remediation (Apache)

```apache
<Directory /var/www/html>
    <LimitExcept GET POST>
        Require all denied
    </LimitExcept>
</Directory>
```

#### Remediation (Nginx)

```nginx
if ($request_method !~ ^(GET|POST|HEAD)$ ) {
    return 405;
}
```

---

### WS-15. Restrict Symbolic Link Usage

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent filesystem access through symbolic links |

#### Remediation (Apache)

```apache
<Directory /var/www/html>
    Options -FollowSymLinks
    # Or use SymLinksIfOwnerMatch
    Options +SymLinksIfOwnerMatch
</Directory>
```

---

### WS-20. Remove Default Pages/Documents

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent information disclosure through default installation pages |

#### Check Targets

- Apache default page (/var/www/html/index.html)
- Nginx default page
- Sample applications
- Manual directories (/manual/)

---

## 5-3. Security Settings (WS-31 ~ WS-43)

### WS-31. Customize Error Pages

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent system information disclosure through error messages |

#### Remediation (Apache)

```apache
# Custom error page configuration
ErrorDocument 400 /error/400.html
ErrorDocument 401 /error/401.html
ErrorDocument 403 /error/403.html
ErrorDocument 404 /error/404.html
ErrorDocument 500 /error/500.html
```

#### Remediation (Nginx)

```nginx
error_page 404 /404.html;
error_page 500 502 503 504 /50x.html;

location = /404.html {
    root /var/www/error;
    internal;
}
```

---

### WS-35. SSL/TLS Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Ensure secure encrypted communication |

#### Recommended Settings (Apache)

```apache
# Allow only modern protocols
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1

# Secure cipher suites
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384

# Server cipher suite preference
SSLHonorCipherOrder on
```

#### Recommended Settings (Nginx)

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
```

> **TIP**
> You can test SSL configuration at SSL Labs (https://www.ssllabs.com/ssltest/).

---

### WS-40. Configure HTTP Security Headers

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| X-Content-Type-Options | Prevent MIME sniffing | nosniff |
| X-Frame-Options | Prevent clickjacking | DENY or SAMEORIGIN |
| X-XSS-Protection | XSS filter | 1; mode=block |
| Strict-Transport-Security | Force HTTPS | max-age=31536000 |
| Content-Security-Policy | Restrict content sources | Configure per policy |

#### Remediation (Apache)

```apache
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

#### Remediation (Nginx)

```nginx
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## 5-4. Patch and Log Management (WS-44 ~ WS-47)

### WS-44. Use Latest Web Server Version

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Patch known vulnerabilities |

#### Assessment Method

```bash
# Check Apache version
httpd -v
apache2 -v

# Check Nginx version
nginx -v
```

---

### WS-46. Log Configuration

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Record access and error logs |

#### Recommended Log Format (Apache)

```apache
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
CustomLog /var/log/httpd/access_log combined
ErrorLog /var/log/httpd/error_log
LogLevel warn
```

#### Recommended Log Format (Nginx)

```nginx
log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_x_forwarded_for"';

access_log /var/log/nginx/access.log main;
error_log /var/log/nginx/error.log warn;
```

---

## Web Service Assessment Script

### Apache Assessment Script

```bash
#!/bin/bash
#===============================================
# KESE KIT - Apache Web Server Vulnerability Check
#===============================================

echo "===== Apache Web Server Check ====="
echo "Check Date: $(date)"

# WS-01: Check running account
echo -e "\n[WS-01] Web Service Running Account"
APACHE_USER=$(ps aux | grep -E "httpd|apache2" | grep -v grep | head -1 | awk '{print $1}')
if [ "$APACHE_USER" != "root" ]; then
    echo "  [Good] Running account: $APACHE_USER"
else
    echo "  [Vulnerable] Running as root"
fi

# WS-06: Directory listing
echo -e "\n[WS-06] Directory Listing"
if grep -rq "Options.*Indexes" /etc/httpd/ /etc/apache2/ 2>/dev/null; then
    echo "  [Vulnerable] Indexes option found"
else
    echo "  [Good] Directory listing disabled"
fi

# WS-07: Version information
echo -e "\n[WS-07] Server Version Information"
SERVER_HEADER=$(curl -sI http://localhost 2>/dev/null | grep -i "^Server:")
if echo "$SERVER_HEADER" | grep -qE "[0-9]+\.[0-9]+"; then
    echo "  [Vulnerable] Version exposed: $SERVER_HEADER"
else
    echo "  [Good] Version information hidden"
fi

echo -e "\n===== Check Complete ====="
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Account Management | Dedicated account, shell restriction | Highest |
| Service Management | Directory listing, version hiding, method restriction | Highest |
| Security Settings | SSL/TLS, security headers | High |
| Patch/Log | Latest version, log configuration | High |

---

*Next Chapter: Chapter 6. Web Application Assessment*
