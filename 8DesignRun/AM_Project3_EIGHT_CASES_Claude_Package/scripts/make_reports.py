"""Per-case reports, pilot summaries, pair reports, final report, status, SHA-256 manifest. Usage: python scripts/make_reports.py"""
import os, json, glob, hashlib, csv, re, datetime
import numpy as np

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(PKG, "FINALUPLAD_Folder")
CASES = json.load(open(os.path.join(PKG, "config", "cases_resolved.json")))
SUM = json.load(open(os.path.join(F, "Reports", "results_summary_v1.json")))
SHOTS = ["03_ansys_geometry", "04_tough2000_assignment", "05_mesh", "06_fixed_support_and_loading", "07_total_deformation", "08_directional_deformation_z",
         "09_equivalent_stress_von_mises", "10_equivalent_total_strain", "11_mechanical_stress_strain_chart"]
NOTES = json.load(open(os.path.join(PKG, "config", "case_notes.json"))) if os.path.exists(os.path.join(PKG, "config", "case_notes.json")) else {}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()


def rd(p):
    r = list(csv.reader(open(p)))
    return r[0], np.array([[float(x) for x in row] for row in r[1:] if row])


def pilot(c):
    out = None
    for tg in ("pilot2", "pilotpi3", "pilotpi2", "pilot", "pilotsw"):
        p = os.path.join(F, "Cases", c["folder"], "Raw_Data", tg, "raw_history_L1.csv")
        if os.path.exists(p):
            gp = rd(os.path.join(F, "Cases", c["folder"], "Raw_Data", tg, "geometry_probe.csv"))[1][0]
            lg = os.path.join(F, "Logs", "%s_%s_mech.log" % (c["folder"], tg))
            axis = "?"
            if os.path.exists(lg):
                m = re.search(r"COMPRESSION AXIS = (\w)", open(lg).read()); axis = m.group(1) if m else "Z (pre-axis-verification script; tie-case)"
            _, h = rd(p); ok = (h[:, 1] > 0) | (h[:, 0] == 0); lost = None if ok.all() else float(h[ok, 0].max()); h = h[ok]; t, smax, savg, emax, dz, Fz, td = h.T
            A = gp[0] * gp[1]
            out = dict(tag=tg, axis=axis, F_end=float(abs(Fz[-1])), nominal_MPa=float(abs(Fz[-1]) / A), max_axial_def=float(abs(dz).max()), max_total_def=float(td.max()),
                       max_eqv_stress=float(smax.max()), eps_nominal=float(abs(dz).max() / gp[2]), substeps=len(t) - 1, lost_at=lost)
            break
    return out


def shotlist(c):
    d = os.path.join(F, "Cases", c["folder"], "Screenshots")
    rows = []
    for s in SHOTS:
        p = os.path.join(d, s + ".png")
        rows.append((s, "EXPORTED_MECHANICAL_IMAGE" if os.path.exists(p) and os.path.getsize(p) > 0 else "NOT_AVAILABLE"))
    rows.append(("SolidWorks/CAD isometric + mass-properties panels", "NOT_AVAILABLE (SolidWorks GUI automation not run)"))
    rows.append(("yield annotation chart as ANSYS window capture", "NOT_AVAILABLE (Python-generated plot supplied in Plots/; Mechanical chart image 11_* is the reaction history chart)"))
    return rows


def case_report(c):
    s = SUM.get(c["case_id"]); p = pilot(c); st = NOTES.get(c["case_id"], {})
    L = ["# %s — case report" % c["folder"], "", "**Status: %s**" % (s["status"] if s else st.get("status", "NOT SOLVED / BLOCKED")), ""]
    L += ["- IGES: `%s`  | SLDPRT: `%s`  | mapping: **%s**" % (os.path.basename(c["iges"]), os.path.basename(c["sldprt"]), c["mapping_status"])]
    if st.get("note"): L += ["- Note: " + st["note"]]
    if s:
        L += ["- Geometry (ANSYS import): footprint %.3f x %.3f mm, height along compression axis %.3f mm, solid volume %.3f mm3, relative density %.4f, A_full %.2f mm2" % (s["Lx"], s["Ly"], s["Lz"], s["vol"], s["RD"], s["A"]),
              "- Material: Tough 2000 (XML; E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density NOT in XML -> mass TBD",
              "- Loading: bottom fixed support, top face prescribed compressive displacement 0.9 mm in 60 substeps, large deflection ON; reaction from fixed support",
              "- Engineering stress = |F|/A_full, strain = u/H0.  Yield = %s" % s["method"].replace("%%", "%")]
        if s["yield_reached"]:
            L += ["- **Yield: %.4f MPa at strain %.5f mm/mm** (F_y = %.2f N); E_eff = %.2f MPa; yield/RD = %.3f MPa" % (s["sigma_y"], s["eps_y"], s["F_y"], s["E_eff"], s["sigma_y"] / s["RD"])]
        else:
            L += ["- **YIELD NOT IDENTIFIED** within the simulated strain range"]
        L += ["", "## Mesh convergence (%d levels; criterion <2%% for E_eff, yield and Keff between last two)" % s["nlevels"], "", "| level | size mm | elements | E_eff MPa | Keff N/mm | peak F N | yield MPa |", "|---|---|---|---|---|---|---|"]
        for lv in s["levels"]:
            L.append("| %d | %.2f | %d | %.3f | %.3f | %.1f | %s |" % (lv["level"], lv["size"], lv["elements"], lv["E_eff"], lv["Keff"], lv["Fmax"], "%.4f" % lv["sigma_y"] if lv["sigma_y"] else "n/a"))
        L += ["", "Last-two-level change: E_eff %.2f%%, yield %s, Keff %.2f%% -> **%s**" % (100 * s["conv_E"], "%.2f%%" % (100 * s["conv_y"]) if s["conv_y"] is not None else "n/a", 100 * s["conv_K"], "CONVERGED (<2%)" if s["status"] == "SOLVED_CONVERGED" else "NOT converged to 2%")]
    if p:
        L += ["", "## 1000 N pilot (force-ramped, tag %s, axis %s)" % (p["tag"], p["axis"]), "",
              "Reaction at end %.1f N (nominal %.3f MPa on full footprint); max axial deformation %.4f mm (nominal strain %.4f); max local equivalent stress %.2f MPa (constituent onset 19.64 MPa; local only). 1000 N pilot %s effective-yield ranking; displacement control used for the full curve." % (p["F_end"], p["nominal_MPa"], p["max_axial_def"], p["eps_nominal"], p["max_eqv_stress"], "is NOT sufficient for")]
    L += ["", "## Screenshot inventory"] + ["- %s: %s" % x for x in shotlist(c)]
    L += ["", "## Limits", "- 6 mm unit-cell CAD (not a 30-40 mm specimen; >100 cell constraint not demonstrated); free lateral faces; no contact; no literature validation (NOT VALIDATED); density unresolved."]
    open(os.path.join(F, "Cases", c["folder"], "Reports", "%s_report.md" % c["folder"]), "w").write("\n".join(L) + "\n")


def pair_reports():
    pairs = [("BCCZ_Original", "BCCZ_Topo_Optimized"), ("Cube_Original", "Cube_Topo_Optimized"), ("Fluorite_Truss_Original", "Fluorite_Truss_Topo_Optimized"), ("Octet_Truss_Original", "Octet_Truss_Topo_Optimized")]
    for o, t in pairs:
        so, st = SUM.get(o), SUM.get(t)
        L = ["# Pair comparison: %s vs %s" % (o, t), ""]
        if not (so and st):
            L += ["**INCOMPLETE** — %s: %s; %s: %s. No comparison values are invented." % (o, so["status"] if so else "no solved data", t, st["status"] if st else "no solved data")]
        else:
            def f(s, k, fmt="%.4g"): return fmt % s[k] if s.get(k) is not None else "n/a"
            L += ["| metric | Original | Topo | change |", "|---|---|---|---|"]
            def row(name, k):
                a, b = so.get(k), st.get(k)
                ch = "%+.1f%%" % (100 * (b / a - 1)) if (a not in (None, 0) and b is not None) else "n/a"
                L.append("| %s | %s | %s | %s |" % (name, f(so, k), f(st, k), ch))
            for nm, k in (("solid volume mm3 (= mass ratio at equal density)", "vol"), ("relative density", "RD"), ("E_eff MPa", "E_eff"), ("engineering yield MPa", "sigma_y"), ("yield strain", "eps_y"), ("peak eng. stress in run MPa", "max_eng_stress"), ("elements (finest)", "elements")):
                row(nm, k)
            if so["yield_reached"] and st["yield_reached"]:
                L.append("| yield / RD MPa | %.3f | %.3f | %+.1f%% |" % (so["sigma_y"] / so["RD"], st["sigma_y"] / st["RD"], 100 * ((st["sigma_y"] / st["RD"]) / (so["sigma_y"] / so["RD"]) - 1)))
            L += ["", "Mass saving (volume-based) = %.1f%%; mass in grams needs a verified density." % (100 * (so["vol"] - st["vol"]) / so["vol"]),
                  "Mesh status: original %s, topo %s." % (so["status"], st["status"]),
                  "Interpretation must consider that local von Mises concentration differs from effective response; see contour screenshots in each case folder and Comparisons/PAIR_* plots."]
        os.makedirs(os.path.join(F, "Comparisons"), exist_ok=True)
        open(os.path.join(F, "Comparisons", "PAIR_%s_report.md" % o.split("_Original")[0]), "w").write("\n".join(L) + "\n")


def manifest():
    items = []
    for root, _, files in os.walk(F):
        for fn in files:
            p = os.path.join(root, fn)
            if fn.endswith((".lock", ".gitkeep")) or "_files" in root.split(os.sep)[-3:] or "\\_files\\" in p or "_files" + os.sep in p: continue
            sz = os.path.getsize(p)
            items.append(dict(path=os.path.relpath(p, F).replace(os.sep, "/"), bytes=sz, sha256=sha(p) if sz < 600_000_000 else "SKIPPED_TOO_LARGE", nonzero=sz > 0))
    cin = []
    for c in CASES:
        for k in ("iges", "sldprt"):
            p = os.path.join(os.path.dirname(PKG), "..", c[k]); p = os.path.normpath(os.path.join(PKG, "..", "..", c[k]))
            cin.append(dict(case=c["case_id"], kind=k, path=c[k], exists=os.path.exists(p), sha256=sha(p) if os.path.exists(p) else None))
    man = dict(generated=datetime.datetime.now().isoformat(), solver="ANSYS Mechanical 2025 R1", cases=[dict(case_id=c["case_id"], folder=c["folder"], summary=SUM.get(c["case_id"]), mapping=c["mapping_status"]) for c in CASES],
               inputs=cin, outputs=items)
    json.dump(man, open(os.path.join(F, "Logs", "manifest.json"), "w"), indent=1, default=str)
    bad = [i["path"] for i in items if not i["nonzero"]]
    print("manifest files:", len(items), "zero-size:", bad)


if __name__ == "__main__":
    for c in CASES: case_report(c)
    pair_reports(); manifest()
