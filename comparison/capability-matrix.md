# Capability Matrix

A detailed comparison of which functions are supported by which AP.

### Functional Coverage Map
```mermaid
graph TD
    subgraph AP242 ["AP242 (Unified)"]
        direction TB
        PMI[Semantic PMI]
        MESH[Tessellation]
        LOTAR[Archiving]
        subgraph AP214 ["AP214 (Automotive)"]
            direction TB
            COLOR[Color / Layer]
            STYLING[Styling]
            subgraph AP203 ["AP203 (Legacy)"]
                direction TB
                GEOM[B-rep Geometry]
                ASSY[Assembly Structure]
            end
        end
    end
```

| Feature Category | Detailed Feature | AP203 | AP214 | AP242 |
| :--- | :--- | :---: | :---: | :---: |
| **Geometry** | B-rep | ✅ | ✅ | ✅ |
| | Surface / Wireframe | ✅ | ✅ | ✅ |
| | Tessellated (Mesh) | ❌ | ⚠ | ✅ |
| **Presentation** | Color / Layer | ❌ | ✅ | ✅ |
| | Transparency | ❌ | ✅ | ✅ |
| **Assembly** | Structure | ✅ | ✅ | ✅ |
| | Simplified Assembly | ❌ | ❌ | ✅ |
| **PMI** | Graphical PMI | ❌ | ⚠ | ✅ |
| | Semantic PMI | ❌ | ❌ | ✅ |
| **Admin** | Material Properties | ⚠ | ✅ | ✅ |
| | User Defined Props | ⚠ | ✅ | ✅ |

**Legend**: ✅ Fully Supported | ⚠ Partially Supported | ❌ Not Supported

---
## 📚 Next Steps
- **[STEP File Walkthrough](../examples/step-file-walkthrough.md)** - Understand real files line by line.

[Back to README](../README.md)
