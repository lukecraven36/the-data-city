# The Data City — private conversation site

Current implementation has exactly four pages: **Data**, **AI Lead**, **Commercial Product Lead**, **About Me**. The original brief is [docs/handoff.md](docs/handoff.md). The [revised AI Discovery brief](docs/ai-discovery-revised-brief.md) proposes a new homepage after local migration is verified. Start with [the local handoff](docs/CODEX-LOCAL-HANDOFF.md) and [phone workflow](docs/MOBILE-LOCAL-WORKFLOW.md). No homepage rebuild has been made as part of the handoff review. No cheat-sheet or bulk retrieval.

## Current version

Data presents the real HTTP 200 response from Luke's first local Instant Classification request. The input describes a hypothetical AI manufacturing business. The sample returned three RTICs, eight RSICs, two RNAICs, no SICs and ten similar companies. Company descriptions, financials and supplier suitability were not returned. Raw scores retain their own scales; unexpected matches remain visible.

The non-secret reviewed sample is now tracked at `data/reviewed-sample.json` in this **private** repository so cloud builds can reproduce the page without another provider call. Its contents are the response Luke shared and the hypothetical input; it contains no password, token or account email. Its inclusion supersedes earlier notes saying all samples were kept outside Git. Keep both the repository and any hosted build private.

The design derives from the actual Family Hub source: dark `#15242a` sidebar, lime `#d7fa69`, blue `#2548cb`, pale background, rounded cards and bold sans-serif headings with serif emphasis. No household records, integrations or credentials were copied.

## GitHub and cloud workflow

The private repository is `lukecraven36/the-data-city`. GitHub Actions automatically checks the site and exports its four static pages on pushes to `main` and pull requests. Builds read the saved sample and never authenticate with or call The Data City. Review artifacts expire after seven days.

`python3 build_site.py` generates `dist/`. No dependency installation is needed. The hosting manifest identifies the owner-only Site at https://data-city-conversation.lukecraven36.chatgpt.site, separate from the earlier Data City dashboard. Version 2 is published (see `.openai/publication.json`). GitHub is the source of truth; publishing requires syncing that commit to the Site source repository and saving/deploying the matching build. GitHub CI alone does **not** publish a live site. Luke has authorised private publication and ongoing updates requested in this chat. Codex can perform the GitHub sync and private publication without another approval for routine edits; no laptop server is needed. Arbitrary GitHub pushes are not yet wired to automatic live deployment.

Never enable public GitHub Pages or publish the exported files publicly. A private GitHub repository does not make public hosting private.

## Credentials and two-attempt budget

Luke completed signup and authenticated on his Windows PC. His authoritative local ledger reports **1/2 attempts used**. No second data request was made. Provider remaining balance is unknown.

Keep `.private/` on that PC securely: it contains the authoritative ledger, original response and token. It is ignored by Git. Preserve it across sessions; do not run `init`, delete it, recreate the zero-attempt transfer, or create another allowance. Cloud dispatch is disabled after the handoff. Missing/corrupt state fails closed, reservations commit before dispatch, concurrent requests share the cap, failures count, repeated inputs use cache, and the client does not retry or follow redirects. No data call occurs on page load. Login/token checks are separate from classifications. No provider credentials or request endpoints are needed in the hosted static build.

See [ledger reconciliation](docs/ledger-reconciliation.md) for the recovery and handoff history. Richer company records require a separately issued key and confirmed display rights; any future retrieval shares the same budget.

## Local review (optional)

```bash
python3 site.py
```

Choose a separate review password of at least 12 characters. Open `http://127.0.0.1:8000`; username `luke`. The loopback-only server authenticates every page and asset and sends no-store/CSP headers. Do not expose it through a public tunnel.

## Validation

```bash
python3 -m unittest discover -s tests -v
node --check static/data.js
python3 build_site.py
```

Tests use mock transports and temporary ledgers. No live allowance is consumed. Browser visual verification remains pending because this cloud environment has no browser-control tool.
