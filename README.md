# STEP Standards Explained

> A practical guide to the STEP standard (ISO 10303): Explaining versions, capabilities, and implementation methods.

---

## 🚀 STEP in 30 Seconds

**STEP** is an international standard (ISO 10303) for exchanging 3D CAD data between different CAD systems.

- **File Formats**: `.stp` / `.step` (text files)
- **Primary Uses**: CAD data exchange, long-term archiving
- **Difference from STL**: STL only contains geometry (triangular mesh), while STEP can preserve colors, assemblies, and PMI (Product and Manufacturing Information/tolerances).

**Who is this repository for?**:
- ✅ Engineers implementing STEP parsers or exporters
- ✅ Project managers for CAD data conversion
- ✅ Implementers seeking a systematic understanding of the STEP standard

---

## 📚 Learning Path for Implementers (Recommended Order)

Designed for implementers new to STEP to learn efficiently.

### Step 1: Establish Foundational Knowledge (Time: 30 mins)

1. **[⭐ Glossary](./docs/glossary.md)** - Understand STEP-specific terminology (Crucial!)
2. **[Persistent IDs and Face Naming](./docs/persistent-ids.md)** - Critical for simulation (Ansys/Rhino)
3. **[Getting Started Guide for Implementers](./docs/getting-started.md)** - Quickly grasp the big picture
3. **[FAQ](./docs/faq.md)** - Resolve common questions

### Step 2: Select the Right AP for Your Project (Time: 15 mins)

4. **[Which AP should I use?](./decision-guides/which-ap-should-i-use.md)** - Decision guide
5. **[Capability Matrix](./comparison/capability-matrix.md)** - Check detailed functional differences

### Step 3: Understand Data Structures (Time: 1-2 hours)

6. **[STEP File Walkthrough](./examples/step-file-walkthrough.md)** - Understand real files line by line
7. **[Data Model Map](./format/data-model-map.md)** - Grasp the entity hierarchy
8. **[Geometry and Topology](./format/geometry-and-topology.md)** - Deep dive into mathematical representation (NURBS, etc.)
9. **[EXPRESS Language Basics](./format/express-overview.md)** - Learn how to read schemas

### Step 4: Implementation & Troubleshooting (Reference as needed)

10. **[Common Pitfalls](./implementation/common-pitfalls.md)** - Implementation warnings and solutions
11. **[Validation and CAx-IF](./implementation/validation-and-caxif.md)** - Methods for quality assurance

---

## ❓ Quick FAQ

<details>
<summary><strong>Q1: What is the difference between STEP and STL?</strong></summary>

**STL (Stereolithography)**:
- Triangular mesh only
- No color or assembly information
- Low precision (approximate representation)
- Primary use: 3D printing

**STEP**:
- Precise mathematical geometry (B-rep: Boundary Representation)
- Supports colors, assemblies, and PMI (tolerances)
- Larger file sizes
- Primary use: CAD data exchange, long-term archiving
</details>

<details>
<summary><strong>Q2: Which CAD software supports STEP?</strong></summary>

All major CAD software supports it:
- SolidWorks, CATIA, NX, Creo, Inventor
- Fusion360, FreeCAD, Rhino, etc.

However, **supported APs (standard versions) vary**. See the [CAD Support Matrix](./comparison/cad-support-matrix.md) for details.
</details>

<details>
<summary><strong>Q3: Is it okay to open it in a text editor?</strong></summary>

**Yes, it is.** Since STEP files are plain text, you can open them with Notepad or VS Code.

However:
- Large files (tens of MBs or more) may take time to open.
- Be careful when editing (syntax errors can corrupt the file).
- Use a STEP viewer (like FreeCAD) to view the actual geometry.

**Recommended uses**: Header inspection, entity searching, debugging.
</details>

<details>
<summary><strong>Q4: Why are the file sizes so large?</strong></summary>

STEP tends to be large due to:
- **Text Format**: More redundant than binary.
- **Complete Geometry Description**: Mathematically precise definitions of surfaces and curves.
- **Management Data**: Metadata for products, assemblies, PMI, etc.

**Mitigation**:
- Use tessellation (polygonal approximation) (AP242).
- Compression (.zip or .step.gz).
- Remove unnecessary information.
</details>

<details>
<summary><strong>Q5: What's the difference between AP203, AP214, and AP242 in one sentence?</strong></summary>

- **AP203**: Legacy. Geometry only. High compatibility.
- **AP214**: Automotive origin. Supports colors and layers. Current mainstream.
- **AP242**: Latest. Supports PMI (tolerances) and MBD (Model Based Definition).

**Advice for Implementers**: If in doubt, **AP242 ed2** is a safe choice.
</details>

**[→ View more FAQs (20+ items)](./docs/faq.md)**

---

## 📊 Quick Comparison

**Legend**: ✅ Fully Supported | ⚠ Partially Supported | ❌ Not Supported

| Feature | AP203 | AP214 | AP242 ed2 | AP242 ed3 |
| :--- | :---: | :---: | :---: | :---: |
| 3D B-rep | ✅ | ✅ | ✅ | ✅ |
| Assembly | ✅ | ✅ | ✅ | ✅ |
| Color / Layer | ❌ | ✅ | ✅ | ✅ |
| PMI (Graphical) | ❌ | ⚠ | ✅ | ✅ |
| PMI (Semantic) | ❌ | ❌ | ✅ | ✅ |
| Tessellation | ❌ | ❌ | ✅ | ✅ |
| AM / Electrical | ❌ | ❌ | ⚠ | ✅ |

**Details**: [Capability Matrix](./comparison/capability-matrix.md) | [PMI Support](./comparison/pmi-support.md) | [CAD Support Matrix](./comparison/cad-support-matrix.md)

---

## 🗺 Repository Structure (Navigation Map)

```
step-standards-explained/
├─ docs/               ← 📘 Intro guides, Glossary, FAQ
├─ decision-guides/    ← 🎯 AP selection guides
├─ versions/           ← 📑 AP details (AP203/AP214/AP242, etc.)
├─ comparison/         ← 📊 Capability matrices, CAD support
├─ format/             ← ⚙️ Data structures, EXPRESS explanation
├─ implementation/     ← 🔧 Implementation know-how, Pitfalls
└─ examples/           ← 💡 Sample files and walkthroughs
```

**Quick Links**:
- 🛠️ **[Common Pitfalls](./implementation/common-pitfalls.md)** - Start here if you're stuck
- 📐 **[AP242 ed2 Details](./versions/ap242-ed2.md)** - The current mainstream standard
- 📖 **[Glossary](./docs/glossary.md)** - Check terminology if confused

---

## 🤝 Contributing

Suggestions for fixes or new information are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## Disclaimer

The content of this repository is based on community research. For definitive information, always refer to the official ISO standards. [Details: disclaimer.md](./disclaimer.md)

[LICENSE (CC-BY-4.0)](./LICENSE.md)
