🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin do Claude Code para avaliacao de vulnerabilidades em Infraestruturas Criticas de Informacao (CII), avaliacao de seguranca de IA, inspecao de seguranca de robos, inspecao de seguranca espacial, guia de codificacao segura, avaliacao de seguranca Zero Trust e seguranca da cadeia de suprimentos SW (SBOM).

---

## Visao Geral

KESE (KISA Enhanced Security Evaluation Kit) e um plugin do Claude Code que oferece recursos abrangentes de avaliacao de vulnerabilidades de seguranca com base nas diretrizes da KISA (Agencia Coreana de Internet e Seguranca). Suporta avaliacoes CII, seguranca de IA, seguranca de robos, seguranca espacial, codificacao segura e avaliacao de seguranca Zero Trust.

## Funcionalidades

| Skill | Descricao |
|-------|-----------|
| `/kesekit-start` | Executar avaliacao completa de vulnerabilidades de seguranca (CII 560+ / Seguranca de IA / Seguranca de robos / Seguranca espacial / Codificacao segura / Zero Trust / Cadeia de suprimentos SW) |
| `/kesekit-check` | Lista de verificacao de conformidade de seguranca pre-implantacao (CII / IA / Robos / Espaco / Codificacao segura / Zero Trust / Cadeia de suprimentos SW) |
| `/kesekit-fix` | Gerar automaticamente scripts de hardening e correcoes de seguranca (CII / IA / Robos / Espaco / Codificacao segura / Zero Trust / Cadeia de suprimentos SW) |
| `/kesekit-guide` | Gerar prompts de codificacao segura para ferramentas de IA (CII / IA / Robos / Espaco / JS·Python·Generico / Zero Trust / Cadeia de suprimentos SW) |

## Diretrizes Suportadas

### 1. CII (Infraestruturas Criticas de Informacao) — 560+ itens

**Avaliacao Tecnica**
| Sistema | Codigo | Itens |
|---------|--------|:-----:|
| Servidor Unix/Linux | U-01~U-67 | 67 |
| Servidor Windows | W-01~W-64 | 64 |
| Servico Web | WEB-01~WEB-26 | 26 |
| Equipamento de Seguranca | S-01~S-23 | 23 |
| Equipamento de Rede | N-01~N-38 | 38 |
| Sistema de Controle | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| Dispositivo Movel | M-01~M-04 | 4 |
| Aplicacao Web | 21 codigos | 21 |
| Virtualizacao | HV-01~HV-25 | 25 |
| Nuvem | CA-01~CA-19 | 19 |

**Avaliacao Administrativa**: A-1~A-127 (127 itens, 14 dominios)
**Avaliacao Fisica**: P-1~P-18 (18 itens)

### 2. Guia de Seguranca de IA — 54+ itens

| Publico-alvo | Itens | Ciclo de Vida |
|--------------|:-----:|---------------|
| Desenvolvedor de IA | 54 | 6 etapas (Planejamento→Dados→Modelo→Implantacao→Monitoramento→Descarte) |
| Provedor de Servicos | ~43 | 6 etapas (Planejamento→Desenvolvimento→Operacao→Manutencao→Feedback→Descarte) |
| Usuario | 7 | Boas praticas de seguranca |

### 3. Seguranca de Robos — ~103 itens

| Categoria | Codigo | Itens | Padroes de referencia |
|-----------|--------|:-----:|------------------------|
| Desenvolvimento SW seguro (SSDF) | SSDF-01~19 | 19 | NIST SP 800-218 |
| Seguranca da cadeia de suprimentos | SC-01~07 | 7 | NIST SP 800-161 |
| Identificacao e autenticacao | IA-01~11 | 11 | IEC 62443 |
| Controle de uso | UC-01~11 | 11 | IEC 62443 |
| Integridade do sistema | SI-01~11 | 11 | IEC 62443 |
| Protecao de dados | DP-01~04 | 4 | IEC 62443 |
| Restricao de fluxo de dados | DFR-01~02 | 2 | IEC 62443 |
| Resposta a eventos | ER-01~03 | 3 | IEC 62443 |
| Disponibilidade de recursos | RA-01~08 | 8 | IEC 62443 |
| Ciber-resiliencia | CR-01~13 | 13 | EU CRA |
| Seguranca sem fio | WS-01~14 | 14 | EU RED |

Publico-alvo: robos industriais / de servico / medicos (ISO 8373)

### 4. Seguranca Espacial — 53 itens

| Area | Codigo | Itens | Padroes de referencia |
|------|--------|:-----:|------------------------|
| Controle de acesso | AC-01~12 | 12 | CMMC, K-RMF |
| Identificacao e autenticacao | IA-01~02 | 2 | CMMC, NIS2 |
| Seguranca de sistemas e comunicacoes | SC-01~07 | 7 | NIST IR 8401 |
| Integridade de sistemas e informacoes | SI-01~04 | 4 | NIST CSF |
| Gestao de operacoes de sistema/servico | SO-01~09 | 9 | ISMS-P |
| Resposta a incidentes | IR-01~02 | 2 | NIS2 |
| Seguranca de pessoal | PS-01~02 | 2 | CMMC |
| Seguranca fisica | PE-01~03 | 3 | K-RMF |
| Avaliacao de riscos e seguranca | RA-01~02 | 2 | NIST CSF |
| Governanca de seguranca | SG-01~04 | 4 | ISMS-P |
| Plano de contingencia | CP-01~02 | 2 | NIST IR 8270 |
| Gestao da cadeia de suprimentos | SM-01~04 | 4 | CMMC, NIS2 |

Publico-alvo: operadores de satelites, provedores GSaaS, operadores de estacoes terrestres, empresas da cadeia de suprimentos espacial

### 5. Guia de Codificacao Segura — 46 itens

| Categoria | Itens | CWE | Padroes de referencia |
|-----------|:-----:|:---:|------------------------|
| Validacao de dados de entrada e representacao | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| Funcoes de seguranca | 16 | 16 | CWE/SANS Top 25 |
| Tempo e estado | 2 | 3 | CWE |
| Tratamento de erros | 3 | 3 | CWE |
| Erros de codigo | 3 | 3 | CWE |
| Encapsulamento | 4 | 5 | CWE |
| Uso incorreto de API | 2 | 1 | CWE |

**Linguagens suportadas:**
| Linguagem | Itens | Frameworks |
|-----------|:-----:|-----------|
| Pseudo Code (generico) | 46 | Padroes independentes de linguagem |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

Publico-alvo: desenvolvedores web JavaScript/Python, usuarios de ferramentas IA (Claude, Cursor, Copilot), desenvolvedores de vibe coding

### 6. Seguranca Zero Trust — ~421 itens

| Elemento central | Codigo | Itens | Maturidade |
|------------------|--------|:-----:|------------|
| Identidade | ZT-ID-01~53 | 53 | Tradicional/Inicial/Avancado/Otimo |
| Dispositivo e ponto final | ZT-DV-01~36 | 36 | Tradicional/Inicial/Avancado/Otimo |
| Rede | ZT-NW-01~54 | 54 | Tradicional/Inicial/Avancado/Otimo |
| Sistema | ZT-SY-01~49 | 49 | Tradicional/Inicial/Avancado/Otimo |
| Aplicacao e carga de trabalho | ZT-AP-01~60 | 60 | Tradicional/Inicial/Avancado/Otimo |
| Dados | ZT-DA-01~58 | 58 | Tradicional/Inicial/Avancado/Otimo |
| Visibilidade e analise | ZT-VA-01~43 | 43 | Tradicional/Inicial/Avancado/Otimo |
| Automacao e orquestracao | ZT-AU-01~43 | 43 | Tradicional/Inicial/Avancado/Otimo |
| OT/ICS especifico | ZT-OT-01~25 | 25 | Tradicional/Inicial/Avancado/Otimo |

**4 niveis de maturidade**: Tradicional (Traditional) → Inicial (Initial) → Avancado (Advanced) → Otimo (Optimal)
**Padroes de referencia**: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model

Publico-alvo: empresas adotando Zero Trust, ambientes OT/ICS, organizacoes em migracao para nuvem, responsaveis por avaliacao de maturidade de seguranca

### 7. Seguranca da cadeia de suprimentos SW (SBOM) — 29 itens

| Fase | Codigo | Itens | Padroes de referencia |
|------|--------|:-----:|------------------------|
| Projeto | SC-01~05 | 5 | NIST SP 800-161r1 |
| Desenvolvimento | SC-06~16 | 11 | NIST SP 800-218 |
| Fornecimento/Distribuicao | SC-17~19 | 3 | NTIA SBOM |
| Implantacao e operacoes | SC-20~26 | 7 | NIS-SBOM |
| Manutencao | SC-27~29 | 3 | NIS-SBOM |

## Instalacao

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

> **Para atualizar:**
> ```
> /plugin marketplace update kesekit
> /plugin update kesekit@kesekit
> /reload-plugins
> ```

## Uso

```bash
# Iniciar avaliacao completa de seguranca
/kesekit-start

# Executar lista de verificacao pre-implantacao
/kesekit-check

# Gerar scripts de hardening
/kesekit-fix

# Obter prompts de codificacao segura
/kesekit-guide
```

---

## Estrutura do Projeto

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← Metadados do plugin
├── skills/                            ← Skills em ingles
│   ├── start/
│   │   ├── SKILL.md                  ← Roteador (~80 linhas)
│   │   ├── references/               ← Documentos de descricao/criterios
│   │   │   ├── ai-security/          ← Visao geral, provedor de servicos, guia do usuario
│   │   │   ├── space-security/       ← Visao geral, cenarios de ameacas da cadeia de suprimentos
│   │   │   └── zero-trust/           ← Maturidade Zero Trust, OT/ICS
│   │   ├── templates/                ← Formularios anexos, tabelas de checklist
│   │   │   ├── cii/                  ← 14 tabelas de verificacao CII
│   │   │   ├── ai-security/          ← Verificacao de desenvolvedor IA, checklist de usuario
│   │   │   ├── robot-security/       ← 6 checklists de seguranca de robos
│   │   │   ├── space-security/       ← 4 tabelas de verificacao de seguranca espacial
│   │   │   └── zero-trust/           ← 9 checklists de elementos centrais Zero Trust
│   │   └── scripts/                  ← Scripts de verificacao/correcao executaveis
│   │       ├── cii/                  ← Scripts bash, PowerShell, SQL
│   │       └── robot-security/       ← Scripts de firewall, SBOM, certificados
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skills em coreano (mesma estrutura)
├── 문서/                              ← PDFs originais (14)
├── authorkit/                         ← Documentos originais e artefatos de trabalho
│   ├── converted/
│   │   ├── ref-001/                  ← Guia administrativo/fisico (full.md)
│   │   ├── ref-002/                  ← Guia tecnico (full.md)
│   │   ├── ref-003/                  ← Guia de Seguranca de IA (full.md)
│   │   ├── ...
│   │   ├── ref-013/                  ← Zero Trust Guideline 2.0 (full.md)
│   │   ├── ref-014/                  ← Guia do modelo de maturidade Zero Trust (full.md)
│   │   └── ref-015/                  ← Guia de aplicacao Zero Trust para OT (full.md)
│   └── ...
├── docs/                              ← README em 20 idiomas
├── CONTRIBUTING.md
└── README.md
```

---

## Historico de Alteracoes

### v4.0.0 (2026-04-03)

**Nova Diretriz: Seguranca Zero Trust**
- Fonte: KISA Zero Trust Guideline 2.0 (245p) + Guia do modelo de maturidade Zero Trust (182p) + Guia de aplicacao Zero Trust para OT (67p)
- 9 elementos centrais, ~421 itens de checklist
- 4 niveis de maturidade: Traditional → Initial → Advanced → Optimal
- Padroes de referencia: KISA Zero Trust Guideline 2.0, NIST SP 800-207, CISA ZT Maturity Model
- 25 itens especificos de OT/ICS incluidos

### v3.2.0 (2026-04-02)

**Nova Diretriz: Guia de Codificacao Segura**
- Fonte: KISA Javascript Secure Coding Guide 159p + Python Secure Coding Guide 176p (edicao revisada 2023)
- 7 categorias, 46 itens, 49 mapeamentos CWE
- Novo guia generico Pseudo Code (padroes UNSAFE/SAFE independentes de linguagem)
- Exemplos de codigo por framework: JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy)
- `references/secure-coding/` + `templates/secure-coding/` implantados em todos os 8 skills (EN/KO)

### v3.0.0 (2026-04-02)

**Breaking Change: Mudanca de formato de comandos**
- Todos os skills unificados sob o namespace `kesekit`
- Formato de comandos: `/start` → `/kesekit-start` (prefixo de namespace adicionado)

**Nova Diretriz: Seguranca Espacial**
- Fonte: Modelo de seguranca espacial Part1 134p + Part2 223p + Guia explicativo 218p
- 12 areas, 53 itens de checklist
- Padroes de referencia: CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, CCSDS

**Nova Diretriz: Seguranca de Robos** (v2.1)
- Fonte: Modelo de seguranca de robos (avancado) 156p + Guia de checklist de seguranca de robos 225p
- 11 categorias, ~103 itens de checklist
- Padroes de referencia: NIST SP 800-218, IEC 62443, EU CRA, EU RED, NIS2

### v2.0.0 (2026-03-30)

**Refatoracao de Estrutura — Aplicacao do padrao Progressive Disclosure**

| Alteracao | Antes (v1.0) | Depois (v2.0) |
|-----------|-------------|--------------|
| SKILL.md | Todo o conhecimento inline (270~465 linhas) | Apenas roteador (~50~80 linhas) |
| Diretrizes | Somente CII | CII + Seguranca de IA |
| Armazenamento de conhecimento | Hardcoded no SKILL.md | Separado em `references/` (18 arquivos) |
| Codigos de itens | Apenas alguns itens incluidos | Todos os itens com base no guia 2026 |
| Extensibilidade | Adicao de novas diretrizes aumentava o numero de skills | 4 skills fixos, apenas referencias adicionadas |

**Nova Diretriz Adicionada: Guia de Seguranca de IA**
- Fonte: Ministerio da Ciencia e TIC / KISA "Guia de Seguranca de Inteligencia Artificial (IA)"
- 54 itens de verificacao para desenvolvedores de IA (ciclo de vida de 6 etapas)
- Requisitos de seguranca para provedores de servicos de IA
- 7 praticas de seguranca para usuarios de IA

**Atualizacao das Diretrizes CII**
- Reextracao completa de todos os itens com base no guia detalhado de 2026
- Reflexao do sistema de codigos de itens (novos codigos como WEB, HV, CA)

### v1.0.0 (2026-03-29)

- Lancamento inicial
- 4 skills de avaliacao de vulnerabilidades CII (coreano/ingles)
- Itens tecnicos (424) + administrativos (127) + fisicos (9)

---

## Base Legal

- **Lei de Protecao de Infraestruturas de Informacao e Comunicacao** (정보통신기반 보호법)
- **Lei de Governo Eletronico** (전자정부법)
- **Lei de Protecao de Informacoes Pessoais** (개인정보 보호법)
- **Lei Basica de Inteligencia Artificial** (인공지능 기본법, em vigor desde 22/01/2026)

---

## Recursos Relacionados

- [Guia Detalhado de Avaliacao de Vulnerabilidades Tecnicas da KISA](https://www.kisa.or.kr)
- [Guia de Seguranca de Inteligencia Artificial (IA)](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 para LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## Construido Com

| Plugin | Descricao |
|--------|-----------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | Skill de apoio a redacao de livros - analise de PDF, extracao de estrutura, revisao/reescrita |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Compatibilidade de hooks de plugins do Claude Code para ambiente Windows |

---

## Licenca

MIT License

## Autor

CDPP Corp (https://github.com/cdppcorp)
