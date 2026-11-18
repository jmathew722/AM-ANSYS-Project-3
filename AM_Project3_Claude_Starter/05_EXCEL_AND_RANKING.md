# 05 — Editable Excel, formulas, density and comparisons

Starter workbook `templates/AM_Project3_Editable_Calculations.xlsx` has editable input cells; copy/populate it into `OUTPUTS_Folder/Excel/`. It is a template, not output data. Populate design-by-design with verified CAD and ANSYS values. Design cells must be changeable without invalidating formulas.

Formulas required: `V_envelope=L×W×H`; `A_gross=L×W` on actual loading plane; `RD=V_solid/V_envelope`; `porosity_pct=100×(1-RD)`; `mass_g=V_solid(mm³)×rho(g/cm³)/1000`; `RD_by_mass=measured_mass_g×1000/(rho×V_envelope)` when density and mass known; `sigma_y=F_y/A_gross` in MPa when N/mm²; `ratio=sigma_y/RD` (MPa); `E_eff = (dF/du)×H/A_gross`. Validate positive denominator, proper units, source of each value.

Export a completed `.xlsx` with dashboard, design inputs, material properties and 21 hardening points, SolidWorks mass/volume, final results, each design's force-displacement and local/engineering stress-strain histories, yield method and red-marked point, mesh convergence, design-ranking comparison, checklist, solver/validation provenance and optional measured Instron data when available. Use editable Excel charts as well as exported high-quality Python charts. Blank absent data; never synthesize ANSYS response.

Apply explicit project constraints (L 30–40, W 30–40, H 15–20 mm, >100 unit cells, RD <0.5, minimum strut 0.2 mm). Sort designs by **validated** `engineering_yield_strength / relative_density`; do not include unverified results in a winning design recommendation.
