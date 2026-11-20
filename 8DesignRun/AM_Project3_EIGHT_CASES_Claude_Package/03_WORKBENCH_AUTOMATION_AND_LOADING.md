# 03 — ANSYS Workbench/Mechanical automation and loading

Environment preflight: OS, ANSYS version, license, Workbench path, Mechanical batch interface, Python environment, CAD import route. Choose tested Workbench journal/Mechanical scripting/PyMechanical. Do not assume `python` alone controls Workbench. Demonstrate tiny static analysis save/open/export first. Record command, dependencies and logs. 

Geometry import of IGES: repair or fail with logs; do not arbitrarily thicken struts/close holes. Save native Workbench project and material assignment. Use quadratic structural solids where appropriate; inspect curvature/local radius, joint mesh, mesh quality and DOF. For topologically optimized geometry especially inspect tiny fins, narrow-neck areas, disconnected solids and sliver surfaces.

**Boundary conditions:** verify the compression direction/axis for each CAD. Bottom supported face or representative platen fixed in physically justified manner; load top in compression along actual specimen axis, no transverse force components. Retain lateral freedom unless platen physics requires otherwise. Document differences from the tutorial and do not equate it to experiments without comparable contact/platen models.

**Loading phase A:** nonlinear static structural, ramped force pilot up to 1000 N, using appropriately many saved converged load increments. Record whether any yield onset and expected strain has been reached. 1000 N is a user-proposed trial, not validated as enough/safe. For cases showing yield inaccessible or load-control instability, perform **phase B: displacement-controlled compression**, with gradual adaptive increments through the supported initial post-yield response. Determine target displacement from actual geometry, material and numerical behavior—not a hardcoded huge compression. Separate pilot and final files. Ensure engineering curves are from actual load histories, not individual snapshots.

Enable large deformation where needed, validate nonlinear plasticity from XML, employ automatic time stepping and residual diagnostics; model contact/self-contact only if relevant and justified. Do not use arbitrary failure criterion/element deletion. Preserve peak force/yield force, reaction balance, total applied force, geometry boundary screenshots and solver status.

For every case save .wbpj + matching _files subdirectory and .wbpz *after* saving, within `FINALUPLAD_Folder/Workbench_Projects/` and `/Workbench_Archives/`. Verify archive opens, or record why not. Avoid overwritten naming: one case ID per project/archive.
