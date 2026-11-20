#!/bin/bash
cd "$(dirname "$0")/.."
while [ ! -f FINALUPLAD_Folder/Logs/batch4.done ]; do sleep 30; done
export CASE_TIMEOUT=21600 DISP_MM=0.9 FORCE_N=1000
for c in Octet_Truss_Original Fluorite_Truss_Original; do
 CASE_ID=$c TAG=v3 MODE=disp MESH_SIZES=0.25,0.18,0.13,0.10,0.08 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
done
echo done > FINALUPLAD_Folder/Logs/batch6.done
