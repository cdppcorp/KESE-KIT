🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin Claude Code untuk analisis dan evaluasi kerentanan Infrastruktur Informasi Kritis (CII) serta evaluasi keamanan AI berdasarkan pedoman KISA (Badan Internet dan Keamanan Korea).

---

## Ikhtisar

KESE (KISA Enhanced Security Evaluation Kit) adalah plugin Claude Code yang menyediakan kemampuan penilaian kerentanan keamanan secara menyeluruh berdasarkan pedoman KISA (Badan Internet dan Keamanan Korea). Mendukung penilaian Infrastruktur Informasi Kritis (CII) maupun penilaian Keamanan AI.

## Fitur

| Skill | Deskripsi |
|-------|-----------|
| `/kesekit:start` | Menjalankan penilaian kerentanan keamanan lengkap (CII 560+ item atau AI Security) |
| `/kesekit:check` | Daftar periksa kepatuhan keamanan sebelum deployment |
| `/kesekit:fix` | Menghasilkan skrip hardening dan perbaikan keamanan secara otomatis |
| `/kesekit:guide` | Membuat prompt secure coding untuk alat AI |

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

## Instalasi

```bash
claude plugins install kesekit
```

## Penggunaan

```bash
# Memulai penilaian keamanan lengkap
/kesekit:start

# Menjalankan daftar periksa sebelum deployment
/kesekit:check

# Menghasilkan skrip hardening
/kesekit:fix

# Mendapatkan prompt secure coding
/kesekit:guide
```

---

## Struktur Proyek

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Metadata plugin
├── skills/                            ← Skill bahasa Inggris (router)
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 baris)
│   │   └── references/               ← Basis pengetahuan per pedoman
│   │       ├── cii/                  ← 14 referensi CII
│   │       └── ai-security/          ← 4 referensi keamanan AI
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skill bahasa Korea (struktur sama)
├── authorkit/                         ← Dokumen sumber dan hasil kerja
│   ├── converted/
│   │   ├── ref-001/                  ← Panduan administratif & fisik (full.md)
│   │   ├── ref-002/                  ← Panduan teknis (full.md)
│   │   └── ref-003/                  ← Panduan keamanan AI (full.md)
│   └── ...
├── 문서/                              ← PDF asli
└── README.md
```

---

## Riwayat Perubahan

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
