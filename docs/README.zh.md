🌐 [한국어](../README.md) | [English](../README.md#english) | [Francais](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Espanol](README.es.md) | [Deutsch](README.de.md) | [Portugues](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Turkce](README.tr.md) | [Tieng Viet](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

面向关键信息基础设施（CII）漏洞分析评估、AI安全评估、机器人安全检查、太空安全检查、安全编码指南、零信任安全评估、SW供应链安全（SBOM）的Claude Code技能插件。

---

## 概述

KESE（KISA Enhanced Security Evaluation Kit）是一款基于KISA（韩国互联网振兴院）指南的Claude Code插件，提供全面的安全漏洞分析评估能力。支持关键信息基础设施（CII）漏洞分析评估、AI安全评估、机器人安全检查、太空安全检查、安全编码指南、零信任安全评估。

## 功能

| 技能 | 说明 |
|------|------|
| `/kesekit-start` | 运行完整的安全漏洞评估（CII 560+ / AI安全 / 机器人安全 / 太空安全 / 安全编码 / 零信任 / SW供应链） |
| `/kesekit-check` | 部署前安全合规检查清单（CII / AI / 机器人 / 太空 / 安全编码 / 零信任 / SW供应链） |
| `/kesekit-fix` | 自动生成加固脚本和安全修复方案（CII / AI / 机器人 / 太空 / 安全编码 / 零信任 / SW供应链） |
| `/kesekit-guide` | 为AI工具生成安全编码提示词（CII / AI / 机器人 / 太空 / JS·Python·通用 / 零信任 / SW供应链） |

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

### 3. 机器人安全 — ~103项

| 类别 | 代码 | 项数 | 参考标准 |
|------|------|:----:|----------|
| 安全SW开发（SSDF） | SSDF-01~19 | 19 | NIST SP 800-218 |
| 供应链安全 | SC-01~07 | 7 | NIST SP 800-161 |
| 识别与认证 | IA-01~11 | 11 | IEC 62443 |
| 使用控制 | UC-01~11 | 11 | IEC 62443 |
| 系统完整性 | SI-01~11 | 11 | IEC 62443 |
| 数据保护 | DP-01~04 | 4 | IEC 62443 |
| 数据流限制 | DFR-01~02 | 2 | IEC 62443 |
| 事件响应 | ER-01~03 | 3 | IEC 62443 |
| 资源可用性 | RA-01~08 | 8 | IEC 62443 |
| 网络韧性 | CR-01~13 | 13 | EU CRA |
| 无线安全 | WS-01~14 | 14 | EU RED |

适用对象：工业用 / 服务用 / 医疗用机器人（ISO 8373）

### 4. 太空安全 — 53项

| 领域 | 代码 | 项数 | 参考标准 |
|------|------|:----:|----------|
| 访问控制 | AC-01~12 | 12 | CMMC, K-RMF |
| 识别与认证 | IA-01~02 | 2 | CMMC, NIS2 |
| 系统与通信安全 | SC-01~07 | 7 | NIST IR 8401 |
| 系统与信息完整性 | SI-01~04 | 4 | NIST CSF |
| 系统/服务运维管理 | SO-01~09 | 9 | ISMS-P |
| 事件响应 | IR-01~02 | 2 | NIS2 |
| 人员安全 | PS-01~02 | 2 | CMMC |
| 物理安全 | PE-01~03 | 3 | K-RMF |
| 风险评估与安全评估 | RA-01~02 | 2 | NIST CSF |
| 安全治理 | SG-01~04 | 4 | ISMS-P |
| 应急计划 | CP-01~02 | 2 | NIST IR 8270 |
| 供应链管理 | SM-01~04 | 4 | CMMC, NIS2 |

适用对象：卫星运营商、GSaaS提供商、地面站运营商、太空供应链参与企业

### 5. 安全编码指南 — 46项

| 类别 | 项数 | CWE数 | 参考标准 |
|------|:----:|:----:|----------|
| 输入数据验证与表示 | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| 安全功能 | 16 | 16 | CWE/SANS Top 25 |
| 时间与状态 | 2 | 3 | CWE |
| 错误处理 | 3 | 3 | CWE |
| 代码错误 | 3 | 3 | CWE |
| 封装 | 4 | 5 | CWE |
| API误用 | 2 | 1 | CWE |

**支持语言：**
| 语言 | 项数 | 框架 |
|------|:----:|------|
| Pseudo Code（通用） | 46 | 语言无关模式 |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

适用对象：JavaScript/Python Web开发者、AI工具（Claude, Cursor, Copilot）用户、Vibe编程开发者

### 6. 零信任安全 — ~421项

| 核心要素 | 代码 | 项数 | 成熟度 |
|----------|------|:----:|--------|
| 身份认证 | ZT-ID-01~53 | 53 | 传统/初始/高级/最优 |
| 设备与终端 | ZT-DV-01~36 | 36 | 传统/初始/高级/最优 |
| 网络 | ZT-NW-01~54 | 54 | 传统/初始/高级/最优 |
| 系统 | ZT-SY-01~49 | 49 | 传统/初始/高级/最优 |
| 应用与工作负载 | ZT-AP-01~60 | 60 | 传统/初始/高级/最优 |
| 数据 | ZT-DA-01~58 | 58 | 传统/初始/高级/最优 |
| 可视性与分析 | ZT-VA-01~43 | 43 | 传统/初始/高级/最优 |
| 自动化与编排 | ZT-AU-01~43 | 43 | 传统/初始/高级/最优 |
| OT/ICS专用 | ZT-OT-01~25 | 25 | 传统/初始/高级/最优 |

**4个成熟度等级**：传统（Traditional） → 初始（Initial） → 高级（Advanced） → 最优（Optimal）
**参考标准**：KISA 零信任指南 2.0、NIST SP 800-207、CISA ZT Maturity Model

适用对象：零信任实施企业、OT/ICS环境、云迁移组织、安全成熟度评估负责人

### 7. SW供应链安全（SBOM） — 29项

| 阶段 | 代码 | 项数 | 参考标准 |
|------|------|:----:|----------|
| 设计 | SC-01~05 | 5 | NIST SP 800-161r1 |
| 开发 | SC-06~16 | 11 | NIST SP 800-218 |
| 供应/分发 | SC-17~19 | 3 | NTIA SBOM |
| 部署与运维 | SC-20~26 | 7 | NIS-SBOM |
| 维护 | SC-27~29 | 3 | NIS-SBOM |

## 安装

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

> **更新时：**
> ```
> /plugin marketplace update kesekit
> /plugin update kesekit@kesekit
> /reload-plugins
> ```

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
├── skills/                            ← 英文技能
│   ├── start/
│   │   ├── SKILL.md                  ← 路由器（约80行）
│   │   ├── references/               ← 说明/基准文档
│   │   │   ├── ai-security/          ← 概要、服务提供者、用户指南
│   │   │   ├── space-security/       ← 概要、供应链威胁场景
│   │   │   └── zero-trust/           ← 零信任成熟度、OT/ICS
│   │   ├── templates/                ← 附表、检查清单表格
│   │   │   ├── cii/                  ← CII 14项检查表
│   │   │   ├── ai-security/          ← AI开发者验证项、用户检查清单
│   │   │   ├── robot-security/       ← 机器人安全 6项检查清单
│   │   │   ├── space-security/       ← 太空安全 4项检查表
│   │   │   └── zero-trust/           ← 零信任 9核心要素检查清单
│   │   └── scripts/                  ← 可执行的检查/修复脚本
│   │       ├── cii/                  ← bash, PowerShell, SQL脚本
│   │       └── robot-security/       ← 防火墙、SBOM、证书脚本
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← 韩文技能（相同结构）
├── 문서/                              ← 源PDF（14份）
├── authorkit/                         ← 转换产出物及工作文件
│   ├── converted/
│   │   ├── ref-001/                  ← 管理与物理指南（full.md）
│   │   ├── ref-002/                  ← 技术指南（full.md）
│   │   ├── ref-003/                  ← AI安全指南（full.md）
│   │   ├── ...
│   │   ├── ref-013/                  ← 零信任指南 2.0（full.md）
│   │   ├── ref-014/                  ← 零信任成熟度模型解说书（full.md）
│   │   └── ref-015/                  ← OT环境的零信任应用指南（full.md）
│   └── ...
├── docs/                              ← 20种语言README
├── CONTRIBUTING.md
└── README.md
```

---

## 变更记录

### v4.0.0 (2026-04-03)

**新增指南：零信任安全**
- 来源：KISA 零信任指南 2.0（245p） + 零信任成熟度模型解说书（182p） + OT环境的零信任应用指南（67p）
- 9个核心要素，~421项检查清单
- 4个成熟度等级：Traditional → Initial → Advanced → Optimal
- 参考标准：KISA 零信任指南 2.0、NIST SP 800-207、CISA ZT Maturity Model
- 含OT/ICS专用项目 25项

### v3.2.0 (2026-04-02)

**新增指南：安全编码指南**
- 来源：KISA Javascript 安全编码指南 159p + Python 安全编码指南 176p（2023年修订版）
- 7个类别、46项、49 CWE映射
- 新建通用 Pseudo Code 指南（语言无关 UNSAFE/SAFE 模式）
- JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy) 框架代码示例
- 8个技能（EN/KO）均配置 `references/secure-coding/` + `templates/secure-coding/`

### v3.0.0 (2026-04-02)

**Breaking Change：命令格式变更**
- 所有技能统一至 `kesekit` 命名空间
- 命令格式：`/start` → `/kesekit-start`（添加命名空间前缀）

**新增指南：太空安全**
- 来源：太空安全模型 Part1 134p + Part2 223p + 解说书 218p
- 12个领域、53项检查清单
- 参考标准：CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, CCSDS

**新增指南：机器人安全**（v2.1）
- 来源：机器人安全模型（高级版）156p + 机器人安全漏洞检查清单解说书 225p
- 11个类别、~103项检查清单
- 参考标准：NIST SP 800-218, IEC 62443, EU CRA, EU RED, NIS2

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
