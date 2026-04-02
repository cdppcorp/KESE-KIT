🌐 [한국어](../README.md) | [English](../README.md#english) | [Français](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Türkçe](README.tr.md) | [Tiếng Việt](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

Plugin do Claude Code para avaliacao de vulnerabilidades em Infraestruturas Criticas de Informacao (CII) e avaliacao de seguranca de IA, com base nas diretrizes da KISA (Agencia Coreana de Internet e Seguranca).

---

## Visao Geral

KESE (KISA Enhanced Security Evaluation Kit) e um plugin do Claude Code que oferece recursos abrangentes de avaliacao de vulnerabilidades de seguranca com base nas diretrizes da KISA (Agencia Coreana de Internet e Seguranca). Suporta tanto avaliacoes de Infraestruturas Criticas de Informacao (CII) quanto avaliacoes de Seguranca de IA.

## Funcionalidades

| Skill | Descricao |
|-------|-----------|
| `/kesekit-start` | Executar avaliacao completa de vulnerabilidades de seguranca (CII 560+ itens ou Seguranca de IA) |
| `/kesekit-check` | Lista de verificacao de conformidade de seguranca pre-implantacao |
| `/kesekit-fix` | Gerar automaticamente scripts de hardening e correcoes de seguranca |
| `/kesekit-guide` | Gerar prompts de codificacao segura para ferramentas de IA |

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

## Instalacao

```bash
claude plugins install kesekit
```

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
├── skills/                            ← Skills em ingles (roteador)
│   ├── start/
│   │   ├── SKILL.md                  ← Roteador (~80 linhas)
│   │   └── references/               ← Conhecimento por diretriz
│   │       ├── cii/                  ← 14 referencias CII
│   │       └── ai-security/          ← 4 referencias de Seguranca de IA
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← Skills em coreano (mesma estrutura)
├── authorkit/                         ← Documentos originais e artefatos de trabalho
│   ├── converted/
│   │   ├── ref-001/                  ← Guia administrativo/fisico (full.md)
│   │   ├── ref-002/                  ← Guia tecnico (full.md)
│   │   └── ref-003/                  ← Guia de Seguranca de IA (full.md)
│   └── ...
├── 문서/                              ← PDFs originais
└── README.md
```

---

## Historico de Alteracoes

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
