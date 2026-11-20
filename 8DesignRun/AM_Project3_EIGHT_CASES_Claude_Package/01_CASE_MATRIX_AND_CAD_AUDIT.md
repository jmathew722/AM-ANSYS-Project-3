# 01 — Eight-design case matrix and CAD verification

Use **exact** IGES filenames from user image (spaces matter). Do not infer names from model type alone.

| Case ID | Design | Variant | IGES basename |
|---|---|---|---|
| BCCZ_Original | BCCZ | Original | `BCCZ_Original.IGS` |
| BCCZ_Topo_Optimized | BCCZ | Topo Optimized | `BCCZ_Topo Optimized.IGS` |
| Cube_Original | Cube | Original | `Cube_Original.IGS` |
| Cube_Topo_Optimized | Cube | Topo Optimized | `Cube_Topo Optimized.IGS` |
| Fluorite_Truss_Original | Fluorite Truss | Original | `Fluorite Truss_Original.IGS` |
| Fluorite_Truss_Topo_Optimized | Fluorite Truss | Topo Optimized | `Fluorite Truss_Topo Optimized.IGS` |
| Octet_Truss_Original | Octet Truss | Original | `Octet Truss_Original.IGS` |
| Octet_Truss_Topo_Optimized | Octet Truss | Topo Optimized | `Octet Truss_Topo Optimized.IGS` |

All in `geometry/IGES/`. Match SolidWorks `.SLDPRT` equivalents in `geometry/SolidWorks_SLDPRT/` via verified name mapping; never guess if names differ. A `.SLDPRT` is not a prerequisite for a verified IGES solve but is preferred for SolidWorks mass properties and feature inspection.

For each design, record exact path, SHA-256, import success, length-unit assumption/confirmed units, bounding box W×D×H, orientation, bodies and connected components, watertight volume, local min feature/thickness if measurable, zero-thickness/nonmanifold concerns, top/bottom face identification, gross loaded area, solid volume, empty envelope volume and comparison of IGES vs SLDPRT geometry. Preserve evidence screenshots.

Assignment physical constraints: part L=30–40 mm, W=30–40 mm, H=15–20 mm; >100 unit cells; relative density <0.5; feature size ≥0.2 mm. Do **not** assume isolated unit-cell CAD satisfies full part constraints. Flag unknown counts/features rather than mark pass.

Use robust semantic face identification based on bounding extrema + orientation + tolerances, not persistent CAD face IDs that may change when imported. Support/faces must be verified visually before solve. Optimized geometries may have cutouts, tiny ligaments and disconnected islands; check these separately. Confirm same boundary and material conventions across paired comparisons.
