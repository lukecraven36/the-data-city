# The Data City — private conversation draft

Four pages: **Data**, **AI Lead**, **Commercial Product Lead**, **About Me**.
`docs/handoff.md` is the governing project brief. No dashboard, cheat-sheet, chatbot or bulk retrieval.

## Current state

Local implementation only; not deployed. Classification not connected: no verified account, server credential or Luke-selected public input. The first real response must be inspected before agreeing Data's presentation. No fabricated samples are shown. Company-data entitlement is separate and unconfirmed.

Python 3.11+; standard library only. No package installation or frontend build.

```bash
python3 site.py
```

Choose a review password of at least 12 characters at the hidden prompt. Open `http://127.0.0.1:8000`; username `luke`. The server binds only to loopback, authenticates every page/asset and sends no-store headers. It is intended for local review: **do not expose this HTTP server through a public tunnel or port forward**. Private GitHub visibility does not confer private hosting. A later deployment needs explicit instruction and real TLS/access controls.

## Secure provider setup

1. Confirm whether you already have an Instant Classification account. Otherwise use the [official signup](https://instant-classification-api.thedatacity.com/signup) with the planned email in `docs/handoff.md`. Complete password entry, any verification and acceptance of provider terms yourself. No account has been created by this project.
2. In a private terminal on the server, run `python3 api.py login`. Enter the email and password at the prompts. Password input is hidden and discarded; the returned token is retained in `.private/token.json` with owner-only permissions. Do not enter passwords/tokens in chat, command arguments, screenshots or Git. A secure runtime secret binding named `TDC_ACCESS_TOKEN` is also supported. `.env.example` has placeholders only; no dotenv loader is used.
3. Run `python3 api.py test-token` deliberately. This checks authentication without using a classification attempt. Profile data is not printed. Tokens are documented as valid for eight days, with no refresh-token flow. Expiry requires deliberate login; no request replay.
4. Choose one public company website or public description. Put exactly one key (`Website` or `Text`) in `.private/input.json`. Use no confidential customer material. The input must be selected by Luke; no default company is chosen.
5. Run `python3 api.py classify --payload .private/input.json --confirm-public-input` once. Inspect the saved original privately with `python3 api.py inspect 1` **in a private terminal without session recording**. Inspection prints provider data intentionally; do not paste sensitive responses into logs or screenshots. Agree the useful Data page shape after reviewing fields. The second distinct input needs an explicit decision that it adds value.

## Persistent two-attempt budget

The initial ledger was bootstrapped once in this workspace using `python3 api.py init`. `python3 api.py status` reports the current local attempts separately from the unknown provider balance.

`.private/usage.sqlite3` is the authoritative, shared ledger and response cache. An immediate SQLite transaction reserves and commits an attempt **before** network dispatch; an insert trigger independently enforces a cap of two. Failed HTTP responses, timeouts, connection errors and interrupted processes retain their reservation. Repeating an identical input returns its existing attempt, including failures, without dispatch. No retries, redirects, page-load data calls, background jobs, pagination or refreshes exist. Token checks/login are separate from the data budget. The classifier timeout is 150 seconds. Provider-internal retries described in their docs are outside this client's control.

Back up and preserve the entire `.private/` directory securely on persistent storage across restarts, sessions, checkouts and environment changes. It is intentionally ignored by Git. **A new checkout does not carry the usage ledger: restore the existing ledger, never initialize a replacement.** The app refuses to operate when the ledger is missing/corrupt and refuses reinitialization if its marker remains. It cannot infer prior usage if all private state is manually deleted; do not delete it or run parallel copies with separate ledgers. The cap is not account-wide against unrelated external clients.

For a genuinely first setup in a new environment only, initialization must follow confirmation that no earlier data requests have occurred. There is no reset command. If state disappears unexpectedly, stop and reconcile it; no calls should be made.

The provider docs currently describe 20 successful lifetime free classifications, five requests/minute, and no quota reset. Existing account consumption is unknown. Our stricter two dispatched attempts include failures. Do not buy access or raise the limit automatically.

Industry Engine company records require a separately issued API key and confirmed licensing/display rights. This version deliberately implements only Instant Classification. Any later company-data retrieval must use this **same ledger and cap**, never a separate allowance or a classification token.

## Verification

```bash
python3 -m unittest discover -s tests -v
```

Tests use mock transports and temporary databases: concurrency, cap persistence, failed attempts, missing state, original response storage, duplicate cached viewing, authenticated HTTP access and four read-only pages. They consume no provider allowance. Browser visual QA and live authentication have not been completed.

See `docs/access-and-sources.md` for verified sources and remaining editorial checks. To resume: retain private state, configure credentials securely, confirm Luke's public input, make one explicit call, inspect it and agree Data's layout before implementing it.
