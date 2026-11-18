"""Populate the formula-driven template with REAL results (blank where absent). Usage: python scripts/build_excel.py [tag]"""
import os, sys, json, shutil
import openpyxl
from openpyxl.chart import ScatterChart, Reference, Series, BarChart
from openpyxl.chart.marker import Marker

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "OUTPUTS_Folder")
TAG = sys.argv[1] if len(sys.argv) > 1 else "v1"
res = json.load(open(os.path.join(OUT, "Reports", "_results_with_curves_%s.json" % TAG)))
DENSITY = 1.20  # g/cm3 - SOURCED (Formlabs V1 post-cured white paper), NOT in XML; verify for resin version used
dst = os.path.join(OUT, "Excel", "AM_Project3_Four_Design_FEM_Results.xlsx")
shutil.copy(os.path.join(ROOT, "templates", "AM_Project3_Editable_Calculations.xlsx"), dst)
wb = openpyxl.load_workbook(dst)
di = wb["Design_Inputs"]
names = {"Design_01": "BCCZ_Topo_Smooth_6mm_rho26", "Design_02": "Fluorite_Topo_Smooth_6mm_rho49", "Design_03": "Octet_Truss_Smooth", "Design_04": "BLOCKED - no CAD file supplied"}
for r, d in enumerate(["Design_01", "Design_02", "Design_03", "Design_04"], start=2):
    s = res.get(d, {})
    if s.get("status", "").startswith("SOLVED"):
        di.cell(r, 2, s["Lx"]); di.cell(r, 3, s["Ly"]); di.cell(r, 4, s["Lz"]); di.cell(r, 5, s["vol"]); di.cell(r, 6, DENSITY)
        if s["yield_reached"]:
            di.cell(r, 8, s["F_y"])
        di.cell(r, 9, s["Keff"]); di.cell(r, 10, "YES" if s["converged"] else "NO (UNCONVERGED)")
        di.cell(r, 11, "%s; unit-cell CAD (6 mm) not full specimen; volume=Mechanical CAD volume; density sourced not measured; yield=0.2%% offset; literature validation NOT done" % names[d])
    else:
        di.cell(r, 11, names[d])
# mesh convergence
mc = wb["Mesh_Convergence"]; row = 2
for d in ["Design_01", "Design_02", "Design_03"]:
    for lv in res.get(d, {}).get("levels", []):
        mc.cell(row, 1, d); mc.cell(row, 2, lv["level"]); mc.cell(row, 3, lv["size"]); mc.cell(row, 4, lv["elements"]); mc.cell(row, 5, lv["nodes"])
        mc.cell(row, 6, lv["F_y"]); mc.cell(row, 7, lv["sigma_y"]); mc.cell(row, 8, lv["Keff"]); row += 1
# histories + charts
for d in ["Design_01", "Design_02", "Design_03"]:
    s = res.get(d)
    if not s or "_curve" not in s: continue
    c = s["_curve"]; ws = wb.create_sheet("Hist_%s" % d)
    ws.append(["time", "u_top [mm]", "F [N]", "eng strain [mm/mm]", "eng stress [MPa]", "max eqv stress [MPa]", "max eqv total strain", "source"])
    for i in range(len(c["t"])):
        r = i + 2
        ws.append([c["t"][i], c["u"][i], c["F"][i], "=B%d/Design_Inputs!D%d" % (r, "ABCD".index(d[-1]) + 2 if False else int(d[-1]) + 1),
                   "=C%d/Calculated_Results!C%d" % (r, int(d[-1]) + 1), c["smax"][i], c["emax"][i], "ANSYS measured"])
    ws["J1"] = "Yield marker (0.2% offset)"; ws["J2"] = "strain"; ws["K2"] = s["eps_y"] if s["yield_reached"] else None
    ws["J3"] = "stress MPa"; ws["K3"] = s["sigma_y"] if s["yield_reached"] else None
    ws["J4"] = "method"; ws["K4"] = s["method"]
    n = len(c["t"]) + 1
    ch = ScatterChart(); ch.title = "%s engineering stress-strain (red dot = yield)" % d; ch.x_axis.title = "strain [mm/mm]"; ch.y_axis.title = "stress [MPa]"
    ser = Series(Reference(ws, min_col=5, min_row=2, max_row=n), Reference(ws, min_col=4, min_row=2, max_row=n), title="ANSYS")
    ser.graphicalProperties.line.solidFill = "C00000"; ch.series.append(ser)
    if s["yield_reached"]:
        ys = Series(Reference(ws, min_col=11, min_row=3, max_row=3), Reference(ws, min_col=11, min_row=2, max_row=2), title="Yield")
        ys.marker = Marker(symbol="circle", size=10); ys.marker.graphicalProperties.solidFill = "FF0000"; ys.graphicalProperties.line.noFill = True
        ch.series.append(ys)
    ws.add_chart(ch, "M2")
# ranking
rk = wb.create_sheet("Ranking")
rk.append(["Design", "Eng. yield (MPa)", "Relative density", "Yield / RD (MPa)", "Rank (preliminary)", "Status"])
for i, d in enumerate(["Design_01", "Design_02", "Design_03", "Design_04"], start=2):
    cr = "Calculated_Results"
    rk.append(["=%s!A%d" % (cr, i), "=%s!H%d" % (cr, i), "=%s!D%d" % (cr, i), "=%s!I%d" % (cr, i), '=IF(ISNUMBER(D%d),RANK(D%d,$D$2:$D$5),"")' % (i, i),
               "BLOCKED: no CAD" if d == "Design_04" else ("PRELIMINARY - not literature-validated" )])
bc = BarChart(); bc.title = "Yield / relative density (preliminary)"; bc.add_data(Reference(rk, min_col=4, min_row=1, max_row=5), titles_from_data=True); bc.set_categories(Reference(rk, min_col=1, min_row=2, max_row=5))
rk.add_chart(bc, "H2")
# checklist / provenance
ck = wb.create_sheet("Checklist_Provenance")
for line in [
    ["Item", "Status / source"],
    ["Solver", "ANSYS Mechanical 2025 R1 via Workbench batch journals (scripts/*.wbjn, mech_run.py)"],
    ["Material", "Tough 2000 from materials/AM_Formlabs.xml (E=1109.5 MPa, nu=0.35, 21-pt multilinear hardening); never Structural Steel"],
    ["Density", "%.2f g/cm3 SOURCED from Formlabs V1 post-cured density white paper; XML has none; verify" % DENSITY],
    ["Geometry", "6 mm unit-cell CAD (IGES). Assignment limits (30-40 mm, >100 cells) NOT met at specimen level; unit-cell model only"],
    ["Volume/mass", "From Mechanical CAD volume of imported IGES; SolidWorks Mass Properties panel NOT extracted (not automated)"],
    ["Load", "Displacement-controlled -Z top face; bottom fixed support; 1000 N force-ramp pilot run separately (see Reports)"],
    ["Yield", "0.2% offset on initial effective slope of F/A_full vs u/H0"],
    ["Literature validation", "NOT DONE"],
    ["Design_04", "BLOCKED - only three CAD sets (BCCZ, Fluorite, Octet) were provided"],
]: ck.append(line)
wb["README"]["B3"] = "POPULATED with real ANSYS 2025R1 results (tag %s); see Checklist_Provenance for limits" % TAG
wb.save(dst)
print("saved", dst)
