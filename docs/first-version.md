# First version — 13 October 2026

The Data page now presents the real HTTP 200 response from Luke's first local classification attempt. The input describes a hypothetical AI computer-vision business for manufacturing; it is not an identified company. The first response supplied three RTIC classifications, eight RSIC classifications, two RNAIC classifications, no SIC classifications, and ten similar companies. No individual company descriptions, financials or suitability assessments were returned.

The page reads an explicitly reviewed snapshot stored outside Git at `.private/reviewed-sample.json`. This snapshot was transcribed from Luke's shared response; the local installer checks that its response object equals attempt 1's JSON in Luke's authoritative ledger before installing. The original response remains in that ledger. No request occurs when opening pages, expanding classifications or comparing two company cards. Scores are shown on their original scales without probability claims. Unexpected textile and biology matches remain visible, with a prompt to investigate. Website links use the returned domains with HTTPS added; these destinations have not been independently verified.

The AI Lead, Commercial Product Lead and About Me pages retain the existing scope and source links. No fifth page, chatbot, additional data request or publication was introduced. About Me still flags titles and career dates for verification.

## Windows update

Download the private first-version ZIP and extract it into `C:\Users\Luke\DataCity\the-data-city-main`. This creates the `tdc-first-version` subfolder. Stop any existing review server with Ctrl+C before updating. From PowerShell in the project folder run:

```powershell
py .\tdc-first-version\install.py
py site.py
```

The installer checks the existing ledger and cached attempt 1 before replacing presentation files. It does not include, replace or initialize a usage ledger or token. It does not modify the API client. It refuses an unrecognized saved response. Preserve the entire `.private` folder and do not rerun the old zero-attempt transfer package.

Choose a new local review password of at least 12 characters, separate from the provider password. Visit `http://127.0.0.1:8000` in the browser on this PC. Username: `luke`; password: the review password just chosen. The server listens on loopback only, authenticates pages and assets, blocks browser network requests with CSP, and avoids access logging. Do not expose it through a public tunnel. This is local review, not hosted publication.

## Validation

Thirteen Python tests passed for the persistent cap, concurrency, caching, failed attempts, transferred-cloud blocking, private routes, script authentication, missing-state behavior and escaped reviewed-response rendering. JavaScript syntax was checked. Update installation was verified against an isolated one-attempt database, including token/ledger preservation and mismatched-response rejection. No live API request was used. Browser visual and interactive verification remain pending on Luke's PC because no browser-control tool is available in this environment.
