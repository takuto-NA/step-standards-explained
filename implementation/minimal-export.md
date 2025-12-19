# 最小限のエクスポート (Minimal Export)

STEPファイルを自作（実装）する場合、最初から全てのエンティティを揃える必要はありません。

## 1. 成功への最短ルート
1. **HEADERセクションの整備**: 正しいAP名を指定する。
2. **PRODUCT関係の最小構成**:
   - `PRODUCT`
   - `PRODUCT_DEFINITION`
   - `PRODUCT_DEFINITION_SHAPE`
3. **Geometryの基本**:
   - `CARTESIAN_POINT`
   - `DIRECTION`
   - `AXIS2_PLACEMENT_3D`

## 2. 形状確認のコツ
* `ADVANCED_BREP_SHAPE_REPRESENTATION` を使用するのが最も確実です。
* 最初は1つの `CLOSED_SHELL` から始める。

## 3. 検証ツール
* **NIST STEP File Analyzer**: 生成したファイルが規格に準拠しているか強力にチェックできます。

---
[READMEに戻る](../README.md)
