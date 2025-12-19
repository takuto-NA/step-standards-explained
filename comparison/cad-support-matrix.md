# CAD Software STEP Support Matrix

This matrix summarizes the support status of the STEP standard in major CAD software, categorized into "Export" and "Import."

## 1. General Support Matrix (by I/O)

The table below shows the support status for Geometry (G) and PMI (P) as of December 2025.

| Software | Export (Out) | Import (In) | Remarks |
| :--- | :---: | :---: | :--- |
| **Siemens NX** | G:✅ / P:✅ | G:✅ / P:✅ | Industry-leading bidirectional compatibility. ed3 supported. |
| **CATIA V5-6** | G:✅ / P:✅ | G:✅ / P:✅ | Export requires FTA + ST1 licenses. ed2 support is stable. |
| **SolidWorks** | G:✅ / P:✅ | G:✅ / P:✅ | Since 2024, PMI I/O in MBD standard features has been significantly enhanced. |
| **PTC Creo** | G:✅ / P:✅ | G:✅ / P:✅ | Among the fastest to adopt AP242 ed3. |
| **Autodesk Inventor** | G:✅ / P:✅ | G:✅ / P:✅ | Since 2024, the scope of Semantic PMI support has expanded. |
| **Onshape** | G:✅ / P:✅ | G:✅ / P:✅ | PMI support is progressing rapidly due to its cloud-native implementation. |
| **Rhino 8** | G:✅ / P:⚠ | G:✅ / P:⚠ | Improved support for PMI (annotations) in Rhino 8, with some limitations. |
| **FreeCAD** | G:⚠ / P:❌ | G:⚠ / P:❌ | Basic geometry only. AP242 PMI support is limited via plugins. |

---
## 📚 Next Steps
- **[PMI Support](./pmi-support.md)** - Detailed information on dimension and tolerance definitions.

[Back to README](../README.md)

## 2. PMI Support Details

Support levels for "Semantic" and "Graphical" PMI, where caution is particularly required.

| Software | Export (Semantic) | Import (Semantic) | Behavioral Characteristics |
| :--- | :---: | :---: | :--- |
| **NX / CATIA** | ✅ | ✅ | Capable of exchanging semantic information while preserving it. |
| **SolidWorks** | ⚠ (MBD) | ⚠ (2023+) | Prior to 2023, often became display-only upon import. |
| **Inventor** | ✅ | ⚠ | Imported PMI appears as "3D Annotations" but with limitations. |
| **Creo** | ✅ | ✅ | Maintains links between annotations and geometry well. |

---

## 3. Major Milestones by Software

Key milestones that significantly changed I/O capabilities.

| Software | Version | Content |
| :--- | :---: | :--- |
| **SolidWorks** | 2017 | Started AP242 **Export** (including PMI). |
| | 2023 | Enhanced **Semantic Import** from third-party STEP files. |
| **NX** | NX 11 | Established the foundation for full bidirectional AP242 support. |
| **CATIA V5** | V5-6R2018 | Quality improvements for **Graphical PMI** and AP242 ed2 support. |
| **Inventor** | 2019.1 | First support for **PMI Import** from STEP AP242. |
| | 2022.4 | Resolved **AP242 Export** issues for assemblies. |
| **Creo** | Creo 11 | Latest support for AP242 **Edition 3 Export**. |

---

## 4. Implementation Notes

- **Licensing**: In many mid-range to high-end CAD systems, enabling AP242/PMI features requires dedicated packages (MBD, FTA, Extended STEP IF, etc.).
- **Settings**: Many systems have the "Import PMI" option turned off by default, so verification is necessary.
- **CAx-IF**: For the latest interoperability information, it is recommended to refer to test results from the [CAx-IF (CAx Interoperability Forum)](https://www.cax-if.org/).

---

[Back to README](../README.md) | [PMI Support Details](pmi-support.md)
