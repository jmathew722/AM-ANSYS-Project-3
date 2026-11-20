# Design#4_Cube_Topo_Optimized — case report

**Status: SOLVED_CONVERGED**

- IGES: `Cube Topo.IGS`  | SLDPRT: `Cube Topo.SLDPRT`  | mapping: **PROVISIONAL_NEEDS_HUMAN_CONFIRMATION**
- Geometry (ANSYS import): footprint 6.001 x 6.000 mm, height along compression axis 6.000 mm, solid volume 100.765 mm3, relative density 0.4665, A_full 36.00 mm2
- Material: Tough 2000 (XML; E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density NOT in XML -> mass TBD
- Loading: bottom fixed support, top face prescribed compressive displacement 0.9 mm in 60 substeps, large deflection ON; reaction from fixed support
- Engineering stress = |F|/A_full, strain = u/H0.  Yield = 0.2% strain offset on initial effective slope (secant of first 2 increments)
- **Yield: 19.3013 MPa at strain 0.04337 mm/mm** (F_y = 694.90 N); E_eff = 466.58 MPa; yield/RD = 41.378 MPa

## Mesh convergence (4 levels; criterion <2% for E_eff, yield and Keff between last two)

| level | size mm | elements | E_eff MPa | Keff N/mm | peak F N | yield MPa |
|---|---|---|---|---|---|---|
| 1 | 0.50 | 10126 | 467.327 | 2797.405 | 941.9 | 19.3299 |
| 2 | 0.35 | 18592 | 466.981 | 2795.341 | 935.2 | 19.3186 |
| 3 | 0.25 | 31112 | 466.745 | 2793.936 | 930.1 | 19.3077 |
| 4 | 0.18 | 52490 | 466.576 | 2792.930 | 925.7 | 19.3013 |

Last-two-level change: E_eff 0.04%, yield 0.03%, Keff 0.04% -> **CONVERGED (<2%)**

## 1000 N pilot (force-ramped, tag pilot, axis Y)

Reaction at end 800.0 N (nominal 22.220 MPa on full footprint); max axial deformation 0.3821 mm (nominal strain 0.0637); max local equivalent stress 64.81 MPa (constituent onset 19.64 MPa; local only). 1000 N pilot is NOT sufficient for effective-yield ranking; displacement control used for the full curve.

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
