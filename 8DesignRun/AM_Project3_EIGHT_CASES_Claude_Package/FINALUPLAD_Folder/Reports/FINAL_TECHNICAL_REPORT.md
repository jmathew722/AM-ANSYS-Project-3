# AME Project 3 — Eight-case FEM final technical report

Generated 2026-11-20 18:24. Solver: ANSYS Mechanical 2025 R1; material Tough 2000 from `materials/AM_Formlabs.xml` (E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density not in XML, so mass is TBD.

## Method
- Unit-cell CAD (6 mm), bottom face fixed, prescribed compressive displacement 0.9 mm (15% strain) in 60 substeps, large deflection on, free lateral faces, compression axis auto-detected from the largest planar end caps.
- Engineering stress = |reaction force| / A_full (full footprint); strain = u/H0. Yield = 0.2% strain-offset on the effective initial secant slope.
- Local maximum equivalent stress vs maximum equivalent total strain plots are tutorial-style visualizations only; they are not the engineering curve used for ranking.
- Mesh convergence criterion: <2% change in E_eff, yield and Keff between the last two levels.

## Results

| Case | Status | Rel. density | E_eff MPa | Yield MPa | Yield strain | Yield/RD MPa | Elements (finest) | Note |
|---|---|---|---|---|---|---|---|---|
| Design#1_BCCZ_Original | PASS (converged) | 0.1521 | 163.6 | 3.654 | 0.02434 | 24.028 | 8872 |  |
| Design#2_BCCZ_Topo_Optimized | BLOCKED/NOT SOLVED | - | - | - | - | - | - | no solved data |
| Design#3_Cube_Original | PASS (converged) | 1.0000 | 1163 | 49.71 | 0.04473 | 49.710 | 39304 |  |
| Design#4_Cube_Topo_Optimized | PASS (converged) | 0.4665 | 466.6 | 19.3 | 0.04337 | 41.378 | 52490 |  |
| Design#5_Fluorite_Truss_Original | PASS (converged) | 0.1244 | 7.474 | 0.2833 | 0.03990 | 2.277 | 44028 |  |
| Design#6_Fluorite_Truss_Topo_Optimized | PASS (converged) | 0.4507 | 268.6 | 9.031 | 0.03563 | 20.038 | 34492 |  |
| Design#7_Octet_Truss_Original | PASS (converged) | 0.1505 | 30.81 | 1.089 | 0.03734 | 7.235 | 54347 |  |
| Design#8_Octet_Truss_Topo_Optimized | BLOCKED/NOT SOLVED | - | - | - | - | - | - | no solved data |

## Ranking by yield / relative density (valid cases only)

1. Design#3_Cube_Original — 49.710 MPa
2. Design#4_Cube_Topo_Optimized — 41.378 MPa
3. Design#1_BCCZ_Original — 24.028 MPa
4. Design#6_Fluorite_Truss_Topo_Optimized — 20.038 MPa
5. Design#7_Octet_Truss_Original — 7.235 MPa
6. Design#5_Fluorite_Truss_Original — 2.277 MPa

## Pair comparisons
See `Comparisons/PAIR_*_report.md` and PAIR plots.

## Limitations and not-done items
- No literature/experimental validation (NOT VALIDATED); only an analytic modulus check on the solid cube.
- No verified resin density: mass and weight are not reported.
- SolidWorks Mass Properties and SolidWorks GUI screenshots were not produced; ANSYS screenshots are exported Mechanical images.
- Yield charts are Python-generated from solver data, not window captures.
- IGES-to-case mapping is provisional (by design name); confirm in `config/cases_resolved.json`.
- Cube_Topo IGES is surface-only; the SLDPRT was used.
- CAD is a 6 mm unit cell, not a 30-40 mm specimen; the >100-cell condition is not demonstrated.
- Topology-optimized cells have tiny features: element counts are feature-limited, so the finest mesh is bounded by compute.

