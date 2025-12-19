# STEPファイルの基本構造 (STEP File Basics)

STEPファイル（*.stp, *.step）は、ISO 10303-21 で規定されたプレーンテキスト形式です。

## 1. ファイル構成
ファイルは大きく3つのセクションに分かれます。

```text
ISO-10303-21;
HEADER;
  /* ファイル名、作成者、APの定義など */
  FILE_NAME(...);
  FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));
ENDSEC;

DATA;
  /* 実データの実体（エンティティ） */
  #10=PRODUCT('Part1','Part1','',(#20));
  #20=PRODUCT_CONTEXT('',#30,'');
  ...
ENDSEC;

END-ISO-10303-21;
```

## 2. なぜ行番号 (#10, #20...) が重要か
* STEPは**ポインタ（参照）型**の構造をしています。
* あるエンティティが別のエンティティを引用する際、この番号を使用します。
* 注意: この番号はファイル内で一意であればよく、意味（ID）は持ちません。ファイルを保存し直すと番号が変わるのが普通です。

---
## 📚 次のステップ
- **[データモデル・マップ](./data-model-map.md)** - エンティティの階層構造を把握する

[READMEに戻る](../README.md)
