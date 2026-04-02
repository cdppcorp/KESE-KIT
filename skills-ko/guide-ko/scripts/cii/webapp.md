# Web Application 점검 스크립트

## 1. SSTI (Server Side Template Injection)
**취약 패턴:**
```python
# Python (Jinja2) - 사용자 입력을 직접 템플릿에 삽입
template = param  # 사용자 입력이 직접 템플릿으로 사용됨
return render_template_string(template)
```
**안전한 구현:**
```python
# Python (Jinja2) - 사용자 입력을 템플릿 변수로 전달
template = "userinput : {{ userinput }}"
return render_template_string(template, userinput=param)
```

---

## 2. SQL Injection (SI)

### 취약 패턴
```java
// Java - 문자열 연결 방식 쿼리 (취약)
String sql = "SELECT * FROM users WHERE username = '" + userInput + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(sql);
```

### 안전한 구현 - PreparedStatement (Java)
```java
// Java - PreparedStatement 사용
String sql = "SELECT * FROM users WHERE username = ?";
PreparedStatement preparedStatement = connection.prepareStatement(sql);
preparedStatement.setString(1, userInput);
ResultSet resultSet = preparedStatement.executeQuery();
```

### 안전한 구현 - ORM (JPA/Hibernate)
```java
// Java - JPQL 파라미터 바인딩
public class ItemService {
    @PersistenceContext
    private EntityManager em;
    public List<Item> findItemsByUserInput(String userInput) {
        String jpql = "SELECT i FROM Item i WHERE i.itemID > :userInput";
        Query query = em.createQuery(jpql, Item.class);
        query.setParameter("userInput", userInput);
        return query.getResultList();
    }
}
```

### 안전한 구현 - MyBatis 파라미터 바인딩
```xml
<!-- MyBatis - #{} 사용 (${} 사용 금지) -->
<insert id="insertStudent" parameterType="com.example.Student">
    INSERT INTO STUDENTS (NUM, NAME, AGE, GRADE)
    VALUES (#{num}, #{name}, #{age}, #{grade})
</insert>
<delete id="deleteStudent" parameterType="int">
    DELETE FROM STUDENTS WHERE NUM = #{num}
</delete>
```

### 안전한 구현 - SQL 키워드 필터링 (Java)
```java
public static String sanitize(String input) {
    if (input == null) return null;
    String[] sqlKeywords = {"SELECT", "UNION", "INSERT", "UPDATE", "DELETE", "DROP", "--"};
    String pattern = "(?i)\\b(" + String.join("|", sqlKeywords) + ")\\b|['\"\\\\;()<>#/*!]";
    Pattern regex = Pattern.compile(pattern + "|--");
    Matcher matcher = regex.matcher(input);
    return matcher.replaceAll(" ");
}
```

### 안전한 구현 - PreparedStatement (PHP)
```php
// PHP - PDO PreparedStatement
$sql = "SELECT * FROM users WHERE username = ?";
$stmt = $pdo->prepare($sql);
$stmt->execute([$userInput]);
$results = $stmt->fetchAll(PDO::FETCH_ASSOC);
```

### 안전한 구현 - 예외 처리
```java
// Java - 적절한 예외 처리 (에러 메시지 노출 방지)
try {
    // 데이터베이스 작업
} catch (SQLException e) {
    e.printStackTrace();  // 로그에만 기록
    System.out.println("An error occurred. Please try again later.");  // 사용자에게 일반 메시지
}
```
```php
// PHP - PDO 예외 처리
try {
    // 데이터베이스 작업
} catch (PDOException $e) {
    error_log($e->getMessage());
    echo 'SQL Exception';  // 상세 에러 노출 금지
}
```

### 특수문자 필터링 대상
| 문자 | 설명 |
|------|------|
| `'` | 문자 데이터 구분 기호 |
| `;` | 쿼리 구분 기호 |
| `--`, `#` | 라인 주석 구분 기호 |
| `/* */` | 블록 주석 |

---

## 3. 디렉터리 인덱싱 (DI)
**조치:**
```apache
# Apache - Indexes 옵션 제거
<Directory /var/www/html>
    Options FollowSymLinks   # Indexes 제거
</Directory>
```
```xml
<!-- Tomcat - listings=false -->
<init-param>
    <param-name>listings</param-name>
    <param-value>false</param-value>
</init-param>
```
```nginx
# Nginx
server {
    location / {
        autoindex off;
    }
}
```

---

## 4. 에러 페이지 적용 미흡 (EP)
**조치:**
```apache
# Apache - 서버 정보 노출 제거 및 사용자 에러 페이지 정의
ServerTokens Prod
ServerSignature Off
ErrorDocument 404 /main/error.html
ErrorDocument 405 /main/error.html
```
```xml
<!-- Tomcat server.xml - 서버 정보 제거 -->
<Connector port="8080" protocol="HTTP/1.1"
    connectionTimeout="20000" redirectPort="8443"
    maxParameterCount="1000" server=" " />
<!-- Tomcat server.xml - 개발용 리포트 비활성화 -->
<Valve className="org.apache.catalina.valves.ErrorReportValve"
    showReport="false" showServerInfo="false" />
```
```xml
<!-- Tomcat web.xml - 에러 페이지 매핑 -->
<error-page>
    <error-code>404</error-code>
    <location>/errors/404</location>
</error-page>
<error-page>
    <error-code>500</error-code>
    <location>/errors/500</location>
</error-page>
<error-page>
    <exception-type>java.lang.Exception</exception-type>
    <location>/errors/500</location>
</error-page>
```
```nginx
# Nginx - 서버 정보 제거 및 사용자 에러 페이지
http {
    server_tokens off;
}
server {
    error_page 400 401 402 405 /custom_4xx.html;
    error_page 404 /custom_404.html;
    error_page 500 502 503 504 /custom_5xx.html;
    location = /custom_404.html { root /var/www/html; internal; }
    location = /custom_4xx.html { root /var/www/html; internal; }
    location = /custom_5xx.html { root /var/www/html; internal; }
}
```

---

## 5. 정보 누출 (IL)
**조치 항목:**
1. robots.txt, web.config, nginx.conf로 검색 차단 디렉터리/확장자 지정
2. 백업 파일 삭제 (*.bak, *.backup, *.org, *.old, *.zip, *.log, *.sql, *.tmp, *.temp)
3. 초기 페이지/디렉터리/배너 삭제
4. 개인정보 마스킹 처리 (홍\*동, 901231-1\*\*\*\*\*\*, 010-1234-\*\*\*\* 등)
5. 개발 중 주석/디버그 정보 제거

---

## 6. 크로스사이트 스크립트 - XSS (XS)

### 취약 패턴
```javascript
// JavaScript - innerHTML 사용 (취약)
document.getElementById('output').innerHTML = userInput;
// document.write(userInput);  // 취약
```

### 안전한 구현 - HTML Entity 변환 (Java)
```java
public static String sanitizeInput(String input) {
    if (input == null) return null;
    return input.replaceAll("&", "&amp;")
                .replaceAll("<", "&lt;")
                .replaceAll(">", "&gt;")
                .replaceAll("\"", "&quot;")
                .replaceAll("'", "&#39;");
}
```

### 안전한 구현 - HTML Entity 변환 (PHP)
```php
function escapeHtml($input) {
    return htmlspecialchars($input, ENT_QUOTES | ENT_HTML5, 'UTF-8', false);
}
// 추가 문자열 필터링이 필요한 경우
function escapeHtmlExtended($input) {
    $escaped = htmlspecialchars($input, ENT_QUOTES | ENT_HTML5, 'UTF-8', false);
    $additionalEscapes = [
        '\\' => '&#92;',
        '('  => '&#40;',
        ')'  => '&#41;',
        '#'  => '&#35;'
    ];
    return strtr($escaped, $additionalEscapes);
}
```

### 특수문자 필터링 대상
| 변경 전 | 변경 후 |
|---------|---------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `(` | `&#40;` |
| `)` | `&#41;` |
| `#` | `&#35;` |
| `&` | `&amp;` |

### 쿠키 보안 설정
```
Set-Cookie: sessionId=abc123; HttpOnly; Secure; SameSite=Strict
```

---

## 7. 크로스사이트 요청 위조 - CSRF (CF)

### 안전한 구현 - CSRF Token (Java/Spring)
```java
// CSRF Token 생성 및 세션 저장
public String index(Model model, HttpServletRequest request) {
    HttpSession session = request.getSession();
    String csrfToken = generateCsrfToken();
    session.setAttribute("csrfToken", csrfToken);
    model.addAttribute("csrfToken", csrfToken);
    return "index";
}

// CSRF Token 생성 함수
private String generateCsrfToken() {
    SecureRandom secureRandom = new SecureRandom();
    byte[] token = new byte[16];
    secureRandom.nextBytes(token);
    return Base64.getUrlEncoder().encodeToString(token);
}

// CSRF Token 검증
@PostMapping("/submit")
public String submit(@RequestParam("input") String input,
                     @RequestParam("csrfToken") String csrfToken,
                     HttpServletRequest request, Model model) {
    HttpSession session = request.getSession();
    String sessionToken = (String) session.getAttribute("csrfToken");
    if (sessionToken == null || !sessionToken.equals(csrfToken)) {
        throw new IllegalStateException("Invalid CSRF token");
    }
    String sanitizedInput = sanitizeInput(input);
    inputs.add(sanitizedInput);
    return "index";
}
```

### HTML 폼에 CSRF Token 포함
```html
<form action="/submit" method="post">
    <input type="hidden" name="csrfToken" th:value="${csrfToken}" />
    <label for="input">Enter text:</label>
    <input type="text" id="input" name="input">
    <button type="submit">Add</button>
</form>
```

### 추가 방어 조치
1. Referer/Origin 헤더 검증으로 외부 도메인 요청 차단
2. SameSite 쿠키 옵션 적용
3. HTTPS 환경에서 Secure, HttpOnly 속성 적용

---

## 8. 서버사이드 요청 위조 - SSRF (SF)

### 안전한 구현 - URL 화이트리스트 (Java)
```java
private final List<String> allowedDomains = Arrays.asList("example.com");
private final Map<String, List<Integer>> allowedIPsAndPorts = new HashMap<>();

public UrlValidator() {
    allowedIPsAndPorts.put("192.168.1.100", Arrays.asList(80, 443, 8080));
    allowedIPsAndPorts.put("10.0.0.1", Arrays.asList(80, 443));
}

public boolean isUrlAllowed(String urlString) {
    try {
        URL url = new URL(urlString);
        String protocol = url.getProtocol();
        // HTTP와 HTTPS만 허용
        if (!("http".equalsIgnoreCase(protocol) || "https".equalsIgnoreCase(protocol))) {
            return false;
        }
        String host = url.getHost();
        int port = url.getPort() == -1 ? url.getDefaultPort() : url.getPort();
        if (allowedDomains.contains(host)) return true;
        if (allowedIPsAndPorts.containsKey(host)) {
            return allowedIPsAndPorts.get(host).contains(port);
        }
        return false;
    } catch (Exception e) {
        return false;
    }
}
```

### 안전한 구현 - URL 화이트리스트 (PHP)
```php
function isUrlAllowed($url) {
    $allowedDomains = ['example.com', 'api.example.com'];
    $allowedIPsAndPorts = [
        '192.168.10.10' => [80, 443, 8000],
        '10.0.0.1' => [80, 443]
    ];
    $parsedUrl = parse_url($url);
    if (!$parsedUrl || !isset($parsedUrl['host'])) return false;

    $host = $parsedUrl['host'];
    $port = isset($parsedUrl['port']) ? $parsedUrl['port']
          : ($parsedUrl['scheme'] === 'https' ? 443 : 80);
    if (in_array($host, $allowedDomains, true)) return true;
    if (filter_var($host, FILTER_VALIDATE_IP)) {
        if (array_key_exists($host, $allowedIPsAndPorts)) {
            return in_array($port, $allowedIPsAndPorts[$host], true);
        }
    }
    return false;
}
```

### PHP 설정 강화
```ini
; php.ini - 원격 URL 접근 차단
allow_url_fopen=Off
allow_url_include=Off
```

### 추가 방어 조치
1. 내부 네트워크 대역 및 관리용 포트 요청 차단
2. http, https 외 프로토콜(file://, gopher://, data://) 차단
3. 에러 발생 시 응답값 노출 금지
4. 애플리케이션 서버와 내부 시스템 간 네트워크 분리

---

## 9. 약한 비밀번호 정책 (BF)
**비밀번호 복잡성 검증 (JavaScript):**
```javascript
function isPasswordStrong(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    return password.length >= minLength
        && hasUpperCase && hasLowerCase
        && hasNumber && hasSpecialChar;
}
```
**취약 ID 예시:** admin, administrator, manager, guest, tomcat, root, user
**취약 비밀번호 예시:** abcd, 1234, 1111, test, password, public, 빈 비밀번호, ID와 동일

---

## 10. 불충분한 인증 절차 (IA)

### 안전한 구현 - 재인증 로직 (Java)
```java
// 중요 페이지 접근 시 세션 기반 인증 검증
public String editProfile(HttpSession session, Model model) {
    User user = (User) session.getAttribute("user");
    Boolean isVerified = (Boolean) session.getAttribute("isVerified");
    if (user == null || isVerified == null || !isVerified) {
        return "redirect:/user/authenticate";
    }
    model.addAttribute("user", user);
    return "edit_profile";
}

@PostMapping("/verify_code")
public String verifyCode(@RequestParam String code, HttpSession session) {
    if (input.equals(code)) {
        session.setAttribute("isVerified", true);
        return "redirect:/user/edit_profile";
    } else {
        return "redirect:/user/authenticate?error=true";
    }
}
```

### 안전한 구현 - 접근 통제 공통 모듈 (Java)
```java
public class AccessControl {
    public static boolean isAuthenticated(HttpSession session) {
        return session.getAttribute("user") != null;
    }
    public static boolean isVerified(HttpSession session) {
        return Boolean.TRUE.equals(session.getAttribute("isVerified"));
    }
}
```

---

## 11. 불충분한 권한 검증 (IN)

### 안전한 구현 - 서버 사이드 세션 검증 (Java)
```java
@GetMapping("/inquiry/{id}")
public String viewInquiry(@PathVariable Long id, Model model, HttpSession session) {
    User currentUser = (User) session.getAttribute("currentUser");
    if (currentUser == null) {
        throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Not logged in");
    }
    Inquiry inquiry = inquiryService.findInquiryById(id);
    if (!inquiry.getUser().getUsername().equals(currentUser.getUsername())) {
        throw new ResponseStatusException(HttpStatus.FORBIDDEN, "permission denied");
    }
    model.addAttribute("inquiry", inquiry);
    return "inquiry_detail";
}
```

---

## 12. 취약한 비밀번호 복구 절차 (PR)

### 안전한 구현 - 안전한 임시 비밀번호 생성 (Java)
```java
private static final String CHARACTERS =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
private static final int PASSWORD_LENGTH = 12;

private String generateTemporaryPassword() {
    SecureRandom secureRandom = new SecureRandom();
    StringBuilder password = new StringBuilder(PASSWORD_LENGTH);
    for (int i = 0; i < PASSWORD_LENGTH; i++) {
        int randomIndex = secureRandom.nextInt(CHARACTERS.length());
        password.append(CHARACTERS.charAt(randomIndex));
    }
    return password.toString();
}
```

### 안전한 구현 - 안전한 임시 비밀번호 생성 (PHP)
```php
function generateRandomPassword($length = 12) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()';
    $charactersLength = strlen($characters);
    $randomPassword = '';
    for ($i = 0; $i < $length; $i++) {
        $randomPassword .= $characters[random_int(0, $charactersLength - 1)];
    }
    return $randomPassword;
}
```

---

## 13. 프로세스 검증 누락 (PV)

### 안전한 구현 - 세션 기반 접근 통제 (Java/Spring)
```java
// 인터셉터 설정 - 비공개/공개 페이지 구분
public class SessionConfig implements WebMvcConfigurer {
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new SessionInterceptor())
            .addPathPatterns("/home", "/board/**")
            .excludePathPatterns("/login", "/register", "/error");
    }
}

public class SessionInterceptor implements HandlerInterceptor {
    public boolean preHandle(HttpServletRequest request,
            HttpServletResponse response, Object handler) throws Exception {
        if (request.getSession().getAttribute("user") == null) {
            response.sendRedirect("/login");
            return false;
        }
        return true;
    }
}
```

### 안전한 구현 - 플로우 제어 (PHP)
```php
session_start();
if ($step_completed) {
    $_SESSION['step1_completed'] = true;
    header('Location: step2.php');
    exit;
}
// 2단계 직접 접근 시
if (!isset($_SESSION['step1_completed']) || $_SESSION['step1_completed'] !== true) {
    header('Location: step1.php');  // 1단계 미완료 시 리다이렉트
    exit;
}
```

---

## 14. 악성 파일 업로드 (FU)

### 안전한 구현 - 파일 업로드 보안 (Java)
```java
private static final String[] ALLOWED_EXTENSIONS = {"jpg", "png", "pdf", "txt"};
private static final Set<String> ALLOWED_MIME = Set.of(
    "image/jpeg", "image/png", "application/pdf", "text/plain");

// 파일명 정규화
private static String normalizeFilename(String filename) {
    if (filename == null) return null;
    String name = java.net.URLDecoder.decode(filename, StandardCharsets.UTF_8);
    name = Normalizer.normalize(name, Normalizer.Form.NFC);
    name = name.replace("\0", "");
    name = name.replaceAll("[<>:\"/\\\\|?*]", "");
    name = name.replaceAll("^[.\\s]+|[.\\s]+$", "");
    return name;
}

// 확장자 추출 + 이중 확장자 차단
private static String getExtension(String filename) {
    String safe = normalizeFilename(filename);
    int dotCount = safe.length() - safe.replace(".", "").length();
    if (dotCount != 1) return "";  // 이중 확장자 차단
    int idx = safe.lastIndexOf('.');
    return (idx == -1) ? "" : safe.substring(idx + 1).toLowerCase();
}

public static String saveFile(MultipartFile file, String uploadDir) throws IOException {
    String original = file.getOriginalFilename();
    String ext = getExtension(original);
    if (!Arrays.asList(ALLOWED_EXTENSIONS).contains(ext)) {
        throw new IOException("허용되지 않은 확장자");
    }
    // MIME 시그니처 검증
    Tika tika = new Tika();
    String mime = tika.detect(file.getInputStream());
    if (!ALLOWED_MIME.contains(mime)) {
        throw new IOException("허용되지 않은 파일 유형");
    }
    // 파일명 난수화
    String newName = UUID.randomUUID().toString().replace("-", "") + "." + ext;
    Path savePath = Paths.get(uploadDir, newName);
    file.transferTo(savePath.toFile());
    return newName;
}
```

### 안전한 구현 - 파일 업로드 보안 (PHP)
```php
function normalize_filename($filename) {
    $filename = urldecode($filename);
    $filename = normalizer_normalize($filename, Normalizer::FORM_C);
    $filename = str_replace("\0", "", $filename);
    $filename = preg_replace('/[<>:"\/\\\\|?*]/', '', $filename);
    $filename = preg_replace('/^[\.\s]+|[\.\s]+$/u', '', $filename);
    return $filename;
}

function is_valid_extension($filename, $allowed_exts) {
    $safe = normalize_filename($filename);
    if (substr_count($safe, '.') !== 1) return false;  // 이중 확장자 차단
    $ext = strtolower(pathinfo($safe, PATHINFO_EXTENSION));
    return in_array($ext, $allowed_exts, true);
}

function save_upload($file, $uploadDir) {
    $allowed_exts = ['jpg', 'jpeg', 'png', 'pdf', 'txt'];
    $allowed_mime = ['image/jpeg', 'image/png', 'application/pdf', 'text/plain'];

    if (!is_valid_extension($file['name'], $allowed_exts)) {
        throw new Exception("허용되지 않은 확장자");
    }
    $mime = mime_content_type($file['tmp_name']);
    if (!in_array($mime, $allowed_mime, true)) {
        throw new Exception("허용되지 않은 파일 유형");
    }
    // 파일명 난수화
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    $newName = bin2hex(random_bytes(16)) . '.' . $ext;
    $dest = rtrim($uploadDir, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . $newName;
    if (!move_uploaded_file($file['tmp_name'], $dest)) {
        throw new Exception("파일 저장 실패");
    }
    return $newName;
}
```

### 핵심 보안 조치
1. 확장자 화이트리스트 검증 + MIME 타입 검증
2. 파일명 난수화 (UUID 등)
3. 업로드 경로를 웹 디렉터리 외부에 배치
4. 업로드된 파일의 실행 권한 제거

---

## 15. 파일 다운로드 (FD)

### 안전한 구현 - 파일명 검증 (Java)
```java
public class FileDownloadUtil {
    // 파일명에 영문, 숫자, 일부 특수문자만 허용
    public static boolean isValidFileName(String fileName) {
        return fileName != null && fileName.matches("^[a-zA-Z0-9._-]+$");
    }

    private static final Set<String> ALLOWED_EXTENSIONS = Set.of("jpg", "png");

    public static boolean isAllowedExtension(String filePath) {
        String extension = filePath.substring(filePath.lastIndexOf(".") + 1).toLowerCase();
        return ALLOWED_EXTENSIONS.contains(extension);
    }
}

@GetMapping("/downloadFile")
public ResponseEntity<Resource> downloadFile(@RequestParam String filename) throws IOException {
    if (!FileDownloadUtil.isValidFileName(filename)
        || !FileDownloadUtil.isAllowedExtension(filename)) {
        return ResponseEntity.badRequest().build();
    }
    // ... 다운로드 로직
}
```

### 안전한 구현 - 경로 정규화 (PHP)
```php
if (isset($_GET['file'])) {
    $file = filter_input(INPUT_GET, 'file', FILTER_SANITIZE_STRING);
    $filePath = realpath('../uploads/' . $file);  // 경로 정규화
    // 파일 경로가 지정된 디렉터리 내에 있는지 확인
    if ($filePath && strpos($filePath, realpath('../uploads/')) === 0) {
        downloadFile($filePath);
    } else {
        echo "잘못된 파일 경로입니다.";
        exit;
    }
}
```

### 우회 공격 대응
| 인코딩 방식 | 예시 |
|-------------|------|
| URL 인코딩 | `.(%2e)`, `/(%2f)`, `\(%5c)` |
| 더블 URL 인코딩 | `.(%252e)`, `/(%252f)` |
| 16bit 유니코드 | `.(%u002e)`, `/(%u2215)` |
| 특수문자 중첩 | `....//` → `../` |
| 종단 문자 추가 | `[파일명]%00.jpg` |

---

## 16. 불충분한 세션 관리 (IS)

### 안전한 구현 - 세션 고정 방지 (Java/Spring)
```java
@RequestMapping("/login")
public String login(HttpServletRequest request) {
    request.changeSessionId();  // 신규 로그인 시 세션 ID 변경
    return "redirect:/home";
}

// Spring Security 설정
@Override
protected void configure(HttpSecurity http) throws Exception {
    http.sessionManagement()
        .sessionFixation().migrateSession()
        .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
        .maximumSessions(1).maxSessionsPreventsLogin(false)
        .expiredUrl("/login?expired");
}
```

### 세션 만료 시간 설정
```xml
<!-- Java web.xml -->
<session-config>
    <session-timeout>60</session-timeout>  <!-- 60분 -->
</session-config>
```
```properties
# Spring Boot application.properties
server.servlet.session.timeout=60m
```
```php
// PHP - 세션 재생성 및 만료 설정
session_start();
session_regenerate_id(true);  // 예측 불가능한 세션 ID 생성
ini_set('session.gc_maxlifetime', 3600);   // 60분
ini_set('session.cookie_lifetime', 3600);
```

### JWT 보안 설정
| 안전한 알고리즘 | 설명 |
|----------------|------|
| HS256~512 | 비밀 키 기반 HMAC 해시 |
| RS256~512 | 비대칭 키 RSA 서명 |
| ES256~512 | 타원 곡선 암호화 서명 |

| 취약한 알고리즘 | 설명 |
|----------------|------|
| HS1, RS1 | SHA-1 기반 (취약) |
| none | 서명 생략 (위험) |
| plaintext | 평문 서명 (위험) |

---

## 17. 데이터 평문 전송 (SN)
**조치:**
```apache
# Apache - TLSv1.2 이상 사용, SSLv2/v3 비활성화
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
```
```
# IIS - 레지스트리에서 SSL 2.0, 3.0 비활성화
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 2.0\Server]
"Enabled"=dword:00000000
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\SSL 3.0\Server]
"Enabled"=dword:00000000
```

---

## 18. 쿠키 변조 (CC)

### 안전한 구현 - AES + HMAC 쿠키 (Java)
```java
public class CookieUtil {
    private static final int IV_LEN = 16, HMAC_LEN = 32;
    private final byte[] encKey;   // AES-256 키 (32 bytes)
    private final byte[] hmacKey;  // HMAC 키

    // 보안 쿠키 생성
    public void addSecureCookie(HttpServletResponse resp, String name,
                                String plaintext, int maxAgeSec) throws Exception {
        byte[] iv = new byte[IV_LEN];
        new SecureRandom().nextBytes(iv);

        // AES-256-CBC 암호화
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE,
            new SecretKeySpec(encKey, "AES"), new IvParameterSpec(iv));
        byte[] ciphertext = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));

        // HMAC 생성
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(hmacKey, "HmacSHA256"));
        mac.update(iv);
        mac.update(ciphertext);
        byte[] hmac = mac.doFinal();

        // payload = IV + HMAC + 암호문
        byte[] payload = new byte[iv.length + hmac.length + ciphertext.length];
        System.arraycopy(iv, 0, payload, 0, iv.length);
        System.arraycopy(hmac, 0, payload, iv.length, hmac.length);
        System.arraycopy(ciphertext, 0, payload, iv.length + hmac.length, ciphertext.length);

        String encoded = Base64.getUrlEncoder().withoutPadding().encodeToString(payload);

        // HttpOnly, Secure, SameSite 속성 설정
        String header = String.format(
            "%s=%s; Max-Age=%d; Path=/; HttpOnly; Secure; SameSite=Strict",
            name, encoded, maxAgeSec);
        resp.addHeader("Set-Cookie", header);
    }
}
```

---

## 19. 관리자 페이지 노출 (AE)
**조치:**
1. 유추하기 어려운 URL 및 포트로 관리자 페이지 변경
2. 지정된 IP만 관리자 페이지 접근 허용
3. 관리자 로그인 시 2차 인증(OTP, VPN, 인증서) 적용
4. 하위 페이지별 세션 검증 구현

---

## 20. 자동화 공격 (CC)
**조치:**
1. 로그인 시도, 게시글 등록, SMS 발송 등에 횟수 제한 설정
2. CAPTCHA 등 일회성 확인 로직 구현
3. IDS/IPS 시스템으로 대량 패킷 감지 및 차단
4. 로그인 실패 3~5회 초과 시 계정 잠금 로직 구현

---

## 21. 불필요한 Method 악용 (WM)

### 조치 - Apache
```bash
# WebDAV 비활성화
sudo a2dismod dav
sudo a2dismod dav_fs

# 불필요한 메소드 제한
# /etc/apache2/apache2.conf
<Directory "/var/www/html">
    Dav Off
    <LimitExcept GET POST OPTIONS>
        Order Allow,Deny
        Deny from all
    </LimitExcept>
</Directory>

# TRACE 메소드 비활성화
TraceEnable Off

# CONNECT 메소드 비활성화 (mod_rewrite)
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{REQUEST_METHOD} ^CONNECT
    RewriteRule .* - [F]
</IfModule>
```

### 조치 - Tomcat
```xml
<!-- WebDAV readonly 설정 -->
<init-param>
    <param-name>readonly</param-name>
    <param-value>true</param-value>
</init-param>

<!-- TRACE 비활성화 - server.xml에서 allowTrace 제거 -->
<Connector port="8080" protocol="HTTP/1.1"
    connectionTimeout="20000" redirectPort="8443" />
```

### 조치 - Nginx
```nginx
# WebDAV 비활성화 - dav_methods 지시어 삭제
# Nginx는 0.5.17 이후 TRACE를 405로 거부
# CONNECT 메소드는 기본적으로 미지원
```

### 조치 - IIS
```
# IIS 6.0 이상: 요청 필터링 > HTTP 동사 > 동사 거부에 TRACE 추가
# WebDAV 기능 비활성화 확인
```
