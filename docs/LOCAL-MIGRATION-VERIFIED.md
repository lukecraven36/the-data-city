# Windows migration verification — 18 October 2026

Scope: reconcile local source and private API state, run offline checks and a non-classification authentication check. No homepage implementation, classification, push or publication.

## Host and source

- Commands executed on Windows host `MSI`, OS `Microsoft Windows NT 10.0.26300.0`.
- Actual working directory: `C:\Users\Luke\OneDrive - Pathed Consulting\Documents\ChatGPT\The Data City`.
- Initially this contained only an empty Git repository on unborn `master`, no remote, no commit and no local working files. It was inspected before fetching.
- Added origin `https://github.com/lukecraven36/the-data-city.git`, fetched, and checked out tracking branch `main` at `8a6fc4a996a2680c2e1096b388f708bbab8d8160`. This exactly matches the expected cloud handoff. No existing source files were overwritten.
- Read CODEX-LOCAL-HANDOFF.md, MOBILE-LOCAL-WORKFLOW.md and the complete revised AI Discovery brief. Preserve the Leeds City Council investment/sector research question recorded in the handoff; no new council research was performed.

## Existing local work and private state

`C:\Users\Luke\DataCity\the-data-city-main` is a downloaded source folder, not a Git repository. It contains the authoritative `.private` directory plus older source and transfer folders. All 28 original files outside Python bytecode caches were hashed before work and verified unchanged afterwards. No old installer was run; the archived transfer ledger was not used.

The registered source now resolves the original external private directory through ignored `.openai/local/private-directory.txt`. Only an absolute directory path is stored there, no secret. `api.py` also supports `TDC_PRIVATE_DIR` as an explicit environment override. No `.private` directory was created in the OneDrive checkout. Future Codex calls can run `py api.py status` from this checkout directly; no manual transfer of responses is required. Any future classification still requires authorization for its input and uses the original ledger.

A permission-restricted backup of all five original private files was made and verified at `C:\Users\Luke\DataCity\migration-private-backup-20261018\.private`; the original stays authoritative. The backup is for recovery only, not a second runtime ledger. File hashes are retained outside OneDrive in `C:\Users\Luke\DataCity\migration-original-hashes.json`.

Read-only SQLite inspection: integrity `ok`, budget cap `2`, exactly one attempt, attempt 1 `response saved`, HTTP `200`, enforcement trigger present. Initialization marker and stored token present. Stored token expiry was in the future. After all checks, the ledger, token and other original files were byte-for-byte unchanged. Local usage remains **1/2**; provider remaining balance is unknown. No initialization/reset occurred.

## Executed verification

- Python `3.15.0`, Node `v24.19.0`.
- `py api.py status`: **1/2**, attempt 1 saved HTTP 200.
- `py -m unittest discover -s tests -v`: **16 passed**, mock transports and temporary test ledgers only. These are isolated test fixtures, not another operational allowance.
- First run exposed an existing SQLite connection leak on corrupt-ledger rejection, causing Windows file-lock cleanup failure. Fixed connection closure on both database and validation errors; rerun passed. Added coverage for external-state selection, environment precedence and invalid local settings.
- `node --check static/data.js` and `node --check static/cv.js`: passed.
- `py build_site.py`: four pages exported to ignored `dist/`, from the reviewed cache.
- Temporary authenticated loopback HTTP smoke server: all four pages and all three assets returned 200; anonymous access 401; private token path 404. Provider transport patched to reject calls during this smoke check. Server stopped afterwards.
- Exactly one `py api.py test-token`: POST `/api/v1/login/test-token` returned **HTTP 200** from the existing local credential configuration. No classification call or retry. This verifies authentication now, not access to the separately licensed company-data API.

Local migration and connector authentication are verified. Current migration changes are local working-tree changes on top of the handoff commit; nothing has been pushed or published.

## Next scope

Luke confirms phone control is already connected and working; pairing was not repeated. Local commands and results in this task establish laptop execution. Phone steering/approval and mobile website appearance were not independently exercised here. Laptop must remain awake and connected for local work.

The revised homepage has not started. The implementation can now proceed as a clearly labelled cached Leeds council demonstration, preserving the three supporting pages and CV. First gather/verify the relevant public council evidence and distinguish data gaps. Arbitrary visitor-specific AI output still needs a separately authorized backend/runtime; existing classification access does not answer a sector census, investment or growth research question. No additional classification is needed to begin the cached demonstration. Browser visual QA and the iPhone website journey remain to be checked during implementation.
