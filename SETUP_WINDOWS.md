# Set up NEXUS on Windows

## Before you start

Install Python 3.8 or newer and make sure `python` works from Command Prompt or PowerShell.

The NEXUS 1.8.0 sealed archive is intentionally not included in this public repository. The archive owner keeps sealed files off public infrastructure. See [releases/HASHES.md](releases/HASHES.md) to identify and verify the archive.

## Option A: Owner machine

If the archive is already in a `NEXUS_CHECKPOINTS` folder beside the repository root, double-click `live-runtime\NEXUS.bat`. The launcher checks its own folder first, then the repository root's `NEXUS_CHECKPOINTS` folder.

## Option B: New machine

1. Create a `NEXUS_CHECKPOINTS` folder beside the `live-runtime` folder.
2. Place `NEXUS_1_8_0_phaseD_20261113.zip` in that folder. Alternatively, set `NEXUS_SEAL_PATH` to the full path of that ZIP file.
3. Double-click `live-runtime\NEXUS.bat`.

The batch file stages a temporary copy of the archive for the existing launcher. The sealed archive itself remains unchanged.

## Open and stop NEXUS

After startup, open [http://127.0.0.1:8765/](http://127.0.0.1:8765/) for the dashboard. Check [http://127.0.0.1:8765/healthz](http://127.0.0.1:8765/healthz) for the health response. Press **Ctrl+C** in the console window to stop the runtime.
