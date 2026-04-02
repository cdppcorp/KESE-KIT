# Secure Coding Guide — Python

KISA Python 시큐어코딩 가이드(ref-012, 176p, 46개 항목) 기반, Python 프레임워크별 구현 예시입니다.
모든 항목은 UNSAFE(취약) / SAFE(안전) 쌍으로 구성됩니다.

---

## 1. Input Data Validation (입력데이터 검증 및 표현)

### 1-1. SQL Injection (CWE-89)

외부 입력값을 쿼리 문자열에 직접 삽입하면 공격자가 임의 SQL을 실행할 수 있습니다.

**Django DB API**

```python
# UNSAFE — 입력값을 쿼리에 직접 결합
from django.shortcuts import render
from django.db import connection

def update_board(request):
    name = request.POST.get('name', '')
    content_id = request.POST.get('content_id', '')
    with connection.cursor() as curs:
        sql_query = "UPDATE board SET name='" + name + "' WHERE content_id='" + content_id + "'"
        curs.execute(sql_query)
    connection.commit()
    return render(request, '/success.html')
```

```python
# SAFE — 파라미터 바인딩 (인자화된 쿼리)
from django.shortcuts import render
from django.db import connection

def update_board(request):
    name = request.POST.get('name', '')
    content_id = request.POST.get('content_id', '')
    with connection.cursor() as curs:
        sql_query = 'UPDATE board SET name=%s WHERE content_id=%s'
        curs.execute(sql_query, (name, content_id))
    connection.commit()
    return render(request, '/success.html')
```

**Django ORM raw()**

```python
# UNSAFE — raw() 함수에 문자열 결합 쿼리 사용
from app.models import Member

def member_search(request):
    name = request.POST.get('name', '')
    query = "SELECT * FROM member WHERE name='" + name + "'"
    data = Member.objects.raw(query)
    return render(request, '/member_list.html', {'member_list': data})
```

```python
# SAFE — raw() 함수에 바인딩 변수 사용
from app.models import Member

def member_search(request):
    name = request.POST.get('name', '')
    query = 'SELECT * FROM member WHERE name=%s'
    data = Member.objects.raw(query, [name])
    return render(request, '/member_list.html', {'member_list': data})
```

> **TIP** Django querySets, SQLAlchemy ORM은 기본적으로 인자화된 쿼리를 사용합니다. raw query를 쓸 경우 반드시 바인딩 변수를 사용하세요. SQLite에서는 `?` 또는 `:name` Placeholder를 사용합니다.

---

### 1-2. Code Injection (CWE-94, CWE-95)

동적 코드 실행 함수(eval, exec)에 외부 입력값을 전달하면 임의 코드가 실행됩니다.

**eval() 사용**

```python
# UNSAFE — 외부 입력값을 eval()에 직접 전달
from django.shortcuts import render

def route(request):
    message = request.POST.get('message', '')
    ret = eval(message)
    return render(request, '/success.html', {'data': ret})
```

```python
# SAFE — 입력값을 영문/숫자로 제한하여 검증
from django.shortcuts import render

def route(request):
    message = request.POST.get('message', '')
    if message.isalnum():
        ret = eval(message)
        return render(request, '/success.html', {'data': ret})
    return render(request, '/error.html')
```

**exec() 사용**

```python
# UNSAFE — exec()에 외부 입력값을 직접 전달
from django.shortcuts import render

def request_rest_api(request):
    function_name = request.POST.get('function_name', '')
    exec('{}()'.format(function_name))
    return render(request, '/success.html')
```

```python
# SAFE — 화이트리스트로 허용 함수 제한
from django.shortcuts import render

WHITE_LIST = ['get_friends_list', 'get_address', 'get_phone_number']

def request_rest_api(request):
    function_name = request.POST.get('function_name', '')
    if function_name in WHITE_LIST:
        exec('{}()'.format(function_name))
        return render(request, '/success.html')
    return render(request, '/error.html', {'error': '허용되지 않은 함수입니다.'})
```

> **WARNING** eval(), exec() 등 동적 코드 실행 함수는 외부 입력값과 함께 사용하지 마세요. 정규식(re 모듈)이나 str.isalnum() 등으로 입력값을 검증하세요.

---

### 1-3. Path Traversal / Resource Injection (CWE-22, CWE-99)

파일 경로에 외부 입력값을 직접 사용하면 상위 디렉터리 접근이 가능합니다.

**경로 조작**

```python
# UNSAFE — 입력값을 경로에 직접 사용
import os
from django.shortcuts import render

def get_info(request):
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()
    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})
    with open(request_file) as f:
        data = f.read()
    return render(request, '/success.html', {'data': data})
```

```python
# SAFE — 경로 조작 문자열 필터링
import os
from django.shortcuts import render

def get_info(request):
    request_file = request.POST.get('request_file')
    (filename, file_ext) = os.path.splitext(request_file)
    file_ext = file_ext.lower()
    if file_ext not in ['.txt', '.csv']:
        return render(request, '/error.html', {'error': '파일을 열 수 없습니다.'})
    filename = filename.replace('.', '')
    filename = filename.replace('/', '')
    filename = filename.replace('\\', '')
    try:
        with open(filename + file_ext) as f:
            data = f.read()
    except Exception:
        return render(request, '/error.html', {'error': '파일이 존재하지 않거나 열 수 없습니다.'})
    return render(request, '/success.html', {'data': data})
```

**자원 삽입 (소켓 포트)**

```python
# UNSAFE — 외부 입력값을 포트 번호로 직접 사용
import socket
from django.shortcuts import render

def get_info(request):
    port = int(request.POST.get('port'))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', port))
        return render(request, '/success.html')
```

```python
# SAFE — 포트 번호를 화이트리스트로 제한
import socket
from django.shortcuts import render

ALLOW_PORT = [4000, 6000, 9000]

def get_info(request):
    port = int(request.POST.get('port'))
    if port not in ALLOW_PORT:
        return render(request, '/error.html', {'error': '소켓연결 실패'})
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', port))
        return render(request, '/success.html')
```

---

### 1-4. Cross-Site Scripting — XSS (CWE-79)

외부 입력값이 HTML 응답에 그대로 포함되면 악성 스크립트가 실행됩니다.

**Django — mark_safe 오용**

```python
# UNSAFE — mark_safe로 XSS 보호 정책 무력화
from django.shortcuts import render
from django.utils.safestring import mark_safe

def profile_link(request):
    profile_url = request.POST.get('profile_url')
    profile_name = request.POST.get('profile_name')
    object_link = '<a href="{}">{}</a>'.format(profile_url, profile_name)
    object_link = mark_safe(object_link)
    return render(request, 'my_profile.html', {'object_link': object_link})
```

```python
# SAFE — mark_safe 사용하지 않음 (Django 템플릿 자동 이스케이프 활용)
from django.shortcuts import render

def profile_link(request):
    profile_url = request.POST.get('profile_url')
    profile_name = request.POST.get('profile_name')
    object_link = '<a href="{}">{}</a>'.format(profile_url, profile_name)
    return render(request, 'my_profile.html', {'object_link': object_link})
```

**Flask — html.escape 적용**

```python
# UNSAFE — 입력값을 검증/치환 없이 동적 웹페이지에 사용
from flask import Flask, request, render_template

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form.get('search_keyword')
    return render_template('search.html', search_keyword=search_keyword)
```

```python
# SAFE — html.escape로 HTML 엔티티 치환
import html
from flask import Flask, request, render_template

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form.get('search_keyword')
    escape_keyword = html.escape(search_keyword)
    return render_template('search.html', search_keyword=escape_keyword)
```

> **TIP** Django 템플릿에서 `{% autoescape off %}` 또는 `{{ content | safe }}` 사용을 피하세요. Jinja2 템플릿도 자동 이스케이프를 활성화하세요.

---

### 1-5. OS Command Injection (CWE-78)

시스템 명령어에 외부 입력값을 직접 전달하면 임의 명령 실행이 가능합니다.

```python
# UNSAFE — os.system에 외부 입력값 직접 전달
import os
from django.shortcuts import render

def execute_command(request):
    app_name_string = request.POST.get('app_name', '')
    os.system(app_name_string)
    return render(request, '/success.html')
```

```python
# SAFE — 화이트리스트로 실행 가능 프로그램 제한
import os
from django.shortcuts import render

ALLOW_PROGRAM = ['notepad', 'calc']

def execute_command(request):
    app_name_string = request.POST.get('app_name', '')
    if app_name_string not in ALLOW_PROGRAM:
        return render(request, '/error.html', {'error': '허용되지 않은 프로그램입니다.'})
    os.system(app_name_string)
    return render(request, '/success.html')
```

**subprocess 사용 시**

```python
# UNSAFE — shell=True로 외부 입력값 포함 명령 실행
import subprocess
from django.shortcuts import render

def execute_command(request):
    date = request.POST.get('date', '')
    cmd_str = "cmd /c backuplog.bat " + date
    subprocess.run(cmd_str, shell=True)
    return render(request, '/success.html')
```

```python
# SAFE — 특수문자 필터링 + shell=False(기본값) + 인자 배열 전달
import subprocess
from django.shortcuts import render

def execute_command(request):
    date = request.POST.get('date', '')
    for word in ['|', ';', '&', ':', '>', '<', '`', '\\', '!']:
        date = date.replace(word, "")
    subprocess.run(["cmd", "/c", "backuplog.bat", date])
    return render(request, '/success.html')
```

---

### 1-6. Unrestricted File Upload (CWE-434)

파일 업로드 시 확장자/크기/내용을 검증하지 않으면 웹셸 등 악성 파일이 업로드됩니다.

```python
# UNSAFE — 파일 검증 없이 저장
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def file_upload(request):
    if request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage(location='media/screenshot', base_url='media/screenshot')
        filename = fs.save(upload_file.name, upload_file)
        return render(request, '/success.html', {'filename': filename})
    return render(request, '/error.html', {'error': '파일 업로드 실패'})
```

```python
# SAFE — 파일 개수, 크기, 확장자, Content-Type 검증
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

FILE_COUNT_LIMIT = 5
FILE_SIZE_LIMIT = 5242880  # 5MB
WHITE_LIST_EXT = ['.jpg', '.jpeg']

def file_upload(request):
    if len(request.FILES) == 0 or len(request.FILES) > FILE_COUNT_LIMIT:
        return render(request, '/error.html', {'error': '파일 개수 초과'})
    for filename, upload_file in request.FILES.items():
        if upload_file.content_type != 'image/jpeg':
            return render(request, '/error.html', {'error': '파일 타입 오류'})
        if upload_file.size > FILE_SIZE_LIMIT:
            return render(request, '/error.html', {'error': '파일사이즈 오류'})
        file_name, file_ext = os.path.splitext(upload_file.name)
        if file_ext.lower() not in WHITE_LIST_EXT:
            return render(request, '/error.html', {'error': '파일 타입 오류'})
    fs = FileSystemStorage(location='media/screenshot', base_url='media/screenshot')
    filename_list = []
    for upload_file in request.FILES.values():
        saved = fs.save(upload_file.name, upload_file)
        filename_list.append(saved)
    return render(request, '/success.html', {'filename_list': filename_list})
```

---

### 1-7. Open Redirect (CWE-601)

리다이렉트 URL을 외부 입력으로 받으면 피싱 사이트로 유도될 수 있습니다.

```python
# UNSAFE — 입력 URL로 직접 리다이렉트
from django.shortcuts import redirect

def redirect_url(request):
    url_string = request.POST.get('url', '')
    return redirect(url_string)
```

```python
# SAFE — 화이트리스트로 허용 URL 제한
from django.shortcuts import render, redirect

ALLOW_URL_LIST = [
    '127.0.0.1',
    'https://login.myservice.com',
    '/notice',
]

def redirect_url(request):
    url_string = request.POST.get('url', '')
    if url_string not in ALLOW_URL_LIST:
        return render(request, '/error.html', {'error': '허용되지 않는 주소입니다.'})
    return redirect(url_string)
```

---

### 1-8. XML External Entity — XXE (CWE-611)

XML 파서가 외부 엔티티를 처리하면 서버 파일 읽기, SSRF가 가능합니다.

```python
# UNSAFE — 외부 엔티티 처리 허용
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT

def get_xml(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, True)  # 취약
    doc = parseString(request.body.decode('utf-8'), parser=parser)
    for event, node in doc:
        if event == START_ELEMENT and node.tagName == "foo":
            doc.expandNode(node)
            text = node.toxml()
```

```python
# SAFE — 외부 엔티티 비활성화
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges
from xml.dom.pulldom import parseString, START_ELEMENT

def get_xml(request):
    parser = make_parser()
    parser.setFeature(feature_external_ges, False)  # 안전
    doc = parseString(request.body.decode('utf-8'), parser=parser)
    for event, node in doc:
        if event == START_ELEMENT and node.tagName == "foo":
            doc.expandNode(node)
            text = node.toxml()
```

> **TIP** lxml 라이브러리 사용 시 `XMLParser(resolve_entities=False)` 및 `no_network=True`로 설정하세요.

---

### 1-9. XPath / XML Injection (CWE-643)

XPath 쿼리에 외부 입력값을 직접 삽입하면 인증 우회 등이 가능합니다.

```python
# UNSAFE — 외부 입력값을 XPath 쿼리에 직접 결합
from lxml import etree

def parse_xml(request):
    user_name = request.POST.get('user_name', '')
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()
    query = "/collection/users/user[@name='" + user_name + "']/home/text()"
    elmts = root.xpath(query)
```

```python
# SAFE — lxml의 XPath 파라미터 바인딩 사용
from lxml import etree

def parse_xml(request):
    user_name = request.POST.get('user_name', '')
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse('user.xml', parser)
    root = tree.getroot()
    query = '/collection/users/user[@name = $paramname]/home/text()'
    elmts = root.xpath(query, paramname=user_name)
```

---

### 1-10. LDAP Injection (CWE-90)

LDAP 필터에 외부 입력값을 직접 삽입하면 디렉터리 데이터 유출이 가능합니다.

```python
# UNSAFE — 입력값을 필터링 없이 LDAP 검색에 사용
from ldap3 import Connection, Server, ALL

def ldap_query(request):
    search_keyword = request.POST.get('search_keyword', '')
    server = Server('ldap.example.com', get_info=ALL)
    conn = Connection(server, user=dn, password=password, auto_bind=True)
    search_str = '(&(objectclass=%s))' % search_keyword
    conn.search('dc=company,dc=com', search_str,
                attributes=['sn', 'cn', 'address', 'mail', 'mobile', 'uid'])
```

```python
# SAFE — escape_filter_chars로 특수문자 이스케이프
from ldap3 import Connection, Server, ALL
from ldap3.utils.conv import escape_filter_chars

def ldap_query(request):
    search_keyword = request.POST.get('search_keyword', '')
    server = Server('ldap.example.com', get_info=ALL)
    conn = Connection(server, user=dn, password=password, auto_bind=True)
    escape_keyword = escape_filter_chars(search_keyword)
    search_str = '(&(objectclass=%s))' % escape_keyword
    conn.search('dc=company,dc=com', search_str,
                attributes=['sn', 'cn', 'address', 'mail', 'mobile', 'uid'])
```

---

### 1-11. Cross-Site Request Forgery — CSRF (CWE-352)

상태 변경 요청에 CSRF 토큰이 없으면 사용자 의지와 무관한 요청이 실행됩니다.

**Django — 미들웨어 설정**

```python
# UNSAFE — CSRF 미들웨어 비활성화
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # 주석 처리 = 취약
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
```

```python
# SAFE — CSRF 미들웨어 활성화
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # 활성화
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
```

**Django — 뷰에서 csrf_exempt 사용 금지**

```python
# UNSAFE — csrf_exempt 데코레이터로 CSRF 보호 해제
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pay_to_point(request):
    user_id = request.POST.get('user_id', '')
    pay = request.POST.get('pay', '')
    ret = handle_pay(user_id, pay)
    return render(request, '/view_wallet.html', {'wallet': ret})
```

```python
# SAFE — csrf_exempt 제거, 템플릿에 {% csrf_token %} 사용
def pay_to_point(request):
    user_id = request.POST.get('user_id', '')
    pay = request.POST.get('pay', '')
    ret = handle_pay(user_id, pay)
    return render(request, '/view_wallet.html', {'wallet': ret})
```

**Flask — CSRFProtect 사용**

```python
# UNSAFE — CSRF 보호 미설정
from flask import Flask
app = Flask(__name__)
```

```python
# SAFE — Flask-WTF CSRFProtect 적용
import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
csrf = CSRFProtect(app)
```

> **TIP** Django 템플릿에서는 `{% csrf_token %}`, Flask 템플릿에서는 `{{ csrf_token() }}`을 form 태그 안에 반드시 명시하세요.

---

### 1-12. Server-Side Request Forgery — SSRF (CWE-918)

서버가 외부 입력 URL로 요청을 보내면 내부 네트워크 접근이 가능합니다.

```python
# UNSAFE — 사용자 입력 URL로 직접 HTTP 요청
from django.shortcuts import render
import requests

def call_third_party_api(request):
    addr = request.POST.get('address', '')
    result = requests.get(addr).text
    return render(request, '/result.html', {'result': result})
```

```python
# SAFE — 화이트리스트 IP 기반 검증
from django.shortcuts import render
import requests

ALLOW_SERVER_LIST = [
    'https://127.0.0.1/latest/',
    'https://192.168.0.1/user_data',
    'https://192.168.0.100/v1/public',
]

def call_third_party_api(request):
    addr = request.POST.get('address', '')
    if addr not in ALLOW_SERVER_LIST:
        return render(request, '/error.html', {'error': '허용되지 않은 서버입니다.'})
    result = requests.get(addr).text
    return render(request, '/result.html', {'result': result})
```

---

### 1-13. Untrusted Input for Security Decision (CWE-807)

보안 결정에 클라이언트 조작 가능한 값(쿠키, 히든필드 등)을 사용하면 권한 우회가 가능합니다.

```python
# UNSAFE — 쿠키에서 권한 정보를 가져와 관리자 판단
from django.shortcuts import render

def init_password(request):
    role = request.COOKIES['role']
    request_id = request.POST.get('user_id', '')
    request_mail = request.POST.get('user_email', '')
    if role == 'admin':
        password_init_and_sendmail(request_id, request_mail)
        return render(request, '/success.html')
    return render(request, '/failed.html')
```

```python
# SAFE — 서버 세션에서 권한 확인
from django.shortcuts import render

def init_password(request):
    role = request.session['role']
    request_id = request.POST.get('user_id', '')
    request_mail = request.POST.get('user_email', '')
    if role == 'admin':
        password_init_and_sendmail(request_id, request_mail)
        return render(request, '/success.html')
    return render(request, '/failed.html')
```

---

### 1-14. HTTP Response Splitting (CWE-113) — Python 고유

HTTP 응답 헤더에 개행 문자가 포함되면 응답이 분리되어 캐시 오염 등이 가능합니다.

```python
# UNSAFE — 입력값을 HTTP 응답 헤더에 직접 삽입
from django.http import HttpResponse

def route(request):
    content_type = request.POST.get('content-type')
    res = HttpResponse()
    res['Content-Type'] = content_type
    return res
```

```python
# SAFE — 헤더 값에서 개행 문자 제거
from django.http import HttpResponse

def route(request):
    content_type = request.POST.get('content-type')
    content_type = content_type.replace('\r', '')
    content_type = content_type.replace('\n', '')
    res = HttpResponse()
    res['Content-Type'] = content_type
    return res
```

---

### 1-15. Integer Overflow (CWE-190) — Python 고유

Python 3.x는 기본 int에서 오버플로우가 발생하지 않지만, numpy 등 C 기반 패키지 사용 시 발생합니다.

```python
# UNSAFE — numpy int64 범위 검증 없이 사용
import numpy as np

def handle_data(number, pow):
    res = np.power(number, pow, dtype=np.int64)
    return res
```

```python
# SAFE — Python 기본 자료형으로 계산 후 범위 검증
import numpy as np

MAX_NUMBER = np.iinfo(np.int64).max
MIN_NUMBER = np.iinfo(np.int64).min

def handle_data(number, pow):
    calculated = number ** pow
    if calculated > MAX_NUMBER or calculated < MIN_NUMBER:
        return -1
    res = np.power(number, pow, dtype=np.int64)
    return res
```

---

### 1-16. Format String Injection (CWE-134) — Python 고유

포맷 스트링에 외부 입력값을 직접 사용하면 전역 변수 등 내부 정보가 유출됩니다.

```python
# UNSAFE — 외부 입력값을 포맷 문자열로 직접 사용
from django.shortcuts import render

AUTHENTICATE_KEY = 'Passw0rd'

def make_user_message(request):
    user_info = get_user_info(request.POST.get('user_id', ''))
    format_string = request.POST.get('msg_format', '')
    # 공격: format_string = "{user.__init__.__globals__[AUTHENTICATE_KEY]}"
    message = format_string.format(user=user_info)
    return render(request, '/user_page.html', {'message': message})
```

```python
# SAFE — 포맷 지정자를 개발자가 직접 정의
from django.shortcuts import render

AUTHENTICATE_KEY = 'Passw0rd'

def make_user_message(request):
    user_info = get_user_info(request.POST.get('user_id', ''))
    message = 'user name is {}'.format(user_info.name)
    return render(request, '/user_page.html', {'message': message})
```

---

## 2. Security Features (보안기능)

### 2-1. Missing Authentication (CWE-306)

중요 기능에 인증 검사가 없으면 비인가자가 접근할 수 있습니다.

```python
# UNSAFE — 현재 패스워드 확인 없이 변경 허용
from django.shortcuts import render
import hashlib

def change_password(request):
    new_pwd = request.POST.get('new_password', '')
    user = request.session['userid']
    sha = hashlib.sha256(new_pwd.encode())
    update_password_from_db(user, sha.hexdigest())
    return render(request, '/success.html')
```

```python
# SAFE — 현재 패스워드 재인증 후 변경
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import hashlib

@login_required
def change_password(request):
    new_pwd = request.POST.get('new_password', '')
    crnt_pwd = request.POST.get('current_password', '')
    user = request.session['userid']
    crnt_h = hashlib.sha256(crnt_pwd.encode())
    old_pwd = get_password_from_db(user)
    if old_pwd == crnt_h.hexdigest():
        new_h = hashlib.sha256(new_pwd.encode())
        update_password_from_db(user, new_h.hexdigest())
        return render(request, '/success.html')
    return render(request, '/failed.html', {'error': '패스워드가 일치하지 않습니다'})
```

---

### 2-2. Improper Authorization (CWE-285)

인증된 사용자라도 권한 검증 없이 타인의 리소스에 접근할 수 있습니다.

```python
# UNSAFE — 권한 확인 없이 삭제 수행
from django.shortcuts import render
from .model import Content

def delete_content(request):
    action = request.POST.get('action', '')
    content_id = request.POST.get('content_id', '')
    if action == "delete":
        Content.objects.filter(id=content_id).delete()
        return render(request, '/success.html')
    return render(request, '/error.html')
```

```python
# SAFE — @login_required + @permission_required로 권한 검증
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from .model import Content

@login_required
@permission_required('content.delete', raise_exception=True)
def delete_content(request):
    action = request.POST.get('action', '')
    content_id = request.POST.get('content_id', '')
    if action == "delete":
        Content.objects.filter(id=content_id).delete()
        return render(request, '/success.html')
    return render(request, '/error.html', {'error': '삭제 실패'})
```

---

### 2-3. Incorrect Permission Assignment (CWE-732)

파일/자원에 과도한 권한을 부여하면 비인가 접근이 가능합니다.

```python
# UNSAFE — 모든 사용자에게 읽기/쓰기/실행 권한
import os

def write_file():
    os.chmod('/root/system_config', 0o777)
    with open('/root/system_config', 'w') as f:
        f.write("your config is broken")
```

```python
# SAFE — 소유자만 읽기/쓰기/실행, 그룹/기타 접근 차단
import os

def write_file():
    os.chmod('/root/system_config', 0o700)
    with open('/root/system_config', 'w') as f:
        f.write("your config is broken")
```

---

### 2-4. Broken Crypto Algorithm (CWE-327)

취약한 암호화 알고리즘(DES, MD5, SHA1)을 사용하면 암호화된 데이터가 해독됩니다.

**암호화**

```python
# UNSAFE — 취약한 DES 알고리즘 사용
import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

def get_enc_text(plain_text, key):
    cipher_des = DES.new(key, DES.MODE_ECB)
    encrypted_data = base64.b64encode(cipher_des.encrypt(pad(plain_text, 32)))
    return encrypted_data.decode('ASCII')
```

```python
# SAFE — AES-CBC 알고리즘 사용
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def get_enc_text(plain_text, key, iv):
    cipher_aes = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = base64.b64encode(cipher_aes.encrypt(pad(plain_text, 32)))
    return encrypted_data.decode('ASCII')
```

**해시함수**

```python
# UNSAFE — 취약한 MD5 해시함수
import hashlib

def make_md5(plain_text):
    hash_text = hashlib.md5(plain_text.encode('utf-8')).hexdigest()
    return hash_text
```

```python
# SAFE — SHA-256 해시함수
import hashlib

def make_sha256(plain_text):
    hash_text = hashlib.sha256(plain_text.encode('utf-8')).hexdigest()
    return hash_text
```

---

### 2-5. Cleartext Storage / Transmission (CWE-312, CWE-319)

중요 정보를 평문으로 저장/전송하면 유출 위험이 있습니다.

**평문 저장**

```python
# UNSAFE — 패스워드를 평문으로 DB에 저장
def update_pass(dbconn, password, user_id):
    curs = dbconn.cursor()
    curs.execute('UPDATE USERS SET PASSWORD=%s WHERE USER_ID=%s', password, user_id)
    dbconn.commit()
```

```python
# SAFE — SHA-256 + 솔트로 해싱 후 저장
from Crypto.Hash import SHA256

def update_pass(dbconn, password, user_id, salt):
    hash_obj = SHA256.new()
    hash_obj.update(bytes(password + salt, 'utf-8'))
    hash_pwd = hash_obj.hexdigest()
    curs = dbconn.cursor()
    curs.execute('UPDATE USERS SET PASSWORD=%s WHERE USER_ID=%s', (hash_pwd, user_id))
    dbconn.commit()
```

**평문 전송**

```python
# UNSAFE — 패스워드를 암호화 없이 소켓으로 전송
import socket

def send_password(password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 65434))
        s.sendall(password.encode('utf-8'))
```

```python
# SAFE — AES 암호화 후 전송
import socket
import os
from Crypto.Cipher import AES

def send_password(password):
    block_key = os.environ.get('BLOCK_KEY')
    aes = AEScipher(block_key)
    enc_password = aes.encrypt(password)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 65434))
        s.sendall(enc_password.encode('utf-8'))
```

---

### 2-6. Hard-coded Credentials (CWE-259, CWE-321)

소스코드에 비밀번호/키를 직접 기재하면 유출 시 즉시 악용됩니다.

```python
# UNSAFE — 소스코드에 DB 접속 정보 하드코딩
import pymysql

def query_execute(query):
    dbconn = pymysql.connect(
        host='127.0.0.1', port='1234',
        user='root', passwd='1234',
        db='mydb', charset='utf8',
    )
    curs = dbconn.cursor()
    curs.execute(query)
    dbconn.commit()
    dbconn.close()
```

```python
# SAFE — 설정 파일에서 암호화된 접속 정보 로드
import pymysql
import json

def query_execute(query, config_path):
    with open(config_path, 'r') as config:
        dbconf = json.load(fp=config)
    blockKey = get_decrypt_key(dbconf['blockKey'])
    dbUser = decrypt(blockKey, dbconf['user'])
    dbPasswd = decrypt(blockKey, dbconf['passwd'])
    dbconn = pymysql.connect(
        host=dbconf['host'], port=dbconf['port'],
        user=dbUser, passwd=dbPasswd,
        db=dbconf['db_name'], charset='utf8',
    )
    curs = dbconn.cursor()
    curs.execute(query)
    dbconn.commit()
    dbconn.close()
```

> **WARNING** .env 파일은 반드시 .gitignore에 추가하세요.

---

### 2-7. Inadequate Key Size (CWE-326)

짧은 키를 사용하면 무차별 대입으로 해독이 가능합니다.

```python
# UNSAFE — RSA 1024비트, ECC 192비트 사용
from Crypto.PublicKey import RSA
from tinyec import registry
import secrets

def make_rsa_key_pair():
    private_key = RSA.generate(1024)  # 취약
    public_key = private_key.publickey()

def make_ecc():
    ecc_curve = registry.get_curve('secp192r1')  # 취약
    private_key = secrets.randbelow(ecc_curve.field.n)
    public_key = private_key * ecc_curve.g
```

```python
# SAFE — RSA 2048비트 이상, ECC 224비트 이상
from Crypto.PublicKey import RSA
from tinyec import registry
import secrets

def make_rsa_key_pair():
    private_key = RSA.generate(2048)  # 안전
    public_key = private_key.publickey()

def make_ecc():
    ecc_curve = registry.get_curve('secp224r1')  # 안전
    private_key = secrets.randbelow(ecc_curve.field.n)
    public_key = private_key * ecc_curve.g
```

---

### 2-8. Insufficient Randomness (CWE-330)

보안 목적에 random 모듈을 사용하면 예측 가능합니다.

```python
# UNSAFE — random 모듈로 OTP/세션키 생성
import random

def get_otp_number():
    random_str = ''
    for i in range(6):
        random_str += str(random.randrange(10))
    return random_str
```

```python
# SAFE — secrets 모듈로 암호학적 보안 난수 생성
import secrets

def get_otp_number():
    random_str = ''
    for i in range(6):
        random_str += str(secrets.randbelow(10))
    return random_str
```

**세션 토큰 생성**

```python
# UNSAFE — random.choice로 세션키 생성
import random
import string

def generate_session_key():
    RANDOM_STRING_CHARS = string.ascii_letters + string.digits
    return "".join(random.choice(RANDOM_STRING_CHARS) for i in range(32))
```

```python
# SAFE — secrets.choice로 세션키 생성
import secrets
import string

def generate_session_key():
    RANDOM_STRING_CHARS = string.ascii_letters + string.digits
    return "".join(secrets.choice(RANDOM_STRING_CHARS) for i in range(32))
```

---

### 2-9. Weak Password Requirements (CWE-521)

약한 패스워드 정책은 무차별 대입 공격에 취약합니다.

```python
# UNSAFE — 패스워드 복잡도 검증 없이 회원가입
from flask import request
from Models import User, db

@app.route('/register', methods=['POST'])
def register():
    userid = request.form.get('userid')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        return make_response("패스워드가 일치하지 않습니다", 400)
    usertable = User()
    usertable.userid = userid
    usertable.password = password
    db.session.add(usertable)
    db.session.commit()
    return make_response("회원가입 성공", 200)
```

```python
# SAFE — 패스워드 복잡도 검증 (3종 이상 문자 8자리 또는 10자리 이상)
import re
from flask import request
from Models import User, db

def check_password(password):
    patterns = [
        re.compile(r'^(?=.*[A-Z])(?=.*[a-z])[A-Za-z\d!@#$%^&*]{8,}$'),
        re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$'),
        re.compile(r'^(?=.*[a-z])(?=.*\d)[A-Za-z\d!@#$%^&*]{8,}$'),
        re.compile(r'^(?=.*[a-z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'),
        re.compile(r'^(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'),
        re.compile(r'^[A-Za-z\d!@#$%^&*]{10,}$'),
    ]
    return any(p.match(password) for p in patterns)

@app.route('/register', methods=['POST'])
def register():
    userid = request.form.get('userid')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        return make_response("패스워드가 일치하지 않습니다", 400)
    if not check_password(password):
        return make_response("패스워드 조합규칙에 맞지 않습니다", 400)
    usertable = User()
    usertable.userid = userid
    usertable.password = password
    db.session.add(usertable)
    db.session.commit()
    return make_response("회원가입 성공", 200)
```

> **TIP** Django에서는 `AUTH_PASSWORD_VALIDATORS` 설정으로 패스워드 정책을 적용할 수 있습니다.

---

### 2-10. Improper Signature Verification (CWE-347)

전자서명을 검증하지 않으면 위변조된 데이터를 신뢰하게 됩니다.

```python
# UNSAFE — 전자서명 검증 없이 데이터 실행
from Crypto.Cipher import PKCS1_v1_5

def verify_data(request):
    encrypted_code = request.POST.get("encrypted_msg", "")
    with open("/keys/secret_key.out", "rb") as f:
        secret_key = f.read()
    origin_python_code = decrypt_with_symmetric_key(secret_key, encrypted_code)
    eval(origin_python_code)  # 서명 검증 없이 실행
```

```python
# SAFE — RSA 전자서명 검증 후 실행
import base64
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as SIGNATURE_PKCS1_v1_5

def verify_digit_signature(origin_data, origin_signature, client_pub_key):
    hashed_data = SHA256.new(origin_data)
    signer = SIGNATURE_PKCS1_v1_5.new(RSA.importKey(client_pub_key))
    return signer.verify(hashed_data, base64.b64decode(origin_signature))

def verify_data(request):
    encrypted_code = request.POST.get("encrypted_msg", "")
    encrypted_sig = request.POST.get("encrypted_sig", "")
    with open("/keys/secret_key.out", "rb") as f:
        secret_key = f.read()
    with open("/keys/public_key.out", "rb") as f:
        public_key = f.read()
    origin_python_code = decrypt_with_symmetric_key(secret_key, encrypted_code)
    origin_signature = decrypt_with_symmetric_key(secret_key, encrypted_sig)
    if verify_digit_signature(origin_python_code, origin_signature, public_key):
        eval(origin_python_code)
```

---

### 2-11. Improper Certificate Validation (CWE-295)

SSL/TLS 인증서 검증을 비활성화하면 중간자 공격에 노출됩니다.

```python
# UNSAFE — 인증서 검증 비활성화 (CERT_NONE)
import ssl
import socket

def connect_with_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        context = ssl.SSLContext()
        context.verify_mode = ssl.CERT_NONE  # 취약
        with context.wrap_socket(sock) as ssock:
            ssock.connect(('127.0.0.1', 7917))
```

```python
# SAFE — PROTOCOL_TLS_CLIENT로 인증서 검증 활성화
import ssl
import socket

def connect_with_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('/path/to/CA.pem')
        with context.wrap_socket(sock, server_hostname='test-server') as ssock:
            ssock.connect(('127.0.0.1', 7917))
```

> **WARNING** requests 라이브러리 사용 시 `verify=False`를 절대 프로덕션에서 사용하지 마세요.

---

### 2-12. Sensitive Info in Persistent Cookie (CWE-539)

민감 정보를 쿠키에 평문 저장하면 탈취 위험이 있습니다.

```python
# UNSAFE — 쿠키 만료시간 1년, 보안 옵션 미설정
from django.http import HttpResponse

def remind_user_state(request):
    res = HttpResponse()
    res.set_cookie('rememberme', 1, max_age=60*60*24*365)
    return res
```

```python
# SAFE — 적절한 만료시간 + secure + httponly 옵션 활성화
from django.http import HttpResponse

def remind_user_state(request):
    res = HttpResponse()
    res.set_cookie('rememberme', 1, max_age=60*60, secure=True, httponly=True)
    return res
```

---

### 2-13. Sensitive Info in Comments (CWE-615)

주석에 비밀번호/키를 남기면 소스코드 노출 시 즉시 악용됩니다.

```python
# UNSAFE — 주석에 인증 정보 기재
def user_login(id, passwd):
    # id = admin
    # passwd = passw0rd
    result = login(id, passwd)
    return result
```

```python
# SAFE — 주석에 민감 정보 절대 기재 금지
def user_login(id, passwd):
    # 인증 정보는 환경변수에서 로드 (설정 가이드: wiki/db-setup 참조)
    result = login(id, passwd)
    return result
```

---

### 2-14. Unsalted One-Way Hash (CWE-759)

솔트 없이 해싱하면 레인보우 테이블 공격에 취약합니다.

```python
# UNSAFE — 솔트 없이 해싱
import hashlib

def get_hash_from_pwd(pw):
    h = hashlib.sha256(pw.encode())
    return h.digest()
```

```python
# SAFE — secrets로 솔트 생성 후 해싱
import hashlib
import secrets

def get_hash_from_pwd(pw):
    salt = secrets.token_hex(32)
    h = hashlib.sha256(salt.encode() + pw.encode())
    return h.digest(), salt
```

---

### 2-15. Download Without Integrity Check (CWE-494)

코드/라이브러리 다운로드 시 무결성을 검증하지 않으면 변조된 파일이 실행됩니다.

```python
# UNSAFE — 해시 검증 없이 다운로드
import requests

def execute_remote_code():
    url = "https://www.somewhere.com/storage/code.py"
    file = requests.get(url)
    with open('save.py', 'wb') as f:
        f.write(file.content)
```

```python
# SAFE — 해시 검증 후 저장
import requests
import hashlib
import configparser

def execute_remote_code():
    config = configparser.RawConfigParser()
    config.read('sample_config.cfg')
    url = "https://www.somewhere.com/storage/code.py"
    remote_code_hash = config.get('HASH', 'file_hash')
    file = requests.get(url)
    remote_code = file.content
    sha = hashlib.sha256()
    sha.update(remote_code)
    if sha.hexdigest() != remote_code_hash:
        raise Exception('파일이 손상되었습니다.')
    with open('save.py', 'wb') as f:
        f.write(file.content)
```

---

### 2-16. Missing Brute Force Protection (CWE-307)

인증 시도 횟수 제한이 없으면 무차별 대입 공격이 가능합니다.

```python
# UNSAFE — 시도 횟수 무제한
import hashlib
from django.shortcuts import render

def login(request):
    user_id = request.POST.get('user_id', '')
    user_pw = request.POST.get('user_pw', '')
    sha = hashlib.sha256()
    sha.update(user_pw.encode('utf-8'))
    hashed_passwd = get_user_pw(user_id)
    if sha.hexdigest() == hashed_passwd:
        return render(request, '/index.html', {'state': 'login_success'})
    return render(request, '/login.html', {'state': 'login_failed'})
```

```python
# SAFE — 로그인 실패 횟수 제한 + 계정 잠금
import hashlib
from django.shortcuts import render
from .models import LoginFail

LOGIN_TRY_LIMIT = 5

def login(request):
    user_id = request.POST.get('user_id', '')
    user_pw = request.POST.get('user_pw', '')
    sha = hashlib.sha256()
    sha.update(user_pw.encode('utf-8'))
    hashed_passwd = get_user_pw(user_id)
    if sha.hexdigest() == hashed_passwd:
        LoginFail.objects.filter(user_id=user_id).delete()
        return render(request, '/index.html', {'state': 'login_success'})
    if LoginFail.objects.filter(user_id=user_id).exists():
        login_fail = LoginFail.objects.get(user_id=user_id)
        count = login_fail.count
    else:
        count = 0
    if count >= LOGIN_TRY_LIMIT:
        return render(request, '/account_lock.html', {'state': 'account_lock'})
    LoginFail.objects.update_or_create(
        user_id=user_id, defaults={"count": count + 1}
    )
    return render(request, '/login.html', {'state': 'login_failed'})
```

---

## 3. Time and State (시간 및 상태)

### 3-1. TOCTOU Race Condition (CWE-367) — Python 고유

검사 시점과 사용 시점 사이에 상태가 변경되면 보안 검사가 무효화됩니다.

```python
# UNSAFE — 파일 검사와 사용 사이에 갭 존재 (멀티스레드 환경)
import os
import io
import threading

def write_shared_file(filename, content):
    if os.path.isfile(filename) is True:
        f = open(filename, 'w')
        f.seek(0, io.SEEK_END)
        f.write(content)
        f.close()

def start():
    filename = './temp.txt'
    content = "start time is now"
    my_thread = threading.Thread(target=write_shared_file, args=(filename, content))
    my_thread.start()
```

```python
# SAFE — threading.Lock으로 공유 자원 동기화
import os
import io
import threading

lock = threading.Lock()

def write_shared_file(filename, content):
    with lock:
        if os.path.isfile(filename) is True:
            f = open(filename, 'w')
            f.seek(0, io.SEEK_END)
            f.write(content)
            f.close()

def start():
    filename = './temp.txt'
    content = "start time is now"
    my_thread = threading.Thread(target=write_shared_file, args=(filename, content))
    my_thread.start()
```

---

### 3-2. Infinite Loop / Uncontrolled Recursion (CWE-835, CWE-674)

종료 조건이 없는 반복문/재귀는 서비스 거부를 유발합니다.

```python
# UNSAFE — 재귀 탈출 조건 없음
def factorial(num):
    return num * factorial(num - 1)
```

```python
# SAFE — 탈출 조건 명시
def factorial(num):
    if num == 0:
        return 1
    return num * factorial(num - 1)
```

```python
# SAFE — 재귀 깊이 제한 설정 (과도하게 크게 설정하지 않음)
import sys
sys.setrecursionlimit(1000)
```

---

## 4. Error Handling (에러처리)

### 4-1. Error Message Information Exposure (CWE-209)

상세 에러 메시지가 사용자에게 노출되면 시스템 정보가 유출됩니다.

**Django 에러 페이지**

```python
# UNSAFE — 별도 에러 페이지 미설정 (Django 기본 에러 페이지 출력)
# config/urls.py
# (에러 핸들러 미정의)
```

```python
# SAFE — 사용자 정의 에러 페이지 설정
# config/urls.py
from django.conf.urls import handler400, handler403, handler404, handler500

handler400 = "blog.views.error400"
handler403 = "blog.views.error403"
handler404 = "blog.views.error404"
handler500 = "blog.views.error500"
```

**traceback 노출**

```python
# UNSAFE — traceback.print_exc()로 스택 정보 노출
import traceback

def fetch_url(url, useragent):
    try:
        response = requests.get(url, stream=True, timeout=5,
                                headers={'User-Agent': useragent})
    except IOError:
        traceback.print_exc()  # 스택 정보 노출
```

```python
# SAFE — 에러 코드와 최소 정보만 로깅
import logging

logger = logging.getLogger(__name__)

def fetch_url(url, useragent):
    try:
        response = requests.get(url, stream=True, timeout=5,
                                headers={'User-Agent': useragent})
    except IOError:
        logger.error('ERROR-01:통신에러')
```

---

### 4-2. Error Condition Without Action (CWE-390)

예외를 포착하고도 아무 처리를 하지 않으면 오류가 무시됩니다.

```python
# UNSAFE — 예외를 무시 (pass)
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encryption(key_id, plain_text):
    static_key = {'key': b'0000000000000000', 'iv': b'0000000000000000'}
    try:
        static_key = static_keys[key_id]
    except IndexError:
        pass  # 기본 약한 키로 암호화 수행됨
    cipher_aes = AES.new(static_key['key'], AES.MODE_CBC, static_key['iv'])
    encrypted_data = base64.b64encode(cipher_aes.encrypt(pad(plain_text.encode(), 32)))
    return encrypted_data.decode('ASCII')
```

```python
# SAFE — 예외 시 안전한 랜덤 키 생성
import secrets
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encryption(key_id, plain_text):
    try:
        static_key = static_keys[key_id]
    except IndexError:
        static_key = {'key': secrets.token_bytes(16), 'iv': secrets.token_bytes(16)}
        static_keys.append(static_key)
    cipher_aes = AES.new(static_key['key'], AES.MODE_CBC, static_key['iv'])
    encrypted_data = base64.b64encode(cipher_aes.encrypt(pad(plain_text.encode(), 32)))
    return encrypted_data.decode('ASCII')
```

---

### 4-3. Improper Exception Handling (CWE-754)

지나치게 넓은 예외 처리는 예기치 않은 오류를 숨깁니다.

```python
# UNSAFE — bare except로 모든 예외를 한꺼번에 처리
def get_content():
    try:
        f = open('myfile.txt')
        s = f.readline()
        i = int(s.strip())
    except:
        print("Unexpected error")
```

```python
# SAFE — 예외를 구체적으로 분리 처리
def get_content():
    try:
        f = open('myfile.txt')
        s = f.readline()
        i = int(s.strip())
    except FileNotFoundError:
        print("file is not found")
    except OSError:
        print("cannot open file")
    except ValueError:
        print("Could not convert data to an integer.")
```

---

## 5. Code Quality (코드오류)

### 5-1. NULL Pointer Dereference (CWE-476)

Python에서는 None 값 참조 오류로 나타납니다. None 체크 없이 사용하면 비정상 종료됩니다.

```python
# UNSAFE — None 체크 없이 사용
import os
from django.shortcuts import render

def parse_xml(request):
    filename = request.POST.get('filename')
    if filename.count('.') > 0:  # filename이 None이면 크래시
        name, ext = os.path.splitext(filename)
    else:
        ext = ''
```

```python
# SAFE — None 체크 후 사용
import os
from django.shortcuts import render

def parse_xml(request):
    filename = request.POST.get('filename')
    if filename is None or filename.strip() == "":
        return render(request, '/error.html', {'error': '파일 이름이 없습니다.'})
    if filename.count('.') > 0:
        name, ext = os.path.splitext(filename)
    else:
        ext = ''
```

---

### 5-2. Improper Resource Shutdown (CWE-404)

사용 후 리소스를 해제하지 않으면 리소스 고갈이 발생합니다.

```python
# UNSAFE — 예외 발생 시 close() 미실행
def get_config():
    try:
        f = open('config.cfg')
        lines = f.readlines()
        raise Exception("Throwing the exception!")
        f.close()  # 예외 시 도달하지 않음
        return lines
    except Exception:
        return ''
```

```python
# SAFE (방법 1) — finally 블록에서 자원 해제
def get_config():
    lines = None
    try:
        f = open('config.cfg')
        lines = f.readlines()
        raise Exception("Throwing the exception!")
    except Exception:
        pass
    finally:
        f.close()
        return lines
```

```python
# SAFE (방법 2) — with 문으로 자동 자원 해제
with open('config.cfg') as f:
    print(f.read())
```

---

### 5-3. Deserialization of Untrusted Data (CWE-502)

신뢰할 수 없는 데이터를 pickle로 역직렬화하면 임의 코드가 실행됩니다.

```python
# UNSAFE — 외부 데이터를 pickle로 직접 역직렬화
import pickle
from django.shortcuts import render

def load_user_object(request):
    pickled_userinfo = pickle.dumps(request.POST.get('userinfo', ''))
    user_obj = pickle.loads(pickled_userinfo)
    return render(request, '/load_user_obj.html', {'obj': user_obj})
```

```python
# SAFE — HMAC으로 데이터 무결성 검증 후 역직렬화
import hmac
import hashlib
import pickle
from django.shortcuts import render

def load_user_object(request):
    hashed_pickle = request.POST.get("hashed_pickle", "")
    pickled_userinfo = pickle.dumps(request.POST.get("userinfo", ""))
    m = hmac.new(key="secret_key".encode("utf-8"), digestmod=hashlib.sha512)
    m.update(pickled_userinfo)
    if hmac.compare_digest(str(m.digest()), hashed_pickle):
        user_obj = pickle.loads(pickled_userinfo)
        return render(request, "/load_user_obj.html", {"obj": user_obj})
    return render(request, "/error.html", {"error": "신뢰할 수 없는 데이터입니다."})
```

> **WARNING** pickle은 원격 코드 실행이 가능합니다. 가능하면 JSON 등 안전한 포맷을 사용하세요.

---

## 6. Encapsulation (캡슐화)

### 6-1. Data Leak Between Sessions (CWE-488, CWE-543)

멀티스레드 환경에서 클래스 변수에 사용자 데이터를 저장하면 세션 간 데이터가 유출됩니다.

```python
# UNSAFE — 클래스 변수에 사용자 데이터 저장
from django.shortcuts import render

class UserDescription:
    user_name = ''

    def get_user_profile(self):
        result = self.get_user_description(UserDescription.user_name)
        return result

    def show_user_profile(self, request):
        UserDescription.user_name = request.POST.get('name', '')
        self.user_profile = self.get_user_profile()
        return render(request, 'profile.html', {'profile': self.user_profile})
```

```python
# SAFE — 인스턴스 변수로 사용해 스레드 간 공유 방지
from django.shortcuts import render

class UserDescription:
    def get_user_profile(self):
        result = self.get_user_description(self.user_name)
        return result

    def show_user_profile(self, request):
        self.user_name = request.POST.get('name', '')
        self.user_profile = self.get_user_profile()
        return render(request, 'profile.html', {'profile': self.user_profile})
```

---

### 6-2. Active Debug Code (CWE-489)

디버그 코드가 프로덕션에 남으면 시스템 내부 정보가 노출됩니다.

**Django**

```python
# UNSAFE — settings.py에 DEBUG = True
DEBUG = True
```

```python
# SAFE — 배포 시 DEBUG = False
DEBUG = False
```

**Flask**

```python
# UNSAFE — debug 모드 활성화
from flask import Flask
app = Flask(__name__)
app.debug = True

if __name__ == '__main__':
    app.run(debug=True)
```

```python
# SAFE — debug 모드 비활성화
from flask import Flask
app = Flask(__name__)
app.debug = False

if __name__ == '__main__':
    app.run(debug=False)
```

---

### 6-3. Private Data Returned from Public Method (CWE-495)

내부 배열/객체의 참조를 직접 반환하면 외부에서 수정이 가능합니다.

```python
# UNSAFE — private 배열의 참조를 직접 반환
class UserObj:
    __private_variable = []

    def get_private_member(self):
        return self.__private_variable  # 외부에서 수정 가능
```

```python
# SAFE — 복사본 반환 ([:]로 새 객체 생성)
class UserObj:
    __private_variable = []

    def get_private_member(self):
        return self.__private_variable[:]  # 복사본 반환
```

---

### 6-4. Public Data Assigned to Private Field (CWE-496)

외부 배열/객체를 내부 필드에 직접 할당하면 외부 변경이 내부에 반영됩니다.

```python
# UNSAFE — 외부 참조를 private 배열에 직접 할당
class UserObj:
    __private_variable = []

    def set_private_member(self, input_list):
        self.__private_variable = input_list  # 외부 참조 공유
```

```python
# SAFE — 복사본을 할당 ([:]로 새 객체 생성)
class UserObj:
    def __init__(self):
        self.__privateVariable = []

    def set_private_member(self, input_list):
        self.__privateVariable = input_list[:]  # 복사본 할당
```

---

## 7. API Misuse (API 오용)

### 7-1. Reliance on DNS Lookup (CWE-350)

DNS 기반 보안 결정은 DNS 스푸핑으로 우회될 수 있습니다.

```python
# UNSAFE — 도메인명으로 신뢰 여부 판단
def is_trust(host_domain_name):
    trusted = False
    trusted_host = "trust.example.com"
    if trusted_host == host_domain_name:
        trusted = True
    return trusted
```

```python
# SAFE — IP 주소로 직접 비교
import socket

def is_trust(host_domain_name):
    trusted = False
    trusted_ip = "192.168.10.7"
    dns_resolved_ip = socket.gethostbyname(host_domain_name)
    if trusted_ip == dns_resolved_ip:
        trusted = True
    return trusted
```

---

### 7-2. Use of Vulnerable API

취약한 API/패키지를 사용하면 보안 위협에 노출됩니다.

```python
# UNSAFE — 취약한 버전의 패키지 사용, SBOM 미관리
# requirements.txt
# urllib3==1.24.1  (CVE가 알려진 취약 버전)
```

```python
# SAFE — 취약점이 패치된 최신 버전 사용 + SBOM 관리
# requirements.txt
# urllib3>=1.26.5  (취약점 패치된 버전)
#
# SBOM을 적용하여 의존 패키지의 보안 이슈를 지속 모니터링합니다.
# - NIST NVD (https://nvd.nist.gov/vuln/search)
# - CVEdetails (https://www.cvedetails.com)
# - pip-audit, safety 등 도구로 정기 검사
```

> **TIP** 사용 중인 패키지의 보안 권고(advisory)를 정기적으로 확인하세요. `pip-audit` 또는 `safety check` 명령으로 취약점을 스캔할 수 있습니다.
