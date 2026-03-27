# Glossary — 용어집

> KESE KIT 프로젝트 용어 통일을 위한 글로서리
> KESE KIT: Korea Enhanced Security Evaluation - KISA Infrastructure Toolkit
> 형식: 한글(영문, 약어)

---

## 기관/조직

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 한국인터넷진흥원 | Korea Internet & Security Agency | KISA | 주무기관 |
| 과학기술정보통신부 | Ministry of Science and ICT | MSIT | |
| 국가정보원 | National Intelligence Service | NIS | |
| 관리기관 | Management Agency | - | CII 관리 주체 |

---

## 법령/제도

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 정보통신기반보호법 | Act on the Protection of Information and Communications Infrastructure | - | 제9조: 취약점 분석·평가 |
| 주요정보통신기반시설 | Critical Information Infrastructure | CII | 핵심 대상 |
| 취약점 분석·평가 | Vulnerability Analysis and Assessment | VAA | 연 1회 의무 |
| 정보보호관리체계 | Information Security Management System | ISMS | |
| 개인정보보호관리체계 | Privacy Information Management System | PIMS | |
| ISMS-P | ISMS-Personal Information | ISMS-P | ISMS + PIMS 통합 |

---

## 점검 항목 코드 체계

| 코드 접두어 | 대상 시스템 | 예시 |
|:-----------:|-------------|------|
| U | Unix/Linux 서버 | U-01 ~ U-68 |
| W | Windows 서버 | W-01 ~ W-73 |
| WS | 웹 서비스 (Apache, Nginx) | WS-01 ~ WS-47 |
| S | 보안 장비 (방화벽, IDS 등) | S-01 ~ S-19 |
| N | 네트워크 장비 | N-01 ~ N-40 |
| C | 제어시스템 (OT) | C-01 ~ C-45 |
| PC | PC/단말기 | PC-01 ~ PC-18 |
| D | DBMS | D-01 ~ D-32 |
| M | 이동통신 | M-01 ~ M-02 |
| V | 가상화 장비 | V-01 ~ V-36 |
| CL | 클라우드 | CL-01 ~ CL-14 |
| A | 관리적 취약점 | A-1 ~ A-127 |
| B | 물리적 취약점 | B-1 ~ B-9 |

---

## 기술 용어

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 취약점 | Vulnerability | - | |
| 위협 | Threat | - | |
| 위험 | Risk | - | |
| 패치 | Patch | - | |
| 보안 설정 | Security Configuration | - | |
| 접근 제어 | Access Control | - | |
| 인증 | Authentication | - | |
| 권한 | Authorization | - | |
| 암호화 | Encryption | - | |
| 로그 | Log | - | |
| 감사 | Audit | - | |
| 계정 잠금 | Account Lockout | - | |
| 세션 타임아웃 | Session Timeout | - | |
| 비밀번호 정책 | Password Policy | - | |

---

## 서버/인프라

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 운영체제 | Operating System | OS | |
| 웹 서버 | Web Server | - | Apache, Nginx 등 |
| 데이터베이스 | Database | DB | |
| 방화벽 | Firewall | FW | |
| 침입탐지시스템 | Intrusion Detection System | IDS | |
| 침입방지시스템 | Intrusion Prevention System | IPS | |
| 웹 방화벽 | Web Application Firewall | WAF | |
| 가상사설망 | Virtual Private Network | VPN | |
| 네트워크 분리 | Network Segregation | 망분리 | |

---

## Unix/Linux 관련

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 루트 계정 | root account | root | 최고 권한 |
| 사용자 식별자 | User Identifier | UID | |
| 그룹 식별자 | Group Identifier | GID | |
| 접근 권한 | File Permission | - | rwx |
| SUID | Set User ID | SUID | |
| SGID | Set Group ID | SGID | |
| 스티키 비트 | Sticky Bit | - | |
| 크론 | Cron | - | 작업 스케줄러 |
| 쉐도우 파일 | Shadow File | - | /etc/shadow |

---

## 웹 보안 관련

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| SQL 삽입 | SQL Injection | SQLi | |
| 크로스사이트 스크립팅 | Cross-Site Scripting | XSS | |
| 크로스사이트 요청 위조 | Cross-Site Request Forgery | CSRF | |
| 디렉터리 리스팅 | Directory Listing | - | |
| 파일 업로드 취약점 | File Upload Vulnerability | - | |
| 세션 고정 | Session Fixation | - | |
| 세션 하이재킹 | Session Hijacking | - | |

---

## 네트워크 관련

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 간이 네트워크 관리 프로토콜 | Simple Network Management Protocol | SNMP | |
| 커뮤니티 스트링 | Community String | - | SNMP 인증 |
| 텔넷 | Telnet | - | 비암호화 원격접속 |
| 보안 셸 | Secure Shell | SSH | 암호화 원격접속 |
| 파일 전송 프로토콜 | File Transfer Protocol | FTP | |
| 보안 파일 전송 프로토콜 | Secure FTP | SFTP | |
| 접근 제어 목록 | Access Control List | ACL | |

---

## 평가 항목 분류

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 기술적 취약점 | Technical Vulnerability | - | ~424개 항목 |
| 관리적 취약점 | Administrative Vulnerability | - | 127개 항목 |
| 물리적 취약점 | Physical Vulnerability | - | 9개 항목 |

---

## 판정 기준

| 한글 | 설명 |
|------|------|
| 양호 | 점검 항목에 명확히 부합 |
| 부분 이행 | 일부 만족, 개선 필요 |
| 취약 | 점검 항목에 부합하지 못함 |

---

## 중요도 분류

| 등급 | 설명 |
|:----:|------|
| 상 | 침해 시 심각한 영향, 즉시 조치 필요 |
| 중 | 침해 시 중간 수준 영향 |
| 하 | 침해 시 낮은 영향 |

---

## 사용 규칙

1. **첫 등장**: 전체 형식 사용
   - 예: 주요정보통신기반시설(Critical Information Infrastructure, CII)
2. **이후 등장**: 한글 또는 약어 사용
   - 예: 주요정보통신기반시설 또는 CII
3. **새 용어 추가 시**: 이 파일에 등록 후 사용
4. **점검 항목 코드**: 본문에서 `U-01`, `W-02` 형식으로 직접 사용 가능

---

*분석 완료 후 업데이트됨: 2026-03-27*
