# STEP規格 FAQ (Frequently Asked Questions)

STEP初心者・実装者がよく持つ疑問に答えます。**30+項目**を網羅。

---

## 📑 目次

1. [基本概念](#基本概念)
2. [ファイル操作](#ファイル操作)
3. [AP選択](#ap選択)
4. [実装](#実装)
5. [トラブルシューティング](#トラブルシューティング)
6. [ツールとリソース](#ツールとリソース)

---

## 基本概念

### Q1: STEPとは何ですか？

**A:** STEP (Standard for the Exchange of Product model data) は、3D CADデータを異なるCADシステム間で交換するための国際標準規格（ISO 10303）です。形状だけでなく、色・アセンブリ・PMI（寸法公差）なども保持できます。

---

### Q2: STEPとSTLの違いは？

**A:**

| | STEP | STL |
|---|---|---|
| **表現方法** | B-rep（数学的に正確な面） | 三角形メッシュ（近似） |
| **精度** | 理論上無限精度 | 近似（三角形サイズ依存） |
| **色・アセンブリ** | 対応 | 非対応 |
| **PMI** | 対応（AP242） | 非対応 |
| **ファイルサイズ** | 大きめ | 小さめ |
| **主な用途** | CAD間データ交換 | 3Dプリント |

**使い分け**: CAD間の正確なデータ交換にはSTEP、3Dプリントや可視化にはSTL。

---

### Q3: STEPとIGES/OBJの違いは？

**A:**

**IGES** (Initial Graphics Exchange Specification):
- STEPの前身
- 2D/3Dサポート
- 現在は非推奨（STEPに置き換わっている）

**OBJ**:
- シンプルな3Dメッシュフォーマット
- 色・テクスチャ対応
- CGや可視化向け（CADデータ交換には不向き）

→ **CADデータ交換には現代ではSTEP一択**

---

### Q4: Part 21とPart 28の違いは？

**A:**

**Part 21 (ISO 10303-21)**:
- ASCII形式（`.stp`, `.step`）
- 最も一般的
- 人間が読める

**Part 28 (ISO 10303-28)**:
- XML形式
- XML技術との親和性高い
- 冗長で大きい

**実務**: 99%がPart 21形式。Part 28はほとんど使われない。

---

### Q5: B-repとは何ですか？

**A:** **Boundary Representation**（境界表現）。3D形状を面・稜線・頂点の境界で定義する方式。STEPの主要な形状表現方法です。

**階層**:
```
Solid (ソリッド)
  └─ Shell (シェル)
      └─ Face (面)
          └─ Edge (稜線)
              └─ Vertex (頂点)
```

**メリット**: 数学的に正確、パラメトリック編集可能  
**デメリット**: 複雑、計算コスト高

---

## ファイル操作

### Q6: テキストエディタで開いても大丈夫？

**A:** **はい**。STEPファイルはプレーンテキストなので、メモ帳やVS Codeで開けます。

**注意点**:
- 大きなファイル（数十MB以上）は開くのに時間がかかる
- 編集には注意（文法エラーでファイルが壊れる）
- 実際の形状を見るにはSTEPビューワー使用

**推奨用途**: ヘッダー確認、エンティティ検索、デバッグ

---

### Q7: ファイルサイズが大きいのはなぜ？

**A:** STEPは以下の理由で大きくなりがちです:

1. **テキスト形式**: バイナリより冗長
2. **完全な形状記述**: 数学的に正確な面・曲線の定義
3. **管理情報**: プロダクト、アセンブリ、PMI等のメタデータ

**対策**:
- テセレーション（多角形近似）を使用（AP242）
- 圧縮（`.zip`や`.step.gz`）
- 不要な情報を削除

---

### Q8: バイナリ形式はありますか？

**A:** 公式には**ありません**。STEPは基本的にテキスト形式です。

ただし:
- 一部のCADベンダーが独自にバイナリ圧縮版を提供
- 標準ではないため互換性に問題

**実務**: Zip圧縮が一般的な対策

---

### Q9: エンコーディングは？

**A:** STEP Part 21の仕様では**ISO 8859-1**（Latin-1）が基本ですが、実際には:

- ASCII範囲内のみ使用が推奨
- 非ASCII文字は`\X2\...\X0\`エスケープシーケンスで表現（Unicode）

**実装上の注意**:
- UTF-8として読み込むと問題が起きる場合がある
- エスケープシーケンスの処理が必要

---

### Q10: どのくらいのファイルサイズが一般的？

**A:**

| 形状の複雑さ | ファイルサイズ目安 |
|---|---|
| シンプルな部品（立方体等） | 数KB〜数百KB |
| 一般的な部品 | 1MB〜10MB |
| 複雑なアセンブリ | 10MB〜100MB |
| 超大規模アセンブリ | 100MB〜数GB |

**巨大ファイルの扱い**:
- ストリーミングパーサーの使用
- 部分読み込み
- アセンブリの分割

---

## AP選択

### Q11: どのAPを使うべきですか？

**A:** 用途によります:

**PMI（寸法公差）が必要** → **AP242必須**  
**航空宇宙・防衛・MBD** → **AP242推奨**  
**自動車業界・色レイヤ重要** → **AP214** （ただしAP242移行が進行中）  
**単純な形状のみ・レガシーシステム** → **AP203**（ただし現在はAP214以降が一般的）

**迷ったら**: **AP242 ed2**が無難

詳細: [どのAPを使うべきか？](../decision-guides/which-ap-should-i-use.md)

---

### Q12: AP間の互換性は？

**A:**

**後方互換性**: 一般的にあり
- AP242 → AP214: PMIなどの情報が失われる
- AP214 → AP203: 色・レイヤが失われる

**前方互換性**: なし
- AP203データをAP214として読むのは問題ない（機能が増えるだけ）

**実務**: 送受信双方がサポートするAPのうち最新版を使用

---

### Q13: AP242 ed2とed3の違いは？

**A:**

**AP242 ed3 (ISO 10303-242:2022)** の主な追加機能:
- 電気ハーネス（Electrical Harness）強化
- 付加製造（Additive Manufacturing / 3Dプリント）対応
- MBSE（Model Based Systems Engineering）連携

**互換性**: ed2との高い互換性あり

**実装**: ed3対応CADは増加中だが、電気系・AM機能は普及途上

---

## 実装

### Q14: おすすめのパーサーライブラリは？

**A:**

| 言語 | ライブラリ | 特徴 |
|------|-----------|------|
| **C++** | OpenCascade | Commercial-grade, 多機能 |
| | STEP Tools SDK | 商用、高機能 |
| **Python** | pythonOCC | OpenCascadeのWrapper |
| | ifcopenshell | IFC向けだが参考になる |
| **JavaScript/TS** | 自前実装 | Part 21パーサーは比較的シンプル |
| **C#** | Xbim | IFC向けだが応用可能 |

**推奨**: C++で本格実装ならOpenCascade、軽量パーサーなら自前実装

---

### Q15: エンティティの辿り方は？

**A:** 基本パターン:

```python
# 1. PRODUCTを探す
product = find_entity_by_type(step_file, 'PRODUCT')

# 2. 参照を辿る
product_def_formation = traverse(product, 'PRODUCT_DEFINITION_FORMATION')
product_def = traverse(product_def_formation, 'PRODUCT_DEFINITION')

# 3. 形状データにアクセス
shape = traverse(product_def, 'PRODUCT_DEFINITION_SHAPE')
shape_rep = traverse(shape, 'SHAPE_REPRESENTATION')

# 4. 形状要素を取得
faces = filter_items(shape_rep.items, 'ADVANCED_FACE')
```

詳細: [データモデル・マップ](../format/data-model-map.md)

---

### Q16: 単位系の扱い方は？

**A:** STEPファイル内で`GEOMETRIC_REPRESENTATION_CONTEXT`に定義されています:

```step
#500 = ( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) );
```
→ `.MILLI.,.METRE.` = mm

**プレフィックス**:
- `.MILLI.` = 10^-3
- `.CENTI.` = 10^-2
- `.KILO.` = 10^3
- なし = 1

**実装**: 単位変換係数を事前計算してキャッシュ

詳細: [よくある落とし穴 - 単位](../implementation/common-pitfalls.md)

---

### Q17: 精度の扱い方は？

**A:** `UNCERTAINTY_MEASURE_WITH_UNIT`で定義:

```step
#600 = UNCERTAINTY_MEASURE_WITH_UNIT(1.0E-6,(#500),'distance_accuracy_value','...');
```
→ 精度は10^-6 mm

**実装上の注意**:
- 幾何演算時の許容誤差として使用
- 送受信側で精度が異なると「隙間」として認識される問題あり

---

## トラブルシューティング

### Q18: ファイルが壊れているか確認する方法は？

**A:**

**簡易チェック**:
1. HEADERとDATAセクションが存在するか
2. `ISO-10303-21;`で始まるか
3. `END-ISO-10303-21;`で終わるか
4. すべての`#番号`参照が解決できるか

**ツール**:
- **STEPバリデーター**: STEP Tools, CAx-IFツール
- **FreeCAD**: 開いてエラーが出ないか確認

**よくあるエラー**:
- 参照の不整合（#番号が存在しない）
- 文法エラー（括弧の不一致等）
- エンコーディング問題

---

### Q19: 色が消える原因は？

**A:** よくある原因:

1. **APの制限**: AP203には色情報がない → AP214以降必要
2. **スタイル定義の問題**: `STYLED_ITEM`が形状に直接紐付いていない
3. **色の定義層**: Shellに付いているかFaceに付いているかでCADの挙動が異なる

**対策**:
- AP214またはAP242を使用
- `STYLED_ITEM` → `PRESENTATION_STYLE_ASSIGNMENT` → `SURFACE_STYLE_RENDERING` → `COLOUR_RGB` のリンクを確認

---

### Q20: アセンブリ構造が崩れる原因は？

**A:**

1. **NAUO (NEXT_ASSEMBLY_USAGE_OCCURRENCE) の欠落**
2. **配置行列の不整合**: `CONTEXT_DEPENDENT_SHAPE_REPRESENTATION`の問題
3. **親子関係のリンク切れ**: `PRODUCT_DEFINITION`間の参照エラー

**デバッグ方法**:
- PRODUCTエンティティを全てリストアップ
- NAUOでの親子関係をツリー表示
- 配置行列の妥当性を確認（単位行列になっていないか等）

詳細: [よくある落とし穴 - アセンブリ](../implementation/common-pitfalls.md)

---

### Q21: PMIが読めない・消える原因は？

**A:**

1. **APの非対応**: Semantic PMIはAP242専用
2. **PMIの浮き（Dangling）**: `GEOMETRIC_TOLERANCE`が対象面（`SHAPE_ASPECT`）に紐付いていない
3. **CADの実装差**: PMIの解釈がCADごとに異なる

**対策**:
- AP242を使用
- CAx-IF推奨プラクティスに従う
- テストケースで検証

---

## ツールとリソース

### Q22: 無料のSTEPビューワーは？

**A:**

| ツール | プラットフォーム | 特徴 |
|--------|----------------|------|
| **FreeCAD** | Windows/Mac/Linux | オープンソース、編集可能 |
| **3D-Tool Free Viewer** | Windows | 軽量、高速 |
| **OpenCascade CAD Assistant** | Windows/Mac/Linux | OpenCascadeベース |

**オンライン**:
- 一部のWebサービス（品質は限定的）

---

### Q23: バリデーターはどこで入手できますか？

**A:**

**無料**:
- CAx-IF推奨プラクティスのチェッカー: https://www.cax-if.org/

**商用**:
- STEP Tools: 高機能バリデーター（有料）

**簡易チェック**:
- FreeCADで開いて警告・エラーを確認

---

### Q24: 公式ドキュメントはどこにありますか？

**A:**

**公式規格書** (有料):
- ISO 10303シリーズ: ISOまたは各国標準化機関から購入

**無料リソース**:
- **CAx-IF**: https://www.cax-if.org/ （推奨プラクティス）
- **STEP modularization**: https://www.stepmod.org/ （スキーマ参照）
- **WikiSTEP**: http://www.wikistep.org/

---

### Q25: CAx-IFとは？

**A:** **CAD-CAx Implementor Forum**: CADベンダー間でのSTEP実装ガイドラインを策定する国際的な団体。

**提供するもの**:
- 推奨プラクティス（Recommended Practices）
- テストケース
- ベンチマークファイル
- 相互運用性の検証結果

**実装者にとっての重要性**:
- CAx-IFガイドラインに従うことで相互運用性が大幅に向上
- 実装の「正解」を知る唯一の非公式標準

Website: https://www.cax-if.org/

---

### Q26: LOTARとは？

**A:** **Long Term Archiving and Retrieval**: STEPデータの長期保存・検索のための標準。

**目的**:
- 数十年後（30-50年）もデータを読めるようにする
- 航空宇宙・防衛産業で重要（部品のライフサイクルが長い）

**AP242との関係**: AP242がLOTARをサポート

---

### Q27: MBDとは？

**A:** **Model Based Definition**: 3Dモデルを唯一の正（Master）とし、そこにすべての設計・製造情報を集約する手法。

**従来との違い**:
- **従来**: 2D図面がマスター、3Dは参考
- **MBD**: 3Dモデルがマスター、2D図面は不要または従属

**STEPとの関係**: AP242のSemantic PMIがMBDを実現

---

### Q28: パーサーを自作すべきか、ライブラリを使うべきか？

**A:**

**自作を推奨する場合**:
- Part 21の基本パーサーのみ必要（比較的単純）
- 軽量・高速が必須
- ライセンスの制約

**ライブラリ推奨**:
- B-rep幾何演算が必要（NURBS処理等）
- 商用プロダクト（品質保証重要）
- 開発時間の短縮

**ハイブリッド**:
- Part 21パーサーは自作、幾何処理はOpenCascadeを使用

---

### Q29: STEPファイルをプログラマ的に生成するには？

**A:**

**方法1**: テキストとして生成
```python
with open('output.step', 'w') as f:
    f.write("ISO-10303-21;\n")
    f.write("HEADER;\n")
    # ... HEADERを書く
    f.write("DATA;\n")
    f.write(f"#10 = PRODUCT('{name}','{name}','',());\n")
    # ... DATAを書く
    f.write("END-ISO-10303-21;\n")
```

**方法2**: ライブラリ使用
- OpenCascade (C++)
- pythonOCC (Python)

**注意点**:
- エンティティの依存関係を正しく解決
- インスタンスIDの一意性を保証
- 単位系・精度を正しく設定

---

### Q30: STEPの学習に最適なサンプルファイルは？

**A:**

1. **CAx-IFテストケース**: https://www.cax-if.org/
   - 検証済みの標準サンプル

2. **STEP modularization**: https://www.stepmod.org/
   - EXPRESS スキーマと簡単な例

3. **自分で作成**:
   - FreeCADで simply な立方体を作成 → STEPエクスポート
   - テキストエディタで内容を確認

4. **このリポジトリ**:
   - [最小構成のSTEPファイル](../examples/minimal-product.step.md)
   - [STEPファイル完全解説](../examples/step-file-walkthrough.md)

---

## さらに質問がありますか？

まだ疑問が解決しない場合は:

1. **[用語集](./glossary.md)** で用語を確認
2. **[Getting Started](./getting-started.md)** で基礎を学ぶ
3. **[Data Model Map](../format/data-model-map.md)** でエンティティ構造を理解
4. **[Common Pitfalls](../implementation/common-pitfalls.md)** で実装の注意点を確認

---
## 📚 次のステップ
- **[どのAPを使うべきか？](../decision-guides/which-ap-should-i-use.md)** - プロジェクトに最適なAPを選択

[READMEに戻る](../README.md)
