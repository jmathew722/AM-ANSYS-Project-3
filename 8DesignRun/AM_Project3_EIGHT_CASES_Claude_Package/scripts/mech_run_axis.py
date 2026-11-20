# IronPython executed INSIDE Mechanical (via model.SendCommand). CFG dict is prepended by the WB journal.
import os, sys, traceback, math
def L(m):
    try:
        f = open(CFG['logfile'], 'a'); f.write(str(m) + "\n"); f.close()
    except:
        pass
def Q(v, u): return Quantity(v, u)
m = ExtAPI.DataModel.Project.Model
OUT = CFG['simdir']
SS = CFG['shotdir']
for d in (OUT, SS):
    if not os.path.isdir(d): os.makedirs(d)
def W(name, rows, header):
    f = open(os.path.join(OUT, name), 'w'); f.write(header + "\n")
    for r in rows: f.write(",".join([str(x) for x in r]) + "\n")
    f.close()
def shot(name, note=''):
    p = os.path.join(SS, name)
    try:
        ExtAPI.Graphics.Camera.SetFit()
        st = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
        st.Resolution = Ansys.Mechanical.DataModel.Enums.GraphicsResolutionType.EnhancedResolution
        st.Width = 1600; st.Height = 1000; st.CurrentGraphicsDisplay = False
        ExtAPI.Graphics.ExportImage(p, Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat.PNG, st)
        ok = os.path.exists(p) and os.path.getsize(p) > 0
        L("SHOT %s ok=%s %s" % (name, ok, note)); return ok
    except Exception as e:
        L("SHOT FAIL %s: %s" % (name, e)); return False
def table(res, label):
    try:
        pd = res.PlotData
        cols = [str(c) for c in pd.Keys]
        data = {}
        for c in cols: data[c] = [x for x in pd[c]]
        L("TABLE %s cols=%s n=%d" % (label, cols, len(data[cols[0]]) if cols else 0))
        return cols, data
    except Exception as e:
        L("TABLE FAIL %s: %s" % (label, traceback.format_exc())); return None, None
def write_hist(nm, c, d, tag):
    if c is None: return
    rows = []
    n = len(d[c[0]])
    for i in range(n): rows.append([d[k][i] for k in c])
    W("raw_%s_%s.csv" % (nm, tag), rows, ",".join([str(k) for k in c]))

try:
    geo = m.Geometry
    parts = [p for p in geo.Children]
    bodies = [b for p in parts for b in p.Children]
    L("bodies=%d" % len(bodies))
    for b in bodies: b.Material = CFG['material']
    Lx = geo.LengthX.Value; Ly = geo.LengthY.Value; Lz = geo.LengthZ.Value
    L("LengthXYZ %s %s %s unit=%s" % (Lx, Ly, Lz, geo.LengthX.Unit))
    vol = sum([b.Volume.Value for b in bodies])
    L("volume %s %s" % (vol, bodies[0].Volume.Unit))
    L("material assigned: " + ",".join([str(b.Material) for b in bodies]))
    allfaces = []; xs = [1e30, 1e30, 1e30, -1e30, -1e30, -1e30]
    for b_ in bodies:
        gb_ = b_.GetGeoBody(); bb_ = list(gb_.GetBoundingBox())
        for k in range(3):
            xs[k] = min(xs[k], bb_[k]); xs[k + 3] = max(xs[k + 3], bb_[k + 3])
        for f in gb_.Faces: allfaces.append(f)
    L("bbox raw " + str(xs) + " nfaces=%d" % len(allfaces))
    ext = [xs[3] - xs[0], xs[4] - xs[1], xs[5] - xs[2]]
    scale = Lx / ext[0] if ext[0] > 0 else 1000.0
    L("scale coord->mm = %s ; extents mm = %s" % (scale, [e * scale for e in ext]))
    tol = 0.02
    lo = [xs[k] * scale for k in range(3)]; hi = [xs[k + 3] * scale for k in range(3)]
    dims = [hi[k] - lo[k] for k in range(3)]
    cap = {}
    for ax_ in range(3):
        topf = []; botf = []; ta = 0.0; ba = 0.0
        for f in allfaces:
            try:
                c = f.Centroid; z = c[ax_] * scale
                fb = list(f.GetBoundingBox())
                if abs(fb[ax_ + 3] - fb[ax_]) * scale >= tol: continue
                ar = f.Area * scale * scale
                if abs(z - hi[ax_]) < tol: topf.append(f.Id); ta += ar
                elif abs(z - lo[ax_]) < tol: botf.append(f.Id); ba += ar
            except Exception as e:
                L("face err %s" % e)
        cap[ax_] = (topf, botf, ta, ba)
        L("axis %s: top faces=%d area=%.4f | bottom faces=%d area=%.4f" % ("XYZ"[ax_], len(topf), ta, len(botf), ba))
    forced = CFG.get('axis', 'auto')
    if forced in ('X', 'Y', 'Z'): AX = "XYZ".index(forced)
    else:
        ar_ = [min(cap[k][2], cap[k][3]) for k in range(3)]
        best_ = max(ar_)
        AX = [k for k in (2, 1, 0) if ar_[k] >= 0.98 * best_][0]   # ties (symmetric cells) -> prefer Z, then Y, then X
        L("axis areas (min of top/bottom) X,Y,Z = %s ; selected %s" % (ar_, "XYZ"[AX]))
    top, bot = cap[AX][0], cap[AX][1]
    oth = [k for k in range(3) if k != AX]
    Lx, Ly, Lz = dims[oth[0]], dims[oth[1]], dims[AX]   # Lx,Ly = footprint dims, Lz = height along compression axis
    zmin = lo[AX]; zmax = hi[AX]
    L("COMPRESSION AXIS = %s (forced=%s); footprint %.4f x %.4f mm; H0=%.4f mm" % ("XYZ"[AX], forced, Lx, Ly, Lz))
    gb = None
    W("geometry_probe.csv", [[Lx, Ly, Lz, vol, len(top), len(bot), zmin, zmax, len(bodies), len(allfaces), AX, cap[AX][2], cap[AX][3], dims[0], dims[1], dims[2]]], "Lx_mm,Ly_mm,Lz_mm,volume_mm3,n_top_faces,n_bottom_faces,zmin,zmax,n_bodies,n_faces,axis_index,top_area_mm2,bottom_area_mm2,bboxX,bboxY,bboxZ")
    if CFG.get('probe_only'):
        raise SystemExit
    def sel(ids):
        s = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities); s.Ids = ids; return s
    an = m.Analyses[0]
    nt = m.AddNamedSelection(); nt.Name = "TOP_FACES"; nt.Location = sel(top)
    nb = m.AddNamedSelection(); nb.Name = "BOTTOM_FACES"; nb.Location = sel(bot)
    fs = an.AddFixedSupport(); fs.Location = sel(bot); fs.Name = "Fixed Support (bottom)"
    mode = CFG['mode']
    if mode == 'force':
        ld = an.AddForce(); ld.DefineBy = LoadDefineBy.Components; ld.Location = sel(top)
        getattr(ld, 'XYZ'[AX] + 'Component').Output.DiscreteValues = [Q(-CFG['force_N'], 'N')]
        ld.Name = "Top compressive force (-%s)" % "XYZ"[AX]
    else:
        ld = an.AddDisplacement(); ld.Location = sel(top); ld.Name = "Top displacement (-%s)" % "XYZ"[AX]
        getattr(ld, 'XYZ'[AX] + 'Component').Output.DiscreteValues = [Q(-CFG['disp_mm'], 'mm')]
    s = an.AnalysisSettings
    s.NumberOfSteps = 1; s.CurrentStepNumber = 1
    s.StepEndTime = Q(1, 'sec')
    s.AutomaticTimeStepping = AutomaticTimeStepping.On
    s.DefineBy = TimeStepDefineByType.Substeps
    s.InitialSubsteps = CFG['init_sub']; s.MinimumSubsteps = CFG['init_sub']; s.MaximumSubsteps = CFG['max_sub']
    s.LargeDeflection = True
    try: s.NodalForces = OutputControlsNodalForcesType.Yes
    except Exception as e: L("nodal forces opt: %s" % e)
    sol = an.Solution
    fr = sol.AddForceReaction(); fr.LocationMethod = LocationDefinitionMethod.BoundaryCondition; fr.BoundaryConditionSelection = fs; fr.Name = "Reaction Z (bottom support)"
    dz = sol.AddDirectionalDeformation(); dz.NormalOrientation = [NormalOrientationType.XAxis, NormalOrientationType.YAxis, NormalOrientationType.ZAxis][AX]; dz.Name = "Directional Deformation (compression axis)"
    td = sol.AddTotalDeformation()
    es = sol.AddEquivalentStress()
    ee = sol.AddEquivalentTotalStrain()
    eps = sol.AddEquivalentPlasticStrain()
    summary = []
    nlev = len(CFG['mesh_sizes'])
    for lvl in range(nlev):
        size = CFG['mesh_sizes'][lvl]
        tag = "L%d" % (lvl + 1)
        mesh = m.Mesh
        mesh.ElementSize = Q(size, 'mm')
        try: mesh.ElementOrder = ElementOrder.Quadratic
        except Exception as e: L("order: %s" % e)
        import time as _t
        t0 = _t.time()
        for pn, pv in CFG.get('mesh_props', []):
            try: setattr(mesh, pn, eval(pv))
            except Exception as e: L("mesh prop %s fail %s" % (pn, e))
        mesh.GenerateMesh()
        L("mesh time %.1f s" % (_t.time() - t0))
        nn = mesh.Nodes; ne = mesh.Elements
        L("LEVEL %d size=%s nodes=%s elements=%s" % (lvl + 1, size, nn, ne))
        try:
            mesh.Activate(); ExtAPI.Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Iso)
        except Exception as e: L("mesh activate %s" % e)
        shot("05_mesh_%s_size%s.png" % (tag, size), "mesh")
        if lvl == nlev - 1: shot("05_mesh.png", "mesh final")
        an.Solve(True)
        L("solve returned; status=%s" % str(an.Solution.Status))
        sol.EvaluateAllResults()
        if lvl == 0 and CFG.get('diag'):
            try:
                tdta = es.TabularData
                L("DIAG TabularData type %s attrs %s" % (type(tdta), [a for a in dir(tdta) if not a.startswith('_')]))
                try: L("DIAG Columns %s" % str([c for c in tdta.Columns]))
                except Exception as e: L("diag cols err %s" % e)
                try: L("DIAG Rows/Count %s %s" % (tdta.Count, tdta.RowCount))
                except Exception as e: L("diag count err %s" % e)
                try: L("DIAG sol attrs %s" % str([a for a in dir(sol) if not a.startswith('_')]))
                except Exception as e: L("diag sol %s" % e)
                try: L("DIAG an.Solution.TimeStepList %s" % str(dir(an)))
                except Exception as e: pass
                L("DIAG PlotData attrs: " + str([a for a in dir(es.PlotData) if not a.startswith('_')]))
                L("DIAG fr attrs: " + str([a for a in dir(fr) if not a.startswith('_')]))
                L("DIAG es attrs: " + str([a for a in dir(es) if not a.startswith('_')]))
            except Exception as e: L("diag err %s" % e)
        try:
            N = CFG['init_sub']
            rows = []
            for i in range(0, N + 1):
                t = float(i) / N
                try:
                    if i == 0:
                        rows.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]); continue
                    for r_ in (es, ee, dz, fr, td):
                        r_.DisplayTime = Q(t, 'sec')
                    es.EvaluateAllResults()
                    rows.append([t, es.Maximum.Value, es.Average.Value, ee.Maximum.Value, dz.Minimum.Value, getattr(fr, 'XYZ'[AX] + 'Axis').Value, td.Maximum.Value])
                except Exception as e:
                    L("history point t=%s failed: %s" % (t, e))
            W("raw_history_%s.csv" % tag, rows, "Time,EqvStress_max_MPa,EqvStress_avg_MPa,EqvTotalStrain_max,DirDefZ_min_mm,ReactionZ_N,TotalDef_max_mm")
            L("history rows %d last=%s" % (len(rows), rows[-1]))
        except Exception as e: L("history loop fail %s" % traceback.format_exc())
        summary.append([lvl + 1, size, nn, ne, str(an.Solution.Status)])
        if lvl == nlev - 1:
            for r_ in (es, ee, dz, fr, td, eps): r_.DisplayTime = Q(1.0, 'sec')
            sol.EvaluateAllResults()
            for res, fn in ((td, "07_total_deformation.png"), (dz, "08_directional_deformation_z.png"), (es, "09_equivalent_stress_von_mises.png"), (ee, "10_equivalent_total_strain.png"), (eps, "10b_equivalent_plastic_strain.png")):
                try:
                    res.Activate(); ExtAPI.Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Iso); shot(fn, res.Name)
                except Exception as e: L("contour %s: %s" % (fn, e))
            try:
                ld.Activate(); shot("06_fixed_support_and_loading.png", "loading")
            except Exception as e: L("loading shot %s" % e)
            try:
                geo.Activate(); shot("03_ansys_geometry.png", "geometry")
                bodies[0].Activate(); shot("04_tough2000_assignment.png", "body details")
            except Exception as e: L("geo shot %s" % e)
            try:
                fr.Activate(); shot("11_mechanical_stress_strain_chart.png", "reaction chart")
            except Exception as e: L("chart shot %s" % e)
    W("mesh_metrics.csv", summary, "level,element_size_mm,nodes,elements,solution_status")
    L("DONE")
except SystemExit:
    L("probe only done")
except Exception as e:
    L("ERR " + traceback.format_exc())
