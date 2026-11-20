out = []
try:
    out.append("MethodType: " + str([a for a in dir(MethodType) if not a.startswith('_')]))
except Exception as e: out.append("MethodType err %s" % e)
for nm in ("MeshMethodAlgorithm", "MethodAlgorithm", "MeshMethodType", "AlgorithmType", "TetrahedronAlgorithm", "MeshAlgorithm"):
    try: out.append(nm + ": " + str([a for a in dir(eval(nm)) if not a.startswith('_')]))
    except Exception as e: out.append(nm + " err")
try:
    mm = ExtAPI.DataModel.Project.Model.Mesh
    out.append("MeshProps: " + str([a for a in dir(mm) if not a.startswith('_') and any(k in a for k in ("Capture", "Curv", "Prox", "Size", "Adapt", "Span", "Smooth", "Transition", "Growth", "Defeature", "Relevance"))]))
    meth = mm.AddAutomaticMethod()
    out.append("MethodProps: " + str([a for a in dir(meth) if not a.startswith('_')]))
except Exception as e: out.append("err %s" % e)
open(CFG['simdir'] + "_names.txt", "w").write("\n".join(out))
