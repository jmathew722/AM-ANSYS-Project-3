Each Workbench .wbpz archive (a zip) is split into 90 MB parts (GitHub 100 MB file limit).
Reassemble:  cat NAME.wbpz.part* > NAME.wbpz   (Windows: copy /b NAME.wbpz.part000+NAME.wbpz.part001+... NAME.wbpz)
Then open in Workbench via File > Restore Archive. Verify with sha256 listed in ../Logs/manifest.json when possible.
