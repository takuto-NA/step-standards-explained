# STEP File Basics

STEP files (`*.stp`, `*.step`) are plain text files specified by ISO 10303-21.

## 1. File Structure
The file is broadly divided into three sections.

```text
ISO-10303-21;
HEADER;
  /* Metadata: Filename, author, AP definition, etc. */
  FILE_NAME(...);
  FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF'));
ENDSEC;

DATA;
  /* Actual data entities */
  #10=PRODUCT('Part1','Part1','',(#20));
  #20=PRODUCT_CONTEXT('',#30,'');
  ...
ENDSEC;

END-ISO-10303-21;
```

## 2. Why Instance IDs (#10, #20...) Matter
- STEP uses a **pointer (reference)** based structure.
- When one entity references another, it uses these numbers.
- **Note**: These numbers only need to be unique within the file and have no inherent meaning (IDs). It is normal for these numbers to change when a file is re-saved.

---
## 📚 Next Steps
- **[Data Model Map](./data-model-map.md)** - Understand the entity hierarchy.

[Back to README](../README.md)
