# Persistent IDs and Face Naming in STEP

For simulation (CAE) and manufacturing, being able to identify specific faces or edges consistently is crucial. This guide explains how names and IDs are handled in the STEP standard.

## 1. ID vs. Name: The Reality of Persistence

In the STEP file itself, every entity has an **Instance ID** (e.g., `#10`, `#500`). However, these are **not persistent**. If you re-save the file from your CAD software, these numbers will likely change.

For "Persistent IDs" that survive re-exports and work in tools like Ansys, the standard uses **`SHAPE_ASPECT`**.

- **Internal ID (#123)**: Volatile. Changes every time the file is saved.
- **`SHAPE_ASPECT` Name**: Persistent. This is a string label (e.g., `'Inlet'`, `'FixedSupport'`) attached to the geometry.

## 2. Technical Implementation (AP242)

To name a face, the STEP file creates a link between the geometric face and a "Shape Aspect" entity.

### STEP Code Snippet
Here is how a named face looks inside a Part 21 file:

```step
/* 1. The geometric face */
#100 = ADVANCED_FACE('Face_Name_Internal', (#110), #120, .T.);

/* 2. The Semantic Label (The "Persistent ID") */
#200 = SHAPE_ASPECT('Inlet', 'Description', #300, .T.);

/* 3. The link between the name and the geometry */
#400 = ( SHAPE_ASPECT_RELATIONSHIP('','',#200,#500) );
/* ... simplified for readability ... */
```

## 3. Rhino 8 / Grasshopper Workflow

Rhino 8 significantly improved the export of these attributes.

### Rhino 8 Manual Export
1. Select the face (Sub-object selection: `Ctrl+Shift+Click`).
2. In the **Properties** panel, set the **Object Name**.
3. When exporting as STEP, select **AP242**.
4. Ensure "Export object names" or similar is checked in the options.

### Grasshopper (Rhino 8)
1. Use the **Model Object** components to assign attributes to geometry.
2. Use the **Bake** component with the attributes set.
3. The names assigned to faces in Grasshopper will now carry through to the STEP export if AP242 is used.

## 4. Ansys Workbench Integration

Ansys Workbench can read these labels and automatically convert them into **Named Selections**.

### Required Settings in Ansys
1. **Geometry Import Options**:
   - Set **Named Selections** to `On`.
   - **Named Selection Key**: This is a filter prefix. If you leave it blank, Ansys will try to import all compatible labels. If you set it to `NS`, it will only import labels starting with `NS`.
2. **Filtering**:
   - Ansys looks for `SHAPE_ASPECT` labels (and sometimes `GEOMETRIC_SET` names) and maps them to its internal selection system.
   - If names don't appear, check if the export was **AP242** (best) or **AP214** (standard for colors/layers).

## 5. Summary Table

| Feature | AP203 | AP214 | AP242 |
| :--- | :---: | :---: | :---: |
| Instance IDs (#) | Volatile | Volatile | Volatile |
| Face Names (Labels) | ❌ Poor | ⚠ Partial | ✅ Robust |
| Persistence | ❌ No | ⚠ Manual | ✅ Semantic |

---
[Back to README](../README.md)

