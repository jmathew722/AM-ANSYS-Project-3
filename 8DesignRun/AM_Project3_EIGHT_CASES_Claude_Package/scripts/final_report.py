"""Final technical report (MD) + two-page FEM summary (PDF via matplotlib). Run after postprocess8.py and make_reports.py."""
import os, json, datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(PKG, "FINALUPLAD_Folder")
CASES = json.load(open(os.path.join(PKG, "config", "cases_resolved.json")))
SUM = json.load(open(os.path.join(F, "Reports", "results_summary_v1.json")))
NOTES = json.load(open(os.path.join(PKG, "config", "case_notes.json"))) if os.path.exists(os.path.join(PKG, "config", "case_notes.json")) else {}


def row(c):
    s = SUM.get(c["case_id"]); n = NOTES.get(c["case_id"], {})
    if not s:
        return [c["folder"], n.get("status", "BLOCKED/NOT SOLVED"), "-", "-", "-", "-", "-", "-", n.get("note", "no solved data")]
    st = {"SOLVED_CONVERGED": "PASS (converged)"}.get(s["status"], "PARTIAL (" + s["status"] + ")")
    if n.get("status"): st = n["status"]
    yv = "%.4g" % s["sigma_y"] if s["yield_reached"] else "YIELD NOT IDENTIFIED"
    return [c["folder"], st, "%.4f" % s["RD"], "%.4g" % s["E_eff"], yv, "%.5f" % s["eps_y"] if s["yield_reached"] else "-",
            "%.3f" % (s["sigma_y"] / s["RD"]) if s["yield_reached"] else "-", str(s["elements"]), n.get("note", "")]


HDR = ["Case", "Status", "Rel. density", "E_eff MPa", "Yield MPa", "Yield strain", "Yield/RD MPa", "Elements (finest)", "Note"]
rows = [row(c) for c in CASES]
rank = sorted([(r, SUM[c["case_id"]]) for r, c in zip(rows, CASES) if SUM.get(c["case_id"]) and SUM[c["case_id"]]["yield_reached"]], key=lambda x: -x[1]["sigma_y"] / x[1]["RD"])

L = ["# AME Project 3 — Eight-case FEM final technical report", "", "Generated %s. Solver: ANSYS Mechanical 2025 R1; material Tough 2000 from `materials/AM_Formlabs.xml` (E=1109.5 MPa, nu=0.35, 21-point multilinear hardening); density not in XML, so mass is TBD." % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "",
     "## Method", "- Unit-cell CAD (6 mm), bottom face fixed, prescribed compressive displacement 0.9 mm (15% strain) in 60 substeps, large deflection on, free lateral faces, compression axis auto-detected from the largest planar end caps.",
     "- Engineering stress = |reaction force| / A_full (full footprint); strain = u/H0. Yield = 0.2% strain-offset on the effective initial secant slope.",
     "- Local maximum equivalent stress vs maximum equivalent total strain plots are tutorial-style visualizations only; they are not the engineering curve used for ranking.",
     "- Mesh convergence criterion: <2% change in E_eff, yield and Keff between the last two levels.", "", "## Results", "", "| " + " | ".join(HDR) + " |", "|" + "---|" * len(HDR)]
L += ["| " + " | ".join(r) + " |" for r in rows]
L += ["", "## Ranking by yield / relative density (valid cases only)", ""] + ["%d. %s — %.3f MPa" % (i + 1, r[0], s["sigma_y"] / s["RD"]) for i, (r, s) in enumerate(rank)]
L += ["", "## Pair comparisons", "See `Comparisons/PAIR_*_report.md` and PAIR plots.", "",
      "## Limitations and not-done items",
      "- No literature/experimental validation (NOT VALIDATED); only an analytic modulus check on the solid cube.",
      "- No verified resin density: mass and weight are not reported.",
      "- SolidWorks Mass Properties and SolidWorks GUI screenshots were not produced; ANSYS screenshots are exported Mechanical images.",
      "- Yield charts are Python-generated from solver data, not window captures.",
      "- IGES-to-case mapping is provisional (by design name); confirm in `config/cases_resolved.json`.",
      "- Cube_Topo IGES is surface-only; the SLDPRT was used.",
      "- CAD is a 6 mm unit cell, not a 30-40 mm specimen; the >100-cell condition is not demonstrated.",
      "- Topology-optimized cells have tiny features: element counts are feature-limited, so the finest mesh is bounded by compute.", ""]
open(os.path.join(F, "Reports", "FINAL_TECHNICAL_REPORT.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

with PdfPages(os.path.join(F, "Reports", "FEM_Preliminary_Summary_2page.pdf")) as pdf:
    fig = plt.figure(figsize=(8.5, 11)); fig.text(0.07, 0.95, "AME Project 3 - Preliminary FEM summary (8 cases)", fontsize=14, weight="bold")
    txt = ("Method: ANSYS Mechanical 2025 R1, Tough 2000 (XML), 6 mm unit cells, fixed bottom, displacement-controlled\ncompression to 15% strain, large deflection. Engineering stress = F/A_full, strain = u/H0.\n"
           "Yield: 0.2% offset on initial effective slope. Convergence: <2% (E_eff, yield, Keff) over last two meshes.\nLocal max-stress/max-strain plots are separate and are not used for ranking.")
    fig.text(0.07, 0.90, txt, fontsize=8.5, va="top")
    ax = fig.add_axes([0.03, 0.45, 0.94, 0.38]); ax.axis("off")
    t = ax.table(cellText=[r[:8] for r in rows], colLabels=HDR[:8], loc="upper center", cellLoc="center"); t.auto_set_font_size(False); t.set_fontsize(6.5); t.scale(1, 1.6)
    fig.text(0.07, 0.40, "Ranking by yield/relative density:\n" + "\n".join("%d. %s: %.3f MPa" % (i + 1, r[0], s["sigma_y"] / s["RD"]) for i, (r, s) in enumerate(rank)), fontsize=8.5, va="top")
    pdf.savefig(fig); plt.close(fig)
    fig = plt.figure(figsize=(8.5, 11)); fig.text(0.07, 0.95, "Limitations / not validated", fontsize=14, weight="bold")
    fig.text(0.07, 0.92, "\n".join("- " + x[2:] for x in L if x.startswith("- ") and "SolidWorks" in x or x.startswith("- No ") or x.startswith("- IGES") or x.startswith("- Cube_Topo") or x.startswith("- CAD") or x.startswith("- Topology") or x.startswith("- Yield charts")), fontsize=8.5, va="top", wrap=True)
    cmp = os.path.join(F, "Comparisons", "COMPARISON_8_CASES_stress_strain.png")
    if os.path.exists(cmp):
        ax = fig.add_axes([0.07, 0.30, 0.86, 0.45]); ax.imshow(plt.imread(cmp)); ax.axis("off")
    pdf.savefig(fig); plt.close(fig)
print("report written")
