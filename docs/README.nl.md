🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Een Claude Code skill-plugin voor kwetsbaarheidsanalyse van kritieke informatie-infrastructuur (CII) en AI-beveiligingsevaluatie.

---

## Overzicht

KESE (KISA Enhanced Security Evaluation Kit) is een Claude Code-plugin die uitgebreide mogelijkheden biedt voor kwetsbaarheidsanalyse op basis van de richtlijnen van KISA (Korea Internet & Security Agency). Het ondersteunt zowel evaluaties van kritieke informatie-infrastructuur (CII) als AI-beveiligingsevaluaties.

## Functies

| Skill | Beschrijving |
|-------|-------------|
| `/kesekit-start` | Volledige beveiligingskwetsbaarheidsanalyse uitvoeren (CII 560+ items of AI-beveiliging) |
| `/kesekit-check` | Beveiligingschecklist voor compliance voor implementatie |
| `/kesekit-fix` | Automatisch hardening-scripts en beveiligingsoplossingen genereren |
| `/kesekit-guide` | Secure coding-prompts genereren voor AI-tools |

## Ondersteunde richtlijnen

### 1. CII (Kritieke Informatie-Infrastructuur) — 560+ items

**Technische kwetsbaarheidsevaluatie**
| Systeem | Code | Aantal items |
|---------|------|:------:|
| Unix/Linux-server | U-01~U-67 | 67 |
| Windows-server | W-01~W-64 | 64 |
| Webservice | WEB-01~WEB-26 | 26 |
| Beveiligingsapparatuur | S-01~S-23 | 23 |
| Netwerkapparatuur | N-01~N-38 | 38 |
| Besturingssysteem | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobiel | M-01~M-04 | 4 |
| Web Application | 21 codes | 21 |
| Virtualisatie | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Organisatorische kwetsbaarheidsevaluatie**: A-1~A-127 (127 items, 14 domeinen)
**Fysieke kwetsbaarheidsevaluatie**: P-1~P-18 (18 items)

### 2. AI-beveiligingsgids — 54+ items

| Doelgroep | Aantal items | Levenscyclus |
|-----------|:------:|---------|
| AI-ontwikkelaar | 54 | 6 fasen (Planning→Data→Modelontwikkeling→Implementatie→Monitoring→Buitengebruikstelling) |
| AI-serviceprovider | ~43 | 6 fasen (Planning→Ontwikkeling→Beheer→Onderhoud→Feedback→Buitengebruikstelling) |
| AI-gebruiker | 7 | Beveiligingsrichtlijnen |

## Installatie

```bash
claude plugins install kesekit
```

## Gebruik

```bash
# Volledige beveiligingsevaluatie starten
/kesekit-start

# Checklist voor implementatie uitvoeren
/kesekit-check

# Hardening-scripts genereren
/kesekit-fix

# Secure coding-prompts ophalen
/kesekit-guide
```

---

## Projectstructuur

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Plugin-metadata
├── skills/                            ← Engelstalige skills (router)
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 regels)
│   │   └── references/               ← Kennis per richtlijn
│   │       ├── cii/                  ← CII 14 referenties
│   │       └── ai-security/          ← AI-beveiliging 4 referenties
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Koreaanse skills (zelfde structuur)
├── authorkit/                         ← Brondocumenten en werkproducten
│   ├── converted/
│   │   ├── ref-001/                  ← Organisatorische/fysieke gids (full.md)
│   │   ├── ref-002/                  ← Technische gids (full.md)
│   │   └── ref-003/                  ← AI-beveiligingsgids (full.md)
│   └── ...
├── 문서/                              ← Originele PDF's
└── README.md
```

---

## Wijzigingsgeschiedenis

### v2.0.0 (2026-03-30)

**Structuurherziening — Progressive Disclosure-patroon toegepast**

| Wijziging | Vorige versie (v1.0) | Huidige versie (v2.0) |
|-----------|------------|------------|
| SKILL.md | Alle kennis inline (270~465 regels) | Alleen router (~50~80 regels) |
| Richtlijnen | Alleen CII ondersteund | CII + AI-beveiliging ondersteund |
| Kennisopslag | Hardcoded in SKILL.md | Gescheiden in `references/` (18 bestanden) |
| Itemcodes | Slechts enkele items opgenomen | Alle items op basis van de gids van 2026 |
| Uitbreidbaarheid | Meer skills nodig bij nieuwe richtlijnen | 4 skills vast, alleen references toevoegen |

**Nieuwe richtlijn toegevoegd: AI-beveiligingsgids**
- Bron: Ministerie van Wetenschap en ICT / KISA "Artificial Intelligence (AI) Security Guide"
- 54 verificatie-items voor AI-ontwikkelaars (6-fasen levenscyclus)
- Beveiligingsvereisten voor AI-serviceproviders
- 7 beveiligingsrichtlijnen voor AI-gebruikers

**CII-richtlijnupdate**
- Alle items opnieuw geextraheerd op basis van de gedetailleerde gids van 2026
- Nieuw codesysteem weergegeven (WEB, HV, CA en andere nieuwe codes)

### v1.0.0 (2026-03-29)

- Eerste release
- 4 CII-kwetsbaarheidsanalyse-skills (Koreaans/Engels)
- Technisch (424) + Organisatorisch (127) + Fysiek (9) items

---

## Juridische grondslag

- **Wet op de bescherming van informatie- en communicatie-infrastructuur** (Act on Protection of Information and Communications Infrastructure)
- **Wet op elektronisch bestuur** (e-Government Act)
- **Wet op de bescherming van persoonsgegevens** (Personal Information Protection Act)
- **AI-basiswet** (AI Basic Act, in werking getreden op 22-01-2026)

---

## Gerelateerde bronnen

- [KISA Gedetailleerde gids voor technische kwetsbaarheidsanalyse](https://www.kisa.or.kr)
- [Artificial Intelligence (AI) Security Guide](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Gebouwd met

| Plugin | Beschrijving |
|--------|-------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill voor ondersteuning bij het schrijven van boeken - PDF-analyse, structuurextractie, revisie/herschrijving |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Compatibiliteit met Claude Code plugin-hooks in Windows-omgeving |

---

## Licentie

MIT License

## Auteur

CDPP Corp (https://github.com/cdppcorp)
