# Minimal STEP Analysis

A guide to deciphering a real STEP file (`.stp`). Here, we break down the minimal configuration required to define a "single part."
You can download the actual file here: **[minimal_part.step](./minimal_part.step)**

## 1. Header Section
```step
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('STEP AP242 ed2'),'21;1');
FILE_NAME('minimal_part.stp','2023-10-27T10:00:00',('Author Name'),('Company'),'Processor Name','CAD Version','');
FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF { 1 0 10303 442 1 1 4 }'));
ENDSEC;
```
- **FILE_SCHEMA**: Defines which AP (standard version) this file complies with.

## 2. Data Section: Admin Data
```step
DATA;
#10 = PRODUCT('Part_A','Part_A','Part_A description',(#20));
#20 = PRODUCT_CONTEXT('',#30,'design');
#30 = APPLICATION_CONTEXT('managed model based 3d engineering');
#40 = PRODUCT_DEFINITION_FORMATION('1','first version',#10);
#50 = PRODUCT_DEFINITION('design','',#40,#60);
#60 = PRODUCT_DEFINITION_CONTEXT('part definition',#30,'design');
```
- **#10**: The "Part" itself.
- **#50**: Defines the "Design State (Definition)" of the part. Geometry data is attached here.

## 3. Data Section: Links to Shape (Shape Header)
```step
#70 = PRODUCT_DEFINITION_SHAPE('','',#50);
#80 = SHAPE_DEFINITION_REPRESENTATION(#70,#90);
#90 = SHAPE_REPRESENTATION('',(#100),#110);
```
- **#70**: The "junction point" between management data and geometry data.
- **#90**: Acts like a "catalog" for the geometry.

## 4. Data Section: Geometry
```step
#100 = ADVANCED_FACE('',(#120),#130,.T.);
#110 = ( GEOMETRIC_REPRESENTATION_CONTEXT(3) 
         GLOBAL_UNCERTAINTY_ASSIGNMENT((#140))
         GLOBAL_UNIT_ASSIGNMENT((#150,#160,#170))
         REPRESENTATION_CONTEXT('Context #1','3D Context') );
```
- **#100**: A Face. From here, it is further detailed into Surfaces, Edges, and Vertices.
- **#110**: An important context defining units and precision (Uncertainty).

---
## Implementation Hint
When reading a file, first find the `PRODUCT_DEFINITION` (#50). From there, follow the path `PRODUCT_DEFINITION_SHAPE` (#70) -> `SHAPE_REPRESENTATION` (#90) to identify the "main geometry" of that part.
