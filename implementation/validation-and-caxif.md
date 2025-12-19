# Validation and CAx-IF

This document explains the mechanisms for ensuring the quality of STEP data and the activities of the community.

## 1. What is CAx-IF (Implementor Forum)?
* An international group consisting of major CAD vendors (Autodesk, Dassault, Siemens, PTC, etc.) that develops the "Recommended Practices," which serve as the implementation bible for STEP.
* **Following these "Recommended Practices" is more critical for successful practical implementation than following the official standard alone.**

## 2. Geometric Validation Properties (GVP)
* A mechanism to verify that geometric data has been transmitted correctly.
* Geometric information such as volume, surface area, and center of mass is embedded within the STEP data. The receiver can then recalculate these values and compare them to detect conversion errors.

### GVP Workflow
```mermaid
flowchart LR
    subgraph Sender ["Sender (CAD Exporter)"]
        S_GEO[Original Geometry] --> S_CALC[Calculate Volume/Area]
        S_CALC --> S_EMBED["Embed GVP Entities<br/>(GEOMETRIC_VALIDATION_PROPERTY)"]
        S_EMBED --> S_STEP[Output STEP File]
    end
    
    S_STEP --> Receiver
    
    subgraph Receiver ["Receiver (CAD Importer)"]
        R_STEP[Read STEP File] --> R_GEO[Imported Geometry]
        R_STEP --> R_VAL["Read Embedded GVP"]
        R_GEO --> R_RECALC[Recalculate Volume/Area]
        R_RECALC --> COMP{Compare}
        R_VAL --> COMP
        COMP -->|Match| Success([Success])
        COMP -->|Mismatch| Warn([Warning: Data Corrupted])
    end
```

## 3. Recommended Resources
* [CAx-IF Recommended Practices](https://www.cax-if.org/joint_testing_info.html) - Guidelines for implementation.
* [MBx Interoperability Forum](https://www.mbx-if.org/) - Latest interoperability information.

---
## 📚 Next Steps
- **[Minimal Export](./minimal-export.md)** - Try exporting your own STEP file.

[Back to README](../README.md)
