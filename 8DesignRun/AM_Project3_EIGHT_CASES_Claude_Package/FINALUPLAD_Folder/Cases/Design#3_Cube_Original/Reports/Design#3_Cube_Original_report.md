# Design#3_Cube_Original — case report

**Status: SOLVED_CONVERGED**

- IGES: `Cube base.IGS`  | SLDPRT: `Cube base.SLDPRT`  | mapping: **PROVISIONAL_NEEDS_HUMAN_CONFIRMATION**
- Geometry (ANSYS import): footprint 6.000 x 6.000 mm, height along compression axis 6.000 mm, solid volume 216.000 mm3, relative density 1.0000, A_full 36.00 mm2
- Material: Tough 2000 (XML; E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density NOT in XML -> mass TBD
- Loading: bottom fixed support, top face prescribed compressive displacement 0.9 mm in 60 substeps, large deflection ON; reaction from fixed support
- Engineering stress = |F|/A_full, strain = u/H0.  Yield = 0.2% strain offset on initial effective slope (secant of first 2 increments)
- **Yield: 49.7105 MPa at strain 0.04473 mm/mm** (F_y = 1789.58 N); E_eff = 1163.49 MPa; yield/RD = 49.710 MPa

## Mesh convergence (4 levels; criterion <2% for E_eff, yield and Keff between last two)

| level | size mm | elements | E_eff MPa | Keff N/mm | peak F N | yield MPa |
|---|---|---|---|---|---|---|
| 1 | 0.50 | 1728 | 1164.586 | 6971.309 | 2727.4 | 49.9482 |
| 2 | 0.35 | 5832 | 1163.981 | 6967.709 | 2724.5 | 49.8445 |
| 3 | 0.25 | 13824 | 1163.707 | 6966.075 | 2723.0 | 49.7809 |
| 4 | 0.18 | 39304 | 1163.486 | 6964.762 | 2721.4 | 49.7105 |

Last-two-level change: E_eff 0.02%, yield 0.14%, Keff 0.02% -> **CONVERGED (<2%)**

## 1000 N pilot (force-ramped, tag pilot, axis Z (pre-axis-verification script; tie-case))

Reaction at end 1000.0 N (nominal 27.778 MPa on full footprint); max axial deformation 0.1437 mm (nominal strain 0.0239); max local equivalent stress 49.53 MPa (constituent onset 19.64 MPa; local only). 1000 N pilot is NOT sufficient for effective-yield ranking; displacement control used for the full curve.

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
