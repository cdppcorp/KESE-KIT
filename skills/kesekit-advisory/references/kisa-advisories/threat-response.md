# KISA Threat-Response Advisory Checklist (2025-01 ~ 2026-11)

> Source: KISA Boho-nara (보호나라, KrCERT/CC) security notices of the types 보안 조치·강화 권고 (security action/hardening advisory) / 취약점 조치 권고 (vulnerability remediation advisory) / 주의 권고 (caution advisory) / 기타 (other). Patch-type '보안 업데이트 권고' (security update advisory) notices are handled by an advisories.json lookup.
>
> Scope: 91 non-patch notices out of the 519 rows in 목록.csv (18 security action/hardening, 7 vulnerability remediation, 63 caution, 3 other). Five pinned notices carry no number and are shown as `공지` (pinned notice).

## How to use
- Pick only the sections that match the environment under review: A servers, B web, C development and CI/CD, D network devices and NAS, E products in inventory, F work endpoints and accounts, G staff awareness material.
- Each TR item is one check. Rate each as **Pass / Partial / Vulnerable / N/A** (N/A when the product or environment is not present). The Korean terms are 양호 / 부분이행 / 취약 / 해당없음.
- Commands are copied exactly as they appear in the notice or attachment. Following KISA's caution, confirm company policy and system impact before running them on production systems. "(per attachment)" marks facts taken from an attached PDF.
- IOCs (hashes, IPs, domains) go stale, so they are not reproduced here; only the attachment file name and IOC counts are given.

---

## A. Server and system compromise response

### TR-01 BPFDoor backdoor infection check
- **Notice**: 2025-05-12 · #2210 · Security action/hardening advisory — BPFDoor 악성코드 점검 가이드 배포 (BPFDoor malware inspection guide released) / Related IOC notices: 2025-04-25 · #2193, 2025-05-03 · #2198 · Caution advisory — 최근 해킹공격에 악용된 악성코드(, IP 등) 위협정보 공유 및 주의 안내 (threat intelligence on malware [and IPs] used in recent attacks)
- **Scope**: Linux servers. #2198 covers Linux attacks found while responding to a telecom-carrier breach.
- **Background**: A backdoor that opens no port; it waits for a magic packet via a BPF filter and then connects a shell. The 4 hash values in the guide's YARA rule metadata are the same file hashes shared in #2193.
- **Checks** (root/sudo required, per attachment):
  - [ ] 0-byte `*.pid`/`*.lock` files with permission 644 under `/var/run/`
    ```
    $ sudo ls -l /var/run/*.pid | awk '$5 == 0 {print $9}'
    $ sudo ls -l /var/run/*.lock | awk '$5 == 0 {print $9}'
    ```
  - [ ] Autorun statements in `/etc/sysconfig/` (of the form `[ -f “악성코드 경로” ] && “악성코드 경로”`, i.e. "malware path")
    ```
    $ sudo grep -Er '\[\s*-f\s+/[^]]+\]\s*&&\s*/' /etc/sysconfig/
    ```
  - [ ] Magic numbers in BPF filters (requires Kernel 3.2+ and iproute2 4.0+; on CentOS 6.x and earlier use the RAW-socket check instead)
    ```
    $ sudo ss -0pb | grep -E "21139|29269|960051513|36204|40783"
    ```
  - [ ] Processes using RAW sockets and their executable path (a file deleted but still running in memory shows as e.g. `/dev/shm/kdmtmpflush (deleted)`)
    ```
    $ sudo lsof 2>/dev/null | grep -E "IP type=SOCK_RAW|IP type=SOCK_DGRAM" | awk '{print $2}' | sort -u | xargs -r ps -fp
    $ sudo ls -l /proc/<PID>/exe
    ```
  - [ ] Processes holding all of HOME=/tmp, HISTFILE=/dev/null, MYSQL_HISTFILE=/dev/null ([붙임2] / Annex 2 `bpfdoor_env.sh`)
  - [ ] Use of ports 42391–43390 and 8000 (`sudo netstat -tulpn`); whether disguised process names (/usr/sbin/abrtd, /sbin/udevd, cmathreshd, /sbin/sgaSolAgent, /usr/sbin/atd, pickup) match their actual executable path
  - [ ] Triage suspicious files with strings, then confirm with [붙임3] / Annex 3 `bpfdoor.yar` (ELF_BPFDoor, ELF_BPFDoor_Controller). Running YARA over a whole directory can cause outages, so copy the files out and scan the copies.
  - [ ] Network magic sequences (UDP·ICMP 0x7255, 0x9F4F / TCP 0x5293, 0x39393939, 0x8D6C) and the marker `9999` in HTTP POST URIs
- **Action**: If traces are found, report the incident to Boho-nara. A rule built on a single magic sequence can false-positive, so review and customise it internally. Some step cross-references inside the guide are inconsistent ("(6)/(7)" and "(8)/(9)" are both used).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71754 · Attachment: 250512_KISA_BPFDoor_악성코드_점검_가이드.pdf (2 scripts, YARA rules) / #2193 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71726 (IOCs: 1 IP, 4 files) / #2198 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71735 (IOCs: 8 files) · Attachment: none

### TR-02 Linux kernel rootkit check
- **Notice**: 2025-12-11 · #2322 · Security action/hardening advisory — 리눅스 커널 루트킷 점검 가이드 배포 (Linux kernel rootkit inspection guide released)
- **Scope**: Red Hat-family Linux (RHEL, CentOS, etc.), file systems XFS/EXT2/EXT3/EXT4/BTRFS. Unix systems are not supported (per attachment).
- **Background**: A kernel rootkit hides boot/service scripts and a backdoor so that ordinary user-level commands cannot see them. Example symptoms are a hidden rootkit (was-patch) and a hidden backdoor (was_sys_relay) (per attachment).
- **Checks** (per attachment):
  - [ ] Run KISA's official scanner (attached ZIP) as root with execute permission. On POSIX environments use `rootkit_detect_scanner_posix_v1.0.sh`.
    ```
    ./rootkit_detect_scanner_v1.0.sh
    ```
  - [ ] Interpret the result: normal `[OK] No Hidden Entry | Rootkit Not Found | Backdoor Not Found` / abnormal `[ALERT] Hidden Entry Found! | Suspicious Rootkit Found! | Backdoor Found!` → if abnormal, investigate the suspicious files it prints.
  - [ ] The scanned paths are `/etc/systemd/system/`, `/etc/init.d/`, `/etc/rc2.d/`, `/etc/rc3.d/`, `/etc/rc5.d/`. If the company has other autorun paths, edit the script before running it.
  - [ ] How it works: it takes the difference between the file list read from inodes/data blocks and the `ls` output to find hidden scripts, then prints the rootkit and backdoor paths, hashes and processes to the terminal and `*.log`.
  - [ ] For a broader review use KISA's Linux hacking-diagnosis tool, and put antivirus/EDR and monitoring in place.
- **Action**: If compromise is confirmed, report it to Boho-nara (https://www.boho.or.kr/kr/report/list.do?menuNo=205034).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71917 · Attachments: 20251212_리눅스_커널_루트킷_점검_가이드.pdf (v1.0-rev1, BTRFS added 2025.12.12), rootkit_detect_scanner_v1.0-rev1.zip (official KISA tool; not extracted or run while preparing this document)

### TR-03 Ransomware prevention hardening (recurring notice, 5 editions)
- **Notice**: Security action/hardening advisory — 2025-02-26 · #2149 「랜섬웨어 악성코드 감염 예방을 위한 보안강화 권고」 / 2025-06-11 · #2222, 2025-08-14 · #2268, 2025-12-06 · #2319 「랜섬웨어 악성코드 감염피해 예방을 위한 보안강화 권고」 / 2026-02-04 · #2348 「랜섬웨어 감염 피해 예방을 위한 보안 강화 권고」 (all: hardening advisory to prevent ransomware infection/damage)
- **Scope**: Corporate servers, PCs, NAS, Active Directory, mail systems
- **What changed between editions**: #2149 targets manufacturing and covers entry via maintenance vendors' remote access, brute-forcing the MS-SQL `sa` account, web vulnerabilities plus privilege escalation, double extortion, and company-wide spread through a central management server. #2222 splits cases into server/PC/NAS, adds AD and NAS sections, and adds port 22 to the default ports. #2268 reflects growing groupware and NAS damage and adds an item to minimise software and internet use on admin PCs. #2319 adds cases exploiting React Server Components vulnerabilities (CVE-2025-55182, CVE-2025-66478); its attached PDF matches the body. #2348 stresses the medical, education and ICT sectors and focused monitoring of EMR and PACS, adds cases of unpatched VPN appliances and VMware, expands the remote-port examples to SSH 22, MS-SQL 1433, MySQL 3306, RDP 3389, VNC 5900, TeamViewer 5938, and adds a new "critical-system administrator security check" (isolate or update end-of-support OS/apps, least privilege).
- **Checks**:
  - [ ] Externally exposed assets (DB, NAS, routers, test/idle servers) are inventoried and unnecessary connections blocked; check whether people who access critical systems have installed remote-control software on personal devices
  - [ ] Avoid exposing default service ports (22, 1433, 3389, etc.). Where external access is needed, apply IP/device restrictions, MFA and per-server access control, and review logs periodically (overseas/night/weekend IPs, unusual traffic volume). Allow maintenance-vendor connections only when needed
  - [ ] Accounts: change default admin passwords, disable unused default accounts, use complex passwords and change them regularly, add a second factor, never store remote-access credentials in plaintext
  - [ ] Backups: regular backups to storage separated from the network (many victims kept backups on the same storage and had them encrypted too); separately back up data kept in the cloud
  - [ ] Mail: show file extensions (File Explorer > View > 'File name extensions'), open attachments in an isolated environment, use a mail security solution. Admins check for unauthorised accounts and abnormal logins, and change credentials that were sent in plaintext
  - [ ] AD: separate privileged admin accounts and rotate their credentials, protect admin endpoints and control access paths, centrally log and monitor privileged authentication and abnormal service installation
  - [ ] NAS: change the default password, enable auto-update, block direct internet access (operate inside the internal network)
  - [ ] Other: automatic OS/software updates, up-to-date antivirus, a recovery plan and drills
- **Action**: If infected, report the incident to Boho-nara. References are Boho-nara reports/guides 1505 (Ransomware Response Guide, 2023 revision), 1466 (backup guide), 1515 (NAS security guide), 1383 and 1379 (AD case study and technical report).
- **Source**: #2149 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71666 · #2222 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71771 · #2268 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71840 · #2319 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71914 · #2348 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71960 · Attachment: only #2319 has 251206_랜섬웨어 사고 증가에 따른 주의 공지.pdf; the others have none

### TR-04 Eight data-backup security rules for ransomware response
- **Notice**: 2025-07-17 · #2244 · Security action/hardening advisory — 랜섬웨어 대응을 위한 데이터백업 8대 보안 수칙 (8 data-backup security rules for ransomware response)
- **Scope**: Backup servers, backup storage, backup software
- **Background**: More incidents now encrypt the backups as well. The rules are cited again in #2268's references and as Figure 2 of #2541.
- **Checks** ([Important] is the original marking):
  - [ ] ① [Important] Back up to an offsite location separated from the service network (cloud, external storage, or offline).
  - [ ] ② 3-2-1 strategy: 3 copies, on 2 different media, 1 offsite
  - [ ] ③ [Important] Least privilege on backup storage; block access by anyone other than backup staff (multi-factor such as OTP where possible).
  - [ ] ④ [Important] Monitoring that can check backup server and data integrity, such as antivirus or EDR.
  - [ ] ⑤ [Important] At least one recovery drill a year to prove recovery actually works.
  - [ ] ⑥ [Important] Patch backup servers and software promptly.
  - [ ] ⑦ Verify integrity before backing up so an infected source does not overwrite good backups.
  - [ ] ⑧ Automate daily/weekly/monthly backups.
- **Action**: Close any rule that is not met.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71809 · Attachment: 랜섬웨어 대응을 위한 데이터백업 8대 보안수칙.pdf (one-page infographic)

### TR-05 Midnight (Endpoint) ransomware spread by email
- **Notice**: 2026-04-16 · #2405 · Other — 국내 중소기업 대상 신규 랜섬웨어 범죄 확산에 따른 보안 권고문 (advisory on new ransomware targeting Korean SMEs; co-authored with the Korean National Police Agency)
- **Scope**: SME mail users, mail and server administrators
- **Background**: Damage from Midnight (Endpoint) ransomware delivered by malicious email has surged. [Case 1] a victim ran an attachment disguised as an official letter, résumé or quotation. [Case 2] mail impersonating an IT service provider (infrastructure design, service installation guide) was used to take over privileges, break into servers and install ransomware. The attached PDF shows sample emails disguised as a job application, a consulting inquiry, an infrastructure build request and a security-guideline distribution (per attachment).
- **Checks**:
  - [ ] Verify the sender exactly and do not open unknown mail or attachments. Open attachments in a virtualised, isolated environment.
  - [ ] Show file extensions and do not open executables (.exe, etc.) disguised with document icons. Block malicious mail with a mail security solution.
  - [ ] Mail admins: check for unauthorised account registration and abnormal logins; review and change system credentials that were sent in plaintext; forbid sending them in plaintext.
  - [ ] Check external access, accounts and backups with the same items as TR-03.
- **Action**: If infected, report the incident to Boho-nara.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72028 · Attachment: 260416_[보안공지]_국내 중소기업 대상 신규 랜섬웨어 범죄 확산에 따른 보안 권고문.pdf

### TR-06 Request to strengthen corporate security after recent incidents (same title twice, different content)
- **Notice**: Security action/hardening advisory 「최근 침해사고 증가에 따른 기업보안 강화 요청」 (request to strengthen corporate security as incidents rise) — 2026-01-06 · #2332, 2026-06-05 · #2456
- **Scope**: #2332 covers web servers and admin pages; #2456 covers cloud IAM/Access Keys and developer endpoints.
- **Background**: Same title, different content. #2332: an unidentified hacker group kept attacking Korean websites and stealing data; signs of personal-data leaks were found at non-profit associations, universities and small hospitals (Jan 2026). #2456: developer/operator endpoints were infected, cloud credentials were stolen from code repositories, config files and logs, and admin-level rights (e.g. S3 read/write) were used to browse assets and exfiltrate backup data.
- **Checks (#2332)**:
  - [ ] Latest OS and application patches, especially Apache Tomcat-based Java solutions (Oracle WebLogic, Atlassian Confluence, Apache Struts 2, etc.) and GNU Bash
  - [ ] Web admin password complexity and regular change, two-factor login, IP restriction on admin pages, a dedicated admin endpoint
  - [ ] WAF/IPS detecting and blocking web attacks; focused review of file upload (upload type validation, execute permission on upload folders) and admin login pages; SQL injection countermeasures (input validation) and secure coding
  - [ ] Compromise traces: abnormal admin login history, abnormal file creation, abnormal DB queries
- **Checks (#2456)**:
  - [ ] Immediately restrict/disable any Access Key suspected of leaking and replace it with a new key.
  - [ ] Re-review IAM policies against least privilege; trace abnormal API calls, asset listing and data access in cloud logs; preserve evidence such as CloudTrail without modification.
  - [ ] Prevention: rotate keys and shorten their lifetime, never hard-code keys in source, config or public repos (use environment variables or Secrets Manager), use STS/IAM Roles instead of long-lived keys, retire unused keys and use MFA, run threat detection and anomaly monitoring, avoid installing utilities/dev tools of unknown origin (→ TR-21)
- **Action**: Report to KISA without delay once an incident is known. SMEs can apply for Boho-nara's free "SME website security hardening" check and "내 서버 돌보미" (My Server Care) service (#2332).
- **Source**: #2332 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71932 · #2456 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72086 · Attachment: none

### TR-07 Holiday-period security checks and monitoring (Chuseok 2025 and 2026)
- **Notice**: 2025-10-02 · #2292 · Caution advisory — 추석연휴기간 사이버 공격(랜섬웨어, 스미싱 등) 대비 주의사항 안내 (precautions against cyber attacks [ransomware, smishing, etc.] during the Chuseok holiday) / 2026-09-17 · #2541 · Security action/hardening advisory — 추석 명절 대비 기업 보안점검·모니터링 강화 (strengthen corporate security checks and monitoring ahead of Chuseok)
- **Scope**: Corporate and institutional security staff (before and during the holiday)
- **Background**: Incidents are expected to rise while security staff are away. #2292 republishes the #2268 ransomware advisory as-is and adds smishing tips for the public (see table G). #2541 is reorganised into a table of five areas, each with "pre-holiday check / during-holiday monitoring".
- **Checks (#2541)**:
  - [ ] API — before: verify authentication and access rights, block unused APIs, rate-limit / during: repeated authentication failures, sequential data lookups, spikes in call or response volume
  - [ ] Cloud access keys — before: check for key exposure in code, config, collaboration tools and repo history; least privilege; block exposed keys; retire unused keys / during: abnormal access, account or permission changes, bulk downloads, log collection stopping
  - [ ] Ransomware — before: confirm antivirus/EDR is working, keep backups separated, test restores / during: mass file changes or encryption, backup deletion, security software being stopped
  - [ ] Admin endpoints and accounts — before: separate admin accounts, MFA, review allowed access targets and paths / during: abnormal admin access, new privileged accounts, access-control policy changes
  - [ ] Externally exposed services — before: confirm services and versions, block unnecessary external access, apply security updates (move end-of-support software to a supported version) / during: spikes in SSH login failures, suspicious files created on web servers, bulk DB queries
  - [ ] Response readiness: log collection and alert delivery verified; emergency contacts for staff, deputies and maintenance vendors up to date; first-response owner assigned; unresolved alerts shared at handover
- **Action**: If compromise is suspected, isolate the system from the network and block use of potentially leaked credentials. Preserve logs and other evidence and report.
- **Source**: #2292 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71881 · #2541 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72189 · Attachment: #2292 참고1. 안드로이드 및 iOS 휴대폰 소프트웨어 업데이트 방법.hwpx (how to update Android and iOS phones; HWPX, not opened), #2541 none

### TR-08 Hardening against DDoS and credential stuffing
- **Notice**: 2025-03-11 · #2154 · Security action/hardening advisory — 사이버 위협 증가에 따른 보안강화 권고 (hardening advisory in response to rising cyber threats)
- **Scope**: Key corporate and institutional systems and public-facing services
- **Background**: Credential stuffing leaked personal data from a retailer and a job platform, and an international hacker group announced and carried out DDoS attacks on government agencies and mobile carriers.
- **Checks**:
  - [ ] Systems and security appliances run stably and have appropriate security policies applied
  - [ ] Unnecessary internet exposure checked and blocked in preparation for external scanning
  - [ ] Infrastructure, OS and software vulnerabilities checked and patched; status of backups of important data
  - [ ] Subscription to a DDoS protection service: small businesses and SMEs can use KISA's free DDoS protection service (antiddos@krcert.or.kr, 02-405-4769); others can use carriers' or other private services
  - [ ] Staff guidance on hacking mail and smishing, latest updates for the OS and document software (hwp, doc), antivirus scans
- **Action**: Report incidents to the KISA situation room (02-405-4911, certgen@krcert.or.kr) or Boho-nara. Report personal-data leaks to the Personal Information Protection portal (privacy.go.kr).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71677 · Attachment: none

### TR-09 Responding to hacktivist threats driven by geopolitical tension
- **Notice**: 2026-03-20 · #2385 · Security action/hardening advisory — 중동발 지정학적 긴장고조에 따른 사이버 위협 대응 강화 권고 (strengthen response to cyber threats from Middle East geopolitical tension)
- **Scope**: Government, defence-industry and corporate IT infrastructure
- **Background**: Hacktivist DDoS (RipperSec attempted attacks on Korean defence-industry and government targets), combined attacks that also destroy and leak data (Handala), automated logins used to reach internal mail and file servers, and ransomware double extortion (Everest, LockBit Black).
- **Checks**:
  - [ ] Monitoring of key systems and admin (developer) endpoints; patching of external IT infrastructure and checks for abnormal account creation; ACLs (HOST, NETWORK) re-verified
  - [ ] Overseas branches' IT infrastructure checked to the same level as in Korea; focused monitoring of central management systems (asset, account, antivirus)
  - [ ] Supply-chain software and partner endpoints checked (including open source and external libraries); access control on collaboration servers and services (e.g. SharePoint); admin and dev tools downloaded only from official sites
  - [ ] Web vulnerability checks and web-shell detection (KISA hacking-diagnosis tools, web vulnerability check service)
  - [ ] 3-2-1 backup re-checked and actual restore confirmed
  - [ ] DDoS: cooperation with carriers (blocking abnormal IPs, traffic diversion); consider the KISA cyber shelter (사이버대피소) service
  - [ ] MFA against credential stuffing; no reused passwords and regular changes
  - [ ] Staff: confirm by phone with internal security staff whenever asked to change accounts, install apps or open URLs; block any request to install remote-control apps at once. Security training for IT admins and developers
- **Action**: Report incidents to Boho-nara as a hacking incident.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72005 · Attachment: none

### TR-10 Emergency patching based on the US CISA KEV catalog
- **Notice**: 2025-01-09 · #2116 · Other — 美 CISA 발표 주요 Exploit 정보공유(Update. 2025-01-07) (sharing key exploit information published by US CISA)
- **Scope**: All IT assets
- **Background**: The body only links to the list of frequently exploited vulnerabilities; the list itself is not in the notice.
- **Checks**:
  - [ ] Software versions in use have been compared against the CISA KEV catalog (https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- **Action**: Apply emergency patches where a vulnerable version is in use (as stated in the notice).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71622 · Attachment: none

---

## B. Web and applications

### TR-11 PHP2Shell (CVE-2026-109618, CVE-2026-109619) corporate response rules
- **Notice**: 2026-10-22 · 공지 (pinned) · Vulnerability remediation advisory — PHP 보안취약점(PHP2Shell) 관련 기업 보안 대응 수칙 (corporate response rules for the PHP2Shell vulnerability)
- **Scope**: Web servers running PHP, appliances and solutions with embedded PHP, container images (where a hosting provider or vendor manages PHP, confirm with them)
- **Background**: Unauthenticated remote command execution (CVSS 9.2). Details leaked before the patch and attack attempts have been reported. Passwords, tokens and API keys in server memory can also leak.
- **Checks**:
  - [ ] Identify PHP use and version based on servers actually running, not the asset list. Include outsourced, abandoned, event and test servers, admin pages, appliances and Windows installers with embedded PHP, and external container images.
  - [ ] Apply the fixed versions PHP 8.5.12, 8.4.27, 8.3.36, 8.2.35 or later (including Linux-distribution and vendor updates), internet-facing servers first.
  - [ ] After updating, restart every service that runs PHP, such as PHP-FPM, Apache mod_php, php-cgi, FrankenPHP and LiteSpeed (otherwise it stays vulnerable). Redeploy containers from a new image.
  - [ ] Confirm the PHP version the web service actually uses. It can differ from `php -v`, so check each install if there are several. Distribution packages may keep the same version number after patching, so check the package changelog for the CVE fix.
  - [ ] Move PHP 8.1 and earlier to a supported version. PHP 8.2 security support also ends on 2026.12.31, so 8.3 or later is recommended. Until then, apply distribution/LTS-vendor patches or the PHP security team's source patches for 7.4, 8.0 and 8.1 as a stopgap.
  - [ ] If you cannot update right away, limit request size in front of PHP (WAF, web server, proxy), including requests with no size information. Block multipart upload requests where uploads are not needed and make sure WAF rules are current. Apply PHP's official temporary settings, then restart all PHP processes.
    ```
    session.upload_progress.enabled = 0
    memory_limit = -1
    ```
    Set `memory_limit` as an admin setting the application cannot change (e.g. `php_admin_value` in the PHP-FPM pool). Lower `post_max_size` to about 8M if uploads are not needed or 32M if they are, and keep `upload_max_filesize` below it. On PHP 8.5 also add `fatal_error_backtraces = 0`.
  - [ ] Log review (at least from 10.20.): unusually large requests followed by repeated HTTP 500, unexplained PHP restarts, segfaults or out-of-memory errors, signs of the web server running sh, bash or download tools, new PHP files (web shells) in web, upload or temp folders, external scripts added to the site or payment pages, new connections from the web server to unknown external addresses
  - [ ] Servers exposed to the internet before the update: rotate DB passwords, external integration keys and admin passwords (mandatory if compromise traces are found).
- **Action**: On compromise: ① do not shut down or restart the server; block external access only ② report to Boho-nara ③ preserve logs, the running-process list and network connections (before any restart) ④ update and restart, remove web shells, rotate credentials. Do not run PoCs of unknown origin; judge exposure from versions and logs. The related patch notice is 2026-10-21 #2574 (advisories.json).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72230 · Attachment: none

### TR-12 PHP session-handling remote code execution (CVE-2026-115560) temporary mitigation
- **Notice**: 2026-10-24 · #2581 · Vulnerability remediation advisory — PHP 신규 취약점(CVE-2026-115560) 임시 조치 권고 (temporary mitigation for a new PHP vulnerability)
- **Scope**: PHP. At the time of the notice the vendor had not disclosed affected versions and no fixed version had been released (planned for the next regular update).
- **Background**: Remote code execution in session handling. The updates released on 10.21. (8.5.12, 8.4.27, 8.3.36, 8.2.35) do not fix it.
- **Checks** (affected only if all three conditions hold):
  - [ ] `session.serialize_handler` in the config file is `php_binary` or `php_serialize`
  - [ ] Code calls `ini_set()` to change that value to `php` before calling `session_start()`
  - [ ] `session.upload_progress.enabled` is on (the default)
- **Action**: Until a security update is released, set `session.upload_progress.enabled=0` in php.ini, the PHP-FPM pool, etc., and restart all PHP workers. If you already applied this as the TR-11 temporary measure, nothing more is needed. The notice is due to be updated, so re-check it for the latest information.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72237 · Attachment: none

### TR-13 Web- and API-focused corporate hardening
- **Notice**: 2026-10-03 · 공지 (pinned) · Security action/hardening advisory — 최근 사이버공격 대비 기업 보안강화 권고 (corporate hardening against recent cyber attacks)
- **Scope**: Web/APIs, accounts and credentials, servers and internal networks (financial sector and private companies)
- **Background**: After a string of incidents at financial and private companies, KISA advises checking web/API vulnerabilities and credential exposure first, since these are most often used for initial access.
- **Checks**:
  - [ ] Exposed assets: inventory domains, subdomains, IPs, web and remote-access services; clean up assets with no owner and test or unused services. Allow admin pages, DBs and management access only from designated paths. Check whether config files, repository metadata, backup files or detailed error messages are exposed on public web paths.
  - [ ] Web/API: verify permission on the server for every request and block admin functions for ordinary users. Using a test account, change document or user IDs in requests to see whether other users' data can be read or modified. Use parameterised queries. Restrict features that fetch external URLs to allowed destinations and protocols, and block access to internal management services and cloud credential endpoints. Limit call counts, query periods, returned records and download volume per account or token.
  - [ ] Accounts and credentials: MFA for admin and remote access, separate admin and regular accounts, check code, repository history, config and collaboration tools for exposed secrets. Revoke and replace exposed secrets and investigate their usage history. Give integration accounts least privilege and short-lived credentials, and always delete external maintenance accounts after use.
  - [ ] Servers and internal network: remove admin rights from the web/app runtime account; restrict web-server-to-internal traffic and unnecessary outbound internet; block server-side script execution in upload paths; check web paths for unauthorised files; EDR alerts for abnormal command execution by web-server processes and internal connection attempts
  - [ ] Leak detection: minimise query/download/export rights; time-sync and correlate web/API, authentication, server, DB and cloud logs; never write raw passwords or tokens to logs; combine short-window detection with long-window cumulative analysis
  - [ ] Monitoring: sequential lookups with changing identifiers, lookups via another path after an access denial, attempts to fetch config or backup files, credential use from new environments, log deletion or collection stopping
- **Action**: If compromise is suspected, isolate the system quickly, preserve logs and evidence, then report to Boho-nara or call 118.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72207 · Attachment: none

### TR-14 HTTP/2 MadeYouReset denial of service
- **Notice**: 2025-08-18 · #2272 · Caution advisory — HTTP2 보안 주의 권고 (HTTP/2 security caution)
- **Scope**: HTTP/2 implementations (Apache Tomcat, Netty, SUSE, Fastly, H2O, etc.)
- **Background**: A DoS that abuses client-triggered server-side stream resets (CVE-2025-8671), plus related flaws in Tomcat (CVE-2025-48989) and Netty (CVE-2025-55163).
- **Checks**:
  - [ ] Apache Tomcat: 11.0.0-M1–11.0.9 → 11.0.10+, 10.1.0-M1–10.1.43 → 10.1.44+, 9.0.0.M1–9.0.107 → 9.0.108+
  - [ ] Netty: 4.2.3 and earlier → 4.2.4+, 4.1.123 and earlier → 4.1.124+
  - [ ] For other HTTP/2 implementations and operating systems, follow each product's reference site (SUSE, Fastly, H2O, etc.).
- **Action**: Update. For reference, a patch-type HTTP/2 notice exists: 2026-06-18 #2467 「웹서버 HTTP/2 관련 제품 보안 업데이트 권고」 (outside this document's scope; its relation to this vulnerability was not checked → advisories.json).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71844 · Attachment: none

### TR-15 Jiransoft (지란지교소프트) CrossUploader sample-file upload flaw
- **Notice**: 2026-11-03 · #2607 · Security action/hardening advisory — 지란지교소프트 제품 보안 조치 권고 (security action for Jiransoft products)
- **Scope**: CrossUploader 1.0.00 to 3.0.09
- **Background**: Improper file upload through the sample file (UploadProcess.jsp). No separate fixed version has been announced.
- **Checks**:
  - [ ] Delete the `/NamoCrossUploaderH5Samples` and `/NamoCrossUploaderJaSamples` folders if they exist in production.
  - [ ] Check whether `UploadProcess.jsp` exists outside the default install path and delete it if not needed.
  - [ ] Check web access logs for calls to that file and check upload paths for unexpected JSP or other scripts.
  - [ ] If the sample is used in a live service, allow only the extensions the business needs, verify authentication and authorisation on upload requests, validate extension, content and file name on the server, store uploads outside web-accessible paths, and block JSP execution in upload folders.
- **Action**: Deleting sample folders that are not used in the live service does not affect the product (per the notice). If they are used, assess the impact first.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72269 · Attachment: none

### TR-16 STEG (에스티이지) E-GENE ITSM unauthorised sign-up and file upload
- **Notice**: 2026-11-06 · #2612 · Security action/hardening advisory — 에스티이지 제품 보안 조치 권고 (security action for STEG products)
- **Scope**: E-GENE ITSM 7.0 and earlier
- **Background**: Unauthorised account registration and improper file upload vulnerabilities.
- **Checks**:
  - [ ] Self sign-up is temporarily disabled and new users are registered manually
  - [ ] File upload extensions are validated against an allow-list
  - [ ] The vendor's security patch has been applied
- **Action**: For other measures, patch as instructed by the vendor (02-811-2211, sd@steg.co.kr).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72284 · Attachment: none

---

## C. Development environment and software supply chain

### TR-17 Chained dev-tool supply-chain attack (Trivy → npm, PyPI, OpenVSX, GitHub Actions, Docker, Jenkins; TanStack)
- **Notice**: Caution advisory — 2026-04-01 · #2392 「개발도구 공급망을 통한 연쇄적 사이버 공격주의 권고」 (caution: chained attacks via the dev-tool supply chain; hunting guide v1) / 2026-05-20 · #2432 「…2차 권고」 (second advisory; hunting guide ver2.0)
- **Scope**: CI/CD (GitHub Actions, Jenkins), developer endpoints, npm/PyPI/Docker environments, Claude Code and VS Code environments
- **Background**: TeamPCP abused a CI/CD workflow flaw in Trivy (`pull_request_target`) to steal credentials, published a malicious Trivy v0.69.4, and used the tokens stolen through it to infect other ecosystems in a chain (CVE-2026-33634, CVSS 9.4). The second notice adds 84 malicious versions across 42 TanStack packages, the KICS Docker image and ast-github-action v2.3.35, @cap-js/db-service 2.10.1 and @cap-js/sqlite 2.2.2, Jenkins Checkmarx AST Scanner 2026.5.09, CVE-2026-45321 (9.6), and IDE persistence (Claude Code hooks, VS Code tasks) (per attachment).
- **Checks**:
  - [ ] Whether affected versions are installed: Trivy v0.69.4, litellm 1.82.7/1.82.8, telnyx 4.87.1/4.87.2, ast-results 2.53.0, cx-dev-assist 1.7.0, 64+ npm CanisterWorm packages and TanStack (guide Appendices A and C)
  - [ ] Host checks (per attachment, verbatim; the Korean `echo` text means "[infected] …"):
    ```
    ls ~/.local/share/pgmon/service.py 2>/dev/null && echo "[감염] CanisterWorm 백도어 존재"
    ls /tmp/pglog /tmp/.pg_state 2>/dev/null && echo "[감염] CanisterWorm 흔적 존재"
    systemctl --user is-active pgmon.service 2>/dev/null | grep -q "active" && echo "[감염] pgmon 서비스 실행 중"
    ls ~/.config/sysmon/sysmon.py 2>/dev/null && echo "[감염] sysmon 백도어 존재"
    systemctl --user is-active sysmon.service 2>/dev/null | grep -q "active" && echo "[감염] sysmon 서비스 실행 중"
    pip show litellm 2>/dev/null | grep -q "^Version: 1\.82\.\(7\|8\)$" && echo "[감염] litellm 악성 버전"
    pip show telnyx 2>/dev/null | grep -q "^Version: 4\.87\.\(1\|2\)$" && echo "[감염] telnyx 악성 버전"
    grep -l "setup\.mjs" ~/.claude/hooks.json .vscode/tasks.json 2>/dev/null && echo "[감염] IDE persistence 발견"
    ls ~/.claude/router_runtime.js 2>/dev/null && echo "[감염] TanStack IDE persistence"
    ```
    Windows (telnyx): `dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\msbuild.exe" 2>nul && echo [감염] Telnyx 백도어`. The hash-based confirmation commands for KICS, SAP CAP, Jenkins and TanStack are in section 4.1 of the guide.
  - [ ] CI/CD run history (KST): trivy-action/setup-trivy runs 3.20 02:43–14:40; pulls of aquasec/trivy:latest or :0.69.4–6 between 3.20 and 3.23; kics-github-action/ast-github-action runs 3.23 21:58–3.24 01:50; checkmarx/kics pulls and ast-github-action@v2.3.35 use on 4.22; Jenkins plugin update to 2026.5.09 on 5.09–10; @tanstack/ installs or updates 5.12 04:20–04:50
  - [ ] Whether a `tpcp-docs` or `docs-tpcp` repo exists in the organisation, and whether repos contain suspicious commits to `.claude/settings.json` or `.vscode/tasks.json` (message "chore: update dependencies", Co-authored-by: claude)
  - [ ] Network: the `X-Filename: tpcp.tar.gz` header and traffic to the guide's IOCs. CI/CD infections happen on cloud runners, so always pair this with host and CI/CD history checks.
  - [ ] Unnecessary `pull_request_target` triggers have been changed to `pull_request`, or a condition blocking execution of external contributors' code has been added where it is truly needed (ver2.0 recommendation)
- **Action**: If infection is suspected, immediately reissue npm/PyPI/GitHub tokens, SSH keys, cloud (AWS, GCP, Azure) credentials, Kubernetes configs, crypto wallets, DB credentials, .env files and CI/CD settings, and report to Boho-nara.
- **Source**: #2392 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72014 · #2432 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72059 · Attachments: 개발도구 공급망의 연쇄적 공격(Supply Chain Diffusion Attack) 헌팅.pdf (v1, 8 pages, campaigns A–E) / 개발도구_공급망의_연쇄적_공격(Supply_Chain_Diffusion_Attack)_헌팅.pdf (ver2.0, 12 pages, campaigns A–I; 21 network IOCs, 27 file SHA-256 hashes, appendix of infected packages)

### TR-18 Malicious LiteLLM versions (1.82.7, 1.82.8)
- **Notice**: 2026-04-01 · #2393 · Caution advisory — LiteLLM 제품 사용 주의 권고 (caution on using LiteLLM)
- **Scope**: LiteLLM (PyPI) 1.82.7, 1.82.8
- **Background**: Distribution on PyPI was halted because these versions may attempt credential theft. This is part of the TR-17 supply-chain attack: on `pip install` a `.pth` file runs automatically and installs the sysmon backdoor (per attachment).
- **Checks**:
  - [ ] Installed version (the `pip show litellm` command in TR-17)
  - [ ] A safe version, 1.82.6 or earlier, is in use
- **Action**: Self-check with the hunting guide and report if there are signs of compromise.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72015 · Attachment: none

### TR-19 Preventing credential exposure in development and operations
- **Notice**: 2026-07-16 · 공지 (pinned) · Security action/hardening advisory — 개발 운영 환경의 자격증명 노출에 따른 침해사고 예방 강화 요청 (request to prevent incidents caused by credential exposure in dev/ops environments)
- **Scope**: Code repositories (GitHub, etc.), collaboration tools, CI/CD, cloud consoles, developer endpoints
- **Background**: Access keys, tokens and API keys were exposed in repositories or collaboration tools, or stolen from infected developer endpoints and IDE extensions, leading to takeover of core systems, source-code leaks and supply-chain contamination. Because secrets remain in commit history, deleting the file does not complete remediation.
- **Checks**:
  - [ ] Credentials are not hard-coded in source; they are injected at run time from a secrets-management solution
  - [ ] `.gitignore` or similar prevents certificates and `.env` files from being uploaded
  - [ ] Automated secret detection runs before upload. Secret scanning and push protection are on by default only for public repositories, so confirm the policy covers the whole organisation, including private and internal repos
  - [ ] A rule forbids sharing credentials via collaboration tools (messengers, issue trackers, documents), and past sharing has been reviewed
  - [ ] Temporary credentials (e.g. IAM Role-based), MFA on DBs, cloud consoles, repositories and deployment systems, no standing admin-level keys, narrower repository access, minimal scope and lifetime for CI/CD tokens
  - [ ] Credential use restricted by IP/network segment; long-unused permissions revoked; cloud audit logs collected continuously with detection and alerts for abnormal API calls (permission enumeration, user/role creation, policy changes, mass instance creation)
  - [ ] IDE extensions and open-source packages are adopted only after checking source and publisher, pinning versions and verifying integrity. MFA on developer accounts, EDR on developer endpoints, hard-coded credentials checked in code review, regular security training
- **Action**: Always revoke and replace exposed credentials. Report incidents to Boho-nara.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72132 · Attachment: none

### TR-20 Malicious ZIPs posing as AI dev tools (spread via GitHub and GitHub Pages)
- **Notice**: 2026-07-16 · 공지 (pinned) · Caution advisory — AI 개발도구 위장 악성코드 유포 주의 권고 (caution: malware disguised as AI development tools)
- **Scope**: Windows endpoints of developers and users who download AI dev tools and assistants (paths per attachment)
- **Background**: The attacker pre-built 49 repositories impersonating Gemini, Claude Code, Codex, Grok CLI and others, then from '26.7.14. 22:02 (KST) switched their download links to malicious ZIPs. The ZIP hashes vary but the files inside are the same. C2 is re-resolved from a Polygon contract, so blocking IPs alone is not enough (per attachment).
- **Checks** (per attachment):
  - [ ] `Application.cmd`, `certificate.txt` and `utility.exe` all present together in a download path
  - [ ] An execution chain with `utility.exe` running under `cmd.exe`; `luau.exe dist.lua` being run
  - [ ] `%LOCALAPPDATA%\Programs\Chromium\Chromium.exe` created and run with the argument `"NTE3YjdjNWU1NjYzNjU2YTA1N2Y="`
  - [ ] Persistence: `C:\Windows\Setup\Scripts\ErrorHandler.cmd` present; scheduled task `OneDriveStandaloneUpdater_7d7752` created
  - [ ] Network: requests to Polygon RPC with `"method":"eth_call"` combined with the contract and selector given in the guide; the fixed /api/ and /task/ paths given in the guide; second-stage file requests to raw.githubusercontent.com
- **Action**: Download AI assistants (anything related to Claude/Codex/Gemini/Grok) only from official project pages and official distribution channels. For GitHub repositories, check star count, contributor history and account creation date. Scan for the IOCs immediately and report if there are signs of compromise.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72133 · Attachment: AI 개발도구 위장 악성코드 감염 헌팅가이드.pdf (list of 49 impersonating repositories; 7 file SHA-256 hashes + 49 distributed ZIPs; 8 network IOCs; 13-entry Polygon C2 history)

### TR-21 Malware disguised as IT admin and developer utilities (Operation SearchStrike)
- **Notice**: 2026-03-11 · #2378 · Caution advisory — IT 관리자·개발자 대상 유틸리티 도구로 위장한 악성코드 유포 주의 권고 (caution: malware disguised as utilities for IT admins and developers)
- **Scope**: Windows admin and developer endpoints
- **Background**: GitHub repositories pushed to the top of search results through SEO distribute MSIs disguised as Tftpd64, Postman, WinDbg, PsExec, USMT, IntuneWinAppUtil, BgInfo and RDCMan. They install a Node.js bot and use an Ethereum smart contract as the C2 channel.
- **Checks** (per attachment):
  - [ ] Files: a random 6-character directory under `%LOCALAPPDATA%`; `%LOCALAPPDATA%\<6자>\<6자>\node.exe` (6자 = 6 characters); high-entropy `.xml`/`.bak`/`.cfg`/`.bin` files in the working directory; randomly named `.cmd` files in `%LOCALAPPDATA%\Temp`
  - [ ] Registry: a random hex key under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` whose value runs a `.cfg`/`.ini` file with node.exe; random-string keys under `HKCU\Software\`
  - [ ] Processes: `msiexec.exe → cmd.exe → node.exe` or `explorer.exe → node.exe`; node.exe running from `%LOCALAPPDATA%` (hidden window)
  - [ ] Network: HTTPS requests from business endpoints to Ethereum RPC endpoints (rpc.mevblock[.]io, eth.llamarpc[.]com, etc.); an `X-Bot-Server` header; paths of the form `/api/<UUID>.<이미지확장자>` (image extension)
- **Action**: Allow only official distribution channels (Microsoft Store, learn.microsoft.com, official GitHub), verify a repository's star count, contributor history and account creation date, and scan for the IOCs immediately. Report if there are signs of compromise.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71998 · Attachment: Operation SearchStrike - IT 관리자 및 개발자 대상 유틸리티 위장 악.pdf (11 SHA-256 hashes, 10 C2 domains, 9 Ethereum RPC endpoints)

### TR-22 Fake OAuth phishing against GitHub users
- **Notice**: 2025-03-18 · #2158 · Caution advisory — 해외 파일 저장소(Github, 깃허브) 이용자 대상 사이버 공격 발생대비 주의 권고 (caution: attacks on users of an overseas file repository, GitHub)
- **Scope**: Developers and organisations using GitHub
- **Background**: Overseas, phishing mail using a "Security alert: unusual access attempt" lure targeted 12,000 repositories and led victims to a fake OAuth page that took over access to repositories, profiles, organisations and Gists.
- **Checks**:
  - [ ] When something suspicious is noticed: ① reset the password at once ② reset 2FA recovery codes ③ review the safety of personal access tokens ④ do not use password auto-save
  - [ ] Verify the sender address exactly and check that links in the mail point to the genuine site.
- **Action**: Report incidents to Boho-nara as a hacking incident.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71683 · Attachment: none

### TR-23 FreeType library out-of-bounds write
- **Notice**: 2025-03-17 · #2155 · Vulnerability remediation advisory — FreeType 라이브러리에서 발생하는 취약점에 대한 업데이트 권고 (update advisory for a FreeType library vulnerability)
- **Scope**: FreeType 2.13.0 and earlier
- **Background**: An out-of-bounds write while processing glyph structures for TrueType GX and variable fonts (CVE-2025-27363).
- **Checks**:
  - [ ] FreeType version checked and updated to 2.13.3
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71679 · Attachment: none

### TR-24 Generative AI usage policy
- **Notice**: 2025-02-07 · #2139 · Caution advisory — 생성형 AI 사용 관련 주의 보안권고 (security caution on using generative AI)
- **Scope**: The company's AI-service usage policy and its staff
- **Background**: As generative AI spreads, there is concern about leaks of confidential data and AI-assisted malware and phishing.
- **Checks** (for companies):
  - [ ] A policy forbids entering confidential data such as internal documents, source code and customer information into AI services
  - [ ] AI service usage is logged and access control prevents unauthorised use from the internal network
  - [ ] Generated content goes through source verification and review
  - [ ] There is a response plan for AI-driven attacks (automated hacking, social engineering)
  - [ ] (General-user items) Personal data is not entered, and code produced by AI code generators is scanned with a security solution before it is run
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71652 · Attachment: none

---

## D. Network devices, IoT and NAS

### TR-25 Ransomware targeting Synology NAS
- **Notice**: 2026-11-03 · #2605 · Caution advisory — Synology NAS 대상 랜섬웨어 공격 주의 권고 (caution: ransomware attacks on Synology NAS)
- **Scope**: Synology NAS (DSM)
- **Background**: Stored files are being encrypted. Extensions change to `L0CK3D`, `locked`, `lock3d`, `lock3D` and similar, and a ransom note appears. The URL of Synology's notice in reference [2] mentions extending PHP2Shell fixes to older DSM releases (related to TR-11).
- **Checks**:
  - [ ] Updated to the latest DSM and packages supported by the model (down to the detailed update number). If the version is end-of-support, move to a supported version or consider replacing the device. Patch details are in 2026-10-30 #2593 「Synology 제품 보안 업데이트 권고」 (advisories.json).
  - [ ] Direct internet exposure of the admin UI minimised and unnecessary port forwarding, remote access and services turned off. Remote access goes only through a controlled path such as VPN, with firewall allow-lists.
  - [ ] Default admin account disabled, a strong password not shared with other services, multi-factor authentication
  - [ ] Important data kept on offline storage separate from the NAS or in backups that restrict modification and deletion, with regular restore tests. Always-connected or synced storage can be hit too.
- **Action (if infection is suspected)**: Disconnect the NAS from the network and stop connected sync and backup jobs. Preserve ransom notes, encrypted files and system/access logs, and record the time of discovery, model, DSM version and actions taken. Do not reset, format, reinstall, or delete/overwrite encrypted files, and avoid unnecessary power-off, reboot or update. Report to KISA as a ransomware incident and follow its guidance. Beware of recovery tools of unknown origin and private recovery firms that guarantee recovery for money.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72267 · Attachment: Synology NAS 대상 랜섬웨어 공격 주의 권고.pdf (same as the body)

### TR-26 Credential theft from Fortinet firewalls and VPNs
- **Notice**: 2026-06-21 · #2471 · Caution advisory — 포티넷 제품 계정정보 탈취에 따른 피해 주의 (caution: damage from stolen Fortinet account credentials)
- **Scope**: Internet-exposed Fortinet firewall and VPN appliances
- **Background**: Not a new vulnerability: attackers break in automatically using password lists obtained from past leaks. A compromised appliance becomes an interception point that harvests more credentials, which are then used against other appliances (self-propagating).
- **Checks**:
  - [ ] Checked with reference site ① (Fortinet device compromise lookup, https://www.hudsonrock.com/fortinet)
  - [ ] Any anomalies such as abnormal logins
  - [ ] IDs and passwords changed for every account, including admins
- **Action**: Report any anomaly to KISA immediately. Check device firmware patches through the separate Fortinet patch-type notices (advisories.json).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72105 · Attachment: none

### TR-27 SECUWIZ (시큐위즈) SecuwaySSL U series emergency measures (2 notices)
- **Notice**: 2025-08-21 · #2274 · Security action/hardening advisory — 시큐위즈 제품 보안 조치 권고 (security action for SECUWIZ products) / 2025-09-04 · #2280 · Caution advisory — 시큐위즈 제품 보안 주의 권고 (security caution for SECUWIZ products)
- **Scope**: SecuwaySSL U 1.0/2.0 (#2274); all U-series versions 1.0/2.0/2.1 (#2280)
- **Background**: #2274 is an emergency fix for a Root password exposure vulnerability. #2280 is a patch adding integrity verification to strengthen incident response; devices that already have the July SSH patch must apply it too.
- **Checks**:
  - [ ] Affected version confirmed at the bottom of the [장비셋업] (Device setup) - [환경설정] (Settings) menu
  - [ ] SSH port blocked from the internet (check the deny rule under "장비보안정책" (device security policy) in the admin page)
  - [ ] Root password changed after the latest patch was applied (#2274)
  - [ ] `en_bohoKrCert_1.0_2.0_2.1_20250903.tar.gz` applied via [관리자페이지]-[장비셋업]-[장비패치] (Admin page - Device setup - Device patch); takes about 5–10 minutes, so keep other admin-page work to a minimum (#2280)
  - [ ] Patch history: `patch.md` under [관리자페이지]-[로그관리]-[백업파일관리] (Log management - Backup file management) and [관리자페이지]-[리포트]-[보안로그] (Reports - Security log)
- **Action**: Patching disables the SSH process. If SSH is needed, contact the vendor (02-6380-3680). The vendor supports online patching even if the maintenance contract has expired.
- **Source**: #2274 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71847 · #2280 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71859 · Attachment: none

### TR-28 Printer and multifunction-device vulnerabilities
- **Notice**: 2025-07-01 · #2232 · Caution advisory — 프린터 및 복합기 제품군 보안 주의 권고 (security caution for printers and MFPs)
- **Scope**: Brother, FUJIFILM, Konica Minolta, RICOH and TOSHIBA printers and MFPs
- **Background**: CVE-2017-9765 (stack buffer overflow), CVE-2024-51978 (weak credentials), CVE-2024-51979, CVE-2024-51982, CVE-2024-51983.
- **Checks**:
  - [ ] Whether models and versions in use appear in each vendor's affected list
  - [ ] Vendor remediation (security measures or firmware update) applied
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71784 · Attachment: none

### TR-29 D-Link DIR series (EoS) firmware vulnerability
- **Notice**: 2026-06-23 · #2472 · Caution advisory — D-Link 제품 보안 주의 권고 (security caution for D-Link products)
- **Scope**: DIR-895L A1, 890L A1, 885L A1, 880L A1, 868L C1/B1, 850L B1, 823 A1, 822 C1, 818LW Bx, 817 Ax
- **Background**: Improper restriction of operations within the bounds of a memory buffer (CVE-2016-5681). All are end-of-sale/support (EoS) products.
- **Checks**:
  - [ ] Firmware at or above the fixed version: 895L A1 v1.11WWb04, 890L A1 v1.09b14, 885L A1 v1.11WWb07, 880L A1 v1.07WWb08, 868L C1 v3.00WWb01, 868L B1 v2.03WWb01, 850L B1 v2.07WWB05, 823 A1 v1.00WWb05, 822 C1 v3.01WWb02, 818LW Bx v2.05b03beta03, 817 Ax v104WWB04
  - [ ] Whether EoS products are still in use
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72106 · Attachment: none

---

## E. Product-use cautions (EoL, stop using, replace)

### TR-30 PostgreSQL quoting API SQL injection
- **Notice**: 2025-02-19 · #2146 · Caution advisory — PostgreSQL 제품 이용 주의 권고 (caution on using PostgreSQL)
- **Scope**: PostgreSQL and software built with PostgreSQL as a component (vendors of such software must check)
- **Background**: SQL injection in the quoting API (CVE-2025-1094).
- **Checks**:
  - [ ] Version check (commands from the notice):
    ```
    psql --version
    SELECT version();
    SHOW server_version;
    ```
  - [ ] At or above fixed versions 17.3 / 16.7 / 15.11 / 14.16 / 13.19 (versions below these in each line are affected)
- **Action**: Update to the latest version immediately.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71662 · Attachment: none

### TR-31 Oracle WebLogic Server CVE-2017-10271
- **Notice**: 2025-09-03 · #2279 · Caution advisory — Oracle 제품 사용 주의 권고 (caution on using Oracle products)
- **Scope**: Oracle WebLogic Server 10.3.6.0.0, 12.1.3.0.0, 12.2.1.1.0, 12.2.1.2.0 and earlier
- **Background**: There has been recent real-world exploitation. Insufficient input validation in the WLS Security component allows remote code execution.
- **Checks**:
  - [ ] WebLogic version checked and updated to the latest version (see Oracle CPU Oct 2017)
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71858 · Attachment: none

### TR-32 LG Innotek (LG이노텍) LNV5110R (discontinued)
- **Notice**: 2025-07-29 · #2256 · Caution advisory — LG이노텍 제품 사용 주의 권고 (caution on using LG Innotek products)
- **Scope**: LNV5110R, all versions
- **Background**: Arbitrary command execution (CVE-2025-7742, CISA ICSA-25-205-04).
- **Checks**:
  - [ ] Removed from external networks immediately or isolated in the internal network
  - [ ] External HTTP access blocked by a firewall or similar; remote access allowed only through a VPN with current security settings
  - [ ] Abnormal traffic and unexpected file uploads monitored
  - [ ] Replacement of the discontinued product considered
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71823 · Attachment: none

### TR-33 SGA Solutions (SGA솔루션즈) TrustPKI Enterprise (discontinued)
- **Notice**: 2025-08-01 · #2257 · Caution advisory — SGA솔루션즈 제품 사용 주의 권고 (caution on using SGA Solutions products)
- **Scope**: TrustPKI Enterprise 1.2.8.9 and earlier (installed on PCs)
- **Background**: Insufficient validation allows remote code execution and arbitrary file download. The product is discontinued (service ended).
- **Checks**:
  - [ ] Removed immediately wherever it is installed on a PC
- **Action**: It is also a target of the July 2026 cleaning service (TrustPKI v1.2.8.9 and earlier, #2502 → TR-37).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71826 · Attachment: none

### TR-34 Xiaomi Redmi Buds Pro Bluetooth vulnerabilities (no patch)
- **Notice**: 2026-02-05 · #2350 · Caution advisory — Xiaomi 제품 사용 주의 권고 (caution on using Xiaomi products)
- **Scope**: Redmi Buds 3 Pro / 4 Pro / 5 Pro / 6 Pro
- **Background**: Information disclosure (CVE-2025-13834) and denial of service (CVE-2025-13328). No security patch is provided.
- **Checks**:
  - [ ] Bluetooth turned off when the earbuds are not in use in public places (crowded areas)
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71962 · Attachment: none

### TR-35 Stop using certain software (IoT) products (2 notices)
- **Notice**: Caution advisory 「일부 SW 제품 사용 주의 권고」 (caution on using certain software products) — 2025-09-16 · #2288, 2026-08-19 · #2518
- **Scope**: #2288: Seojin Networks (서진네트웍스) TCAM-D20, eBiz Networks (이비즈네트웍스) 별씨 2.070+, JWC Networks (제이더블유씨네트웍스) JCURI-HOME1 PRO 4.8.6.5+, Commax (코맥스) CND-501M, Humantalk (휴먼토크) 다뷰인디 9.181+, HL Holdings (HL홀딩스) MHD100 1.2.1+ / #2518: Petnuri (펫누리) F10, Seojin Networks TCAM-S30 24.09.25
- **Background**: Vulnerabilities that could pose a security threat were found (the notices give no vulnerability details). The second notice only changes the product list; the recommendation is the same.
- **Checks**:
  - [ ] Whether any listed product is in use
  - [ ] Use suspended until the vendor releases and applies a security patch
  - [ ] If use is unavoidable, only on a closed network cut off from the internet
- **Action**: Contact the vendor at the number given in the notice.
- **Source**: #2288 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71868 · #2518 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72161 · Attachment: none

### TR-36 WBJ Soft SoftManager cleartext transmission of sensitive data (no patch)
- **Notice**: 2026-07-10 · #2490 · Caution advisory — SoftManager 제품 보안 주의 권고 (security caution for SoftManager)
- **Scope**: SoftManager v5.2.xxxx, v6.2.xxxx
- **Background**: Cleartext Transmission of Sensitive Information. No patch exists; mitigate by changing settings.
- **Checks**:
  - [ ] Version check: '클라이언트 시작 화면' (client start screen), '도움말 - SoftManager 정보' (Help - About SoftManager)
  - [ ] Server settings changed to `HTTP 0(비활성화)` (disabled) and `HTTPS 8065(활성화, 임의지정)` (enabled, custom)
  - [ ] Only trusted clients may reach the server, DB logs are monitored, and the firewall blocks access once the purpose of use ends
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72128 · Attachment: none

---

## F. Endpoints, accounts and targeted threats

### TR-37 Cleaning service for vulnerable security-authentication and e-banking software (4 notices)
- **Notice**: Vulnerability remediation advisory — 2026-04-09 · #2400 「기업뱅킹 전자금융 소프트웨어 취약점 관련 클리닝 서비스 가동 안내」 (cleaning service launched for corporate e-banking software vulnerabilities) / 2026-06-01 · #2445, 2026-07-27 · #2502, 2026-10-06 · #2558 「보안인증 소프트웨어 취약점 관련 클리닝 서비스 가동 안내」 (cleaning service for security-authentication software vulnerabilities)
- **Scope**: Security-authentication and e-banking plug-ins installed on work PCs
- **Background**: Since 2026-04-09 KISA and the Ministry of Science and ICT have run a "security vulnerability cleaning service" with INCA Internet, SGA EPS, Exosphere Labs and Everyzone. The antivirus products (nProtect Online Security, VirusChaser, Exosphere, TurboVaccine) find vulnerable old software and remediate it with the user's consent. Patch-type notices that look related by title (outside this document's scope): 2025-07-07 #2238 「…보안 업데이트 권고 및 클리닝 서비스 시범 운영 안내」 (pilot) and 2025-11-17 #2308 「…보안 업데이트 권고 및 클리닝 서비스 가동 안내」.
- **Checks** (target per notice):
  - [ ] #2400 Inswave WGear 1.100.7.0205 and earlier (except 1.100.2.25091), remote code execution → delete or update to 1.100.11
  - [ ] #2445 Hancom With AnySign4PC v1.1.4.4 to v1.1.4.6, buffer overflow and remote code execution → deletion recommended (fixed version v1.1.5.0)
  - [ ] #2502 SGA Solutions TrustPKI v1.2.8.9 and earlier, arbitrary file creation and data tampering → delete
  - [ ] #2558 INNORIX Agent 1.1.1.001 to 1.3.5.576, local privilege escalation → delete
  - [ ] If one of the antivirus products above is in use, confirm the cleaning function has remediated these
- **Action**: Review security software across the organisation in one pass and remove what is unused (ties in with TR-38).
- **Source**: #2400 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72023 · #2445 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72074 · #2502 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72141 · #2558 https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72210 · Attachment: none

### TR-38 Hacking mail and watering-hole attacks by state-backed groups
- **Notice**: 2026-07-30 · #2504 · Caution advisory — (합동사이버보안권고문) 국가배후 해킹조직의 우리 국민·기업 해킹 공격 주의 권고 (joint cybersecurity advisory: state-backed hacking of Korean citizens and companies; KISA, NIS, KNPA, FSI and a public-private analysis council)
- **Scope**: Corporate PCs (with security software installed), website operators and hosting providers, software vendors
- **Background**: Mail poses as résumés, job offers, donations or investments. Links lead to blogs or github.io sites the attackers set up or hacked; attachments are ZIPs disguised as DRM-protected documents; real headhunters' accounts are sometimes hijacked. News, hospital and small websites are hacked and used as watering holes, combined with flaws in old e-signature, security-authentication and keyboard-security programs so that merely visiting infects the PC (per attachment).
- **Checks** (per attachment):
  - [ ] [Security team] All software in the organisation, including e-signature and security-authentication tools, has been reviewed and updated in one pass, and unused software removed
  - [ ] [Security team] Asset and patch management, network separation and access control are systematised, with IOC-based detection and monitoring
  - [ ] [Security team] Critical servers and work PCs are physically or logically separated, or blocked from direct internet access; different passwords per system and MFA
  - [ ] [Security team] Training and drills that share watering-hole and fake-headhunter mail cases
  - [ ] [Individuals] Avoid saving passwords in browsers, use two-step verification for important accounts, double-check even work mail through official contacts
  - [ ] [Website/hosting] Unnecessary ports and services blocked, admin-page access control, web shells/unused admin accounts/temp files removed, continuous monitoring for defacement and injected scripts, WAF in place and access logs retained and reviewed
  - [ ] [Software vendors] Patch release and vulnerability-report handling process, vulnerability checks at each development stage, integrity of source code and build environment, pre-checking open source for known vulnerabilities and SBOM
- **Action**: Report to the competent authority as soon as an incident is known (Boho-nara 118, NIS 111, KNPA National Security Investigation Bureau, FSI 02-3495-9494).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72144 · Attachment: (합동사이버보안권고문) 국가배후 해킹조직의 우리 국민·기업 해킹 공격 주의 권고.pdf (8 pages, links to 4 technical reports by participating security firms, no IOCs)

### TR-39 Fake installers at the top of search results: KakaoTalk PC impersonation
- **Notice**: 2026-04-15 · 공지 (pinned) · Caution advisory — 카카오톡 사칭 악성코드 유포 주의권고 (caution: malware impersonating KakaoTalk)
- **Scope**: Windows PC users (including work PCs)
- **Background**: Searching for '카카오톡 PC버전' (KakaoTalk PC version) on Google or Bing shows a phishing site imitating the official download page at the top. About 560 downloads are estimated for '26.2.10.–4.14., and an international or state-backed group is suspected. Antivirus detection names include Dropper/Win.Agent, Trojan/Win.Dapato and Trojan/Win.Masquerading.
- **Checks**:
  - [ ] Major software is downloaded from the official homepage (Kakao: https://www.kakaocorp.com), not from search results
  - [ ] The domain of "Ad" or top-ranked search links is checked against the genuine site
  - [ ] Antivirus real-time protection is on and scans run regularly with current signatures
- **Action**: Report to Boho-nara if infection is suspected. The same technique appears in TR-20 and TR-21.
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72027 · Attachment: none

### TR-40 KISA-impersonating `.lnk` attachment malware
- **Notice**: 2025-05-11 · #2207 · Caution advisory — KISA(한국인터넷진흥원) 사칭, 악성코드 유포에 따른 주의 권고 (caution: malware distributed by impersonating KISA)
- **Scope**: Windows PC mail users
- **Background**: An attachment named 'KISA알림.pdf.lnk' ("KISA notice") lures users into running it; it then downloads info-stealing malware that exfiltrates sensitive data from the PC. The phishing mail itself was not found, but it is believed to have spread under subjects or content about issues such as 'KISA's security service' or 'the recent SKT breach'.
- **Checks**:
  - [ ] File Explorer is set to show 'File name extensions' and `.lnk` attachments are not run
  - [ ] The sender is verified exactly and site addresses in the mail are checked against the genuine site
  - [ ] OS and document software (Hangul, etc.) are up to date and antivirus scans run regularly
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71748 · Attachment: none

### TR-41 Browser auto-login credential leakage
- **Notice**: 2025-02-13 · #2141 · Caution advisory — 인터넷 브라우저 제품 자동로그인 사용 주의 권고 (caution on browser auto-login)
- **Scope**: Google Chrome, Microsoft Edge, Mozilla Firefox (all versions)
- **Background**: Using auto-login can leak the credentials stored on the PC. The #2504 joint advisory also lists theft of credentials saved in browsers as a type of damage.
- **Checks**:
  - [ ] Auto-login is avoided until a related security patch is available
  - [ ] Passwords are changed periodically and a second factor such as OTP is set up
  - [ ] On shared PCs, users log out after use and delete stored credentials
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71655 · Attachment: none

### TR-42 Targeted quishing impersonating government agencies and think tanks
- **Notice**: 2026-01-10 · #2334 · Caution advisory — 정부기관, 싱크탱크 사칭 큐싱(Quishing) 유포 주의 권고 (caution: quishing impersonating government agencies and think tanks)
- **Scope**: Smartphones of corporate and organisational staff (devices outside the company's security controls)
- **Background**: Attackers pose as staff of domestic or foreign think tanks (asking for advice or a survey on current affairs) or of diplomacy-related government agencies (offering access to sensitive information) and get victims to scan a QR code. This installs a malicious app (stealing device info, SMS and photos) or opens a fake SNS login page, with the aim of stealing credentials for the victim's organisation's IT infrastructure.
- **Checks**:
  - [ ] Staff told not to scan QR codes in mail or messages from unknown senders
  - [ ] Staff told about the "quishing check service" on the Boho-nara KakaoTalk channel
  - [ ] Staff told that government agencies and financial companies never ask, by phone or text, for a remote-control app to be installed (even one from an official store)
- **Action**: If a malicious app was installed, remove it with mobile antivirus or manually; if financial services were used on the phone, revoke and reissue the joint certificate (공동인증서) and security card; apply for the number-spoofing SMS blocking service (번호도용문자차단서비스).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71936 · Attachment: none

### TR-43 Hacking mail impersonating public institutions and companies (fraud attempt cases)
- **Notice**: 2026-09-29 · #2551 · Other — 공공기관 사칭 해킹메일을 통한 사기 시도 사례 보고 (report of fraud attempts via hacking mail impersonating public institutions)
- **Scope**: Staff and individual mail users
- **Background**: Keywords such as "involvement in a crime", "legal violation" and "compensation for a personal-data leak" are used. Public-institution impersonation ("suspension of use", "summons", "explanation procedure") leads to phishing sites and mobile malware; company impersonation ("damage compensation", "payout") leads to entering personal data.
- **Checks**:
  - [ ] Sender addresses are checked carefully and unknown mail and attachments are not opened. When arriving via a link in the mail, users confirm it matches the genuine site and do not enter account details if it does not
  - [ ] OS and document software are kept current and antivirus scans run regularly
- **Action**: Check suspicious URLs with the "smishing/phishing check service" on the Boho-nara KakaoTalk channel. The reporting-centre address 'conterscam112.go.kr' in the original appears to be a typo (other notices give counterscam112.go.kr).
- **Source**: https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=72202 · Attachment: 260929_공공기관 사칭 해킹메일을 통한 사기 시도 사례 보고.pdf (the same file is also in the #2500 folder)

---

## G. Social engineering (phishing and smishing) trends

These are caution advisories aimed at individuals; use them as staff awareness material. Common responses: the "smishing/phishing (quishing) check service" on the Boho-nara KakaoTalk channel, "Report as spam" on the phone, the Telecom Financial Fraud Integrated Reporting Center (1394, counterscam112.go.kr), carriers' number-spoofing SMS blocking service (번호도용문자차단서비스), and the 118 hotline.

| Posted | No. | Impersonated party / theme | Technique |
|---|---|---|---|
| 2025-01-17 | 2127 | Portal-site phishing mail aimed at crypto-asset users | Targets picked from community posts; phishing mail steals accounts; wallet data stored in the cloud is used to transfer assets |
| 2025-01-24 | 2131 | Lunar New Year (traffic fines, gift-money transfers) | Smishing; promotes the smishing/quishing check service |
| 2025-02-18 | 2145 | Card delivery / issuance | Lures victims to call a fake call centre → install a remote-control app from the official store → data theft |
| 2025-03-11 | 2153 | Acquaintances (online wedding invitations) | SMS URL that appears to come from an acquaintance's number → malware that hides its icon → re-spreads via contacts |
| 2025-03-20 | 2163 | Police (교통민원24, traffic civil service) | Violation notice / fine SMS → malware posing as police apps; identifiable by the [국제발신] (international) tag |
| 2025-04-14 | 2186 | KISA staff | Promises refunds of crypto-fraud losses, shows press releases, then demands a wallet-opening fee and ID documents |
| 2025-04-27 | 2194 | Free SIM replacement / SIM protection service | Sites in search results redirect via non-profit domains to gambling sites |
| 2025-05-08 | 2202 | SKT and government agencies (SIM hacking) | Fake call centres / voice phishing under the guise of relief → remote-control apps and malware |
| 2025-06-09 | 2218 | Blockchain Nuridan (블록체인누리단) secretariat | Look-alike mail account with '.co' appended to the real address, urging users to run an attachment |
| 2025-06-17 | 2224 | (Not impersonation) public charging ports and open Wi-Fi | Choice Jacking installs malware to steal data; account and payment data stolen on open Wi-Fi |
| 2025-07-02 | 2233 | Government agencies (fraud-victim relief) | Relief-application phishing sites shown when searching e.g. "몸캠피싱" (sextortion) → personal and card data |
| 2025-07-09 | 2241 | Consumer-recovery coupon (Gov24, local-currency apps, card companies) | Smishing, phishing sites at the top of search results or in ads, voice phishing for remote-control apps; official notices contain no URLs |
| 2025-07-29 | 2255 | Repeal of the device distribution act (carriers, phone shops) | Subsidy / pre-order SMS → malware and phishing sites, promoted to the top of search results |
| 2025-08-21 | 2273 | Fines and penalties (government, local authorities) | Administrative-penalty SMS → sites misusing agency MI (logo) and malware |
| 2025-09-07 | 2283 | Payment agents and dispute-mediation bodies (micropayment fraud) | Refund / compensation lures → malware takes over phone permissions for micropayments |
| 2025-10-01 | 2291 | Gov24 and mobile ID (government system fire) | Fake "alternative system" SMS, search phishing sites, compensation voice phishing |
| 2025-10-02 | 2292 | Chuseok (national grants, "new Gov24 address", 교통민원24, trash fines, gifts) | Shares sample smishing texts (corporate part in TR-07) |
| 2025-11-26 | 2310 | Korea Post main numbers (card delivery) | Calls from Korea Post numbers to confirm personal data and provide a fake delivery-tracking URL |
| 2025-11-28 | 2315 | Ministry of the Interior and Safety (coupon over-payment / clawback) | Phishing mail from addresses resembling government domains → phishing sites and malicious attachments |
| 2025-11-29 | 2316 | E-commerce (Coupang) breach | Compensation / refund SMS, search phishing sites, compensation voice phishing |
| 2025-12-19 | 2328 | E-commerce (Coupang), prosecutors, police, Korea Post (cases) | SMS containing personal data → phishing sites and Telegram; law-enforcement impersonation → remote-control apps |
| 2026-02-12 | 2353 | Lunar New Year (public institutions, gifts, shopping malls) | Fine lookups, gift-receipt checks, fake shopping malls; 2.14 million government/public-institution impersonation cases in '23–'25 (53.4%) |
| 2026-03-16 | 2381 | Fuel costs / fuel subsidies (Middle East crisis) | Subsidy, energy-voucher and airfare-refund SMS, search phishing sites, voice phishing |
| 2026-03-25 | 2387 | (Not impersonation) illegal streaming apps | Unofficial apps (e.g. 티비위키) → SMS theft and unauthorised gambling spam |
| 2026-04-16 | 2406 | High-oil-price relief grant (Gov24, local-currency apps, card companies) | Smishing, search phishing sites, voice phishing |
| 2026-04-28 | 2411 | Community centre and Korea Credit Information Services | Calls/messages posing as a community centre → asks victims to call back a fake KCIS number → identity verification and personal data |
| 2026-05-12 | 2423 | Hotels (data leaked from a travel booking platform) | Real booking data used in "payment problem / reconfirm" SMS → payment data entered on phishing URLs |
| 2026-05-21 | 2433 | Gov24 ("national grant", high oil prices) (cases) | Fake PDF-viewer app → second-stage malware steals screen contents |
| 2026-06-03 | 2448 | OTT platform (TVING) data leak | Compensation / refund SMS, search phishing sites, voice phishing |
| 2026-07-16 | 2493 | Card companies | Account-suspension SMS → theft of card number, expiry date and CVC |
| 2026-07-21 | 2500 | Telegram, Apple, WhatsApp | Verification SMS such as "login attempt from a new device" → account theft on phishing login pages (the attachment is the #2551 document, misfiled) |
| 2026-08-11 | 2515 | Community-centre phone numbers (caller-ID spoofing) | Asks victims to call back a fake KCIS number; report spoofed caller IDs at anti-forgery.kisa.or.kr |
| 2026-09-17 | 2542 | Chuseok (big-company prizes, delivery tracking, traffic violations) | Prize event pages, fake shopping malls, fine-lookup smishing |
| 2026-10-06 | 2559 | Compensation for financial-sector and other data leaks | Compensation / leak-check SMS, search phishing sites, voice phishing |
| 2026-10-16 | 2567 | Crypto exchanges and wallets | Payout / unusual-activity SMS → phishing sites and malware; seed phrase requested on the pretext of asset recovery |

Original links follow the form `https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=<nttId>`. No.=nttId: 2127=71638, 2131=71643, 2145=71661, 2153=71676, 2163=71689, 2186=71718, 2194=71727, 2202=71739, 2218=71767, 2224=71774, 2233=71791, 2241=71801, 2255=71821, 2273=71846, 2283=71862, 2291=71880, 2292=71881, 2310=71904, 2315=71909, 2316=71910, 2328=71925, 2353=71966, 2381=72001, 2387=72007, 2406=72029, 2411=72036, 2423=72049, 2433=72060, 2448=72078, 2493=72131, 2500=72139, 2515=72158, 2542=72191, 2559=72211, 2567=72219

---

## Appendix. Notice number → item index
- A: 2116→TR-10 · 2149/2222/2268/2319/2348→TR-03 · 2154→TR-08 · 2193/2198/2210→TR-01 · 2244→TR-04 · 2292/2541→TR-07 · 2322→TR-02 · 2332/2456→TR-06 · 2385→TR-09 · 2405→TR-05
- B: 공지 (2026-10-22)→TR-11 · 2581→TR-12 · 공지 (2026-10-03)→TR-13 · 2272→TR-14 · 2607→TR-15 · 2612→TR-16
- C: 2392/2432→TR-17 · 2393→TR-18 · 공지 (2026-07-16, credentials)→TR-19 · 공지 (2026-07-16, AI dev tools)→TR-20 · 2378→TR-21 · 2158→TR-22 · 2155→TR-23 · 2139→TR-24
- D: 2605→TR-25 · 2471→TR-26 · 2274/2280→TR-27 · 2232→TR-28 · 2472→TR-29
- E: 2146→TR-30 · 2279→TR-31 · 2256→TR-32 · 2257→TR-33 · 2350→TR-34 · 2288/2518→TR-35 · 2490→TR-36
- F: 2400/2445/2502/2558→TR-37 · 2504→TR-38 · 공지 (2026-04-15)→TR-39 · 2207→TR-40 · 2141→TR-41 · 2334→TR-42 · 2551→TR-43
- G (table): 2127, 2131, 2145, 2153, 2163, 2186, 2194, 2202, 2218, 2224, 2233, 2241, 2255, 2273, 2283, 2291, 2292 (corporate part in TR-07), 2310, 2315, 2316, 2328, 2353, 2381, 2387, 2406, 2411, 2423, 2433, 2448, 2493, 2500, 2515, 2542, 2559, 2567
