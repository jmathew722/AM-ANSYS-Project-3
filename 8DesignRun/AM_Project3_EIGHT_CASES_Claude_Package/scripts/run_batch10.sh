#!/bin/bash
cd "$(dirname "$0")/.."
export CASE_TIMEOUT=43200 DISP_MM=0.9 FORCE_N=1000 MECH_SCRIPT=mech_run_pi.py MESH_METHOD=pi MESH_PROPS="CaptureCurvature=False;CaptureProximity=False"
CASE_ID=Fluorite_Truss_Topo_Optimized TAG=v5 MODE=disp MESH_SIZES=0.6,0.45,0.35 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/batch10.done
