# Status log (updated by Claude Code)
## Stage 1 — environment & input audit (2026-11-18) — DONE
- ANSYS 2025 R1 (v251) installed; license server reachable; Workbench batch (`RunWB2 -B -R`) and Mechanical scripting (`model.SendCommand`) verified by real runs.
- Python 3.14 + numpy/matplotlib/openpyxl installed for post-processing. SolidWorks installed but **no SolidWorks COM automation was run** (mass properties not extracted from SolidWorks).
- CAD inputs found: 3 designs (BCCZ rho26, Fluorite rho49, Octet). **Design_04: BLOCKED (no files).** `BCCZ_..._2024.SLDPRT` is 0 bytes (unusable); `~$` lock file ignored.
- Provided CAD are **6 x 6 x 6 mm single unit cells**, not 30–40 mm specimens: assignment constraints (L/W 30–40, H 15–20, >100 cells) are NOT demonstrated; simulations are unit-cell level. Free lateral boundaries (no periodic BC).
- Material: Tough 2000 imported from XML into Engineering Data and assigned to all bodies (verified in Mechanical log). Density not in XML: 1.20 g/cm3 sourced (Formlabs white paper, V1 post-cured) — unverified for this resin version.
- Mapping (needs human confirmation): Design_01=BCCZ, Design_02=Fluorite, Design_03=Octet (alphabetical).
## Stage 2 — Design_03 (Octet) — DONE (3 mesh levels, nonlinear, displacement-controlled 0.9 mm = 15 % strain)
See Reports/Design_03_validation.md.
## Stage 3 — Design_01/02 — IN PROGRESS (see below, updated at end)
