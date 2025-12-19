# Geometry and Topology

> [!NOTE]
> **Target Audience**: Advanced Implementers & Geometry Kernel Developers  
> **Prerequisites**: Please read the **[Glossary](../docs/glossary.md)** and **[Data Model Map](./data-model-map.md)** first.

This page provides a deep dive into the mathematical and structural representation of geometry in STEP, covering NURBS, complex topology, and geometric continuity.

---

## 1. Foundations of NURBS

NURBS (Non-Uniform Rational B-Splines) are the mathematical backbone of STEP B-rep.

### Relationships: Bézier, B-Spline, and NURBS

Think of these as a hierarchy of increasing control and mathematical complexity:

| Curve Type | Hierarchy | Key Characteristics |
| :--- | :--- | :--- |
| **Bézier Curve** | Base | The simplest form. A single polynomial segment. Moving one control point affects the **entire curve**. |
| **B-Spline** | Extension | A sequence of Bézier curves joined together. Moving a control point only affects a **local segment** (Local Control). |
| **NURBS** | Final Form | Adds **Weights** (Rational) and **Non-Uniform** knots. Can perfectly represent **circles and ellipses**, which regular B-splines cannot. |

**The "NURBS" Name Breakdown**:
*   **Non-Uniform**: Knots don't have to be equally spaced (allows for varying "speed" along the parameter $u$).
*   **Rational**: Uses **Weights**. This is required to define exact conic sections (circles, ellipses, hyperbolas).
*   **B-Spline**: Basis-Spline. A method of joining multiple polynomial segments with a specific level of continuity.

**Note on T-Splines**:
Standard STEP (ISO 10303) **does not natively support T-Splines** as a distinct mathematical entity. When CAD systems (like Fusion 360 or Rhino) export T-Spline models to STEP, they are automatically **converted into a collection of standard NURBS patches**. This ensures compatibility with all STEP-compliant software but may result in a higher number of faces.

### Key Components

| Term | Meaning | Impact on Shape |
| :--- | :--- | :--- |
| **Degree** (次数) | The degree of the polynomial (e.g., 3 for cubic splines). | Higher degrees allow for smoother curves but increase calculation cost. |
| **Knot Vector** (ノットベクトル) | A sequence of parameter values that determine where the spline segments meet. | Multiple knots at the same position (multiplicity) create "sharp" corners or discontinuities. |
| **Control Points** | Points that "pull" the curve toward them. | Moving a control point locally affects the shape. |
| **Weights** (重み) | Used in **Rational** B-splines. | Allows exact representation of conic sections (circles, ellipses, hyperbolas). |

### Mathematical Definition

NURBS can represent both curves and surfaces.

#### 1. NURBS Curve $C(u)$

A NURBS curve is defined as:

$$
C(u) = \frac{\sum_{i=0}^n N_{i,p}(u) w_i P_i}{\sum_{i=0}^n N_{i,p}(u) w_i}
$$

*(In plain text: Sum of (Basis * Weight * ControlPoint) / Sum of (Basis * Weight))*

#### 2. NURBS Surface $S(u, v)$

A NURBS surface is defined as the bivariate extension:

$$
S(u, v) = \frac{\sum_{i=0}^n \sum_{j=0}^m N_{i,p}(u) N_{j,q}(v) w_{i,j} P_{i,j}}{\sum_{i=0}^n \sum_{j=0}^m N_{i,p}(u) N_{j,q}(v) w_{i,j}}
$$

*(In plain text: Sum of (Basis_u * Basis_v * Weight * ControlPoint) / Sum of (Basis_u * Basis_v * Weight))*

Where:
*   **$P$**: Control Points (grid for surfaces).
*   **$w$**: Weights.
*   **$N$**: B-spline Basis Functions of degree $p$ (and $q$ for surfaces), defined by the **Cox-de Boor recursion formula**.
*   **$u, v$**: Parameters.

#### Basis Function Recursion (Cox-de Boor)

The basis functions $N_{i,p}(u)$ are defined recursively:
- **Degree 0**: $N_{i,0}(u) = 1$ if $u_i \le u < u_{i+1}$, else $0$.
- **Degree $p$**: $N_{i,p}(u) = \frac{u - u_i}{u_{i+p} - u_i} N_{i,p-1}(u) + \frac{u_{i+p+1} - u}{u_{i+p+1} - u_{i+1}} N_{i+1,p-1}(u)$

#### Matrix Representation (Implementation Perspective)

In computer graphics and CAD kernels, B-splines can be evaluated using matrix forms. For a single segment:

$$
C(u) = \mathbf{U} \mathbf{M} \mathbf{P}
$$

Where:
*   **$\mathbf{U}$**: The parameter vector $[u^p, u^{p-1}, \dots, u, 1]$.
*   **$\mathbf{M}$**: The basis matrix (determined by the degree and knot vector).
*   **$\mathbf{P}$**: The vector of control points.

*Note: For NURBS, the same operation is performed on weighted control points in homogeneous coordinates $(w_i x_i, w_i y_i, w_i z_i, w_i)$, then projected back.*

#### How is it uniquely determined?

A NURBS curve is uniquely defined by four inputs:
1.  **Degree ($p$)**: Determines the polynomial complexity.
2.  **Knot Vector ($U$)**: A non-decreasing sequence of numbers (e.g., $\{0, 0, 0, 1, 2, 3, 3, 3\}$). It dictates how the control points influence the curve along the parameter $u$.
3.  **Control Points ($P_i$)**: The skeleton of the curve.
4.  **Weights ($w_i$)**: The "strength" of each control point. If all weights are 1.0, the curve is a non-rational B-spline.

**Uniqueness Note**: In STEP, these are explicitly stored in entities like `B_SPLINE_CURVE_WITH_KNOTS`. A NURBS curve is only "determined" within the range of its knot vector (typically $[u_{min}, u_{max}]$).

---

### Parameter Space: 2D vs. 3D

STEP uses two ways to define curves on surfaces:

1.  **Space Curve (3D)**: Defined directly in 3D XYZ space (e.g., `B_SPLINE_CURVE_WITH_KNOTS`).
2.  **PCurve (2D)**: Defined in the 2D UV parameter space of a surface (e.g., `PCURVE`).

**Why both?**  
Robust geometry kernels use `PCURVE` to ensure that the boundary of a face (the trim line) lies exactly on the surface, preventing "gaps" or "leaks" in the model during import/export.

---

## 2. Topology and B-rep Types

STEP differentiates between "Solid" (Closed) and "Surface" (Open) models.

### Closed vs. Open Shells

```mermaid
graph TD
    MSB["MANIFOLD_SOLID_BREP<br/>(Solid/Water-tight)"] --> CS["CLOSED_SHELL"]
    SBSM["SHELL_BASED_SURFACE_MODEL<br/>(Sheet/Open)"] --> OS["OPEN_SHELL"]
    
    CS --> AF["ADVANCED_FACE"]
    OS --> AF
```

*   **MANIFOLD_SOLID_BREP**: Represents a "water-tight" solid. It must have a volume.
*   **SHELL_BASED_SURFACE_MODEL**: Represents surfaces with no volume (e.g., a thin sheet of metal).

### Voids and Hollow Solids

For solids with internal cavities (voids), STEP uses `ORIENTED_CLOSED_SHELL`.

1.  **Outer Bound**: The exterior shell (oriented "out").
2.  **Voids**: One or more internal closed shells (oriented "in").

---

## 3. Geometric Entities & Primitives

### Primitives (CSG)
While STEP is primarily B-rep, it supports "Primitives" which can be used in CSG (Constructive Solid Geometry) operations or as B-rep underlying geometry:

*   `BLOCK`: A rectangular box.
*   `CYLINDER`: A cylinder.
*   `SPHERE`: A sphere.
*   `TORUS`: A doughnut shape.

### Complex Surfaces & Fillets

CAD kernels prioritize using the simplest mathematical definition (**Elementary Surfaces**) to keep files lightweight and precise before falling back to **NURBS**.

*   **Elementary Surfaces for Fillets**:
    *   `CYLINDRICAL_SURFACE`: Often used for constant-radius fillets along straight edges.
    *   `TOROIDAL_SURFACE` / `SPHERICAL_SURFACE`: Used for fillets at corners or along circular edges.
*   **NURBS (`B_SPLINE_SURFACE`)**: Used for **Variable Radius Fillets** or complex "blends" where multiple surfaces meet.
*   **Note**: Many CAD systems offer an "Export all surfaces as NURBS" option. While this increases file size, it is sometimes used to improve compatibility between systems that might struggle to interpret complex elementary surface intersections.
*   **Offset Surface**: A surface defined at a constant distance from a base surface (`OFFSET_SURFACE`).

---

## 4. Continuity and Quality

### Geometric Continuity (G0, G1, G2)

When two surfaces or curves meet, their "smoothness" is defined by continuity:

| Type | Name | Visual Result |
| :--- | :--- | :--- |
| **G0** | Positional | The elements touch, but there is a visible "crease". |
| **G1** | Tangential | The transition is smooth (no crease), but the reflection might "jump". |
| **G2** | Curvature | The transition is perfectly smooth; reflections flow across the boundary. |

**STEP Implementation**: Continuity is often explicitly declared in NURBS entities (e.g., `continuity: geometric_continuity_2`).

---

## 5. Physical Properties (Mass Properties)

STEP can store calculated physical data so that the receiving system can verify the integrity of the geometry.

*   **Volume**: Stored in `GEOMETRIC_ITEM_SPECIFIC_USAGE` linked to a `VOLUME_UNIT`.
*   **Mass / Center of Gravity**: Often stored under `PROPERTY_DEFINITION` entities.
*   **Validation Properties**: Special entities like `VALUATION_PROPERTY` are used to store "check values" for area and volume. If the imported model's volume differs from this value, the import is considered failed or "lossy".

---

## 💡 Implementation Tips

1.  **Check for Water-tightness**: If you are importing a `MANIFOLD_SOLID_BREP`, verify that every `EDGE_CURVE` is shared by exactly two `ADVANCED_FACE`s (manifold condition).
2.  **Handle Degree 1 Splines**: Often, CAD systems export polylines as degree 1 NURBS.
3.  **Torus Inversion**: Pay attention to the `axis` and `radius` attributes of `TOROIDAL_SURFACE`. If the minor radius is larger than the major radius, it becomes a self-intersecting "spindle torus".

---
## 📚 Next Steps
- **[Common Pitfalls](../implementation/common-pitfalls.md)** - Learn about tolerance issues.
- **[Validation and CAx-IF](../implementation/validation-and-caxif.md)** - How to use validation properties.

---
## 🔗 Further Reading & References

1.  **The NURBS Book** (Les Piegl and Wayne Tiller): The "Bible" of NURBS. Essential for anyone implementing geometry kernels.
2.  **NURBS-Python (geomdl) Documentation**: Excellent practical examples and visual explanations of NURBS math.
3.  **CAx-IF Recommended Practices**: Official guidelines on how to implement STEP geometry to ensure interoperability between CAD systems.
4.  **ISO 10303-42**: The official part of the STEP standard that defines "Geometric and topological representation."

[Back to README](../README.md)

