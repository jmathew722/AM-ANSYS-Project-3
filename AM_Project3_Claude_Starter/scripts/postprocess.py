"""Post-process REAL ANSYS Mechanical histories into engineering stress-strain, yield, plots, CSVs.
Never synthesises data: every number comes from OUTPUTS_Folder/Simulation_Data/<design>/<tag>/raw_history_L*.csv
Usage: python scripts/postprocess.py [tag]   (default tag = v1)
"""
import os, sys, csv, glob, json, shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "OUTPUTS_Folder")
TAG = sys.argv[1] if len(sys.argv) > 1 else "v1"
OFFSET = 0.002          # 0.2 % strain offset (documented yield definition)
NFIT = 2                # initial points used for effective modulus (through origin)

DESIGNS = {
    "Design_01": dict(name="BCCZ_Topo_Smooth_6mm_rho26", color="#c00000"),
    "Design_02": dict(name="Fluorite_Topo_Smooth_6mm_rho49", color="#c00000"),
    "Design_03": dict(name="Octet_Truss_Smooth (Octet Truss Optimized 2025)", color="#c00000"),
    "Design_04": dict(name="BLOCKED - no CAD supplied", color="#c00000"),
}
DISP = {"Design_01": 0.9, "Design_02": 0.9, "Design_03": 0.9, "Design_04": 0.9}
CMP_COLORS = {"Design_01": "#1f77b4", "Design_02": "#2ca02c", "Design_03": "#9467bd", "Design_04": "#7f7f7f"}


def load_csv(p):
    with open(p) as f:
        r = list(csv.reader(f))
    hdr = r[0]
    a = np.array([[float(x) for x in row[:4 if "solution_status" in hdr else len(row)]] for row in r[1:] if row], dtype=float)
    return hdr, a


def yield_offset(eps, sig):
    """0.2 % offset yield on the effective initial slope. Returns dict (never fabricates)."""
    n = min(NFIT, len(eps) - 1)
    e0, s0 = eps[1:1 + n], sig[1:1 + n]
    E = float(np.sum(e0 * s0) / np.sum(e0 * e0))
    res = dict(E_eff=E, reached=False, sigma_y=None, eps_y=None, idx=None, method="0.2%% strain offset on initial effective slope (secant of first %d increments)" % n)
    f = sig - E * (eps - OFFSET)
    for i in range(1, len(eps)):
        if f[i] <= 0 < f[i - 1] or (f[i] <= 0 and i == 1):
            t = f[i - 1] / (f[i - 1] - f[i]) if f[i - 1] != f[i] else 0
            e = eps[i - 1] + t * (eps[i] - eps[i - 1]); s = sig[i - 1] + t * (sig[i] - sig[i - 1])
            res.update(reached=True, sigma_y=float(s), eps_y=float(e), idx=float(i - 1 + t))
            break
    # first local maximum (peak) as secondary indicator
    pk = None
    for i in range(1, len(sig) - 1):
        if sig[i] >= sig[i - 1] and sig[i] > sig[i + 1]:
            pk = (float(eps[i]), float(sig[i])); break
    res["first_peak"] = pk
    return res


def save_all(fig, base):
    os.makedirs(os.path.dirname(base), exist_ok=True)
    for ext in ("png", "pdf", "svg"):
        fig.savefig("%s.%s" % (base, ext), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def style(ax, xl, yl, title):
    ax.set_xlabel(xl, fontweight="bold"); ax.set_ylabel(yl, fontweight="bold")
    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=.25); ax.set_xlim(left=0); ax.set_ylim(bottom=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)


def eng_plot(d, did, name, eps, sig, y, mesh_label, base):
    fig, ax = plt.subplots(figsize=(8.2, 5))
    ax.plot(eps, sig, "-o", color="#c00000", ms=3, lw=1.6, label="Engineering stress-strain (ANSYS, F/A_full vs u/H0)")
    style(ax, "Engineering strain [mm/mm]", "Engineering stress [MPa]",
          "%s | %s | Tough 2000 | displacement-controlled -Z compression | %s | MPa, mm/mm" % (did, name, mesh_label))
    if y["reached"]:
        ax.plot([y["eps_y"]], [y["sigma_y"]], "o", color="red", ms=13, mec="darkred", mew=1.5, zorder=5,
                label="Yield (0.2%% offset): %.3f MPa at strain %.5f" % (y["sigma_y"], y["eps_y"]))
        xl = np.array([OFFSET, eps.max()]); ax.plot(xl, y["E_eff"] * (xl - OFFSET), "--", color="gray", lw=1, label="0.2%% offset line (E_eff = %.1f MPa)" % y["E_eff"])
        ax.set_ylim(0, sig.max() * 1.15)
        ax.annotate("Yield = %.3f MPa; strain = %.5f mm/mm" % (y["sigma_y"], y["eps_y"]),
                    xy=(y["eps_y"], y["sigma_y"]), xytext=(y["eps_y"] + 0.12 * eps.max(), y["sigma_y"] * 0.45 + 0.02 * sig.max()),
                    fontsize=11, bbox=dict(boxstyle="square", fc="#d9d9d9", ec="none"),
                    arrowprops=dict(arrowstyle="-|>", color="red", lw=2.5, mutation_scale=20))
    else:
        ax.text(0.5, 0.5, "YIELD NOT REACHED — NO VALIDATED POINT", transform=ax.transAxes, ha="center", fontsize=14, color="red",
                bbox=dict(fc="white", ec="red"))
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    fig.text(0.01, -0.02, "Method: sigma=|Fz|/(L*W) full outer footprint, eps=|uz|/H0; yield = %s. Source: ANSYS Mechanical 2025 R1 nonlinear solve." % y["method"], fontsize=6.5)
    save_all(fig, base)


def local_plot(did, name, e_max, s_max, y, t, base, mesh_label):
    fig, ax = plt.subplots(figsize=(8.2, 5))
    ax.plot(e_max, s_max, "-o", color="#c00000", ms=3, lw=1.6, label="Max equivalent stress vs max equivalent total strain (ANSYS)")
    style(ax, "Maximum Equivalent Total Strain [mm/mm]", "Maximum Equivalent (von Mises) Stress [MPa]",
          "%s | %s | Tough 2000 | tutorial-style local-maximum plot | %s" % (did, name, mesh_label))
    if y["reached"]:
        e_i = float(np.interp(y["idx"], np.arange(len(e_max)), e_max)); s_i = float(np.interp(y["idx"], np.arange(len(s_max)), s_max))
        ax.plot([e_i], [s_i], "o", color="red", ms=13, mec="darkred", mew=1.5, zorder=5, label="Increment of engineering yield (local maxima there: %.2f MPa, %.5f)" % (s_i, e_i))
        ax.annotate("Increment at engineering yield\n(local maxima, NOT engineering values)", xy=(e_i, s_i), xytext=(e_i + 0.15 * e_max.max(), s_i * 0.5),
                    fontsize=9, bbox=dict(boxstyle="square", fc="#d9d9d9", ec="none"), arrowprops=dict(arrowstyle="-|>", color="red", lw=2.5, mutation_scale=20))
    else:
        ax.text(0.5, 0.5, "YIELD NOT REACHED — NO VALIDATED POINT", transform=ax.transAxes, ha="center", fontsize=13, color="red", bbox=dict(fc="white", ec="red"))
    ax.legend(loc="lower right", fontsize=8, frameon=False)
    fig.text(0.01, -0.02, "Maxima occur at different mesh locations; this is not a constitutive curve.", fontsize=7)
    save_all(fig, base)


def fu_plot(did, name, u, F, y, A, base):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(u, F, "-o", color="#c00000", ms=3, label="Reaction force vs top displacement (ANSYS)")
    style(ax, "Top displacement |u_z| [mm]", "Reaction force |F_z| [N]", "%s | %s | force-displacement" % (did, name))
    if y["reached"]:
        # force at yield from stress*A
        H0 = u.max() / eps_global_max(u, y)
        ax.plot([y["eps_y"] * H0_cache[did]], [y["sigma_y"] * A], "o", color="red", ms=12, mec="darkred", zorder=5, label="Yield: F=%.1f N" % (y["sigma_y"] * A))
    ax.legend(frameon=False); save_all(fig, base)


H0_cache = {}
def eps_global_max(u, y): return 1.0


def mesh_plot(did, name, lv, base):
    fig, ax = plt.subplots(1, 2, figsize=(9, 4))
    ne = [r["elements"] for r in lv]
    ax[0].plot(ne, [r["E_eff"] for r in lv], "-o", color="#c00000"); ax[0].set_xlabel("Elements"); ax[0].set_ylabel("E_eff [MPa]")
    ys = [r["sigma_y"] if r["sigma_y"] is not None else np.nan for r in lv]
    ax[1].plot(ne, ys, "-o", color="#c00000"); ax[1].set_xlabel("Elements"); ax[1].set_ylabel("Engineering yield [MPa]")
    for a in ax: a.grid(alpha=.25)
    fig.suptitle("%s | %s | mesh convergence (3 levels)" % (did, name), fontsize=10)
    save_all(fig, base)


def main():
    os.makedirs(os.path.join(OUT, "Reports"), exist_ok=True)
    summary = {}
    for did, cfg in DESIGNS.items():
        sd = os.path.join(OUT, "Simulation_Data", did, TAG)
        files = sorted(glob.glob(os.path.join(sd, "raw_history_L*.csv")))
        if not files:
            summary[did] = dict(status="BLOCKED" if did == "Design_04" else "NO_DATA")
            continue
        gp = load_csv(os.path.join(sd, "geometry_probe.csv"))[1][0]
        Lx, Ly, Lz, vol = gp[:4]
        A = Lx * Ly; H0 = Lz; H0_cache[did] = H0
        mm = load_csv(os.path.join(sd, "mesh_metrics.csv"))[1]
        levels = []
        for i, fpath in enumerate(files):
            hdr, h = load_csv(fpath)
            ok = h[:, 0] >= 0
            t, smax, savg, emax, dzmin, Fz, tdmax = h.T
            u = t * DISP.get(did, 0.9); F = np.abs(Fz)   # prescribed top displacement (exact BC); dz-min is NOT used (local nodes can move more)
            eps = u / H0; sig = F / A
            y = yield_offset(eps, sig)
            keff = float(F[1] / u[1]) if u[1] > 0 else float("nan")
            lv = dict(level=i + 1, size=mm[i][1], nodes=int(mm[i][2]), elements=int(mm[i][3]), E_eff=y["E_eff"], sigma_y=y["sigma_y"],
                      eps_y=y["eps_y"], F_y=(y["sigma_y"] * A if y["reached"] else None), Keff=keff, y=y, t=t, u=u, F=F, eps=eps, sig=sig, smax=smax, emax=emax)
            levels.append(lv)
        fin = levels[-1]
        # convergence
        def chg(a, b): return abs(a - b) / abs(b) if (a is not None and b not in (None, 0)) else None
        c_E = chg(levels[-1]["E_eff"], levels[-2]["E_eff"]) if len(levels) > 1 else None
        c_y = chg(levels[-1]["sigma_y"], levels[-2]["sigma_y"]) if len(levels) > 1 else None
        c_K = chg(levels[-1]["Keff"], levels[-2]["Keff"]) if len(levels) > 1 else None
        conv = (c_E is not None and c_y is not None and c_E < .02 and c_y < .02)
        mesh_label = "mesh L%d (%.2f mm, %d elem)" % (fin["level"], fin["size"], fin["elements"])
        pdir = os.path.join(OUT, "Plots", did)
        base = os.path.join(pdir, "%s_ENGINEERING_STRESS_STRAIN_YIELD" % did)
        eng_plot(did, did, cfg["name"], fin["eps"], fin["sig"], fin["y"], mesh_label, base)
        for ext in ("png", "pdf", "svg"):
            shutil.copy("%s.%s" % (base, ext), os.path.join(pdir, "engineering_stress_strain_yield.%s" % ext))
        local_plot(did, cfg["name"], fin["emax"], fin["smax"], fin["y"], fin["t"], os.path.join(pdir, "equivalent_max_stress_strain_yield"), mesh_label)
        # force-displacement
        fig, ax = plt.subplots(figsize=(8, 4.8))
        ax.plot(fin["u"], fin["F"], "-o", color="#c00000", ms=3, label="Reaction force vs top displacement (ANSYS)")
        style(ax, "Top displacement |u_z| [mm]", "Reaction force |F_z| [N]", "%s | %s | force-displacement | %s" % (did, cfg["name"], mesh_label))
        if fin["y"]["reached"]:
            ax.plot([fin["y"]["eps_y"] * H0], [fin["F_y"]], "o", color="red", ms=12, mec="darkred", zorder=5, label="Yield: F=%.1f N at u=%.4f mm" % (fin["F_y"], fin["y"]["eps_y"] * H0))
        ax.legend(frameon=False); save_all(fig, os.path.join(pdir, "force_displacement"))
        mesh_plot(did, cfg["name"], levels, os.path.join(pdir, "mesh_convergence"))
        mesh_plot(did, cfg["name"], levels, os.path.join(OUT, "Mesh_Convergence", "%s_mesh_convergence" % did))
        # per-design data
        dd = os.path.join(OUT, "Simulation_Data", did)
        with open(os.path.join(dd, "force_displacement.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["time", "top_displacement_mm", "reaction_force_N", "source"])
            for a, b, c in zip(fin["t"], fin["u"], fin["F"]): w.writerow([a, b, c, "ANSYS Mechanical measured (final mesh)"])
        with open(os.path.join(dd, "engineering_stress_strain.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["time", "eng_strain_mm_per_mm", "eng_stress_MPa", "A_full_mm2", "H0_mm", "source"])
            for a, b, c in zip(fin["t"], fin["eps"], fin["sig"]): w.writerow([a, b, c, A, H0, "computed from ANSYS reaction & displacement"])
        with open(os.path.join(dd, "equivalent_max_history.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["time", "max_equivalent_stress_MPa", "max_equivalent_total_strain_mm_per_mm", "source"])
            for a, b, c in zip(fin["t"], fin["smax"], fin["emax"]): w.writerow([a, b, c, "ANSYS Mechanical measured"])
        with open(os.path.join(dd, "mesh_metrics.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["level", "element_size_mm", "nodes", "elements", "E_eff_MPa", "Keff_N_per_mm", "yield_MPa", "yield_strain", "yield_force_N"])
            for r in levels: w.writerow([r["level"], r["size"], r["nodes"], r["elements"], r["E_eff"], r["Keff"], r["sigma_y"], r["eps_y"], r["F_y"]])
        lg = os.path.join(OUT, "Logs", "%s_%s_mech.log" % (did, TAG))
        if os.path.exists(lg): shutil.copy(lg, os.path.join(dd, "solver.log"))
        summary[did] = dict(status="SOLVED" + ("" if conv else "_UNCONVERGED"), Lx=Lx, Ly=Ly, Lz=Lz, vol=vol, A=A, H0=H0, RD=vol / (Lx * Ly * Lz),
                            E_eff=fin["E_eff"], sigma_y=fin["sigma_y"], eps_y=fin["eps_y"], F_y=fin["F_y"], Keff=fin["Keff"], yield_reached=fin["y"]["reached"],
                            first_peak=fin["y"]["first_peak"], conv_E=c_E, conv_y=c_y, conv_K=c_K, converged=bool(conv), elements=fin["elements"],
                            levels=[dict(level=r["level"], size=r["size"], nodes=r["nodes"], elements=r["elements"], E_eff=r["E_eff"], Keff=r["Keff"], sigma_y=r["sigma_y"], eps_y=r["eps_y"], F_y=r["F_y"]) for r in levels],
                            max_eng_stress=float(fin["sig"].max()), max_strain=float(fin["eps"].max()), method=fin["y"]["method"], tag=TAG)
        summary[did]["_curve"] = dict(eps=fin["eps"].tolist(), sig=fin["sig"].tolist(), u=fin["u"].tolist(), F=fin["F"].tolist(), t=fin["t"].tolist(), smax=fin["smax"].tolist(), emax=fin["emax"].tolist())
    # combined plots
    ok = [d for d in summary if summary[d].get("status", "").startswith("SOLVED")]
    if ok:
        fig, ax = plt.subplots(figsize=(8.5, 5.2))
        for d in ok:
            c = summary[d]["_curve"]; ax.plot(c["eps"], c["sig"], "-", color=CMP_COLORS[d], lw=1.8, label="%s (%s)" % (d, DESIGNS[d]["name"].split(" ")[0]))
            if summary[d]["yield_reached"]:
                ax.plot([summary[d]["eps_y"]], [summary[d]["sigma_y"]], "o", color="red", ms=11, mec="black", zorder=5)
        ax.plot([], [], "o", color="red", mec="black", label="0.2% offset yield")
        style(ax, "Engineering strain [mm/mm]", "Engineering stress [MPa]", "COMPARISON - validated-solve designs only (Design_04 BLOCKED: no CAD) | Tough 2000 | unit-cell level")
        ax.legend(fontsize=8, frameon=False); save_all(fig, os.path.join(OUT, "Plots", "COMPARISON_4_DESIGNS_stress_strain"))
        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        rk = [d for d in ok if summary[d]["yield_reached"]]
        vals = [summary[d]["sigma_y"] / summary[d]["RD"] for d in rk]
        order = np.argsort(vals)[::-1]
        ax.bar([rk[i] for i in order], [vals[i] for i in order], color=[CMP_COLORS[rk[i]] for i in order])
        for j, i in enumerate(order): ax.text(j, vals[i], "%.1f" % vals[i], ha="center", va="bottom")
        ax.set_ylabel("Engineering yield / relative density [MPa]"); ax.set_title("Yield ranking (PRELIMINARY: literature validation pending; Design_04 BLOCKED)", fontsize=9)
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        save_all(fig, os.path.join(OUT, "Plots", "COMPARISON_4_DESIGNS_yield_to_relative_density"))
    clean = {k: {kk: vv for kk, vv in v.items() if kk != "_curve"} for k, v in summary.items()}
    json.dump(clean, open(os.path.join(OUT, "Reports", "results_summary_%s.json" % TAG), "w"), indent=1, default=str)
    json.dump(summary, open(os.path.join(OUT, "Reports", "_results_with_curves_%s.json" % TAG), "w"), default=str)
    for k, v in clean.items(): print(k, {kk: v[kk] for kk in v if kk in ("status", "RD", "E_eff", "sigma_y", "eps_y", "F_y", "converged", "conv_E", "conv_y", "first_peak")})


if __name__ == "__main__":
    main()
