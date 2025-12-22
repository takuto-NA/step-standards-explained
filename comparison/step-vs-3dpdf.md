# Deep Dive: STEP vs. 3D PDF (PRC)

While STEP is the undisputed king of CAD data exchange, **3D PDF (specifically the PRC format)** has emerged as a powerful "dark horse" for collaboration and Model-Based Definition (MBD).

This page provides a thorough comparison to help you understand when to use which.

---

## Data vs. Document

| | **STEP (ISO 10303)** | **3D PDF (PRC / ISO 14739)** |
| :--- | :--- | :--- |
| **Concept** | **Pure Data**. A set of mathematical instructions for machines/CAD. | **Document**. A human-readable container that *includes* 3D data. |
| **Primary Audience** | Engineers, CAM Programmers, Inspection software. | Decision-makers, Suppliers, Shop floor, Maintenance. |
| **Viewer** | Requires a CAD viewer or CAD system. | Adobe Acrobat Reader (Universal). |

---

## 🛠️ Detailed Technical Comparison

### 1. Geometry Fidelity
- **STEP**: Always provides the exact mathematical definition (B-rep). Perfect for downstream manufacturing.
- **3D PDF (PRC)**: Can also store exact B-rep geometry. PRC is highly compressed but mathematically identical to the source.
- **3D PDF (U3D)**: Only stores a mesh (tessellated) approximation. **Avoid U3D for engineering exchange.**

### 2. PMI (Product Manufacturing Information)
- **STEP (AP242)**: Supports **Semantic PMI**. The data is machine-interpretable (e.g., an automated CMM machine can "read" the tolerance).
- **3D PDF (PRC)**: Excellent support for **Graphical PMI**. It looks exactly like the CAD drawing, which is great for humans. While it can store semantic data, many PDF tools prioritize the visual representation.

### 3. IP Protection & Security
- **STEP**: A plain text file. Anyone with the file has your full intellectual property. There is no built-in encryption or rights management.
- **3D PDF**: Inherits all the security features of PDF. You can:
    - Password protect the file.
    - Disable printing.
    - Disable measurement.
    - Add watermarks.
    - Set expiration dates for access (DRM).

### 4. Integration with Non-3D Data
- **STEP**: Strictly 3D and product metadata. You cannot embed a "User Manual" or "Inspection Report" inside a STEP file.
- **3D PDF**: You can combine the 3D model with 2D text, interactive forms, tables, and even video. You can build a complete "Technical Data Package" (TDP) in a single file.

---

## 📊 Comparison Matrix

| Feature | **STEP (AP242)** | **3D PDF (PRC)** |
| :--- | :--- | :--- |
| **ISO Standard** | ✅ Yes (10303) | ✅ Yes (14739 / 24517) |
| **Machine-Interpretable** | ✅ Excellent | ⚠ Limited |
| **Human-Readable (Visual)** | ⚠ Requires CAD software | ✅ Excellent (Universal) |
| **File Compression** | ⚠ Large (Text) | ✅ Excellent (Binary/Compressed) |
| **Security / Encryption** | ❌ No | ✅ Strong (Adobe DRM) |
| **Long-Term Archiving** | ✅ LOTAR Compliant | ✅ PDF/A-4 and PDF/E |
| **Interactive Forms** | ❌ No | ✅ Yes |

---

## 🏗️ CAD Software Support for 3D PDF

While 3D PDF is widely used, native support for **PRC (Exact Geometry)** varies by CAD system. Many systems support **U3D (Mesh)** natively but require plugins for high-fidelity PRC export.

### 1. Support Matrix (Native Export)

| CAD Software | 3D PDF Support | Export Type | Notes |
| :--- | :---: | :--- | :--- |
| **SolidWorks** | ✅ Native | PRC | High-quality export with PMI. |
| **CATIA V5 / V6** | ✅ Native | PRC | Integrated into the core export options. |
| **Siemens NX** | ✅ Native | PRC / U3D | Robust support via "Technical Data Package" (TDP). |
| **Autodesk Inventor** | ✅ Native | PRC | Added in newer versions (2017+). |
| **Creo Parametric** | ✅ Native | PRC / U3D | Extensive support for MBD workflows. |
| **Fusion 360** | ⚠ Limited | U3D | Primarily for visualization; limited PMI support. |
| **FreeCAD** | ⚠ Plugin | U3D | Requires community plugins or macros. |

### 2. Native vs. Third-Party Plugins

For many CAD systems, the "Save As PDF" option might only produce a 2D drawing or a low-fidelity 3D mesh (U3D). To get full **PRC B-rep** support with semantic PMI, many companies use specialized technical publishing tools:

- **Anark**: High-end technical data package (TDP) publishing.
- **PROSTEP (PDF Generator 3D)**: Advanced server-side conversion from major CAD formats to 3D PDF.
- **Elysium (3D PDF Solution)**: High-fidelity translation specializing in data integrity.
- **Tetra4D**: The official Adobe technology partner for 3D PDF (converter and enrichment tools).

---

## 💡 Which one should I choose?

### Choose **STEP (AP242)** if...
- You are sending data to a **supplier who needs to manufacture the part** (CNC, Mold making).
- You are performing **automated inspection** (CMM).
- You need the data to be the "Master" for **future CAD modifications**.

### Choose **3D PDF (PRC)** if...
- You need to **share design concepts with non-CAD users** (Marketing, Sales, Clients).
- You are providing **assembly instructions** to the shop floor.
- You want to **protect your intellectual property** (sharing the shape but preventing easy replication).
- You need to bundle the 3D model with **legal contracts or technical reports**.

---

## 🔗 Further Reading
- [ISO 10303 (STEP) Official Site](https://www.iso.org/standard/65743.html)
- [3D PDF Consortium](https://www.3dpdfconsortium.org/)
- [LOTAR (Long Term Archiving and Retrieval)](http://www.lotar-international.org/)

[Back to Format Comparison](./format-comparison.md) | [Back to README](../README.md)

