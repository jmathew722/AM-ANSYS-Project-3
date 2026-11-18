"""Geometry audit from the STL tessellations shipped next to each SLDPRT/IGS (estimates; NOT SolidWorks Mass Properties).
Usage: python scripts/00_preflight_stl_audit.py  -> OUTPUTS_Folder/Geometry_Mass_Properties/stl_audit.csv"""
import numpy as np, struct, os, hashlib, csv, glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO=os.path.dirname(ROOT)
def load_stl(p):
    with open(p,'rb') as f: d=f.read()
    n=struct.unpack('<I',d[80:84])[0]
    if 84+50*n==len(d):
        a=np.frombuffer(d[84:],dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]),count=n)
        return a['v'].astype(float)
    import re
    v=np.array(re.findall(rb'vertex\s+(\S+)\s+(\S+)\s+(\S+)',d),dtype=float); return v.reshape(-1,3,3)
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<24),b''): h.update(b)
    return h.hexdigest()
rows=[]
for stl in sorted(glob.glob(os.path.join(GEO,'*','*.stl'))):
    t=load_stl(stl); lo=t.reshape(-1,3).min(0); hi=t.reshape(-1,3).max(0)
    vol=np.einsum('ij,ij->i',t[:,0],np.cross(t[:,1],t[:,2])).sum()/6
    # edge-manifold check
    e={}
    key=np.round(t.reshape(-1,3),5)
    idx={}; ids=np.array([idx.setdefault(tuple(k),len(idx)) for k in key]).reshape(-1,3)
    for tri in ids:
        for a,b in ((0,1),(1,2),(2,0)):
            k=(min(tri[a],tri[b]),max(tri[a],tri[b])); e[k]=e.get(k,0)+1
    bad=sum(1 for c in e.values() if c!=2)
    d=os.path.basename(os.path.dirname(stl)); env=np.prod(hi-lo)
    r=dict(folder=d,file=os.path.basename(stl),triangles=len(t),bbox_x=hi[0]-lo[0],bbox_y=hi[1]-lo[1],bbox_z=hi[2]-lo[2],
      stl_volume_mm3=abs(vol),envelope_mm3=env,rel_density_est=abs(vol)/env,nonmanifold_edges=bad,sha256_stl=sha(stl))
    rows.append(r); print(r)
out=os.path.join(ROOT,'OUTPUTS_Folder','Geometry_Mass_Properties','stl_audit.csv')
os.makedirs(os.path.dirname(out),exist_ok=True)
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
