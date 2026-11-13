🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin Claude Code untuk analisis dan evaluasi kerentanan Infrastruktur Informasi Kritis (CII), evaluasi keamanan AI, keamanan robot, keamanan ruang angkasa, panduan secure coding, evaluasi Zero Trust, dan Keamanan Rantai Pasokan SW (SBOM) berdasarkan pedoman KISA (Badan Internet dan Keamanan Korea).

---

## Ikhtisar

KESE (KISA Enhanced Security Evaluation Kit) adalah plugin Claude Code yang menyediakan kemampuan penilaian kerentanan keamanan secara menyeluruh berdasarkan pedoman KISA (Badan Internet dan Keamanan Korea). Mendukung penilaian Infrastruktur Informasi Kritis (CII), Keamanan AI, Keamanan Robot, Keamanan Ruang Angkasa, Secure Coding, dan evaluasi Zero Trust.

## Fitur

| Skill | Deskripsi |
|-------|-----------|
| `/kesekit-start` | Menjalankan penilaian kerentanan keamanan lengkap (CII 560+ / AI / Robot / Ruang Angkasa / Secure Coding / Zero Trust / Rantai Pasokan SW) |
| `/kesekit-check` | Daftar periksa kepatuhan keamanan sebelum deployment (CII / AI / Robot / Ruang Angkasa / Secure Coding / Zero Trust / Rantai Pasokan SW) |
| `/kesekit-fix` | Menghasilkan skrip hardening dan perbaikan keamanan secara otomatis (CII / AI / Robot / Ruang Angkasa / Secure Coding / Zero Trust / Rantai Pasokan SW) |
| `/kesekit-guide` | Membuat prompt secure coding untuk alat AI (CII / AI / Robot / Ruang Angkasa / JS·Python·Umum / Zero Trust / Rantai Pasokan SW) |

## Pedoman yang Didukung

### 1. Infrastruktur Informasi Kritis (CII) — 560+ item

**Penilaian Teknis**
| Sistem | Kode | Jumlah Item |
|--------|------|:----------:|
| Server Unix/Linux | U-01~U-67 | 67 |
| Server Windows | W-01~W-64 | 64 |
| Layanan Web | WEB-01~WEB-26 | 26 |
| Perangkat Keamanan | S-01~S-23 | 23 |
| Perangkat Jaringan | N-01~N-38 | 38 |
| Sistem Kendali | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Perangkat Seluler | M-01~M-04 | 4 |
| Web Application | 21 kode | 21 |
| Virtualisasi | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Penilaian Administratif**: A-1~A-127 (127 item, 14 domain)
**Penilaian Fisik**: P-1~P-18 (18 item)

### 2. Panduan Keamanan AI — 54+ item

| Target | Jumlah Item | Siklus Hidup |
|--------|:----------:|-------------|
| Pengembang AI | 54 | 6 tahap (Perencanaan→Data→Pengembangan Model→Deployment→Pemantauan→Penghentian) |
| Penyedia Layanan AI | ~43 | 6 tahap (Perencanaan→Pengembangan→Operasi→Pemeliharaan→Umpan Balik→Penghentian) |
| Pengguna AI | 7 | Praktik terbaik keamanan |

### 3. Keamanan Robot — ~103 item

| Kategori | Kode | Jumlah Item | Standar Referensi |
|----------|------|:----------:|------------------|
| Pengembangan SW Aman (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Keamanan Rantai Pasok | SC-01~07 | 7 | NIST SP 800-161 |
| Identifikasi dan Otentikasi | IA-01~11 | 11 | IEC 62443 |
| Kontrol Penggunaan | UC-01~11 | 11 | IEC 62443 |
| Integritas Sistem | SI-01~11 | 11 | IEC 62443 |
| Perlindungan Data | DP-01~04 | 4 | IEC 62443 |
| Pembatasan Aliran Data | DFR-01~02 | 2 | IEC 62443 |
| Respons Kejadian | ER-01~03 | 3 | IEC 62443 |
| Ketersediaan Sumber Daya | RA-01~08 | 8 | IEC 62443 |
| Ketahanan Siber | CR-01~13 | 13 | EU CRA |
| Keamanan Nirkabel | WS-01~14 | 14 | EU RED |

Target: Robot industri / Robot layanan / Robot medis (ISO 8373)

### 4. Keamanan Ruang Angkasa — 53 item

| Bidang | Kode | Jumlah Item | Standar Referensi |
|--------|------|:----------:|------------------|
| Kontrol Akses | AC-01~12 | 12 | CMMC, K-RMF |
| Identifikasi dan Otentikasi | IA-01~02 | 2 | CMMC, NIS2 |
| Keamanan Sistem dan Komunikasi | SC-01~07 | 7 | NIST IR 8401 |
| Integritas Sistem dan Informasi | SI-01~04 | 4 | NIST CSF |
| Manajemen Operasi Sistem/Layanan | SO-01~09 | 9 | ISMS-P |
| Respons Insiden | IR-01~02 | 2 | NIS2 |
| Keamanan Personel | PS-01~02 | 2 | CMMC |
| Keamanan Fisik | PE-01~03 | 3 | K-RMF |
| Penilaian Risiko dan Keamanan | RA-01~02 | 2 | NIST CSF |
| Tata Kelola Keamanan | SG-01~04 | 4 | ISMS-P |
| Rencana Darurat | CP-01~02 | 2 | NIST IR 8270 |
| Manajemen Rantai Pasok | SM-01~04 | 4 | CMMC, NIS2 |

Target: Operator satelit, Penyedia GSaaS, Operator stasiun bumi, Perusahaan dalam rantai pasok ruang angkasa

### 5. Panduan Secure Coding — 46 item

| Kategori | Jumlah Item | Jumlah CWE | Standar Referensi |
|----------|:----------:|:--------:|------------------|
| Validasi dan Representasi Data Input | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Fungsi Keamanan | 16 | 16 | CWE/SANS Top 25 |
| Waktu dan Status | 2 | 3 | CWE |
| Penanganan Kesalahan | 3 | 3 | CWE |
| Kesalahan Kode | 3 | 3 | CWE |
| Enkapsulasi | 4 | 5 | CWE |
| Penyalahgunaan API | 2 | 1 | CWE |

**Bahasa yang Didukung:**
| Bahasa | Jumlah Item | Framework |
|--------|:----------:|-----------|
| Pseudo Code (Umum) | 46 | Pola yang tidak terikat bahasa |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Target: Pengembang web JavaScript/Python, Pengguna alat AI (Claude, Cursor, Copilot), Pengembang Vibe Coding

### 6. Keamanan Zero Trust — ~421 item

| Elemen Inti | Kode | Jumlah Item | Kematangan |
|-------------|------|:----------:|-----------|
| Identitas | ZT-ID-01~53 | 53 | Tradisional/Awal/Lanjutan/Optimal |
| Perangkat & Titik Akhir | ZT-DV-01~36 | 36 | Tradisional/Awal/Lanjutan/Optimal |
| Jaringan | ZT-NW-01~54 | 54 | Tradisional/Awal/Lanjutan/Optimal |
| Sistem | ZT-SY-01~49 | 49 | Tradisional/Awal/Lanjutan/Optimal |
| Aplikasi & Beban Kerja | ZT-AP-01~60 | 60 | Tradisional/Awal/Lanjutan/Optimal |
| Data | ZT-DA-01~58 | 58 | Tradisional/Awal/Lanjutan/Optimal |
| Visibilitas & Analitik | ZT-VA-01~43 | 43 | Tradisional/Awal/Lanjutan/Optimal |
| Otomatisasi & Orkestrasi | ZT-AU-01~43 | 43 | Tradisional/Awal/Lanjutan/Optimal |
| Khusus OT/ICS | ZT-OT-01~25 | 25 | Tradisional/Awal/Lanjutan/Optimal |

**4 Tingkat Kematangan**: Tradisional (Traditional) → Awal (Initial) → Lanjutan (Advanced) → Optimal (Optimal)
**Standar Referensi**: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Target: Organisasi yang mengadopsi Zero Trust, Lingkungan OT/ICS, Organisasi yang bermigrasi ke cloud, Penilai kematangan keamanan

### 7. Keamanan Rantai Pasokan SW (SBOM) — 29 item

| Fase | Kode | Jumlah Item | Standar |
|------|------|:----------:|---------|
| Desain | SC-01~05 | 5 | NIST SP 800-161r1 |
| Pengembangan | SC-06~16 | 11 | NIST SP 800-218 |
| Pasokan/Distribusi | SC-17~19 | 3 | NTIA SBOM |
| Deployment & Operasi | SC-20~26 | 7 | NIS-SBOM |
| Pemeliharaan | SC-27~29 | 3 | NIS-SBOM |

## Instalasi

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

## Penggunaan

```bash
# Memulai penilaian keamanan lengkap
/kesekit-start

# Menjalankan daftar periksa sebelum deployment
/kesekit-check

# Menghasilkan skrip hardening
/kesekit-fix

# Mendapatkan prompt secure coding
/kesekit-guide
```

---

## Struktur Proyek

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Metadata plugin
├── skills/                            ← Skill bahasa Inggris
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 baris)
│   │   ├── references/               ← Dokumen deskripsi/kriteria
│   │   │   ├── ai-security/          ← Ikhtisar, penyedia layanan, panduan pengguna
│   │   │   └── space-security/       ← Ikhtisar, skenario ancaman rantai pasok
│   │   ├── templates/                ← Formulir, tabel daftar periksa
│   │   │   ├── cii/                  ← 14 tabel pemeriksaan CII
│   │   │   ├── ai-security/          ← Daftar periksa pengembang AI, pengguna
│   │   │   ├── robot-security/       ← 6 daftar periksa keamanan robot
│   │   │   ├── space-security/       ← 4 tabel pemeriksaan ruang angkasa
│   │   │   └── zero-trust/           ← Tabel daftar periksa Zero Trust
│   │   └── scripts/                  ← Skrip pemeriksaan/perbaikan
│   │       ├── cii/                  ← bash, PowerShell, SQL
│   │       └── robot-security/       ← Firewall, SBOM, sertifikat
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skill bahasa Korea (struktur sama)
├── 문서/                              ← PDF asli
├── authorkit/                         ← Dokumen sumber dan hasil kerja
├── docs/                              ← README 20 bahasa
└── README.md
```

---

## Riwayat Perubahan

### v4.0.0 (2026-04-03)

**Pedoman Baru: Keamanan Zero Trust — ~421 item**
- Sumber: KISA Zero Trust Guideline 2.0 (245 hal) + Panduan Model Kematangan (182 hal) + Panduan Penerapan OT (67 hal)
- 9 elemen inti, ~421 item daftar periksa, 4 tingkat kematangan
- Standar: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

### v3.2.0 (2026-04-02)

**Pedoman Baru: Secure Coding**
- Sumber: KISA Javascript Secure Coding Guide 159 hal + Python Secure Coding Guide 176 hal (revisi 2023)
- 7 kategori, 46 item, 49 CWE
- JavaScript / Python / Pseudo Code (umum)

### v3.0.0 (2026-04-02)

**Breaking Change: Perubahan format perintah**
- Semua skill digabungkan ke namespace `kesekit` tunggal
- Format perintah: `/start` → `/kesekit-start`

**Pedoman Baru: Keamanan Ruang Angkasa**
- Sumber: Space Security Model Part1 134 hal + Part2 223 hal + Panduan Penjelasan 218 hal
- 12 bidang, 53 item daftar periksa

### v2.0.0 (2026-03-30)

**Refaktorisasi Struktur — Penerapan Pola Progressive Disclosure**

| Perubahan | Sebelum (v1.0) | Sesudah (v2.0) |
|-----------|---------------|----------------|
| SKILL.md | Semua pengetahuan inline (270~465 baris) | Hanya router (~50~80 baris) |
| Pedoman | Hanya mendukung CII | Mendukung CII + Keamanan AI |
| Penyimpanan pengetahuan | Hardcoded di SKILL.md | Dipisahkan ke `references/` (18 file) |
| Kode item | Hanya sebagian item | Seluruh item berdasarkan panduan 2026 |
| Skalabilitas | Menambah pedoman baru = menambah jumlah skill | 4 skill tetap, cukup tambah references |

**Pedoman Baru: Panduan Keamanan AI**
- Sumber: Kementerian Sains dan ICT / KISA 「Panduan Keamanan Kecerdasan Buatan (AI)」
- 54 item verifikasi untuk pengembang AI (siklus hidup 6 tahap)
- Persyaratan keamanan untuk penyedia layanan AI
- 7 praktik terbaik keamanan untuk pengguna AI

**Pembaruan Pedoman CII**
- Ekstraksi ulang seluruh item berdasarkan panduan detail 2026
- Penerapan sistem kode item (kode baru seperti WEB, HV, CA)

### v1.0.0 (2026-03-29)

- Rilis awal
- 4 skill penilaian kerentanan CII (Korea/Inggris)
- Item teknis (424) + administratif (127) + fisik (9)

---

## Dasar Hukum

- **Undang-Undang Perlindungan Infrastruktur Informasi dan Komunikasi** (Act on Protection of Information and Communications Infrastructure)
- **Undang-Undang Pemerintahan Elektronik** (e-Government Act)
- **Undang-Undang Perlindungan Informasi Pribadi** (Personal Information Protection Act)
- **Undang-Undang Dasar Kecerdasan Buatan** (AI Basic Act, berlaku 22 Januari 2026)

---

## Referensi Terkait

- [Panduan Detail Analisis dan Evaluasi Kerentanan Teknis KISA](https://www.kisa.or.kr)
- [Panduan Keamanan Kecerdasan Buatan (AI)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Dibangun Dengan

| Plugin | Deskripsi |
|--------|-----------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill pendukung penulisan buku - analisis PDF, ekstraksi struktur, revisi/penulisan ulang |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Kompatibilitas hook plugin Claude Code untuk lingkungan Windows |

---

## Lisensi

MIT License

## Pembuat

CDPP Corp (https://github.com/cdppcorp)
