🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Kritik Bilgi Altyapisi (CII) zafiyet analiz-degerlendirmesi, AI guvenlik degerlendirmesi, robot guvenligi, uzay guvenligi, guvenli kodlama kilavuzu, Sifir Guven (Zero Trust) guvenlik degerlendirmesi ve SW Tedarik Zinciri Guvenligi (SBOM) icin Claude Code beceri eklentisidir.

---

## Genel Bakis

KESE (KISA Enhanced Security Evaluation Kit), KISA (Kore Internet ve Guvenlik Ajansi) kilavuzlarina dayali kapsamli guvenlik zafiyet degerlendirme yetenekleri sunan bir Claude Code eklentisidir. Kritik Bilgi Altyapisi (CII), AI Guvenlik, Robot Guvenligi, Uzay Guvenligi, Guvenli Kodlama ve Sifir Guven (Zero Trust) degerlendirmelerini destekler.

## Ozellikler

| Beceri | Aciklama |
|--------|----------|
| `/kesekit-start` | Tam guvenlik zafiyet degerlendirmesi calistir (CII 560+ / AI Guvenlik / Robot Guvenligi / Uzay Guvenligi / Guvenli Kodlama / Sifir Guven / SW Tedarik Zinciri) |
| `/kesekit-check` | Dagitim oncesi guvenlik uyumluluk kontrol listesi (CII / AI / Robot / Uzay / Guvenli Kodlama / Sifir Guven / SW Tedarik Zinciri) |
| `/kesekit-fix` | Sikilastirma betikleri ve guvenlik duzeltmeleri otomatik olustur (CII / AI / Robot / Uzay / Guvenli Kodlama / Sifir Guven / SW Tedarik Zinciri) |
| `/kesekit-guide` | AI araclari icin guvenli kodlama komut istemi olustur (CII / AI / Robot / Uzay / JS·Python·Genel / Sifir Guven / SW Tedarik Zinciri) |

## Desteklenen Kilavuzlar

### 1. CII (Kritik Bilgi Altyapisi) — 560+ madde

**Teknik Degerlendirme**
| Sistem | Kod | Madde |
|--------|-----|:-----:|
| Unix/Linux Sunucu | U-01~U-67 | 67 |
| Windows Sunucu | W-01~W-64 | 64 |
| Web Hizmeti | WEB-01~WEB-26 | 26 |
| Guvenlik Ekipmani | S-01~S-23 | 23 |
| Ag Ekipmani | N-01~N-38 | 38 |
| Kontrol Sistemi | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobil | M-01~M-04 | 4 |
| Web Application | 21 kod | 21 |
| Sanallastirma | HV-01~HV-25 | 25 |
| Bulut | CA-01~CA-19 | 19 |

**Yonetimsel Degerlendirme**: A-1~A-127 (127 madde, 14 alan)
**Fiziksel Degerlendirme**: P-1~P-18 (18 madde)

### 2. AI Guvenlik Kilavuzu — 54+ madde

| Hedef Kitle | Madde | Yasam Dongusu |
|-------------|:-----:|---------------|
| AI Gelistirici | 54 | 6 asama (Planlama→Veri→Model→Dagitim→Izleme→Tasfiye) |
| Hizmet Saglayici | ~43 | 6 asama (Planlama→Gelistirme→Isletme→Bakim→Geri Bildirim→Tasfiye) |
| Kullanici | 7 | Guvenlik en iyi uygulamalari |

### 3. Robot Guvenligi — ~103 madde

| Kategori | Kod | Madde | Referans Standart |
|----------|-----|:-----:|-------------------|
| Guvenli SW Gelistirme (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Tedarik Zinciri Guvenligi | SC-01~07 | 7 | NIST SP 800-161 |
| Tanimlama ve Kimlik Dogrulama | IA-01~11 | 11 | IEC 62443 |
| Kullanim Kontrolu | UC-01~11 | 11 | IEC 62443 |
| Sistem Butunlugu | SI-01~11 | 11 | IEC 62443 |
| Veri Koruma | DP-01~04 | 4 | IEC 62443 |
| Veri Akisi Kisitlamasi | DFR-01~02 | 2 | IEC 62443 |
| Olay Mudahalesi | ER-01~03 | 3 | IEC 62443 |
| Kaynak Erisilebilirligi | RA-01~08 | 8 | IEC 62443 |
| Siber Dayaniklilik | CR-01~13 | 13 | EU CRA |
| Kablosuz Guvenlik | WS-01~14 | 14 | EU RED |

Hedef Kitle: Endustriyel / hizmet / tibbi robotlar (ISO 8373)

### 4. Uzay Guvenligi — 53 madde

| Alan | Kod | Madde | Referans Standart |
|------|-----|:-----:|-------------------|
| Erisim Kontrolu | AC-01~12 | 12 | CMMC, K-RMF |
| Tanimlama ve Kimlik Dogrulama | IA-01~02 | 2 | CMMC, NIS2 |
| Sistem ve Iletisim Guvenligi | SC-01~07 | 7 | NIST IR 8401 |
| Sistem ve Bilgi Butunlugu | SI-01~04 | 4 | NIST CSF |
| Sistem/Hizmet Isletme Yonetimi | SO-01~09 | 9 | ISMS-P |
| Olay Mudahalesi | IR-01~02 | 2 | NIS2 |
| Personel Guvenligi | PS-01~02 | 2 | CMMC |
| Fiziksel Guvenlik | PE-01~03 | 3 | K-RMF |
| Risk ve Guvenlik Degerlendirmesi | RA-01~02 | 2 | NIST CSF |
| Guvenlik Yonetisimi | SG-01~04 | 4 | ISMS-P |
| Acil Durum Planlari | CP-01~02 | 2 | NIST IR 8270 |
| Tedarik Zinciri Yonetimi | SM-01~04 | 4 | CMMC, NIS2 |

Hedef Kitle: Uydu operatorleri, GSaaS saglayicilari, yer istasyonu operatorleri, uzay tedarik zinciri sirketleri

### 5. Guvenli Kodlama Kilavuzu — 46 madde

| Kategori | Madde | CWE | Referans Standart |
|----------|:-----:|:---:|-------------------|
| Giris Verisi Dogrulama ve Temsil | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Guvenlik Islevleri | 16 | 16 | CWE/SANS Top 25 |
| Zaman ve Durum | 2 | 3 | CWE |
| Hata Yonetimi | 3 | 3 | CWE |
| Kod Hatalari | 3 | 3 | CWE |
| Kapsulleme | 4 | 5 | CWE |
| API Kotuye Kullanimi | 2 | 1 | CWE |

**Desteklenen Diller:**
| Dil | Madde | Cerceve |
|-----|:-----:|---------|
| Pseudo Code (genel) | 46 | Dilden bagimsiz kaliplar |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Hedef Kitle: JavaScript/Python web gelistiricileri, AI arac (Claude, Cursor, Copilot) kullanicilari, vibe coding gelistiricileri

### 6. Sifir Guven (Zero Trust) Guvenligi — ~421 madde

| Temel Oge | Kod | Madde | Olgunluk |
|-----------|-----|:-----:|----------|
| Kimlik | ZT-ID-01~53 | 53 | Geleneksel/Baslangic/Gelismis/Optimal |
| Cihaz ve Uc Nokta | ZT-DV-01~36 | 36 | Geleneksel/Baslangic/Gelismis/Optimal |
| Ag | ZT-NW-01~54 | 54 | Geleneksel/Baslangic/Gelismis/Optimal |
| Sistem | ZT-SY-01~49 | 49 | Geleneksel/Baslangic/Gelismis/Optimal |
| Uygulama ve Is Yuku | ZT-AP-01~60 | 60 | Geleneksel/Baslangic/Gelismis/Optimal |
| Veri | ZT-DA-01~58 | 58 | Geleneksel/Baslangic/Gelismis/Optimal |
| Gorunurluk ve Analitik | ZT-VA-01~43 | 43 | Geleneksel/Baslangic/Gelismis/Optimal |
| Otomasyon ve Orkestrasyon | ZT-AU-01~43 | 43 | Geleneksel/Baslangic/Gelismis/Optimal |
| OT/ICS Ozel | ZT-OT-01~25 | 25 | Geleneksel/Baslangic/Gelismis/Optimal |

**4 Olgunluk Duzeyi**: Geleneksel (Traditional) → Baslangic (Initial) → Gelismis (Advanced) → Optimal (Optimal)
**Referans Standartlar**: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Hedef Kitle: Sifir Guven benimseyen kuruluslar, OT/ICS ortamlari, buluta gecis yapan organizasyonlar, guvenlik olgunluk degerlendirme sorumlulari

### 7. SW Tedarik Zinciri Guvenligi (SBOM) — 29 madde

| Asama | Kod | Madde | Standart |
|-------|-----|:-----:|----------|
| Tasarim | SC-01~05 | 5 | NIST SP 800-161r1 |
| Gelistirme | SC-06~16 | 11 | NIST SP 800-218 |
| Tedarik/Dagitim | SC-17~19 | 3 | NTIA SBOM |
| Dagitim ve Isletme | SC-20~26 | 7 | NIS-SBOM |
| Bakim | SC-27~29 | 3 | NIS-SBOM |

## Kurulum

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

## Kullanim

```bash
# Tam guvenlik degerlendirmesini baslat
/kesekit-start

# Dagitim oncesi kontrol listesini calistir
/kesekit-check

# Sikilastirma betikleri olustur
/kesekit-fix

# Guvenli kodlama komut istemlerini al
/kesekit-guide
```

---

## Proje Yapisi

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Eklenti meta verileri
├── skills/                            ← Ingilizce beceriler
│   ├── start/
│   │   ├── SKILL.md                  ← Yonlendirici (~80 satir)
│   │   ├── references/               ← Tanimlayici/normatif belgeler
│   │   │   ├── ai-security/          ← Genel bakis, saglayicilar, kullanici kilavuzu
│   │   │   └── space-security/       ← Genel bakis, tehdit senaryolari
│   │   ├── templates/                ← Formlar, kontrol listesi tablolari
│   │   │   ├── cii/                  ← CII 14 denetim tablosu
│   │   │   ├── ai-security/          ← AI gelistirici dogrulamasi, kullanici kontrol listesi
│   │   │   ├── robot-security/       ← Robot guvenligi 6 kontrol listesi
│   │   │   ├── space-security/       ← Uzay guvenligi 4 denetim tablosu
│   │   │   └── zero-trust/           ← Sifir Guven denetim tablolari
│   │   └── scripts/                  ← Calistirilabilir denetim/duzeltme betikleri
│   │       ├── cii/                  ← bash, PowerShell, SQL betikleri
│   │       └── robot-security/       ← Guvenlik duvari, SBOM, sertifika betikleri
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Korece beceriler (ayni yapi)
├── 문서/                              ← Orijinal PDF'ler
├── authorkit/                         ← Orijinal belgeler ve ciktilar
├── docs/                              ← 20 dilde README
├── CONTRIBUTING.md                    ← Kilavuz ekleme yontemi
└── README.md
```

---

## Degisiklik Gecmisi

### v4.0.0 (2026-04-03)

**Yeni Kilavuz Eklendi: Sifir Guven (Zero Trust) Guvenligi**
- Kaynak: KISA Zero Trust Guideline 2.0 (245 sayfa) + Zero Trust Olgunluk Modeli (182 sayfa) + OT icin Zero Trust Kilavuzu (67 sayfa)
- 9 temel oge, ~421 denetim maddesi, 4 olgunluk duzeyi
- OT/ICS ozel destek (ZT-OT-01~25)
- Standartlar: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

### v3.2.0 (2026-04-02)

**Yeni Kilavuz Eklendi: Guvenli Kodlama Kilavuzu**
- Kaynak: KISA Javascript Secure Coding Guide 159 sayfa + Python Secure Coding Guide 176 sayfa (2023 revizyonu)
- 7 kategori, 46 madde, 49 CWE eslesmesi
- Genel Pseudo Code kilavuzu yeni olusturuldu (dilden bagimsiz UNSAFE/SAFE kaliplari)
- JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy) cerceve kod ornekleri

### v3.0.0 (2026-04-02)

**Uyumsuz Degisiklik: komut formati guncellendi**
- Tum beceriler tek `kesekit` ad alaninda birlesti
- Komut formati: `/start` → `/kesekit-start` (ad alani oneki eklendi)

**Yeni Kilavuz Eklendi: Uzay Guvenligi**
- Kaynak: Uzay Guvenlik Modeli Part1 134 sayfa + Part2 223 sayfa + Aciklama Kilavuzu 218 sayfa (MSIT/KISA)
- 12 alan, 53 kontrol listesi maddesi
- Hedef Kitle: Uydu operatorleri, GSaaS saglayicilari, yer istasyonu operatorleri

### v2.0.0 (2026-03-30)

**Yapisal Yeniden Duzenleme — Progressive Disclosure Deseni Uygulandi**

| Degisiklik | Onceki (v1.0) | Sonraki (v2.0) |
|-----------|--------------|----------------|
| SKILL.md | Tum bilgi satir ici (270~465 satir) | Yalnizca yonlendirici (~50~80 satir) |
| Kilavuzlar | Yalnizca CII destegi | CII + AI Guvenlik destegi |
| Bilgi depolama | SKILL.md icinde sabit kodlanmis | `references/` olarak ayrilmis (18 dosya) |
| Madde kodlari | Yalnizca bazi maddeler dahil | 2026 kilavuzuna dayali tum maddeler |
| Genisletilebilirlik | Yeni kilavuz eklerken beceri sayisi artar | Beceriler 4'te sabit, yalnizca references eklenir |

**Yeni Kilavuz Eklendi: AI Guvenlik Kilavuzu**
- Kaynak: Bilim ve ICT Bakanligi · KISA 「Yapay Zeka (AI) Guvenlik Kilavuzu」
- AI Gelistirici 54 dogrulama maddesi (6 asamali yasam dongusu)
- AI Hizmet Saglayici guvenlik gereksinimleri
- AI Kullanici guvenlik kurallari 7 madde

**CII Kilavuzu Guncellemesi**
- 2026 ayrintili kilavuzuna dayali olarak tum maddeler yeniden cikarildi
- Madde kod sistemi yansitildi (WEB, HV, CA vb. yeni kodlar)

### v1.0.0 (2026-03-29)

- Ilk surum
- CII zafiyet analiz-degerlendirmesi 4 beceri (Korece/Ingilizce)
- Teknik (424) + Yonetimsel (127) + Fiziksel (9) madde

---

## Yasal Dayanak

- **Bilgi ve Iletisim Altyapisi Koruma Kanunu** (Act on Protection of Information and Communications Infrastructure)
- **e-Devlet Kanunu** (e-Government Act)
- **Kisisel Bilgi Koruma Kanunu** (Personal Information Protection Act)
- **Yapay Zeka Temel Kanunu** (AI Basic Act, 2026.1.22 tarihinde yururluge girmistir)

---

## Ilgili Kaynaklar

- [KISA Teknik Zafiyet Analiz-Degerlendirme Ayrintili Kilavuzu](https://www.kisa.or.kr)
- [Yapay Zeka (AI) Guvenlik Kilavuzu](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Built With

| Eklenti | Aciklama |
|---------|----------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Kitap yazarligi destek becerisi - PDF analizi, yapi cikarma, duzeltme/yeniden yazma |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Windows ortami Claude Code eklenti kanca uyumlulugu |

---

## License

MIT License

## Author

CDPP Corp (https://github.com/cdppcorp)
