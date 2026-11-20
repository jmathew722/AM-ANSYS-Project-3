# CONTINUE.md — what is left (written 2026-11-20 ~18:20)

Package root: `8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package`. Outputs: `FINALUPLAD_Folder/`. Python: `/c/Program Files/Python314/python.exe` (plain `python` is the Store stub and fails). ANSYS 2025 R1 (v251).

## Status
| # | Case | State |
|---|---|---|
| 1 | BCCZ_Original | SOLVED, converged (tag v2, Y axis) |
| 3 | Cube_Original | SOLVED, converged |
| 4 | Cube_Topo_Optimized | SOLVED, converged (from SLDPRT; IGES is surface-only) |
| 7 | Octet_Truss_Original | SOLVED, converged (tag v3) |
| 5 | Fluorite_Truss_Original | v3 (5 levels) finished; NOT yet post-processed/checked for 2% convergence |
| 6 | Fluorite_Truss_Topo | v4 finished but INVALID for convergence: sizes 0.6/0.45/0.35 mm all gave ~33.9k elements (feature-limited default mesher). Rerun as **v5** with patch-independent mesher, curvature/proximity off (0.6 mm = 249k elements); was at level 1 at 18:16 |
| 2 | BCCZ_Topo_Optimized | tag **v4** (PI mesher, sizes 1.5,1.0,0.6; 323k–381k elements) running; level 1 solve done, history extraction in progress. Levels are nearly the same mesh, so convergence may be weak |
| 8 | Octet_Truss_Topo | tag **pilotpi3** then **v5** (sizes 1.4,1.0,0.8) via `scripts/run_batch9.sh`; just started, no results yet. 93k faces |

Background jobs may still be running (check `tasklist | grep -i ansys`, `FINALUPLAD_Folder/Logs/*_mech.log`). Batch8 (`run_batch8.sh`) will later try Octet_Topo tags pilotpi2/v4; those are blocked by `.skip` flag files in `Logs/` (`wb_run_case.wbjn` exits if `<folder>_<tag>.skip` exists). Hung default-mesh Design#2 processes could not be killed (kill was denied); they time out on their own.

## To do
1. Wait for batches 8/9/10 (`Logs/batch9.done`, `batch10.done`, `batch8.done`). Per-level logs: `Logs/<folder>_<tag>_mech.log` (`LEVEL`, `solve returned`, `DONE`). Expect many hours.
2. When data exists: `python scripts/postprocess8.py v1` (auto-picks v5>v4>v3>v2 if complete incl. `mesh_metrics.csv`), then write `config/case_notes.json` / `Reports/case_status.json` for BLOCKED/PARTIAL notes, `python scripts/make_reports.py`, `python scripts/build_excel8.py v1`.
3. If a topo case cannot finish: mark PARTIAL/BLOCKED with the exact reason. Never fabricate.
4. Not yet written: final technical report (MD/PDF), two-page FEM summary, screenshot gallery, `Logs/run_manifest.json`, per-case PASS/PARTIAL/BLOCKED table, 8-case ranking (valid cases only), verification that `.wbpz` archives reopen, final ZIP.
5. Known gaps to state in the report: no literature validation (NOT VALIDATED); no verified resin density (mass TBD); no SolidWorks Mass Properties/GUI screenshots; yield charts are Python plots (not window captures); IGES→case mapping is provisional (confirm in `config/cases_resolved.json`); CAD is a 6 mm unit cell, not a 30–40 mm specimen; BCCZ and topo cells compress along Y (auto axis detection).
6. Commit and push regularly: `git add -A 8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package && git commit && git push`.

## Handy
- Run one case: `CASE_ID=<id> TAG=<tag> MODE=disp MESH_SIZES=a,b,c scripts/run_case.sh` (for PI mesher also `MECH_SCRIPT=mech_run_pi.py MESH_METHOD=pi MESH_PROPS="CaptureCurvature=False;CaptureProximity=False"`).
- Status table: `FINALUPLAD_Folder/Reports/status.md` (stale; update it).
