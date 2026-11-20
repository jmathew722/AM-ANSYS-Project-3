#!/bin/bash
cd "$(dirname "$0")/.."
export CASE_TIMEOUT=28800 DISP_MM=0.9 FORCE_N=1000
CASE_ID=Fluorite_Truss_Topo_Optimized TAG=pilot2 MODE=force MESH_SIZES=0.6 INIT_SUB=20 MAX_SUB=80 scripts/run_case.sh
CASE_ID=Fluorite_Truss_Topo_Optimized TAG=v4 MODE=disp MESH_SIZES=0.6,0.45,0.35 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/batch7.done
