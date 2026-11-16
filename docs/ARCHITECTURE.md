# NEXUS Architecture

## System diagram

```text
┌──────────────────────┐   extract from sealed release   ┌──────────────────────┐
│ Sealed checkpoints   │ ──────────────────────────────> │ Local live runtime   │
│ versioned ZIP + hash │                                  │ orchestrator process│
└──────────────────────┘                                  └──────────┬───────────┘
                                                                     │ append history
                                                                     v
                                                          ┌──────────────────────┐
                                                          │ SQLite live database│
                                                          └──────────┬───────────┘
                                                                     │ mode=ro queries
                                                                     v
                                                          ┌──────────────────────┐
                                                          │ Read-only dashboard │
                                                          │ 127.0.0.1 only       │
                                                          └──────────────────────┘
        ┌──────────────────────┐
        │ Windows launcher     │ ── extracts to TEMP, starts runtime, opens browser
        └──────────────────────┘
```

## Components

- **Sealed checkpoints:** versioned archives with SHA-256 identity and manifests. The archives are not included in this repository; `releases/HASHES.md` records the expected identities.
- **Live runtime:** a local Python process that starts the orchestrator and demo data against a file-backed SQLite database.
- **SQLite database:** stores the runtime's workflow history. The local live database is generated at runtime and is excluded from version control.
- **Dashboard:** serves workflow state and history on loopback. It opens per-request SQLite connections in read-only mode and uses `query_only`; dashboard reads do not update the database.
- **Launcher:** the Windows batch file starts the Python launcher. The launcher extracts the sealed runtime into a temporary working directory, copies in the selected live wrapper, starts it, and opens the browser.

## Data flow

```text
NEXUS.bat → nexus_launcher.py → extract sealed checkpoint to TEMP
           → start nexus_live_runtime.py → orchestrator runs workflow tasks
                                          → append events to SQLite history
Browser ← HTTP response ← dashboard reads SQLite in read-only mode
```

The dashboard presents recorded workflow state. It does not execute tasks or make workflow decisions. Human decisions are recorded through the orchestrator decision API.

## Security model

- The dashboard binds to `127.0.0.1`; it is intended for the local computer, not LAN exposure.
- Dashboard database connections use SQLite read-only mode and `query_only`; request handlers close their connections after reading.
- Sealed checkpoint archives are treated as immutable release inputs and are not stored in this public repository.
- The runtime is designed for local operation without outbound network calls. The completed live-LLM check used a local Ollama service; it did not require a cloud API key.
- The launcher extracts to a disposable directory under the user TEMP path. The live database is runtime state, not source control content.

## Version history

| Artifact | Date | SHA-256 | Summary |
|---|---|---|---|
| 1.5.1 | 2026-11-12 | `f713fd04ec1e46b96e0adc56be0b3027dcd35a47f85fbfce22bcda299b894316` | Phase B, W1 registry, G-1 guard, and pristine-contract fix |
| 1.6.0 | 2026-11-13 | `b5db85b0961b7eb5a41f34046f6cc03e4333858ae874eb6351266eb8233a9ef1` | Phase C decision API, NoEffect type, and audit support |
| 1.7.0 | 2026-11-13 | `21d9378c2d95161fba6c9bbd68e56a6bc6c88b069e40403a8f199983fa276270` | Canonical local runtime and dashboard integration |
| 1.8.0 | 2026-11-13 | `0d7861a329e20ffb25f611351d4cbdb063f577ba772736c0d741d5375bb78021` | Phase D retry and deadline characterization support |
| Dashboard Option B | 2026-11-12 | `4096301983319bb73183b5d22bc8908a14b31aa129d5a8ac433a0336affc8638` | Standalone standard-library read-only dashboard |
