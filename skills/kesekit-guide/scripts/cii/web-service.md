# 웹 서비스 점검 스크립트 (WEB-01 ~ WEB-26)

## 1. 계정 관리

### WEB-01: Default 관리자 계정명 변경
**점검:**
```bash
# Tomcat - 기본 계정명(tomcat, admin) 사용 여부 확인
grep -i 'username=' <Tomcat_DIR>/conf/server.xml
# JEUS - Security Domains > Account & Policies > Users에서 기본 계정 확인
```
**조치:**
```bash
# Tomcat - 기본 계정명을 유추 불가능한 이름으로 변경
vi <Tomcat_DIR>/conf/server.xml
# <user username="custom_admin" password="XNDJxndn264!@" roles="manager-gui"/>
systemctl restart tomcat

# JEUS - Lock & EDIT > Security > Security Domains > Users > ADD
# administrator 대신 유추 불가능한 계정명 입력 후 Administrators 그룹 체크
./stopServer -host <도메인명>:<포트>
./startDomainAdminServer -host <도메인명>:<포트>
```

### WEB-02: 취약한 비밀번호 사용 제한
**점검:**
```bash
# Tomcat
grep -i 'password=' <Tomcat_DIR>/conf/server.xml
# 비밀번호 복잡도 기준: 2종류 이상 조합 최소 10자리 또는 3종류 이상 조합 최소 8자리
# (영문대/소문자, 숫자, 특수문자)
```
**조치:**
```bash
# Tomcat - 복잡도 만족하는 비밀번호 설정
vi <Tomcat_DIR>/conf/server.xml
# <user username="admin" password="XNDJxndn264!@" roles="manager-gui"/>
systemctl restart tomcat

# JEUS - Lock & EDIT > Security > Security Domains > Users > 비밀번호 변경
# SHA-256 이상 암호화 방식 비밀번호 설정
```

### WEB-03: 비밀번호 파일 권한 관리
**점검:**
```bash
# Tomcat
ls -al <Tomcat_DIR>/conf/tomcat-users.xml
# IIS
# %systemroot%\system32\config\SAM 파일 속성 > 보안 확인
# JEUS
ls -al <JEUS_DIR>/jeus_domain/config/security/SYSTEM_DOMAIN/accounts.xml
ls -al <JEUS_DIR>/jeus_domain/config/security/SYSTEM_DOMAIN/policies.xml
```
**조치:**
```bash
# Tomcat - 비밀번호 파일 권한 600 이하 설정
chmod 600 <Tomcat_DIR>/conf/tomcat-users.xml

# IIS - SAM 파일 속성 > 보안 > 편집 > Administrators, SYSTEM만 허용

# JEUS
chmod 600 <JEUS_DIR>/jeus_domain/config/security/SYSTEM_DOMAIN/accounts.xml
chmod 600 <JEUS_DIR>/jeus_domain/config/security/SYSTEM_DOMAIN/policies.xml
```

---

## 2. 서비스 관리

### WEB-04: 디렉터리 리스팅 방지 설정
**점검:**
```bash
# Apache
grep -i "Options" /etc/httpd/conf/httpd.conf | grep -i "Indexes"
# Nginx
grep -i "autoindex" /etc/nginx/nginx.conf
# Tomcat
grep -i "listings" <Tomcat_DIR>/conf/web.xml
# JEUS
grep -i "allow-indexing" <JEUS_DIR>/WEB-INF/jeus-web-dd.xml
# WebtoB
grep -i "Options" <WebtoB_DIR>/config/http.m | grep -i "Indexes"
```
**조치:**
```bash
# Apache - httpd.conf 내 모든 디렉터리에서 Indexes 옵션 제거
vi <Apache_DIR>/conf/httpd.conf
# <Directory />
#   Options -Indexes  (Indexes 삭제 또는 -Indexes 설정)
# </Directory>
systemctl restart apache2

# Tomcat - web.xml 내 listings=false 설정
vi <Tomcat_DIR>/conf/web.xml
# <init-param>
#   <param-name>listings</param-name>
#   <param-value>false</param-value>
# </init-param>

# Nginx - autoindex off 설정
vi <Nginx_DIR>/conf/nginx.conf
# server { autoindex off; }
systemctl restart nginx

# IIS - IIS 관리자 > 해당 웹사이트 > 디렉터리 검색 > "사용 안 함" 설정

# JEUS
vi <JEUS_DIR>/WEB-INF/jeus-web-dd.xml
# <allow-indexing>false</allow-indexing>

# WebtoB
vi <WebtoB_DIR>/config/http.m
# *NODE
#   Options = "-Indexes",
wscfl -I http.m && wsdown && wsboot
```

### WEB-05: 지정하지 않은 CGI/ISAPI 실행 제한
**점검:**
```bash
# Apache
grep -i "LoadModule.*cgi" <Apache_DIR>/conf/httpd.conf
grep -i "ExecCGI" <Apache_DIR>/conf/httpd.conf
# Nginx
grep -i "fastcgi_pass" <Nginx_DIR>/conf/nginx.conf
```
**조치:**
```bash
# Apache - CGI 모듈 비활성화 및 ExecCGI 옵션 제거
vi <Apache_DIR>/conf/httpd.conf
# #LoadModule cgi_module modules/mod_cgi.so
# #LoadModule cgid_module modules/mod_cgid.so
# <Directory "/var/www/cgi-bin">
#   Options -ExecCGI
# </Directory>
systemctl restart apache2

# Tomcat - web.xml 내 CGI 매핑 비활성화(주석 처리)
# <!-- <servlet-mapping>
#   <servlet-name>cgi</servlet-name>
#   <url-pattern>/cgi-bin/*</url-pattern>
# </servlet-mapping> -->

# Nginx - fastcgi 설정 주석 처리
# location ~ \.cgi$ {
#   #fastcgi_pass <FastCGI서버주소>:<포트>;
#   #include fastcgi_params;
# }

# IIS - ISAPI 및 CGI 제한 > 사용하지 않는 CGI/ISAPI 모듈 해제

# WebtoB - http.m 내 *SVRGROUP, *SERVER, *URI에서 CGI 설정 주석 처리
```

### WEB-06: 상위 디렉터리 접근 제한 설정
**점검:**
```bash
# Apache
grep -i "AllowOverride" <Apache_DIR>/conf/httpd.conf
# Tomcat
grep -i "allowLinking" <Tomcat_DIR>/conf/server.xml
# Nginx
grep -i "auth_basic" <Nginx_DIR>/conf/nginx.conf
```
**조치:**
```bash
# Apache - AllowOverride AuthConfig 설정 + .htaccess 인증 파일 생성
vi <Apache_DIR>/conf/httpd.conf
# <Directory "/usr/local/apache2/htdocs">
#   AllowOverride AuthConfig
# </Directory>
htpasswd <Apache_DIR>/.htpasswd [사용자명]
systemctl restart apache2

# Tomcat - allowLinking 옵션 제거
vi <Tomcat_DIR>/conf/server.xml
# <Context>  (allowLinking="true" 제거)

# Nginx - 기본 인증으로 디렉터리 접근 제한
# location /<접근제한 디렉터리>/ {
#   auth_basic "Restricted Content";
#   auth_basic_user_file /etc/nginx/.htpasswd;
# }

# IIS 7.0+ - web.config 내 enableParentPaths="false" 설정
# <httpRuntime enableParentPaths="false" />

# WebtoB - UpperDirRestrict = N 설정
```

### WEB-07: 웹 서비스 경로 내 불필요한 파일 제거
**점검/조치:**
```bash
# Apache
rm -rf <Apache_DIR>/htdocs/manual
rm -rf <Apache_DIR>/manual

# Tomcat
rm -rf <Tomcat_DIR>/webapps/docs/<불필요 파일>
# BUILDING.txt, RELEASE-NOTES.txt 등 매뉴얼 파일 포함

# Nginx
rm -rf <Nginx_DIR>/html/index.html

# IIS - 샘플 디렉터리 제거
# c:\inetpub\iissamples
# c:\winnt\help\iishelp
# c:\program files\common files\system\msadc\sample

# JEUS
rm -rf <JEUS_DIR>/docs/manuals/default/web-manager/<불필요 파일>
rm -rf <JEUS_HOME>/samples/<불필요 파일>

# WebtoB
rm -rf <WebtoB_DIR>/docs/manuals/<불필요 파일>
rm -rf <WebtoB_HOME>/samples/<불필요 파일>
```

### WEB-08: 파일 업로드 및 다운로드 용량 제한
**점검:**
```bash
# Apache
grep -i "LimitRequestBody" <Apache_DIR>/conf/httpd.conf
# Tomcat
grep -i "maxPostSize" <Tomcat_DIR>/conf/server.xml
# Nginx
grep -i "client_max_body_size" <Nginx_DIR>/conf/nginx.conf
```
**조치:**
```bash
# Apache - LimitRequestBody 지시자 설정 (5MB = 5000000)
# <Directory />
#   LimitRequestBody 5000000
# </Directory>

# Tomcat - server.xml 내 maxPostSize 설정 + web.xml 내 multipart-config 설정
# <Connector port="8080" ... maxPostSize="5242880" />
# <multipart-config>
#   <max-file-size>2097152</max-file-size>
#   <max-request-size>4194304</max-request-size>
# </multipart-config>

# Nginx - client_max_body_size 설정
# client_max_body_size 5M;
systemctl restart nginx

# IIS - web.config 내 maxAllowedContentLength 설정 (기본값 30MB)
# applicationHost.config 내 bufferingLimit(4MB) 및 maxRequestEntityAllowed(0.2MB) 설정

# JEUS - web.xml 내 max-file-size 설정
# <multipart-config><max-file-size>5242880</max-file-size></multipart-config>

# WebtoB - LimitRequestBody 설정
# LimitRequestBody = 2048000
```

### WEB-09: 웹 서비스 프로세스 권한 제한
**점검:**
```bash
# 프로세스 실행 계정 확인
ps -ef | grep httpd | grep -v root
ps -ef | grep nginx
ps -ef | grep tomcat
ps -ef | grep jeus
```
**조치:**
```bash
# Apache - www-data 계정으로 실행
vi <Apache_DIR>/envvars
# export APACHE_RUN_USER=www-data
# export APACHE_RUN_GROUP=www-data
chown -R www-data:www-data /etc/apache2/ /var/www/ /var/log/apache2/
usermod -s /sbin/nologin www-data
systemctl restart apache2

# Tomcat - tomcat 전용 계정으로 실행
vi /etc/systemd/system/tomcat.service
# [Service]
# User=tomcat
# Group=tomcat
chown -R tomcat:tomcat <Tomcat_DIR>/
usermod -s /sbin/nologin tomcat
systemctl restart tomcat

# Nginx - nginx 전용 계정으로 실행
vi <Nginx_DIR>/conf/nginx.conf
# user nginx nginx;
adduser --system --no-create-home --shell /bin/false nginx
groupadd nginx && usermod -aG nginx nginx
systemctl restart nginx

# IIS - 응용프로그램 풀 ID를 ApplicationPoolIdentity로 설정

# JEUS - jeus 전용 계정 생성 후 소유권 변경
useradd -m jeus
chown -R jeus:jeus <JEUS_DIR>/
```

### WEB-10: 불필요한 프록시 설정 제한
**점검:**
```bash
# Apache
grep -i "ProxyPass\|ProxyRequests" <Apache_DIR>/conf/httpd.conf
# Tomcat
grep -i "proxyName\|proxyPort" <Tomcat_DIR>/conf/server.xml
# Nginx
grep -i "proxy_pass" <Nginx_DIR>/conf/nginx.conf
```
**조치:**
```bash
# Apache - 불필요한 Proxy 설정 제거, ProxyRequests Off 유지
# <VirtualHost *:80>
#   ProxyRequests Off
# </VirtualHost>

# Tomcat - Connector 요소에서 불필요한 proxyName, proxyPort 제거
# Nginx - 불필요한 proxy_pass 설정 제거
# IIS - 루트 디렉터리에서 불필요한 Proxy 설정 제거
# JEUS - web.xml 내 불필요한 ReverseProxy 설정 제거
# WebtoB - http.m 내 REVERSE_PROXY 설정 제거
```

### WEB-11: 웹 서비스 경로 설정
**조치:**
```bash
# Apache - DocumentRoot를 별도 경로로 변경
# DocumentRoot [별도의 경로]

# Tomcat - docBase를 별도 경로로 변경
# <Context path="" docBase="[별도의 경로]" />

# Nginx - root를 별도 경로로 변경
# root [별도의 경로];

# IIS - 사이트 편집 > 실제 경로를 별도 경로로 변경
# JEUS - Docroot = "[별도의 경로]"
# WebtoB - DOCROOT="[별도의 경로]"
```

### WEB-12: 웹 서비스 링크 사용 금지
**조치:**
```bash
# Apache - FollowSymLinks 옵션 제거
vi <Apache_DIR>/conf/httpd.conf
# <Directory />
#   Options -FollowSymLinks
# </Directory>

# Tomcat - allowLinking 옵션 제거 (기본값: false)
# Nginx - disable_symlinks on 설정
# location / { disable_symlinks on; }

# IIS - 홈 디렉터리 내 바로가기 파일 제거
# JEUS - jeus-web-dd.xml 내 alias 요소 제거
# WebtoB - http.m 내 ALIAS 절 불필요 설정 제거
```

### WEB-13: 웹 서비스 설정 파일 노출 제한
**조치:**
```bash
# Tomcat - 불필요한 DB 연결 리소스 설정 제거 후 접근 권한 설정
chmod 600 <Tomcat_DIR>/conf/server.xml

# IIS - 처리기 매핑에서 *.asa/*.asax 항목 제거
# 요청 필터링에서 "파일 이름 확장명 거부"에 등록

# JEUS - domain.xml 내 불필요한 DB 연결 리소스 제거
chmod 600 <JEUS_DIR>/conf/domain.xml
```

### WEB-14: 웹 서비스 경로 내 파일의 접근 통제
**조치:**
```bash
# Apache
chown -R www-data:www-data <Apache_DIR>/conf/apache2.conf
chmod -R 750 <Apache_DIR>/conf/apache2.conf

# Tomcat
chown -R tomcat:tomcat <Tomcat_DIR>/conf/web.xml
chmod -R 750 <Tomcat_DIR>/conf/web.xml

# Nginx
chown -R nginx:nginx <Nginx_DIR>/conf/nginx.conf
chmod -R 750 <Nginx_DIR>/conf/nginx.conf

# IIS - web.config > 속성 > 보안 > 불필요 권한 제거

# JEUS
chown -R jeus:jeus <JEUS_DIR>/config/security/SYSTEM_DOMAIN/accounts.xml
chmod -R 750 <JEUS_DIR>/config/security/SYSTEM_DOMAIN/accounts.xml

# WebtoB
chown -R webtob:webtob <WebtoB_DIR>/config/http.m
chmod -R 750 <WebtoB_DIR>/config/http.m
```

### WEB-15: 불필요한 스크립트 매핑 제거
**점검:**
```bash
# Tomcat - 불필요한 servlet-mapping 확인
grep -A2 "servlet-mapping" <Tomcat_DIR>/conf/web.xml
# IIS - 처리기 매핑에서 취약한 확장자 확인
# (.htr, .idc, .stm, .shtm, .shtml, .printer, .htw, .ida, .idq)
```
**조치:**
```bash
# Tomcat - 불필요한 servlet-mapping 제거
# IIS - 처리기 매핑에서 미사용 확장자 매핑 제거
# JEUS - web.xml 내 불필요한 <servlet-mapping> 제거
```

### WEB-16: 웹 서비스 헤더 정보 노출 제한
**점검:**
```bash
# Apache
grep -i "ServerTokens\|ServerSignature" <Apache_DIR>/conf/httpd.conf
# Nginx
grep -i "server_tokens" <Nginx_DIR>/conf/nginx.conf
# WebtoB
grep -i "ServerTokens" <WebtoB_DIR>/config/http.m
```
**조치:**
```bash
# Apache - ServerTokens Prod, ServerSignature Off 설정
vi <Apache_DIR>/conf/httpd.conf
# ServerTokens Prod
# ServerSignature Off

# Tomcat - server.xml 내 server 값을 임의 정보로 변경
# <Connector port="8080" ... server="{임의 정보}" />
# + ErrorReportValve에 showServerInfo="false" 추가
# <Valve className="org.apache.catalina.valves.ErrorReportValve"
#   showReport="true" showServerInfo="false"/>

# Nginx
# server_tokens off;

# IIS - 오류 페이지 > 기능 설정 편집 > "사용자 지정 오류 페이지" 설정

# JEUS 7 이전 - JEUSMain.xml 내 command-option 추가
# -Djeus.servlet.response.header.serverInfo=false
# JEUS 7 - domain.xml 내 response-header 설정

# WebtoB
# ServerTokens ProductOnly
# ServerSignature off
```

### WEB-17: 웹 서비스 가상 디렉터리 삭제
**점검/조치:**
```bash
# Apache - 불필요한 Alias 지시자 확인 후 제거
grep -i "Alias" <Apache_DIR>/conf/httpd.conf

# Tomcat - Context path 속성값 확인 후 불필요 제거
grep -i "Context path" <Tomcat_DIR>/conf/server.xml

# Nginx - 불필요한 alias 지시자 제거
grep -i "alias" <Nginx_DIR>/conf/nginx.conf

# WebtoB - NODE절의 불필요한 Alias 설정 삭제
grep -i "ALIAS" <WebtoB_DIR>/config/http.m
```

### WEB-18: WebDAV 비활성화
**점검:**
```bash
# Apache
grep -i "Dav On" <Apache_DIR>/conf/httpd.conf
grep -i "LoadModule.*dav" <Apache_DIR>/conf/httpd.conf
# Nginx
grep -i "dav_methods" <Nginx_DIR>/conf/nginx.conf
```
**조치:**
```bash
# Apache - WebDAV 비활성화
vi <Apache_DIR>/conf/httpd.conf
# <Directory "/path/to/directory">
#   Dav Off
# </Directory>
systemctl restart apache2

# Nginx - dav_methods 설정 주석 처리 또는 제거
systemctl restart nginx

# IIS - ISAPI 및 CGI 제한 > WebDAV 항목 > 확장 경로 실행 허용 체크 해제

# WebtoB - VHOST 절에서 PUT, DELETE, MKCOL, COPY, MOVE 메소드 제거
```

---

## 3. 보안 설정

### WEB-19: SSI(Server Side Includes) 사용 제한
**점검:**
```bash
# Apache
grep -i "Includes" <Apache_DIR>/conf/httpd.conf
# Tomcat
grep -i "SSIServlet\|SSIFilter" <Tomcat_DIR>/conf/web.xml
# Nginx
grep -i "ssi on" <Nginx_DIR>/conf/nginx.conf
# WebtoB
grep -i "SSI" <WebtoB_DIR>/config/http.m
```
**조치:**
```bash
# Apache - Options Includes 제거
# <Directory /> Options </Directory>   (Includes 삭제)

# Tomcat - SSI 서블릿/필터 설정 주석 처리 또는 삭제
# Nginx - ssi off; 설정
# IIS - 처리기 매핑에서 .shtml, .shtm, .stm 확장자 매핑 제거
# WebtoB - *SVRGROUP, *SERVER에서 SSI 관련 설정 삭제
```

### WEB-20: SSL/TLS 활성화
**점검:**
```bash
# Apache
apache2ctl -M | grep ssl
# Nginx
grep -i "ssl_protocols" <Nginx_DIR>/conf/nginx.conf
# WebtoB
grep -i "SSLFLAG\|SSLNAME" <WebtoB_DIR>/config/http.m
```
**조치:**
```bash
# Apache - SSL 모듈 활성화 및 인증서 설정
vi <Apache_DIR>/sites-available/default-ssl.conf
# <VirtualHost *:443>
#   SSLEngine on
#   SSLCertificateFile /path/to/cert.crt
#   SSLCertificateKeyFile /path/to/privkey.key
# </VirtualHost>
a2ensite default-ssl
systemctl restart apache2

# Nginx - SSL 인증서 설정
# server {
#   listen 443 ssl;
#   ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
#   ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
#   ssl_protocols TLSv1.2 TLSv1.3;
#   ssl_prefer_server_ciphers on;
# }
systemctl restart nginx

# IIS - SSL 인증서 바인딩 설정 (IIS 관리자 > 사이트 바인딩 > https 추가)

# WebtoB - http.m 내 SSLFLAG = Y, SSLNAME 설정
# *SSL 절에 인증서 경로 설정
# Protocols = "-SSLv2, -SSLv3, -TLSv1, -TLSv1.1, TLSv1.2, TLSv1.3"
```

### WEB-21: HTTP 리디렉션
**조치:**
```bash
# Apache - HTTP → HTTPS 리디렉션 설정
# <VirtualHost *:80>
#   RewriteEngine On
#   RewriteCond %{HTTPS} off
#   RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
# </VirtualHost>

# Nginx
# server {
#   listen 80;
#   return 301 https://$host$request_uri;
# }

# IIS - 사이트 바인딩 종류를 HTTPS로 설정

# WebtoB - URLRewrite = Y 설정
# RewriteCond %{HTTPS} off
# RewriteRule .* https://%{SERVER_NAME}%{REQUEST_URI} [R=307,L]
```

### WEB-22: 에러 페이지 관리
**조치:**
```bash
# Apache - 에러 코드별 일원화된 에러 페이지 설정
vi <Apache_DIR>/sites-available/000-default.conf
# ErrorDocument 400 /error.html
# ErrorDocument 401 /error.html
# ErrorDocument 403 /error.html
# ErrorDocument 404 /error.html
# ErrorDocument 500 /error.html
systemctl restart apache2

# Tomcat - web.xml 내 에러 페이지 설정
# <error-page>
#   <error-code>404</error-code>
#   <location>/error/404.html</location>
# </error-page>

# Nginx
# error_page 404 /404.html;
# error_page 500 502 503 504 /50x.html;
# location = /404.html { root html; internal; }

# IIS - 오류 페이지 > 기능 설정 편집 > "사용자 지정 오류 페이지" 설정

# JEUS - web.xml 내 에러 메시지 설정
# WebtoB - *ERRORDOCUMENT 절에 에러 페이지 설정
# 503  status = 503, url = "/503.html"
```

### WEB-23: LDAP 알고리즘 적절하게 구성
**점검:**
```bash
# Tomcat - 비밀번호 다이제스트 알고리즘 확인
grep 'digest=' <Tomcat_DIR>/conf/server.xml
```
**조치:**
```bash
# Tomcat - SHA-256 이상 알고리즘 설정
vi <Tomcat_DIR>/conf/server.xml
# digest="SHA-256"
systemctl restart tomcat
```

---

## 4. 패치 및 로그 관리

### WEB-24: 별도의 업로드 경로 사용 및 권한 설정
**조치:**
```bash
# Apache - 별도 업로드 경로 생성 및 권한 설정
mkdir /var/www/html/uploads
chmod 750 /var/www/html/uploads/
chown www-data:www-data /var/www/html/uploads/
# apache2.conf 내 업로드 디렉터리 접근 제한
# <Directory "/var/www/html/uploads/">
#   Require all denied
# </Directory>

# Tomcat - 별도 업로드 경로 생성 및 권한 설정
mkdir /var/www/html/uploads
chmod 750 /var/www/html/uploads/
chown tomcat:tomcat /var/www/html/uploads/

# Nginx - 별도 업로드 경로 생성 및 권한 설정
mkdir /var/www/html/uploads
chmod 750 /var/www/html/uploads/
chown www-data:www-data /var/www/html/uploads/

# IIS - 웹 서비스 외부에 업로드 디렉터리 생성, IIS 구동 계정에 쓰기 권한 부여

# JEUS - 업로드 디렉터리 권한 설정
chmod 750 <JEUS_UPLOAD_DIR>
chown jeus:jeus <JEUS_UPLOAD_DIR>

# WebtoB - 업로드 디렉터리 권한 설정
chmod 750 <WebtoB_UPLOAD_DIR>
chown tmax:tmax <WebtoB_UPLOAD_DIR>
```

### WEB-25: 주기적 보안 패치 및 벤더 권고사항 적용
**점검:**
```bash
# Apache
<Apache_DIR>/bin/httpd -v

# Tomcat
cd <Tomcat_DIR>/lib && java -cp catalina.jar org.apache.catalina.util.ServerInfo

# Nginx
<Nginx_DIR>/sbin/nginx -v

# IIS
reg query "HKLM\SOFTWARE\Microsoft\InetStp" /v VersionString

# JEUS
jeusadmin -version

# WebtoB
wscfl -version
```
**참고 사이트:**
- Apache: http://httpd.apache.org/download.cgi
- Tomcat: https://tomcat.apache.org/
- Nginx: https://nginx.org/en/download.html
- IIS: https://www.iis.net/downloads/microsoft
- JEUS/WebtoB: https://technet.tmaxsoft.com/

### WEB-26: 로그 디렉터리 및 파일 권한 설정
**점검:**
```bash
# Apache
ls -al <Apache_LOG_DIR>/
# Tomcat
ls -al <Tomcat_DIR>/logs/
# Nginx
ls -al /var/log/nginx/
# JEUS
ls -al <JEUS_DIR>/domains/jeus_domain/servers/sample/logs/
# WebtoB
ls -al <WebtoB_DIR>/log/
```
**조치:**
```bash
# Apache
chmod o-rwx <Apache_LOG_DIR>/*

# Tomcat
chmod o-rwx <Tomcat_DIR>/logs/*

# Nginx
chmod o-rwx /var/log/nginx/*

# IIS - C:\Windows\System32\config 속성 > 보안 > Everyone 권한 제거
# C:\Windows\System32\LogFiles에서도 동일 조치

# JEUS - 로그 디렉터리 750, 로그 파일 640
chmod 750 <JEUS_DIR>/domains/jeus_domain/servers/sample/logs
chmod 640 <JEUS_DIR>/domains/jeus_domain/servers/sample/logs/*

# WebtoB - 로그 디렉터리 750, 로그 파일 640
chmod 750 <WebtoB_DIR>/log/
chmod 640 <WebtoB_DIR>/log/*
```
