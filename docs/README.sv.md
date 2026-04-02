🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Ett Claude Code skill-plugin for sarbarhetsanalys av kritisk informationsinfrastruktur (CII) och AI-sakerhetsutvardering.

---

## Oversikt

KESE (KISA Enhanced Security Evaluation Kit) ar ett Claude Code-plugin som erbjuder omfattande funktioner for sarbarhetsanalys baserad pa KISA:s (Korea Internet & Security Agency) riktlinjer. Det stoder bade utvarderingar av kritisk informationsinfrastruktur (CII) och AI-sakerhetsutvarderingar.

## Funktioner

| Skill | Beskrivning |
|-------|-------------|
| `/kesekit-start` | Kor fullstandig sakerhetsarbarhetsanalys (CII 560+ objekt eller AI-sakerhet) |
| `/kesekit-check` | Sakerhetschecklista for efterlevnad fore driftsattning |
| `/kesekit-fix` | Generera hardening-skript och sakerhetsatgarder automatiskt |
| `/kesekit-guide` | Generera secure coding-promptar for AI-verktyg |

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

## Installation

```bash
claude plugins install kesekit
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
├── skills/                            ← Engelska skills (router)
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 rader)
│   │   └── references/               ← Kunskap per riktlinje
│   │       ├── cii/                  ← CII 14 referenser
│   │       └── ai-security/          ← AI-sakerhet 4 referenser
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Koreanska skills (samma struktur)
├── authorkit/                         ← Kalldokument och arbetsprodukter
│   ├── converted/
│   │   ├── ref-001/                  ← Administrativ/fysisk guide (full.md)
│   │   ├── ref-002/                  ← Teknisk guide (full.md)
│   │   └── ref-003/                  ← AI-sakerhetsguide (full.md)
│   └── ...
├── 문서/                              ← Original-PDF:er
└── README.md
```

---

## Andringshistorik

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
