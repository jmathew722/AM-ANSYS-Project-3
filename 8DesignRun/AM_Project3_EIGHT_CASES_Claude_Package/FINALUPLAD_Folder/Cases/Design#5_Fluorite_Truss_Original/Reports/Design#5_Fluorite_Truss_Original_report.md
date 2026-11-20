# Design#5_Fluorite_Truss_Original — case report

**Status: SOLVED_UNCONVERGED**

- IGES: `Fluorite Truss Optimized.IGS`  | SLDPRT: `Fluorite Truss Optimized.SLDPRT`  | mapping: **PROVISIONAL_NEEDS_HUMAN_CONFIRMATION**
- Geometry (ANSYS import): footprint 6.000 x 6.000 mm, height along compression axis 6.000 mm, solid volume 26.873 mm3, relative density 0.1244, A_full 36.00 mm2
- Material: Tough 2000 (XML; E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density NOT in XML -> mass TBD
- Loading: bottom fixed support, top face prescribed compressive displacement 0.9 mm in 60 substeps, large deflection ON; reaction from fixed support
- Engineering stress = |F|/A_full, strain = u/H0.  Yield = 0.2% strain offset on initial effective slope (secant of first 2 increments)
- **Yield: 0.2961 MPa at strain 0.04047 mm/mm** (F_y = 10.66 N); E_eff = 7.70 MPa; yield/RD = 2.380 MPa

## Mesh convergence (4 levels; criterion <2% for E_eff, yield and Keff between last two)

| level | size mm | elements | E_eff MPa | Keff N/mm | peak F N | yield MPa |
|---|---|---|---|---|---|---|
| 1 | 0.50 | 2354 | 7.791 | 46.865 | 30.1 | 0.3066 |
| 2 | 0.35 | 3068 | 7.467 | 44.914 | 29.0 | 0.2940 |
| 3 | 0.25 | 4082 | 7.542 | 45.368 | 29.0 | 0.2954 |
| 4 | 0.18 | 10706 | 7.698 | 46.307 | 28.8 | 0.2961 |

Last-two-level change: E_eff 2.07%, yield 0.22%, Keff 2.07% -> **NOT converged to 2%**

## 1000 N pilot (force-ramped, tag pilot, axis Z (pre-axis-verification script; tie-case))

Reaction at end 0.0 N (nominal 0.000 MPa on full footprint); max axial deformation 0.0000 mm (nominal strain 0.0000); max local equivalent stress 0.00 MPa (constituent onset 19.64 MPa; local only). 1000 N pilot is NOT sufficient for effective-yield ranking; displacement control used for the full curve.

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
