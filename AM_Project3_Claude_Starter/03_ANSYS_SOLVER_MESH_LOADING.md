# 03 — ANSYS Workbench FEM: boundary conditions, 1000 N trial and convergence

Follow tutorial PDF pp. 15–59 for **Static Structural**: Engineering Data, IGES import, Geometry→Solid→material, mesh, fixed bottom support, top-face force, Z component, ramped loading, Solution→Directional Deformation (Z), Equivalent Total Strain and Equivalent Stress (von Mises), chart, save and archive.

## Loading: do not assume 1000 N is automatically correct
- Source example screenshot shows **5000 N ramped in global +Z**, *not* a required project value. Start with **a 1000 N ramped trial only** once geometry and compression direction are confirmed; choose +/-Z so load actually compresses specimen. Force vector should be zero X/Y, nonzero only Z.
- Run pilot magnitude sweep (e.g., 100/250/500/1000 N as **engineering trial candidates**, not guaranteed safe) and inspect the resulting strain range, material yielding, element distortion, convergence and force balance.
- 1000 N through full footprint 30×30–40×40 mm corresponds to nominal **0.625–1.111 MPa**, substantially lower than material onset stress 19.64 MPa, although local stress concentrations may still yield. Hence 1000 N might NEVER reach effective yield; do not fabricate a yield point.
- For a full stress–strain curve across yield, prefer verified **displacement-controlled stepped compression** if force control stalls/does not reach yield. Keep force-ramped case for tutorial reproduction and compare.
- Use small strain elastic benchmark first; then nonlinear plasticity and large-deflection if warranted; check supports, unintended rigidity, contact, lateral freedom, mesh connectivity and reaction balance.

## Meshing
Use suitable quadratic 3D solids and validate geometry. At least 3 mesh levels; refine successively (for example size multiplier ~0.7), preserve equivalent conditions. Check element metrics, topology, mesh count, solve times, residuals. Compare yield force/yield stress and effective stiffness; proposed <2% change for both across the last two refinements (engineering acceptance choice, **not** lecture's numeric prescription). Peak von Mises stress at a singular corner is not a reliable convergence quantity. If 2% not reached, flag UNCONVERGED and report mesh sensitivity; do not claim mesh independence.

Version-compatible Workbench journaling/Mechanical scripting or PyMechanical needs a verified connection, not a guessed API. A GUI-only manual setup path is acceptable if scripted import isn't available, but report manual requirements honestly.
