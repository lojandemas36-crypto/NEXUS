# NEXUS User Guide

## What NEXUS does

NEXUS runs work as connected workflows. When it cannot confirm what happened, it sends the task to **Needs review** instead of treating an uncertain result as success. A human decision can be recorded through the decision feature. The dashboard is a read-only view of workflow history; it does not change tasks or decisions.

## Starting NEXUS

Double-click **C:\Users\Admin\Desktop\NEXUS.bat**. A console window stays open while NEXUS runs, the launcher extracts the runtime to `%TEMP%\nexus_runtime\nexus180`, and your browser opens to the dashboard. To stop NEXUS, focus the console and press **Ctrl+C**.

## What you will see

- **Workflows** lists recorded workflows and their latest status, such as completed, running, or needs review.
- **Needs review** highlights tasks whose outcome could not be confirmed. Check the reason and attempt details before deciding what to do.
- **Decision history** appears when decision events are present in dashboard history.
- **Health** tells you whether the dashboard is responding.

The demo workflows are planned for a later step. The examples will cover normal completion, an uncertain result, a human decision, a NoEffect retry, and a task reaching its deadline.

**Live dashboard data is being wired in the next build; current dashboard shows seed/empty state.**

## Dashboard addresses

- Dashboard: http://127.0.0.1:8765/
- Health check: http://127.0.0.1:8765/healthz — a healthy dashboard responds with `{"status": "ok"}`.

The launcher forces port **8765**. The sealed runtime’s default is **18765**, but the launcher overrides it to 8765.

## If something goes wrong

- **“This site can’t be reached”**: check that the NEXUS console is still running. Start NEXUS.bat again if needed.
- **Port 8765 is in use**: close any other NEXUS console window first, then start NEXUS.bat again.
- **The browser did not open**: manually go to http://127.0.0.1:8765/.
- **The dashboard shows seed/empty data or data unavailable**: this build does not yet connect live orchestrator history to the dashboard. Leave the console open and report the message; do not edit or replace database files.

## What NEXUS is not

NEXUS is a local, single-user tool. Its dashboard is intended for this computer only. It is not a public website, does not provide multi-user access, and does not make cloud API calls during normal local operation. Live-model validation was performed separately with local Ollama.

## Version

NEXUS v1.1 engineering was declared complete on 13 November 2026. The release includes five sealed artifacts: 1.5.1, 1.6.0, 1.7.0, 1.8.0, and Dashboard Option B. Local live-model validation used Ollama with qwen3.5:2b.