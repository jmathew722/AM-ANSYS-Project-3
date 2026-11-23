# 02. Strength/density table (provisional)

Computed 2026-11-22 from the repo's committed ANSYS results, using the instructor's formulas:

- relative yield strength = lattice yield / yield of fully dense Tough 2000
- strength/density ratio = relative yield strength / relative density (must be below 1)

## Fully dense reference
Design 3 (Cube Original) is a solid 6 mm cube (volume 216 mm3, relative density 1.000). Its FEM yield, **49.71 MPa**, is used as the fully dense Tough 2000 value. Confirm with the instructor that this solid-cube run is acceptable as "FEM of a fully dense solid". If not, run a dedicated solid model with the same loading and 0.2% offset rule.

Yield is the 0.2% strain-offset yield on the engineering stress-strain curve (stress = force / full loaded-face area), as computed by `scripts/postprocess8.py`.

## Table

| Design | Relative density | Yield strength (MPa) | Relative yield strength | Strength/density ratio | Reliability |
|---|---|---|---|---|---|
| 1 BCCZ Original | 0.1521 | 3.654 | 0.0735 | 0.483 | Converged (4 levels). Curve stops at t=0.68. |
| 2 BCCZ Topo Optimized | 0.2627 | 8.29 | 0.1668 | 0.635 | **Provisional.** One mesh level that is effectively the same as the second; no convergence; case BLOCKED. |
| 3 Cube Original (solid reference) | 1.000 | 49.71 | 1.000 | 1.000 | Reference only. Not a lattice, exceeds the 50% density limit. |
| 4 Cube Topo Optimized | 0.4665 | 19.30 | 0.3883 | 0.832 | Converged (4 levels). Close to the 50% density limit. |
| 5 Fluorite Truss Original | 0.1244 | 0.2833 | 0.0057 | 0.046 | Converged (5 levels, 0.98% yield change). |
| 6 Fluorite Truss Topo Optimized | 0.4507 | 9.03 | 0.1817 | 0.403 | **Not trustworthy.** Mesh levels were identical (about 34k elements); needs a v5 rerun. |
| 7 Octet Truss Original | 0.1505 | 1.089 | 0.0219 | 0.146 | Converged (5 levels). Curve stops at t=0.5. |
| 8 Octet Truss Topo Optimized | 0.4235 | 9.10 | 0.1831 | 0.432 | **Partial.** Force-controlled pilot, solver stopped at 55% of ramp; single mesh. Needs a rerun. |

All lattice ratios are below 1, as the instructor requires.

## How the numbers were obtained
- Relative density for Designs 1, 3, 4, 5, 6, 7: `RD` field in `FINALUPLAD_Folder/Cases/<case>/Reports/case_results_v1.json` (volume divided by bounding-box volume).
- Relative density for Designs 2 and 8: volume in `Raw_Data/probe/geometry_probe.csv` (56.74 and 91.48 mm3) divided by the 216 mm3 cell volume. Recheck these when the cases are rerun.
- Yield for Designs 1, 3-7: `sigma_y` in the same JSON files. Yield for Designs 2 and 8: computed from the raw histories with the same 0.2% offset rule (see `REPORT/` plots and the notes on those plots).

## Caveats to state in any report
- These are unit-cell FEM values. Printed 30-40 mm parts will differ (free lateral faces, defects, anisotropy, printing resolution). Do not compare them directly to Instron results without discussion.
- Tough 2000 is a polymer resin; yield for the FEM material comes from the XML in `materials/AM_Formlabs.xml`. Resin density is unverified, so no mass or measured-density comparison is possible yet. Relative density here is a geometric volume fraction.
- The strength/density values for Designs 2, 6 and 8 should not be reported as final until their simulations are finished (see `CLAUDE.md` in this folder).
- Rows are only comparable if the loading direction and area convention match. BCCZ and topo cells compress along Y by the repo's axis detection, not Z.
