# STEP規格解説 (STEP Standards Explained)

> Practical guide to STEP (ISO 10303): versions, capabilities, and implementation.

## 1. このリポジトリの目的

**STEPの各APが「何ができて、何ができないか」を、膨大な規格書を読まなくても判断できるようにする**

### ターゲット読者
- CAD/PLMシステムの実装者
- 製造IT/データ変換の担当者
- MBD (Model Based Definition) 推進者

---

## 2. クイック比較表

| 機能 | AP203 | AP214 | AP242 |
| :--- | :---: | :---: | :---: |
| 3D B-rep | ✅ | ✅ | ✅ |
| アセンブリ | ✅ | ✅ | ✅ |
| 色・レイヤ | ❌ | ✅ | ✅ |
| PMI (表示) | ❌ | ⚠ | ✅ |
| PMI (意味型) | ❌ | ❌ | ✅ |
| テセレーション | ❌ | ❌ | ✅ |

👉 **[どのAPを使うべきか？（意思決定ガイド）](./decision-guides/which-ap-should-i-use.md)**

---

## 3. コンテンツ構成

### [Versions (各APの解説)](./versions/)
- [AP242 ed2 (最新・全部入り)](./versions/ap242-ed2.md)
- [AP214 (自動車・意匠重視)](./versions/ap214.md)
- [AP203 (Legacy)](./versions/ap203.md)

### [Comparison (機能比較)](./comparison/)
- [機能マトリックス](./comparison/capability-matrix.md)
- [PMIサポートの詳細](./comparison/pmi-support.md)
- [アセンブリ構造](./comparison/assembly-support.md)

### [Format & Implementation (実装ガイド)](./format/)
- [データモデル・マップ (最重要)](./format/data-model-map.md)
- [よくある落とし穴](./implementation/common-pitfalls.md)
- [STEPファイルの最小構成を解読する](./examples/minimal-product.step.md)
- [STEPファイルの基本構造](./format/step-file-basics.md)

---

## 免責事項
本リポジトリの内容は有志による調査に基づいています。正確な情報は必ず公式のISO規格書を参照してください。[詳細：disclaimer.md](./disclaimer.md)
