# Missing usage ledger investigation — 13 October 2026

No original ledger or initialization marker was found under the currently accessible /workspace. No replacement was created, and no provider request was dispatched during this investigation.

The original “Build private Data City site” chat (01a136b0-1f25-7376-9c0f-ad2b01df9062) contains successful command outputs from `python3 api.py status` showing `Local attempts used: 0/2`, including after the source was pushed to GitHub. Its final status also reports zero attempts. Source commit 8340180 records that no provider request had been dispatched at repository setup.

The ledger was deliberately ignored by Git. The source archive excluded it too. A fresh source checkout therefore did not restore private runtime state.

This is evidence of zero attempts at repository handoff, not recovery of the original database or a complete audit of later activity. The environment-setup chat could not be read through the available thread reader. The current build chat has dispatched no classification requests. Luke reports signup completed during this chat and does not know earlier request history.

Keep data dispatch blocked. Restore the original database if it becomes available. Reconstructing a ledger from the recorded zero count requires Luke's explicit recovery instruction because docs/handoff.md says to stop when usage state is missing unexpectedly rather than reset it. No recovery has been performed.

## Recovery completed

Luke explicitly confirmed that no calls had ever been made. Together with the original recorded zero count, this reconciles the request history. The private ledger was reconstructed using `python3 api.py init --confirm-no-prior-attempts`; `python3 api.py status` verified 0/2 local attempts. No provider request was made. Preserve this ledger across future runs; do not initialize another allowance. Provider quota remains unknown.

## Local handoff prepared

Luke selected the hypothetical AI manufacturing description and instructed us to try it. Cloud dispatch is now disabled by `.private/dispatch-disabled`; its ledger was archived as `.private/usage.cloud-archive.sqlite3`. The private handoff ZIP transfers the recorded zero-attempt ledger and selected input to the Windows project. It contains no authentication token or password. The installer preserves the existing local token and refuses to overwrite a ledger or initialization marker. Only the Windows copy is to dispatch requests after installation. Do not restore or initialize a parallel cloud allowance. No data request was dispatched during preparation. Installer checks and the eleven safety tests passed. Local installation and the first response remain pending Luke's terminal actions.

## First real response

Luke installed the transferred ledger and explicitly dispatched attempt 1 from his Windows PC. He shared status showing HTTP 200, response saved, and 1/2 attempts used, together with the response JSON. No cloud request was dispatched. The ledger on Luke's PC is authoritative; the archived zero ledger and initial transfer ZIP must never be reused to reset it. The new first-version installer does not contain or replace a ledger or token.
