# EXPRESS言語の概要 (EXPRESS Overview)

STEPのデータモデルは、**EXPRESS** (ISO 10303-11) という情報モデリング言語で定義されています。

## 1. EXPRESSとは
* オブジェクト指向に近い特徴を持つデータ定義言語。
* エンティティ（Entity）、型（Type）、関数（Function）、制約（Rule）を定義する。
* STEP AP（例：AP214）は、このEXPRESSで書かれた巨大なスキーマです。

## 2. スキーマの読み方
```express
ENTITY product;
  id : identifier;
  name : label;
  description : OPTIONAL text;
  frame_of_reference : SET [1:?] OF product_context;
END_ENTITY;
```
* `ENTITY`: クラスのようなもの。
* `id`, `name`: 属性。
* `OPTIONAL`: データがなくても良い。
* `SET [1:?]`: 1つ以上の重複しないリスト。

## 3. 実装者が知っておくべきこと
実装時、規格書の「どの属性が必須か」「どの型に変換可能か」はこのEXPRESS定義に基づいています。

---
## 📚 次のステップ
- **[よくある落とし穴](../implementation/common-pitfalls.md)** - 実装時に遭遇しやすい問題と対策

[READMEに戻る](../README.md)
