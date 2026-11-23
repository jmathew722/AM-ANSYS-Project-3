#!/bin/bash
# commit+push to FINALIZE every 30 min (and once immediately). Stop by creating /tmp/stopsync or touching FINALUPLAD_Folder/Logs/finalize.done then one final pass.
cd /c/Users/jmathew7/Downloads/ANSYS
PY="/c/Program Files/Python314/python.exe"
LOG=8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package/FINALUPLAD_Folder/Logs/sync.log
while true; do
  "$PY" 8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package/scripts/bigfiles.py >> $LOG 2>&1
  git add -A -- . ':!*.lic' ':!*license*' ':!*.env' >> $LOG 2>&1
  git commit -q -m "Auto-save: FINALIZE $(date '+%Y-%m-%d %H:%M')

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" >> $LOG 2>&1
  git push -q origin FINALIZE >> $LOG 2>&1 || echo "PUSH FAILED $(date)" >> $LOG
  echo "synced $(date) $(git rev-parse --short HEAD)" >> $LOG
  [ -f 8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package/FINALUPLAD_Folder/Logs/finalize.done ] && break
  for i in $(seq 1 180); do [ -f /tmp/stopsync ] && exit 0; sleep 10; done
done
