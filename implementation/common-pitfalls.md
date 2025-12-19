# よくある落とし穴 (Common Pitfalls)

STEPの実装や変換でよく遭遇する問題と、その**対策・検出方法・実装例**を解説します。

---

## 📋 目次

1. [単位 (Units) の不一致](#1-単位-units-の不一致)
2. [精度 (Tolerance) の問題](#2-精度-tolerance-の問題)
3. [面の向きと整合性](#3-面の向きと整合性)
4. [アセンブリ構造の消失](#4-アセンブリ構造の消失)
5. [PMIの「浮き（Dangling）」](#5-pmiの浮きdangling)
6. [色やレイヤが消える](#6-色やレイヤが消える)
7. [エンコーディング問題](#7-エンコーディング問題)
8. [前方参照の処理ミス](#8-前方参照の処理ミス)

---

## 1. 単位 (Units) の不一致

**難易度**: ★★☆（中級）  
**頻度**: ★★★（非常によくある）  
**影響度**: 🔴 高（形状サイズが大きく変わる）

### ❌ 問題

- `SI_UNIT` と `CONVERSION_BASED_UNIT` (Inchなど) の変換ミス
- ファイル内に「長さはmm、角はRadian」といった定義が正しく書かれていない
- **実装者の盲点**: プレフィックス（kilo, milli）の解釈漏れ

**具体例**:
- mmのつもりがmで解釈→1000倍の巨大な形状
- Inchで作成したファイルをmmと誤認→40倍程度の誤差

### ✅ 対策

#### 1. 必ずUNIT_CONTEXTを確認

```step
#500 = ( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) );
#510 = ( PLANE_ANGLE_UNIT() NAMED_UNIT(*) SI_UNIT($,.RADIAN.) );
```

- `.MILLI.,.METRE.` = mm
- `.CENTI.,.METRE.` = cm
- なし（`$`）または`.METRE.` = m

#### 2. プレフィックスの変換表を実装

| PREFIX | 係数 | 例 |
|--------|------|---|
| `.PICO.` | 10^-12 | |
| `.NANO.` | 10^-9 | |
| `.MICRO.` | 10^-6 | μm |
| `.MILLI.` | 10^-3 | mm |
| `.CENTI.` | 10^-2 | cm |
| なし or `$` | 1 | m |
| `.KILO.` | 10^3 | km |

### 🔍 検出方法

**バリデーションコード（Python）**:

```python
def validate_and_get_unit_scale(step_file):
    """
    単位を取得し、mmへの変換係数を返す
    """
    # GEOMETRIC_REPRESENTATION_CONTEXTを探す
    contexts = find_all_by_type(step_file, 'GEOMETRIC_REPRESENTATION_CONTEXT')
    
    for ctx in contexts:
        units = ctx.units if hasattr(ctx, 'units') else []
        
        for unit in units:
            if 'LENGTH_UNIT' in str(unit.entity_types):
                # SI_UNITからプレフィックスを取得
                prefix = unit.prefix if hasattr(unit, 'prefix') else None
                
                # プレフィックスから係数を計算
                scale = get_si_prefix_scale(prefix)  # .MILLI. → 0.001
                
                return scale  # mへの係数（mmなら0.001）
    
    # デフォルト：mと仮定
    logger.warning("LENGTH_UNIT not found, assuming meters")
    return 1.0

def get_si_prefix_scale(prefix):
    """SI接頭辞から係数を取得"""
    prefix_map = {
        'PICO': 1e-12, 'NANO': 1e-9, 'MICRO': 1e-6,
        'MILLI': 1e-3, 'CENTI': 1e-2,
        'DECI': 1e-1,
        'DECA': 1e1, 'HECTO': 1e2, 'KILO': 1e3
    }
    if prefix is None or prefix == '$':
        return 1.0
    return prefix_map.get(prefix.upper().strip('.'), 1.0)
```

### 💡 実装時のベストプラクティス

- **単位変換係数を事前に計算してキャッシュ**
- すべての座標取得時に自動変換（内部はmmに統一など）
- 出力時は明示的に単位を指定（`SI_UNIT(.MILLI.,.METRE.)`）

---

## 2. 精度 (Tolerance) の問題

**難易度**: ★★☆（中級）  
**頻度**: ★★☆（よくある）  
**影響度**: 🟡 中（幾何演算で隙間が発生）

### ❌ 問題

`UNCERTAINTY_MEASURE_WITH_UNIT` の値が送信側と受信側で異なり、幾何演算の許容誤差が合わない。

**具体例**:
- 送信側: 精度 10^-6 mm
- 受信側: 精度 10^-2 mm で判定
- 結果: 「Faceに隙間がある」と誤って判定

### ✅ 対策

```step
#600 = UNCERTAINTY_MEASURE_WITH_UNIT(1.0E-6,(#500),'distance_accuracy_value','');
```
→ 精度は 10^-6 (mの単位系なら、mの10^-6 = 1 μm)

**推奨値**:
- mmベース: `1.0E-3` (0.001 mm = 1 μm)
- mベース: `1.0E-6` (1 μm)

### 🔍 検出方法

```python
def get_geometric_tolerance(step_file):
    """幾何精度を取得"""
    uncertainties = find_all_by_type(step_file, 'UNCERTAINTY_MEASURE_WITH_UNIT')
    
    for unc in uncertainties:
        if 'distance_accuracy' in unc.description.lower():
            value = unc.value_component
            unit = unc.unit_component
            
            # 単位変換を考慮
            scale = get_unit_scale(unit)
            tolerance_in_mm = value * scale * 1000  # mmに変換
            
            return tolerance_in_mm
    
    # デフォルト
    return 0.001  # 1 μm
```

### 💡 実装時のベストプラクティス

- 幾何演算ライブラリ（OpenCascade等）の許容誤差設定に使用
- エクスポート時は適切な精度値を必ず設定
- 精度が極端に大きい（1mm以上）場合は警告

---

## 3. 面の向きと整合性

**難易度**: ★★★（上級）  
**頻度**: ★★☆（よくある）  
**影響度**: 🔴 高（ソリッドが壊れる）

### ❌ 問題

`FACE_BOUND` と `ORIENTED_EDGE` の向き（方向フラグ `.T.` / `.F.`）が反転し、ソリッドが閉じていないと判定される。

**STEPでの面の定義**:
```step
#100 = ADVANCED_FACE('',(#110),#120,.T.);  ← .T. = 面の法線方向
#110 = FACE_OUTER_BOUND('',(#111,#112,#113,#114),.T.);
#111 = ORIENTED_EDGE('',*,*,#115,.F.);  ← .F. = エッジを逆向きに使用
```

### ✅ 対策

#### 1. 面の向き一貫性をチェック

```python
def validate_face_orientation(face):
    """
    ADVANCED_FACEの向き整合性を検証
    """
    face_orientation = face.same_sense  # .T. or .F.
    face_surface = face.face_geometry
    
    for bound in face.bounds:
        bound_orientation = bound.orientation
        
        for oriented_edge in bound.bound:
            edge_sense = oriented_edge.orientation
            
            # 向きの組み合わせが妥当かチェック
            # （詳細な幾何検証はOpenCascadeなどに委ねる）
            
    return True
```

#### 2. 法線ベクトルの確認

エッジループを辿って面積ベクトルを計算し、面の法線方向と一致するか確認。

### 🔍 検出方法

- **CADで開いてエラーが出ないか確認**
- OpenCascadeの`BRepCheck_Analyzer`を使用
- 自前実装する場合は Euler の多面体定理（V - E + F = 2）を確認

### 💡 実装時のベストプラクティス

- 面の向きは変更せず、CADからのエクスポート結果をそのまま使用
- エクスポート時にCADの「修復」機能を使用
- 受信側では向きを自動修正する機能を実装（OpenCascadeの`ShapeFix`など）

---

## 4. アセンブリ構造の消失

**難易度**: ★★★（上級）  
**頻度**: ★★☆（よくある）  
**影響度**: 🟡 中（構造が失われる）

### ❌ 問題

- `NEXT_ASSEMBLY_USAGE_OCCURRENCE` (NAUO) と配置行列の紐付けミス
- 親部品と子部品の `PRODUCT_DEFINITION` 間のリンクが途切れている
- 配置行列（`ITEM_DEFINED_TRANSFORMATION`）が単位行列になっている

### ✅ 対策

#### 1. NAUOの検証

```python
def validate_assembly_structure(step_file):
    """
    アセンブリ構造を検証
    """
    nauos = find_all_by_type(step_file, 'NEXT_ASSEMBLY_USAGE_OCCURRENCE')
    
    issues = []
    for nauo in nauos:
        # 親・子のPRODUCT_DEFINITIONが存在するか
        parent_pd = nauo.relating_product_definition
        child_pd = nauo.related_product_definition
        
        if parent_pd is None or child_pd is None:
            issues.append(f"NAUO {nauo.id}: Broken PD reference")
            continue
        
        # 配置行列の存在確認
        cdsrs = find_referencing(nauo, 'CONTEXT_DEPENDENT_SHAPE_REPRESENTATION')
        if not cdsrs:
            issues.append(f"NAUO {nauo.id}: No placement transform")
        
        # 配置行列が単位行列でないか確認
        for cdsr in cdsrs:
            transform = extract_transform_matrix(cdsr)
            if is_identity_matrix(transform):
                logger.warning(f"NAUO {nauo.id}: Identity transform (may be intentional)")
    
    return issues
```

#### 2. 配置行列の抽出

```python
def extract_transform_matrix(cdsr):
    """
    CONTEXT_DEPENDENT_SHAPE_REPRESENTATIONから4x4行列を抽出
    """
    rep_rel = cdsr.representation_relation
    
    if hasattr(rep_rel, 'transformation_operator'):
        item_transform = rep_rel.transformation_operator
        
        # AXIS2_PLACEMENT_3D から行列を構築
        origin = item_transform.location.coordinates  # (x, y, z)
        axis = item_transform.axis.direction_ratios if hasattr(item_transform, 'axis') else (0, 0, 1)
        ref_direction = item_transform.ref_direction.direction_ratios if hasattr(item_transform, 'ref_direction') else (1, 0, 0)
        
        # 4x4変換行列を構築（詳細は線形代数の知識が必要）
        matrix = build_transformation_matrix(origin, axis, ref_direction)
        return matrix
    
    return identity_matrix_4x4()
```

### 🔍 検出方法

- **ツリー表示**: PRODUCTエンティティをツリー表示し、親子関係を可視化
- **孤立検出**: NAUOで参照されていないPRODUCT_DEFINITIONを検出
- **配置確認**: すべての配置行列が単位行列でないか確認

### 💡 実装時のベストプラクティス

- **デフォルト値を設定**: 配置行列が見つからない場合は単位行列を使用
-  **循環参照チェック**: 親が子を参照し、子が親を参照する循環を検出
- **多重インスタンス対応**: 同じ子部品が複数回使用される場合に対応

---

## 5. PMIの「浮き（Dangling）」

**難易度**: ★★★（上級）  
**頻度**: ★☆☆（AP242のみ）  
**影響度**: 🟡 中（PMIが失われる）

### ❌ 問題

公差（`GEOMETRIC_TOLERANCE`）はあるが、対象の面（`SHAPE_ASPECT`）への参照が壊れている。

**原因**:
- AP242のPMIリンクは複雑で多重化
- CAD間での解釈の違い
- エクスポート時の不完全な実装

### ✅ 対策

```python
def validate_pmi_linkage(step_file):
    """
    PMIのリンク整合性を検証
    """
    tolerances = find_all_by_type(step_file, 'GEOMETRIC_TOLERANCE')
    
    for tol in tolerances:
        # 1. Shape Aspectへのリンクを確認
        shape_aspects = find_all_referencing(tol, 'SHAPE_ASPECT')
        
        if not shape_aspects:
            logger.warning(f"Tolerance {tol.id}: No SHAPE_ASPECT reference (dangling PMI)")
            continue
        
        # 2. Shape Aspectから幾何要素へのリンクを確認
        for sa in shape_aspects:
            if not hasattr(sa, 'of_shape') or sa.of_shape is None:
                logger.warning(f"SHAPE_ASPECT {sa.id}: No geometry reference")
```

### 🔍 検出方法

- すべての`GEOMETRIC_TOLERANCE`から`SHAPE_ASPECT`への参照をチェック
- `SHAPE_ASPECT`から実際の形状要素（FACE等）への参照をチェック

### 💡 実装時のベストプラクティス

- PMIの読み込みはオプション機能として実装（失敗しても形状は読める）
- CAx-IF推奨プラクティスに従う
- PMIが不完全な場合は警告を出して継続

---

## 6. 色やレイヤが消える

**難易度**: ★★☆（中級）  
**頻度**: ★★★（非常によくある）  
**影響度**: 🟢 低（見た目のみ）

### ❌ 問題

- 色情報の定義層が不適切（Shellに付いているか、Faceに付いているか）
- `PRESENTATION_STYLE_ASSIGNMENT` がジオメトリに直接紐付いていない
- APの制限（AP203には色情報なし）

### ✅ 対策

#### 1. APの確認

AP203では色・レイヤ非対応 → **AP214以降を使用**

#### 2. STYLED_ITEMの正しい作成

```step
# 正しい例: FACEに直接STYLED_ITEMを紐付け
#100 = ADVANCED_FACE(...);
#200 = STYLED_ITEM('',(#210),#100);  # itemがFACE
#210 = PRESENTATION_STYLE_ASSIGNMENT((#220));
#220 = SURFACE_STYLE_USAGE(.BOTH.,#230);
#230 = SURFACE_SIDE_STYLE('',(#240));
#240 = SURFACE_STYLE_RENDERING(#250,.MATTE.);
#250 = COLOUR_RGB('Red',1.0,0.0,0.0);
```

**間違った例**:
```step
# STYLED_ITEMがShellを参照（CADによっては無視される）
#100 = CLOSED_SHELL(...);
#200 = STYLED_ITEM('',(#210),#100);  # ← CADによっては認識しない
```

### 🔍 検出方法

```python
def validate_color_assignment(step_file):
    """
    色定義の妥当性を検証
    """
    styled_items = find_all_by_type(step_file, 'STYLED_ITEM')
    
    for si in styled_items:
        item = si.item
        
        # 色が付けられている対象をチェック
        if item.entity_type not in ['ADVANCED_FACE', 'MANIFOLD_SOLID_BREP', 'SHELL_BASED_SURFACE_MODEL']:
            logger.warning(f"STYLED_ITEM {si.id}: Attached to {item.entity_type} (may not be supported)")
        
        # COLOUR_RGBまで辿れるかチェック
        色 = extract_color_from_styled_item(si)
        if 色 is None:
            logger.warning(f"STYLED_ITEM {si.id}: No COLOUR_RGB found")
```

### 💡 実装時のベストプラクティス

- **FACEレベルに色を付ける**（最も互換性が高い）
- 色値は0.0〜1.0の範囲（0-255に変換: `int(value * 255)`）
- デフォルト色を設定（色がない場合はグレーなど）

---

## 7. エンコーディング問題

**難易度**: ★☆☆（初級）  
**頻度**: ★☆☆（たまにある）  
**影響度**: 🟡 中（文字化け）

### ❌ 問題

非ASCII文字（日本語、中国語など）の扱いが不適切。

**仕様**: STEP Part 21は基本的にISO 8859-1（Latin-1）、非ASCII文字は`\X2\...\X0\`エスケープ

### ✅ 対策

```step
# 正しい例: Unicodeエスケープ
#10 = PRODUCT('\X2\30D130FC30C8\X0\','Part A',...);
              ↑ Unicode hex (UTF-16BE)
# \X2\30D130FC30C8\X0\ = 「パート」（カタカナ）
```

**パーサー実装**:
```python
def decode_step_string(s):
    """
    STEPの文字列をデコード（\X2\...\X0\エスケープ処理）
    """
    import re
    
    def replace_unicode_escape(match):
        hex_str = match.group(1)
        # UTF-16BEとして解釈
        bytes_data = bytes.fromhex(hex_str)
        return bytes_data.decode('utf-16-be')
    
    # \X2\...\X0\ パターンを置換
    result = re.sub(r'\\X2\\([0-9A-F]+)\\X0\\', replace_unicode_escape, s)
    return result
```

### 🔍 検出方法

- ファイルに`\X2\`が含まれているか確認
- ASCII範囲外の文字（0x80以上）が直接含まれている場合は警告

### 💡 実装時のベストプラクティス

- 入力時: エスケープシーケンスを正しくデコード
- 出力時: 非ASCII文字は必ずエスケープ
- ファイル全体はASCIIとして読み込む（UTF-8ではない）

---

## 8. 前方参照の処理ミス

**難易度**: ★★☆（中級）  
**頻度**: ★★☆（よくある）  
**影響度**: 🔴 高（パースエラー）

### ❌ 問題

参照先（`#番号`）が、参照元より後に定義されている場合の処理ミス。

```step
#10 = PRODUCT(..., (#20, #30), ...);  ← #20, #30を参照
#20 = PRODUCT_CONTEXT(...);  ← #10より後に定義
#30 = APPLICATION_CONTEXT(...);
```

**パーサーの誤った実装**:
```python
# ❌ 間違い: 逐次処理
for line in step_file:
    inst = parse_instance(line)
    instance_map[inst.id] = inst
    # この時点で参照を解決 → #20がまだ存在しない！
    resolve_references(inst)  # エラー！
```

### ✅ 対策

**2パスパーサー**:
```python
# ✅ 正しい: 2パス処理
# Pass 1: すべてのインスタンスを読み込み
instance_map = {}
for line in step_file:
    inst = parse_instance(line)
    instance_map[inst.id] = inst  # 参照は未解決のまま

# Pass 2: すべての参照を解決
for inst in instance_map.values():
    resolve_references(inst, instance_map)
```

### 🔍 検出方法

- パース後に未解決参照がないか確認
- 存在しない`#番号`への参照を検出

```python
def validate_all_references(instance_map):
    """すべての参照が解決されているか確認"""
    for inst in instance_map.values():
        for ref in inst.get_all_references():
            if ref.target_id not in instance_map:
                logger.error(f"Instance {inst.id}: Reference to non-existent #{ref.target_id}")
```

### 💡 実装時のベストプラクティス

- **必ず2パス処理を実装**
- インスタンスIDの重複チェック
- 循環参照の検出（稀だが発生しうる）

---

## まとめ

「STEPは壊れやすい」のではなく、**「規格の厳密さに対して、CADベンダーの実装がルーズな部分で齟齬が起きている」**のが実態です。

**実装者へのアドバイス**:
1. **バリデーションを徹底**: 単位・精度・参照整合性を必ずチェック
2. **エラーハンドリング**: 不完全なデータでも可能な限り読み込む
3. **CAx-IF推奨プラクティスに従う**: 互換性が大幅に向上
4. **テストケースを活用**: CAx-IFのベンチマークファイルで検証

---

## 📚 次のステップ

- **[データモデル・マップ](../format/data-model-map.md)** - エンティティの階層構造を理解
- **[バリデーションとCAx-IF](./validation-and-caxif.md)** - 品質確保の方法
- **[FAQ](../docs/faq.md)** - よくある疑問

---

[READMEに戻る](../README.md)
