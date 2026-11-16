# NEXUS — Workflow Orchestrator with Uncertain-Resume

> **Run workflows that know when to ask for help.**

![Version](https://img.shields.io/badge/version-v1.1-0a6e0a)
![License](https://img.shields.io/badge/license-MIT-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

NEXUS runs multi-step workflows and makes uncertainty visible. When a task cannot be safely resolved, the workflow can pause for review instead of treating an unknown result as success. A local, read-only dashboard helps operators inspect workflow history and status.

## Features

- **Workflow orchestration:** define tasks, dependencies, and handlers, then run them as a workflow.
- **Uncertain-resume:** preserve unresolved outcomes for review instead of silently reporting success.
- **Decision API:** record an explicit human decision for a task that needs review.
- **NoEffect retry:** support bounded retry handling for operations that report no side effect.
- **Read-only dashboard:** inspect workflows, runs, and review items through a local SQLite-backed web interface.
- **Live-LLM validation:** validated locally with Ollama and the `qwen3.5:2b` model at zero API cost.

## Quick start

On the prepared Windows setup, double-click `NEXUS.bat`. Your browser opens to <http://127.0.0.1:8765/>. Stop the local runtime with **Ctrl+C** in its console window.

For a fresh Windows setup, follow [SETUP_WINDOWS.md](SETUP_WINDOWS.md). [GitHub repository](https://github.com/lojandemas36-crypto/nexus) · [Live landing page](https://lojandemas36-crypto.github.io/nexus/)

## Architecture

```text
┌──────────────────┐    extract/run    ┌──────────────────┐
│ Sealed archives  │ ────────────────> │ Live runtime     │
│ (versioned ZIPs) │                   │ (local process)  │
└──────────────────┘                   └────────┬─────────┘
                                                 │ writes
                                                 v
                                       ┌──────────────────┐
                                       │ SQLite database │
                                       └────────┬─────────┘
                                                │ read-only queries
                                                v
                                       ┌──────────────────┐
                                       │ Local dashboard  │
                                       └──────────────────┘
```

## Screenshots

Screenshots will be added to this repository:

- Dashboard overview: `screenshots/nexus_dashboard_overview.png`
- Capabilities page: `screenshots/nexus_capabilities.png`
- Workflow detail: `screenshots/nexus_workflow_detail.png`

## Technical specs

- Python 3.8 or newer
- Python standard library; no third-party runtime dependencies
- SQLite for workflow history and dashboard reads
- Versioned sealed checkpoints with SHA-256 manifests
- Local dashboard binding: `127.0.0.1:8765` in the prepared launcher configuration

## Credits

Built by Lojan Demas, 2026.

## License

MIT. See the included `LICENSE` file for the full license text.


