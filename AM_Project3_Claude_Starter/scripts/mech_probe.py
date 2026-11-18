# IronPython inside Mechanical
OUT=r"C:\Users\jmathew7\Downloads\AM-ANSYS-Project-3\AM_Project3_Claude_Starter\OUTPUTS_Folder\Logs\mech_probe.txt"
lines=[]
def L(m): lines.append(str(m))
try:
    m=ExtAPI.DataModel.Project.Model
    g=m.Geometry
    L("version "+str(ExtAPI.Application.Version) if hasattr(ExtAPI.Application,'Version') else "nover")
    L("geo children %d"%g.Children.Count)
    L([a for a in dir(g) if not a.startswith('_')])
    for part in g.Children:
        L("part "+part.Name+" children %d"%part.Children.Count)
        for b in part.Children:
            L(["body",b.Name,b.Volume,b.Mass if hasattr(b,'Mass') else None, str(b.Material)])
            L([a for a in dir(b) if not a.startswith('_')])
            gb=b.GetGeoBody()
            L([a for a in dir(gb) if not a.startswith('_')])
            break
    L("units "+str(ExtAPI.Application.ActiveUnitSystem))
except Exception as e:
    import traceback; L("ERR "+traceback.format_exc())
f=open(OUT,"w"); f.write("\n".join(lines)); f.close()
