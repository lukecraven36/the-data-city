# iPhone to local Codex — setup and proof

Prepared 18 October 2026. **Documented, not yet paired or tested on Luke's devices.**

Official instructions: https://developers.openai.com/training/walkthroughs/working-on-your-phone
Background: https://developers.openai.com/blog/mastering-codex-remote-for-engineering

## One-time device setup

1. On the Windows laptop, open the **ChatGPT desktop app**. Use the same account and workspace as the iPhone.
2. The official guide specifies **Settings → Connections → Control this Mac or PC → Set up / Add**. Scan the displayed QR code with the phone and select the connected computer. These are documented labels; availability in Luke's installed app/account is not yet verified. If absent, record the app/version and actual screen instead of guessing another menu.
3. Keep the laptop powered, awake, online and signed in. Do not alter corporate security controls or open router ports.
4. In local Codex select the actual project folder. Reconcile the two known folders in `CODEX-LOCAL-HANDOFF.md` first; source checkout selection must preserve the authoritative API ledger and token.
5. On the iPhone open **Remote**, select the Windows host and the local project/task. A cloud Work conversation alone does not establish local execution.

## Harmless first proof

Send this to the local task from the phone:

> Read docs/CODEX-LOCAL-HANDOFF.md and docs/MOBILE-LOCAL-WORKFLOW.md. Verify the Windows host, actual project path, Git branch/commit and working-tree changes. Reconcile the two documented folders without overwriting private state. Do not initialise a ledger, authenticate, classify or publish. Run the existing offline tests and static build yourself. Return the commands, results and any blockers here. Never print credentials.

Review the result on the phone; queue or steer a small follow-up such as asking for the test count. Verify the displayed host/path really are Windows and results arrive without copying PowerShell output. If an action needs approval, verify it can be reviewed on the phone without granting broad persistent access. Record those observations, not just a QR pairing.

## What depends on the laptop

Local commands, source edits, tests and the local provider connector run on Windows. Secrets remain there. Phone Remote provides control; it does not expose `127.0.0.1` as a website. The existing owner-only hosted preview can be reviewed separately at https://data-city-conversation.lukecraven36.chatgpt.site . Do not expose the local API service or enable public hosting for convenience.

After offline proof, local Codex can inspect ledger status and deliberately check authentication; renewed password entry remains a private human action if needed. No classification should run just to test pairing. Keep the two-attempt budget and no automatic retries.

## Verification record to complete locally

- Windows host / app version: pending.
- Reconciled project path / branch / commit: pending.
- Offline tests and build: pending on Windows.
- Phone starts task and receives result: pending.
- Phone review / approval / follow-up: pending.
- Current API ledger and token check: pending; historic usage 1/2.
- Mobile website visual test: pending; distinct from Remote control.
