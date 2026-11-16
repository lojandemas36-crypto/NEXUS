# GitHub publication checklist

Run these steps from the local publication setup. The scripts automate the matching GitHub UI or copy/push work.

1. [ ] Generate the social preview: run `make_social_preview.ps1`. Replaces manual image design; success signal is `social-preview.png` in the local clone with a printed SHA-256. If the SVG fallback appears, export it to PNG before continuing.
2. [ ] Publish the second commit: run `finalize_repo.ps1`. Replaces copying the four community documents and available Desktop screenshots, then committing and pushing. Success signal is a commit hash, tracked-file count, and successful push message. Missing screenshots are warned and skipped.
3. [ ] Set the repository About box: run `set_about.ps1`. Replaces entering description, website, topics, Issues, and Discussions in Settings. Success signal is `About updated`; without GitHub CLI, the script prints copy-ready values.
4. [ ] Enable GitHub Pages: run `enable_pages.ps1`. Replaces Settings → Pages setup and URL polling. Success signal is `Pages is live: https://lojandemas36-crypto.github.io/NEXUS/`; without GitHub CLI, the script prints the manual steps.
5. [ ] Confirm the public pages: open `https://github.com/lojandemas36-crypto/NEXUS` and `https://lojandemas36-crypto.github.io/NEXUS/` in a browser. Confirm the repository files and landing page render as expected.

The scripts do not include sealed archives or database files in the repository.
