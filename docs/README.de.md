🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Ein Claude Code-Plugin zur Schwachstellenanalyse und -bewertung kritischer Informationsinfrastrukturen (CII), KI-Sicherheitsbewertung, Roboter-Sicherheitspruefung, Weltraum-Sicherheitspruefung, Secure-Coding-Leitfaden, Zero-Trust-Sicherheitsbewertung und SW-Lieferkettensicherheit (SBOM).

---

## Ueberblick

KESE (KISA Enhanced Security Evaluation Kit) ist ein Claude Code-Plugin, das umfassende Schwachstellenbewertungsfunktionen auf Basis der KISA-Richtlinien (Koreanische Agentur fuer Internet und Sicherheit) bereitstellt. Es unterstuetzt CII-Schwachstellenbewertung, KI-Sicherheitsbewertung, Roboter-Sicherheitspruefung, Weltraum-Sicherheitspruefung, Secure-Coding-Leitfaden und Zero-Trust-Sicherheitsbewertung.

## Funktionen

| Skill | Beschreibung |
|-------|--------------|
| `/kesekit-start` | Vollstaendige Sicherheits-Schwachstellenbewertung ausfuehren (CII 560+ / KI-Sicherheit / Roboter-Sicherheit / Weltraum-Sicherheit / Secure Coding / Zero Trust / SW-Lieferkette) |
| `/kesekit-check` | Sicherheits-Compliance-Checkliste vor der Bereitstellung (CII / KI / Roboter / Weltraum / Secure Coding / Zero Trust / SW-Lieferkette) |
| `/kesekit-fix` | Automatische Generierung von Haertungsskripten und Sicherheitskorrekturen (CII / KI / Roboter / Weltraum / Secure Coding / Zero Trust / SW-Lieferkette) |
| `/kesekit-guide` | Sichere Coding-Prompts fuer KI-Werkzeuge generieren (CII / KI / Roboter / Weltraum / JS·Python·Generisch / Zero Trust / SW-Lieferkette) |

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
| Nutzer | 7 | Bewaehrte Sicherheitspraktiken |

### 3. Roboter-Sicherheit — ~103 Elemente

| Kategorie | Code | Elemente | Referenzstandards |
|-----------|------|:--------:|-------------------|
| Sichere SW-Entwicklung (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Lieferketten-Sicherheit | SC-01~07 | 7 | NIST SP 800-161 |
| Identifizierung und Authentifizierung | IA-01~11 | 11 | IEC 62443 |
| Nutzungskontrolle | UC-01~11 | 11 | IEC 62443 |
| Systemintegritaet | SI-01~11 | 11 | IEC 62443 |
| Datenschutz | DP-01~04 | 4 | IEC 62443 |
| Datenfluss-Beschraenkung | DFR-01~02 | 2 | IEC 62443 |
| Ereignisreaktion | ER-01~03 | 3 | IEC 62443 |
| Ressourcenverfuegbarkeit | RA-01~08 | 8 | IEC 62443 |
| Cyber-Resilienz | CR-01~13 | 13 | EU CRA |
| Drahtlose Sicherheit | WS-01~14 | 14 | EU RED |

Zielgruppe: Industrie- / Service- / Medizinroboter (ISO 8373)

### 4. Weltraum-Sicherheit — 53 Elemente

| Bereich | Code | Elemente | Referenzstandards |
|---------|------|:--------:|-------------------|
| Zugriffskontrolle | AC-01~12 | 12 | CMMC, K-RMF |
| Identifizierung und Authentifizierung | IA-01~02 | 2 | CMMC, NIS2 |
| System- und Kommunikationssicherheit | SC-01~07 | 7 | NIST IR 8401 |
| System- und Informationsintegritaet | SI-01~04 | 4 | NIST CSF |
| System-/Dienstbetriebsmanagement | SO-01~09 | 9 | ISMS-P |
| Vorfallreaktion | IR-01~02 | 2 | NIS2 |
| Personalsicherheit | PS-01~02 | 2 | CMMC |
| Physische Sicherheit | PE-01~03 | 3 | K-RMF |
| Risiko- und Sicherheitsbewertung | RA-01~02 | 2 | NIST CSF |
| Sicherheits-Governance | SG-01~04 | 4 | ISMS-P |
| Notfallplanung | CP-01~02 | 2 | NIST IR 8270 |
| Lieferketten-Management | SM-01~04 | 4 | CMMC, NIS2 |

Zielgruppe: Satellitenbetreiber, GSaaS-Anbieter, Bodenstationsbetreiber, Unternehmen der Weltraum-Lieferkette

### 5. Secure-Coding-Leitfaden — 46 Elemente

| Kategorie | Elemente | CWE | Referenzstandards |
|-----------|:--------:|:---:|-------------------|
| Eingabedaten-Validierung und Darstellung | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Sicherheitsfunktionen | 16 | 16 | CWE/SANS Top 25 |
| Zeit und Zustand | 2 | 3 | CWE |
| Fehlerbehandlung | 3 | 3 | CWE |
| Code-Fehler | 3 | 3 | CWE |
| Kapselung | 4 | 5 | CWE |
| API-Missbrauch | 2 | 1 | CWE |

**Unterstuetzte Sprachen:**
| Sprache | Elemente | Frameworks |
|---------|:--------:|-----------|
| Pseudo Code (generisch) | 46 | Sprachunabhaengige Muster |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Zielgruppe: JavaScript/Python-Webentwickler, KI-Tool-Nutzer (Claude, Cursor, Copilot), Vibe-Coding-Entwickler

### 6. Zero-Trust-Sicherheit — ~421 Elemente

| Kernelement | Code | Elemente | Reifegrad |
|-------------|------|:--------:|-----------|
| Identitaet | ZT-ID-01~53 | 53 | Traditionell/Initial/Fortgeschritten/Optimal |
| Geraet und Endpunkt | ZT-DV-01~36 | 36 | Traditionell/Initial/Fortgeschritten/Optimal |
| Netzwerk | ZT-NW-01~54 | 54 | Traditionell/Initial/Fortgeschritten/Optimal |
| System | ZT-SY-01~49 | 49 | Traditionell/Initial/Fortgeschritten/Optimal |
| Anwendung und Workload | ZT-AP-01~60 | 60 | Traditionell/Initial/Fortgeschritten/Optimal |
| Daten | ZT-DA-01~58 | 58 | Traditionell/Initial/Fortgeschritten/Optimal |
| Sichtbarkeit und Analyse | ZT-VA-01~43 | 43 | Traditionell/Initial/Fortgeschritten/Optimal |
| Automatisierung und Orchestrierung | ZT-AU-01~43 | 43 | Traditionell/Initial/Fortgeschritten/Optimal |
| OT/ICS-spezifisch | ZT-OT-01~25 | 25 | Traditionell/Initial/Fortgeschritten/Optimal |

**4 Reifegradstufen**: Traditionell (Traditional) → Initial (Initial) → Fortgeschritten (Advanced) → Optimal (Optimal)
**Referenzstandards**: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Zielgruppe: Unternehmen mit Zero-Trust-Einfuehrung, OT/ICS-Umgebungen, Cloud-Migrationsorganisationen, Verantwortliche fuer Sicherheitsreifegradbeurteilung

### 7. SW-Lieferkettensicherheit (SBOM) — 29 Elemente

| Phase | Code | Elemente | Referenzstandards |
|-------|------|:--------:|-------------------|
| Entwurf | SC-01~05 | 5 | NIST SP 800-161r1 |
| Entwicklung | SC-06~16 | 11 | NIST SP 800-218 |
| Lieferung/Verteilung | SC-17~19 | 3 | NTIA SBOM |
| Bereitstellung und Betrieb | SC-20~26 | 7 | NIS-SBOM |
| Wartung | SC-27~29 | 3 | NIS-SBOM |

## Installation

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

> **Zum Aktualisieren:**
> ```
> /plugin marketplace update kesekit
> /plugin update kesekit@kesekit
> /reload-plugins
> ```

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
├── skills/                            ← Englische Skills
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 Zeilen)
│   │   ├── references/               ← Beschreibungs-/Kriteriendokumente
│   │   │   ├── ai-security/          ← Uebersicht, Dienstanbieter, Nutzerleitfaden
│   │   │   ├── space-security/       ← Uebersicht, Lieferketten-Bedrohungsszenarien
│   │   │   └── zero-trust/           ← Zero-Trust-Reifegradmodell, OT/ICS
│   │   ├── templates/                ← Anhangsformulare, Checklisten-Tabellen
│   │   │   ├── cii/                  ← 14 CII-Pruefungstabellen
│   │   │   ├── ai-security/          ← KI-Entwickler-Verifizierung, Nutzer-Checkliste
│   │   │   ├── robot-security/       ← 6 Roboter-Sicherheits-Checklisten
│   │   │   ├── space-security/       ← 4 Weltraum-Sicherheits-Pruefungstabellen
│   │   │   └── zero-trust/           ← 9 Zero-Trust-Kernelement-Checklisten
│   │   └── scripts/                  ← Ausfuehrbare Pruef-/Korrekturskripte
│   │       ├── cii/                  ← bash, PowerShell, SQL-Skripte
│   │       └── robot-security/       ← Firewall-, SBOM-, Zertifikatskripte
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Koreanische Skills (gleiche Struktur)
├── 문서/                              ← Original-PDFs (14)
├── authorkit/                         ← Konvertierte Ergebnisse und Arbeitsdateien
│   ├── converted/
│   │   ├── ref-001/                  ← Administrativer/physischer Leitfaden (full.md)
│   │   ├── ref-002/                  ← Technischer Leitfaden (full.md)
│   │   ├── ref-003/                  ← KI-Sicherheitsleitfaden (full.md)
│   │   ├── ...
│   │   ├── ref-013/                  ← Zero Trust Guideline 2.0 (full.md)
│   │   ├── ref-014/                  ← Zero Trust Reifegradmodell Erklaerung (full.md)
│   │   └── ref-015/                  ← Zero Trust fuer OT-Umgebungen Leitfaden (full.md)
│   └── ...
├── docs/                              ← README in 20 Sprachen
├── CONTRIBUTING.md
└── README.md
```

---

## Aenderungshistorie

### v4.0.0 (2026-04-03)

**Neue Richtlinie: Zero-Trust-Sicherheit**
- Quelle: KISA Zero Trust Guideline 2.0 (245S.) + Zero Trust Reifegradmodell Erklaerung (182S.) + Zero Trust fuer OT-Umgebungen Leitfaden (67S.)
- 9 Kernelemente, ~421 Checklisten-Elemente
- 4 Reifegradstufen: Traditional → Initial → Advanced → Optimal
- Referenzstandards: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model
- 25 OT/ICS-spezifische Elemente enthalten

### v3.2.0 (2026-04-02)

**Neue Richtlinie: Secure-Coding-Leitfaden**
- Quelle: KISA Javascript Secure Coding Guide 159S. + Python Secure Coding Guide 176S. (ueberarbeitete Ausgabe 2023)
- 7 Kategorien, 46 Elemente, 49 CWE-Zuordnungen
- Neuer generischer Pseudo Code Leitfaden (sprachunabhaengige UNSAFE/SAFE-Muster)
- Framework-spezifische Codebeispiele: JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy)
- `references/secure-coding/` + `templates/secure-coding/` in allen 8 Skills (EN/KO) bereitgestellt

### v3.0.0 (2026-04-02)

**Breaking Change: Aenderung des Befehlsformats**
- Alle Skills unter dem einheitlichen Namespace `kesekit` zusammengefasst
- Befehlsformat: `/start` → `/kesekit-start` (Namespace-Praefix hinzugefuegt)

**Neue Richtlinie: Weltraum-Sicherheit**
- Quelle: Weltraum-Sicherheitsmodell Part1 134S. + Part2 223S. + Erklaerungsleitfaden 218S.
- 12 Bereiche, 53 Checklisten-Elemente
- Referenzstandards: CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, CCSDS

**Neue Richtlinie: Roboter-Sicherheit** (v2.1)
- Quelle: Roboter-Sicherheitsmodell (erweitert) 156S. + Roboter-Sicherheits-Checklisten-Erklaerung 225S.
- 11 Kategorien, ~103 Checklisten-Elemente
- Referenzstandards: NIST SP 800-218, IEC 62443, EU CRA, EU RED, NIS2

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
