#!/bin/bash
cd "$(dirname "$0")/.."
export CASE_TIMEOUT=10800 DISP_MM=0.9 FORCE_N=1000
for c in Cube_Original BCCZ_Original Fluorite_Truss_Original Octet_Truss_Original; do
  CASE_ID=$c TAG=pilot MODE=force MESH_SIZES=0.35 INIT_SUB=20 MAX_SUB=80 scripts/run_case.sh
  CASE_ID=$c TAG=v1 MODE=disp MESH_SIZES=0.5,0.35,0.25,0.18 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
done
echo done > FINALUPLAD_Folder/Logs/batch1.done
