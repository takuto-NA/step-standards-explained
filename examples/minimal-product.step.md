# 最小構成のSTEPファイル解析 (Minimal STEP Analysis)

実ファイル (.stp) を読み解くためのガイドです。ここでは「1つの部品」を定義する最小構成を分解します。
実際のファイルはこちらからダウンロードできます: **[minimal_part.step](./minimal_part.step)**

## 1. ヘッダー部分 (Header)
```step
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('STEP AP242 ed2'),'21;1');
FILE_NAME('minimal_part.stp','2023-10-27T10:00:00',('Author Name'),('Company'),'Processor Name','CAD Version','');
FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF { 1 0 10303 442 1 1 4 }'));
ENDSEC;
```
- **FILE_SCHEMA**: このファイルがどのAP（規格）に従っているかを定義します。

## 2. データセクション：管理データ (Admin Data)
```step
DATA;
#10 = PRODUCT('Part_A','Part_A','Part_A description',(#20));
#20 = PRODUCT_CONTEXT('',#30,'design');
#30 = APPLICATION_CONTEXT('managed model based 3d engineering');
#40 = PRODUCT_DEFINITION_FORMATION('1','first version',#10);
#50 = PRODUCT_DEFINITION('design','',#40,#60);
#60 = PRODUCT_DEFINITION_CONTEXT('part definition',#30,'design');
```
- **#10**: 「部品」そのもの。
- **#50**: 部品の「設計状態（Definition）」を定義。形状データはここにぶら下がります。

## 3. データセクション：形状へのリンク (Shape Header)
```step
#70 = PRODUCT_DEFINITION_SHAPE('','',#50);
#80 = SHAPE_DEFINITION_REPRESENTATION(#70,#90);
#90 = SHAPE_REPRESENTATION('',(#100),#110);
```
- **#70**: 管理データと形状データの「結節点」。
- **#90**: 形状の「カタログ」のような役割。

## 4. データセクション：ジオメトリ (Geometry)
```step
#100 = ADVANCED_FACE('',(#120),#130,.T.);
#110 = ( GEOMETRIC_REPRESENTATION_CONTEXT(3) 
         GLOBAL_UNCERTAINTY_ASSIGNMENT((#140))
         GLOBAL_UNIT_ASSIGNMENT((#150,#160,#170))
         REPRESENTATION_CONTEXT('Context #1','3D Context') );
```
- **#100**: 面 (Face)。ここから Surface, Edge, Vertex へと詳細化されます。
- **#110**: 単位系(Unit)や精度(Uncertainty)を定義する重要なコンテキスト。

---
## 実装へのヒント
ファイルを読む際は、まず `PRODUCT_DEFINITION` (#50) を探し、そこから `PRODUCT_DEFINITION_SHAPE` (#70) -> `SHAPE_REPRESENTATION` (#90) と辿ることで、その部品の「メインの形状」を特定できます。
