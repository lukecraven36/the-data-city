# Local Codex handoff — 18 October 2026

## Instruction precedence and scope

Luke supplied [the revised brief](ai-discovery-revised-brief.md) for review and a move to local Codex. It proposes Home / AI Discovery as the primary experience, retaining AI Lead, Commercial Product Lead and About Me. Preserve existing functionality while preparing migration. Do not rebuild the homepage until local execution and the API workflow are verified. The original [handoff](handoff.md) remains historical context; the revised direction changes the opening page, not the credential and data constraints.

One conflict is resolved conservatively: the revised brief suggests transient retries, but Luke explicitly required **no automatic retries**. Keep no retries, the persistent two-attempt cap across runs and failures, cached responses, and fail-closed missing state. No extra calls are authorised merely by reading this document.

## Preserved source and hosting

- Repository: https://github.com/lukecraven36/the-data-city (private).
- Remote default and sole advertised branch on inspection: main, at `4e7ffed3ed24fbb0e2b0a4c016ab46b78d2d6409`. Cloud working branch: work; initially clean. No pull-request head refs were advertised; PR state beyond that has not been independently checked.
- Latest implementation: `2d3ec9c`, expandable CV timeline, three summary bullets per role and full detail. Preserve date verification notes.
- Existing owner-only preview: https://data-city-conversation.lukecraven36.chatgpt.site — publication receipt in `.openai/publication.json`, version 2. No new publication is part of this review.
- GitHub Actions checks/exports static pages; a Git push alone does not publish the Site. Do not enable public Pages.

## Two Windows folders must be reconciled locally

1. API worked in `C:\Users\Luke\DataCity\the-data-city-main` (Luke's terminal evidence; downloaded source).
2. Codex currently registers a Git project at `C:\Users\Luke\OneDrive - Pathed Consulting\Documents\ChatGPT\The Data City` (project inventory checked 18 October).

These are not proven equivalent. First inspect both locally, including remotes, branch, uncommitted files and presence of private state, without printing tokens. Do not pull over uncommitted work or overwrite a ledger. Prefer the non-synchronised API folder for credentials; avoid casually moving secret state into OneDrive. If source needs updating, back up private state locally and reconcile source without replacing it. Do not upload `.private` or ask Luke to paste credentials. The current cloud process cannot inspect either Windows path.

## Authoritative API state

Luke's local output confirmed **1/2 attempts used**, attempt 1 HTTP 200, response saved. Provider balance is unknown. No second classification is confirmed; check the actual Windows ledger before dispatch. The Windows `.private/usage.sqlite3` is authoritative. Preserve it, its initialization marker and `.private/token.json` locally.

Never run `init` again, restore the archived cloud zero ledger, or reuse the old zero-ledger handoff ZIP. Missing or inconsistent state blocks dispatch. Keep cloud dispatch disabled. A cached website build does not need credentials.

Reuse `api.py` rather than adding a second client:

- Base: `https://instant-classification-api.thedatacity.com`.
- Login: POST `/api/v1/login/access-token`; hidden interactive password, not retained. If renewed authentication is required, Luke enters the password locally; do not seek it in chat.
- Authentication check: POST `/api/v1/login/test-token`; distinct from a data request.
- Classification: POST `/api/v1/instantClassification`, JSON exactly one of Text or Website; persistent reservation before dispatch, 150-second timeout, no redirects/retries.
- Existing command: `py api.py classify --payload <local-json-path> --confirm-public-input`. Codex executes it locally only after verifying ledger and the chosen input. It is not a general market-search command.
- Read-only initial check: `py api.py status`. Do this before network access. Check token presence without printing contents. Token expiry or revocation may require fresh login; historic success does not establish current access.

Configuration names only: `TDC_ACCOUNT_EMAIL` (documentary placeholder) and optional `TDC_ACCESS_TOKEN` (server-side token). `.env.example` already contains placeholders. The program does not automatically load `.env`; local token storage already works. Never add a frontend token variable. Python standard library runs the app/connector; Node checks JavaScript syntax. No third-party runtime dependencies or AI API runtime are currently configured.

## Exact council scenario

**Leeds City Council**, considering its sector landscape and evidence relevant to investment priorities. Tourism and the AI consultancy/agency approach were rejected. The council is a demonstration persona, not a commissioned customer.

Luke's actual research question:

> Help Leeds City Council understand its business landscape: which sectors have a significant local presence, which show evidence of growth, and where investment or funding activity is taking place. Relate the findings to the government's IS-8 priorities, with sources and gaps clearly identified.

This question is a research brief, **not a valid market-search instruction to Instant Classification**. That endpoint classifies an individual description/website and may return similar companies; it does not return a Leeds sector census, investment transactions or a growth ranking.

Ryan's advice, supplied privately by Luke: focus on a council's understanding of sectors/businesses and investment comparison; show Luke's contribution to entering new markets. Do not publish private remarks as official company statements. The supplied Data City video discusses RTIC/R-SIC and industrial strategy measurement; its transcript is not proof of our entitlement or of particular statistics.

## What was actually retrieved

`data/reviewed-sample.json` contains the reviewed, non-secret first response shared by Luke. Input:

> We develop AI software that helps manufacturers inspect products for defects using computer vision. Our platform analyses production-line images, flags potential quality issues for human review, and integrates with existing factory systems.

HTTP 200 returned 3 RTICs, 8 R-SICs, 2 R-NAICs, no SICs and 10 similar companies. AI Ecosystem Products scored 0.614; an unexpected Advanced Materials Textiles match scored 0.417. Keep surprises visible. Scores are not calibrated probabilities. Company names/numbers/websites are supplied, but employment, revenue, investment, growth and Leeds operating locations are not.

Latest discussed possible second classification input, **not executed or a substitute for council research**:

> Technology businesses developing proprietary software platforms and digital products for business customers. Their products include cloud software, cybersecurity tools, data analytics platforms and business process automation.

Do not spend the remaining attempt merely to prove local execution. Status, offline tests and a deliberate token check can establish the workflow first.

## Public research starting points, not completed analysis

- https://thedatacity.com/local-government/
- https://thedatacity.com/blog/how-local-government-uses-the-data-city-platform/
- https://thedatacity.com/case-studies/cumberland-council/
- https://thedatacity.com/case-studies/glasgow-city-region/
- https://news.leeds.gov.uk/news/multibillion-economic-vision-for-leeds-to-drive-creation-of-100-000-jobs
- https://www.nomisweb.co.uk/datasets/newbres6pub — workplace employment.
- https://www.nomisweb.co.uk/datasets/idbrlu — local units, not automatically unique enterprises.
- https://www.ukri.org/publications/gateway-to-research-guide/a-guide-to-gateway-to-research/ — awards/commitments are not proof of expenditure or local economic impact.
- https://docs.thedatacity.com/instant-classification/guides/quickstart
- https://docs.thedatacity.com/data-dictionary — wider platform fields do not establish our access.

Recheck dates, definitions, geography, licensing and availability before using these. The Leeds vision's job/value figures are ambitions, not achieved growth. No Leeds dataset, sector ranking, IS-8 crosswalk or investment analysis has yet been produced. Registered office is not proof of an operating site. Do not equate classifications with an official IS-8 mapping or add overlapping sector counts.

## Local acceptance sequence — execute on Windows, not cloud

1. Reconcile folders and preserve private state; verify current GitHub source without destructive operations.
2. Run read-only `py api.py status` and report a redacted count. Never print token files or secret environment values.
3. Run `py -m unittest discover -s tests -v`, `node --check static/data.js`, `node --check static/cv.js`, and `py build_site.py`. Tests use temporary ledgers and mock transports, not real API requests.
4. Start `py site.py` on loopback and verify navigation/rendering locally. Choose a separate review password interactively. Keep provider password separate.
5. If authorised access can be checked, use test-token once; if it fails, report the exact redacted failure and stop, without retrying classifications.
6. Prove phone control using [the mobile workflow](MOBILE-LOCAL-WORKFLOW.md). Record host, commit, tests and observed results.
7. Only then implement the revised homepage. Keep contact inputs dummy/session-only; exact three questions from the revised brief; label the independent proposal and any cached demonstration. Preserve the three support pages and expandable CV.

## Truthful autonomy evidence

Keep a short development record: task/approved scope, input, host and commit, commands or tools executed, source URLs and retrieval dates, cached versus new data, checks, files changed, remaining gaps and decisions Luke made. Redact credentials. Do not invent time savings, autonomous runs, agent progress or business results.

Distinguish real Codex development/research automation from the visitor product. Arbitrary visitor-specific AI answers require a separately configured, authorised backend and AI runtime. The current hosted site is static; a subscription is not a public inference endpoint. Until configured, use a clearly labelled reproducible council demonstration, with honest missing-data states.

## Status at preparation

Verified: cloud source/remote, latest saved implementation, registered local project path, existing CLI capabilities, historic local successful response, official Remote documentation. Not verified: current Windows checkout, current ledger/token, current API connectivity, app rendering on Windows, phone pairing/control. No new data request or publication occurred during this review.
