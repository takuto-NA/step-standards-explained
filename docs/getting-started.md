# STEP実装者向けスタートガイド (Getting Started)

**所要時間**: 10分

このガイドは、CAD経験はあるがSTEP規格に初めて触れる実装者向けに、STEPの基礎を素早く理解するための超入門です。

---

## 🎯 この10分で理解すること

1. STEPとは何か（実装者視点）
2. 最初の一歩: STEPファイルを読む
3. 推奨ツールとリソース
4. 次に読むべきドキュメント

---

## 1. STEPとは（実装者視点）

### 基本的な性質

**STEP** (Standard for the Exchange of Product model data, ISO 10303) は:
- **テキストベース**のCADデータ交換フォーマット
- **B-rep**（境界表現）で3D形状を表現
- 形状だけでなく**管理情報**（Product、Assembly）や**PMI**（寸法公差）も格納可能

---

## Part 21形式とは？

**Part 21** は、STEPデータをテキストファイルとして保存するための規格です。

### 正式名称と由来

- **正式名称**: ISO 10303-21 "Clear text encoding of the exchange structure"
- **策定**: ISO（国際標準化機構）
- **初版発行**: 1994年
- **最新版**: ISO 10303-21:2016

### なぜ「Part 21」？

STEP規格（ISO 10303）は、数百のパートに分かれた巨大な規格群です:

#### 主要なパート一覧

**Part 1-20番台: 基礎・共通仕様**
- Part 11: EXPRESS言語（データモデル定義言語）
- Part 21: **テキストファイル形式（ASCII/Clear text）** ← **最重要！**
- Part 28: XML形式

**Part 40-50番台: 統合リソース**
- Part 41: 製品記述とサポートの基礎
- Part 42: 幾何・位相表現
- Part 43: 表現構造
- Part 44: 製品構造設定
- Part 45: 材料・その他

**Part 100番台: 統合アプリケーションリソース**
- Part 101: 図面
- Part 104: 有限要素解析
- Part 105: 運動学

**Part 200番台: Application Protocols (AP) - 実装者が最も使う**
- Part 203: **AP203** - 形状管理3D設計
- Part 214: **AP214** - 自動車設計
- Part 238: AP238 - CNC加工
- Part 242: **AP242** - モデルベース3Dエンジニアリング（最新・最重要）

**Part 500番台以降: 抽象テストスイート等**

#### 実装者が知るべきパート

実際の実装で重要なのは以下の5つだけ:

1. **Part 21** (テキストファイル形式) ← ファイルの読み書き
2. **Part 11** (EXPRESS) ← スキーマの理解
3. **Part 203, 214, 242** (AP) ← どのAPを使うか

**Part 21** は「第21番目のパート」という意味で、STEPデータの**エンコーディング方式**（ファイルへの保存方法）を定義しています。

### 他の形式との関係

| 規格 | ファイル形式 | 特徴 |
|------|------------|------|
| **Part 21** | `.stp`, `.step` (ASCII) | 人間が読める、最も普及 |
| Part 28 | `.stpx`, `.stpZ` (XML) | XML技術との親和性、冗長 |
| - | (バイナリ形式) | 公式にはなし |

**実務**: 99%以上のSTEPファイルがPart 21形式です。

---

## Part 21形式の基本構造

最も一般的なSTEPファイル（`.stp` / `.step`）は **Part 21** 形式で、以下の構造を持ちます:

```step
ISO-10303-21;                  ← Part 21形式の宣言
HEADER;                         ← ファイルのメタデータ
  FILE_DESCRIPTION(...);
  FILE_NAME(...);
  FILE_SCHEMA(...);            ← 使用するAP（重要！）
ENDSEC;
DATA;                           ← 実データ
  #10 = PRODUCT(...);          ← エンティティのインスタンス
  #20 = PRODUCT_DEFINITION_FORMATION(...);
  ...
ENDSEC;
END-ISO-10303-21;
```

### 3つの重要概念

#### ① Entity (エンティティ)
データの「型」。オブジェクト指向の「クラス」に相当。
- 例: `PRODUCT`, `SHAPE_REPRESENTATION`, `ADVANCED_FACE`
- すべて大文字で表記

#### ② Instance (インスタンス)
エンティティの具体的なデータ。`#番号`で識別。
```step
#10 = PRODUCT('Part_A', 'Part_A', 'Description', (#20));
```
- `#10` = インスタンスID
- `PRODUCT` = エンティティ型
- `'Part_A', ...` = 属性値

#### ③ Reference (参照)
`#番号`で他のインスタンスを参照。
```step
#10 = PRODUCT(..., (#20));  ← #20を参照
#20 = PRODUCT_CONTEXT(...);
```

**パーサー実装のポイント**:
- インスタンスIDは1から始まり、ファイル内でユニーク
- **前方参照**が可能（後で定義されるインスタンスを先に参照できる）
- 参照の解決にはハッシュマップ（辞書）が効率的

---

## 2. 最初の一歩: STEPファイルを読む

### ステップ1: テキストエディタで開く

STEPファイルはプレーンテキストなので、**メモ帳**や**VS Code**でそのまま開けます。

1. 任意の`.step`ファイルを用意
2. テキストエディタで開く
3. HEADERセクションを確認

### ステップ2: APバージョンを確認

HEADERセクションの`FILE_SCHEMA`を見て、どのAPか確認:

```step
FILE_SCHEMA(('AP214_AUTOMOTIVE_DESIGN { ... }'));
```
→ このファイルはAP214

```step
FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF { ... }'));
```
→ このファイルはAP242

**なぜ重要？**
- APが違うと使えるエンティティが異なる
- パーサーはAPに応じたスキーマを読み込む必要がある

### ステップ3: PRODUCTエンティティを探す

DATAセクションで`PRODUCT(`を検索:
```step
#10 = PRODUCT('Part_A','Part_A','Simple part',(#20));
```

これが部品のトップレベル情報です。

**関連エンティティを辿る**:
```
PRODUCT (#10)
  ↓ (via PRODUCT_DEFINITION_FORMATION)
PRODUCT_DEFINITION (#50)
  ↓ (via PRODUCT_DEFINITION_SHAPE)
SHAPE_REPRESENTATION (#90)
  ↓
REPRESENTATION_ITEM (#100-#500)  ← ここに形状データ
```

詳細は [データモデル・マップ](../format/data-model-map.md) 参照。

### ステップ4: 形状データへの辿り方（概要）

実際の実装では:

**擬似コード（Python風）**:
```python
# 1. PRODUCTインスタンスを取得
product = find_entity(step_file, 'PRODUCT')

#選択 PRODUCT_DEFINITIONを辿る
product_def = traverse(product, 'PRODUCT_DEFINITION')

# 3. SHAPE_REPRESENTATIONを取得
shape_rep = traverse(product_def, 'SHAPE_REPRESENTATION')

# 4. 形状要素（FACE等）を取得
faces = filter_items(shape_rep.items, 'ADVANCED_FACE')
```

詳細な実装例は [データモデル・マップ](../format/data-model-map.md) に記載。

---

## 3. 推奨ツール

### STEPビューワー（無料）

| ツール | 特徴 | URL |
|--------|------|-----|
| **FreeCAD** | オープンソースCAD。STEP読み込み・編集可能 | https://www.freecad.org/ |
| **OpenCascade** | CADライブラリ。C++/Python | https://www.opencascade.com/ |
| **3D-Tool Free Viewer** | Windows用軽量ビューワー | https://www.3d-tool.com/ |

### バリデーター

- **STEP Tools** (有料): 商用の高機能バリデーター
- **CAx-IF推奨テストケース**: https://www.cax-if.org/

### パーサーライブラリ

| 言語 | ライブラリ/ツール |
|------|------------------|
| **Python** | `ifcopenshell` (IFC向けだが参考になる), `pythonOCC` (OpenCascade wrapper) |
| **C++** | OpenCascade, STEP Tools SDK |
| **JavaScript/TypeScript** | 自前実装が多い（Part 21パーサーは比較的シンプル） |

---

## 4. 次に読むべきドキュメント

STEPの基礎を理解したら、以下の順で学習を進めてください:

### ① まず理解を深める

1. **[用語集](./glossary.md)** - 重要用語トップ5を覚える
2. **[FAQ](./faq.md)** - よくある疑問を解消

### ② APを選択する

3. **[どのAPを使うべきか？](../decision-guides/which-ap-should-i-use.md)**
4. **[機能比較マトリックス](../comparison/capability-matrix.md)**

### ③ 実装に入る

5. **[STEPファイル完全解説](../examples/step-file-walkthrough.md)** - 実ファイルを1行ずつ理解
6. **[データモデル・マップ](../format/data-model-map.md)** - エンティティの階層構造
7. **[よくある落とし穴](../implementation/common-pitfalls.md)** - 実装時の注意点

---

## 💡 実装を始める前のチェックリスト

実装に着手する前に、以下を確認してください:

- [ ] STEPの基本構造（HEADER + DATA）を理解した
- [ ] エンティティ・インスタンス・参照の概念がわかった
- [ ] 自分のプロジェクトに適したAPを選択した
- [ ] Part 21形式の文法（基本的なパース方法）を理解した
- [ ] テストに使うサンプルSTEPファイルを入手した
- [ ] STEPビューワーで実際のファイルを開ける環境を用意した

---

## 📚 さらに学ぶために

### 公式リソース

- **ISO 10303規格書**: 正式な仕様（有料）
- **CAx-IF推奨プラクティス**: 実装ガイドライン（無料）

### コミュニティ

- **CAx-IF**: https://www.cax-if.org/
- **STEP modularization**: https://www.stepmod.org/

### おすすめの学習順序

```mermaid
graph LR
    A[Getting Started<br/>このページ] --> B[用語集]
    B --> C[FAQ]
    C --> D{何を実装?}
    D -->|パーサー| E[Data Model Map]
    D -->|エクスポーター| F[AP選択ガイド]
    E --> G[Walkthrough]
    F --> H[Common Pitfalls]
    G --> I[実装開始]
    H --> I
```

---

[READMEに戻る](../README.md)
