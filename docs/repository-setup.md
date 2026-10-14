# Repository and environment handoff

Private repository: https://github.com/lukecraven36/the-data-city

The GitHub connector verified private visibility and push access. Luke created the repository after the integration could not create it automatically. Its initial README commit is preserved in the merged history. The prepared source is on branch `main`; no site is published.

Local checkout: `/workspace/the-data-city`. The current managed environment is running; this project has its own directory and ignored private runtime state.

In Codex Cloud's environment setup UI, select this private repository and create/connect the environment. No environment-creation or repository-attachment tool is available in this session. Python standard-library code requires no install step. Run `python3 -m unittest discover -s tests -v` to verify the project.

Before provider requests in another environment, securely restore this project's existing `.private/` directory, including its authoritative usage ledger. Do not initialize a replacement budget. Configure provider secrets outside Git. No provider request was recorded at repository setup, and none was dispatched in this session. The original private ledger is absent from this checkout, so the lifetime local count cannot currently be verified. Requests remain blocked; do not recreate the budget. See README.md for secure signup/authentication and explicit classification steps.

Private GitHub visibility does not make a website private. Do not enable public preview access or deploy without Luke's instruction.

The source-only ZIP is exported from Git and contains no credentials, response cache or usage database. It is suitable for reviewing/importing source, not for restoring the attempt ledger.
