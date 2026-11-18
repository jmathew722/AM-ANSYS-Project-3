# 01 — Assignment requirements and geometry audit

**Governing PDF**: `reference/AME_40643_60643_Project3_requirements.pdf` pp. 1–3.

## Hard constraints (full printed design)
- Length 30–40 mm; width 30–40 mm; height 15–20 mm.
- **More than 100** unit cells (strict >100); **relative density <0.50** (porosity >50%).
- Minimum feature diameter/thickness **0.2 mm**.
- Team may print four different designs, with two duplicates each; distinct designs must have distinct unit-cell architectures. Do not invent designs or claim duplicates were tested.
- FEM must determine the **effective engineering stress at lattice yield**, compare designs, maximize yield strength / relative density, and validate one model against trustworthy literature before trusting predictions.
- Course requires a two-page FEM summary Nov 18, 5pm; four print designs Nov 18, 11pm; experimental testing Dec 4, 5pm; report Dec 7, noon (year 2026).

## CAD audit
For each pair of `.sldprt`/`.igs` (or `.iges`) files: identify variant, units, BREP solidness, connected volumes, visible geometry, unit cell type and count, feature minima, bounding box XYZ and actual compression axis. Extract SolidWorks **Mass Properties** (volume, mass, density if material assigned) through a verified SolidWorks COM/API workflow or manual report. If unavailable, use a documented geometric fallback and record it as estimated, not SolidWorks-extracted. Verify no assumptions based solely on file name.

Compute **envelope volume** = length × width × height in mm³; **solid volume** from CAD; **relative density** = solid volume/envelope volume; **porosity** = 100(1 - relative density)%; **gross loaded area** = outer width × depth perpendicular to compression. For non-cuboid or uneven footprints, define a justified reference envelope face and document it. CAD mass is only valid with correct physical **Tough 2000 density** assigned; XML has no density entry — obtain authoritative density or measured mass and record provenance. Mass[g] = solid volume[mm³] × density[g/cm³] /1000.

Provide annotated screenshots and a per-part PASS/FAIL table. Do not model production loads on a shell-only IGES without repair and verified meshing.
