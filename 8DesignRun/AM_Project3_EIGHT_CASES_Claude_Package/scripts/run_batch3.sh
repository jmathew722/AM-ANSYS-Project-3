#!/bin/bash
cd "$(dirname "$0")/.."
while [ ! -f FINALUPLAD_Folder/Logs/batch2.done ]; do sleep 30; done
export CASE_TIMEOUT=21600 DISP_MM=0.9 FORCE_N=1000
for c in BCCZ_Topo_Optimized Octet_Truss_Topo_Optimized; do
  CASE_ID=$c TAG=pilot MODE=force MESH_SIZES=0.6 INIT_SUB=20 MAX_SUB=80 scripts/run_case.sh
done
for c in Fluorite_Truss_Topo_Optimized BCCZ_Topo_Optimized Octet_Truss_Topo_Optimized; do
  CASE_ID=$c TAG=v1 MODE=disp MESH_SIZES=0.6,0.45,0.35 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
done
echo done > FINALUPLAD_Folder/Logs/batch3.done
