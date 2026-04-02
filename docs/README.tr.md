🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Kritik Bilgi Altyapısı (CII) zafiyet analiz-değerlendirmesi ve AI güvenlik değerlendirmesi için Claude Code beceri eklentisidir.

---

## Genel Bakış

KESE (KISA Enhanced Security Evaluation Kit), KISA (Kore İnternet ve Güvenlik Ajansı) kılavuzlarına dayalı kapsamlı güvenlik zafiyet değerlendirme yetenekleri sunan bir Claude Code eklentisidir. Hem Kritik Bilgi Altyapısı (CII) hem de AI Güvenlik değerlendirmelerini destekler.

## Özellikler

| Beceri | Açıklama |
|--------|----------|
| `/kesekit-start` | Tam güvenlik zafiyet değerlendirmesi çalıştır (CII 560+ madde veya AI Güvenlik) |
| `/kesekit-check` | Dağıtım öncesi güvenlik uyumluluk kontrol listesi |
| `/kesekit-fix` | Sıkılaştırma betikleri ve güvenlik düzeltmeleri otomatik oluştur |
| `/kesekit-guide` | AI araçları için güvenli kodlama komut istemi oluştur |

## Desteklenen Kılavuzlar

### 1. CII (Kritik Bilgi Altyapısı) — 560+ madde

**Teknik Değerlendirme**
| Sistem | Kod | Madde |
|--------|-----|:-----:|
| Unix/Linux Sunucu | U-01~U-67 | 67 |
| Windows Sunucu | W-01~W-64 | 64 |
| Web Hizmeti | WEB-01~WEB-26 | 26 |
| Güvenlik Ekipmanı | S-01~S-23 | 23 |
| Ağ Ekipmanı | N-01~N-38 | 38 |
| Kontrol Sistemi | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobil | M-01~M-04 | 4 |
| Web Application | 21 kod | 21 |
| Sanallaştırma | HV-01~HV-25 | 25 |
| Bulut | CA-01~CA-19 | 19 |

**Yönetimsel Değerlendirme**: A-1~A-127 (127 madde, 14 alan)
**Fiziksel Değerlendirme**: P-1~P-18 (18 madde)

### 2. AI Güvenlik Kılavuzu — 54+ madde

| Hedef Kitle | Madde | Yaşam Döngüsü |
|-------------|:-----:|---------------|
| AI Geliştirici | 54 | 6 aşama (Planlama→Veri→Model→Dağıtım→İzleme→Tasfiye) |
| Hizmet Sağlayıcı | ~43 | 6 aşama (Planlama→Geliştirme→İşletme→Bakım→Geri Bildirim→Tasfiye) |
| Kullanıcı | 7 | Güvenlik en iyi uygulamaları |

## Kurulum

```bash
claude plugins install kesekit
```

## Kullanım

```bash
# Tam güvenlik değerlendirmesini başlat
/kesekit-start

# Dağıtım öncesi kontrol listesini çalıştır
/kesekit-check

# Sıkılaştırma betikleri oluştur
/kesekit-fix

# Güvenli kodlama komut istemlerini al
/kesekit-guide
```

---

## Proje Yapısı

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Eklenti meta verileri
├── skills/                            ← İngilizce beceriler (yönlendirici)
│   ├── start/
│   │   ├── SKILL.md                  ← Yönlendirici (~80 satır)
│   │   └── references/               ← Kılavuz bazlı bilgi
│   │       ├── cii/                  ← CII 14 referans
│   │       └── ai-security/          ← AI güvenlik 4 referans
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Korece beceriler (aynı yapı)
├── authorkit/                         ← Orijinal belgeler ve çıktılar
│   ├── converted/
│   │   ├── ref-001/                  ← Yönetimsel/fiziksel kılavuz (full.md)
│   │   ├── ref-002/                  ← Teknik kılavuz (full.md)
│   │   └── ref-003/                  ← AI güvenlik kılavuzu (full.md)
│   └── ...
├── 문서/                              ← Orijinal PDF'ler
└── README.md
```

---

## Değişiklik Geçmişi

### v2.0.0 (2026-03-30)

**Yapısal Yeniden Düzenleme — Progressive Disclosure Deseni Uygulandı**

| Değişiklik | Önceki (v1.0) | Sonraki (v2.0) |
|-----------|--------------|----------------|
| SKILL.md | Tüm bilgi satır içi (270~465 satır) | Yalnızca yönlendirici (~50~80 satır) |
| Kılavuzlar | Yalnızca CII desteği | CII + AI Güvenlik desteği |
| Bilgi depolama | SKILL.md içinde sabit kodlanmış | `references/` olarak ayrılmış (18 dosya) |
| Madde kodları | Yalnızca bazı maddeler dahil | 2026 kılavuzuna dayalı tüm maddeler |
| Genişletilebilirlik | Yeni kılavuz eklerken beceri sayısı artar | Beceriler 4'te sabit, yalnızca references eklenir |

**Yeni Kılavuz Eklendi: AI Güvenlik Kılavuzu**
- Kaynak: Bilim ve ICT Bakanlığı · KISA 「Yapay Zeka (AI) Güvenlik Kılavuzu」
- AI Geliştirici 54 doğrulama maddesi (6 aşamalı yaşam döngüsü)
- AI Hizmet Sağlayıcı güvenlik gereksinimleri
- AI Kullanıcı güvenlik kuralları 7 madde

**CII Kılavuzu Güncellemesi**
- 2026 ayrıntılı kılavuzuna dayalı olarak tüm maddeler yeniden çıkarıldı
- Madde kod sistemi yansıtıldı (WEB, HV, CA vb. yeni kodlar)

### v1.0.0 (2026-03-29)

- İlk sürüm
- CII zafiyet analiz-değerlendirmesi 4 beceri (Korece/İngilizce)
- Teknik (424) + Yönetimsel (127) + Fiziksel (9) madde

---

## Yasal Dayanak

- **Bilgi ve İletişim Altyapısı Koruma Kanunu** (Act on Protection of Information and Communications Infrastructure)
- **e-Devlet Kanunu** (e-Government Act)
- **Kişisel Bilgi Koruma Kanunu** (Personal Information Protection Act)
- **Yapay Zeka Temel Kanunu** (AI Basic Act, 2026.1.22 tarihinde yürürlüğe girmiştir)

---

## İlgili Kaynaklar

- [KISA Teknik Zafiyet Analiz-Değerlendirme Ayrıntılı Kılavuzu](https://www.kisa.or.kr)
- [Yapay Zeka (AI) Güvenlik Kılavuzu](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Built With

| Eklenti | Açıklama |
|---------|----------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Kitap yazarlığı destek becerisi - PDF analizi, yapı çıkarma, düzeltme/yeniden yazma |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Windows ortamı Claude Code eklenti kanca uyumluluğu |

---

## License

MIT License

## Author

CDPP Corp (https://github.com/cdppcorp)
