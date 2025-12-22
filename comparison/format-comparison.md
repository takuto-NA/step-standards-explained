# Format Comparison: STEP vs. Others

This page compares STEP with other common CAD and 3D data exchange formats to help you choose the right one for your needs.

---

## 📊 Comparison Table

| Feature | **STEP** | **IGES** | **Rhino (.3dm)** | **3D PDF** | **JT** | **Parasolid** | **STL** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Typical Version** | AP242 | 5.3 | (Latest) | PRC | ISO | (Latest) | - |
| **Mathematical Type** | B-rep (Exact) | B-rep / Surface | B-rep (NURBS) | B-rep / Mesh | B-rep + Mesh | B-rep (Kernel) | Mesh |
| **Assembly Support** | ✅ Excellent | ⚠ Limited | ✅ Good | ✅ Good | ✅ Excellent | ✅ Good | ❌ No |
| **Metadata / PMI** | ✅ Semantic | ❌ No | ⚠ Basic | ✅ Semantic | ✅ Semantic | ⚠ Limited | ❌ No |
| **Openness** | 🌍 ISO Standard | 🌍 De-facto | 🔓 Semi-Open | 🌍 ISO Standard | 🌍 ISO Standard | 🔑 Proprietary | 🌍 Open |
| **Primary Use Case** | Interop, Archive | Legacy Data | Design | Collaboration | Visualization | Kernel Native | 3D Printing |

---

## 🔍 Detailed Breakdown

### 1. STEP (ISO 10303)
The gold standard for neutral data exchange. It is the only format that combines mathematical precision (B-rep) with rich metadata (PMI) and international standardization.
- **Pros**: Vendor neutral, precise, supports full product life cycle.
- **Cons**: Large file size, complex implementation.

### 2. IGES (Initial Graphics Exchange Specification)
The predecessor to STEP. While still common in legacy systems, it lacks the data consistency and assembly management capabilities of STEP.
- **Pros**: High compatibility with older systems.
- **Cons**: "Leaky" geometry (gaps), deprecated by many modern systems.

### 3. Rhino (.3dm)
The native format for Rhinoceros 3D. While technically proprietary, it is widely considered "semi-open" due to the **OpenNURBS** initiative.
- **Pros**: Native support for complex NURBS and meshes; excellent for industrial design and computational geometry (Grasshopper).
- **Cons**: Not an ISO standard; version compatibility can be an issue between different Rhino versions.
- **OpenNURBS**: A free, open-source C++ and .NET library that allows developers to read and write .3dm files without needing Rhino installed. This makes it a popular alternative to STEP for design-to-manufacturing workflows in specific industries (like marine or architecture).

### 4. 3D PDF (PRC vs. U3D)
A way to share 3D models using the universal PDF format.
- **PRC (Product Representation Compact)**: The high-end version. Supports **exact B-rep geometry** and **semantic PMI**. It is a direct competitor to STEP for Model-Based Definition (MBD) collaboration.
- **U3D (Universal 3D)**: The legacy/visualization version. Primarily mesh-based (like STL but with colors). Suitable for simple viewing but not for downstream engineering.
- **Pros**: Can be opened by anyone with Adobe Acrobat; combines 2D documentation with 3D data.
- **Cons**: Large file sizes; limited support in non-Adobe PDF viewers.

→ **[Detailed Comparison: STEP vs. 3D PDF](./step-vs-3dpdf.md)**

### 5. JT (Jupiter Tessellation)
Originally proprietary (Siemens), now an ISO standard. Optimized for large-scale visualization and PLM (Product Lifecycle Management).
- **Pros**: High performance for ultra-large assemblies, supports both B-rep and Mesh.
- **Cons**: Heavily tied to the Siemens ecosystem.

### 6. Parasolid (.x_t / .x_b)
A "native" format used by systems built on the Parasolid kernel (Siemens NX, SolidWorks, Onshape). 
- **Pros**: Extremely robust for systems using the same kernel.
- **Cons**: Proprietary; may require conversion for non-Parasolid systems.

### 7. ACIS (.sat)
A "native" format used by systems built on the ACIS kernel (CATIA v4, AutoCAD, Rhino).
- **Pros**: Robust within the ACIS ecosystem.
- **Cons**: Proprietary; less common than Parasolid in modern mainstream CAD.

### 8. STL (Stereolithography)
A mesh-only format that approximates surfaces with triangles.
- **Pros**: Simple, universal standard for 3D printing.
- **Cons**: No precision (lossy), no assembly information, no colors.

---

## 🏗️ Version & Implementation Nuances

To make a fair comparison, it is important to consider the specific versions and implementation details of each format.

### IGES: Surface-only (v4.0) vs. B-rep (v5.1+)
- **Legacy IGES (v4.0 and earlier)**: Primarily focused on individual surfaces and curves. This led to the famous "leaky geometry" problem where surfaces didn't quite meet, making it difficult to form solid models.
- **Modern IGES (v5.3)**: Technically supports B-rep (solid) definitions. However, many CAD exporters still use the older surface-based methods, leading to persistent interoperability issues compared to the more strictly defined STEP.

### STEP: The Evolution of Application Protocols (AP)
- **AP203 / AP214**: The traditional standards. AP214 added colors and layers, which made it the "go-to" for decades.
- **AP242**: The current "Master" protocol. It merges the best of its predecessors and adds critical modern features like **Semantic PMI** and **Tessellation**. When people say "STEP is old," they are usually thinking of AP203; AP242 is a very modern standard.

### 3D PDF: Visualization vs. Engineering Data
- When using 3D PDF for engineering, ensure your exporter is using the **PRC** format. If you use U3D, you are essentially sending a "3D picture" (mesh) that cannot be used for precise measurements or CAM operations.

### Rhino (.3dm): OpenNURBS and Interoperability
- While STEP is the standard for generic CAD exchange, **.3dm** is often preferred in industries using Rhino/Grasshopper because it preserves native NURBS data and attributes (like layers and custom object properties) more reliably when moving between Rhino-friendly applications.

---

## 💡 Which one should I use?

- **For CAD Interoperability**: Use **STEP** (AP242 or AP214).
- **For Industrial Design / Rhino Workflows**: Use **.3dm** (if supported by both ends) or **STEP**.
- **For Non-CAD Collaboration**: Use **3D PDF (PRC)** if the recipient needs to see PMI but doesn't have a CAD viewer.
- **For 3D Printing**: Use **STL** (or 3MF).
- **For High-End Visuals / AR**: Use **glTF** or **OBJ**.
- **For Long-Term Archiving**: Use **STEP** (LOTAR compliant).

[Back to README](../README.md)

