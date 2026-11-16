# NEXUS changelog and sealed artifact ledger

Hashes identify recorded archives; seal/report and manifest hashes identify supporting records. Historical candidate artifacts are labeled as such. The supplied 1.7.0 hash was checked against the archive and seal report; the verified archive hash below is authoritative.

| Version / artifact | Archive SHA-256 and file count | Change summary | Seal report / record path and SHA-256 | Manifest path and SHA-256 |
|---|---|---|---|---|
| Phase B verified baseline (historical) | `20f032de6739eb5bf374b4e54309f710c5f923943613d15c508d7545609b0dad`; 39 files per recorded tree manifest | Verified Phase B baseline before G-1/W1 work. A separate locally built recovery archive has SHA `d4eb36f90a60d14636fd1a58ef9130f1eb4ba2e0f951dd6161848286b3fa8b03`; it is not substituted for the uploaded-original hash. | `NEXUS_CHECKPOINTS/phaseB_verified/NEXUS_1_5_0_phaseB_checkpoint_MANIFEST.txt` (baseline record; SHA-256 `c0f7fbd388ab3472f98d67afc551f2b42b4638e47d39ec1621f227e01e97c5db`) | `NEXUS_CHECKPOINTS/phaseB_verified/MANIFEST.sha256` (SHA-256 `155aebc8fb06e2481901e4e7f040c5787ca4c382302b1f17d7d87476e0c0cc0f`); archive sidecar `NEXUS_1_5_0_phaseB_checkpoint_zip_sha256.txt` SHA-256 `3b1d25d26420aca01b493196e0f3238f13d07469ac64c7be5139739196809f4e` records the separate local archive hash above. |
| G-1 live seal (historical delta; not a frozen checkpoint) | `ec84f2c8addc039512738869d6722b9a78f04ba85e8b04346888edf52706f1d1`; 9 archive entries | G-1 live guard delta and handoff evidence; later integrated by 1.5.1. | `NEXUS_CHECKPOINTS/phaseB_g1_live_verified/SEALED.txt` (SHA-256 `3e8d9650c7cb1ded22b02997381e6ada6b7ada24fd0aa555d91979f0169a0778`); record explicitly labels official acceptance as pending at that historical point. | `NEXUS_CHECKPOINTS/phaseB_g1_live_verified/MANIFEST.sha256` (SHA-256 `e46f7352064b63dade2f3fdc302dd674a497b0a4e9348e888c5a3512c40084c3`). |
| R2 W1/G-1 candidate (superseded, not sealed) | `04d3ccd02d74c6491523e276ec9f1df51b288d9482832bc55da62532f7f64096`; candidate count not established here | Review candidate superseded by sealed 1.5.1. | Seal report: N/A (unsealed candidate). Candidate status and review notes, not a seal record, govern this row. | Seal manifest: N/A (unsealed candidate). |
| NEXUS 1.5.1 | `f713fd04ec1e46b96e0adc56be0b3027dcd35a47f85fbfce22bcda299b894316`; 40 files | Phase B + ratified Windows portability + W1 (01-07) + G-1 guard + 08 needs-review boundary conversion + pristine D5 safety/follow-up tests. | `NEXUS_CHECKPOINTS/NEXUS_1_5_1_phaseB_W1_G1_20261112_SEAL_REPORT.md` (SHA-256 `c2c5203bc24be0ed88e77b6c74229066a98e5ac19fd816ebf2ce3b50cfc76e9d`). | `NEXUS_CHECKPOINTS/NEXUS_1_5_1_phaseB_W1_G1_20261112_MANIFEST.txt` (SHA-256 `3ab7bc3d1737aa66635191d23a25b3cebac4ca3b24f976f8132503906daa3ad8`). |
| Dashboard Option B | `4096301983319bb73183b5d22bc8908a14b31aa129d5a8ac433a0336affc8638`; 6 files | Standalone standard-library localhost HTTP dashboard; read-only SQLite access. Not runtime-integrated in this seal. | `NEXUS_CHECKPOINTS/NEXUS_dashboard_optionB_20261112_SEAL_REPORT.md` (SHA-256 `76b5a83638f752932c1f66f3e27613d4298e2e54353f381370b8a610842e2335`). | `NEXUS_CHECKPOINTS/dashboard_optionB_HANDOFF/MANIFEST.sha256` (SHA-256 `2f4f3c4add44694df85779ad80d3be3ce29455da9e5cce7c6301954165dd7ee5`). |
| NEXUS 1.6.0 | `b5db85b0961b7eb5a41f34046f6cc03e4333858ae874eb6351266eb823a9e9f1`; 41 files | Adds `NoEffect`, `decide(task_id, outcome)`, decision audit, and four Phase C contract tests; seal report records 197 passed under both runners. | `NEXUS_CHECKPOINTS/NEXUS_1_6_0_phaseC_20261113_SEAL_REPORT.md` (SHA-256 `c0ae01c5b6de80382f5e862f5064917a367552f96249f98ba19e3fd0616b0cff`). | `NEXUS_CHECKPOINTS/NEXUS_1_6_0_phaseC_20261113_MANIFEST.txt` (SHA-256 `7bc5b31d74c2cd98ad417ab6712e9dbf1303c7d012e432bcdbfc75c7accd1f6d`). |
| NEXUS 1.7.0 | `21d9378c2d95161fba6c9bbd68e5646bc6c88b069e40403a8f199983fa276270`; 49 files | canonical runtime: 1.6.0 + dashboard merged, 7 integration tests. Seal report records pytest 197 passed and run_tests 197 passed; runtime binds loopback and dashboard reads SQLite read-only. | `NEXUS_CHECKPOINTS/NEXUS_1_7_0_runtime_20261113_SEAL_REPORT.md` (SHA-256 `dd18984dbecca931c48b7e2cfa5c43a56f864559f75d08ba8799788e0439f8b1`). | `NEXUS_CHECKPOINTS/NEXUS_1_7_0_runtime_20261113_MANIFEST.txt` (SHA-256 `f867782ea6e5689215984ac12ee33e33eb0a360435c5d7efd7ab45640264cc9d`). |

## Files added by manifests

- 1.5.1: `tests/test_w1_registry.py` — SHA-256 `3af7d6a90967385c85900ad386ca2cd5b5b801589ee92ae52fff4287f5551775`.
- 1.6.0: `tests/test_phaseC_contract.py` — SHA-256 `493506b0025754b0fb39ccb42c78c1716acf643c02ec74d67dc2c78d6a181a3c`.
- 1.7.0 additions relative to 1.6.0, with hashes from the 1.7.0 manifest:
  - `nexus/runtime.py` — `9e67fde9b9442f43a384b69491c18ee4947feef466c5dee963d7d3f8a4a0b5e4`
  - `nexus_dashboard/README.md` — `3913d149513548f474c9345d1ea3dd5e31e690d672dfd3876d68074de1b68c27`
  - `nexus_dashboard/__init__.py` — `3eef9f8a450cb0ed5d8db48f4a41195e398e0abba8cd015d4353e6c3fce412ba`
  - `nexus_dashboard/__main__.py` — `540fd0a5992ca535482a9d44b2e268ce3a39bb47a0576f301214afa5ef4494b9`
  - `nexus_dashboard/server.py` — `1abf82937c28d58368ea05338a4370e2e422acbe6b7f3773119181acf748d3ec`
  - `nexus_dashboard/tests/test_dashboard.py` — `979e61ce24a0d6179677f1b32c844f94f74f261a62f930488e84e01a493b6df6`
  - `nexus_dashboard/tests/test_integration.py` — `4e2ac825651d73ae8e914e7ec5a76e75919c88cb9d141453b0560dafc8502b13`
  - `nexus_dashboard/verify_live.py` — `d94149cef5f6637c26b7f9f18414c8acd7a8eed7db0fd3c6d547efe476b9d691`
- Dashboard Option B standalone manifest is listed at `NEXUS_CHECKPOINTS/dashboard_optionB_HANDOFF/MANIFEST.sha256`; its manifest hash is recorded above.

Live-LLM v1.0 validation completed locally via Ollama (qwen3.5:2b) at zero cost; REPORT.md SHA-256 651dc76ef38e0a7f79426d8081f3d8eab320b0043dd984818db04f2a7968b004. The report hash was computed directly because RESULT.manifest omits REPORT.md; the seal-hash label discrepancy is disclosed in SIGN_OFF_INSTRUMENT.md.

## NEXUS 1.8.0 — sealed

| Version / artifact | Archive SHA-256 and file count | Change summary | Seal report / record path and SHA-256 | Manifest path and SHA-256 |
|---|---|---|---|---|
| NEXUS 1.8.0 | `0d7861a329e20ffb25f611351d4cbdb063f577ba772736c0d741d5375bb78021`; 50 files | NoEffect retry integration, G-5 deadline characterization helpers, `decide()` retry cancellation, and four Phase D contract tests. | `NEXUS_CHECKPOINTS/NEXUS_1_8_0_phaseD_20261113_SEAL_REPORT.md` (SHA-256 `a714ea210cb99044a5d262bbccbf9111a6e6c897d63ec9f803a635e1c1a46757`) | `NEXUS_CHECKPOINTS/NEXUS_1_8_0_phaseD_20261113_MANIFEST.txt` (SHA-256 `089ab73bd6cc2d5597d4ccb02daa48f38dce17cda63ebbb4fa77efc8420ee6c6`) |

Manifest hashes for Phase D changed files:
- `nexus/engine.py` — `f8cd71a314057803769efc4b16096a34436718d42136d744a1c581d97677f597`
- `nexus/orchestrator.py` — `bb5d46cb9dfcfc26ae0a3a5bbe9a2841c4abcc15f04e332a48d35e64d03637c5`
- `tests/test_phaseD_contract.py` — `4045ac8fdb5190fa96bda0b153d99fecbda826daa8ba749eeb32fea1d463c3ab`
