# プロダクト・エンティティの解剖図 (Anatomy of Product Entities)

STEPファイル（Part 21）でプロダクト情報を正しく定義するための、属性レベルの解説です。

## 1. PRODUCT
部品やアセンブリそのものを定義するトップレベルの要素。

```express
ENTITY product;
  id : identifier;              -- 1. 部品番号 (Part Number)
  name : label;                 -- 2. 表示名
  description : OPTIONAL text;  -- 3. 説明（任意）
  frame_of_reference : SET [1:?] OF product_context; -- 4. 設計コンテキスト
END_ENTITY;
```

- **id**: 実装上、一意である必要があります。
- **frame_of_reference**: 通常は機械設計を表す `'mechanical'` 等を含む `product_context` を参照します。

## 2. PRODUCT_DEFINITION_FORMATION
プロダクトの「バージョン」や「リビジョン」を管理します。

```express
ENTITY product_definition_formation;
  id : identifier;              -- 1. リビジョン番号 (e.g. 'A', '1')
  description : OPTIONAL text;  -- 2. 説明
  of_product : product;         -- 3. 対象のPRODUCT
END_ENTITY;
```

## 3. PRODUCT_DEFINITION
特定の用途（設計、解析など）におけるプロダクトの定義。ここが形状データとの紐付けの起点となります。

```express
ENTITY product_definition;
  id : identifier;              -- 1. 定義ID (e.g. 'design')
  description : OPTIONAL text;  -- 2. 説明
  formation : product_definition_formation; -- 3. 対象のFORMATION
  frame_of_reference : product_definition_context; -- 4. ライフサイクル等のコンテキスト
END_ENTITY;
```

## 実装のアドバイス
- **必須属性の重複**: P21ファイル内では、複数のエンティティが同じ `id` を持つことがありますが、その意味はエンティティによって異なります。
- **Contextの使い回し**: `#1=PRODUCT_CONTEXT(...)` のように定義したコンテキストを、複数の `PRODUCT` から参照するのが標準的な書き方です。

---
## 📚 次のステップ
- **[データモデル・マップ](./data-model-map.md)** - 各エンティティがどのように繋がるかを確認する

[READMEに戻る](../README.md)
| [データモデル・マップに戻る](./data-model-map.md)
