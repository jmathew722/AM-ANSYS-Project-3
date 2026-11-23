# Design 2 (BCCZ_Topo_Optimized) mesh probe, tag probe6* (MESH_ONLY, patch-independent mesher, CaptureCurvature/Proximity off)
Run 2026-11-23 with scripts/mech_run_pi2.py. Geometry: 4840 faces, volume 56.74 mm3, compression axis Y.

| Tag | ElementSize (mm) | Extra settings | Nodes | Elements |
|---|---|---|---|---|
| probe6 | 3.0 | none | 475,105 | 321,561 |
| probe6 | 2.0 | none | 475,239 | 321,671 |
| probe6 | 1.2 | none | 475,095 | 321,552 |
| probe6b | 1.5 | MinimumSize 0.6 | 476,257 | 322,412 |
| probe6a | 1.0 | MinimumSize 0.3 | 591,272 | 405,373 |
| probe6c | 2.0 | MinimumSize 1.0, MaximumSize 2.0 | 591,450 | 405,512 |
| probe6d/e/f | 1.0 | AutomaticMeshBasedDefeaturing=True, tol 0.05/0.1/0.2, MinimumSize 0.1/0.2/0.4 | 591,272-591,287 | 405,373-405,384 (no effect) |
| probe6g | 0.8 | none | 495,925 | 338,107 |
| probe6h | 0.6 | none | 558,438 | 380,975 |
| probe6i | 0.45 | none | 588,933 | 406,456 |
| v4 L1 (existing) | 1.5 | none | 476,623 | 322,676 |

Result: no tested setting gives fewer than ~321k elements; the target of ~40k and ~120k elements is NOT reachable with this mesher on this CAD (small CAD faces set the surface mesh). Counts saturate near 405k at fine sizes. Defeaturing properties were accepted without error but changed nothing.
Element-quality logging failed (`MeshMetric` is not a defined name in this scope; no quality values recorded).
Cost: v4 level 1 history file was written ~4 h after launch (16:53 -> 21:01 on 2026-11-20), level 2 ~3 h 40 min later. One solve at this mesh size exceeds the 2.5 h budget, so no v6 coarse solves were run.
