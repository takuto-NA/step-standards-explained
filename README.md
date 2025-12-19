# STEP規格解説 (STEP Standards Explained)

> Practical guide to STEP (ISO 10303): versions, capabilities, and implementation.

---

## 🚀 はじめに (Getting Started)

このリポジトリは、複雑なSTEP規格を効率的に理解し、実装に役立てるための非公式ガイドです。

1. **全体像を掴む**: [データモデル・マップ](./format/data-model-map.md) でエンティティの階層を確認。
2. **APを選ぶ**: [どのAPを使うべきか？（意思決定ガイド）](./decision-guides/which-ap-should-i-use.md) で用途に合った規格を特定。
3. **実装の要点**: [よくある落とし穴](./implementation/common-pitfalls.md) でハマりやすいポイントを予習。
4. **用語に迷ったら**: [用語集 (Glossary)](./docs/glossary.md) を参照。

---

## 🗺 リポジトリ構成 (Navigation Map)

- `versions/`: [AP242 ed3 (最新)](./versions/ap242-ed3.md), AP242 ed2, AP214, AP203 等の主要バージョン別解説。
- `comparison/`: 機能マトリックスやPMIサポートの比較表。
- `format/`: STEPファイルの基本・データ構造の解説。
- `implementation/`: 実装上のテクニックや注意点。
- `examples/`: [最小構成のSTEPファイル](./examples/minimal-product.step.md) 等のサンプル。
- `reference/`: (Localのみ) 大容量の規格リファレンスHTML（Git管理外）。

---

## 📊 クイック比較表

| 機能 | AP203 | AP214 | AP242 ed2 | AP242 ed3 |
| :--- | :---: | :---: | :---: |
| 3D B-rep | ✅ | ✅ | ✅ | ✅ |
| アセンブリ | ✅ | ✅ | ✅ | ✅ |
| 色・レイヤ | ❌ | ✅ | ✅ | ✅ |
| PMI (表示) | ❌ | ⚠ | ✅ | ✅ |
| PMI (意味型) | ❌ | ❌ | ✅ | ✅ |
| テセレーション | ❌ | ❌ | ✅ | ✅ |
| AM / 電気系 | ❌ | ❌ | ⚠ | ✅ |

---

## 🤝 貢献について (Contributing)

修正の提案や新しい情報は大歓迎です！詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) をご覧ください。

---

## 免責事項
本リポジトリの内容は有志による調査に基づいています。正確な情報は必ず公式のISO規格書を参照してください。[詳細：disclaimer.md](./disclaimer.md)

[LICENSE (CC-BY-4.0)](./LICENSE.md)
