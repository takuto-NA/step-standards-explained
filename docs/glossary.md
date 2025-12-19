# 用語集 (Glossary)

STEP規格（ISO 10303）でよく使われる用語の解説です。

## 基本用語

### AP (Application Protocol)
特定の業界や用途（自動車、航空宇宙、3D形状変換など）向けに定義された規格のサブセット。
- 例: AP203 (Configuration Controlled 3D Design), AP242 (Managed Model Based 3D Engineering)

### MIM (Mapped Interpreted Model)
実装者が実際に目にする、Express言語で記述されたデータモデル（STEPファイルの構成要素）。

### AIM (Application Interpreted Model)
AP間で共通化されたデータモデル。MIMの基盤となる。

### ARM (Application Reference Model)
ユーザー視点での情報モデル。業務要件を定義するためのもの。

## 形状・製品情報

### B-rep (Boundary Representation)
境界表現。面、稜線、頂点によって形状を定義する方式。STEPの得意分野。

### PMI (Product and Manufacturing Information)
製品製造情報。寸法、公差、表面粗さなどの「形状以外の設計意図」を指す。
- **Graphical PMI**: 人間が読むための注記（線や文字）。
- **Semantic PMI**: コンピュータが処理可能な意味を持った公差情報。

### MBD (Model Based Definition)
3Dモデルを唯一の正（Master）とし、そこにすべての設計・製造情報を集約する手法。

## ファイル構造

### Part 21 (ASCII / Clear Text)
拡張子 `.stp` や `.step` で知られる、最も一般的なテキスト形式のファイルフォーマット。

### Part 28 (XML)
STEPデータをXML形式で表現したもの。
