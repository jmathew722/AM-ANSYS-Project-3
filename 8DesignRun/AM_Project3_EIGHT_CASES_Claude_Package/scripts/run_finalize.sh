#!/bin/bash
# Single-mesh runs, finest size that completes. Falls back coarser on failure.
cd "$(dirname "$0")/.."
export CASE_TIMEOUT=28800 DISP_MM=0.9 FORCE_N=1000 MECH_SCRIPT=mech_run_pi.py MESH_METHOD=pi MESH_PROPS="CaptureCurvature=False;CaptureProximity=False" MODE=disp INIT_SUB=60 MAX_SUB=240
run() { # case tag sizes...
  c=$1; t=$2; shift 2
  for s in "$@"; do
    d=$(/c/Program\ Files/Python314/python.exe -c "import json;print([x['folder'] for x in json.load(open('config/cases_resolved.json')) if x['case_id']=='$c'][0])")
    rm -rf "FINALUPLAD_Folder/Cases/$d/Raw_Data/$t"
    echo "$(date) $c size=$s" >> FINALUPLAD_Folder/Logs/finalize_runs.log
    CASE_ID=$c TAG=$t MESH_SIZES=$s scripts/run_case.sh
    if grep -q "^DONE" "FINALUPLAD_Folder/Logs/${d}_${t}_mech.log" 2>/dev/null; then echo "$(date) $c OK size=$s" >> FINALUPLAD_Folder/Logs/finalize_runs.log; return 0; fi
    echo "$(date) $c FAILED size=$s: $(tail -c 300 FINALUPLAD_Folder/Logs/${d}_${t}_mech.log | tr '\n' ' ')" >> FINALUPLAD_Folder/Logs/finalize_runs.log
  done
  echo "$(date) $c BLOCKED all sizes" >> FINALUPLAD_Folder/Logs/finalize_runs.log
}
run Fluorite_Truss_Topo_Optimized v5 0.6 0.9 1.2
run BCCZ_Topo_Optimized v5 1.0 1.5 2.0
run Octet_Truss_Topo_Optimized v5 1.0 1.4 2.0
echo done > FINALUPLAD_Folder/Logs/finalize_solves.done
