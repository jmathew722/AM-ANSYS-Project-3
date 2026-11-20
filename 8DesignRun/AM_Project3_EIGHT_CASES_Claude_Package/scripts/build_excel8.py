"""Eight-case formula-driven workbook from REAL results. Usage: python scripts/build_excel8.py [tag=v1]"""
import os, sys, json
import openpyxl
from openpyxl.chart import ScatterChart, Reference, Series, BarChart
from openpyxl.chart.marker import Marker
from openpyxl.styles import Font, PatternFill, Alignment

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(PKG, "FINALUPLAD_Folder")
TAG = sys.argv[1] if len(sys.argv) > 1 else "v1"
CASES = json.load(open(os.path.join(PKG, "config", "cases_resolved.json")))
S = json.load(open(os.path.join(F, "Reports", "_results_with_curves_%s.json" % TAG)))
status_json = os.path.join(F, "Reports", "case_status.json")
ST = json.load(open(status_json)) if os.path.exists(status_json) else {}
HB = Font(bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="1F3864")
wb = openpyxl.Workbook()

def hdr(ws, row, vals):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row, j, v); c.font = HB; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="center")

# ---- Inputs_and_Source
ws = wb.active; ws.title = "Inputs_and_Source"
hdr(ws, 1, ["#", "Case ID", "Folder", "Design", "Variant", "IGES source file", "SLDPRT source file", "Mapping status", "W (mm)", "D (mm)", "H (mm)", "Solid volume (mm3) [CAD_MEASURED via ANSYS import]",
            "Resin density (g/cm3) [USER ENTRY - not in XML]", "Measured mass (g) [optional]", "Unit cells in CAD", "Yield force (N) [ANSYS_RESULT]", "Elastic slope Keff (N/mm) [ANSYS_RESULT]", "Mesh status", "Notes"])
for i, c in enumerate(CASES, start=2):
    s = S.get(c["case_id"]) or {}
    ok = s and s.get("status", "").startswith("SOLVED")
    vals = [c["num"], c["case_id"], c["folder"], c["case_id"].split("_Original")[0].split("_Topo")[0], "Original" if "Original" in c["case_id"] else "Topo Optimized",
            os.path.basename(c["iges"]), os.path.basename(c["sldprt"]), c["mapping_status"],
            s.get("Lx") if ok else None, s.get("Ly") if ok else None, s.get("Lz") if ok else None, s.get("vol") if ok else None, None, None, 1,
            s.get("F_y") if ok else None, s.get("Keff") if ok else None, s.get("status") if ok else ST.get(c["case_id"], {}).get("status", "NOT SOLVED"),
            ST.get(c["case_id"], {}).get("note", "")]
    for j, v in enumerate(vals, 1): ws.cell(i, j, v)
ws.freeze_panes = "C2"
for col, w in zip("ABCDEFGHIJKLMNOPQRS", [4, 28, 36, 14, 14, 30, 30, 22, 8, 8, 8, 20, 18, 14, 10, 14, 16, 22, 60]): ws.column_dimensions[col].width = w
# ---- Geometry_Properties (formulas)
g = wb.create_sheet("Geometry_Properties")
hdr(g, 1, ["Case ID", "A_gross = W*D (mm2)", "V_env = W*D*H (mm3)", "Relative density = Vsolid/Venv", "Porosity (%)", "Mass (g) = rho*V/1000", "Weight (N) = m/1000*9.80665", "RD from mass", "RD<0.5?", "Cell dims within 30-40x30-40x15-20 mm?", "Note"])
for r in range(2, 10):
    I = "Inputs_and_Source!"
    g.cell(r, 1, "=%sB%d" % (I, r))
    g.cell(r, 2, '=IF(COUNT(%sI%d:J%d)<2,"",%sI%d*%sJ%d)' % (I, r, r, I, r, I, r))
    g.cell(r, 3, '=IF(COUNT(%sI%d:K%d)<3,"",%sI%d*%sJ%d*%sK%d)' % (I, r, r, I, r, I, r, I, r))
    g.cell(r, 4, '=IF(OR(C%d="",%sL%d=""),"",%sL%d/C%d)' % (r, I, r, I, r, r))
    g.cell(r, 5, '=IF(D%d="","",(1-D%d)*100)' % (r, r))
    g.cell(r, 6, '=IF(OR(%sL%d="",%sM%d=""),"",%sL%d*%sM%d/1000)' % (I, r, I, r, I, r, I, r))
    g.cell(r, 7, '=IF(F%d="","",F%d/1000*9.80665)' % (r, r))
    g.cell(r, 8, '=IF(OR(%sN%d="",%sM%d="",C%d=""),"",%sN%d*1000/(%sM%d*C%d))' % (I, r, I, r, r, I, r, I, r, r))
    g.cell(r, 9, '=IF(D%d="","PENDING",IF(D%d<0.5,"PASS","FAIL"))' % (r, r))
    g.cell(r, 10, '=IF(COUNT(%sI%d:K%d)<3,"PENDING",IF(AND(%sI%d>=30,%sI%d<=40,%sJ%d>=30,%sJ%d<=40,%sK%d>=15,%sK%d<=20),"PASS","FAIL (unit-cell CAD)"))' % ((I, r, r) + (I, r) * 5 + (I, r)))
g.freeze_panes = "B2"
# ---- Material
m = wb.create_sheet("Material_Tough2000")
hdr(m, 1, ["Property", "Value", "Unit", "Source"])
for row in [["Young modulus", 1109.5, "MPa", "USER_FILE AM_Formlabs.xml"], ["Poisson ratio", 0.35, "-", "USER_FILE"], ["Bulk modulus", 1232.777778, "MPa", "USER_FILE"],
            ["Shear modulus", 410.925926, "MPa", "USER_FILE"], ["Density", None, "g/cm3", "UNRESOLVED (not in XML). Candidates found online: 1.09 g/mL bulk (V2 TDS), 1.11-1.12 (SDS/retail), ~1.2 post-cured (V1 white paper) - enter verified value in Inputs_and_Source!M"]]:
    m.append(row)
m.append([]); hdr(m, 8, ["Plastic strain (-)", "Stress (MPa)", "", "Source"])
import xml.etree.ElementTree as ET
t = ET.parse(os.path.join(PKG, "materials", "AM_Formlabs.xml")).getroot()
pa = {}
for pv in t.iter("ParameterValue"):
    d = pv.find("Data")
    if d is not None and d.text and "," in d.text: pa[pv.get("parameter")] = [float(x) for x in d.text.split(",")]
keys = sorted(pa, key=lambda k: int(k[2:]))
cand = [k for k in keys if len(pa[k]) == 21]
if len(cand) >= 2:
    pst = pa[cand[0]]; sts = pa[cand[1]]
    # decide which is stress (larger values)
    if max(pst) > 1000: sts, pst = pst, sts
    for e, s_ in zip(pst, sts): m.append([e, s_ / 1e6 if s_ > 1e4 else s_, "", "USER_FILE (parsed from XML)"])
# ---- Eight_Case_Summary
es = wb.create_sheet("Eight_Case_Summary")
hdr(es, 1, ["Case ID", "Engineering yield (MPa) = Fy/A_gross", "Yield strain (mm/mm) [ANSYS_RESULT]", "E_eff (MPa) = Keff*H/A", "Relative density", "Yield/RD (MPa)", "Peak engineering stress in run (MPa) [ANSYS_RESULT]", "Yield method", "Mesh status", "Finest element size (mm)", "Elements (finest)"])
for r, c in enumerate(CASES, start=2):
    s = S.get(c["case_id"]) or {}; ok = s and s.get("status", "").startswith("SOLVED")
    es.cell(r, 1, "=Inputs_and_Source!B%d" % r)
    es.cell(r, 2, '=IF(OR(Inputs_and_Source!P%d="",Geometry_Properties!B%d=""),"",Inputs_and_Source!P%d/Geometry_Properties!B%d)' % (r, r, r, r))
    es.cell(r, 3, s.get("eps_y") if ok and s.get("yield_reached") else None)
    es.cell(r, 4, '=IF(OR(Inputs_and_Source!Q%d="",Geometry_Properties!B%d=""),"",Inputs_and_Source!Q%d*Inputs_and_Source!K%d/Geometry_Properties!B%d)' % (r, r, r, r, r))
    es.cell(r, 5, "=Geometry_Properties!D%d" % r)
    es.cell(r, 6, '=IF(OR(B%d="",E%d=""),"",B%d/E%d)' % (r, r, r, r))
    es.cell(r, 7, s.get("max_eng_stress") if ok else None)
    es.cell(r, 8, s.get("method", "").replace("%%", "%") if ok else None)
    es.cell(r, 9, s.get("status") if ok else ST.get(c["case_id"], {}).get("status", "NOT SOLVED"))
    es.cell(r, 10, s.get("finest_size") if ok else None); es.cell(r, 11, s.get("elements") if ok else None)
es.freeze_panes = "B2"
# ---- Paired comparisons
pc = wb.create_sheet("Four_Paired_Comparisons")
hdr(pc, 1, ["Design", "Original case", "Topo case", "Volume saving % (=mass saving at equal density)", "Mass saving % (needs density)", "Yield change %", "Yield/RD change %", "Stiffness (E_eff) change %", "Yield strain orig", "Yield strain topo", "Comment"])
for k, (o, tcase) in enumerate([(2, 3), (4, 5), (6, 7), (8, 9)]):
    r = k + 2; es_ = "Eight_Case_Summary!"; gp = "Geometry_Properties!"
    ro, rt = (2 * k) + 2, (2 * k) + 3
    pc.cell(r, 1, ["BCCZ", "Cube", "Fluorite Truss", "Octet Truss"][k]); pc.cell(r, 2, "=Inputs_and_Source!B%d" % ro); pc.cell(r, 3, "=Inputs_and_Source!B%d" % rt)
    pc.cell(r, 4, '=IFERROR(100*(Inputs_and_Source!L%d-Inputs_and_Source!L%d)/Inputs_and_Source!L%d,"")' % (ro, rt, ro))
    pc.cell(r, 5, '=IFERROR(100*(%sF%d-%sF%d)/%sF%d,"")' % (gp, ro, gp, rt, gp, ro))
    pc.cell(r, 6, '=IFERROR(100*(%sB%d/%sB%d-1),"")' % (es_, rt, es_, ro))
    pc.cell(r, 7, '=IFERROR(100*(%sF%d/%sF%d-1),"")' % (es_, rt, es_, ro))
    pc.cell(r, 8, '=IFERROR(100*(%sD%d/%sD%d-1),"")' % (es_, rt, es_, ro))
    pc.cell(r, 9, "=%sC%d" % (es_, ro)); pc.cell(r, 10, "=%sC%d" % (es_, rt))
    pc.cell(r, 11, "Blank = a case is unsolved/unidentified; no value invented")
# ---- Ranking (formulas over validated, i.e. numeric yield/RD)
rk = wb.create_sheet("Strength_Density_Ranking")
hdr(rk, 1, ["Case ID", "Yield/RD (MPa)", "Rank (1 = best; numeric entries only)", "Mesh status", "Validation status"])
for r in range(2, 10):
    rk.cell(r, 1, "=Inputs_and_Source!B%d" % r); rk.cell(r, 2, "=Eight_Case_Summary!F%d" % r)
    rk.cell(r, 3, '=IF(ISNUMBER(B%d),RANK(B%d,$B$2:$B$9),"")' % (r, r)); rk.cell(r, 4, "=Eight_Case_Summary!I%d" % r)
    rk.cell(r, 5, "NOT literature-validated; preliminary ranking")
bc = BarChart(); bc.title = "Yield / relative density (MPa)"; bc.add_data(Reference(rk, min_col=2, min_row=1, max_row=9), titles_from_data=True); bc.set_categories(Reference(rk, min_col=1, min_row=2, max_row=9)); rk.add_chart(bc, "G2")
# ---- Mesh convergence
mc = wb.create_sheet("Mesh_Convergence")
hdr(mc, 1, ["Case", "Level", "Size (mm)", "Elements", "Nodes", "Peak force (N)", "Yield force (N)", "Yield (MPa)", "Keff (N/mm)", "Yield change vs prior", "Keff change vs prior"])
row = 2
for c in CASES:
    for lv in (S.get(c["case_id"]) or {}).get("levels", []):
        for j, v in enumerate([c["case_id"], lv["level"], lv["size"], lv["elements"], lv["nodes"], lv["Fmax"], lv["F_y"], lv["sigma_y"], lv["Keff"]], 1): mc.cell(row, j, v)
        if lv["level"] > 1:
            mc.cell(row, 10, '=IFERROR(ABS(H%d-H%d)/ABS(H%d),"")' % (row, row - 1, row - 1)); mc.cell(row, 11, '=IFERROR(ABS(I%d-I%d)/ABS(I%d),"")' % (row, row - 1, row - 1))
        row += 1
# ---- Step history sheets with charts
for c in CASES:
    s = S.get(c["case_id"])
    if not s or "_curve" not in s: continue
    h = wb.create_sheet("Hist_%d" % c["num"]); cv = s["_curve"]
    h.append(["eng strain", "eng stress (MPa)", "max eqv stress (MPa)", "max eqv total strain", "source: ANSYS %s" % TAG])
    for a, b, d, e in zip(cv["eps"], cv["sig"], cv["smax"], cv["emax"]): h.append([a, b, d, e])
    h["G1"] = "yield strain"; h["H1"] = s["eps_y"] if s["yield_reached"] else None; h["G2"] = "yield stress"; h["H2"] = s["sigma_y"] if s["yield_reached"] else None
    n = len(cv["eps"]) + 1
    ch = ScatterChart(); ch.title = "%s engineering stress-strain (red dot = yield)" % c["folder"]; ch.x_axis.title = "strain"; ch.y_axis.title = "MPa"
    se = Series(Reference(h, min_col=2, min_row=2, max_row=n), Reference(h, min_col=1, min_row=2, max_row=n), title="ANSYS"); se.graphicalProperties.line.solidFill = "C00000"; ch.series.append(se)
    if s["yield_reached"]:
        ys = Series(Reference(h, min_col=8, min_row=2, max_row=2), Reference(h, min_col=8, min_row=1, max_row=1), title="Yield"); ys.marker = Marker(symbol="circle", size=10)
        ys.marker.graphicalProperties.solidFill = "FF0000"; ys.graphicalProperties.line.noFill = True; ch.series.append(ys)
    h.add_chart(ch, "J2")
# ---- Yield methods / validation / status
ym = wb.create_sheet("Yield_Methods")
for line in [["Engineering yield", "0.2% strain-offset on initial effective slope (secant of first 2 of 60 increments) of |F|/A_full vs |u|/H0. Resolution: 0.25% strain per increment."],
             ["Material onset", "19.6405 MPa (XML first hardening point) - NOT lattice yield"], ["Local maxima", "Max equivalent stress / total strain are field maxima at different locations, not engineering values"]]: ym.append(line)
va = wb.create_sheet("Validation")
for line in [["Verification", "Cube_Original (solid 6 mm cube) elastic stiffness vs analytic E*A/L - see Reports"], ["Literature validation", "NOT DONE - no applicable Tough 2000 lattice reference supplied; Ling 2019 octet paper must not be labeled Tough 2000 validation"]]: va.append(line)
rs = wb.create_sheet("Run_Status")
hdr(rs, 1, ["Case", "Status", "Note"])
for c in CASES:
    s = S.get(c["case_id"]) or {}
    rs.append([c["folder"], s.get("status") or ST.get(c["case_id"], {}).get("status", "NOT SOLVED"), ST.get(c["case_id"], {}).get("note", "")])
d = wb.create_sheet("Dashboard", 0)
d["A1"] = "AME Project 3 — eight-case FEM workbook (ANSYS 2025 R1, Tough 2000)"; d["A1"].font = Font(bold=True, size=14)
d["A3"] = "Real ANSYS results only; blank = not solved / not identified. Density is a USER INPUT (not in XML): mass formulas stay blank until entered."
d["A4"] = "CAD = 6 mm unit cells; specimen-level constraints (30-40 mm, >100 cells) are not met by the supplied CAD."
d["A5"] = "File mapping IGES->case is PROVISIONAL (see Inputs_and_Source column H)."
out = os.path.join(F, "Excel", "AM_Project3_Eight_Case_Validation.xlsx")
os.makedirs(os.path.dirname(out), exist_ok=True)
wb.save(out); print("saved", out)
