#!/bin/bash
cd "$(dirname "$0")/.."
export CASE_TIMEOUT=43200 DISP_MM=0.9 FORCE_N=1000 MECH_SCRIPT=mech_run_pi.py MESH_METHOD=pi MESH_PROPS="CaptureCurvature=False;CaptureProximity=False"
CASE_ID=Octet_Truss_Topo_Optimized TAG=pilotpi3 MODE=force MESH_SIZES=0.9 INIT_SUB=20 MAX_SUB=80 scripts/run_case.sh
CASE_ID=Octet_Truss_Topo_Optimized TAG=v5 MODE=disp MESH_SIZES=1.4,1.0,0.8 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/batch9.done
