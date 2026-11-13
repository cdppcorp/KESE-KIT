🌐 [한국어](../README.md) | [English](../README.md#english) | [Francais](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Espanol](README.es.md) | [Deutsch](README.de.md) | [Portugues](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Turkce](README.tr.md) | [Tieng Viet](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin Claude Code pour l'analyse des vulnerabilites des infrastructures d'information critiques (CII), l'evaluation de la securite de l'IA, l'inspection de securite des robots, l'inspection de securite spatiale, le guide de codage securise, l'evaluation de securite Zero Trust et la securite de la chaine d'approvisionnement SW (SBOM).

---

## Presentation

KESE (KISA Enhanced Security Evaluation Kit) est un plugin Claude Code qui fournit des capacites completes d'evaluation des vulnerabilites de securite basees sur les directives de la KISA (Korea Internet & Security Agency). Il prend en charge les evaluations CII, la securite de l'IA, la securite des robots, la securite spatiale, le codage securise et l'evaluation de securite Zero Trust.

## Fonctionnalites

| Skill | Description |
|-------|-------------|
| `/kesekit-start` | Executer une evaluation complete des vulnerabilites de securite (CII 560+ / Securite IA / Securite des robots / Securite spatiale / Codage securise / Zero Trust / Chaine d'approvisionnement SW) |
| `/kesekit-check` | Checklist de conformite securite avant deploiement (CII / IA / Robots / Espace / Codage securise / Zero Trust / Chaine d'approvisionnement SW) |
| `/kesekit-fix` | Generation automatique de scripts de durcissement et de correctifs de securite (CII / IA / Robots / Espace / Codage securise / Zero Trust / Chaine d'approvisionnement SW) |
| `/kesekit-guide` | Generer des prompts de codage securise pour les outils d'IA (CII / IA / Robots / Espace / JS·Python·Generique / Zero Trust / Chaine d'approvisionnement SW) |

## Directives prises en charge

### 1. CII (Infrastructures d'information critiques) — 560+ elements

**Evaluation technique des vulnerabilites**
| Systeme | Code | Elements |
|---------|------|:--------:|
| Serveur Unix/Linux | U-01~U-67 | 67 |
| Serveur Windows | W-01~W-64 | 64 |
| Service Web | WEB-01~WEB-26 | 26 |
| Equipement de securite | S-01~S-23 | 23 |
| Equipement reseau | N-01~N-38 | 38 |
| Systeme de controle | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobile | M-01~M-04 | 4 |
| Web Application | 21 codes | 21 |
| Virtualisation | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Evaluation administrative** : A-1~A-127 (127 elements, 14 domaines)
**Evaluation physique** : P-1~P-18 (18 elements)

### 2. Guide de securite IA — 54+ elements

| Cible | Elements | Cycle de vie |
|-------|:--------:|-------------|
| Developpeur IA | 54 | 6 phases (Planification → Donnees → Modele → Deploiement → Surveillance → Mise hors service) |
| Fournisseur de services | ~43 | 6 phases (Planification → Developpement → Exploitation → Maintenance → Retour d'information → Mise hors service) |
| Utilisateur | 7 | Bonnes pratiques de securite |

### 3. Securite des robots — ~103 elements

| Categorie | Code | Elements | Normes de reference |
|-----------|------|:--------:|---------------------|
| Developpement SW securise (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Securite de la chaine d'approvisionnement | SC-01~07 | 7 | NIST SP 800-161 |
| Identification et authentification | IA-01~11 | 11 | IEC 62443 |
| Controle d'utilisation | UC-01~11 | 11 | IEC 62443 |
| Integrite du systeme | SI-01~11 | 11 | IEC 62443 |
| Protection des donnees | DP-01~04 | 4 | IEC 62443 |
| Restriction des flux de donnees | DFR-01~02 | 2 | IEC 62443 |
| Reponse aux evenements | ER-01~03 | 3 | IEC 62443 |
| Disponibilite des ressources | RA-01~08 | 8 | IEC 62443 |
| Cyber-resilience | CR-01~13 | 13 | EU CRA |
| Securite sans fil | WS-01~14 | 14 | EU RED |

Cible : robots industriels / de service / medicaux (ISO 8373)

### 4. Securite spatiale — 53 elements

| Domaine | Code | Elements | Normes de reference |
|---------|------|:--------:|---------------------|
| Controle d'acces | AC-01~12 | 12 | CMMC, K-RMF |
| Identification et authentification | IA-01~02 | 2 | CMMC, NIS2 |
| Securite des systemes et communications | SC-01~07 | 7 | NIST IR 8401 |
| Integrite des systemes et informations | SI-01~04 | 4 | NIST CSF |
| Gestion des operations systeme/service | SO-01~09 | 9 | ISMS-P |
| Reponse aux incidents | IR-01~02 | 2 | NIS2 |
| Securite du personnel | PS-01~02 | 2 | CMMC |
| Securite physique | PE-01~03 | 3 | K-RMF |
| Evaluation des risques et de la securite | RA-01~02 | 2 | NIST CSF |
| Gouvernance de la securite | SG-01~04 | 4 | ISMS-P |
| Plan d'urgence | CP-01~02 | 2 | NIST IR 8270 |
| Gestion de la chaine d'approvisionnement | SM-01~04 | 4 | CMMC, NIS2 |

Cible : operateurs de satellites, fournisseurs GSaaS, operateurs de stations au sol, entreprises de la chaine d'approvisionnement spatiale

### 5. Guide de codage securise — 46 elements

| Categorie | Elements | CWE | Normes de reference |
|-----------|:--------:|:---:|---------------------|
| Validation des donnees d'entree et representation | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Fonctions de securite | 16 | 16 | CWE/SANS Top 25 |
| Temps et etat | 2 | 3 | CWE |
| Gestion des erreurs | 3 | 3 | CWE |
| Erreurs de code | 3 | 3 | CWE |
| Encapsulation | 4 | 5 | CWE |
| Mauvais usage des API | 2 | 1 | CWE |

**Langages pris en charge :**
| Langage | Elements | Frameworks |
|---------|:--------:|-----------|
| Pseudo Code (generique) | 46 | Modeles independants du langage |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Cible : developpeurs web JavaScript/Python, utilisateurs d'outils IA (Claude, Cursor, Copilot), developpeurs en vibe coding

### 6. Securite Zero Trust — ~421 elements

| Element central | Code | Elements | Maturite |
|-----------------|------|:--------:|----------|
| Identite | ZT-ID-01~53 | 53 | Traditionnel/Initial/Avance/Optimal |
| Appareil et point de terminaison | ZT-DV-01~36 | 36 | Traditionnel/Initial/Avance/Optimal |
| Reseau | ZT-NW-01~54 | 54 | Traditionnel/Initial/Avance/Optimal |
| Systeme | ZT-SY-01~49 | 49 | Traditionnel/Initial/Avance/Optimal |
| Application et charge de travail | ZT-AP-01~60 | 60 | Traditionnel/Initial/Avance/Optimal |
| Donnees | ZT-DA-01~58 | 58 | Traditionnel/Initial/Avance/Optimal |
| Visibilite et analyse | ZT-VA-01~43 | 43 | Traditionnel/Initial/Avance/Optimal |
| Automatisation et orchestration | ZT-AU-01~43 | 43 | Traditionnel/Initial/Avance/Optimal |
| OT/ICS specifique | ZT-OT-01~25 | 25 | Traditionnel/Initial/Avance/Optimal |

**4 niveaux de maturite** : Traditionnel (Traditional) → Initial (Initial) → Avance (Advanced) → Optimal (Optimal)
**Normes de reference** : KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Cible : entreprises adoptant le Zero Trust, environnements OT/ICS, organisations en migration cloud, responsables de l'evaluation de la maturite de securite

### 7. Securite de la chaine d'approvisionnement SW (SBOM) — 29 elements

| Phase | Code | Elements | Normes de reference |
|-------|------|:--------:|---------------------|
| Conception | SC-01~05 | 5 | NIST SP 800-161r1 |
| Developpement | SC-06~16 | 11 | NIST SP 800-218 |
| Fourniture/Distribution | SC-17~19 | 3 | NTIA SBOM |
| Deploiement et exploitation | SC-20~26 | 7 | NIS-SBOM |
| Maintenance | SC-27~29 | 3 | NIS-SBOM |

## Installation

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

> **Pour mettre a jour :**
> ```
> /plugin marketplace update kesekit
> /plugin update kesekit@kesekit
> /reload-plugins
> ```

## Utilisation

```bash
# Lancer l'evaluation complete de securite
/kesekit-start

# Executer la checklist avant deploiement
/kesekit-check

# Generer les scripts de durcissement
/kesekit-fix

# Obtenir les prompts de codage securise
/kesekit-guide
```

---

## Structure du projet

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Metadonnees du plugin
├── skills/                            ← Skills anglais
│   ├── start/
│   │   ├── SKILL.md                  ← Routeur (~80 lignes)
│   │   ├── references/               ← Documents de description/criteres
│   │   │   ├── ai-security/          ← Apercu, fournisseur de services, guide utilisateur
│   │   │   ├── space-security/       ← Apercu, scenarios de menaces de la chaine d'approvisionnement
│   │   │   └── zero-trust/           ← Maturite Zero Trust, OT/ICS
│   │   ├── templates/                ← Formulaires annexes, tableaux de checklist
│   │   │   ├── cii/                  ← 14 tableaux de verification CII
│   │   │   ├── ai-security/          ← Verification developpeur IA, checklist utilisateur
│   │   │   ├── robot-security/       ← 6 checklists securite des robots
│   │   │   ├── space-security/       ← 4 tableaux de verification securite spatiale
│   │   │   └── zero-trust/           ← 9 checklists elements centraux Zero Trust
│   │   └── scripts/                  ← Scripts de verification/correction executables
│   │       ├── cii/                  ← Scripts bash, PowerShell, SQL
│   │       └── robot-security/       ← Scripts pare-feu, SBOM, certificats
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skills coreen (meme structure)
├── 문서/                              ← PDF sources (14)
├── authorkit/                         ← Documents source et livrables
│   ├── converted/
│   │   ├── ref-001/                  ← Guide administratif et physique (full.md)
│   │   ├── ref-002/                  ← Guide technique (full.md)
│   │   ├── ref-003/                  ← Guide securite IA (full.md)
│   │   ├── ...
│   │   ├── ref-013/                  ← Zero Trust Guideline 2.0 (full.md)
│   │   ├── ref-014/                  ← Guide du modele de maturite Zero Trust (full.md)
│   │   └── ref-015/                  ← Guide d'application Zero Trust pour l'OT (full.md)
│   └── ...
├── docs/                              ← README en 20 langues
├── CONTRIBUTING.md
└── README.md
```

---

## Historique des modifications

### v4.0.0 (2026-04-03)

**Nouvelle directive ajoutee : Securite Zero Trust**
- Source : KISA Zero Trust Guideline 2.0 (245p) + Guide du modele de maturite Zero Trust (182p) + Guide d'application Zero Trust pour l'OT (67p)
- 9 elements centraux, ~421 elements de checklist
- 4 niveaux de maturite : Traditional → Initial → Advanced → Optimal
- Normes de reference : KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model
- 25 elements specifiques OT/ICS inclus

### v3.2.0 (2026-04-02)

**Nouvelle directive ajoutee : Guide de codage securise**
- Source : KISA Javascript Secure Coding Guide 159p + Python Secure Coding Guide 176p (edition revisee 2023)
- 7 categories, 46 elements, 49 correspondances CWE
- Nouveau guide Pseudo Code generique (motifs UNSAFE/SAFE independants du langage)
- Exemples de code par framework : JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy)
- `references/secure-coding/` + `templates/secure-coding/` deployes dans les 8 skills (EN/KO)

### v3.0.0 (2026-04-02)

**Breaking Change : Changement de format des commandes**
- Tous les skills unifies sous le namespace `kesekit`
- Format des commandes : `/start` → `/kesekit-start` (ajout du prefixe namespace)

**Nouvelle directive ajoutee : Securite spatiale**
- Source : Modele de securite spatiale Part1 134p + Part2 223p + Guide explicatif 218p
- 12 domaines, 53 elements de checklist
- Normes de reference : CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, CCSDS

**Nouvelle directive ajoutee : Securite des robots** (v2.1)
- Source : Modele de securite des robots (avance) 156p + Guide de la checklist de securite des robots 225p
- 11 categories, ~103 elements de checklist
- Normes de reference : NIST SP 800-218, IEC 62443, EU CRA, EU RED, NIS2

### v2.0.0 (2026-03-30)

**Refactoring structurel — Application du pattern Progressive Disclosure**

| Modification | Avant (v1.0) | Apres (v2.0) |
|-------------|-------------|-------------|
| SKILL.md | Toutes les connaissances en ligne (270~465 lignes) | Routeur uniquement (~50~80 lignes) |
| Directives | CII uniquement | CII + Securite IA |
| Stockage des connaissances | Code en dur dans SKILL.md | Separe dans `references/` (18 fichiers) |
| Codes d'elements | Seulement certains elements | Tous les elements bases sur le guide 2026 |
| Extensibilite | Ajout de nouvelles directives = plus de skills | 4 skills fixes, ajout de references uniquement |

**Nouvelle directive ajoutee : Guide de securite IA**
- Source : Ministere des Sciences et des TIC / KISA — « Guide de securite de l'intelligence artificielle (IA) »
- 54 elements de verification pour les developpeurs IA (cycle de vie en 6 phases)
- Exigences de securite pour les fournisseurs de services IA
- 7 regles de securite pour les utilisateurs d'IA

**Mise a jour des directives CII**
- Reextraction complete des elements basee sur le guide detaille 2026
- Integration du systeme de codes d'elements (nouveaux codes WEB, HV, CA, etc.)

### v1.0.0 (2026-03-29)

- Version initiale
- 4 skills d'evaluation des vulnerabilites CII (coreen/anglais)
- Elements techniques (424) + administratifs (127) + physiques (9)

---

## Base juridique

- **Loi sur la protection des infrastructures d'information et de communication** (정보통신기반 보호법)
- **Loi sur l'administration electronique** (전자정부법)
- **Loi sur la protection des donnees personnelles** (개인정보 보호법)
- **Loi fondamentale sur l'intelligence artificielle** (인공지능 기본법, entree en vigueur le 22 janvier 2026)

---

## Ressources associees

- [Guide detaille d'evaluation des vulnerabilites techniques de la KISA](https://www.kisa.or.kr)
- [Guide de securite de l'intelligence artificielle (IA)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Concu avec

| Plugin | Description |
|--------|-------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill d'aide a la redaction — Analyse de PDF, extraction de structure, relecture/reecriture |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Compatibilite des hooks de plugins Claude Code pour environnement Windows |

---

## Licence

MIT License

## Auteur

CDPP Corp (https://github.com/cdppcorp)
