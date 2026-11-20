# CLAUDE.md — Governing instructions for EIGHT final Project 3 FEM cases

Read `README.md`, `01_CASE_MATRIX_AND_CAD_AUDIT.md` through `09_FINAL_ACCEPTANCE_AND_REPORTS.md`, `reference/` and the supplied user geometry files before implementation. This instruction set supersedes all four-design configurations, four-case Excel templates, old `OUTPUTS_Folder` targets, and any octet-only input assumptions. **Exactly 8 cases**, not 4 or 16.

## Nonnegotiable
- Work only in this repository; do not modify the previous octet-lattice validation repo. Output **only** to `FINALUPLAD_Folder/` (native Workbench temporary work files may live in a contained subfolder).
- Material is `Tough 2000` from `materials/AM_Formlabs.xml`; verify **every body** actually uses Tough 2000. Never silently use default Structural Steel.
- Locate real `IGES` and optionally `.SLDPRT` input files; halt the affected case with an explicit missing-file error rather than simulate a substitute geometry. Match Original↔Optimized by design name.
- Discover the installed ANSYS version, license and valid Workbench scripting, Mechanical scripting or PyMechanical API. Execute a minimal verified test; do not hallucinate API methods. Document unavoidable manual GUI steps.
- Maintain the paper/assignment distinction. Project3 PDF: whole original loaded-face area for engineering yield strength; CAD mass/relative density; appropriate benchmark validation; actual experimental comparison if user supplies results.
- Full stress–strain curves require converged multi-increment load histories; **max von Mises vs max equivalent strain** is an instructor-style visualization, NOT the gross engineering stress–strain curve used to rank designs.
- **Never invent yield**. Red-dot annotation only where a defensible yield rule finds a point; otherwise label `YIELD NOT IDENTIFIED` and provide the reason.
- Prefer controlled compression for determining onset and post-yield; 1000 N ramp is a pilot, not a universal stopping load. Determine force direction from model geometry; document positive compression sign conventions.
- **Mesh independence**: minimum 3 meshes per case, continue until predeclared criteria met or report unconverged. No promise of absolute finest mesh/most accurate results without physical and numerical validation.
- Every case must have real ANSYS screenshots of geometry, material assignment, mesh, applied supports/load, equivalent stress, equivalent strain, total and directional deformation, plus plotted curves, CSV, Excel, native .wbpj+_files and .wbpz.
- Never fake GUI screenshots, Workbench saves, archives, solver logs, plots or numeric results. Classify `PASS`, `PARTIAL`, `BLOCKED`, `FAIL`; preserve exact errors and do not claim 'all 8 complete' without a machine-checked output manifest.

## Work stages
(1) inventory and environment (2) geometry/material audit (3) analytic benchmark and independent reference validation (4) pilot original model (5) refined nonlinear solve with yield (6) run remaining 7 (7) real screenshots and exports (8) eight-case Excel and paired comparisons (9) verification and final analysis report.

At each stage update `FINALUPLAD_Folder/Reports/status.md` and `FINALUPLAD_Folder/Logs/run_manifest.json`. Store provenance/assumptions in per-case files. Use deterministic case IDs and no hidden substitutions.
