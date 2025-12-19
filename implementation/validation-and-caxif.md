# バリデーションとCAx-IF (Validation and CAx-IF)

STEPデータの品質を担保するための仕組みと、コミュニティによる活動についての解説です。

## 1. CAx-IF (Implementor Forum) とは
* 主要なCADベンダー（Autodesk, Dassault, Siemens, PTCなど）が参加し、STEPの実装バイブルである「推奨プラクティス（Recommended Practices）」を策定している国際グループです。
* **規格そのものよりも、この「推奨プラクティス」に従うことが、実務的な実装の成功には不可欠です。**

## 2. 幾何検証プロパティ (GVP: Geometric Validation Properties)
* 形状データが正しく伝達されたかを検証するための仕組みです。
* 体積、表面積、重心位置などの幾何情報をSTEPデータ内に埋め込み、受信側で再計算した値と比較することで、変換エラーを検出します。

## 3. 推奨リソース
* [CAx-IF Recommended Practices](https://www.cax-if.org/joint_testing_info.html) - 実装のガイドライン
* [MBx Interoperability Forum](https://www.mbx-if.org/) - 最新の相互運用性情報

---
## 📚 次のステップ
- **[最小限のエクスポート](./minimal-export.md)** - 実際にSTEPファイルを出力してみる

[READMEに戻る](../README.md)
