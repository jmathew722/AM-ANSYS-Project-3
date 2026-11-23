# CLAUDE.md: Finish the remaining ANSYS simulations (Project 3, eight cases)

Written 2026-11-22 from an audit of the cloned repo. Repo root for all paths below:
`ANSYS/8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package/` (called `PKG` here). Outputs go only to `PKG/FINALUPLAD_Folder/`.

**Where this must run:** a Windows machine with ANSYS 2025 R1 (v251) and Workbench. The scripts use Windows paths (`/c/Program Files/Python314/python.exe`; plain `python` is the Store stub and fails). Nothing here can be solved on the Mac this audit was done on.

Read first: `PKG/CLAUDE.md` (governing rules), `PKG/CONTINUE.md`, `PKG/04_MESH_CONVERGENCE_AND_VALIDATION.md`, `PKG/09_FINAL_ACCEPTANCE_AND_REPORTS.md`. The rules in `PKG/CLAUDE.md` still apply: never fake a solve, screenshot, plot or yield; label every case PASS / PARTIAL / BLOCKED / FAIL with the exact error; do not claim "all 8 complete" without a machine-checked manifest.

---

## 1. State of the eight cases

| # | Case | What exists | Verdict |
|---|---|---|---|
| 1 | BCCZ Original | 4-level converged run (tag v2, Y axis). Solve stops at t=0.68. | Usable. Check the early stop. |
| 2 | BCCZ Topo | Tag v4, PI mesher: L1 and L2 solved, **L3 never ran**. No post-processing, no screenshots beyond mesh. | **Not done** |
| 3 | Cube Original | 4-level converged. | Done (solid cube, used as the elastic check) |
| 4 | Cube Topo | 4-level converged, solved from SLDPRT because the IGES is surface-only. | Done |
| 5 | Fluorite Truss Original | Tag v3, 5 levels, E change 0.68%, yield change 0.98%. | Converged by the 2% rule. Confirm it was post-processed (see task 5). |
| 6 | Fluorite Truss Topo | Committed results are tag v4 (3 levels). **v4 is invalid for convergence**: sizes 0.6/0.45/0.35 mm all gave about 34k elements. Tag v5 has only `raw_history_L1.csv`. | **Results not trustworthy. Rerun.** |
| 7 | Octet Truss Original | 5-level converged (tag v3). Solve stops at t=0.5. | Usable. Check the early stop. |
| 8 | Octet Truss Topo | Only pilot runs. Best is `pilotpi3`: force-controlled, solver lost convergence after 55% of the 1000 N ramp (rows after t=0.55 are zeros). v5 has a stdout log only. | **Not done** |

Evidence: `PKG/FINALUPLAD_Folder/Cases/<case>/Raw_Data/`, `Reports/case_results_v1.json`, `PKG/FINALUPLAD_Folder/Logs/<case>_<tag>_mech.log`.

Note: `case_results_v1.json` for Design 6 reports `conv_E` about 9e-5, which looks converged. That value is an artefact of the identical meshes, not real convergence. Do not accept it.

---

## 2. Simulations to run (in priority order)

### Task 1. Design 8, Octet Truss Topo (nothing usable exists)
- Geometry: `Octet_Topo_Cell.IGS` / `.SLDPRT`, 93,160 faces. The default mesher is not practical; use the patch-independent mesher.
- Tag `v5`, sizes `1.4,1.0,0.8` (from `scripts/run_batch9.sh`). Use displacement control (`MODE=disp`), not the 1000 N ramp. The pilot lost convergence at 55% of the ramp, a limit-load symptom, so force control cannot trace post-yield.
- If it still diverges, try a smaller initial substep, more substeps, or a lower maximum displacement. Record what worked.
- Remove or ignore the `.skip` flags `Logs/Design#8_Octet_Truss_Topo_Optimized_pilotpi2.skip` and `..._v4.skip` only if you want those tags run (`wb_run_case.wbjn` exits when its `.skip` exists).

### Task 2. Design 6, Fluorite Truss Topo (rerun, results invalid)
- Rerun as tag `v5` with the patch-independent mesher and curvature/proximity off. At 0.6 mm this gave about 249k elements, so budget hours.
- Choose sizes that really change element count. Verify each level in the log (`LEVEL n size=... elements=...`) before trusting convergence. Counts within a few percent of each other mean the levels are the same mesh.

### Task 3. Design 2, BCCZ Topo (finish)
- Tag `v4` L1 (1.5 mm, 322,676 elements) and L2 (1.0 mm, 322,509 elements) are effectively the **same mesh**, so there is no real convergence yet. L3 (0.6 mm) never ran.
- Rerun with sizes that give clearly different element counts (a genuinely finer level, and a genuinely coarser one if compute allows). Do not call it converged unless the stiffness and yield change is under 2% between the last two levels with distinct meshes.
- Mesh and compute limits are why this stalled; the default mesher hangs for over 3 hours on this geometry (stuck `pilot` processes may still be alive: check `tasklist | grep -i ansys`).

### Task 4. Check the early-stopped solves (Designs 1, 6, 7)
- The committed curves end before the full 0.9 mm displacement: Design 1 at t=0.68, Design 7 at t=0.5, Design 6 at t=0.83 (`truncated_at_time` in each JSON). Find out whether the solver stopped on non-convergence. If so, document it per case. If a longer run is feasible and useful, rerun; otherwise state that the post-yield curve is truncated.

Run one case:
```
CASE_ID=<id> TAG=<tag> MODE=disp MESH_SIZES=a,b,c scripts/run_case.sh
# patch-independent mesher also needs:
MECH_SCRIPT=mech_run_pi.py MESH_METHOD=pi MESH_PROPS="CaptureCurvature=False;CaptureProximity=False"
```
Per-level log markers: `LEVEL`, `solve returned`, `DONE` in `Logs/<case>_<tag>_mech.log`. Completion flags: `Logs/batch<N>.done`.

---

## 3. Work needed after the solves

1. **Post-process:** `python scripts/postprocess8.py v1` (auto-picks the best complete tag: v5 over v4 over v3 over v2, and needs `mesh_metrics.csv`). Writes plots, CSVs and the 8-case comparisons.
2. **Notes and status:** update `config/case_notes.json` and `Reports/case_status.json` with BLOCKED/PARTIAL reasons for any case that cannot finish. Update `Reports/status.md` (stale, last edited 2026-11-20 15:50).
3. **Reports and Excel:** `python scripts/make_reports.py`, then `python scripts/build_excel8.py v1`.
4. **Regenerate the `REPORT/` stress-strain plots** after Designs 2, 6 and 8 have new data. Designs 2 and 8 in `REPORT/` currently come from raw single-mesh histories and carry a warning note; remove that note only when the underlying case is real.

---

## 4. Deliverables that do not exist yet (per the repo's own acceptance list)

- **Screenshots for Designs 2 and 8:** geometry, Tough 2000 assignment, supports and load, total and directional deformation, equivalent stress, equivalent strain. Only Design 2 mesh images and Design 8 pilot images exist. All must be real ANSYS captures.
- **Native Workbench projects and archives:** `.wbpj` + `_files` exist for Designs 1, 3, 4, 5, 6, 7 and a pilot of 8; none for Design 2. **There are zero `.wbpz` archives** (`Workbench_Archives/` is empty). Create one per case and confirm each reopens.
- **Mass properties:** `Geometry_Mass_Properties/` is empty. Resin density is unresolved, so mass is TBD. CAD relative density exists in the JSON results.
- **Manifest:** a `Logs/run_manifest.json` exists, but it must be regenerated and machine-checked against files on disk before any "complete" claim.
- **Final report:** `Reports/FINAL_TECHNICAL_REPORT.md` and `FEM_Preliminary_Summary_2page.pdf` exist but pre-date the missing cases. Redo them after the reruns, including the per-case PASS/PARTIAL/BLOCKED table and an 8-case ranking limited to valid cases.
- **Pair comparisons:** `Comparisons/` has Cube and Fluorite pair plots only. The BCCZ and Octet pair plots need Designs 2 and 8.
- **Final ZIP** of `FINALUPLAD_Folder/`.

---

## 5. Known limitations to state in the report (not fixable by running more solves)

- No literature or experimental validation (label NOT VALIDATED); the solid-cube elastic check (E_eff 1163 MPa vs analytic 1109.5 MPa, +4.9%) is the only benchmark.
- Resin density unverified, so mass TBD.
- No SolidWorks Mass Properties or GUI screenshots.
- Yield charts are Python plots, not Mechanical window captures.
- IGES-to-case mapping is provisional; confirm in `config/cases_resolved.json`.
- CAD is a 6 mm unit cell, not a 30-40 mm specimen; free lateral faces, no contact.
- BCCZ and topo cells compress along Y (auto axis detection); say so wherever Z is mentioned.
- Convergence threshold (<2% for stiffness and yield across the last two levels) is a proposed engineering criterion, not assigned by the instructor.

---

## 6. Working rules for this job

- If a case cannot finish, mark it PARTIAL or BLOCKED with the exact solver error. Never substitute synthetic data or a different geometry.
- Never invent a yield point; where no defensible 0.2% offset intersection exists, label `YIELD NOT IDENTIFIED` with the reason.
- Update `Reports/status.md` and `Logs/run_manifest.json` after each stage.
- Commit regularly; do not push without the user's say-so. Never commit license files or secrets.
