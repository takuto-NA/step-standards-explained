# Anatomy of Product Entities

A detailed look at the attributes required to correctly define product information in a STEP file (Part 21).

## 1. PRODUCT
The top-level element defining the part or assembly itself.

```express
ENTITY product;
  id : identifier;              -- 1. Part Number
  name : label;                 -- 2. Display Name
  description : OPTIONAL text;  -- 3. Description (Optional)
  frame_of_reference : SET [1:?] OF product_context; -- 4. Design Context
END_ENTITY;
```

- **id**: Must be unique within the implementation context.
- **frame_of_reference**: Usually refers to a `product_context` containing `'mechanical'` or similar to indicate mechanical design.

## 2. PRODUCT_DEFINITION_FORMATION
Manages the "version" or "revision" of a product.

```express
ENTITY product_definition_formation;
  id : identifier;              -- 1. Revision ID (e.g., 'A', '1')
  description : OPTIONAL text;  -- 2. Description
  of_product : product;         -- 3. Target PRODUCT
END_ENTITY;
```

## 3. PRODUCT_DEFINITION
The definition of a product in a specific context (design, analysis, etc.). This is the starting point for linking to geometry data.

```express
ENTITY product_definition;
  id : identifier;              -- 1. Definition ID (e.g., 'design')
  description : OPTIONAL text;  -- 2. Description
  formation : product_definition_formation; -- 3. Target FORMATION
  frame_of_reference : product_definition_context; -- 4. Life-cycle or other context
END_ENTITY;
```

## Implementation Advice
- **Duplicate IDs**: In a Part 21 file, multiple entities may have the same `id` value, but their meanings differ by entity type.
- **Reusing Contexts**: It is standard practice to define a context once (e.g., `#1=PRODUCT_CONTEXT(...)`) and reference it from multiple `PRODUCT` entities.

---
## 📚 Next Steps
- **[Data Model Map](./data-model-map.md)** - See how these entities connect to geometry and each other.

[Back to README](../README.md) | [Back to Data Model Map](./data-model-map.md)
