#!/bin/bash
cd "$(dirname "$0")/.."
export TAG=probe PROBE_ONLY=1 CASE_TIMEOUT=1500
for c in Cube_Original BCCZ_Original Fluorite_Truss_Original Octet_Truss_Original Cube_Topo_Optimized BCCZ_Topo_Optimized Fluorite_Truss_Topo_Optimized Octet_Truss_Topo_Optimized; do
  CASE_ID=$c scripts/run_case.sh
done
echo done > FINALUPLAD_Folder/Logs/probe_all.done
