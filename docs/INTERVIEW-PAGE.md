# Interview presentation

The featured `/interview` page is an independent proposal for discussion. The existing discovery demo, role page, CV and legacy role redirects remain available.

`interview_view.py` renders the full semantic content. `static/interview.css` gives it a responsive editorial layout. `static/interview.js` progressively enhances the five-stage customer journey with selectable illustrative handoffs, arrow-key navigation and Home/End support. Without JavaScript all handoffs remain readable. Reduced-motion preferences are respected.

The presentation distinguishes the existing prepared demo from a proposed customer journey and potential RevOps handoffs. It does not simulate integrations, claim live generation, add metrics or send information anywhere. Measures and a 30/60/90-day approach are suggestions to validate with the team.

The new route uses the existing browser email entry. This is a convenience screen on a public site, not server-enforced access control. No access profiles, datasets, API client or private usage state are changed.

The static exporter supports root hosting and `/the-data-city/`, including the new local CSS and JS. Both workflows run the Python suite and browser-script syntax checks. The authenticated local server allows the new route and assets.

## Verification

- 25 offline Python tests; all browser scripts pass Node syntax checks.
- Root and Pages-prefix exports checked, including direct Interview entry, existing routes and legacy redirects.
- Chromium/Edge previews inspected at 1440, 390, 375 and 320px; no horizontal overflow. All five stages, keyboard navigation, CTA destinations, session persistence and sign-out checked.
- All four reviewer profiles still populate the existing discovery form. No browser errors or external requests during the local checks.
- Original data, access configuration, provider client and page-content files match their pre-change SHA-256 hashes.
- Mobile checks use browser emulation; physical iPhone/Safari remains unverified.
