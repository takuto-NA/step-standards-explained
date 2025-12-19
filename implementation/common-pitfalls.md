# よくある落とし穴 (Common Pitfalls)

STEPの実装や変換でよく遭遇する問題とその対策です。

## 1. 単位 (Units) の不一致
* `SI_UNIT` と `CONVERSION_BASED_UNIT` (Inchなど) の変換ミス。
* ファイル内に「長さはmm、角はRadian」といった定義が正しく書かれていない。
* **実装者の盲点**: プレフィックス（kilo, milli）の解釈漏れ。

## 2. 精度 (Tolerance) の問題
* `UNCERTAINTY_MEASURE_WITH_UNIT` の値。
* 送信側が $10^{-3}$ mm の精度なのに、受信側が $10^{-2}$ mm で判定して「隙間がある」とみなされるケース。

## 3. 面の向きと整合性
* `FACE_BOUND` と `ORIENTED_EDGE` の向き（方向フラグ）が反転し、ソリッドが壊れる。

## 4. アセンブリ構造の消失
* `NEXT_ASSEMBLY_USAGE_OCCURRENCE` (NAUO) と配置行列の紐付けミス。
* 親部品と子部品の `PRODUCT_DEFINITION` 間のリンクが途切れている。

## 5. PMIの「浮き（Dangling）」
* 公差（`GEOMETRIC_TOLERANCE`）はあるが、対象の面（`SHAPE_ASPECT`）への参照が壊れている。
* 特にAP242 ed2等の複雑なスキーマでは、リンクが多重化しているため辿りきれないことがある。

## 6. 色やレイヤが消える
* 色情報の定義層が不適切（Shellに付いているか、Faceに付いているか）。
* `PRESENTATION_STYLE_ASSIGNMENT` がジオメトリに直接紐付いていない場合に、多くのCADで無視される。

---
## まとめ
「STEPは壊れやすい」のではなく、**「規格の厳密さに対して、CADベンダーの実装がルーズな部分で齟齬が起きている」**のが実態です。

---
[READMEに戻る](../README.md)
