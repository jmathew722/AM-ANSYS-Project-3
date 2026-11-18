import hashlib,os,csv,glob
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
rows=[]
for f in sorted(glob.glob('*/*')):
    if f.startswith(('AM_Project3','.git')) or os.path.isdir(f) or os.path.basename(f).startswith('~$'): continue
    h=hashlib.sha256()
    with open(f,'rb') as fh:
        for b in iter(lambda:fh.read(1<<24),b''): h.update(b)
    rows.append([f.replace(os.sep,'/'),os.path.getsize(f),h.hexdigest()])
with open('AM_Project3_Claude_Starter/OUTPUTS_Folder/Geometry_Mass_Properties/cad_input_inventory_sha256.csv','w',newline='') as o:
    w=csv.writer(o);w.writerow(['file','bytes','sha256']);w.writerows(rows)
print(len(rows))
