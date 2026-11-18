# Design_03 (Octet_Truss_Smooth) — validation / methods
Status: **SOLVED, preliminary. NOT literature-validated. Mesh: yield change last two levels 1.99 %, E_eff change 1.09 % (target <2 %: met).**
- Solver: ANSYS Mechanical 2025 R1, Static Structural, large deflection, quadratic tets, Tough 2000 (XML, 21-pt multilinear hardening), bottom face fixed, top face prescribed -Z displacement 0.9 mm in 60 substeps.
- CAD: IGES, bbox 6x6x6 mm (single unit cell), Mechanical volume 103.619 mm3, RD 0.4797, A_full=36.0 mm2, H0=6.000 mm. SolidWorks mass-properties panel not extracted.
- Engineering stress = |Fz|/A_full, strain = u/H0. Yield = 0.2 % offset on initial secant slope of first 2 increments: **6.987 MPa at strain 0.03816** (F_y=251.5 N); E_eff=193.2 MPa.
- Stress plateaus ~13.2 MPa (material saturates at last XML plastic point 64.8 MPa; no extrapolation).

| Level | size mm | elements | E_eff MPa | Keff N/mm | yield MPa |
|---|---|---|---|---|---|
| L1 | 0.50 | 2393 | 193.2 | 1159.72 | 7.204 |
| L2 | 0.35 | 5958 | 195.3 | 1172.64 | 7.129 |
| L3 | 0.25 | 10741 | 193.2 | 1159.89 | 6.987 |

Limits: unit-cell model with free lateral faces (no periodic BC, no contact/self-contact, no damage); resolution of 0.2 % offset is limited by 0.25 % strain increments; density sourced not measured; 1000 N pilot see status.md.
Screenshots: EXPORTED_MECHANICAL_IMAGE (Mechanical ExportImage, real) for 03–11; 01/02 SolidWorks views NOT_AVAILABLE (no GUI automation); 12 yield chart NOT_AVAILABLE as window capture (Python plot provided separately).
