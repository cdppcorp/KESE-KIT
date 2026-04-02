🌐 [한국어](../README.md) | [English](../README.md#english) | [Francais](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Espanol](README.es.md) | [Deutsch](README.de.md) | [Portugues](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Turkce](README.tr.md) | [Tieng Viet](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

主要情報通信基盤施設（CII）の脆弱性分析評価およびAIセキュリティ評価のためのClaude Codeスキルプラグインです。

---

## 概要

KESE（KISA Enhanced Security Evaluation Kit）は、KISA（韓国インターネット振興院）のガイドラインに基づいた包括的なセキュリティ脆弱性分析評価機能を提供するClaude Codeプラグインです。主要情報通信基盤施設（CII）の脆弱性分析評価とAIセキュリティ評価の両方に対応しています。

## 機能

| スキル | 説明 |
|--------|------|
| `/kesekit:start` | セキュリティ脆弱性の総合評価を実行（CII 560+項目またはAIセキュリティ） |
| `/kesekit:check` | デプロイ前のセキュリティコンプライアンスチェックリスト |
| `/kesekit:fix` | ハードニングスクリプトおよびセキュリティ修正の自動生成 |
| `/kesekit:guide` | AIツール向けセキュアコーディングプロンプトの生成 |

## 対応ガイドライン

### 1. CII（主要情報通信基盤施設）— 560+項目

**技術的脆弱性評価**
| システム | コード | 項目数 |
|----------|--------|:------:|
| Unix/Linuxサーバー | U-01~U-67 | 67 |
| Windowsサーバー | W-01~W-64 | 64 |
| Webサービス | WEB-01~WEB-26 | 26 |
| セキュリティ機器 | S-01~S-23 | 23 |
| ネットワーク機器 | N-01~N-38 | 38 |
| 制御システム | C-01~C-51 | 46 |
| PC | PC-01~PC-18 | 18 |
| DBMS | D-01~D-26 | 26 |
| モバイル | M-01~M-04 | 4 |
| Web Application | 21コード | 21 |
| 仮想化 | HV-01~HV-25 | 25 |
| クラウド | CA-01~CA-19 | 19 |

**管理的脆弱性評価**：A-1~A-127（127項目、14分野）
**物理的脆弱性評価**：P-1~P-18（18項目）

### 2. AIセキュリティガイド — 54+項目

| 対象 | 項目数 | ライフサイクル |
|------|:------:|---------------|
| AI開発者 | 54 | 6段階（計画→データ→モデル開発→デプロイ→モニタリング→廃棄） |
| AIサービス提供者 | ~43 | 6段階（計画→開発→運用→保守→フィードバック→廃棄） |
| AI利用者 | 7 | セキュリティベストプラクティス |

## インストール

```bash
claude plugins install kesekit
```

## 使用方法

```bash
# セキュリティ総合評価を開始
/kesekit:start

# デプロイ前チェックリストを実行
/kesekit:check

# ハードニングスクリプトを生成
/kesekit:fix

# セキュアコーディングプロンプトを取得
/kesekit:guide
```

---

## プロジェクト構成

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← プラグインメタデータ
├── skills/                            ← 英語スキル（ルーター）
│   ├── start/
│   │   ├── SKILL.md                  ← ルーター（約80行）
│   │   └── references/               ← ガイドライン別ナレッジ
│   │       ├── cii/                  ← CII 14件のリファレンス
│   │       └── ai-security/          ← AIセキュリティ 4件のリファレンス
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← 韓国語スキル（同一構成）
├── authorkit/                         ← 原本ドキュメントおよび成果物
│   ├── converted/
│   │   ├── ref-001/                  ← 管理・物理的ガイド（full.md）
│   │   ├── ref-002/                  ← 技術的ガイド（full.md）
│   │   └── ref-003/                  ← AIセキュリティガイド（full.md）
│   └── ...
├── 문서/                              ← 原本PDF
└── README.md
```

---

## 変更履歴

### v2.0.0 (2026-03-30)

**構造リファクタリング — Progressive Disclosureパターンの適用**

| 変更点 | 変更前（v1.0） | 変更後（v2.0） |
|--------|---------------|---------------|
| SKILL.md | すべてのナレッジをインライン化（270~465行） | ルーターのみ（約50~80行） |
| ガイドライン | CIIのみ対応 | CII + AIセキュリティ対応 |
| ナレッジ格納 | SKILL.mdにハードコーディング | `references/`に分離（18ファイル） |
| 項目コード | 一部の項目のみ含有 | 2026年ガイド基準で全項目を収録 |
| 拡張性 | 新ガイドライン追加時にスキル数が増加 | スキル4つ固定、リファレンスのみ追加 |

**新規ガイドライン追加：AIセキュリティガイド**
- 出典：科学技術情報通信部・韓国インターネット振興院「人工知能（AI）セキュリティガイド」
- AI開発者向け54件の検証項目（6段階ライフサイクル）
- AIサービス提供者向けセキュリティ要件
- AI利用者向けセキュリティルール7件

**CIIガイドラインの更新**
- 2026年詳細ガイドに基づき全項目を再抽出
- 項目コード体系の反映（WEB、HV、CAなど新規コード）

### v1.0.0 (2026-03-29)

- 初回リリース
- CII脆弱性分析評価スキル4つ（韓国語/英語）
- 技術的（424）+ 管理的（127）+ 物理的（9）項目

---

## 法的根拠

- **情報通信基盤保護法**（정보통신기반 보호법）
- **電子政府法**（전자정부법）
- **個人情報保護法**（개인정보 보호법）
- **人工知能基本法**（인공지능 기본법、2026年1月22日施行）

---

## 関連資料

- [KISA 技術的脆弱性分析評価 詳細ガイド](https://www.kisa.or.kr)
- [人工知能（AI）セキュリティガイド](https://www.kisa.or.kr)
- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## 使用ツール

| プラグイン | 説明 |
|-----------|------|
| [authorkit-ko](https://github.com/cdppcorp/authorkit) | 書籍執筆支援スキル — PDF分析、構造抽出、推敲・リライト |
| [win-hooks](https://github.com/anthropics/claude-code-plugins) | Windows環境 Claude Codeプラグインフック互換性 |

---

## ライセンス

MIT License

## 作者

CDPP Corp (https://github.com/cdppcorp)
