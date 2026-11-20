#!/bin/bash
cd "$(dirname "$0")/.."
while [ ! -f FINALUPLAD_Folder/Logs/batch1.done ]; do sleep 30; done
export CASE_TIMEOUT=10800 DISP_MM=0.9 FORCE_N=1000
CASE_ID=BCCZ_Original TAG=pilot2 MODE=force MESH_SIZES=0.35 INIT_SUB=20 MAX_SUB=80 scripts/run_case.sh
CASE_ID=BCCZ_Original TAG=v2 MODE=disp MESH_SIZES=0.5,0.35,0.25,0.18 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/batch4.done
