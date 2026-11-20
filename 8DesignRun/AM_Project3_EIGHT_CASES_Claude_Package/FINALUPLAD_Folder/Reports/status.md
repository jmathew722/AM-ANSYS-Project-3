# Status — eight-case run (updated 2026-11-20 ~15:50)
Solver: ANSYS Mechanical 2025 R1 via Workbench batch journals (scripts/wb_run_case.wbjn + mech_run.py). All numbers below are real solver output.

| # | Case | Status | Notes |
|---|---|---|---|
| 1 | BCCZ_Original | SOLVED, CONVERGED (4 levels) | first run along Z was WRONG (loaded thin side strips); axis check selected Y; rerun tag v2 is the valid one |
| 2 | BCCZ_Topo_Optimized | IN PROGRESS / at risk | default mesher hangs (>3 h, IGES and SLDPRT); patch-independent tetra meshes in 91 s but gives 381k elements at 0.6 mm; queued with PI mesher |
| 3 | Cube_Original | SOLVED, CONVERGED (4 levels) | solid 6 mm cube: E_eff 1163 MPa vs analytic 1109.5 (+4.9 %, bonded-end constraint) = elastic verification |
| 4 | Cube_Topo_Optimized | SOLVED, CONVERGED (4 levels) | IGES is surface-only (volume 0): solved from SLDPRT (100.76 mm3) |
| 5 | Fluorite_Truss_Original | 4-level run 2.07 % E change (UNCONVERGED); 5-level rerun (v3) running | |
| 6 | Fluorite_Truss_Topo_Optimized | IN PROGRESS (v4, 3 levels, default mesh) | 1000 N pilot lost convergence at ~40 % load (limit load) |
| 7 | Octet_Truss_Original | SOLVED, CONVERGED (5 levels, v3) | first 4-level run was unconverged (8-12 %) |
| 8 | Octet_Truss_Topo_Optimized | QUEUED (93,160-face geometry; PI mesher) | |

Global caveats: CAD = 6 mm unit cells (spec constraints not demonstrated); IGES->case mapping provisional; resin density unresolved (mass TBD); no literature validation; SolidWorks Mass-Properties/GUI screenshots not captured; "finest mesh" limited by compute for the topo cells.
Processes: stuck default-mesh runs (Design#2 pilot variants) cannot be killed by this agent (permission denied); they time out on their own.
