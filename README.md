# The Data City — conversation demonstration

Latest research: [the ten-company technology enrichment pack](docs/TECHNOLOGY-ENRICHMENT.md) records the second approved API response, public-source enrichment and dashboard-ready evidence. Luke has broadened the demonstration to a generic local-government authority with no Leeds/geography filter. All ten returned companies are retained. Local usage is now **2/2**. The new homepage uses this evidence with a separate illustrative presentation layer; see [the discovery homepage record](docs/DISCOVERY-HOMEPAGE.md).

Current implementation has four main pages: **Interview**, **Discover Your Market**, **A Role at The Data City**, **About Me**; the two former role URLs redirect to the combined page. The original brief is [docs/handoff.md](docs/handoff.md). The [revised AI Discovery brief](docs/ai-discovery-revised-brief.md) proposes a new homepage after local migration is verified. Start with [the local handoff](docs/CODEX-LOCAL-HANDOFF.md) and [phone workflow](docs/MOBILE-LOCAL-WORKFLOW.md). The homepage now implements the prepared contact-to-discovery-to-report journey; implementation and verification are recorded in [docs/DISCOVERY-HOMEPAGE.md](docs/DISCOVERY-HOMEPAGE.md). No cheat-sheet or bulk retrieval.

## Current version

The original Data renderer is retained in source, with the real HTTP 200 response from Luke's first local Instant Classification request. The input describes a hypothetical AI manufacturing business. The sample returned three RTICs, eight RSICs, two RNAICs, no SICs and ten similar companies. Company descriptions, financials and supplier suitability were not returned. Raw scores retain their own scales; unexpected matches remain visible.

The non-secret reviewed sample is now tracked at `data/reviewed-sample.json` in this repository so cloud builds can reproduce the page without another provider call. Its contents are the response Luke shared and the hypothetical input; it contains no password, token or account email. Its inclusion supersedes earlier notes saying all samples were kept outside Git. Luke authorised a public repository and public GitHub Pages demonstration on 18 October 2026, with a browser-only email entry screen. The screen is a convenience gate, not verified identity or private hosting.

The current visual identity follows The Data City’s US reference: deep navy, cyan/violet gradients, magenta actions, the official logo and locally served Poppins typography. It preserves the existing interactive layout. Ryan’s discovery corrections and the branding update are recorded in [the feedback implementation](docs/RYAN-FEEDBACK.md).

## GitHub and cloud workflow

The repository is `lukecraven36/the-data-city`. Luke has authorised making it public for GitHub Pages. GitHub Actions automatically checks the site and exports its four static pages and two legacy redirects on pushes to `main` and pull requests. Builds read the saved sample and never authenticate with or call The Data City. Review artifacts expire after seven days.

`python3 build_site.py` generates `dist/` for root hosting without the additional email screen. `python3 build_site.py --base-path /the-data-city/ --email-gate` builds the GitHub Pages version. No dependency installation is needed. The new Pages workflow runs offline checks and publishes the static demonstration on pushes to `main`.

The existing ChatGPT Site remains separate at https://data-city-conversation.lukecraven36.chatgpt.site, with its current audience preserved. The GitHub Pages version needs no ChatGPT account or password. See [the email-entry and hosting record](docs/GITHUB-PAGES.md) for configuration and limits.

The public email screen checks normalised SHA-256 email hashes locally and stores the accepted digest in browser session storage. It does not send emails, prove email ownership or protect the public source/HTML. The repository and underlying static files are publicly readable. Only public-demo material belongs in this build; `.private`, tokens, ledgers and local research remain excluded.

## Credentials and two-attempt budget

Windows migration was verified on 18 October 2026; see [the local verification record](docs/LOCAL-MIGRATION-VERIFIED.md). The registered source checkout uses ignored `.openai/local/private-directory.txt` to point to the existing `.private` directory outside OneDrive. An absolute `TDC_PRIVATE_DIR` environment setting takes precedence; absent both, the original source-relative location remains the default. This setting selects state only: it never copies credentials or initializes a ledger. Do not run `init` in either folder.

Luke completed signup and authenticated on his Windows PC. His authoritative local ledger now reports **2/2 attempts used**. The second approved request succeeded with ten companies; the homepage uses this cached result and public-source enrichment. Provider remaining balance is unknown.

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
node --check static/cv.js
node --check static/discovery.js
node --check static/role.js
node --check static/review-access.js
python3 build_site.py
```

Tests use mock transports and temporary ledgers. No live allowance is consumed. The discovery journey passed desktop and mobile-viewport browser checks locally; physical iPhone/Safari verification remains to be done.

Luke’s sign-in-only [Interview page](docs/INTERVIEW-PAGE.md) provides a dated company overview, recent developments and potential contribution. It uses local assets and makes no API requests.
