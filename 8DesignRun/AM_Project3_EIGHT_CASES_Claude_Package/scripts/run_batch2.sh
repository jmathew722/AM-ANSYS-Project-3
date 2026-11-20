#!/bin/bash
cd "$(dirname "$0")/.."
while [ ! -f FINALUPLAD_Folder/Logs/batch1.done ]; do sleep 30; done
export CASE_TIMEOUT=10800 DISP_MM=0.9 FORCE_N=1000
SW='C:\Users\jmathew7\Downloads\AM-ANSYS-Project-3\8DesignRun\SLDPRT 2025\Cube Topo.SLDPRT'
GEOM="$SW" CASE_ID=Cube_Topo_Optimized TAG=pilot MODE=force MESH_SIZES=0.35 INIT_SUB=20 MAX_SUB=80 scripts/run_case.sh
GEOM="$SW" CASE_ID=Cube_Topo_Optimized TAG=v1 MODE=disp MESH_SIZES=0.5,0.35,0.25,0.18 INIT_SUB=60 MAX_SUB=240 scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/batch2.done
