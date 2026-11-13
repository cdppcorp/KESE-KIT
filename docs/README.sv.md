🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Ett Claude Code skill-plugin for sarbarhetsanalys av kritisk informationsinfrastruktur (CII), AI-sakerhetsutvardering, robotsakerhet, rymdsakerhet, saker kodning, Zero Trust-utvardering och SW-leveranskedjesakerhet (SBOM).

---

## Oversikt

KESE (KISA Enhanced Security Evaluation Kit) ar ett Claude Code-plugin som erbjuder omfattande funktioner for sarbarhetsanalys baserad pa KISA:s (Korea Internet & Security Agency) riktlinjer. Det stoder utvarderingar av kritisk informationsinfrastruktur (CII), AI-sakerhet, robotsakerhet, rymdsakerhet, saker kodning och Zero Trust-utvardering.

## Funktioner

| Skill | Beskrivning |
|-------|-------------|
| `/kesekit-start` | Kor fullstandig sakerhetsarbarhetsanalys (CII 560+ / AI / Robot / Rymd / Saker kodning / Zero Trust / SW-leveranskedja) |
| `/kesekit-check` | Sakerhetschecklista for efterlevnad fore driftsattning (CII / AI / Robot / Rymd / Saker kodning / Zero Trust / SW-leveranskedja) |
| `/kesekit-fix` | Generera hardening-skript och sakerhetsatgarder automatiskt (CII / AI / Robot / Rymd / Saker kodning / Zero Trust / SW-leveranskedja) |
| `/kesekit-guide` | Generera secure coding-promptar for AI-verktyg (CII / AI / Robot / Rymd / JS·Python·Allman / Zero Trust / SW-leveranskedja) |

## Riktlinjer som stods

### 1. CII (Kritisk informationsinfrastruktur) — 560+ objekt

**Teknisk sarbarhetsutvarding**
| System | Kod | Antal objekt |
|--------|-----|:------:|
| Unix/Linux-server | U-01~U-67 | 67 |
| Windows-server | W-01~W-64 | 64 |
| Webbtjanst | WEB-01~WEB-26 | 26 |
| Sakerhetsutrustning | S-01~S-23 | 23 |
| Natverksutrustning | N-01~N-38 | 38 |
| Styrsystem | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobil | M-01~M-04 | 4 |
| Web Application | 21 koder | 21 |
| Virtualisering | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Administrativ sarbarhetsutvarding**: A-1~A-127 (127 objekt, 14 domaner)
**Fysisk sarbarhetsutvarding**: P-1~P-18 (18 objekt)

### 2. AI-sakerhetsguide — 54+ objekt

| Malgrupp | Antal objekt | Livscykel |
|----------|:------:|---------|
| AI-utvecklare | 54 | 6 faser (Planering→Data→Modellutveckling→Driftsattning→Overvakning→Avveckling) |
| AI-tjanstleverantor | ~43 | 6 faser (Planering→Utveckling→Drift→Underhall→Aterrapportering→Avveckling) |
| AI-anvandare | 7 | Sakerhetsriktlinjer |

### 3. Robotsakerhet — ~103 objekt

| Kategori | Kod | Antal objekt | Referensstandard |
|----------|-----|:------:|-----------------|
| Saker SW-utveckling (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Leveranskedjesakerhet | SC-01~07 | 7 | NIST SP 800-161 |
| Identifiering och autentisering | IA-01~11 | 11 | IEC 62443 |
| Anvandningskontroll | UC-01~11 | 11 | IEC 62443 |
| Systemintegritet | SI-01~11 | 11 | IEC 62443 |
| Dataskydd | DP-01~04 | 4 | IEC 62443 |
| Begransning av dataflode | DFR-01~02 | 2 | IEC 62443 |
| Incidentrespons | ER-01~03 | 3 | IEC 62443 |
| Resurstillganglighet | RA-01~08 | 8 | IEC 62443 |
| Cyberresiliens | CR-01~13 | 13 | EU CRA |
| Tradlos sakerhet | WS-01~14 | 14 | EU RED |

Malgrupp: Industrirobotar / Tjensterobotar / Medicinska robotar (ISO 8373)

### 4. Rymdsakerhet — 53 objekt

| Omrade | Kod | Antal objekt | Referensstandard |
|--------|-----|:------:|-----------------|
| Atkomstkontroll | AC-01~12 | 12 | CMMC, K-RMF |
| Identifiering och autentisering | IA-01~02 | 2 | CMMC, NIS2 |
| System- och kommunikationssakerhet | SC-01~07 | 7 | NIST IR 8401 |
| System- och informationsintegritet | SI-01~04 | 4 | NIST CSF |
| System-/tjanstdriftsforvaltning | SO-01~09 | 9 | ISMS-P |
| Incidentrespons | IR-01~02 | 2 | NIS2 |
| Personalsakerhet | PS-01~02 | 2 | CMMC |
| Fysisk sakerhet | PE-01~03 | 3 | K-RMF |
| Risk- och sakerhetsbedomning | RA-01~02 | 2 | NIST CSF |
| Sakerhetsstyrning | SG-01~04 | 4 | ISMS-P |
| Beredskapsplan | CP-01~02 | 2 | NIST IR 8270 |
| Leveranskedjehantering | SM-01~04 | 4 | CMMC, NIS2 |

Malgrupp: Satellitoperatorer, GSaaS-leverantorer, Markstationsoperatorer, Foretag i rymdleveranskedjan

### 5. Guide for saker kodning — 46 objekt

| Kategori | Antal objekt | Antal CWE | Referensstandard |
|----------|:------:|:------:|-----------------|
| Indatavalidering och -representation | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Sakerhetsfunktioner | 16 | 16 | CWE/SANS Top 25 |
| Tid och tillstand | 2 | 3 | CWE |
| Felhantering | 3 | 3 | CWE |
| Kodfel | 3 | 3 | CWE |
| Inkapsling | 4 | 5 | CWE |
| API-missbruk | 2 | 1 | CWE |

**Sprak som stods:**
| Sprak | Antal objekt | Ramverk |
|-------|:------:|---------|
| Pseudo Code (Allman) | 46 | Sprakobeorende monster |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Malgrupp: JavaScript/Python-webbutvecklare, AI-verktygsanvandare (Claude, Cursor, Copilot), Vibe Coding-utvecklare

### 6. Zero Trust-sakerhet — ~421 objekt

| Karnelement | Kod | Antal objekt | Mognad |
|-------------|-----|:------:|--------|
| Identitet | ZT-ID-01~53 | 53 | Traditionell/Initial/Avancerad/Optimal |
| Enhet & Andpunkt | ZT-DV-01~36 | 36 | Traditionell/Initial/Avancerad/Optimal |
| Natverk | ZT-NW-01~54 | 54 | Traditionell/Initial/Avancerad/Optimal |
| System | ZT-SY-01~49 | 49 | Traditionell/Initial/Avancerad/Optimal |
| Applikation & Arbetsbelastning | ZT-AP-01~60 | 60 | Traditionell/Initial/Avancerad/Optimal |
| Data | ZT-DA-01~58 | 58 | Traditionell/Initial/Avancerad/Optimal |
| Synlighet & Analys | ZT-VA-01~43 | 43 | Traditionell/Initial/Avancerad/Optimal |
| Automatisering & Orkestrering | ZT-AU-01~43 | 43 | Traditionell/Initial/Avancerad/Optimal |
| OT/ICS-specifik | ZT-OT-01~25 | 25 | Traditionell/Initial/Avancerad/Optimal |

**4 mognadsnivder**: Traditionell (Traditional) → Initial (Initial) → Avancerad (Advanced) → Optimal (Optimal)
**Referensstandarder**: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Malgrupp: Organisationer som infor Zero Trust, OT/ICS-miljoer, Organisationer som migrerar till molnet, Ansvariga for sakerhetsmognadsbedomning

### 7. SW-leveranskedjesakerhet (SBOM) — 29 objekt

| Fas | Kod | Antal objekt | Standard |
|-----|-----|:------:|----------|
| Design | SC-01~05 | 5 | NIST SP 800-161r1 |
| Utveckling | SC-06~16 | 11 | NIST SP 800-218 |
| Leverans/Distribution | SC-17~19 | 3 | NTIA SBOM |
| Driftsattning & Drift | SC-20~26 | 7 | NIS-SBOM |
| Underhall | SC-27~29 | 3 | NIS-SBOM |

## Installation

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

## Anvandning

```bash
# Starta fullstandig sakerhetsutvardering
/kesekit-start

# Kor checklista fore driftsattning
/kesekit-check

# Generera hardening-skript
/kesekit-fix

# Hamta secure coding-promptar
/kesekit-guide
```

---

## Projektstruktur

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Plugin-metadata
├── skills/                            ← Engelska skills
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 rader)
│   │   ├── references/               ← Beskrivnings-/kriteriedokument
│   │   │   ├── ai-security/          ← Oversikt, tjanstleverantorer, anvandarguide
│   │   │   └── space-security/       ← Oversikt, hotscenarier for leveranskedja
│   │   ├── templates/                ← Formulir, checklisttabeller
│   │   │   ├── cii/                  ← CII 14 inspektionstabeller
│   │   │   ├── ai-security/          ← AI-utvecklare, anvandarchecklistor
│   │   │   ├── robot-security/       ← 6 robotsakerhetschecklistor
│   │   │   ├── space-security/       ← 4 rymdsakerhetstabeller
│   │   │   └── zero-trust/           ← Zero Trust-checklisttabeller
│   │   └── scripts/                  ← Inspektions-/atgardsskript
│   │       ├── cii/                  ← bash, PowerShell, SQL
│   │       └── robot-security/       ← Brandvagg, SBOM, certifikat
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Koreanska skills (samma struktur)
├── 문서/                              ← Original-PDF:er
├── authorkit/                         ← Kalldokument och arbetsprodukter
├── docs/                              ← README pa 20 sprak
└── README.md
```

---

## Andringshistorik

### v4.0.0 (2026-04-03)

**Ny riktlinje: Zero Trust-sakerhet — ~421 objekt**
- Kalla: KISA Zero Trust Guideline 2.0 (245 sid.) + Mognadsmodellguide (182 sid.) + OT-implementeringsguide (67 sid.)
- 9 karnelement, ~421 checklistobjekt, 4 mognadsnivder
- Standarder: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

### v3.2.0 (2026-04-02)

**Ny riktlinje: Saker kodning**
- Kalla: KISA Javascript Secure Coding Guide 159 sid. + Python Secure Coding Guide 176 sid. (2023 ars revision)
- 7 kategorier, 46 objekt, 49 CWE
- JavaScript / Python / Pseudo Code (allman)

### v3.0.0 (2026-04-02)

**Breaking Change: Andrat kommandoformat**
- Alla skills samlade i en enda `kesekit`-namnrymd
- Kommandoformat: `/start` → `/kesekit-start`

**Ny riktlinje: Rymdsakerhet**
- Kalla: Space Security Model Part1 134 sid. + Part2 223 sid. + Forklaringsguide 218 sid.
- 12 omraden, 53 checklistobjekt

### v2.0.0 (2026-03-30)

**Strukturomarbetning — Progressive Disclosure-monster tillampad**

| Andring | Tidigare (v1.0) | Nuvarande (v2.0) |
|---------|------------|------------|
| SKILL.md | All kunskap inline (270~465 rader) | Enbart router (~50~80 rader) |
| Riktlinjer | Enbart CII | CII + AI-sakerhet |
| Kunskapslagring | Hardkodad i SKILL.md | Separerad i `references/` (18 filer) |
| Objektkoder | Enbart nagra objekt inkluderade | Alla objekt baserade pa 2026-guiden |
| Skalbarhet | Fler skills kravs vid nya riktlinjer | 4 skills fasta, enbart references tillaggs |

**Ny riktlinje tillagd: AI-sakerhetsguide**
- Kalla: Ministeriet for vetenskap och ICT / KISA "Artificial Intelligence (AI) Security Guide"
- 54 verifieringsobjekt for AI-utvecklare (6-faser livscykel)
- Sakerhetskrav for AI-tjanstleverantorer
- 7 sakerhetsriktlinjer for AI-anvandare

**CII-riktlinjeuppdatering**
- Alla objekt omextraherade baserat pa den detaljerade guiden fran 2026
- Nytt kodsystem avspelgat (WEB, HV, CA och andra nya koder)

### v1.0.0 (2026-03-29)

- Forsta utgavan
- 4 CII-sarbarhetsanalys-skills (koreanska/engelska)
- Tekniskt (424) + Administrativt (127) + Fysiskt (9) objekt

---

## Rattslig grund

- **Lag om skydd av informations- och kommunikationsinfrastruktur** (Act on Protection of Information and Communications Infrastructure)
- **Lag om elektronisk forvaltning** (e-Government Act)
- **Lag om skydd av personuppgifter** (Personal Information Protection Act)
- **AI-grundlag** (AI Basic Act, i kraft fran 2026-01-22)

---

## Relaterade resurser

- [KISA Detaljerad guide for teknisk sarbarhetsanalys](https://www.kisa.or.kr)
- [Artificial Intelligence (AI) Security Guide](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Byggt med

| Plugin | Beskrivning |
|--------|-------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill for bokskrivningsstod - PDF-analys, strukturextraktion, korrekturering/omskrivning |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Kompatibilitet med Claude Code plugin-hooks i Windows-miljo |

---

## Licens

MIT License

## Forfattare

CDPP Corp (https://github.com/cdppcorp)
