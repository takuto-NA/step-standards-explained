# STEPファイル形式対応マトリックス (Part 21 vs Part 28)

このドキュメントでは、主要CADソフトウェアのSTEP Part 21（ASCII）とPart 28（XML）の対応状況を整理します。

---

## 📊 CADソフトウェア対応状況

### メジャーCADソフトウェア

| CADソフトウェア | Part 21<br/>(.stp, .step) | Part 28<br/>(.stpx, .stpZ) | 備考 |
|----------------|---------------------------|---------------------------|------|
| **SolidWorks** | ✅ 完全対応 | ❌ 非対応 | Part 21のみ。AP203/214/242対応 |
| **CATIA V5/V6** | ✅ 完全対応 | ⚠️ 限定的 | Part 21が主。AP214/242対応。Part 28は明示的サポートなし |
| **Siemens NX** | ✅ 完全対応 | ✅ 対応 | .stpx, .stpZ(圧縮版)の読み書き対応 |
| **PTC Creo** | ✅ 完全対応 | ❌ 非対応 | Part 21のみ。AP203/214/242対応 |
| **Autodesk Inventor** | ✅ 完全対応 | ❌ 非対応 | Part 21のみ |
| **Fusion 360** | ✅ 完全対応 | ❌ 非対応 | Part 21のみ |
| **FreeCAD** | ✅ 完全対応 | ❌ 非対応 | OpenCascadeベース、Part 21のみ |
| **Rhino** | ✅ 完全対応 | ❌ 非対応 | Part 21のみ |

### 専用ツール・コンバーター

| ツール | Part 21 | Part 28 | 備考 |
|--------|---------|---------|------|
| **Kubotek Kosmos** | ✅ 対応 | ✅ 対応 | 2025年8月v7.1からPart 28対応開始 |
| **CAD Exchanger** | ✅ 対応 | ⚠️ 限定的 | Part 21が主 |
| **STEP Tools** | ✅ 対応 | ✅ 対応 | 商用ツール、両形式フルサポート |
| **OpenCascade** | ✅ 対応 | ❌ 非対応 | Part 21のみ（オープンソース） |

---

## 📈 Part 28 (STEP-XML) の現状

### 策定と歴史

- **初版発行**: 2007年（ISO 10303-28:2007）
- **最新版**: ISO 10303-28:2016
- **正式名称**: "ISO 10303-28: Industrial automation systems and integration — Product data representation and exchange — Part 28: Implementation methods: XML representations of EXPRESS schemas and data, using XML schemas"

### 特徴

**メリット**:
- XML技術との親和性（XSLT変換、XPath検索等）
- アセンブリレベルPMI対応
- UUID（Unique Universal ID）サポート
- Model-Based Enterprise (MBE) プロセスとの統合

**デメリット**:
- ファイルサイズが大きい（Part 21の2-3倍以上）
- CADソフトウェアの対応が遅れている
- Part 21に比べて普及していない

### 普及状況（2025年時点）

```
Part 21 (ASCII):  ████████████████████ 99%+
Part 28 (XML):    ██                    5%未満
```

**実務での使用例**:
- 🟢 **Part 21**: CAD間のデータ交換（最も一般的）
- 🟡 **Part 28**: 
  - 長期アーカイブ（LOTAR）
  - MBEプロセス統合
  - AI/LLMアプリケーション（新興）
  - 研究・学術用途

---

## 🎯 実装者への推奨

### ファイル形式の選択

**Part 21 (`.step`) を使うべき場合**:
- ✅ 一般的なCAD間データ交換
- ✅ 最大限の互換性が必要
- ✅ ファイルサイズを抑えたい
- ✅ 人間がテキストエディタで読みたい

**Part 28 (`.stpx`) を検討する場合**:
- ⚠️ XML処理ツールを活用したい
- ⚠️ 長期アーカイブが目的（LOTAR準拠）
- ⚠️ MBEプロセスとの統合
- ⚠️ 受信側がPart 28対応を明示している

> [!WARNING]
> **互換性の注意**
> 
> Part 28ファイルを送る前に、**必ず受信側のCADソフトが対応しているか確認**してください。非対応の場合、ファイルが開けない可能性があります。

### パーサー実装の優先順位

実装者がSTEPパーサーを自作する場合:

1. **Phase 1**: Part 21対応（必須）
   - 99%のファイルをカバー
   - 比較的シンプル

2. **Phase 2**: Part 28対応（オプショナル）
   - XML解析ライブラリを活用
   - 需要は限定的

---

## 🔍 Part 28 対応の確認方法

### CADソフトで確認

```
File → Import → STEP
```
で、ファイル形式選択ダイアログに `.stpx` が表示されるか確認。

### コマンドラインで確認

**NX (Siemens)**:
```bash
# NXはPart 28対応
ugopen -import file.stpx
```

**SolidWorks**:
```
# Part 28非対応のため、.stpxは開けない
# Part 21形式(.step)に変換が必要
```

---

## 📚 技術背景: Part 21 vs Part 28

### ファイル構造の違い

**Part 21 (ASCII)**:
```step
ISO-10303-21;
HEADER;
  FILE_DESCRIPTION(('Example'),'2;1');
  FILE_NAME(...);
  FILE_SCHEMA(('AP242...'));
ENDSEC;
DATA;
  #10=PRODUCT('Part_A',...);
  #20=PRODUCT_DEFINITION(...);
ENDSEC;
END-ISO-10303-21;
```

**Part 28 (XML)**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<iso_10303_28 xmlns="urn:oid:1.0.10303.28.2.1.1"
              version="1">
  <exp:iso_10303 xmlns:exp="..." schema="AP242">
    <product id="id1" name="Part_A">
      ...
    </product>
  </exp:iso_10303>
</iso_10303_28>
```

### ファイルサイズ比較（実例）

| ファイル | Part 21 | Part 28 | 比率 |
|---------|---------|---------|------|
| シンプルな立方体 | 5 KB | 15 KB | 3倍 |
| 中規模アセンブリ | 2 MB | 6 MB | 3倍 |
| 大規模製品 | 50 MB | 150 MB | 3倍 |

---

## 🌐 関連リソース

### 公式規格書

- **ISO 10303-21**: Clear text encoding（Part 21）
- **ISO 10303-28**: XML representations（Part 28）
- 購入先: ISO公式サイト、各国標準化機関

### 実装ガイド

- **CAx-IF**: https://www.cax-if.org/
- **PDES Inc.**: https://www.pdesinc.org/
- **Kubotek Kosmos STEP-XML解説**: https://kubotekkosmos.com/

### 対応ツール

- **Siemens NX**: 公式にPart 28サポート
- **Kubotek Kosmos**: 専用コンバーター（Part 28対応）
- **STEP Tools**: 商用ツール（両形式対応）

---

## ❓ FAQ

### Q: Part 28の方が新しいのに、なぜ普及していないのですか？

**A:** 主な理由:

1. **Part 21で十分**: ほとんどのCADデータ交換はPart 21で問題なくできる
2. **ファイルサイズ**: XMLは冗長でファイルが大きい
3. **CAD対応の遅れ**: メジャーCADがPart 28サポートを優先していない
4. **後方互換性**: Part 21の方が古いシステムとの互換性が高い

### Q: 将来的にPart 28が主流になりますか？

**A:** 短期的（5年程度）には**Part 21が主流のまま**と予想されます。

**長期的には**: MBE/AI活用の普及次第で、Part 28の利用が増える可能性はありますが、Part 21が完全に置き換わることはないでしょう。

### Q: Part 21とPart 28は相互変換できますか？

**A:** はい、可能です。

- **Part 21 → Part 28**: 比較的容易（データ構造は同じ）
- **Part 28 → Part 21**: 可能（XML→ASCII変換）

**変換ツール**:
- STEP Tools (商用)
- Kubotek Kosmos (商用)
- カスタムスクリプト（EXPRESS schemaベース）

---

## 📝 まとめ

**実装者へのアドバイス**:

1. **まずPart 21対応を優先**
   - 99%のユースケースをカバー
   - 全てのメジャーCADが対応

2. **Part 28は特定用途のみ**
   - 長期アーカイブ
   - MBE統合
   - 受信側が明示的に対応している場合のみ

3. **迷ったらPart 21**
   - 互換性・ファイルサイズ・対応ツールの豊富さで優位

---

**最終更新**: 2025-12-19  
**情報源**: CADベンダー公式ドキュメント、CAx-IF、ウェブ調査

---
## 📚 次のステップ
- **[アセンブリ構造の解説](./assembly-support.md)** - 複数の部品からなる構造の定義

[READMEに戻る](../README.md)
