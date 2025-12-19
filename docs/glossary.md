# 用語集 (Glossary)

> [!IMPORTANT]
> **このページを最初に読むことを強く推奨します**
> 
> STEP規格の理解は専門用語の理解から始まります。以下の「最重要用語トップ5」を押さえることで、他のドキュメントの理解が格段に容易になります。

---

## ⭐ 最重要用語トップ5（まずはこれだけ覚える）

実装者が最初に理解すべき5つの核心概念です。

### 1. AP (Application Protocol) ★★★

特定の業界や用途向けに定義された規格のサブセット。

**実装者が知るべきこと**:
- AP203, AP214, AP242がメジャーバージョン
- APが違うと使えるエンティティ（データ構造）が異なる
- ファイルのHEADERセクションの`FILE_SCHEMA`で確認可能

**STEPファイル内での例**:
```step
FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF { 1 0 10303 442 1 1 4 }'));
```
→ このファイルはAP242を使用

**関連用語**: [MIM](#mim-mapped-interpreted-model), [AIM](#aim-application-interpreted-model)

---

### 2. Entity (エンティティ) ★★★

STEPデータの構成要素。オブジェクト指向プログラミングの「クラス」に相当。

**実装者が知るべきこと**:
- すべて**大文字**で表記（例: `PRODUCT`, `SHAPE_REPRESENTATION`）
- 属性（Attribute）を持つ
- 継承関係がある（SUPERTYPE/SUBTYPE）

**STEPファイル内での例**:
```step
#10 = PRODUCT('Part_A','Part_A','description',(#20));
```
- `PRODUCT` がエンティティ名
- `#10` がインスタンスID（このファイル内でのユニークな識別子）
- 括弧内が属性値

**パーサー実装時の注意**:
- エンティティ名は大文字小文字を区別しない（仕様上）が、通常は大文字で統一
- `#番号`での参照を正しく解決する必要がある

**関連用語**: [EXPRESS](#express), [Instance](#instance-インスタンス)

---

### 3. B-rep (Boundary Representation) ★★★

**境界表現**。面・稜線・頂点によって形状を定義する方式。

**STLとの違い**:
| | B-rep (STEP) | STL |
|---|---|---|
| 表現方法 | 数学的に正確な面（NURBS等） | 三角形メッシュ（近似） |
| 精度 | 理論上無限精度 | 近似精度（三角形サイズ依存） |
| ファイルサイズ | 中〜大 | 小〜中 |
| 編集可能性 | パラメトリック編集可能 | 困難 |

**STEPでのB-rep階層**:
```
MANIFOLD_SOLID_BREP
  └─ CLOSED_SHELL
      └─ ADVANCED_FACE (面)
          └─ EDGE_LOOP (稜線ループ)
              └─ ORIENTED_EDGE (方向付き稜線)
                  └─ VERTEX_POINT (頂点)
```

**関連用語**: [NURBS](#nurbs), [Tessellation](#tessellation-テセレーション)

---

### 4. PMI (Product and Manufacturing Information) ★★

製品製造情報。寸法、公差、表面粗さなどの「形状以外の設計意図」。

**2種類のPMI**:

**Graphical PMI（表示型）**:
- 人間が読むための注記（見た目の線や文字）
- 3Dビューワーで表示可能
- コンピュータが意味を解釈できない

**Semantic PMI（意味型）**:
- コンピュータが処理可能な意味情報
- `GEOMETRIC_TOLERANCE`等のエンティティで表現
- AP242でフルサポート

**実装者にとっての重要性**:
- PMIの有無でAPの選択が変わる（PMI必要 → AP242必須）
- Semantic PMIの解析には幾何公差の知識が必要
- CAD間でのPMI互換性は完全ではない（CAx-IFガイドライン参照）

**関連用語**: [GD&T](#gdt-geometric-dimensioning-and-tolerancing), [MBD](#mbd-model-based-definition)

---

### 5. EXPRESS ★★

STEPのデータモデルを定義する言語（ISO 10303-11）。

**実装者が知るべきこと**:
- 各APの「スキーマ」はEXPRESSで記述されている
- ENTITYの定義、属性の型、制約などを確認できる
- 実装時は規格書のEXPRESSスキーマを参照

**EXPRESSの例**:
```express
ENTITY product;
  id : identifier;
  name : label;
  description : OPTIONAL text;
  frame_of_reference : SET [1:?] OF product_context;
END_ENTITY;
```
- `OPTIONAL`: この属性は省略可能
- `SET [1:?]`: 1個以上の重複なし集合

**プログラミング言語との対応**:
| EXPRESS | Java/C++ | Python | 意味 |
|---------|----------|--------|------|
| `ENTITY` | `class` | `class` | クラス定義 |
| `TYPE` | `typedef` | `NewType` | 型エイリアス |
| `OPTIONAL` | `Optional<T>` | `Optional[T]` | null許容 |
| `SET [1:?]` | `Set<T>` | `set` | 重複なし集合 |
| `LIST [0:?]` | `List<T>` | `list` | 順序付きリスト |

**関連用語**: [Entity](#2-entity-エンティティ-), [Schema](#schema-スキーマ)

---

## 📂 カテゴリ別用語集

### ファイル構造関連

#### Part 21 (ASCII / Clear Text)
拡張子 `.stp` や `.step` で知られる、最も一般的なテキスト形式のファイルフォーマット（ISO 10303-21）。

**構造**:
```step
ISO-10303-21;
HEADER;
  FILE_DESCRIPTION(...);
  FILE_NAME(...);
  FILE_SCHEMA(...);
ENDSEC;
DATA;
  #10 = PRODUCT(...);
  #20 = ...;
ENDSEC;
END-ISO-10303-21;
```

#### Part 28 (XML)
STEPデータをXML形式で表現したもの。Part 21より冗長だが、XML技術との親和性が高い。

#### Instance (インスタンス)
エンティティの具体的な値を持つデータ。`#10 = PRODUCT(...)`の`#10`がインスタンス識別子。

**実装上の注意**:
- インスタンスIDは1から始まり、ファイル内でユニーク
- 前方参照（後で定義されるインスタンスへの参照）が可能

---

### 形状・幾何関連

#### NURBS (Non-Uniform Rational B-Spline)
非一様有理Bスプライン。複雑な曲線・曲面を数学的に表現する方法。STEPのB-repで多用。

#### Tessellation (テセレーション)
曲面を三角形や四角形のポリゴンで近似表現すること。AP242で標準化。

**用途**:
- 高速な表示（ポリゴンは描画が軽い）
- ファイルサイズ削減（B-repとテセレーションを併用）

#### ADVANCED_FACE
STEPで面を表現する最も一般的なエンティティ。面の境界（EDGEのループ）と表面形状（SURFACE）を定義。

---

### 管理データ関連

#### PRODUCT
部品そのものを表すトップレベルエンティティ。

**属性**:
- `id`: 部品ID（文字列）
- `name`: 部品名
- `description`: 説明（オプション）
- `frame_of_reference`: コンテキスト

#### PRODUCT_DEFINITION
設計、解析、製造などのコンテキストにおける製品の定義。形状データはこのエンティティに紐付く。

#### PRODUCT_DEFINITION_SHAPE
管理データと形状データの「橋渡し」役。`PRODUCT_DEFINITION`と`SHAPE_REPRESENTATION`を結びつける。

---

### PMI・公差関連

#### GD&T (Geometric Dimensioning and Tolerancing)
幾何寸法公差。部品の形状・位置・姿勢に関する許容範囲を定義する体系。

**主な公差タイプ**:
- 平面度、真直度、真円度（形状公差）
- 位置度、同軸度、対称度（位置公差）
- 平行度、直角度、傾斜度（姿勢公差）

#### GEOMETRIC_TOLERANCE
STEPでGD&Tを表現するエンティティの基底型。`POSITION_TOLERANCE`、`FLATNESS_TOLERANCE`等のサブタイプがある。

#### DATUM (データム)
公差の基準となる理論的に正確な面・線・点。

---

### AP・スキーマ関連

#### MIM (Mapped Interpreted Model)
実装者が実際に目にする、Express言語で記述されたデータモデル（STEPファイルの構成要素）。

#### AIM (Application Interpreted Model)
AP間で共通化されたデータモデル。MIMの基盤となる。

#### ARM (Application Reference Model)
ユーザー視点での情報モデル。業務要件を定義するためのもの。MIMに変換（マッピング）される。

#### Schema (スキーマ)
EXPRESSで記述されたデータモデルの定義全体。各APは独自のスキーマを持つ。

---

### MBD・デジタルスレッド関連

#### MBD (Model Based Definition)
3Dモデルを唯一の正（Master）とし、そこにすべての設計・製造情報を集約する手法。

**従来との違い**:
- 従来: 2D図面がマスター、3Dは参考
- MBD: 3Dモデルがマスター、2D図面は不要または従属

#### LOTAR (Long Term Archiving and Retrieval)
STEPデータの長期保存・検索のための標準。AP242で対応。

**目的**:
- 数十年後もデータを読めるようにする
- 航空宇宙・防衛産業で重要

#### CAx-IF (CAD-CAx Implementor Forum)
CADベンダー間でのSTEP実装ガイドラインを策定する団体。

**実装者にとっての重要性**:
- CAx-IFの推奨プラクティスに従うことで相互運用性向上
- テストケースとベンチマークファイルを提供

---

## 🔗 関連リソース

- **公式規格書**: ISO 10303シリーズ（有料）
- **CAx-IF推奨プラクティス**: https://www.cax-if.org/
- **EXPRESSスキーマ**: 各AP規格書の付録に記載

---
## 📚 次のステップ
- **[スタートガイド](./getting-started.md)** - STEPの全体像を把握

[READMEに戻る](../README.md)
