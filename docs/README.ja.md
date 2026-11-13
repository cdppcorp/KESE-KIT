🌐 [한국어](../README.md) | [English](../README.md#english) | [Francais](README.fr.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Русский](README.ru.md) | [Espanol](README.es.md) | [Deutsch](README.de.md) | [Portugues](README.pt.md) | [Italiano](README.it.md) | [العربية](README.ar.md) | [हिन्दी](README.hi.md) | [Turkce](README.tr.md) | [Tieng Viet](README.vi.md) | [ภาษาไทย](README.th.md) | [Bahasa Indonesia](README.id.md) | [Polski](README.pl.md) | [Nederlands](README.nl.md) | [Svenska](README.sv.md) | [Українська](README.uk.md)

---

# KESE - KISA Enhanced Security Evaluation Kit

主要情報通信基盤施設（CII）の脆弱性分析評価、AIセキュリティ評価、ロボットセキュリティ点検、宇宙セキュリティ点検、セキュアコーディングガイド、ゼロトラストセキュリティ評価、SWサプライチェーンセキュリティ（SBOM）のためのClaude Codeスキルプラグインです。

---

## 概要

KESE（KISA Enhanced Security Evaluation Kit）は、KISA（韓国インターネット振興院）のガイドラインに基づいた包括的なセキュリティ脆弱性分析評価機能を提供するClaude Codeプラグインです。主要情報通信基盤施設（CII）の脆弱性分析評価、AIセキュリティ評価、ロボットセキュリティ点検、宇宙セキュリティ点検、セキュアコーディングガイド、ゼロトラストセキュリティ評価に対応しています。

## 機能

| スキル | 説明 |
|--------|------|
| `/kesekit-start` | セキュリティ脆弱性の総合評価を実行（CII 560+ / AIセキュリティ / ロボットセキュリティ / 宇宙セキュリティ / セキュアコーディング / ゼロトラスト / SWサプライチェーン） |
| `/kesekit-check` | デプロイ前のセキュリティコンプライアンスチェックリスト（CII / AI / ロボット / 宇宙 / セキュアコーディング / ゼロトラスト / SWサプライチェーン） |
| `/kesekit-fix` | ハードニングスクリプトおよびセキュリティ修正の自動生成（CII / AI / ロボット / 宇宙 / セキュアコーディング / ゼロトラスト / SWサプライチェーン） |
| `/kesekit-guide` | AIツール向けセキュアコーディングプロンプトの生成（CII / AI / ロボット / 宇宙 / JS・Python・汎用 / ゼロトラスト / SWサプライチェーン） |

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

### 3. ロボットセキュリティ — ~103項目

| カテゴリ | コード | 項目数 | 参照規格 |
|---------|------|:------:|----------|
| セキュアSW開発（SSDF） | SSDF-01~19 | 19 | NIST SP 800-218 |
| サプライチェーンセキュリティ | SC-01~07 | 7 | NIST SP 800-161 |
| 識別・認証 | IA-01~11 | 11 | IEC 62443 |
| 使用制御 | UC-01~11 | 11 | IEC 62443 |
| システム整合性 | SI-01~11 | 11 | IEC 62443 |
| データ保護 | DP-01~04 | 4 | IEC 62443 |
| データフロー制限 | DFR-01~02 | 2 | IEC 62443 |
| イベント対応 | ER-01~03 | 3 | IEC 62443 |
| リソース可用性 | RA-01~08 | 8 | IEC 62443 |
| サイバーレジリエンス | CR-01~13 | 13 | EU CRA |
| 無線セキュリティ | WS-01~14 | 14 | EU RED |

対象：産業用 / サービス用 / 医療用ロボット（ISO 8373）

### 4. 宇宙セキュリティ — 53項目

| 分野 | コード | 項目数 | 参照規格 |
|------|------|:------:|----------|
| アクセス制御 | AC-01~12 | 12 | CMMC, K-RMF |
| 識別・認証 | IA-01~02 | 2 | CMMC, NIS2 |
| システム・通信セキュリティ | SC-01~07 | 7 | NIST IR 8401 |
| システム・情報整合性 | SI-01~04 | 4 | NIST CSF |
| システム/サービス運用管理 | SO-01~09 | 9 | ISMS-P |
| インシデント対応 | IR-01~02 | 2 | NIS2 |
| 人的セキュリティ | PS-01~02 | 2 | CMMC |
| 物理セキュリティ | PE-01~03 | 3 | K-RMF |
| リスク評価・セキュリティ評価 | RA-01~02 | 2 | NIST CSF |
| セキュリティガバナンス | SG-01~04 | 4 | ISMS-P |
| 緊急時対応計画 | CP-01~02 | 2 | NIST IR 8270 |
| サプライチェーン管理 | SM-01~04 | 4 | CMMC, NIS2 |

対象：衛星運用事業者、GSaaS提供者、地上局運用者、宇宙サプライチェーン参加企業

### 5. セキュアコーディングガイド — 46項目

| カテゴリ | 項目数 | CWE数 | 参照規格 |
|---------|:------:|:------:|----------|
| 入力データ検証・表現 | 16 | 18 | CWE/SANS Top 25, OWASP Top 10 |
| セキュリティ機能 | 16 | 16 | CWE/SANS Top 25 |
| 時間・状態 | 2 | 3 | CWE |
| エラー処理 | 3 | 3 | CWE |
| コードエラー | 3 | 3 | CWE |
| カプセル化 | 4 | 5 | CWE |
| API誤用 | 2 | 1 | CWE |

**対応言語：**
| 言語 | 項目数 | フレームワーク |
|------|:------:|-----------|
| Pseudo Code（汎用） | 46 | 言語非依存パターン |
| JavaScript | 42 | Express.js, Sequelize, Mongoose, Node.js crypto |
| Python | 46 | Django, Flask, SQLAlchemy, cryptography |

対象：JavaScript/Python Web開発者、AIツール（Claude, Cursor, Copilot）利用者、バイブコーディング開発者

### 6. ゼロトラストセキュリティ — ~421項目

| コア要素 | コード | 項目数 | 成熟度 |
|----------|------|:------:|--------|
| アイデンティティ | ZT-ID-01~53 | 53 | 従来型/初期/高度/最適化 |
| デバイス・エンドポイント | ZT-DV-01~36 | 36 | 従来型/初期/高度/最適化 |
| ネットワーク | ZT-NW-01~54 | 54 | 従来型/初期/高度/最適化 |
| システム | ZT-SY-01~49 | 49 | 従来型/初期/高度/最適化 |
| アプリケーション・ワークロード | ZT-AP-01~60 | 60 | 従来型/初期/高度/最適化 |
| データ | ZT-DA-01~58 | 58 | 従来型/初期/高度/最適化 |
| 可視性・分析 | ZT-VA-01~43 | 43 | 従来型/初期/高度/最適化 |
| 自動化・オーケストレーション | ZT-AU-01~43 | 43 | 従来型/初期/高度/最適化 |
| OT/ICS特化 | ZT-OT-01~25 | 25 | 従来型/初期/高度/最適化 |

**成熟度4段階**：従来型（Traditional） → 初期（Initial） → 高度（Advanced） → 最適化（Optimal）
**参照規格**：KISA ゼロトラストガイドライン 2.0、NIST SP 800-207、CISA ZT Maturity Model

対象：ゼロトラスト導入企業、OT/ICS環境、クラウド移行組織、セキュリティ成熟度評価担当者

### 7. SWサプライチェーンセキュリティ（SBOM） — 29項目

| フェーズ | コード | 項目数 | 参照規格 |
|----------|--------|:------:|----------|
| 設計 | SC-01~05 | 5 | NIST SP 800-161r1 |
| 開発 | SC-06~16 | 11 | NIST SP 800-218 |
| 供給・配布 | SC-17~19 | 3 | NTIA SBOM |
| デプロイ・運用 | SC-20~26 | 7 | NIS-SBOM |
| 保守 | SC-27~29 | 3 | NIS-SBOM |

## インストール

```
/plugin marketplace add cdppcorp/KESE-KIT
/plugin install kesekit@kesekit
```

> **更新する場合：**
> ```
> /plugin marketplace update kesekit
> /plugin update kesekit@kesekit
> /reload-plugins
> ```

## 使用方法

```bash
# セキュリティ総合評価を開始
/kesekit-start

# デプロイ前チェックリストを実行
/kesekit-check

# ハードニングスクリプトを生成
/kesekit-fix

# セキュアコーディングプロンプトを取得
/kesekit-guide
```

---

## プロジェクト構成

```
KESE-KIT/
├── .claude-plugin/
│   └── marketplace.json              ← プラグインメタデータ
├── skills/                            ← 英語スキル
│   ├── start/
│   │   ├── SKILL.md                  ← ルーター（約80行）
│   │   ├── references/               ← 説明・基準文書
│   │   │   ├── ai-security/          ← 概要、サービス提供者、利用者ガイド
│   │   │   ├── space-security/       ← 概要、サプライチェーン脅威シナリオ
│   │   │   └── zero-trust/           ← ゼロトラスト成熟度・OT/ICS
│   │   ├── templates/                ← 別紙・チェックリストテーブル
│   │   │   ├── cii/                  ← CII 14件の点検項目テーブル
│   │   │   ├── ai-security/          ← AI開発者検証項目、利用者チェックリスト
│   │   │   ├── robot-security/       ← ロボットセキュリティ 6件のチェックリスト
│   │   │   ├── space-security/       ← 宇宙セキュリティ 4件の点検項目テーブル
│   │   │   └── zero-trust/           ← ゼロトラスト 9コア要素チェックリスト
│   │   └── scripts/                  ← 実行可能な点検・修正スクリプト
│   │       ├── cii/                  ← bash, PowerShell, SQLスクリプト
│   │       └── robot-security/       ← ファイアウォール、SBOM、証明書スクリプト
│   ├── check/
│   ├── fix/
│   └── guide/
├── skills-ko/                         ← 韓国語スキル（同一構成）
├── 문서/                              ← 原本PDF（14件）
├── authorkit/                         ← 変換成果物および作業ファイル
│   ├── converted/
│   │   ├── ref-001/                  ← 管理・物理的ガイド（full.md）
│   │   ├── ref-002/                  ← 技術的ガイド（full.md）
│   │   ├── ref-003/                  ← AIセキュリティガイド（full.md）
│   │   ├── ...
│   │   ├── ref-013/                  ← ゼロトラストガイドライン 2.0（full.md）
│   │   ├── ref-014/                  ← ゼロトラスト成熟度モデル解説書（full.md）
│   │   └── ref-015/                  ← OT環境のゼロトラスト適用ガイド（full.md）
│   └── ...
├── docs/                              ← 20ヶ国語README
├── CONTRIBUTING.md
└── README.md
```

---

## 変更履歴

### v4.0.0 (2026-04-03)

**新規ガイドライン追加：ゼロトラストセキュリティ**
- 出典：KISA ゼロトラストガイドライン 2.0（245p） + ゼロトラスト成熟度モデル解説書（182p） + OT環境のゼロトラスト適用ガイド（67p）
- 9つのコア要素、~421件のチェックリスト項目
- 成熟度4段階：Traditional → Initial → Advanced → Optimal
- 参照規格：KISA ゼロトラストガイドライン 2.0、NIST SP 800-207、CISA ZT Maturity Model
- OT/ICS特化項目 25件を含む

### v3.2.0 (2026-04-02)

**新規ガイドライン追加：セキュアコーディングガイド**
- 出典：KISA Javascript セキュアコーディングガイド 159p + Python セキュアコーディングガイド 176p（2023年改訂版）
- 7つのカテゴリ、46項目、49 CWEマッピング
- 汎用 Pseudo Code ガイド新規作成（言語非依存 UNSAFE/SAFE パターン）
- JavaScript (Express.js, Sequelize, Node.js) / Python (Django, Flask, SQLAlchemy) フレームワーク別コード例
- 8つのスキル（EN/KO）すべてに `references/secure-coding/` + `templates/secure-coding/` を配置

### v3.0.0 (2026-04-02)

**Breaking Change：コマンド形式の変更**
- すべてのスキルが単一の `kesekit` ネームスペースに統合
- コマンド形式：`/start` → `/kesekit-start`（ネームスペースプレフィックス追加）

**新規ガイドライン追加：宇宙セキュリティ**
- 出典：宇宙セキュリティモデル Part1 134p + Part2 223p + 解説書 218p
- 12分野、53件のチェックリスト項目
- 参照規格：CMMC, K-RMF, NIS2, ISMS-P, NIST IR 8401/8270, CCSDS

**新規ガイドライン追加：ロボットセキュリティ**（v2.1）
- 出典：ロボットセキュリティモデル（高度化）156p + ロボットセキュリティ脆弱性点検チェックリスト解説書 225p
- 11カテゴリ、~103件のチェックリスト項目
- 参照規格：NIST SP 800-218, IEC 62443, EU CRA, EU RED, NIS2

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
