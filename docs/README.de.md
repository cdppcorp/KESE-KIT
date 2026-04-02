🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Ein Claude Code-Plugin zur Schwachstellenanalyse und -bewertung kritischer Informationsinfrastrukturen (CII) sowie zur KI-Sicherheitsbewertung.

---

## Ueberblick

KESE (KISA Enhanced Security Evaluation Kit) ist ein Claude Code-Plugin, das umfassende Schwachstellenbewertungsfunktionen auf Basis der KISA-Richtlinien (Koreanische Agentur fuer Internet und Sicherheit) bereitstellt. Es unterstuetzt sowohl die Bewertung kritischer Informationsinfrastrukturen (CII) als auch KI-Sicherheitsbewertungen.

## Funktionen

| Skill | Beschreibung |
|-------|--------------|
| `/kesekit-start` | Vollstaendige Sicherheits-Schwachstellenbewertung ausfuehren (CII 560+ Elemente oder KI-Sicherheit) |
| `/kesekit-check` | Sicherheits-Compliance-Checkliste vor der Bereitstellung |
| `/kesekit-fix` | Automatische Generierung von Haertungsskripten und Sicherheitskorrekturen |
| `/kesekit-guide` | Sichere Coding-Prompts fuer KI-Werkzeuge generieren |

## Unterstuetzte Richtlinien

### 1. CII (Kritische Informationsinfrastruktur) — 560+ Elemente

**Technische Bewertung**
| System | Code | Elemente |
|--------|------|:--------:|
| Unix/Linux-Server | U-01~U-67 | 67 |
| Windows-Server | W-01~W-64 | 64 |
| Webdienste | WEB-01~WEB-26 | 26 |
| Sicherheitsausruestung | S-01~S-23 | 23 |
| Netzwerkausruestung | N-01~N-38 | 38 |
| Steuerungssysteme | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobilgeraete | M-01~M-04 | 4 |
| Webanwendungen | 21 Codes | 21 |
| Virtualisierung | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Administrative Bewertung**: A-1~A-127 (127 Elemente, 14 Bereiche)
**Physische Bewertung**: P-1~P-18 (18 Elemente)

### 2. KI-Sicherheitsleitfaden — 54+ Elemente

| Zielgruppe | Elemente | Lebenszyklus |
|------------|:--------:|--------------|
| KI-Entwickler | 54 | 6 Phasen (Planung→Daten→Modell→Bereitstellung→Ueberwachung→Ausserbetriebnahme) |
| Dienstanbieter | ~43 | 6 Phasen (Planung→Entwicklung→Betrieb→Wartung→Feedback→Ausserbetriebnahme) |
| Nutzer | 7 | Bewehrte Sicherheitspraktiken |

## Installation

```bash
claude plugins install kesekit
```

## Verwendung

```bash
# Vollstaendige Sicherheitsbewertung starten
/kesekit-start

# Checkliste vor der Bereitstellung ausfuehren
/kesekit-check

# Haertungsskripte generieren
/kesekit-fix

# Sichere Coding-Prompts abrufen
/kesekit-guide
```

---

## Projektstruktur

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Plugin-Metadaten
├── skills/                            ← Englische Skills (Router)
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 Zeilen)
│   │   └── references/               ← Wissen nach Richtlinie
│   │       ├── cii/                  ← 14 CII-Referenzdateien
│   │       └── ai-security/          ← 4 KI-Sicherheits-Referenzdateien
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Koreanische Skills (gleiche Struktur)
├── authorkit/                         ← Originaldokumente und Arbeitsmaterialien
│   ├── converted/
│   │   ├── ref-001/                  ← Administrativer/physischer Leitfaden (full.md)
│   │   ├── ref-002/                  ← Technischer Leitfaden (full.md)
│   │   └── ref-003/                  ← KI-Sicherheitsleitfaden (full.md)
│   └── ...
├── 문서/                              ← Original-PDFs
└── README.md
```

---

## Aenderungshistorie

### v2.0.0 (2026-03-30)

**Strukturrefaktorierung — Anwendung des Progressive-Disclosure-Musters**

| Aenderung | Vorher (v1.0) | Nachher (v2.0) |
|-----------|---------------|----------------|
| SKILL.md | Gesamtes Wissen inline (270~465 Zeilen) | Nur Router (~50~80 Zeilen) |
| Richtlinien | Nur CII | CII + KI-Sicherheit |
| Wissensspeicherung | Fest in SKILL.md codiert | In `references/` ausgelagert (18 Dateien) |
| Elementcodes | Nur ein Teil der Elemente enthalten | Vollstaendige Elemente basierend auf dem Leitfaden 2026 |
| Skalierbarkeit | Neue Richtlinien erhoehen die Anzahl der Skills | 4 Skills fest, nur References werden hinzugefuegt |

**Neue Richtlinie: KI-Sicherheitsleitfaden**
- Quelle: Ministerium fuer Wissenschaft und IKT · KISA «Leitfaden zur Sicherheit kuenstlicher Intelligenz (KI)»
- 54 Pruefungselemente fuer KI-Entwickler (6-Phasen-Lebenszyklus)
- Sicherheitsanforderungen fuer KI-Dienstanbieter
- 7 Sicherheitsregeln fuer KI-Nutzer

**Aktualisierung der CII-Richtlinie**
- Vollstaendige Neuextraktion der Elemente basierend auf dem detaillierten Leitfaden 2026
- Beruecksichtigung des Elementcode-Systems (neue Codes: WEB, HV, CA usw.)

### v1.0.0 (2026-03-29)

- Erstveroeffentlichung
- 4 Skills zur CII-Schwachstellenbewertung (Koreanisch/Englisch)
- Technische (424) + administrative (127) + physische (9) Elemente

---

## Rechtsgrundlage

- **Gesetz zum Schutz von Informations- und Kommunikationsinfrastrukturen** (Act on Protection of Information and Communications Infrastructure)
- **E-Government-Gesetz** (e-Government Act)
- **Datenschutzgesetz** (Personal Information Protection Act)
- **KI-Grundlagengesetz** (AI Basic Act, in Kraft seit 22.01.2026)

---

## Verwandte Ressourcen

- [KISA Detaillierter Leitfaden zur technischen Schwachstellenbewertung](https://www.kisa.or.kr)
- [Leitfaden zur Sicherheit kuenstlicher Intelligenz (KI)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Erstellt mit

| Plugin | Beschreibung |
|--------|--------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill zur Unterstuetzung beim Buchschreiben — PDF-Analyse, Strukturextraktion, Ueberarbeitung/Neuschreibung |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Kompatibilitaet von Claude Code-Plugin-Hooks in Windows-Umgebungen |

---

## Lizenz

MIT License

## Autor

CDPP Corp (https://github.com/cdppcorp)
