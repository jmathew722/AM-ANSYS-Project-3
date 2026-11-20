# 06 — Real screenshots, traceable ANSYS saves, and exact output destinations

Everything belongs under `FINALUPLAD_Folder/` (exact uppercase spelling). Do not place final deliverables in old `OUTPUTS_Folder`. Make folders and manifest early, then verify each path after each case. Native input CAD remains in geometry, but snapshots and audit data inside final folder.

For EACH case require actual saved screenshots, not restyled reconstructions, of: (1) imported original CAD and front/iso view (2) material Tough 2000 assigned (3) mesh overall and joint closeup at final mesh (4) top load applied and bottom support (5) equivalent von Mises stress contour, legend+units (6) equivalent total strain contour, legend+units (7) total deformation contour, units, deformation scale (8) directional axial deformation (9) instructor-style chart (10) engineering curve with red yield dot if determined (11) Workbench model and solve status (12) mesh convergence graph. Capture relevant load increment/time and include the number in screenshot filename/metadata.

Output paths:
- `FINALUPLAD_Folder/Cases/{case_id}/Screenshots/`
- `.../Plots/` png/pdf/svg/CSV
- `.../Raw_Data/` history CSV, local extrema, nodal/element exports where available
- `.../Mesh_Convergence/` mesh snapshots, stats, metrics, solver logs
- `.../Reports/` case report, parameters YAML/JSON, warnings
- `FINALUPLAD_Folder/Workbench_Projects/{case_id}.wbpj` + `{case_id}_files/`
- `FINALUPLAD_Folder/Workbench_Archives/{case_id}.wbpz`
- `FINALUPLAD_Folder/Excel/AM_Project3_Eight_Case_Validation.xlsx`
- `FINALUPLAD_Folder/Comparisons/` all overlays and summary plots
- `FINALUPLAD_Folder/Reports/` combined results, ranked decision, methodology, missing/failed report
- `FINALUPLAD_Folder/Logs/` status, machine-readable manifest, ANSYS and Python logs

Workbenches save FIRST through File > Save, then File > Archive; use verified API or exact manual steps. A `.wbpj` without `_files` is incomplete. If archive cannot be produced, log failure. Screenshot export must be from actual ANSYS interface/solver results; if headless capture cannot be automated, provide exact manual procedure and mark screenshot pending. Avoid including temporary `.lock` files as validated deliverables. Create a final all-deliverables ZIP only AFTER verifying source deliverables; include a manifest and checksums. Do not rename or overwrite results silently.
