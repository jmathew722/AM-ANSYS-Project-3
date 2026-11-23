#!/bin/bash
# FINALANALYSIS reruns: Design 8 first (nothing usable), then 6, then 2. Sequential: one license/solver at a time.
cd "$(dirname "$0")/.."
export CASE_TIMEOUT=43200 DISP_MM=0.9 FORCE_N=1000 MECH_SCRIPT=mech_run_pi.py MESH_METHOD=pi MESH_PROPS="CaptureCurvature=False;CaptureProximity=False"
CASE_ID=Octet_Truss_Topo_Optimized TAG=v5 MODE=disp MESH_SIZES=1.4,1.0,0.8 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
CASE_ID=Fluorite_Truss_Topo_Optimized TAG=v5 MODE=disp MESH_SIZES=1.2,0.9,0.7 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
CASE_ID=BCCZ_Topo_Optimized TAG=v5 MODE=disp MESH_SIZES=2.0,1.2,0.8 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/final.done
