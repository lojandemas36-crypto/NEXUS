"""NEXUS v1.1 launcher: extract sealed 1.8.0 and start the local dashboard."""
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import webbrowser
import zipfile

CK = os.path.join(
    os.environ["USERPROFILE"], "Documents", "ALL NEXUS PROJECT FILES AND DATES",
    "NEXUS_WORK", "work_PhaseB", "NEXUS_CHECKPOINTS")
Z180 = os.path.join(CK, "NEXUS_1_8_0_phaseD_20261113.zip")
TEMP_ROOT = os.path.realpath(tempfile.gettempdir())
DST = os.path.abspath(os.environ.get(
    "NEXUS_RUNTIME_ROOT", os.path.join(TEMP_ROOT, "nexus_runtime")))
PORT = int(os.environ.get("NEXUS_PORT", "8765"))


def fail(message, code=1):
    print("ERROR: " + message, file=sys.stderr)
    input("Press Enter to exit...")
    raise SystemExit(code)


def within_temp(path):
    try:
        return (os.path.commonpath([TEMP_ROOT, os.path.realpath(path)]) == TEMP_ROOT
                and os.path.realpath(path) != TEMP_ROOT)
    except ValueError:
        return False


def dashboard_ready(url):
    try:
        with urllib.request.urlopen(url + "workflows", timeout=1.0) as response:
            sample = response.read(512).decode("utf-8", "replace")
            return response.status == 200 and "NEXUS" in sample
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


if not os.path.isfile(Z180):
    fail("NEXUS 1.8.0 seal not found at: " + Z180)
if not within_temp(DST):
    fail("runtime extraction path must be a child of the Windows TEMP folder")
if not 1 <= PORT <= 65535:
    fail("port must be between 1 and 65535")

url = f"http://127.0.0.1:{PORT}/"
if dashboard_ready(url):
    print("An NEXUS dashboard is already running at " + url)
    if os.environ.get("NEXUS_NO_BROWSER") != "1":
        webbrowser.open(url)
    raise SystemExit(0)

# Check before removing/recreating the extraction folder. A non-NEXUS listener
# on the requested port must not cause the existing runtime files to be erased.
probe = socket.socket()
try:
    probe.bind(("127.0.0.1", PORT))
except OSError:
    fail(f"port {PORT} is occupied but no NEXUS dashboard answered. Close the "
         "other process or choose another port; the existing extraction was left untouched.", 2)
finally:
    probe.close()

if os.path.isdir(DST):
    shutil.rmtree(DST)
os.makedirs(DST, exist_ok=True)

print("Extracting NEXUS 1.8.0 seal...")
with zipfile.ZipFile(Z180) as archive:
    archive.extractall(DST)
base = os.path.join(DST, "nexus180")
if not os.path.isdir(base):
    fail("the 1.8.0 archive did not contain the expected nexus180 folder")

live_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nexus_live_runtime.py")
if not os.path.isfile(live_src):
    fail("live runtime wrapper is missing: " + live_src)
shutil.copy2(live_src, os.path.join(base, "nexus_live_runtime.py"))
print("[Launcher] Live runtime copied into the disposable extraction.")

ready_url = url + "workflows"
print("Starting NEXUS demo workflows and dashboard...")
process = subprocess.Popen(
    [sys.executable, "nexus_live_runtime.py", "--port", str(PORT), "--seed"], cwd=base)

try:
    deadline = time.monotonic() + 30.0
    ready = False
    while time.monotonic() < deadline:
        if process.poll() is not None:
            fail(f"NEXUS exited during startup (exit code {process.returncode}). "
                 "Read the runtime error above.", process.returncode or 1)
        if dashboard_ready(url):
            ready = True
            break
        time.sleep(0.25)

    if not ready:
        process.terminate()
        process.wait(timeout=5)
        fail("dashboard did not become ready within 30 seconds. Check the runtime output and port.", 2)

    print("[Launcher] Dashboard data route is ready: " + ready_url)
    if os.environ.get("NEXUS_NO_BROWSER") != "1":
        webbrowser.open(url)
        print("[Launcher] Dashboard opened in your browser.")
    else:
        print("[Launcher] Browser opening suppressed by NEXUS_NO_BROWSER=1.")
    print("Press Ctrl+C in this window to stop NEXUS.")
    process.wait()
except KeyboardInterrupt:
    print("\n[Launcher] Stopping NEXUS...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
