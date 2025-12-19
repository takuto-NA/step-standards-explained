# STEP File Format Support Matrix (Part 21 vs Part 28)

This document outlines the support status for STEP Part 21 (ASCII) and Part 28 (XML) across major CAD software.

---

## 📊 CAD Software Support Status

### Major CAD Software

| CAD Software | Part 21<br/>(.stp, .step) | Part 28<br/>(.stpx, .stpZ) | Remarks |
|----------------|---------------------------|---------------------------|------|
| **SolidWorks** | ✅ Full Support | ❌ Not Supported | Part 21 only. AP203/214/242 support. |
| **CATIA V5/V6** | ✅ Full Support | ⚠️ Limited | Part 21 is primary. AP214/242 support. No explicit Part 28 support. |
| **Siemens NX** | ✅ Full Support | ✅ Supported | Supports reading/writing .stpx and .stpZ (compressed). |
| **PTC Creo** | ✅ Full Support | ❌ Not Supported | Part 21 only. AP203/214/242 support. |
| **Autodesk Inventor** | ✅ Full Support | ❌ Not Supported | Part 21 only. |
| **Fusion 360** | ✅ Full Support | ❌ Not Supported | Part 21 only. |
| **FreeCAD** | ✅ Full Support | ❌ Not Supported | Based on OpenCascade; Part 21 only. |
| **Rhino** | ✅ Full Support | ❌ Not Supported | Part 21 only. |

### Specialized Tools & Converters

| Tool | Part 21 | Part 28 | Remarks |
|--------|---------|---------|------|
| **Kubotek Kosmos** | ✅ Supported | ✅ Supported | Part 28 support started in Aug 2025 (v7.1). |
| **CAD Exchanger** | ✅ Supported | ⚠️ Limited | Part 21 is primary. |
| **STEP Tools** | ✅ Supported | ✅ Supported | Commercial tool; full support for both formats. |
| **OpenCascade** | ✅ Supported | ❌ Not Supported | Part 21 only (Open Source). |

---

## 📈 Current Status of Part 28 (STEP-XML)

### Standards & History

- **First Published**: 2007 (ISO 10303-28:2007)
- **Latest Version**: ISO 10303-28:2016
- **Official Name**: "ISO 10303-28: Industrial automation systems and integration — Product data representation and exchange — Part 28: Implementation methods: XML representations of EXPRESS schemas and data, using XML schemas"

### Characteristics

**Pros**:
- Compatibility with XML technologies (XSLT transformation, XPath search, etc.).
- Support for assembly-level PMI.
- Support for UUID (Unique Universal ID).
- Integration with Model-Based Enterprise (MBE) processes.

**Cons**:
- Large file sizes (2-3 times larger than Part 21).
- Slow adoption by CAD software vendors.
- Less prevalent compared to Part 21.

### Prevalence (as of 2025)

```
Part 21 (ASCII):  ████████████████████ 99%+
Part 28 (XML):    ██                    Less than 5%
```

**Common Use Cases**:
- 🟢 **Part 21**: CAD data exchange (most common).
- 🟡 **Part 28**: 
  - Long-Term Archiving (LOTAR)
  - MBE process integration
  - Emerging AI/LLM applications
  - Academic and research purposes

---

## 🎯 Recommendations for Implementers

### Choosing a File Format

**When to use Part 21 (`.step`)**:
- ✅ For general CAD-to-CAD data exchange.
- ✅ When maximum compatibility is required.
- ✅ To keep file sizes manageable.
- ✅ When human-readability in a text editor is desired.

**When to consider Part 28 (`.stpx`)**:
- ⚠️ When you want to leverage XML processing tools.
- ⚠️ For long-term archiving purposes (LOTAR compliance).
- ⚠️ For integration with MBE processes.
- ⚠️ When the receiver explicitly specifies Part 28 support.

> [!WARNING]
> **Compatibility Warning**
> 
> Before sending a Part 28 file, **always confirm that the receiver's CAD software supports it.** If not, the file may fail to open.

### Parser Implementation Priority

If you are building a custom STEP parser:

1. **Phase 1**: Support Part 21 (Mandatory)
   - Covers 99% of files.
   - Relatively simple to implement.

2. **Phase 2**: Support Part 28 (Optional)
   - Leverage existing XML parsing libraries.
   - Demand is currently limited.

---

## 🔍 How to Check Part 28 Support

### In CAD Software

Check if `.stpx` appears in the file selection dialog:
```
File → Import → STEP
```

### Via Command Line

**NX (Siemens)**:
```bash
# NX supports Part 28
ugopen -import file.stpx
```

**SolidWorks**:
```
# SolidWorks does not support Part 28; .stpx files will not open.
# Conversion to Part 21 (.step) is required.
```

---

## 📚 Technical Background: Part 21 vs Part 28

### Differences in File Structure

**Part 21 (ASCII)**:
```step
ISO-10303-21;
HEADER;
  FILE_DESCRIPTION(('Example'),'2;1');
  FILE_NAME(...);
  FILE_SCHEMA(('AP242...'));
ENDSEC;
DATA;
  #10=PRODUCT('Part_A',...);
  #20=PRODUCT_DEFINITION(...);
ENDSEC;
END-ISO-10303-21;
```

**Part 28 (XML)**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<iso_10303_28 xmlns="urn:oid:1.0.10303.28.2.1.1"
              version="1">
  <exp:iso_10303 xmlns:exp="..." schema="AP242">
    <product id="id1" name="Part_A">
      ...
    </product>
  </exp:iso_10303>
</iso_10303_28>
```

### File Size Comparison (Examples)

| File | Part 21 | Part 28 | Ratio |
|---------|---------|---------|------|
| Simple Cube | 5 KB | 15 KB | ~3x |
| Mid-size Assembly | 2 MB | 6 MB | ~3x |
| Large Product | 50 MB | 150 MB | ~3x |

---

## 🌐 Related Resources

### Official Standards

- **ISO 10303-21**: Clear text encoding (Part 21)
- **ISO 10303-28**: XML representations (Part 28)
- Available for purchase from ISO or national standards bodies.

### Implementation Guides

- **CAx-IF**: https://www.cax-if.org/
- **PDES Inc.**: https://www.pdesinc.org/
- **Kubotek Kosmos STEP-XML Guide**: https://kubotekkosmos.com/

---

## ❓ FAQ

### Q: Why isn't Part 28 more common given it's newer?

**A:** Main reasons include:

1. **Part 21 is Sufficient**: Most CAD exchange needs are met perfectly well by Part 21.
2. **File Size**: XML is redundant, leading to much larger files.
3. **Slow CAD Adoption**: Major CAD vendors haven't prioritized Part 28 support.
4. **Backward Compatibility**: Part 21 has better compatibility with older systems.

### Q: Will Part 28 become the mainstream in the future?

**A:** In the short term (next ~5 years), **Part 21 will remain the dominant format.**

**In the long term**: Adoption of Part 28 may increase as MBE and AI applications grow, but it is unlikely to completely replace Part 21.

### Q: Can I convert between Part 21 and Part 28?

**A:** Yes, it is possible.

- **Part 21 → Part 28**: Relatively easy since the underlying data structure is the same.
- **Part 28 → Part 21**: Possible (XML to ASCII conversion).

**Conversion Tools**:
- STEP Tools (Commercial)
- Kubotek Kosmos (Commercial)
- Custom scripts (based on EXPRESS schemas)

---

## 📝 Summary

**Advice for Implementers**:

1. **Prioritize Part 21 Support First**
   - Covers 99% of use cases.
   - Supported by all major CAD systems.

2. **Use Part 28 for Specific Needs Only**
   - Long-term archiving.
   - MBE integration.
   - Only when the receiver explicitly supports it.

3. **When in Doubt, Use Part 21**
   - Superior in terms of compatibility, file size, and available tooling.

---

**Last Updated**: 2025-12-19  
**Sources**: Official CAD vendor documentation, CAx-IF, Web research.

---
## 📚 Next Steps
- **[Assembly Support](./assembly-support.md)** - Definition of structures composed of multiple parts.

[Back to README](../README.md)
