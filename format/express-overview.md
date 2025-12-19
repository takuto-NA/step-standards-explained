# EXPRESS Overview

The data models for STEP are defined using **EXPRESS** (ISO 10303-11), an information modeling language.

## 1. What is EXPRESS?
- A data definition language with object-oriented-like characteristics.
- It defines Entities, Types, Functions, and Rules.
- A STEP Application Protocol (e.g., AP214) is essentially a massive schema written in EXPRESS.

## 2. How to Read the Schema
```express
ENTITY product;
  id : identifier;
  name : label;
  description : OPTIONAL text;
  frame_of_reference : SET [1:?] OF product_context;
END_ENTITY;
```
- `ENTITY`: Similar to a class.
- `id`, `name`: Attributes.
- `OPTIONAL`: The data value may be null.
- `SET [1:?]`: A set of one or more unique items.

## 3. What Implementers Need to Know
During implementation, rules like "which attributes are mandatory" and "which types are convertible" are all based on these EXPRESS definitions found in the standard.

---
## 📚 Next Steps
- **[Common Pitfalls](../implementation/common-pitfalls.md)** - Problems often encountered during implementation and their solutions.

[Back to README](../README.md)
