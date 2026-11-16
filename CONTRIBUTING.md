# Contributing to NEXUS

Thanks for taking the time to improve NEXUS. Open a GitHub issue to describe a bug or propose a change. For code work, explain the behavior you expect and identify affected workflows or contracts before opening a pull request.

## Project covenant

Sealed archives are immutable. Make new work on a disposable copy, never by editing a sealed archive. Preserve all frozen tests. A change that weakens, skips, or removes a frozen test is not acceptable. Both project runners, `run_tests.py` and pytest, must pass on the proposed tree before it is ready for review. Include the exact commands and results in the pull request.

## Pull request checklist

- [ ] The change addresses an issue or states its purpose and expected behavior.
- [ ] Work was performed on a disposable copy; sealed archives remain untouched.
- [ ] Existing frozen tests are unchanged in strength and coverage.
- [ ] New behavior has focused tests, where applicable.
- [ ] `python run_tests.py` passes.
- [ ] `python -m pytest -q` passes.
- [ ] The pull request records commands, observed results, and any remaining limitations.
- [ ] No secrets, live database files, or sealed ZIP archives are included.
