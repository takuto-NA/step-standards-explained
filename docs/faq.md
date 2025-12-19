# STEP Standard FAQ (Frequently Asked Questions)

Answers to common questions from STEP beginners and implementers, covering **30+ items**.

---

## 📑 Table of Contents

1. [Basic Concepts](#basic-concepts)
2. [File Operations](#file-operations)
3. [AP Selection](#ap-selection)
4. [Persistence and Simulation (IDs/Names)](#persistence-and-simulation-idsnames)
5. [Implementation](#implementation)
6. [Troubleshooting](#troubleshooting)
7. [Tools and Resources](#tools-and-resources)

---

## Basic Concepts

### Q1: What is STEP?

**A:** STEP (Standard for the Exchange of Product model data) is an international standard (ISO 10303) for exchanging 3D CAD data between different CAD systems. It can store not only geometry but also colors, assemblies, and PMI (Product and Manufacturing Information/tolerances).

---

### Q2: What is the difference between STEP and STL?

**A:**

| | STEP | STL |
|---|---|---|
| **Representation** | B-rep (Mathematically precise surfaces) | Triangular mesh (approximate) |
| **Precision** | Theoretically infinite | Approximate (mesh size dependent) |
| **Colors/Assemblies** | Supported | Not Supported |
| **PMI** | Supported (AP242) | Not Supported |
| **File Size** | Larger | Smaller |
| **Primary Use** | CAD data exchange | 3D printing |

**Guideline**: Use STEP for precise data exchange between CAD systems; use STL for 3D printing or visualization.

---

### Q3: What is the difference between STEP and IGES/OBJ?

**A:**

**IGES** (Initial Graphics Exchange Specification):
- Predecessor to STEP.
- Supports 2D/3D.
- Now deprecated (replaced by STEP).

**OBJ**:
- Simple 3D mesh format.
- Supports colors/textures.
- For CG and visualization (not suitable for CAD data exchange).

→ **For modern CAD data exchange, STEP is the standard choice.**

---

### Q4: What is the difference between Part 21 and Part 28?

**A:**

**Part 21 (ISO 10303-21)**:
- ASCII format (`.stp`, `.step`).
- Most common.
- Human-readable.

**Part 28 (ISO 10303-28)**:
- XML format.
- High affinity with XML technologies.
- Redundant and large.

**In Practice**: 99% of files use Part 21. Part 28 is rarely used.

---

### Q5: What is B-rep?

**A:** **Boundary Representation**. A method for defining 3D shapes by their boundaries: faces, edges, and vertices. It is the primary geometry representation in STEP.

**Hierarchy**:
```
Solid
  └─ Shell
      └─ Face
          └─ Edge
              └─ Vertex
```

**Pros**: Mathematically precise, parametrically editable.  
**Cons**: Complex, high computational cost.

---

## File Operations

### Q6: Is it okay to open it in a text editor?

**A:** **Yes**. Since STEP files are plain text, you can open them with Notepad or VS Code.

**Considerations**:
- Large files (tens of MBs+) take time to open.
- Be careful when editing (syntax errors can corrupt the file).
- Use a STEP viewer to view the actual geometry.

**Recommended uses**: Header inspection, entity searching, debugging.

---

### Q7: Why are the file sizes so large?

**A:** STEP tends to be large due to:

1. **Text Format**: More redundant than binary.
2. **Complete Geometry Description**: Mathematically precise surfaces and curves.
3. **Management Data**: Metadata for products, assemblies, PMI, etc.

**Mitigation**:
- Use tessellation (polygonal approximation) (AP242).
- Compression (`.zip` or `.step.gz`).
- Remove unnecessary information.

---

### Q8: Is there a binary format?

**A:** Officially, **no**. STEP is fundamentally a text format.

However:
- Some CAD vendors offer proprietary binary compression versions.
- Not standard, leading to compatibility issues.

**In Practice**: Zip compression is the standard mitigation.

---

### Q9: What is the encoding?

**A:** The STEP Part 21 specification is based on **ISO 8859-1** (Latin-1), but in practice:

- It is recommended to stay within the ASCII range.
- Non-ASCII characters are represented using `\X2\...\X0\` escape sequences (Unicode).

**Implementation Note**:
- Reading as UTF-8 may cause issues.
- Handling of escape sequences is necessary.

---

### Q10: What is a typical file size?

**A:**

| Geometry Complexity | Estimated File Size |
|---|---|
| Simple Part (cube, etc.) | A few KB to hundreds of KB |
| Typical Part | 1MB to 10MB |
| Complex Assembly | 10MB to 100MB |
| Ultra-Large Assembly | 100MB to several GB |

**Handling Large Files**:
- Use streaming parsers.
- Use partial loading.
- Split assemblies.

---

## AP Selection

### Q11: Which AP should I use?

**A:** It depends on your use case:

**Need PMI (Tolerances)** → **AP242 is mandatory.**  
**Aerospace/Defense/MBD** → **AP242 is recommended.**  
**Automotive/Need Colors & Layers** → **AP214** (though migration to AP242 is ongoing).  
**Simple Geometry only/Legacy Systems** → **AP203** (though AP214+ is more common now).

**If in doubt**: **AP242 ed2** is a safe choice.

Detail: [Which AP should I use?](../decision-guides/which-ap-should-i-use.md)

---

### Q12: Is there compatibility between APs?

**A:**

**Backward Compatibility**: Generally yes.
- AP242 → AP214: PMI and other data will be lost.
- AP214 → AP203: Colors and layers will be lost.

**Forward Compatibility**: None.
- Reading AP203 data as AP214 is fine (it just provides more features).

**In Practice**: Use the latest version supported by both the sender and receiver.

---

### Q13: What is the difference between AP242 ed2 and ed3?

**A:**

**AP242 ed3 (ISO 10303-242:2022)** Key Additions:
- Enhanced Electrical Harness support.
- Additive Manufacturing (3D printing) support.
- MBSE (Model Based Systems Engineering) integration.

**Compatibility**: High compatibility with ed2.

**Adoption**: CAD support for ed3 is increasing, but Electrical and AM features are still being adopted.

---

## Persistence and Simulation (IDs/Names)

### Q14: Can I assign persistent IDs or names to faces?

**A: Yes**, but not using the `#123` instance IDs. You must use **`SHAPE_ASPECT`** (labels).
- **AP242**: Full support for semantic face/edge naming.
- **AP214**: Partial support (depends on CAD implementation).
- **AP203**: Generally not supported for user-defined names.

Detailed guide: [Persistent IDs and Face Naming](./persistent-ids.md)

---

### Q15: Does Ansys Workbench read face names?

**A: Yes**, it can import them as **Named Selections**.
- Ensure the STEP file is exported as **AP242**.
- In Ansys Geometry import settings, set "Named Selections" to `On`.
- Use a consistent naming convention in CAD to help Ansys filter the selections.

---

### Q16: Why do my face names disappear in simulation?

**A:** Common reasons:
1. **Topology Change**: If you modify the geometry significantly, the CAD system might "lose" the link between the name and the new face.
2. **AP Version**: Exporting as AP203 will strip all name labels.
3. **Export Settings**: Many CAD tools have "Export names" disabled by default.

---

## Implementation

### Q14: What is the recommended parser library?

**A:**

| Language | Library | Characteristics |
|------|-----------|------|
| **C++** | OpenCascade | Commercial-grade, feature-rich |
| | STEP Tools SDK | Commercial, high performance |
| **Python** | pythonOCC | Wrapper for OpenCascade |
| | ifcopenshell | Targeted for IFC but a useful reference |
| **JS/TS** | Custom Implementation | Part 21 parsers are relatively simple |
| **C#** | Xbim | Targeted for IFC but applicable |

**Recommendation**: Use OpenCascade for full-scale C++ implementation; use a custom parser for lightweight requirements.

---

### Q15: How do I traverse entities?

**A:** Basic pattern:

```python
# 1. Find the PRODUCT
product = find_entity_by_type(step_file, 'PRODUCT')

# 2. Traverse references
product_def_formation = traverse(product, 'PRODUCT_DEFINITION_FORMATION')
product_def = traverse(product_def_formation, 'PRODUCT_DEFINITION')

# 3. Access geometry data
shape = traverse(product_def, 'PRODUCT_DEFINITION_SHAPE')
shape_rep = traverse(shape, 'SHAPE_REPRESENTATION')

# 4. Get geometry items
faces = filter_items(shape_rep.items, 'ADVANCED_FACE')
```

Detail: [Data Model Map](../format/data-model-map.md)

---

### Q16: How are units handled?

**A:** Defined in the `GEOMETRIC_REPRESENTATION_CONTEXT` within the STEP file:

```step
#500 = ( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) );
```
→ `.MILLI.,.METRE.` = mm

**Prefixes**:
- `.MILLI.` = 10^-3
- `.CENTI.` = 10^-2
- `.KILO.` = 10^3
- None = 1

**Implementation**: Pre-calculate and cache unit conversion factors.

Detail: [Common Pitfalls - Units](../implementation/common-pitfalls.md)

---

### Q17: How is precision handled?

**A:** Defined by `UNCERTAINTY_MEASURE_WITH_UNIT`:

```step
#600 = UNCERTAINTY_MEASURE_WITH_UNIT(1.0E-6,(#500),'distance_accuracy_value','...');
```
→ Precision is 10^-6 mm.

**Implementation Note**:
- Use as the tolerance for geometric operations.
- Differences in precision between sender and receiver can lead to "gaps" in geometry.

---

## Troubleshooting

### Q18: How do I check if a file is corrupted?

**A:**

**Quick Check**:
1. Do HEADER and DATA sections exist?
2. Does it start with `ISO-10303-21;`?
3. Does it end with `END-ISO-10303-21;`?
4. Can all `#number` references be resolved?

**Tools**:
- **STEP Validators**: STEP Tools, CAx-IF tools.
- **FreeCAD**: Check if it opens without errors.

**Common Errors**:
- Reference inconsistency (missing #number).
- Syntax errors (mismatched parentheses, etc.).
- Encoding issues.

---

### Q19: Why are colors disappearing?

**A:** Common causes:

1. **AP Limitation**: AP203 does not support color; AP214 or later is required.
2. **Style Definition Issue**: `STYLED_ITEM` is not directly linked to the geometry.
3. **Color Definition Layer**: Different CAD systems behave differently depending on whether the color is attached to a Shell or a Face.

**Mitigation**:
- Use AP214 or AP242.
- Verify the link: `STYLED_ITEM` → `PRESENTATION_STYLE_ASSIGNMENT` → `SURFACE_STYLE_RENDERING` → `COLOUR_RGB`.

---

### Q20: Why is the assembly structure breaking?

**A:**

1. **Missing NAUO (NEXT_ASSEMBLY_USAGE_OCCURRENCE)**.
2. **Placement Matrix Inconsistency**: Issues with `CONTEXT_DEPENDENT_SHAPE_REPRESENTATION`.
3. **Broken Parent-Child Links**: Reference errors between `PRODUCT_DEFINITION`s.

**Debugging**:
- List all `PRODUCT` entities.
- Display parent-child relationships via NAUO as a tree.
- Verify validity of placement matrices (e.g., checking if they are not identity matrices by mistake).

Detail: [Common Pitfalls - Assembly](../implementation/common-pitfalls.md)

---

### Q21: Why is PMI missing or unreadable?

**A:**

1. **AP Incompatibility**: Semantic PMI is exclusive to AP242.
2. **Dangling PMI**: `GEOMETRIC_TOLERANCE` is not linked to the target face (`SHAPE_ASPECT`).
3. **CAD Implementation Differences**: Each CAD system interprets PMI differently.

**Mitigation**:
- Use AP242.
- Follow CAx-IF Recommended Practices.
- Validate with test cases.

---

## Tools and Resources

### Q22: Are there free STEP viewers?

**A:**

| Tool | Platforms | Features |
|--------|----------------|------|
| **FreeCAD** | Windows/Mac/Linux | Open-source, editable |
| **3D-Tool Free Viewer** | Windows | Lightweight, fast |
| **OpenCascade CAD Assistant** | Windows/Mac/Linux | Based on OpenCascade |

**Online**:
- Various web services exist, but quality is limited.

---

### Q23: Where can I get a validator?

**A:**

**Free**:
- CAx-IF Recommended Practice checkers: https://www.cax-if.org/

**Commercial**:
- STEP Tools: High-performance validator (Paid).

**Quick Check**:
- Open in FreeCAD and check for warnings/errors.

---

### Q24: Where is the official documentation?

**A:**

**Official Standards** (Paid):
- ISO 10303 series: Purchase from ISO or national standards organizations.

**Free Resources**:
- **CAx-IF**: https://www.cax-if.org/ (Recommended Practices)
- **STEP modularization**: https://www.stepmod.org/ (Schema reference)
- **WikiSTEP**: http://www.wikistep.org/

---

### Q25: What is CAx-IF?

**A:** **CAD-CAx Implementor Forum**: An international group that establishes STEP implementation guidelines between CAD vendors.

**What they provide**:
- Recommended Practices.
- Test Cases.
- Benchmark Files.
- Interoperability validation results.

**Importance for Implementers**:
- Following CAx-IF guidelines significantly improves interoperability.
- It is the only "de-facto standard" for correct implementation.

Website: https://www.cax-if.org/

---

### Q26: What is LOTAR?

**A:** **Long Term Archiving and Retrieval**: A standard for long-term preservation and retrieval of digital STEP data.

**Purpose**:
- Ensure data remains readable for decades (30-50 years).
- Essential for aerospace and defense industries with long product lifecycles.

**Relationship with AP242**: AP242 supports LOTAR.

---

### Q27: What is MBD?

**A:** **Model Based Definition**: A practice where the 3D model is the only "source of truth" (Master), containing all design and manufacturing information.

**Difference from Traditional Methods**:
- **Traditional**: 2D drawings are the master; 3D is a reference.
- **MBD**: 3D model is the master; 2D drawings are unnecessary or subordinate.

**Relationship with STEP**: Semantic PMI in AP242 enables MBD.

---

### Q28: Should I build my own parser or use a library?

**A:**

**Recommended for Custom Implementation**:
- Only a basic Part 21 parser is needed (relatively simple).
- Lightweight and high performance are required.
- License constraints.

**Recommended for Libraries**:
- B-rep geometry operations are needed (NURBS processing, etc.).
- Commercial product (quality assurance is critical).
- Reducing development time.

**Hybrid**:
- Build a custom Part 21 parser and use OpenCascade for geometry processing.

---

### Q29: How do I generate STEP files programmatically?

**A:**

**Method 1: Generate as Text**
```python
with open('output.step', 'w') as f:
    f.write("ISO-10303-21;\n")
    f.write("HEADER;\n")
    # ... Write HEADER
    f.write("DATA;\n")
    f.write(f"#10 = PRODUCT('{name}','{name}','',());\n")
    # ... Write DATA
    f.write("END-ISO-10303-21;\n")
```

**Method 2: Use a Library**
- OpenCascade (C++)
- pythonOCC (Python)

**Key Considerations**:
- Correctly resolve entity dependencies.
- Ensure instance ID uniqueness.
- Set units and precision correctly.

---

### Q30: What are the best sample files for learning?

**A:**

1. **CAx-IF Test Cases**: https://www.cax-if.org/
   - Verified standard samples.

2. **STEP modularization**: https://www.stepmod.org/
   - EXPRESS schemas and simple examples.

3. **DIY**:
   - Create a simple cube in FreeCAD → Export as STEP.
   - Inspect the contents in a text editor.

4. **This Repository**:
   - [Minimal STEP Analysis](../examples/minimal-product.step.md)
   - [STEP File Walkthrough](../examples/step-file-walkthrough.md)

---

## Have more questions?

If your questions are still not answered:

1. Check terms in the **[Glossary](./glossary.md)**.
2. Learn the basics in **[Getting Started](./getting-started.md)**.
3. Understand entity structure in the **[Data Model Map](../format/data-model-map.md)**.
4. Check implementation warnings in **[Common Pitfalls](../implementation/common-pitfalls.md)**.

---
## 📚 Next Steps
- **[Which AP should I use?](../decision-guides/which-ap-should-i-use.md)** - Select the best AP for your project.

[Back to README](../README.md)
