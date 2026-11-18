# 02 — Tough 2000 Engineering Data and plasticity

File: `materials/AM_Formlabs.xml` — ANSYS Engineering Data XML version 24.1.0.230. Import through Workbench **Engineering Data → Engineering Data Sources → add custom library**, then **add Tough 2000 to the project**, return to Mechanical and **explicitly assign Tough 2000 to every solid body**; screenshot Details → Material → Assignment (not Structural Steel).

**Exact XML properties:** E = 1,109,500,000 Pa = **1109.5 MPa**; Poisson ratio = **0.35**; bulk modulus = 1232.7777778 MPa; shear modulus = 410.9259259 MPa. Isotropic multilinear hardening contains **21 points** from stress 19.6405024 MPa at plastic strain 0 through stress 64.8184716 MPa at plastic strain 0.0324693243. Preserve and apply all 21 ordered paired points with MPa / dimensionless plastic strain units; do not invent extension beyond last plastic point. Do not mistake 19.6405 MPa constituent onset for effective lattice yield. The XML **does not include density**; do not assume the deck's SolidWorks example mass applies to Tough 2000.

Verify: XML parsed successfully; compatible library and version; each assigned solid uses Tough 2000 and has linear elasticity + actual isotropic hardening. Check material curves visually and export inputs as CSV. If the XML does not import as expected, state the precise failure and provide the verified manual procedure; do not silently replace with steel.

Material model may be inadequate for large deformation, damage, fracture, strain-rate/viscoelastic response: report limits without inventing missing physics.
