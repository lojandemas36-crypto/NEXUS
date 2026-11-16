# NEXUS v1.1.0

NEXUS v1.1.0 brings together the sealed work from 1.5.1 through 1.8.0: workflow safety and uncertain-resume behavior, explicit decisions, a local dashboard, and Phase D retry and deadline handling. The dashboard is available as a standalone sealed artifact as well as part of the runtime release.

## What shipped

- **1.5.1:** Phase B workflow stability, W1 registry changes, G-1 guard, and the orchestrator boundary fix for uncertain outcomes.
- **1.6.0:** Phase C `decide()` API, `NoEffect` type, decision audit behavior, and contract tests.
- **1.7.0:** Canonical single-process runtime integrating the orchestrator and dashboard.
- **1.8.0:** Phase D NoEffect retry integration and deadline characterization work.
- **Dashboard Option B:** Standalone standard-library HTTP dashboard with read-only SQLite access.

The five seal names, dates, and full SHA-256 values are recorded in [releases/HASHES.md](releases/HASHES.md). The sealed archives themselves are not included in this repository.

## Live-LLM validation

The sealed runtime was validated locally through Ollama using `qwen3.5:2b` at zero API cost. The recorded run completed with `LIVE_LLM_PASS`; no API key or network egress was used for that local validation.

## Known limitations

- The Windows launcher requires access to the 1.8.0 sealed archive locally; the archive is intentionally distributed separately.
- The prepared runtime is single-user and runs on one machine.
- The dashboard binds to localhost (`127.0.0.1`); LAN access is not part of this release.
- Phase D retry helpers remain opt-in for specific task configurations.
