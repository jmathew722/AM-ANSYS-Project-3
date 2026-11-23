# 03. Checklists: mini report, final report, experiments

Tick items off as they are done. Deadlines are in `01_REQUIREMENTS_AND_DEADLINES.md`.

## A. 2-page mini report (instructor email, due "Monday", confirm the date)
- [ ] Confirm the date and whether it replaces or adds to the Nov 18 FEM summary.
- [ ] Table with yield strength, relative density and strength/density ratio for **all** designs (start from `02_STRENGTH_DENSITY_TABLE.md`).
- [ ] Stress-strain curve of each design (the 8 plots in `REPORT/`). Fit them on two pages (a 2 x 4 grid, or one combined plot plus the table).
- [ ] State the fully dense Tough 2000 FEM yield used as the reference (49.71 MPa from the solid cube) and the formulas.
- [ ] Say plainly which designs are provisional (2, 6, 8) and why.
- [ ] Check every strength/density ratio is below 1 and every relative density is between 0 and 1.

## B. FEM work
- [ ] Finish or label the unfinished simulations: Designs 2, 6, 8 (details in `CLAUDE.md`).
- [ ] **Validate the FEM against published results** for one design (PDF section 2.4). Find a paper with a comparable lattice and material, reproduce its loading, and report the percent difference. Currently NOT VALIDATED.
- [ ] Confirm yield uses engineering stress on the entire loaded-face area.
- [ ] Mesh convergence evidence for every design: at least 3 genuinely different meshes, under 2% change in stiffness and yield between the last two.
- [ ] Decide what to do about the early-stopped curves (Designs 1, 6, 7).

## C. Design checks (PDF section 2.3)
- [ ] Part dimensions within 30-40 x 30-40 x 15-20 mm for every design.
- [ ] More than 100 unit cells per part.
- [ ] Relative density below 50% for each printed design (Cube Topo is 46.7%, close to the limit; check the full printed part, not only the cell).
- [ ] Minimum feature size at least 0.2 mm for every design.
- [ ] Four different unit cell designs, two duplicates each. Confirm with the TA how Original vs Topo versions count.

## D. Printing and testing
- [ ] Confirm the Nov 18 EIH print submission (which 4 designs, which printer, project code AMEADDFA26) and that it is queued for Nov 25.
- [ ] Collect parts after Nov 25 and remove supports carefully.
- [ ] Weigh and measure each printed part; compute actual density (mass / total volume).
- [ ] Instron compression test of every part (8 parts if 4 designs x 2 duplicates) before 5 pm Dec 4. Book the machine early.
- [ ] Convert Instron force-displacement to engineering stress-strain with the same area convention as the FEM; find yield with the same 0.2% offset rule.
- [ ] Compare experiment with FEM: yield, stiffness, curve shape, failure mode. Discuss the gap (printing defects, anisotropy, unit cell vs full part, boundary conditions).

## E. Final report (noon Dec 7)
- [ ] 12 pt Times New Roman, 1 in margins, single spaced; correct page count for your level; captions below figures and above tables.
- [ ] Abstract (0.5 page).
- [ ] Introduction (1-2 pages, no figures): literature summary with at least 10 cited articles (undergraduate) or 20 (graduate).
- [ ] Results and discussion (3-5 pages): designs, FEM results with validation and convergence, experimental results, FEM vs experiment.
- [ ] Conclusions (0.5 page).
- [ ] References.
- [ ] Appendix: team roles and structure.
- [ ] 6-minute presentation, prepared for 2 minutes of questions.

## F. Open questions for the TA or instructor
- Is the solid-cube FEM run acceptable as the fully dense reference?
- Do Original and Topo versions of one unit cell count as different designs?
- Is the mini report due Monday Nov 23, and does it replace the Nov 18 summary?
- Undergraduate or graduate page and citation requirements?
