# Design#6_Fluorite_Truss_Topo_Optimized — case report

**Status: NOT SOLVED / BLOCKED**

- IGES: `Fluorite_Topo Cell.IGS`  | SLDPRT: `Fluorite_Topo Cell.SLDPRT`  | mapping: **PROVISIONAL_NEEDS_HUMAN_CONFIRMATION**

## 1000 N pilot (force-ramped, tag pilot2, axis Y)

Reaction at end 399.5 N (nominal 11.096 MPa on full footprint); max axial deformation 0.6471 mm (nominal strain 0.1079); max local equivalent stress 64.81 MPa (constituent onset 19.64 MPa; local only). 1000 N pilot is NOT sufficient for effective-yield ranking; displacement control used for the full curve.

## Screenshot inventory
- 03_ansys_geometry: EXPORTED_MECHANICAL_IMAGE
- 04_tough2000_assignment: EXPORTED_MECHANICAL_IMAGE
- 05_mesh: EXPORTED_MECHANICAL_IMAGE
- 06_fixed_support_and_loading: EXPORTED_MECHANICAL_IMAGE
- 07_total_deformation: EXPORTED_MECHANICAL_IMAGE
- 08_directional_deformation_z: EXPORTED_MECHANICAL_IMAGE
- 09_equivalent_stress_von_mises: EXPORTED_MECHANICAL_IMAGE
- 10_equivalent_total_strain: EXPORTED_MECHANICAL_IMAGE
- 11_mechanical_stress_strain_chart: EXPORTED_MECHANICAL_IMAGE
- SolidWorks/CAD isometric + mass-properties panels: NOT_AVAILABLE (SolidWorks GUI automation not run)
- yield annotation chart as ANSYS window capture: NOT_AVAILABLE (Python-generated plot supplied in Plots/; Mechanical chart image 11_* is the reaction history chart)

## Limits
- 6 mm unit-cell CAD (not a 30-40 mm specimen; >100 cell constraint not demonstrated); free lateral faces; no contact; no literature validation (NOT VALIDATED); density unresolved.
