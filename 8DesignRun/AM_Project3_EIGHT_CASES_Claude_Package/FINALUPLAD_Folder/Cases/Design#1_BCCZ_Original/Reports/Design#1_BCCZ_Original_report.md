# Design#1_BCCZ_Original — case report

**Status: SOLVED_CONVERGED**

- IGES: `BCCZ Optimized Config1.IGS`  | SLDPRT: `BCCZ Optimized Config1.SLDPRT`  | mapping: **PROVISIONAL_NEEDS_HUMAN_CONFIRMATION**
- Geometry (ANSYS import): footprint 6.000 x 6.000 mm, height along compression axis 6.000 mm, solid volume 32.848 mm3, relative density 0.1521, A_full 36.00 mm2
- Material: Tough 2000 (XML; E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density NOT in XML -> mass TBD
- Loading: bottom fixed support, top face prescribed compressive displacement 0.9 mm in 60 substeps, large deflection ON; reaction from fixed support
- Engineering stress = |F|/A_full, strain = u/H0.  Yield = 0.2% strain offset on initial effective slope (secant of first 2 increments)
- **Yield: 3.6540 MPa at strain 0.02434 mm/mm** (F_y = 131.54 N); E_eff = 163.56 MPa; yield/RD = 24.028 MPa

## Mesh convergence (4 levels; criterion <2% for E_eff, yield and Keff between last two)

| level | size mm | elements | E_eff MPa | Keff N/mm | peak F N | yield MPa |
|---|---|---|---|---|---|---|
| 1 | 0.50 | 2277 | 164.140 | 982.852 | 87.8 | n/a |
| 2 | 0.35 | 3377 | 163.829 | 980.998 | 116.7 | 2.9155 |
| 3 | 0.25 | 4992 | 163.680 | 980.104 | 133.4 | 3.6761 |
| 4 | 0.18 | 8872 | 163.562 | 979.403 | 132.7 | 3.6540 |

Last-two-level change: E_eff 0.07%, yield 0.60%, Keff 0.07% -> **CONVERGED (<2%)**

## 1000 N pilot (force-ramped, tag pilot2, axis Y)

Reaction at end 45.0 N (nominal 1.250 MPa on full footprint); max axial deformation 0.0733 mm (nominal strain 0.0122); max local equivalent stress 16.89 MPa (constituent onset 19.64 MPa; local only). 1000 N pilot is NOT sufficient for effective-yield ranking; displacement control used for the full curve.

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
