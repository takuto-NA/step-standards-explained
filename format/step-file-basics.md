# STEP File Basics

STEP files (`*.stp`, `*.step`) are plain text files specified by ISO 10303-21.

## 1. File Structure (Anatomy)

A STEP file is a collection of "Instances" that reference each other. Visually, you can think of it as a book where each page (Instance) can point to other pages.

```mermaid
graph TD
    subgraph File_Skeleton [File Skeleton]
        ISO["ISO-10303-21;"]
        HEADER_START["HEADER;"]
        HEADER_DATA["FILE_NAME, FILE_SCHEMA..."]
        HEADER_END["ENDSEC;"]
        DATA_START["DATA;"]
        DATA_ENTITIES["#10=PRODUCT(...)<br/>#20=PRODUCT_CONTEXT(...)<br/>#30=..."]
        DATA_END["ENDSEC;"]
        ISO_END["END-ISO-10303-21;"]
    end

    ISO --> HEADER_START
    HEADER_START --> HEADER_DATA
    HEADER_DATA --> HEADER_END
    HEADER_END --> DATA_START
    DATA_START --> DATA_ENTITIES
    DATA_ENTITIES --> DATA_END
    DATA_END --> ISO_END

    subgraph Logical_View [Logical View]
        H[Header: Metadata]
        D[Data: Graph of Entities]
    end
    
    HEADER_DATA -.-> H
    DATA_ENTITIES -.-> D
```

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

### How Instance IDs Reference Each Other

The following diagram shows how entities reference each other using Instance IDs:

```mermaid
graph LR
    P10["#10 PRODUCT<br/>'Part1'"] -->|"frame_of_reference"| PC20["#20 PRODUCT_CONTEXT"]
    PC20 -->|"frame_of_reference"| AC30["#30 APPLICATION_CONTEXT"]
    PDF40["#40 PRODUCT_DEFINITION_FORMATION"] -->|"of_product"| P10
    PD50["#50 PRODUCT_DEFINITION"] -->|"formation"| PDF40
    PDS70["#70 PRODUCT_DEFINITION_SHAPE"] -->|"definition"| PD50
    SDR200["#200 SHAPE_DEFINITION_REPRESENTATION"] -->|"definition"| PDS70
    SDR200 -->|"used_representation"| SR210["#210 SHAPE_REPRESENTATION"]
    SR210 -->|"items"| MSB220["#220 MANIFOLD_SOLID_BREP"]
```

**Key Points**:
- Each arrow shows a reference from one entity to another using `#ID`.
- `#10` references `#20` via the `frame_of_reference` attribute.
- This creates a chain of references that connects product information to geometry.

### Forward References Are Allowed

STEP files allow **forward references**, meaning an entity can reference another entity that is defined later in the file:

```mermaid
graph TD
    P10["#10 PRODUCT<br/>References #20"] -->|"Forward Reference"| PC20["#20 PRODUCT_CONTEXT<br/>Defined Later"]
    PC20 -->|"References #30"| AC30["#30 APPLICATION_CONTEXT<br/>Defined Even Later"]
```

**Why This Matters**:
- Parsers must use **two-pass processing**: First pass builds an instance map, second pass resolves references.
- You cannot resolve references in a single pass because forward references exist.
- This is why using a hash map (dictionary) to store all instances before resolving references is essential.

---
## 📚 Next Steps
- **[Data Model Map](./data-model-map.md)** - Understand the entity hierarchy.

[Back to README](../README.md)
