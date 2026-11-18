#!/bin/bash
# usage: DESIGN=.. TAG=.. IGES=.. MODE=.. MESH_SIZES=.. DISP_MM=.. scripts/run_case.sh
cd "$(dirname "$0")/.."
timeout ${CASE_TIMEOUT:-5400} "/c/Program Files/ANSYS Inc/v251/Framework/bin/Win64/RunWB2.exe" -B -R scripts/wb_run_design.wbjn > OUTPUTS_Folder/Logs/${DESIGN}_${TAG}_stdout.log 2>&1
echo "exit $?" >> OUTPUTS_Folder/Logs/${DESIGN}_${TAG}_stdout.log
