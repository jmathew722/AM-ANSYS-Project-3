# Design#7_Octet_Truss_Original — case report

**Status: SOLVED_CONVERGED**

- IGES: `Octet Truss Optimized Config1.IGS`  | SLDPRT: `Octet Truss Optimized Config1.SLDPRT`  | mapping: **PROVISIONAL_NEEDS_HUMAN_CONFIRMATION**
- Geometry (ANSYS import): footprint 6.000 x 6.000 mm, height along compression axis 6.000 mm, solid volume 32.513 mm3, relative density 0.1505, A_full 36.00 mm2
- Material: Tough 2000 (XML; E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density NOT in XML -> mass TBD
- Loading: bottom fixed support, top face prescribed compressive displacement 0.9 mm in 60 substeps, large deflection ON; reaction from fixed support
- Engineering stress = |F|/A_full, strain = u/H0.  Yield = 0.2% strain offset on initial effective slope (secant of first 2 increments)
- **Yield: 1.0891 MPa at strain 0.03734 mm/mm** (F_y = 39.21 N); E_eff = 30.81 MPa; yield/RD = 7.235 MPa

## Mesh convergence (5 levels; criterion <2% for E_eff, yield and Keff between last two)

| level | size mm | elements | E_eff MPa | Keff N/mm | peak F N | yield MPa |
|---|---|---|---|---|---|---|
| 1 | 0.25 | 4524 | 28.592 | 172.015 | 58.7 | 0.9729 |
| 2 | 0.18 | 9067 | 31.017 | 186.562 | 63.0 | 1.0970 |
| 3 | 0.13 | 21889 | 30.896 | 185.834 | 61.7 | 1.0923 |
| 4 | 0.10 | 36180 | 30.866 | 185.650 | 61.0 | 1.0915 |
| 5 | 0.08 | 54347 | 30.812 | 185.329 | 60.8 | 1.0891 |

Last-two-level change: E_eff 0.17%, yield 0.23%, Keff 0.17% -> **CONVERGED (<2%)**

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
