@echo off
setlocal
 title NEXUS v1.1 Live Launcher
color 0A
set "SEAL_NAME=NEXUS_1_8_0_phaseD_20261113.zip"
set "SEAL_PATH="

if exist "%~dp0NEXUS_CHECKPOINTS\%SEAL_NAME%" set "SEAL_PATH=%~dp0NEXUS_CHECKPOINTS\%SEAL_NAME%"
if not defined SEAL_PATH if exist "%~dp0..\NEXUS_CHECKPOINTS\%SEAL_NAME%" set "SEAL_PATH=%~dp0..\NEXUS_CHECKPOINTS\%SEAL_NAME%"
if not defined SEAL_PATH if defined NEXUS_SEAL_PATH if exist "%NEXUS_SEAL_PATH%" set "SEAL_PATH=%NEXUS_SEAL_PATH%"

if not defined SEAL_PATH (
    echo NEXUS 1.8.0 seal was not found.
    echo Place %SEAL_NAME% in NEXUS_CHECKPOINTS or set NEXUS_SEAL_PATH to the archive path.
    echo See SETUP_WINDOWS.md for setup instructions.
    echo.
    pause
    exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on PATH. Install Python 3.8 or newer, then try again.
    echo See SETUP_WINDOWS.md for setup instructions.
    echo.
    pause
    exit /b 1
)

set "TEMP_PROFILE=%TEMP%\NEXUS_profile_%RANDOM%_%RANDOM%"
set "EXPECTED_SEAL=%TEMP_PROFILE%\Documents\ALL NEXUS PROJECT FILES AND DATES\NEXUS_WORK\work_PhaseB\NEXUS_CHECKPOINTS\%SEAL_NAME%"
mkdir "%TEMP_PROFILE%\Documents\ALL NEXUS PROJECT FILES AND DATES\NEXUS_WORK\work_PhaseB\NEXUS_CHECKPOINTS" >nul 2>nul
if errorlevel 1 (
    echo Could not prepare the temporary launcher profile.
    pause
    exit /b 1
)
copy /b /y "%SEAL_PATH%" "%EXPECTED_SEAL%" >nul
if errorlevel 1 (
    echo Could not stage the seal into the temporary launcher profile.
    rmdir /s /q "%TEMP_PROFILE%"
    pause
    exit /b 1
)

set "ORIGINAL_USERPROFILE=%USERPROFILE%"
set "USERPROFILE=%TEMP_PROFILE%"
echo.
echo   ============================================
echo    NEXUS v1.1 - Live Workflow Orchestrator
echo   ============================================
echo.
echo   Dashboard: http://127.0.0.1:8765/
echo   Health:    http://127.0.0.1:8765/healthz
echo.
echo   Press Ctrl+C to stop the runtime.
echo.
python "%~dp0nexus_launcher.py"
set "LAUNCH_EXIT=%ERRORLEVEL%"
set "USERPROFILE=%ORIGINAL_USERPROFILE%"
rmdir /s /q "%TEMP_PROFILE%" >nul 2>nul
echo.
echo   NEXUS stopped.
pause
exit /b %LAUNCH_EXIT%
