# PMI サポート状況 (PMI Support)

PMI (Product Manufacturing Information) のSTEPにおける扱いは、実装上の最も大きな課題の一つです。

## 1. PMIの種類

### Graphical PMI (Representation)
* 「人間が見るための線と文字」
* CAD上で見た目は正しいが、データとして「公差値」などは持っていない（単なる `POLYLINE` の集合）。

### Semantic PMI (Data)
* 「コンピュータが理解できる属性データ」
* 下流のCAMや計測ソフトが、公差タイプや数値を直接読み取れる。AP242の核心部分。

## 2. APごとのPMIサポート

| AP | Graphical | Semantic | 主要エンティティ |
| :--- | :---: | :---: | :--- |
| **AP203** | ❌ | ❌ | - |
| **AP214** | ✅ | ❌ | `DRAUGHTING_CALLOUT` |
| **AP242** | ✅ | ✅ | `GEOMETRIC_TOLERANCE`, `SHAPE_ASPECT` |

## 3. 実装の構造 (Semantic PMI)

AP242における公差情報の紐付け構造です。

```mermaid
graph TD
    Face[ADVANCED_FACE] -- "Linked by" --> SA[SHAPE_ASPECT]
    SA -- "Definition for" --> GT[GEOMETRIC_TOLERANCE]
    GT -- "Uses" --> DS[DIMENSIONAL_SIZE / LOCATION]
    GT -- "Refers to" --> DR[DATUM_REFERENCE]
```

## 4. 実装の壁
「AP242で出したのにPMIが消えた」原因のほとんどは、受信側CADの実装不足、または送信側が「グラフィカル」のみで出力していることにあります。セマンティック情報をやり取りするには、CAx-IF などの実装ガイドラインに厳密に従う必要があります。

---
[READMEに戻る](../README.md)
