"""Post-process REAL ANSYS Mechanical histories for the 8-case study. No synthetic data.
Usage: python scripts/postprocess8.py [tag=v1]
Reads  FINALUPLAD_Folder/Cases/<folder>/Raw_Data/<tag>/raw_history_L*.csv (+ geometry_probe.csv, mesh_metrics.csv)
Writes plots (png 300dpi/pdf/svg), CSVs, per-case JSON, comparison plots, results_summary_<tag>.json
"""
import os, sys, csv, glob, json, shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(PKG, "FINALUPLAD_Folder")
TAG = sys.argv[1] if len(sys.argv) > 1 else "v6"
CASE_FILTER = sys.argv[2] if len(sys.argv) > 2 else None   # e.g. BCCZ_Topo_Optimized
SUF = "_" + TAG if TAG != "v1" else ""
WARN = ""
OFFSET = 0.002; NFIT = 2
DISP_MM = float(os.environ.get("DISP_MM", "0.9"))   # must match the solve (v6s: 0.42)
CASES = json.load(open(os.path.join(PKG, "config", "cases_resolved.json")))
PAIRS = [("BCCZ_Original", "BCCZ_Topo_Optimized"), ("Cube_Original", "Cube_Topo_Optimized"),
         ("Fluorite_Truss_Original", "Fluorite_Truss_Topo_Optimized"), ("Octet_Truss_Original", "Octet_Truss_Topo_Optimized")]
COL = {"BCCZ": "#1f77b4", "Cube": "#7f7f7f", "Fluorite_Truss": "#2ca02c", "Octet_Truss": "#9467bd"}


def load_csv(p):
    r = list(csv.reader(open(p)))
    hdr = r[0]
    n = 4 if "solution_status" in hdr else len(hdr)
    return hdr, np.array([[float(x) for x in row[:n]] for row in r[1:] if row], dtype=float)


def yield_offset(eps, sig):
    n = min(NFIT, len(eps) - 1)
    e0, s0 = eps[1:1 + n], sig[1:1 + n]
    E = float(np.sum(e0 * s0) / np.sum(e0 * e0))
    res = dict(E_eff=E, reached=False, sigma_y=None, eps_y=None, idx=None,
               method="0.2%% strain offset on initial effective slope (secant of first %d increments)" % n)
    f = sig - E * (eps - OFFSET)
    for i in range(1, len(eps)):
        if f[i] <= 0 < f[i - 1] or (f[i] <= 0 and i == 1):
            t = f[i - 1] / (f[i - 1] - f[i]) if f[i - 1] != f[i] else 0
            res.update(reached=True, sigma_y=float(sig[i - 1] + t * (sig[i] - sig[i - 1])),
                       eps_y=float(eps[i - 1] + t * (eps[i] - eps[i - 1])), idx=float(i - 1 + t)); break
    pk = None
    for i in range(1, len(sig) - 1):
        if sig[i] >= sig[i - 1] and sig[i] > sig[i + 1]:
            pk = (float(eps[i]), float(sig[i])); break
    res["first_peak"] = pk
    return res


def save_all(fig, base):
    os.makedirs(os.path.dirname(base), exist_ok=True)
    if WARN: fig.text(0.5, -0.07, WARN, ha="center", fontsize=8, color="red", fontweight="bold")
    for ext in ("png", "pdf", "svg"):
        fig.savefig("%s.%s" % (base, ext), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def style(ax, xl, yl, title):
    ax.set_xlabel(xl, fontweight="bold"); ax.set_ylabel(yl, fontweight="bold"); ax.set_title(title, fontsize=9)
    ax.grid(True, alpha=.25); ax.set_xlim(left=0); ax.set_ylim(bottom=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)


def eng_plot(c, eps, sig, y, ml, base):
    fig, ax = plt.subplots(figsize=(8.2, 5))
    ax.plot(eps, sig, "-o", color="#c00000", ms=3, lw=1.6, label="Engineering stress-strain (ANSYS: |F|/A_full vs u/H0)")
    style(ax, "Engineering strain [mm/mm]", "Engineering stress [MPa]", "%s\nTough 2000 | displacement-controlled -Y compression | %s" % (c["folder"], ml))
    if y["reached"]:
        ax.set_ylim(0, sig.max() * 1.15)
        xl = np.array([OFFSET, eps.max()]); ax.plot(xl, y["E_eff"] * (xl - OFFSET), "--", color="gray", lw=1, label="0.2%% offset line (E_eff=%.1f MPa)" % y["E_eff"])
        ax.plot([y["eps_y"]], [y["sigma_y"]], "o", color="red", ms=13, mec="darkred", mew=1.5, zorder=5, label="Yield (0.2%% offset): %.3f MPa at strain %.5f" % (y["sigma_y"], y["eps_y"]))
        ax.annotate("Yield = %.3f MPa; strain = %.5f mm/mm" % (y["sigma_y"], y["eps_y"]), xy=(y["eps_y"], y["sigma_y"]),
                    xytext=(y["eps_y"] + 0.12 * eps.max(), y["sigma_y"] * 0.4), fontsize=11, bbox=dict(boxstyle="square", fc="#d9d9d9", ec="none"),
                    arrowprops=dict(arrowstyle="-|>", color="red", lw=2.5, mutation_scale=20))
    else:
        ax.text(.5, .5, "YIELD NOT IDENTIFIED — NO VALIDATED POINT (no 0.2%% offset intersection within %.1f%% strain)" % (100 * eps.max()), transform=ax.transAxes, ha="center", color="red", fontsize=11, bbox=dict(fc="white", ec="red"))
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    fig.text(0.01, -0.03, "Method: %s. Source: ANSYS Mechanical 2025 R1 nonlinear solve." % y["method"].replace("%%", "%"), fontsize=6.5)
    save_all(fig, base)


def local_plot(c, e_max, s_max, y, base, ml):
    fig, ax = plt.subplots(figsize=(8.2, 5))
    ax.plot(e_max, s_max, "-o", color="#c00000", ms=3, lw=1.6, label="Max equivalent stress vs max equivalent total strain (ANSYS)")
    style(ax, "Maximum Equivalent Total Strain [mm/mm]", "Maximum Equivalent (von Mises) Stress [MPa]", "%s | tutorial-style local-maximum plot | %s" % (c["folder"], ml))
    if y["reached"]:
        e_i = float(np.interp(y["idx"], np.arange(len(e_max)), e_max)); s_i = float(np.interp(y["idx"], np.arange(len(s_max)), s_max))
        ax.plot([e_i], [s_i], "o", color="red", ms=13, mec="darkred", mew=1.5, zorder=5, label="Increment of ENGINEERING yield: local maxima %.2f MPa, %.5f" % (s_i, e_i))
        ax.annotate("Increment at engineering yield\n(local maxima, not engineering values)", xy=(e_i, s_i), xytext=(e_i + 0.15 * e_max.max(), s_i * 0.5), fontsize=9,
                    bbox=dict(boxstyle="square", fc="#d9d9d9", ec="none"), arrowprops=dict(arrowstyle="-|>", color="red", lw=2.5, mutation_scale=20))
    else:
        ax.text(.5, .5, "YIELD NOT IDENTIFIED", transform=ax.transAxes, ha="center", color="red", fontsize=13, bbox=dict(fc="white", ec="red"))
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    fig.text(0.01, -0.02, "Maxima occur at different mesh locations; not a constitutive curve.", fontsize=7)
    save_all(fig, base)


def mesh_plot(c, lv, base):
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
    ne = [r["elements"] for r in lv]
    ax[0].plot(ne, [r["E_eff"] for r in lv], "-o", color="#c00000"); ax[0].set_ylabel("E_eff [MPa]")
    ax[1].plot(ne, [r["sigma_y"] if r["sigma_y"] else np.nan for r in lv], "-o", color="#c00000"); ax[1].set_ylabel("Engineering yield [MPa]")
    ax[2].plot(ne, [r["Fmax"] for r in lv], "-o", color="#c00000"); ax[2].set_ylabel("Peak reaction force [N]")
    for a in ax: a.set_xlabel("Elements"); a.grid(alpha=.25)
    fig.suptitle("%s | mesh convergence (%d levels)" % (c["folder"], len(lv)), fontsize=10)
    save_all(fig, base)


def get_mesh(sd, folder, tg, nfiles):
    """mesh rows [level,size,nodes,elements]; mesh_metrics.csv if present, else parse per-level log lines; mesh_extra.csv rows (documented provenance) appended."""
    import re
    rows = []
    p = os.path.join(sd, "mesh_metrics.csv")
    if os.path.exists(p): rows = [list(r[:4]) for r in load_csv(p)[1]]
    else:
        lg = os.path.join(F, "Logs", "%s_%s_mech.log" % (folder, tg))
        for ln in (open(lg, errors="ignore") if os.path.exists(lg) else []):
            m_ = re.search(r"LEVEL (\d+) size=([\d.]+) nodes=(\d+) elements=(\d+)", ln)
            if m_: rows.append([float(x) for x in m_.groups()])
    pe = os.path.join(sd, "mesh_extra.csv")
    if os.path.exists(pe): rows += [list(r[:4]) for r in load_csv(pe)[1]]
    if len(rows) < nfiles: raise RuntimeError("mesh rows %d < history files %d in %s" % (len(rows), nfiles, sd))
    return np.array(rows, dtype=float)


def chg(a, b): return abs(a - b) / abs(b) if (a is not None and b not in (None, 0)) else None


def process_case(c):
    tg = TAG
    if TAG == "v1":
        for cand in ("v6", "v5", "v4", "v3", "v2"):
            if glob.glob(os.path.join(F, "Cases", c["folder"], "Raw_Data", cand, "raw_history_L*.csv")) and os.path.exists(os.path.join(F, "Cases", c["folder"], "Raw_Data", cand, "mesh_metrics.csv")): tg = cand; break
    sd = os.path.join(F, "Cases", c["folder"], "Raw_Data", tg)
    files = sorted(glob.glob(os.path.join(sd, "raw_history_L*.csv")))
    if not files: return None
    gp = load_csv(os.path.join(sd, "geometry_probe.csv"))[1][0]
    Lx, Ly, Lz, vol = gp[:4]; A = Lx * Ly; H0 = Lz
    mm = get_mesh(sd, c["folder"], tg, len(files))
    levels = []
    for i, fp in enumerate(files):
        arr = load_csv(fp)[1]
        valid = (arr[:, 1] > 0) | (arr[:, 0] == 0)           # unsolved increments are written as zeros by the extractor -> exclude
        trunc = None if valid.all() else float(arr[valid, 0].max())
        t, smax, savg, emax, dzmin, Fz, tdmax = arr[valid].T
        u = t * DISP_MM; Fa = np.abs(Fz); eps = u / H0; sig = Fa / A
        y = yield_offset(eps, sig)
        levels.append(dict(trunc=trunc, level=i + 1, size=float(mm[i][1]), nodes=int(mm[i][2]), elements=int(mm[i][3]), E_eff=y["E_eff"], sigma_y=y["sigma_y"], eps_y=y["eps_y"],
                           F_y=(y["sigma_y"] * A if y["reached"] else None), Keff=float(Fa[1] / u[1]), Fmax=float(Fa.max()), y=y, t=t, u=u, F=Fa, eps=eps, sig=sig, smax=smax, emax=emax))
    fin = levels[-1]; prev = levels[-2] if len(levels) > 1 else None
    cE = chg(fin["E_eff"], prev["E_eff"]) if prev else None; cY = chg(fin["sigma_y"], prev["sigma_y"]) if prev else None
    cK = chg(fin["Keff"], prev["Keff"]) if prev else None
    conv = bool(cE is not None and cY is not None and cE < .02 and cY < .02 and cK is not None and cK < .02)
    global WARN
    WARN = "" if conv else "WARNING: mesh NOT converged (<2%% on E_eff, yield, K between last two levels not met) - PARTIAL" if False else ("" if conv else "WARNING: mesh NOT converged (needs <2% change on E_eff, yield and stiffness between last two levels) - PARTIAL")
    ml = "final mesh L%d (%.2f mm, %d elem, %d levels)" % (fin["level"], fin["size"], fin["elements"], len(levels))
    pd_ = os.path.join(F, "Cases", c["folder"], "Plots")
    base = os.path.join(pd_, "%s_ENGINEERING_STRESS_STRAIN_YIELD%s" % (c["folder"], SUF))
    eng_plot(c, fin["eps"], fin["sig"], fin["y"], ml, base)
    local_plot(c, fin["emax"], fin["smax"], fin["y"], os.path.join(pd_, "%s_equivalent_max_stress_strain_yield%s" % (c["folder"], SUF)), ml)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(fin["u"], fin["F"], "-o", color="#c00000", ms=3, label="Reaction force vs top displacement (ANSYS)")
    style(ax, "Top displacement |u_y| [mm]", "Reaction force |F_y| [N]", "%s | force-displacement | %s" % (c["folder"], ml))
    if fin["y"]["reached"]:
        ax.plot([fin["y"]["eps_y"] * H0], [fin["F_y"]], "o", color="red", ms=12, mec="darkred", zorder=5, label="Yield: F=%.1f N" % fin["F_y"])
    ax.legend(frameon=False); save_all(fig, os.path.join(pd_, "%s_force_displacement%s" % (c["folder"], SUF)))
    mesh_plot(c, levels, os.path.join(pd_, "%s_mesh_convergence%s" % (c["folder"], SUF)))
    mesh_plot(c, levels, os.path.join(F, "Cases", c["folder"], "Mesh_Convergence", "%s_mesh_convergence%s" % (c["folder"], SUF)))
    rd = sd   # v6: CSVs go beside the tagged raw histories (never touch older tags)
    def wcsv(nm, hdr, rows):
        with open(os.path.join(rd, nm), "w", newline="") as f:
            w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
    wcsv("force_displacement.csv", ["time", "top_displacement_mm", "reaction_force_N", "source"], [[a, b, d, "ANSYS measured, final mesh"] for a, b, d in zip(fin["t"], fin["u"], fin["F"])])
    wcsv("engineering_stress_strain.csv", ["time", "eng_strain", "eng_stress_MPa", "A_full_mm2", "H0_mm"], [[a, b, d, A, H0] for a, b, d in zip(fin["t"], fin["eps"], fin["sig"])])
    wcsv("equivalent_max_history.csv", ["time", "max_eqv_stress_MPa", "max_eqv_total_strain"], [[a, b, d] for a, b, d in zip(fin["t"], fin["smax"], fin["emax"])])
    wcsv("mesh_convergence.csv", ["level", "size_mm", "nodes", "elements", "E_eff_MPa", "Keff_N_per_mm", "Fmax_N", "yield_MPa", "yield_strain", "yield_force_N"],
         [[r["level"], r["size"], r["nodes"], r["elements"], r["E_eff"], r["Keff"], r["Fmax"], r["sigma_y"], r["eps_y"], r["F_y"]] for r in levels])
    lg = os.path.join(F, "Logs", "%s_%s_mech.log" % (c["folder"], tg))
    if os.path.exists(lg): shutil.copy(lg, os.path.join(rd, "solver.log"))
    s = dict(status="SOLVED_CONVERGED" if conv else "SOLVED_UNCONVERGED", Lx=Lx, Ly=Ly, Lz=Lz, vol=vol, A=A, H0=H0, RD=vol / (Lx * Ly * Lz), E_eff=fin["E_eff"], Keff=fin["Keff"],
             yield_reached=fin["y"]["reached"], sigma_y=fin["sigma_y"], eps_y=fin["eps_y"], F_y=fin["F_y"], Fmax=fin["Fmax"], max_eng_stress=float(fin["sig"].max()), first_peak=fin["y"]["first_peak"],
             truncated_at_time=fin['trunc'], conv_E=cE, conv_y=cY, conv_K=cK, elements=fin["elements"], nlevels=len(levels), finest_size=fin["size"], method=fin["y"]["method"], tag=tg,
             levels=[{k: r[k] for k in ("level", "size", "nodes", "elements", "E_eff", "Keff", "Fmax", "sigma_y", "eps_y", "F_y")} for r in levels],
             _curve=dict(eps=fin["eps"].tolist(), sig=fin["sig"].tolist(), smax=fin["smax"].tolist(), emax=fin["emax"].tolist()))
    json.dump({k: v for k, v in s.items() if k != "_curve"}, open(os.path.join(F, "Cases", c["folder"], "Reports", "case_results_%s.json" % TAG), "w"), indent=1, default=str)
    return s


def comparisons(S):
    cd = os.path.join(F, "Comparisons"); os.makedirs(cd, exist_ok=True)
    ok = [c for c in CASES if c["case_id"] in S and S[c["case_id"]]]
    def dsg(cid): return cid.split("_Original")[0].split("_Topo")[0]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for c in ok:
        s = S[c["case_id"]]; col = COL[dsg(c["case_id"])]; ls = "-" if "Original" in c["case_id"] else "--"
        ax.plot(s["_curve"]["eps"], s["_curve"]["sig"], ls, color=col, lw=1.7, label=c["folder"])
        if s["yield_reached"]: ax.plot([s["eps_y"]], [s["sigma_y"]], "o", color="red", ms=10, mec="black", zorder=5)
    ax.plot([], [], "o", color="red", mec="black", label="0.2% offset yield")
    style(ax, "Engineering strain [mm/mm]", "Engineering stress [MPa]", "Eight-case engineering stress-strain comparison (solved cases only; others BLOCKED/PENDING per status)")
    ax.legend(fontsize=7, frameon=False); save_all(fig, os.path.join(cd, "COMPARISON_8_CASES_stress_strain"))
    for o, t in PAIRS:
        if o in S and t in S and S[o] and S[t]:
            fig, ax = plt.subplots(figsize=(8, 5))
            for cid, ls in ((o, "-"), (t, "--")):
                s = S[cid]; ax.plot(s["_curve"]["eps"], s["_curve"]["sig"], ls, color=COL[dsg(cid)], lw=2, label=cid)
                if s["yield_reached"]: ax.plot([s["eps_y"]], [s["sigma_y"]], "o", color="red", ms=11, mec="black", zorder=5)
            style(ax, "Engineering strain [mm/mm]", "Engineering stress [MPa]", "Pair: %s vs %s" % (o, t)); ax.legend(frameon=False)
            save_all(fig, os.path.join(cd, "PAIR_%s_vs_Topo_stress_strain" % dsg(o)))
    rk = [(c, S[c["case_id"]]) for c in ok if S[c["case_id"]]["yield_reached"]]
    if rk:
        vals = [(c["folder"], s["sigma_y"] / s["RD"], s["status"]) for c, s in rk]
        vals.sort(key=lambda x: -x[1])
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.bar([v[0].replace("_", "\n", 1) for v in vals], [v[1] for v in vals], color=["#2ca02c" if v[2] == "SOLVED_CONVERGED" else "#ff7f0e" for v in vals])
        for i, v in enumerate(vals): ax.text(i, v[1], "%.1f" % v[1], ha="center", va="bottom", fontsize=8)
        ax.set_ylabel("Engineering yield / relative density [MPa]"); ax.set_title("Ranking (green = mesh-converged, orange = UNCONVERGED; literature validation pending)", fontsize=9)
        plt.setp(ax.get_xticklabels(), fontsize=6)
        for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
        save_all(fig, os.path.join(cd, "COMPARISON_8_CASES_yield_to_relative_density"))


def main():
    S = {}
    for c in CASES:
        if CASE_FILTER and c["case_id"] != CASE_FILTER: continue
        try: S[c["case_id"]] = process_case(c)
        except Exception as e:
            import traceback; print("FAIL", c["case_id"], traceback.format_exc()); S[c["case_id"]] = None
    if not CASE_FILTER: comparisons(S)
    clean = {k: ({kk: vv for kk, vv in v.items() if kk != "_curve"} if v else None) for k, v in S.items()}
    json.dump(clean, open(os.path.join(F, "Reports", "results_summary_%s.json" % TAG), "w"), indent=1, default=str)
    json.dump(S, open(os.path.join(F, "Reports", "_results_with_curves_%s.json" % TAG), "w"), default=str)
    for k, v in clean.items():
        print(k, None if not v else {kk: v[kk] for kk in ("status", "RD", "E_eff", "sigma_y", "eps_y", "conv_E", "conv_y", "conv_K", "elements")})


if __name__ == "__main__":
    main()
