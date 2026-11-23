# REPORTPNG: latest final figures per design (2026-11-23, branch FINALANSYS)
Copied unmodified from `8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package/FINALUPLAD_Folder/Cases/<design>/Plots/`. All curves are real ANSYS Mechanical 2025 R1 results (Tough 2000). Compression axis is Y for the BCCZ, topology and truss cells (older plot titles may say Z).

| Design | Folder status | Note |
|---|---|---|
| 01 BCCZ Original | converged, 4 levels | curve stops at t=0.68 |
| 02 BCCZ Topo | **PARTIAL (newest, tag v6c)** | 3 meshes 322.6k/380.9k/405.4k, yield 8.235 MPa @0.03664; mesh range only 26%; ANSYS contour screenshots included |
| 03 Cube Original | converged, 4 levels | solid cube, fully dense reference |
| 04 Cube Topo | converged, 4 levels | solved from SLDPRT (IGES surface-only) |
| 05 Fluorite Original | converged by 2% rule, 5 levels | |
| 06 Fluorite Topo | **NOT TRUSTWORTHY** | old tag v4: all mesh levels were the same ~34k mesh; not rerun |
| 07 Octet Original | converged, 5 levels | curve stops at t=0.5 |
| 08 Octet Topo | **NO RESULT** | no valid solve, no plots exist |

Comparison plots in `Comparisons/` pre-date the Design 2 rerun and include unrerun cases; treat as provisional.
