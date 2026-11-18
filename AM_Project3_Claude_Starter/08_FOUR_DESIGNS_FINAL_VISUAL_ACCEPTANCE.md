# 08 — Final four-design plotting, screenshot and delivery contract

## Nonnegotiable scope
The project has EXACTLY **four distinct physical metamaterial designs**: Design_01, Design_02, Design_03, Design_04. For each, pair one verified SolidWorks file with the correct IGES source, record geometric hash and CAD volume to prevent mismatches, and use the exact Tough 2000 XML supplied. Do not invent design names/dimensions if filenames are absent; construct a manifest for human confirmation if ambiguous.

## Critical chart to recreate
Refer to `screenshots/reference_slides/REFERENCE_YIELD_GRAPH_RED_DOT.png`, an instructor *example*, NOT the user's data. Reproduce a clean, professional visual style without copying its sample numbers. The principal deliverable is each design's **effective engineering stress vs engineering strain** graph derived from verified reaction-force and original gross-area data; show a prominent **RED FILLED CIRCLE** at yield, with arrow and callout `Yield strength: XX.XXX MPa` and `Yield strain: 0.XXXXX mm/mm`. Use meaningful ticks beginning at zero, units, legend and methodology label. No forcing the chart to the example shape and no assuming 213 MPa. When yield is undefined, omit marker and add a conspicuous caption explaining why. Save PNG at 300dpi or greater, SVG, PDF, data CSV and figure-generation Python script. Additionally reproduce the tutorial-specific **maximum equivalent stress vs maximum equivalent total strain** curve with the same polished format and legitimate yield-step identification if possible. Stress and strain field maxima may be at different locations.

## Mandatory screenshot set PER DESIGN
`OUTPUTS_Folder/Screenshots/Design_XX/`:
- `01_solidworks_isometric.png` — actual SolidWorks model view if SolidWorks is accessible, otherwise CAD viewer screen named honestly
- `02_solidworks_mass_properties.png` — actual source-mass-properties panel when available; otherwise explicitly mark unavailable
- `03_ansys_geometry.png`
- `04_tough2000_assignment.png`
- `05_mesh.png`
- `06_fixed_support_and_loading.png`
- `07_total_deformation.png`
- `08_directional_deformation_z.png`
- `09_equivalent_stress_von_mises.png`
- `10_equivalent_total_strain.png`
- `11_mechanical_stress_strain_chart.png`
- `12_yield_annotation_chart.png` — actual window screenshot, not an exported Python figure disguised as screenshot
- additional fine-mesh contour screenshots as useful.
Screenshot filenames in manifest shall be marked `REAL_CAPTURE`, `EXPORTED_MECHANICAL_IMAGE`, or `NOT_AVAILABLE`. Never fake GUI screenshots or claim human-like desktop control is available unless verified.

## Per-design output files
- `OUTPUTS_Folder/Workbench_Projects/Design_XX.wbpj` and `Design_XX_files/`
- `OUTPUTS_Folder/Workbench_Archives/Design_XX.wbpz` (archive must contain intended solved state, or say otherwise)
- `OUTPUTS_Folder/Simulation_Data/Design_XX/force_displacement.csv`, `engineering_stress_strain.csv`, `equivalent_max_history.csv`, `mesh_metrics.csv`, `solver.log`
- `OUTPUTS_Folder/Plots/Design_XX/{engineering_stress_strain_yield,equivalent_max_stress_strain_yield,force_displacement,mesh_convergence}.{png,pdf,svg}`
- `OUTPUTS_Folder/Screenshots/Design_XX/` documented images
- `OUTPUTS_Folder/Reports/Design_XX_validation.md`

## Combined outputs
`OUTPUTS_Folder/Plots/COMPARISON_4_DESIGNS_stress_strain.png` (PDF/SVG), `COMPARISON_4_DESIGNS_yield_to_relative_density.png` (PDF/SVG), and `OUTPUTS_Folder/Excel/AM_Project3_Four_Design_FEM_Results.xlsx`. The Excel workbook must use linked formulas for mass, volume, porosity, full-face area, engineering yield strength and yield-strength/relative-density ratio, editable CAD/material inputs, yield marker numerical data, charts, mesh tables and a clear ranking of four *validated* designs. Four designs, no fifth-eighth phantom rows.

## Acceptance gates
1. Four distinct CAD-to-IGES matches and units/bounding boxes checked.
2. Tough 2000 full elastic and multilinear plasticity imported/assigned; no steel.
3. Every intended case solved or explicitly BLOCKED; no fake numerical data.
4. At least three increasingly refined meshes per feasible design; 2% changes in key output metrics a *target*, not a scientific guarantee.
5. Each design has correct bottom support and top compression along verified sign/direction; 1000 N ramp only as first pilot, not universal final load.
6. Each final yield value has a stated algorithm and valid point from converged solution history; give stress in MPa, strain in mm/mm; annotate the red dot on the engineering plot.
7. All expected per-design screenshots present OR specifically inventoried as unavailable with reason.
8. Four .wbpj+_files pairs and four .wbpz, or detailed blocker for each; no false assertions.
9. Verify all files exist, save SHA-256 manifest, produce a four-case pass/block/fail status table and two-page FEM summary.
