#!/bin/bash
# usage: CASE_ID=.. TAG=.. MODE=.. MESH_SIZES=.. scripts/run_case.sh
cd "$(dirname "$0")/.."
N=$(/c/Program\ Files/Python314/python.exe -c "import json,os;print([c['folder'] for c in json.load(open('config/cases_resolved.json')) if c['case_id']=='$CASE_ID'][0])")
timeout ${CASE_TIMEOUT:-5400} "/c/Program Files/ANSYS Inc/v251/Framework/bin/Win64/RunWB2.exe" -B -R scripts/wb_run_case2.wbjn > "FINALUPLAD_Folder/Logs/${N}_${TAG}_stdout.log" 2>&1
echo "exit $?" >> "FINALUPLAD_Folder/Logs/${N}_${TAG}_stdout.log"
