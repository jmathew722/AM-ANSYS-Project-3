#!/bin/bash
cd "$(dirname "$0")/.."
export TAG=probeaxis PROBE_ONLY=1 CASE_TIMEOUT=2400 MECH_SCRIPT=mech_run_axis.py
SW='C:\Users\jmathew7\Downloads\AM-ANSYS-Project-3\8DesignRun\SLDPRT 2025\Cube Topo.SLDPRT'
for c in BCCZ_Original Cube_Original Fluorite_Truss_Original Octet_Truss_Original Fluorite_Truss_Topo_Optimized BCCZ_Topo_Optimized Octet_Truss_Topo_Optimized; do CASE_ID=$c scripts/run_case.sh; done
GEOM="$SW" CASE_ID=Cube_Topo_Optimized scripts/run_case.sh
echo done > FINALUPLAD_Folder/Logs/probeaxis.done
