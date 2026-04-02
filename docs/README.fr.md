🌐 [한국어](../README.md) | [English](../README.md#english) | [Francais](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Espanol](README.es.md) | [Deutsch](README.de.md) | [Portugues](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Turkce](README.tr.md) | [Tieng Viet](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin Claude Code pour l'analyse des vulnérabilités des infrastructures d'information critiques (CII) et l'évaluation de la sécurité de l'IA.

---

## Présentation

KESE (KISA Enhanced Security Evaluation Kit) est un plugin Claude Code qui fournit des capacités complètes d'évaluation des vulnérabilités de sécurité basées sur les directives de la KISA (Korea Internet & Security Agency). Il prend en charge à la fois les évaluations des infrastructures d'information critiques (CII) et les évaluations de sécurité de l'IA.

## Fonctionnalités

| Skill | Description |
|-------|-------------|
| `/kesekit-start` | Exécuter une évaluation complète des vulnérabilités de sécurité (CII 560+ éléments ou sécurité IA) |
| `/kesekit-check` | Checklist de conformité sécurité avant déploiement |
| `/kesekit-fix` | Génération automatique de scripts de durcissement et de correctifs de sécurité |
| `/kesekit-guide` | Générer des prompts de codage sécurisé pour les outils d'IA |

## Directives prises en charge

### 1. CII (Infrastructures d'information critiques) — 560+ éléments

**Évaluation technique des vulnérabilités**
| Système | Code | Éléments |
|---------|------|:--------:|
| Serveur Unix/Linux | U-01~U-67 | 67 |
| Serveur Windows | W-01~W-64 | 64 |
| Service Web | WEB-01~WEB-26 | 26 |
| Équipement de sécurité | S-01~S-23 | 23 |
| Équipement réseau | N-01~N-38 | 38 |
| Système de contrôle | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Mobile | M-01~M-04 | 4 |
| Web Application | 21 codes | 21 |
| Virtualisation | HV-01~HV-25 | 25 |
| Cloud | CA-01~CA-19 | 19 |

**Évaluation administrative** : A-1~A-127 (127 éléments, 14 domaines)
**Évaluation physique** : P-1~P-18 (18 éléments)

### 2. Guide de sécurité IA — 54+ éléments

| Cible | Éléments | Cycle de vie |
|-------|:--------:|-------------|
| Développeur IA | 54 | 6 phases (Planification → Données → Modèle → Déploiement → Surveillance → Mise hors service) |
| Fournisseur de services | ~43 | 6 phases (Planification → Développement → Exploitation → Maintenance → Retour d'information → Mise hors service) |
| Utilisateur | 7 | Bonnes pratiques de sécurité |

## Installation

```bash
claude plugins install kesekit
```

## Utilisation

```bash
# Lancer l'évaluation complète de sécurité
/kesekit-start

# Exécuter la checklist avant déploiement
/kesekit-check

# Générer les scripts de durcissement
/kesekit-fix

# Obtenir les prompts de codage sécurisé
/kesekit-guide
```

---

## Structure du projet

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Métadonnées du plugin
├── skills/                            ← Skills anglais (routeur)
│   ├── start/
│   │   ├── SKILL.md                  ← Routeur (~80 lignes)
│   │   └── references/               ← Base de connaissances par directive
│   │       ├── cii/                  ← 14 références CII
│   │       └── ai-security/          ← 4 références sécurité IA
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skills coréen (même structure)
├── authorkit/                         ← Documents source et livrables
│   ├── converted/
│   │   ├── ref-001/                  ← Guide administratif et physique (full.md)
│   │   ├── ref-002/                  ← Guide technique (full.md)
│   │   └── ref-003/                  ← Guide sécurité IA (full.md)
│   └── ...
├── 문서/                              ← PDF sources
└── README.md
```

---

## Historique des modifications

### v2.0.0 (2026-03-30)

**Refactoring structurel — Application du pattern Progressive Disclosure**

| Modification | Avant (v1.0) | Après (v2.0) |
|-------------|-------------|-------------|
| SKILL.md | Toutes les connaissances en ligne (270~465 lignes) | Routeur uniquement (~50~80 lignes) |
| Directives | CII uniquement | CII + Sécurité IA |
| Stockage des connaissances | Codé en dur dans SKILL.md | Séparé dans `references/` (18 fichiers) |
| Codes d'éléments | Seulement certains éléments | Tous les éléments basés sur le guide 2026 |
| Extensibilité | Ajout de nouvelles directives = plus de skills | 4 skills fixes, ajout de références uniquement |

**Nouvelle directive ajoutée : Guide de sécurité IA**
- Source : Ministère des Sciences et des TIC / KISA — « Guide de sécurité de l'intelligence artificielle (IA) »
- 54 éléments de vérification pour les développeurs IA (cycle de vie en 6 phases)
- Exigences de sécurité pour les fournisseurs de services IA
- 7 règles de sécurité pour les utilisateurs d'IA

**Mise à jour des directives CII**
- Réextraction complète des éléments basée sur le guide détaillé 2026
- Intégration du système de codes d'éléments (nouveaux codes WEB, HV, CA, etc.)

### v1.0.0 (2026-03-29)

- Version initiale
- 4 skills d'évaluation des vulnérabilités CII (coréen/anglais)
- Éléments techniques (424) + administratifs (127) + physiques (9)

---

## Base juridique

- **Loi sur la protection des infrastructures d'information et de communication** (정보통신기반 보호법)
- **Loi sur l'administration électronique** (전자정부법)
- **Loi sur la protection des données personnelles** (개인정보 보호법)
- **Loi fondamentale sur l'intelligence artificielle** (인공지능 기본법, entrée en vigueur le 22 janvier 2026)

---

## Ressources associées

- [Guide détaillé d'évaluation des vulnérabilités techniques de la KISA](https://www.kisa.or.kr)
- [Guide de sécurité de l'intelligence artificielle (IA)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Conçu avec

| Plugin | Description |
|--------|-------------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill d'aide à la rédaction — Analyse de PDF, extraction de structure, relecture/réécriture |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Compatibilité des hooks de plugins Claude Code pour environnement Windows |

---

## Licence

MIT License

## Auteur

CDPP Corp (https://github.com/cdppcorp)
