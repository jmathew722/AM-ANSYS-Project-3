# Pair comparison: Cube_Original vs Cube_Topo_Optimized

| metric | Original | Topo | change |
|---|---|---|---|
| solid volume mm3 (= mass ratio at equal density) | 216 | 100.8 | -53.3% |
| relative density | 1 | 0.4665 | -53.4% |
| E_eff MPa | 1163 | 466.6 | -59.9% |
| engineering yield MPa | 49.71 | 19.3 | -61.2% |
| yield strain | 0.04473 | 0.04337 | -3.0% |
| peak eng. stress in run MPa | 75.6 | 25.71 | -66.0% |
| elements (finest) | 3.93e+04 | 5.249e+04 | +33.5% |
| yield / RD MPa | 49.710 | 41.378 | -16.8% |

Mass saving (volume-based) = 53.3%; mass in grams needs a verified density.
Mesh status: original SOLVED_CONVERGED, topo SOLVED_CONVERGED.
Interpretation must consider that local von Mises concentration differs from effective response; see contour screenshots in each case folder and Comparisons/PAIR_* plots.
