"""Find files >90MB under repo, zip (and split into <90MB parts if still large) into Archive_Parts/, exclude originals from git."""
import os, sys, zipfile, subprocess
ROOT = r"C:\Users\jmathew7\Downloads\ANSYS"
PKG = os.path.join(ROOT, "8DesignRun", "AM_Project3_EIGHT_CASES_Claude_Package", "FINALUPLAD_Folder")
PARTS = os.path.join(PKG, "Archive_Parts")
LIM = 90 * 1024 * 1024
EXC = os.path.join(ROOT, ".git", "info", "exclude")
os.makedirs(PARTS, exist_ok=True)
excl = set(open(EXC).read().splitlines()) if os.path.exists(EXC) else set()
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d != ".git"]
    for f in fn:
        p = os.path.join(dp, f)
        if os.path.abspath(dp) == os.path.abspath(PARTS) or ".part" in f: continue
        try: sz = os.path.getsize(p)
        except OSError: continue
        if sz <= LIM: continue
        if subprocess.call(["git", "-C", ROOT, "check-ignore", "-q", os.path.relpath(p, ROOT)]) == 0 and (sz > 1024**3 or f.lower().rsplit(".", 1)[-1] in ("rst", "rth", "full", "esav", "emat")):
            note = os.path.join(PARTS, f + ".LOCAL_ONLY.txt")
            if not os.path.exists(note): open(note, "w").write("%s is %.1f GB: too large to push to GitHub even when split; kept locally only (git-ignored). Regenerate by re-running the case or copy from the original machine.\n" % (f, sz / 1024**3))
            continue
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if rel in excl: continue
        base = os.path.join(PARTS, f)
        if not (os.path.exists(base + ".zip") or os.path.exists(base + ".zip.part000")):
            zp = base + ".zip"
            with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z: z.write(p, f)
            if os.path.getsize(zp) > LIM:
                with open(zp, "rb") as src:
                    i = 0
                    while True:
                        chunk = src.read(LIM - 1024 * 1024)
                        if not chunk: break
                        open("%s.part%03d" % (zp, i), "wb").write(chunk); i += 1
                os.remove(zp)
            open(base + ".REJOIN.txt", "w").write(
                "Original %s exceeded GitHub's 100 MB limit.\nRejoin: copy /b %s.zip.part000+%s.zip.part001+... %s.zip (or cat parts > file.zip), then unzip.\n" % (f, f, f, f))
        open(EXC, "a").write(rel + "\n"); excl.add(rel)
        subprocess.call(["git", "-C", ROOT, "rm", "--cached", "-q", "--ignore-unmatch", rel])
        print("split/excluded", rel, sz)
