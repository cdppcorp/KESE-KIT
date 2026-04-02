🌐 [한국어](../README.md) | [English](../README.md#english) | [Francais](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Espanol](README.es.md) | [Deutsch](README.de.md) | [Portugues](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Turkce](README.tr.md) | [Tieng Viet](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

面向关键信息基础设施（CII）漏洞分析评估及AI安全评估的Claude Code技能插件。

---

## 概述

KESE（KISA Enhanced Security Evaluation Kit）是一款基于KISA（韩国互联网振兴院）指南的Claude Code插件，提供全面的安全漏洞分析评估能力。同时支持关键信息基础设施（CII）漏洞分析评估和AI安全评估。

## 功能

| 技能 | 说明 |
|------|------|
| `/kesekit-start` | 运行完整的安全漏洞评估（CII 560+项或AI安全） |
| `/kesekit-check` | 部署前安全合规检查清单 |
| `/kesekit-fix` | 自动生成加固脚本和安全修复方案 |
| `/kesekit-guide` | 为AI工具生成安全编码提示词 |

## 支持的指南

### 1. CII（关键信息基础设施）— 560+项

**技术漏洞评估**
| 系统 | 代码 | 项数 |
|------|------|:----:|
| Unix/Linux服务器 | U-01~U-67 | 67 |
| Windows服务器 | W-01~W-64 | 64 |
| Web服务 | WEB-01~WEB-26 | 26 |
| 安全设备 | S-01~S-23 | 23 |
| 网络设备 | N-01~N-38 | 38 |
| 控制系统 | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| 移动通信 | M-01~M-04 | 4 |
| Web Application | 21个代码 | 21 |
| 虚拟化 | HV-01~HV-25 | 25 |
| 云 | CA-01~CA-19 | 19 |

**管理漏洞评估**：A-1~A-127（127项，14个领域）
**物理漏洞评估**：P-1~P-18（18项）

### 2. AI安全指南 — 54+项

| 对象 | 项数 | 生命周期 |
|------|:----:|---------|
| AI开发者 | 54 | 6个阶段（规划→数据→模型开发→部署→监控→退役） |
| AI服务提供者 | ~43 | 6个阶段（规划→开发→运营→维护→反馈→退役） |
| AI用户 | 7 | 安全最佳实践 |

## 安装

```bash
claude plugins install kesekit
```

## 使用方法

```bash
# 启动完整安全评估
/kesekit-start

# 运行部署前检查清单
/kesekit-check

# 生成加固脚本
/kesekit-fix

# 获取安全编码提示词
/kesekit-guide
```

---

## 项目结构

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← 插件元数据
├── skills/                            ← 英文技能（路由器）
│   ├── start/
│   │   ├── SKILL.md                  ← 路由器（约80行）
│   │   └── references/               ← 按指南分类的知识库
│   │       ├── cii/                  ← CII 14个参考文件
│   │       └── ai-security/          ← AI安全 4个参考文件
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← 韩文技能（相同结构）
├── authorkit/                         ← 源文档及工作成果
│   ├── converted/
│   │   ├── ref-001/                  ← 管理与物理指南（full.md）
│   │   ├── ref-002/                  ← 技术指南（full.md）
│   │   └── ref-003/                  ← AI安全指南（full.md）
│   └── ...
├── 문서/                              ← 源PDF
└── README.md
```

---

## 变更记录

### v2.0.0 (2026-03-30)

**结构重构 — 应用渐进式展示（Progressive Disclosure）模式**

| 变更 | 变更前（v1.0） | 变更后（v2.0） |
|------|---------------|---------------|
| SKILL.md | 所有知识内联（270~465行） | 仅路由器（约50~80行） |
| 指南 | 仅支持CII | 支持CII + AI安全 |
| 知识存储 | 硬编码在SKILL.md中 | 分离至`references/`（18个文件） |
| 项目代码 | 仅包含部分项目 | 基于2026指南收录全部项目 |
| 可扩展性 | 添加新指南需增加技能数量 | 固定4个技能，仅需添加references |

**新增指南：AI安全指南**
- 来源：科学技术信息通信部·韩国互联网振兴院《人工智能（AI）安全指南》
- AI开发者54项验证要素（6阶段生命周期）
- AI服务提供者安全要求
- AI用户7条安全准则

**CII指南更新**
- 基于2026详细指南重新提取全部项目
- 纳入项目代码体系（WEB、HV、CA等新代码）

### v1.0.0 (2026-03-29)

- 初始版本
- CII漏洞分析评估技能4个（韩文/英文）
- 技术（424）+ 管理（127）+ 物理（9）项

---

## 法律依据

- **信息通信基础设施保护法**（정보통신기반 보호법）
- **电子政务法**（전자정부법）
- **个人信息保护法**（개인정보 보호법）
- **人工智能基本法**（인공지능 기본법，2026年1月22日施行）

---

## 相关资料

- [KISA 技术漏洞分析评估详细指南](https://www.kisa.or.kr)
- [人工智能（AI）安全指南](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## 构建工具

| 插件 | 说明 |
|------|------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | 书籍撰写辅助技能 — PDF分析、结构提取、校对/改写 |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Windows环境Claude Code插件钩子兼容性 |

---

## 许可证

MIT License

## 作者

CDPP Corp (https://github.com/cdppcorp)
