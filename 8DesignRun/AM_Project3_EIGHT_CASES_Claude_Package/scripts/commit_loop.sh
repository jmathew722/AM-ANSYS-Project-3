#!/bin/bash
cd /c/Users/jmathew7/Downloads/ANSYS
while true; do
  git add -A 8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package ':!*.lic' ':!*license*' 2>/dev/null
  git commit -q -m "FINALANALYSIS periodic sync $(date +%H:%M)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" 2>/dev/null
  git push -q origin FINALANALYSIS >> /tmp/push.log 2>&1
  [ -f 8DesignRun/AM_Project3_EIGHT_CASES_Claude_Package/FINALUPLAD_Folder/Logs/final.done ] && [ -f /tmp/stoploop ] && break
  sleep 1800
done
