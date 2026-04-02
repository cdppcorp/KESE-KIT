🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin per Claude Code dedicato alla valutazione delle vulnerabilita delle Infrastrutture Critiche Informatiche (CII) e alla valutazione della sicurezza dell'IA, basato sulle linee guida della KISA (Agenzia Coreana per Internet e la Sicurezza).

---

## Panoramica

KESE (KISA Enhanced Security Evaluation Kit) e un plugin per Claude Code che fornisce funzionalita complete di valutazione delle vulnerabilita di sicurezza basate sulle linee guida della KISA (Agenzia Coreana per Internet e la Sicurezza). Supporta sia le valutazioni delle Infrastrutture Critiche Informatiche (CII) sia le valutazioni della Sicurezza dell'IA.

## Funzionalita

| Skill | Descrizione |
|-------|-------------|
| `/kesekit:start` | Eseguire la valutazione completa delle vulnerabilita di sicurezza (CII 560+ elementi o Sicurezza IA) |
| `/kesekit:check` | Checklist di conformita di sicurezza pre-distribuzione |
| `/kesekit:fix` | Generare automaticamente script di hardening e correzioni di sicurezza |
| `/kesekit:guide` | Generare prompt di codifica sicura per strumenti di IA |

## Linee Guida Supportate

### 1. CII (Infrastrutture Critiche Informatiche) — 560+ elementi

**Valutazione Tecnica**
| Sistema | Codice | Elementi |
|---------|--------|:--------:|
| Server Unix/Linux | U-01~U-67 | 67 |
| Server Windows | W-01~W-64 | 64 |
| Servizio Web | WEB-01~WEB-26 | 26 |
| Apparecchiature di Sicurezza | S-01~S-23 | 23 |
| Apparecchiature di Rete | N-01~N-38 | 38 |
| Sistema di Controllo | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Dispositivo Mobile | M-01~M-04 | 4 |
| Applicazione Web | 21 codici | 21 |
| Virtualizzazione | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Valutazione Amministrativa**: A-1~A-127 (127 elementi, 14 domini)
**Valutazione Fisica**: P-1~P-18 (18 elementi)

### 2. Guida alla Sicurezza dell'IA — 54+ elementi

| Destinatari | Elementi | Ciclo di Vita |
|-------------|:--------:|---------------|
| Sviluppatore IA | 54 | 6 fasi (Pianificazione→Dati→Modello→Distribuzione→Monitoraggio→Dismissione) |
| Fornitore di Servizi | ~43 | 6 fasi (Pianificazione→Sviluppo→Operazioni→Manutenzione→Feedback→Dismissione) |
| Utente | 7 | Best practice di sicurezza |

## Installazione

```bash
claude plugins install kesekit
```

## Utilizzo

```bash
# Avviare la valutazione completa di sicurezza
/kesekit:start

# Eseguire la checklist pre-distribuzione
/kesekit:check

# Generare script di hardening
/kesekit:fix

# Ottenere prompt di codifica sicura
/kesekit:guide
```

---

## Struttura del Progetto

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Metadati del plugin
├── skills/                            ← Skill in inglese (router)
│   ├── start/
│   │   ├── SKILL.md                  ← Router (~80 righe)
│   │   └── references/               ← Conoscenze per linea guida
│   │       ├── cii/                  ← 14 riferimenti CII
│   │       └── ai-security/          ← 4 riferimenti Sicurezza IA
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skill in coreano (stessa struttura)
├── authorkit/                         ← Documenti originali e artefatti di lavoro
│   ├── converted/
│   │   ├── ref-001/                  ← Guida amministrativa/fisica (full.md)
│   │   ├── ref-002/                  ← Guida tecnica (full.md)
│   │   └── ref-003/                  ← Guida Sicurezza IA (full.md)
│   └── ...
├── 문서/                              ← PDF originali
└── README.md
```

---

## Registro delle Modifiche

### v2.0.0 (2026-03-30)

**Refactoring della Struttura — Applicazione del pattern Progressive Disclosure**

| Modifica | Prima (v1.0) | Dopo (v2.0) |
|----------|-------------|------------|
| SKILL.md | Tutta la conoscenza inline (270~465 righe) | Solo router (~50~80 righe) |
| Linee guida | Solo CII | CII + Sicurezza IA |
| Archiviazione conoscenze | Hardcoded in SKILL.md | Separato in `references/` (18 file) |
| Codici elementi | Solo alcuni elementi inclusi | Tutti gli elementi basati sulla guida 2026 |
| Estensibilita | L'aggiunta di nuove linee guida aumentava il numero di skill | 4 skill fissi, si aggiungono solo riferimenti |

**Nuova Linea Guida Aggiunta: Guida alla Sicurezza dell'IA**
- Fonte: Ministero della Scienza e delle TIC / KISA "Guida alla Sicurezza dell'Intelligenza Artificiale (IA)"
- 54 elementi di verifica per sviluppatori IA (ciclo di vita a 6 fasi)
- Requisiti di sicurezza per fornitori di servizi IA
- 7 pratiche di sicurezza per utenti IA

**Aggiornamento delle Linee Guida CII**
- Riestratta la totalita degli elementi sulla base della guida dettagliata 2026
- Integrazione del sistema di codifica degli elementi (nuovi codici come WEB, HV, CA)

### v1.0.0 (2026-03-29)

- Rilascio iniziale
- 4 skill di valutazione delle vulnerabilita CII (coreano/inglese)
- Elementi tecnici (424) + amministrativi (127) + fisici (9)

---

## Base Giuridica

- **Legge sulla Protezione delle Infrastrutture di Informazione e Comunicazione** (정보통신기반 보호법)
- **Legge sull'e-Government** (전자정부법)
- **Legge sulla Protezione dei Dati Personali** (개인정보 보호법)
- **Legge Fondamentale sull'Intelligenza Artificiale** (인공지능 기본법, in vigore dal 22/01/2026)

---

## Risorse Correlate

- [Guida Dettagliata alla Valutazione delle Vulnerabilita Tecniche della KISA](https://www.kisa.or.kr)
- [Guida alla Sicurezza dell'Intelligenza Artificiale (IA)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 per LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Realizzato Con

| Plugin | Descrizione |
|--------|-------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill di supporto alla scrittura di libri - analisi PDF, estrazione struttura, revisione/riscrittura |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Compatibilita degli hook dei plugin Claude Code per ambiente Windows |

---

## Licenza

MIT License

## Autore

CDPP Corp (https://github.com/cdppcorp)
