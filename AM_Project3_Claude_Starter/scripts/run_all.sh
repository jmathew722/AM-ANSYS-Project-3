#!/bin/bash
cd "$(dirname "$0")/.."
G='C:\Users\jmathew7\Downloads\AM-ANSYS-Project-3'
export DIAG=0 CASE_TIMEOUT=14400
run(){ DESIGN=$1 TAG=$2 IGES="$3" MODE=$4 DISP_MM=0.9 FORCE_N=1000 MESH_SIZES=$5 INIT_SUB=$6 MAX_SUB=$7 scripts/run_case.sh; }
run Design_01 v1 "$G\BCCZ_Topo_Smooth\BCCZ_Topo_Smooth_6mm_rho26.IGS" disp 0.5,0.35,0.25 60 240
run Design_02 v1 "$G\Fluorite_Topo_Smooth\Fluorite_Topo_Smooth_6mm_rho49.IGS" disp 0.5,0.35,0.25 60 240
run Design_03 pilot "$G\Octet_Truss_Smooth\Octet Truss Optimized 2025.IGS" force 0.35 20 80
run Design_01 pilot "$G\BCCZ_Topo_Smooth\BCCZ_Topo_Smooth_6mm_rho26.IGS" force 0.35 20 80
run Design_02 pilot "$G\Fluorite_Topo_Smooth\Fluorite_Topo_Smooth_6mm_rho49.IGS" force 0.35 20 80
echo ALLDONE > OUTPUTS_Folder/Logs/run_all.done
