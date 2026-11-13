🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin ky nang Claude Code danh cho phan tich-danh gia lo hong Ha tang Thong tin Trong yeu (CII), danh gia bao mat AI, bao mat robot, bao mat khong gian, huong dan lap trinh an toan, danh gia bao mat Zero Trust va Bao mat chuoi cung ung SW (SBOM).

---

## Tong quan

KESE (KISA Enhanced Security Evaluation Kit) la mot plugin Claude Code cung cap kha nang danh gia lo hong bao mat toan dien dua tren huong dan cua KISA (Co quan An ninh va Internet Han Quoc). Ho tro danh gia Ha tang Thong tin Trong yeu (CII), Bao mat AI, Bao mat Robot, Bao mat Khong gian, Lap trinh An toan va Bao mat Zero Trust.

## Tinh nang

| Ky nang | Mo ta |
|---------|-------|
| `/kesekit-start` | Chay danh gia lo hong bao mat toan dien (CII 560+ / Bao mat AI / Bao mat Robot / Bao mat Khong gian / Lap trinh An toan / Zero Trust / Chuoi cung ung SW) |
| `/kesekit-check` | Danh sach kiem tra tuan thu bao mat truoc trien khai (CII / AI / Robot / Khong gian / Lap trinh An toan / Zero Trust / Chuoi cung ung SW) |
| `/kesekit-fix` | Tu dong tao script tang cuong bao mat va ban va lo hong (CII / AI / Robot / Khong gian / Lap trinh An toan / Zero Trust / Chuoi cung ung SW) |
| `/kesekit-guide` | Tao prompt lap trinh an toan cho cac cong cu AI (CII / AI / Robot / Khong gian / JS·Python·Chung / Zero Trust / Chuoi cung ung SW) |

## Huong dan duoc ho tro

### 1. CII (Ha tang Thong tin Trong yeu) — 560+ hang muc

**Danh gia Ky thuat**
| He thong | Ma | Hang muc |
|----------|-----|:--------:|
| May chu Unix/Linux | U-01~U-67 | 67 |
| May chu Windows | W-01~W-64 | 64 |
| Dich vu Web | WEB-01~WEB-26 | 26 |
| Thiet bi Bao mat | S-01~S-23 | 23 |
| Thiet bi Mang | N-01~N-38 | 38 |
| He thong Dieu khien | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Di dong | M-01~M-04 | 4 |
| Web Application | 21 ma | 21 |
| Ao hoa | HV-01~HV-25 | 25 |
| Dam may | CA-01~CA-19 | 19 |

**Danh gia Quan ly**: A-1~A-127 (127 hang muc, 14 linh vuc)
**Danh gia Vat ly**: P-1~P-18 (18 hang muc)

### 2. Huong dan Bao mat AI — 54+ hang muc

| Doi tuong | Hang muc | Vong doi |
|-----------|:--------:|----------|
| Nha phat trien AI | 54 | 6 giai doan (Lap ke hoach→Du lieu→Mo hinh→Trien khai→Giam sat→Loai bo) |
| Nha cung cap dich vu | ~43 | 6 giai doan (Lap ke hoach→Phat trien→Van hanh→Bao tri→Phan hoi→Loai bo) |
| Nguoi dung | 7 | Cac phuong phap bao mat tot nhat |

### 3. Bao mat Robot — ~103 hang muc

| Danh muc | Ma | Hang muc | Tieu chuan Tham chieu |
|----------|-----|:--------:|----------------------|
| Phat trien PM an toan (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Bao mat chuoi cung ung | SC-01~07 | 7 | NIST SP 800-161 |
| Nhan dang va Xac thuc | IA-01~11 | 11 | IEC 62443 |
| Kiem soat Su dung | UC-01~11 | 11 | IEC 62443 |
| Toan ven He thong | SI-01~11 | 11 | IEC 62443 |
| Bao ve Du lieu | DP-01~04 | 4 | IEC 62443 |
| Han che Luong Du lieu | DFR-01~02 | 2 | IEC 62443 |
| Phan hoi Su kien | ER-01~03 | 3 | IEC 62443 |
| Kha dung Tai nguyen | RA-01~08 | 8 | IEC 62443 |
| Khuc phuc Mang | CR-01~13 | 13 | EU CRA |
| Bao mat Khong day | WS-01~14 | 14 | EU RED |

Doi tuong: Robot cong nghiep / dich vu / y te (ISO 8373)

### 4. Bao mat Khong gian — 53 hang muc

| Linh vuc | Ma | Hang muc | Tieu chuan Tham chieu |
|----------|-----|:--------:|----------------------|
| Kiem soat Truy cap | AC-01~12 | 12 | CMMC, K-RMF |
| Nhan dang va Xac thuc | IA-01~02 | 2 | CMMC, NIS2 |
| Bao mat He thong va Truyen thong | SC-01~07 | 7 | NIST IR 8401 |
| Toan ven He thong va Thong tin | SI-01~04 | 4 | NIST CSF |
| Quan ly Van hanh He thong/Dich vu | SO-01~09 | 9 | ISMS-P |
| Phan hoi Su co | IR-01~02 | 2 | NIS2 |
| Bao mat Nhan su | PS-01~02 | 2 | CMMC |
| Bao mat Vat ly | PE-01~03 | 3 | K-RMF |
| Danh gia Rui ro va Bao mat | RA-01~02 | 2 | NIST CSF |
| Quan tri Bao mat | SG-01~04 | 4 | ISMS-P |
| Ke hoach Khan cap | CP-01~02 | 2 | NIST IR 8270 |
| Quan ly Chuoi cung ung | SM-01~04 | 4 | CMMC, NIS2 |

Doi tuong: Nha van hanh ve tinh, nha cung cap GSaaS, nha van hanh tram mat dat, cong ty chuoi cung ung khong gian

### 5. Huong dan Lap trinh An toan — 46 hang muc

| Danh muc | Hang muc | CWE | Tieu chuan Tham chieu |
|----------|:--------:|:---:|----------------------|
| Xac thuc va Bieu dien Du lieu Dau vao | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Chuc nang Bao mat | 16 | 16 | CWE/SANS Top 25 |
| Thoi gian va Trang thai | 2 | 3 | CWE |
| Xu ly Loi | 3 | 3 | CWE |
| Loi Ma nguon | 3 | 3 | CWE |
| Dong goi | 4 | 5 | CWE |
| Lam dung API | 2 | 1 | CWE |

**Ngon ngu duoc ho tro:**
| Ngon ngu | Hang muc | Framework |
|----------|:--------:|-----------|
| Pseudo Code (chung) | 46 | Mau doc lap ngon ngu |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Doi tuong: Nha phat trien web JavaScript/Python, nguoi dung cong cu AI (Claude, Cursor, Copilot), nha phat trien vibe coding

### 6. Bao mat Zero Trust — ~421 hang muc

| Yeu to Cot loi | Ma | Hang muc | Muc do Truong thanh |
|----------------|-----|:--------:|---------------------|
| Danh tinh | ZT-ID-01~53 | 53 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| Thiet bi va Diem cuoi | ZT-DV-01~36 | 36 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| Mang | ZT-NW-01~54 | 54 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| He thong | ZT-SY-01~49 | 49 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| Ung dung va Khoi luong Cong viec | ZT-AP-01~60 | 60 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| Du lieu | ZT-DA-01~58 | 58 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| Kha nang Quan sat va Phan tich | ZT-VA-01~43 | 43 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| Tu dong hoa va Dieu phoi | ZT-AU-01~43 | 43 | Truyen thong/Khoi dau/Nang cao/Toi uu |
| Dac thu OT/ICS | ZT-OT-01~25 | 25 | Truyen thong/Khoi dau/Nang cao/Toi uu |

**4 Muc do Truong thanh**: Truyen thong (Traditional) → Khoi dau (Initial) → Nang cao (Advanced) → Toi uu (Optimal)
**Tieu chuan Tham chieu**: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Doi tuong: Doanh nghiep ap dung Zero Trust, moi truong OT/ICS, to chuc chuyen doi dam may, nguoi phu trach danh gia muc do truong thanh bao mat

### 7. Bao mat chuoi cung ung SW (SBOM) — 29 hang muc

| Giai doan | Ma | Hang muc | Tieu chuan |
|-----------|-----|:--------:|------------|
| Thiet ke | SC-01~05 | 5 | NIST SP 800-161r1 |
| Phat trien | SC-06~16 | 11 | NIST SP 800-218 |
| Cung ung/Phan phoi | SC-17~19 | 3 | NTIA SBOM |
| Trien khai va Van hanh | SC-20~26 | 7 | NIS-SBOM |
| Bao tri | SC-27~29 | 3 | NIS-SBOM |

## Cai dat

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

## Cach su dung

```bash
# Bat dau danh gia bao mat toan dien
/kesekit-start

# Chay danh sach kiem tra truoc trien khai
/kesekit-check

# Tao script tang cuong bao mat
/kesekit-fix

# Nhan prompt lap trinh an toan
/kesekit-guide
```

---

## Cau truc Du an

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Sieu du lieu plugin
├── skills/                            ← Ky nang tieng Anh
│   ├── start/
│   │   ├── SKILL.md                  ← Bo dinh tuyen (~80 dong)
│   │   ├── references/               ← Tai lieu mo ta/quy chuan
│   │   │   ├── ai-security/          ← Tong quan, nha cung cap, huong dan nguoi dung
│   │   │   └── space-security/       ← Tong quan, kich ban de doa
│   │   ├── templates/                ← Bieu mau, bang danh sach kiem tra
│   │   │   ├── cii/                  ← CII 14 bang kiem tra
│   │   │   ├── ai-security/          ← Xac minh nha phat trien AI, danh sach kiem tra nguoi dung
│   │   │   ├── robot-security/       ← Bao mat robot 6 danh sach kiem tra
│   │   │   ├── space-security/       ← Bao mat khong gian 4 bang kiem tra
│   │   │   └── zero-trust/           ← Bang kiem tra Zero Trust
│   │   └── scripts/                  ← Script kiem tra/sua loi co the thuc thi
│   │       ├── cii/                  ← Script bash, PowerShell, SQL
│   │       └── robot-security/       ← Script tuong lua, SBOM, chung chi
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Ky nang tieng Han (cung cau truc)
├── 문서/                              ← PDF goc
├── authorkit/                         ← Tai lieu goc va san pham cong viec
├── docs/                              ← README bang 20 ngon ngu
├── CONTRIBUTING.md                    ← Cach them huong dan
└── README.md
```

---

## Lich su Thay doi

### v4.0.0 (2026-04-03)

**Them huong dan moi: Bao mat Zero Trust**
- Nguon: KISA Zero Trust Guideline 2.0 (245 trang) + Mo hinh Truong thanh Zero Trust (182 trang) + Huong dan Zero Trust cho OT (67 trang)
- 9 yeu to cot loi, ~421 hang muc kiem tra, 4 muc do truong thanh
- Ho tro dac thu OT/ICS (ZT-OT-01~25)
- Tieu chuan: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

### v3.2.0 (2026-04-02)

**Them huong dan moi: Huong dan Lap trinh An toan**
- Nguon: KISA Javascript Secure Coding Guide 159 trang + Python Secure Coding Guide 176 trang (ban cap nhat 2023)
- 7 danh muc, 46 hang muc, 49 CWE
- Huong dan Pseudo Code chung moi (mau UNSAFE/SAFE doc lap ngon ngu)
- Vi du ma nguon cho framework JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy)

### v3.0.0 (2026-04-02)

**Thay doi khong tuong thich: dinh dang lenh da cap nhat**
- Tat ca ky nang duoc hop nhat vao khong gian ten `kesekit`
- Dinh dang lenh: `/start` → `/kesekit-start` (them tien to khong gian ten)

**Them huong dan moi: Bao mat Khong gian**
- Nguon: Mo hinh Bao mat Khong gian Part1 134 trang + Part2 223 trang + Huong dan Giai thich 218 trang (MSIT/KISA)
- 12 linh vuc, 53 hang muc danh sach kiem tra
- Doi tuong: Nha van hanh ve tinh, nha cung cap GSaaS, nha van hanh tram mat dat

### v2.0.0 (2026-03-30)

**Tai cau truc — Ap dung mau Progressive Disclosure**

| Thay doi | Truoc (v1.0) | Sau (v2.0) |
|----------|-------------|------------|
| SKILL.md | Toan bo kien thuc noi tuyen (270~465 dong) | Chi bo dinh tuyen (~50~80 dong) |
| Huong dan | Chi ho tro CII | Ho tro CII + Bao mat AI |
| Luu tru kien thuc | Ma cung trong SKILL.md | Tach rieng vao `references/` (18 tep) |
| Ma hang muc | Chi bao gom mot so hang muc | Toan bo hang muc dua tren huong dan 2026 |
| Kha nang mo rong | Them huong dan moi tang so ky nang | Co dinh 4 ky nang, chi them references |

**Them huong dan moi: Huong dan Bao mat AI**
- Nguon: Bo Khoa hoc va ICT · KISA 「Huong dan Bao mat Tri tue Nhan tao (AI)」
- Nha phat trien AI: 54 hang muc xac minh (vong doi 6 giai doan)
- Yeu cau bao mat cho nha cung cap dich vu AI
- 7 quy tac bao mat cho nguoi dung AI

**Cap nhat Huong dan CII**
- Trich xuat lai toan bo hang muc dua tren huong dan chi tiet 2026
- Phan anh he thong ma hang muc (WEB, HV, CA va cac ma moi khac)

### v1.0.0 (2026-03-29)

- Phien ban dau tien
- 4 ky nang phan tich-danh gia lo hong CII (Han/Anh)
- Ky thuat (424) + Quan ly (127) + Vat ly (9) hang muc

---

## Co so Phap ly

- **Luat Bao ve Ha tang Thong tin va Truyen thong** (Act on Protection of Information and Communications Infrastructure)
- **Luat Chinh phu Dien tu** (e-Government Act)
- **Luat Bao ve Thong tin Ca nhan** (Personal Information Protection Act)
- **Luat Co ban ve Tri tue Nhan tao** (AI Basic Act, co hieu luc tu 2026.1.22)

---

## Tai lieu Lien quan

- [Huong dan Chi tiet Phan tich-Danh gia Lo hong Ky thuat KISA](https://www.kisa.or.kr)
- [Huong dan Bao mat Tri tue Nhan tao (AI)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Built With

| Plugin | Mo ta |
|--------|-------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Ky nang ho tro viet sach - phan tich PDF, trich xuat cau truc, bien tap/viet lai |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Tuong thich hook plugin Claude Code tren moi truong Windows |

---

## License

MIT License

## Author

CDPP Corp (https://github.com/cdppcorp)
