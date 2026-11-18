# AME 40643/60643 — Additive Manufacturing Project 3

**Starter package; no ANSYS simulations have been run.** Open this folder in VS Code and launch Claude Code with `START_HERE_PROMPT.md`. This is a **separate repository** from the octet-truss paper reproduction. Copy only vetted utilities if needed; no octet-specific material/geometry settings.

## What is included
- `CLAUDE.md` governing project instructions; numbered engineering and execution documents.
- Original uploaded 60-page ANSYS tutorial PDF, 3-page assignment, 5-slide yield deck, Tough 2000 `.xml`, and six reference screenshots.
- An editable formula-based workbook in `templates/AM_Project3_Editable_Calculations.xlsx` (blank design inputs, **not simulation output**).
- Placeholder folders for .SLDPRT and .IGS files; **those files were NOT among the uploaded files this turn**.
- `config/project_settings.yaml` with a *trial* 1000 N ramp, not a prescriptive correct load.

## Next steps
1. Place SolidWorks models and IGES equivalents in `geometry/SolidWorks_SLDPRT/` and `geometry/IGES/`.
2. Read instructions and run the prompt in VS Code with Claude Code and ANSYS Workbench installed.
3. Review material, geometry and loading audits before any production solve.
4. All actual results go in `OUTPUTS_Folder/`, with saved `.wbpj` + matching `_files`, `.wbpz` archives, data and images.

**Never claim 1000 N is automatically suitable.** An appropriate force must be determined by preliminary nonlinearity, specimen response, contact and convergence; displacement control may be better for post-yield curves.

## Final scope lock: FOUR designs
Exactly four distinct CAD/IGES designs are required. Before running, add four corresponding models into `geometry/SolidWorks_SLDPRT/` and `geometry/IGES/`. The high-priority output for each is a stress-strain graph showing a **red dot marking the computed yield point and its value**, and real stress/strain/deformation contours; see `08_FOUR_DESIGNS_FINAL_VISUAL_ACCEPTANCE.md`. The reference red plot included in the ZIP is an instructor example, not an ANSYS outcome.
