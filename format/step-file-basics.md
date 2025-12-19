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

## 2. Syntax Overview

Each line in the `DATA` section represents an **entity instance** and follows this standard format:

**`#ID = ENTITY_NAME(Attribute1, Attribute2, ...);`**

| Symbol | Name | Meaning |
| :--- | :--- | :--- |
| `#` | Hash/Pound | Prefix indicating an **Instance ID** follows. |
| `10` | Instance ID | A unique integer identifier for this object within this specific file. |
| `=` | Assignment | Links the ID on the left to the data definition on the right. |
| `ENTITY` | Entity Name | The type of data (defined in the EXPRESS schema, e.g., `PRODUCT`). |
| `(...)` | Attributes | The data values or references to other IDs (e.g., `(#20)`). |
| `;` | Semicolon | Mandatory terminator for every STEP statement. |

## 3. Why Instance IDs (#10, #20...) Matter

- **Reference System**: STEP uses a pointer-based structure. When one entity needs to use another, it refers to its `#ID`.
- **Volatile Nature**: These numbers only need to be unique within the file. It is normal and expected for these numbers to change when a file is re-saved by CAD software.
- **Numbering Convention**: You will often see IDs incremented by 10 (`#10, #20, #30`). This is a legacy practice to allow for manual insertion of entities (e.g., `#15`) without renumbering the whole file.

---
## 📚 Next Steps
- **[Data Model Map](./data-model-map.md)** - Understand the entity hierarchy.

[Back to README](../README.md)
