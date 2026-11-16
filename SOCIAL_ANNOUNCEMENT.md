# NEXUS launch announcement drafts

Repo: https://github.com/lojandemas36-crypto/NEXUS
Pages: https://lojandemas36-crypto.github.io/NEXUS/

## X / Twitter thread

Each post is under 280 characters, including both links.

1. NEXUS is on GitHub: a workflow orchestrator that makes uncertain outcomes visible and routes unresolved work for human review. Repo: https://github.com/lojandemas36-crypto/NEXUS Demo: https://lojandemas36-crypto.github.io/NEXUS/

2. NEXUS supports explicit human decisions for work that needs review, bounded NoEffect retries, and a local read-only dashboard. Details: https://github.com/lojandemas36-crypto/NEXUS Demo: https://lojandemas36-crypto.github.io/NEXUS/

3. The release is backed by five hash-anchored sealed artifacts. Live-LLM validation ran locally with Ollama qwen3.5:2b at zero API cost. Repo: https://github.com/lojandemas36-crypto/NEXUS Demo: https://lojandemas36-crypto.github.io/NEXUS/

4. The dashboard is for one user on one machine and binds to 127.0.0.1. The sealed archives are kept separate from the public repository. Setup: https://github.com/lojandemas36-crypto/NEXUS Demo: https://lojandemas36-crypto.github.io/NEXUS/

5. Want to inspect the code, release notes, or local setup? NEXUS is available here: https://github.com/lojandemas36-crypto/NEXUS Try the landing page: https://lojandemas36-crypto.github.io/NEXUS/

## LinkedIn

I’m sharing NEXUS, a Python workflow orchestrator built around a practical problem: sometimes a task ends without a reliable answer, and software needs to make that uncertainty visible.

NEXUS can run multi-step workflows, preserve unresolved outcomes for human review, record explicit decisions, and support bounded retries for operations that report no side effect. Its local dashboard is read-only and runs on localhost. The project’s versioned releases are recorded with SHA-256 manifests, and the sealed archives are kept outside the public repository.

The v1.1 release brings together the 1.5.1–1.8.0 work and a standalone dashboard package. A local live-LLM validation used Ollama with qwen3.5:2b at zero API cost.

NEXUS is currently single-user and localhost-only. LAN access and broader integrations are outside this release.

Repository: https://github.com/lojandemas36-crypto/NEXUS
Project page: https://lojandemas36-crypto.github.io/NEXUS/

## Reddit: r/selfhosted

I built NEXUS, a small Python workflow orchestrator for local use. It keeps uncertain task outcomes visible for human review, records explicit decisions, and includes a read-only localhost dashboard backed by SQLite. It is single-user and does not expose the dashboard to a LAN. The release has hash-anchored sealed artifacts; the archives are not hosted in the repo. Feedback on the workflow safety model and local setup is welcome.

Repo: https://github.com/lojandemas36-crypto/NEXUS
Project page: https://lojandemas36-crypto.github.io/NEXUS/

## Reddit: r/Python

NEXUS is a standard-library-focused Python workflow orchestrator with an uncertain-resume flow, a decision API, bounded NoEffect retry support, and a read-only local dashboard. The repository includes release documentation and hashes for separately held sealed artifacts. I’d appreciate technical feedback, especially on the workflow contracts and test approach. The runtime is currently single-user and localhost-only.

Repo: https://github.com/lojandemas36-crypto/NEXUS
Project page: https://lojandemas36-crypto.github.io/NEXUS/
