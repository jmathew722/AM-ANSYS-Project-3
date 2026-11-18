# 07 — Acceptance criteria, literature comparison and milestones

**Mandatory per assignment**: compare at least one calibration design to trustworthy published experimental or numerical results before trusting other FEA designs. The tutorial screenshot's example yield 213 MPa and example 166 MPa experimental comparison **do not validate the user's geometry/material**; obtain and cite a suitable source and check comparability (material, dimensions, load, topology and manufacturing). Do not claim the old octet paper's grey/durable resins represent Tough 2000.

Gates:
1. `CAD_PASS`: valid solid bodies and verified orientation/dimensions, units, density and unit cell count.
2. `MATERIAL_PASS`: Tough 2000 assigned, actual 21-point hardening, density provenance stated.
3. `LOAD_PASS`: correct compressive direction, reaction balance, meaningful range through yield or label not reached.
4. `MESH_PASS`: at least 3 successively refined levels and documented material quantity convergence (<2% target on both yield and Keff as proposed).
5. `YIELD_PASS`: defensible yield algorithm on effective F/A curve, red marker and no fabricated yield.
6. `VALIDATION_PASS`: literature or experimental reference used, comparison errors given, limitations identified.
7. `OUTPUT_PASS`: reopenable Workbench save and archive, Excel formula checks, image/log/export manifest.

Produce a class-ready **two-page FEM results summary** (deadline in reference: Nov 18, 5pm) with full method, side-by-side design metrics, convergence, stress-strain/yield plot and status; no invented outcomes. Note remaining requirements for print (Nov 18, 11pm), testing (Dec 4), full report (Dec 7). Undergraduate report 5–6 pages and graduate 7–8 pages, TNR 12pt, 1-inch margins, single-spaced; references/appendix excluded.

## FINAL FOUR-DESIGN REQUIREMENT (MANDATORY)
Exactly **four candidate designs** named `Design_01` through `Design_04` must be discovered, mapped unambiguously to their native SolidWorks and IGES files, and simulated separately. Do not silently skip a design, duplicate a geometry, or treat example screenshots as genuine results. If files are missing, mark the associated design BLOCKED and continue independently verifiable work.

**Highest-priority output for EACH design:** `OUTPUTS_Folder/Plots/Design_XX/Design_XX_ENGINEERING_STRESS_STRAIN_YIELD.png` plus matching PDF and SVG, using the style shown in `screenshots/reference_slides/REFERENCE_YIELD_GRAPH_RED_DOT.png`: visible red plotted curve, distinct **filled red circular yield marker**, arrow and legend/text `Yield = [actual computed value] MPa; strain = [actual computed strain] mm/mm`. Mark no-yield as `YIELD NOT REACHED — NO VALIDATED POINT`, not a fabricated dot. Generate the tutorial-style local maximum equivalent-stress-versus-maximum equivalent-total-strain plot separately, annotated only if the corresponding yield increment can be located legitimately.

For ALL four designs output verified screenshots of original CAD, imported geometry, mesh, loading and support, **equivalent von Mises stress**, **equivalent total strain**, **total deformation**, **Z directional deformation**, and marked-yield plot; raw history and solver logs; each saved Workbench `.wbpj` plus its `_files` directory and `.wbpz` archive. Export four individual charts, four local-maximum charts, one combined engineering stress–strain comparison, a four-design yield ranking, and four mesh-convergence plots. Cite missing/unsupported evidence explicitly.
