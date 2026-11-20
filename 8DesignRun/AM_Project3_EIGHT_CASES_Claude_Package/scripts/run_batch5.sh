#!/bin/bash
cd "$(dirname "$0")/.."
while [ ! -f FINALUPLAD_Folder/Logs/batch3.done ]; do sleep 30; done
export CASE_TIMEOUT=10800 DISP_MM=0.9 FORCE_N=1000
CASE_ID=Fluorite_Truss_Topo_Optimized TAG=pilot2 MODE=force MESH_SIZES=0.6 INIT_SUB=20 MAX_SUB=80 scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/batch5.done
