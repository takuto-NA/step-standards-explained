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

## 2. 最小構成テンプレート (AP242)
これをベースに、必要に応じて幾何要素を追加してください。
[実ファイル (minimal_part.step)](../examples/minimal_part.step) も参考にしてください。

```step
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Minimal Export Template'),'21;1');
FILE_NAME('export.step','2025-12-19T10:00:00',('Author'),('Organization'),'Processor','System','');
FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF { 1 0 10303 442 1 1 4 }'));
ENDSEC;
DATA;
#10 = PRODUCT('PART_ID','PART_NAME','',(#20));
#20 = PRODUCT_CONTEXT('',#30,'mechanical');
#30 = APPLICATION_CONTEXT('managed model based 3d engineering');
#40 = PRODUCT_DEFINITION_FORMATION('1','',#10);
#50 = PRODUCT_DEFINITION('design','',#40,#60);
#60 = PRODUCT_DEFINITION_CONTEXT('part definition',#30,'design');
#70 = PRODUCT_DEFINITION_SHAPE('','',#50);
#80 = SHAPE_DEFINITION_REPRESENTATION(#70,#90);
#90 = SHAPE_REPRESENTATION('',(#100),#110);
#100 = AXIS2_PLACEMENT_3D('',#120,#130,#140);
#110 = ( GEOMETRIC_REPRESENTATION_CONTEXT(3) 
         GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#150))
         GLOBAL_UNIT_ASSIGNED_CONTEXT((#160,#170,#180))
         REPRESENTATION_CONTEXT('Context #1','3D Context') );
#120 = CARTESIAN_POINT('',(0.0,0.0,0.0));
#130 = DIRECTION('',(0.0,0.0,1.0));
#140 = DIRECTION('',(1.0,0.0,0.0));
#150 = UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.0E-06),#160,'DISTANCE_ACCURACY_VALUE','');
#160 = ( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) );
#170 = ( NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.) );
#180 = ( NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT() );
ENDSEC;
END-ISO-10303-21;
```

## 3. 実装チェックリスト
- [ ] **インスタンスIDの一貫性**: `#番号`が重複していないか。
- [ ] **HEADERのAP名**: `FILE_SCHEMA` の記述が正しいか（AP214とAP242を間違えていないか）。
- [ ] **単位系 (SI_UNIT)**: `.MILLI.,.METRE.` (mm) か `.METRE.` (m) かを明示しているか。
- [ ] **閉じているか**: `ENDSEC;` や `END-ISO-10303-21;` が抜けていないか。

## 4. 形状確認のコツ
* `ADVANCED_BREP_SHAPE_REPRESENTATION` を使用するのが最も確実です。
* 最初は1つの `CLOSED_SHELL` から始める。

## 5. 検証ツール
* **NIST STEP File Analyzer**: 生成したファイルが規格に準拠しているか強力にチェックできます。
* **CAx-IF Checkers**: 相互運用性の観点からチェック。

---
## 📚 次のステップ
- **[よくある落とし穴](./common-pitfalls.md)** - 実装時にハマりやすいポイント

[READMEに戻る](../README.md)
