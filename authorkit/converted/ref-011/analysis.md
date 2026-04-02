# ref-011: JavaScript 시큐어코딩 가이드 (2023년 개정본)

## 문서 정보

| 항목 | 값 |
|------|-----|
| 제목 | Javascript 시큐어코딩 가이드 (2023년 개정본) |
| 발행기관 | KISA (한국인터넷진흥원) |
| 연도 | 2023 |
| 페이지 | 159p |
| 대상 언어 | JavaScript (ES13+, Node.js) |

## 구조 (목차)

```
PART 제1장 개요 (p.7~14)
  제1절 배경 (p.8)
  제2절 왜 자바스크립트인가 (p.10)
  제3절 가이드 목적 및 구성 (p.12)

PART 제2장 시큐어코딩 가이드 (p.15~150)
  제1절 입력데이터 검증 및 표현 (p.16~67) — 13개 항목
    1. SQL 삽입 (p.16)
    2. 코드 삽입 (p.22)
    3. 경로 조작 및 자원 삽입 (p.25)
    4. 크로스사이트 스크립트 XSS (p.29)
    5. 운영체제 명령어 삽입 (p.38)
    6. 위험한 형식 파일 업로드 (p.41)
    7. 신뢰되지 않은 URL주소로 자동접속 연결 (p.44)
    8. 부적절한 XML 외부 개체 참조 (p.46)
    9. XML 삽입 (p.49)
    10. LDAP 삽입 (p.52)
    11. 크로스사이트 요청 위조 CSRF (p.56)
    12. 서버사이드 요청 위조 SSRF (p.62)
    13. 보안기능 결정에 사용되는 부적절한 입력값 (p.65)

  제2절 보안기능 (p.68~112) — 16개 항목
    1. 적절한 인증 없는 중요 기능 허용 (p.68)
    2. 부적절한 인가 (p.71)
    3. 중요한 자원에 대한 잘못된 권한 설정 (p.73)
    4. 취약한 암호화 알고리즘 사용 (p.75)
    5. 암호화되지 않은 중요정보 (p.79)
    6. 하드코드된 중요정보 (p.83)
    7. 충분하지 않은 키 길이 사용 (p.86)
    8. 적절하지 않은 난수 값 사용 (p.89)
    9. 취약한 패스워드 허용 (p.91)
    10. 부적절한 전자서명 확인 (p.94)
    11. 부적절한 인증서 유효성 검증 (p.97)
    12. 사용자 하드디스크에 저장되는 쿠키를 통한 정보 노출 (p.100)
    13. 주석문 안에 포함된 시스템 주요정보 (p.103)
    14. 솔트 없이 일방향 해쉬 함수 사용 (p.105)
    15. 무결성 검사없는 코드 다운로드 (p.107)
    16. 반복된 인증시도 제한 기능 부재 (p.110)

  제3절 시간 및 상태 (p.113~114) — 1개 항목
    1. 종료되지 않는 반복문 또는 재귀 함수 (p.113)

  제4절 에러처리 (p.115~124) — 3개 항목
    1. 오류 메시지 정보노출 (p.115)
    2. 오류상황 대응 부재 (p.119)
    3. 부적절한 예외 처리 (p.122)

  제5절 코드오류 (p.125~132) — 3개 항목
    1. Null Pointer 역참조 (p.125)
    2. 부적절한 자원 해제 (p.127)
    3. 신뢰할 수 없는 데이터의 역직렬화 (p.130)

  제6절 캡슐화 (p.133~141) — 4개 항목
    1. 잘못된 세션에 의한 데이터 정보 노출 (p.133)
    2. 제거되지 않고 남은 디버그 코드 (p.136)
    3. Public 메소드로부터 반환된 Private 배열 (p.138)
    4. Private 배열에 Public 데이터 할당 (p.140)

  제7절 API 오용 (p.142~150) — 2개 항목
    1. DNS lookup에 의존한 보안결정 (p.142)
    2. 취약한 API 사용 (p.145)

PART 제3장 부록 (p.151~159)
  제1절 구현단계 보안약점 제거 기준 (p.152)
  제2절 용어정리 (p.155)
```

**총 항목 수: 42개** (13+16+1+3+3+4+2)

## CWE 매핑 (47개)

| CWE | 보안약점 | 카테고리 |
|-----|---------|---------|
| CWE-89 | SQL Injection | 입력데이터 |
| CWE-94 | Code Injection | 입력데이터 |
| CWE-95 | Eval Injection | 입력데이터 |
| CWE-22 | Path Traversal | 입력데이터 |
| CWE-99 | Resource Injection | 입력데이터 |
| CWE-79 | Cross-site Scripting (XSS) | 입력데이터 |
| CWE-78 | OS Command Injection | 입력데이터 |
| CWE-434 | Unrestricted File Upload | 입력데이터 |
| CWE-601 | Open Redirect | 입력데이터 |
| CWE-611 | XML External Entity (XXE) | 입력데이터 |
| CWE-643 | XPath Injection | 입력데이터 |
| CWE-90 | LDAP Injection | 입력데이터 |
| CWE-352 | CSRF | 입력데이터 |
| CWE-918 | SSRF | 입력데이터 |
| CWE-807 | Untrusted Input for Security Decision | 입력데이터 |
| CWE-306 | Missing Authentication | 보안기능 |
| CWE-285 | Improper Authorization | 보안기능 |
| CWE-732 | Incorrect Permission Assignment | 보안기능 |
| CWE-327 | Broken Crypto Algorithm | 보안기능 |
| CWE-312 | Cleartext Storage | 보안기능 |
| CWE-319 | Cleartext Transmission | 보안기능 |
| CWE-259 | Hard-coded Password | 보안기능 |
| CWE-321 | Hard-coded Crypto Key | 보안기능 |
| CWE-326 | Inadequate Key Size | 보안기능 |
| CWE-330 | Insufficient Randomness | 보안기능 |
| CWE-521 | Weak Password Requirements | 보안기능 |
| CWE-347 | Improper Signature Verification | 보안기능 |
| CWE-295 | Improper Certificate Validation | 보안기능 |
| CWE-539 | Sensitive Info in Persistent Cookie | 보안기능 |
| CWE-615 | Sensitive Info in Comments | 보안기능 |
| CWE-759 | Unsalted Hash | 보안기능 |
| CWE-494 | Download Without Integrity Check | 보안기능 |
| CWE-307 | Brute Force | 보안기능 |
| CWE-835 | Infinite Loop | 시간/상태 |
| CWE-674 | Uncontrolled Recursion | 시간/상태 |
| CWE-209 | Error Message Info Exposure | 에러처리 |
| CWE-390 | Error Condition Without Action | 에러처리 |
| CWE-754 | Improper Check for Exceptional Conditions | 에러처리 |
| CWE-476 | NULL Pointer Dereference | 코드오류 |
| CWE-404 | Improper Resource Shutdown | 코드오류 |
| CWE-502 | Deserialization of Untrusted Data | 코드오류 |
| CWE-488 | Data Leak Between Sessions | 캡슐화 |
| CWE-543 | Stale Session Variable | 캡슐화 |
| CWE-489 | Active Debug Code | 캡슐화 |
| CWE-495 | Private Array Returned from Public Method | 캡슐화 |
| CWE-496 | Public Data Assigned to Private Array | 캡슐화 |
| CWE-350 | Reliance on DNS Lookup | API 오용 |

## 특이사항

- 각 항목마다 **안전하지 않은 코드 예시** + **안전한 코드 예시** 쌍으로 구성
- Express.js, Sequelize, Mongoose, Node.js crypto 등 실무 프레임워크 코드 포함
- PART 3 부록에 **구현단계 보안약점 제거 기준** 매트릭스 포함 (7카테고리 × 항목별 점검 기준)
