# Minimal Export

When creating (implementing) a STEP file from scratch, you don't need to include every possible entity from the start.

## 1. Shortest Path to Success

1. **Prepare the HEADER Section**: Specify the correct AP name.
2. **Minimal PRODUCT Configuration**:
   - `PRODUCT`
   - `PRODUCT_DEFINITION`
   - `PRODUCT_DEFINITION_SHAPE`
3. **Geometry Basics**:
   - `CARTESIAN_POINT`
   - `DIRECTION`
   - `AXIS2_PLACEMENT_3D`

## 2. Minimal Template (AP242)

Use this as a base and add geometric elements as needed. See the [sample file (minimal_part.step)](../examples/minimal_part.step) for reference.

```step
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Minimal Export Template'),'21;1');
FILE_NAME('export.step','2025-12-19T10:00:00',('Author'),('Organization'),'Processor','System','');
FILE_SCHEMA(('AP242_MANAGED_MODEL_BASED_3D_ENGINEERING_MIM_LF { 1 0 10303 442 1 1 4 }'));
ENDSEC;
DATA;
#10 = PRODUCT('PART_ID','PART_NAME','',(#20));
#20 = PRODUCT_CONTEXT('',#30,'mechanical');
#30 = APPLICATION_CONTEXT('managed model based 3d engineering');
#40 = PRODUCT_DEFINITION_FORMATION('1','',#10);
#50 = PRODUCT_DEFINITION('design','',#40,#60);
#60 = PRODUCT_DEFINITION_CONTEXT('part definition',#30,'design');
#70 = PRODUCT_DEFINITION_SHAPE('','',#50);
#80 = SHAPE_DEFINITION_REPRESENTATION(#70,#90);
#90 = SHAPE_REPRESENTATION('',(#100),#110);
#100 = AXIS2_PLACEMENT_3D('',#120,#130,#140);
#110 = ( GEOMETRIC_REPRESENTATION_CONTEXT(3) 
         GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#150))
         GLOBAL_UNIT_ASSIGNED_CONTEXT((#160,#170,#180))
         REPRESENTATION_CONTEXT('Context #1','3D Context') );
#120 = CARTESIAN_POINT('',(0.0,0.0,0.0));
#130 = DIRECTION('',(0.0,0.0,1.0));
#140 = DIRECTION('',(1.0,0.0,0.0));
#150 = UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.0E-06),#160,'DISTANCE_ACCURACY_VALUE','');
#160 = ( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) );
#170 = ( NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.) );
#180 = ( NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT() );
ENDSEC;
END-ISO-10303-21;
```

## 3. Implementation Checklist
- [ ] **Instance ID Consistency**: Ensure `#numbers` are unique within the file.
- [ ] **HEADER AP Name**: Is the `FILE_SCHEMA` correct? (Did you mix up AP214 and AP242?)
- [ ] **Unit System (SI_UNIT)**: Explicitly state whether you are using `.MILLI.,.METRE.` (mm) or `.METRE.` (m).
- [ ] **Structure Integrity**: Are `ENDSEC;` and `END-ISO-10303-21;` present?

## 4. Geometry Verification Tips
* Using `ADVANCED_BREP_SHAPE_REPRESENTATION` is the most reliable method.
* Start with a single `CLOSED_SHELL`.

## 5. Validation Tools
* **NIST STEP File Analyzer**: A powerful tool to check if generated files comply with the standard.
* **CAx-IF Checkers**: Validate files from an interoperability perspective.

---
## 📚 Next Steps
- **[Common Pitfalls](./common-pitfalls.md)** - Points where implementations often fail.

[Back to README](../README.md)
