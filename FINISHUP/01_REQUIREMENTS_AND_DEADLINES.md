# 01. Project requirements and deadlines (AME 40643/60643 Project 3)

Source: `8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package/reference/AME_40643_60643_Project3_requirements.pdf` (read in full) plus the instructor's email about the strength/density ratio. Last checked 2026-11-22.

## Deadlines

| Date | Milestone | Status as of 2026-11-22 |
|---|---|---|
| Nov 4 | Literature review, 10 designs | Past |
| Nov 11 | Design review (>6 designs + preliminary FEM) | Past |
| 5 pm Nov 18 | 2-page summary of final FEM results | **Past.** Confirm what was submitted. |
| 11 pm Nov 18 | Submit 4 different designs to EIH for printing | **Past.** Confirm which 4 designs were submitted and that the jobs are in the queue. |
| Nov 25 | Finish printing | Upcoming |
| 5 pm Dec 4 | Finish mechanical testing (Instron) of all parts | Not started as far as the repo shows |
| noon Dec 7 | Written report and team presentation | Not started |
| "Monday" (assumed Nov 23; confirm) | 2-page mini report, per the instructor's email | See `02_STRENGTH_DENSITY_TABLE.md` and `03_REPORT_CHECKLISTS.md` |

Print code: AMEADDFA26. Print jobs go through the EIH portal (state the printer). EIH contact: Joseph Perri. TA: Philip Root. Both emails are in the PDF.

## Design requirements (PDF section 2.3)
- Part size: length 30-40 mm, width 30-40 mm, height 15-20 mm.
- More than 100 unit cells. A 6 mm cell at 36 x 36 x 18 mm gives 6 x 6 x 3 = 108, which passes; 5 x 5 x 3 = 75 fails.
- Relative density below 50%.
- 4 different designs, 2 duplicates of each. The unit cell designs must differ between designs. The repo's four families are BCCZ, Cube, Fluorite Truss and Octet Truss, each with an Original and a Topo version. Ask the TA whether the Original and Topo versions of one family count as different designs.
- Minimum feature size 0.2 mm. Not checked in the repo for any design.

## FEM requirements (PDF section 2.4)
- FEM may be done on one unit cell.
- **Validate the FEM against trustworthy literature results for one design.** The repo says NOT VALIDATED. Only a solid-cube elastic check exists (E_eff 1163 MPa vs analytic 1109.5 MPa, +4.9%).
- Yield strength = engineering stress at the yield point, using the **entire area of the loaded surface of the unit cell**.

## Testing requirements (PDF section 2.6)
- Instron: stress-strain curve and yield strength for each printed part.
- Measured density for every printed part (weight divided by total volume).
- The report must compare experiment with modeling and assess how well they agree.

## Instructor email: strength/density ratio
1. Run FEM on a **fully dense solid** of Tough 2000 to get its yield strength.
2. relative yield strength = lattice yield strength / solid yield strength.
3. strength/density ratio = relative yield strength / relative density.
4. Relative density must be between 0 and 1. The ratio must be below 1 for any lattice. A value above 1 means something is wrong.
5. The 2-page mini report needs a table (yield strength, relative density, strength/density ratio for all designs) and the stress-strain curve of each design.

## Report format (PDF section 4)
- Length: 5-6 pages (undergraduate teams) or 7-8 pages (graduate teams), including figures and tables, excluding references and appendix. Confirm which applies to you.
- 12 pt Times New Roman, 1 in margins, single spaced.
- Figures and tables embedded where discussed. Figure captions below, table captions above.

| Section | Length | Points |
|---|---|---|
| 1 Abstract | 0.5 page | 5 |
| 2 Introduction (no figures) | 1-2 pages | 15 |
| 3 Results and discussion | 3-5 pages | 70 |
| 4 Conclusions | 0.5 page | 5 |
| 5 References | | 5 |
| 6 Appendix: team roles and structure | | |

Introduction literature: undergraduates cite at least 10 articles with at least half a page of summary; graduates cite at least 20 with at least 1 page.

Section 3 breakdown: design quality and originality 15, technical soundness of FEM 25, experimental stress-strain and yield analysis 15, depth of technical discussion 15.

Presentation: 6 minutes plus 2 minutes of questions.
