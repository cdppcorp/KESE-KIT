# Web Application 취약점 분석·평가 항목

> KISA 주요정보통신기반시설 기술적 취약점 분석·평가 방법 상세가이드 (2026)
> 대상: 웹 애플리케이션 소스 코드 및 설정

## 1. 입력값 검증 (8항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| CI | Command Injection | 상 |
| SI | SQL Injection | 상 |
| XS | Cross-Site Scripting (XSS) | 상 |
| CF | Cross-Site Request Forgery (CSRF) | 상 |
| SF | Server-Side Request Forgery (SSRF) | 상 |
| FU | File Upload 취약점 | 상 |
| FD | File Download 취약점 | 상 |
| DI | 디렉터리 인덱싱 | 중 |

## 2. 인증/세션 관리 (6항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| BF | Brute Force 공격 | 상 |
| IA | 불충분한 인증 (Insufficient Authentication) | 상 |
| PR | 비밀번호 복구 취약점 | 중 |
| IS | 불충분한 세션 관리 | 상 |
| CC | 세션 고정 (Credential/Session Prediction) | 상 |
| SN | 세션 만료 미설정 | 중 |

## 3. 접근제어 (4항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| IN | 불충분한 인가 (Insufficient Authorization) | 상 |
| PV | 경로 조작 (Path Traversal) | 상 |
| AE | 관리자 페이지 노출 | 상 |
| WM | HTTP Method 제한 미설정 | 중 |

## 4. 정보노출 (3항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| EP | 에러 페이지를 통한 정보 노출 | 중 |
| IL | 불필요한 정보 노출 | 중 |
| AU | 부적절한 감사 로깅 | 중 |

## 통계: 총 21항목 (상 14, 중 7, 하 0)
