# GitHub Pages email-entry demonstration

Luke authorised making `lukecraven36/the-data-city` public on 18 October 2026 after GitHub rejected Pages activation for the private repository on the current plan. The intended URL is `https://lukecraven36.github.io/the-data-city/`. The existing ChatGPT Site is separate and its sharing is unchanged.

## What the email screen does

The public Pages build shows an email entry screen before the normal interface on all three pages, including direct links. It normalises case and whitespace, checks an email hash against `data/review-access.json`, and stores the accepted hash and normalised sign-in email in browser session storage. Navigation within the same tab keeps the session; Leave review clears it. It sends no email or authentication request and requires no ChatGPT account or password. A changed allowlist or reviewer profile invalidates older stored sessions.

This is a browser-only convenience screen. It does not verify ownership of an email address, prevent impersonation, protect source/HTML or make a public repository private. Hashing avoids publishing a plain email list; it does not turn the allowlist into a secret. JavaScript-disabled browsers retain the entry screen in the normal UI, but public files remain retrievable. Actual private access requires server-side authentication and authorisation.

The four email hashes correspond to the addresses Luke supplied for himself, Ryan Williams, Alex Craven and Mitali Mookerjee. To add another approved reviewer, compute SHA-256 of the trimmed lowercase address, append the lowercase 64-character digest to `allowed_email_hashes` in `data/review-access.json`, then commit and push. Add corresponding display defaults under `review_profiles`, keyed by the same hash, to personalise the contact form. Do not store passwords or tokens in that file.

## Build and deployment

`python build_site.py --base-path /the-data-city/ --email-gate` creates the Pages export. Internal asset/navigation links are prefixed for the project subpath. The old role URLs redirect within the same prefix. `.nojekyll` and a crawler-disallowing robots file are generated; robots/noindex are discovery preferences, not access restrictions. GitHub Pages does not apply the `_headers` file used by other hosts.

`.github/workflows/pages.yml` checks the source, builds the gated export and deploys the Pages artifact on `main` pushes or manual dispatch. No API token, ledger, environment file, local research cache or publication checkout is exported. All data comes from the prepared demonstration. The default build remains compatible with the existing root-hosted ChatGPT Site and does not add this screen.

## Verification

21 Python tests passed, including project-prefix export and access-list revision checks. JavaScript syntax passed. The exported static build passed desktop and mobile browser checks: initial/direct-page entry, malformed and unlisted emails, both approved addresses, whitespace/case normalisation, navigation persistence, leaving/reloading, all three pages, legacy redirects, the contact-to-report journey, no-JavaScript UI, no outbound requests and no browser errors. Widths 320/390/768/1440 were checked. Entry screenshots were visually reviewed. Browser mobile checks are emulation, not a physical Safari test.

Authoritative Data City provider credentials and the 2/2 usage ledger remain in the original directory outside OneDrive. No provider request, credential migration or allowance reset occurred.

## Personalised contact defaults — 20 October 2026

The sign-in address selects the matching reviewer profile before the main interface appears. The form fills first name, surname, sign-in email, job title, organisation and office phone. The topbar initials, discovery persona and generated brief use the same person. Restarting the demo restores that person's defaults; leaving review and signing in as someone else resets the journey rather than retaining the previous person's form. Same-tab navigation and reload restore the matching profile. If session storage is blocked, the current page still fills correctly; another navigation may require re-entry.

Profiles: Luke Craven, AI specialist, Pathed Consulting; Ryan Williams, Business Development Executive; Alex Craven, CEO; Mitali Mookerjee, Managing Director (UK). The latter three are at The Data City. The company team pages list Mitali as Managing Director (UK), rather than CRO: https://thedatacity.com/about-us/meet-the-team/mitali-mookerjee/ . Ryan and Alex roles were checked against their corresponding official team profiles. The office placeholder is 0333 335 5665, published at https://thedatacity.com/contact-us/ . It is used for the demonstration's phone field, including Luke's profile. Industry remains Local Government to preserve the prepared authority use case.

The static profile map contains display fields keyed by email hash, not the plain-text email allowlist. The sign-in email is retained in this browser tab for the form and is removed on Leave review. Saved email/hash mismatches keep the entry screen visible. This association check is for consistent defaults; the public screen remains a browser-only convenience gate, not verified identity.

Verification: 22 offline tests, JavaScript syntax and the static build passed. Browser checks exercised every contact field for all four reviewers, uppercase input, same-tab switching, navigation and reload, persona and report-brief names, restart, mismatched saved sessions and disabled storage. There were no browser errors or outbound page requests. No company dataset or provider state changed.
