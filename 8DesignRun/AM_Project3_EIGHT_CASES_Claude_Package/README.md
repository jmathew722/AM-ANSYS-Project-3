# AME Project 3 — Eight-Case Final FEM Rerun

**Eight geometry cases:** BCCZ, Cube, Fluorite Truss, Octet Truss × Original and Topology Optimized. Use Tough 2000 only, from `materials/AM_Formlabs.xml`. Build in VS Code/Claude Code and solve in installed ANSYS Workbench/Mechanical. **No simulations are included in this starter; no results are claimed.**

## Start
1. Open this repository folder in VS Code. Place all eight `.IGS` files (exact names in `01_CASE_MATRIX_AND_CAD_AUDIT.md`) in `geometry/IGES/` and all corresponding `.SLDPRT` files in `geometry/SolidWorks_SLDPRT/`.
2. Review `reference/` and the supplied tutorials; start ANSYS Workbench.
3. Run Claude Code from this directory and paste `START_HERE_PROMPT.md`.
4. Claude must first discover supported local ANSYS automation, inspect the actual CAD, and run a benchmark, then perform eight solves. Workbench must run locally/on a compatible machine; merely opening Workbench does not establish an automation connection.
5. All generated results must be written into the **exact spelling** `FINALUPLAD_Folder/` (user-requested name; do not silently rename to FINALUPLOAD).

## Instructions
`CLAUDE.md` is mandatory; read `01` through `09` in order. The reference images are presentation targets, **not** result evidence. Updated four-design instructions are superseded. Do not confuse the research-paper octet validation with Project 3 results; perform a separate appropriate validation study.
