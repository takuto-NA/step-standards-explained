# STEP規格解説 (STEP Standards Explained)

> Practical guide to STEP (ISO 10303): versions, capabilities, and implementation.

---

## 🚀 30秒でわかるSTEP

**STEP** は、3D CADデータを異なるCADシステム間で交換するための国際標準規格（ISO 10303）です。

- **ファイル形式**: `.stp` / `.step` (テキストファイル)
- **主な用途**: CAD間のデータ変換、長期保存・アーカイブ
- **STLとの違い**: STLは形状のみ（三角メッシュ）、STEPは色・アセンブリ・PMI（寸法公差）も保持可能

**こんな人のためのリポジトリ**:
- ✅ STEPパーサー/エクスポーターを実装したいエンジニア
- ✅ CADデータ変換プロジェクトの担当者
- ✅ STEP規格を体系的に理解したい実装者

---

## 📚 実装者向け学習パス（推奨順序）

STEP規格に初めて触れる実装者が、効率的に学習できるように構成されています。

### ステップ1: 基礎知識を固める（所要時間: 30分）

1. **[⭐ 用語集](./docs/glossary.md)** - STEP特有の用語を理解（最重要！）
2. **[STEP実装者向けスタートガイド](./docs/getting-started.md)** - 全体像を素早く把握
3. **[FAQ](./docs/faq.md)** - よくある疑問を解消

### ステップ2: プロジェクトに適したAPを選択（所要時間: 15分）

4. **[どのAPを使うべきか？](./decision-guides/which-ap-should-i-use.md)** - 意思決定ガイド
5. **[機能比較マトリックス](./comparison/capability-matrix.md)** - 詳細な機能差を確認

### ステップ3: データ構造を理解する（所要時間: 1-2時間）

6. **[STEPファイル完全解説](./examples/step-file-walkthrough.md)** - 実ファイルを1行ずつ理解
7. **[データモデル・マップ](./format/data-model-map.md)** - エンティティの階層構造を把握
8. **[EXPRESS言語の基礎](./format/express-overview.md)** - スキーマの読み方を学ぶ

### ステップ4: 実装とトラブルシューティング（随時参照）

9. **[よくある落とし穴](./implementation/common-pitfalls.md)** - 実装時の注意点と対策
10. **[バリデーションとCAx-IF](./implementation/validation-and-caxif.md)** - 品質確保の方法

---

## ❓ よくある質問（クイックFAQ）

<details>
<summary><strong>Q1: STEPとSTLの違いは？</strong></summary>

**STL（Stereolithography）**:
- 三角形メッシュのみ
- 色・アセンブリ情報なし
- 精度が低い（近似表現）
- 用途: 3Dプリント

**STEP**:
- 正確な数学的形状（B-rep: 境界表現）
- 色・アセンブリ・PMI（寸法公差）対応
- ファイルサイズ大きめ
- 用途: CAD間データ交換、長期保存
</details>

<details>
<summary><strong>Q2: どのCADがSTEPをサポートしていますか？</strong></summary>

主要なCADソフトはすべてサポートしています:
- SolidWorks, CATIA, NX, Creo, Inventor
- Fusion360, FreeCAD, Rhino 等

ただし、**サポートするAP（規格バージョン）が異なります**。詳細は [CADサポートマトリックス](./comparison/cad-support-matrix.md) を参照してください。
</details>

<details>
<summary><strong>Q3: テキストエディタで開いても大丈夫？</strong></summary>

**はい、大丈夫です**。STEPファイルはプレーンテキストなので、メモ帳やVS Codeで開けます。

ただし:
- 大きなファイル（数十MB以上）は開くのに時間がかかる
- 編集には注意（文法エラーでファイルが壊れる可能性）
- 実際の形状を見るにはSTEPビューワー（FreeCAD等）を使用

**推奨用途**: ヘッダー確認、エンティティ検索、デバッグ
</details>

<details>
<summary><strong>Q4: ファイルサイズが大きいのはなぜ？</strong></summary>

STEPは以下の理由で大きくなりがちです:
- **テキスト形式**: バイナリより冗長
- **完全な形状記述**: 数学的に正確な面・曲線の定義
- **管理情報**: プロダクト、アセンブリ、PMI等のメタデータ

**対策**:
- テセレーション（多角形近似）を使用（AP242）
- 圧縮（.zip や .step.gz）
- 不要な情報を削除
</details>

<details>
<summary><strong>Q5: AP203、AP214、AP242の違いを一言で言うと？</strong></summary>

- **AP203**: 古い。形状のみ。互換性重視。
- **AP214**: 自動車業界発。色・レイヤ対応。現在の標準。
- **AP242**: 最新。PMI（寸法公差）対応。MBD（Model Based Definition）向け。

**実装者向けアドバイス**: 迷ったら **AP242 ed2** が無難です。
</details>

**[→ その他のFAQを見る（20+項目）](./docs/faq.md)**

---

## 📊 クイック比較表

**凡例**: ✅ 完全サポート | ⚠ 部分サポート | ❌ 非サポート

| 機能 | AP203 | AP214 | AP242 ed2 | AP242 ed3 |
| :--- | :---: | :---: | :---: | :---: |
| 3D B-rep | ✅ | ✅ | ✅ | ✅ |
| アセンブリ | ✅ | ✅ | ✅ | ✅ |
| 色・レイヤ | ❌ | ✅ | ✅ | ✅ |
| PMI (表示) | ❌ | ⚠ | ✅ | ✅ |
| PMI (意味型) | ❌ | ❌ | ✅ | ✅ |
| テセレーション | ❌ | ❌ | ✅ | ✅ |
| AM / 電気系 | ❌ | ❌ | ⚠ | ✅ |

**詳細**: [機能マトリックス](./comparison/capability-matrix.md) | [PMIサポート](./comparison/pmi-support.md) | [CAD対応状況](./comparison/cad-support-matrix.md)

---

## 🗺 リポジトリ構成 (Navigation Map)

```
step-standards-explained/
├─ docs/               ← 📘 入門ガイド・用語集・FAQ
├─ decision-guides/    ← 🎯 AP選択ガイド
├─ versions/           ← 📑 AP別詳細（AP203/AP214/AP242 等）
├─ comparison/         ← 📊 機能比較表・CAD対応マトリックス
├─ format/             ← ⚙️ データ構造・EXPRESS解説
├─ implementation/     ← 🔧 実装ノウハウ・落とし穴
└─ examples/           ← 💡 サンプルファイル・解説
```

**推奨**: まず`docs/`で基礎を固め、`decision-guides/`でAPを選び、`format/`と`implementation/`で実装を進める。

---

## 🤝 貢献について (Contributing)

修正の提案や新しい情報は大歓迎です！詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) をご覧ください。

---

## 免責事項

本リポジトリの内容は有志による調査に基づいています。正確な情報は必ず公式のISO規格書を参照してください。[詳細：disclaimer.md](./disclaimer.md)

[LICENSE (CC-BY-4.0)](./LICENSE.md)
