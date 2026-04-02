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

## AI 보안 관련 (ref-003)

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 대규모 언어 모델 | Large Language Model | LLM | |
| 생성형 인공지능 | Generative AI | GenAI | |
| 예측형 인공지능 | Predictive AI | Pred AI | |
| 적대적 예제 | Adversarial Example | - | AI 공격 유형 |
| 회피 공격 | Evasion Attack | - | AI 공격 유형 |
| 오염 공격 | Poisoning Attack | - | 학습 데이터 오염 |
| 전도 공격 | Inversion Attack | - | 모델 역추론 |
| 모델 추출 | Model Extraction | - | AI 공격 유형 |
| AI 탈옥 | AI Jailbreak | - | 프롬프트 우회 공격 |
| 데이터 오염 | Data Poisoning | - | |
| 연합 학습 | Federated Learning | FL | |
| 검색 증강 생성 | Retrieval-Augmented Generation | RAG | |
| 인간 피드백 강화학습 | Reinforcement Learning from Human Feedback | RLHF | |
| 서비스형 기계학습 | Machine Learning as a Service | MLaaS | |
| AI 위험관리 프레임워크 | AI Risk Management Framework | AI RMF | NIST 표준 |
| 역할 기반 접근 제어 | Role-Based Access Control | RBAC | |
| 다중 인증 | Multi-Factor Authentication | MFA | |
| 보안 정보 이벤트 관리 | Security Information and Event Management | SIEM | |
| 보안 중심 설계 | Security by Design | - | |
| 최소 권한 원칙 | Least Privilege Principle | - | |

---

## 사용 규칙

1. **첫 등장**: 전체 형식 사용
   - 예: 주요정보통신기반시설(Critical Information Infrastructure, CII)
2. **이후 등장**: 한글 또는 약어 사용
   - 예: 주요정보통신기반시설 또는 CII
3. **새 용어 추가 시**: 이 파일에 등록 후 사용
4. **점검 항목 코드**: 본문에서 `U-01`, `W-02` 형식으로 직접 사용 가능

---

## 로봇 보안 관련 (ref-004, ref-005)

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 산업용 로봇 | Industrial Robot | - | ISO 8373 |
| 서비스 로봇 | Service Robot | - | ISO 8373 |
| 의료용 로봇 | Medical Robot | - | ISO 8373 |
| 보안 소프트웨어 개발 프레임워크 | Secure Software Development Framework | SSDF | NIST SP 800-218 |
| 산업제어시스템 보안 | Industrial Control System Security | IEC 62443 | 국제 표준 |
| 사이버 복원력 법 | Cyber Resilience Act | CRA | EU 규정 |
| 무선기기 지침 | Radio Equipment Directive | RED | EU 규정 |
| 소프트웨어 자재명세서 | Software Bill of Materials | SBoM | 공급망 보안 |

---

## 우주 보안 관련 (ref-006~010)

### 우주 아키텍처 용어

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 정지궤도 위성 | Geostationary Earth Orbit | GEO | ~36,000km |
| 중궤도 위성 | Middle Earth Orbit | MEO | 2,000~30,000km |
| 저궤도 위성 | Low Earth Orbit | LEO | 250~2,000km |
| 저궤도 군집위성 | LEO Constellation | - | 소형위성 집단 |
| 지상국 서비스 | Ground Station as a Service | GSaaS | 클라우드 기반 지상국 |
| 위성항법시스템 | Global Navigation Satellite System | GNSS | 위치/항법/시각 제공 |
| 도심항공모빌리티 | Urban Air Mobility | UAM | 저고도 항공운송 |
| 초소형 위성통신지구국 | Very Small Aperture Terminal | VSAT | 소형 위성 지상국 |
| 탑재체 | Payload | - | 위성 임무수행 부분 |
| 위성 본체 | Satellite Bus | - | 위성 구동 부분 |
| 온보드 컴퓨터 | On Board Computer | OBC | 위성 탑재 컴퓨터 |
| 우주 데이터시스템 자문위원회 | Consultative Committee for Space Data Systems | CCSDS | 우주 통신 표준 기구 |

### 우주 보안위협 용어

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 재밍 | Jamming | - | 방해전파 송출 |
| 스푸핑 | Spoofing | - | 위장 공격 |
| GPS 위장 교란 | GPS Spoofing | - | 위치정보 위변조 |
| 양자내성암호 | Post-Quantum Cryptography | PQC | 양자컴퓨터 내성 |
| 소프트웨어 정의 라디오 | Software Defined Radio | SDR | 전파분석 장치 |
| 일방향 전송장비 | One-way Transfer Device | - | 제어망 보호 |
| 무선침입방지시스템 | Wireless Intrusion Prevention System | WIPS | 무선AP 불법접속 방지 |
| 네트워크 접근통제 | Network Access Control | NAC | 인가 장치 접속 통제 |
| 정보유출방지 | Data Loss Prevention | DLP | 매체제어/유출차단 |
| 주파수 호핑 | Frequency Hopping | - | 안티재밍 기술 |
| 확산 스펙트럼 | Spread Spectrum | - | 안티재밍 기술 |

### 우주 보안 체크리스트 분야 코드

| 코드 | 분야명 | 영문 | 항목 수 |
|:----:|--------|------|:-------:|
| AC | 접근통제 | Access Control | 12 |
| IA | 식별 및 인증 | Identification & Authentication | 2 |
| SC | 시스템 및 통신 보안 | System & Communication Security | 7 |
| SI | 시스템 및 정보 무결성 | System & Information Integrity | 4 |
| SO | 시스템/서비스 운영관리 | System/Service Operations Management | 9 |
| IR | 사고 대응 | Incident Response | 2 |
| PS | 인원 보안 | Personnel Security | 2 |
| PE | 물리보안 | Physical & Environmental Security | 3 |
| RA | 위험평가 및 보안 평가 | Risk Assessment & Security Evaluation | 2 |
| SG | 보안 거버넌스 | Security Governance | 4 |
| CP | 비상 계획 | Contingency Planning | 2 |
| SM | 공급망 관리 | Supply Chain Management | 4 |

### 우주 보안 준거 기준

| 한글 | 영문 | 약어 | 비고 |
|------|------|------|------|
| 사이버보안 성숙도 모델 인증 | Cybersecurity Maturity Model Certification | CMMC | 미 국방부 공급망 인증 |
| 한국형 위험관리체계 | Korea Risk Management Framework | K-RMF | 국내 표준 |
| 네트워크 및 정보 보안 지침 | Network and Information Security Directive | NIS2 | EU 사이버보안 지침 |
| 사이버보안 프레임워크 | Cyber Security Framework | CSF | NIST 표준 |
| 위성 지상국 사이버보안 | Satellite Ground Segment Cybersecurity | NIST IR 8401 | NIST 지침 |
| 상업 위성 운영 사이버보안 | Commercial Satellite Operations Cybersecurity | NIST IR 8270 | NIST 지침 |
| 우주 시스템 위협 분석 | Space Threat Landscape | - | ENISA 보고서 |

---

## 사용 규칙

1. **첫 등장**: 전체 형식 사용
   - 예: 주요정보통신기반시설(Critical Information Infrastructure, CII)
2. **이후 등장**: 한글 또는 약어 사용
   - 예: 주요정보통신기반시설 또는 CII
3. **새 용어 추가 시**: 이 파일에 등록 후 사용
4. **점검 항목 코드**: 본문에서 `U-01`, `W-02`, `AC-01` 형식으로 직접 사용 가능

---

*최종 업데이트: 2026-04-02 (ref-006~010 우주 보안 용어 추가)*
