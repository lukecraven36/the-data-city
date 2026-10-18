# Discovery homepage — first draft, 18 October 2026

## Latest interaction update

The mobile processing state now sits at the top of the viewport. Navigation, topbar and journey headers are temporarily hidden during the prepared sequence; the progress list and cancel action fit within a 320×568 viewport. Cancelling restores the discovery interface. The content wrapper no longer centres the short loading screen vertically.

The three editable answers use native textareas with an aria-hidden, matching highlight layer. Selected discovery phrases are marked yellow and update during editing, resizing and restoring the example. The actual field values and submitted brief stay plain text. Highlight rendering escapes user input before adding marker elements; this is a prepared phrase matcher and makes no AI/provider request.

Yellow markers in the results connect the brief to company count, activities, registered geography, company scale/funding and the corresponding narrative. They do not imply that the preview contains GVA, jobs/skills, sector-level employment or IS-8 analysis. Those requests appear in the existing next-demonstration list. All seven data files remain byte-for-byte unchanged.

Verification: 21 offline tests and static build passed. Focused browser checks covered aligned editable highlights, preservation of exact field values, edited HTML escaping, keyword restoration, mobile loading/cancel position at 320×568, 375×667 and 390×844, unchanged report metrics (10 companies, £3.75m turnover, £845k funding, 5 regions/nations), visible evidence highlights, header restoration, and no browser errors or external requests. Desktop and mobile screenshots were visually reviewed.

The main route now presents **Your details → Your challenge → Your insights**, using the existing Family Hub palette, sidebar, rounded cards and serif emphasis. AI Lead, Commercial Product Lead and About Me remain supporting pages; the CV remains expandable. The earlier classification renderer and first reviewed response are retained in source.

## Implemented journey

- Contact form pre-populated with the seven fields Luke explicitly supplied: first name, surname, work email, telephone, job title, organisation and industry. These are intentional presentation defaults, not harvested contacts.
- Three editable, pre-populated discovery answers for a generic local-government technology-business use case. No Leeds restriction or automatic geographic exclusion.
- A short, cancellable prepared sequence before the report. No live AI, provider connection or background research is represented as happening.
- Four headline cards, turnover/funding bars, UK registered-location map, statutory SIC activity breakdown, interpretive summaries and proposed follow-up copy.
- All ten original businesses in a searchable table; company profiles open from chart rows, table entries and map points. Up to three businesses can be compared.
- Evidence tab with original description-level classifications and a downloadable local discovery brief.
- Back/edit/restart controls, accessible field labels, validation, keyboard tab navigation, focus-managed company dialog and reduced-motion support.
- Prominent rationale sections explain contact-first discovery, the three questions, earlier value and the more focused demonstration handoff.

## Data used for presentation

`data/technology-discovery-enriched.json` remains the researched record, with sources, missing financial values and company-level identity caveats unchanged.

Luke explicitly authorised illustrative turnover/funding values for this presentation and asked that individual chart numbers not carry demonstration labels. `data/discovery-demo-values.json` is a separate presentation layer. These are **fictional visualisation values, not researched estimates**; they must never be imported back into the source dataset or described as Companies House, Dealroom or Data City facts. The original disclosed London Software Tech turnover is retained. Reported employee averages, filed net assets, company identities, SIC codes and registered postcodes remain sourced.

The whole experience carries an independent-concept label; the processing screen says it is a prepared sequence. No per-number disclaimer appears in the dashboard. The downloadable brief records that turnover/funding visuals include illustrative values. The presenter should give the explanation Luke described before presenting these numbers as a concept. Mixed-period totals are presentation composition, not economic analysis or investment advice.

The contact form holds edits only in page memory. It does not submit to The Data City, a CRM, email, analytics or any API. Reloading restores the presentation defaults. The proposed follow-up text explicitly notes that no enquiry has been sent. No meeting or callback is actually arranged.

The current [official trial page](https://thedatacity.com/free-trial/), checked 18 October 2026, describes a use-case-led 30-minute demo and seven-day platform access. The proposal adds earlier insight; it does not claim that their current published offer is a generic walkthrough.

## Verification

- 19 Python tests passed, covering existing ledger/HTTP/CV safety and new dataset separation, safe embedded-data escaping and the authorised contact defaults.
- JavaScript syntax checks passed for discovery, prior data view and CV scripts.
- Full authenticated-loopback browser journey exercised with desktop Edge/Chromium and a 390px mobile viewport. No browser errors and no outbound page requests.
- Tested invalid email, cancellation, answer escaping, report charts, company drill-down, search/empty state, three-company comparison limit, local brief download, keyboard tabs, all supporting routes and restart.
- Responsive widths 320, 375, 390 and 768px checked for root horizontal overflow. The table scrolls within its container. Fixed mobile dialog positioning and small-width report actions during QA.
- Browser checks emulate iPhone dimensions; they are not a physical iPhone/Safari test. Phone Remote pairing was already completed by Luke and was not repeated.
- Static four-page export built successfully. Credential scan of the export passed. The original external private ledger remains healthy at 2/2; no classification, authentication request, allowance change or credential migration occurred.
- Preview screenshots and browser verification JSON are in ignored `.openai/local/preview/`. Temporary authenticated QA servers were stopped after checks.

## Main implementation files

- `discovery_view.py`: renders the journey and embeds the minimum prepared company dataset.
- `static/discovery.js`: browser-local state, validation, report rendering and interaction.
- `static/discovery.css`: responsive homepage styles scoped to the discovery route.
- `data/discovery-demo-values.json`: isolated illustrative financial presentation values.
- `data/uk-map.json`: UK/Ireland geometry from Natural Earth, with source attribution. Registered postcode coordinates come from the enrichment pack.
- `site.py`, `build_site.py`: route and asset integration; the existing authenticated local server remains loopback-only.

Scope for the next review: wording, visual hierarchy, chart selection and form-to-report pacing. The three supporting pages have not been editorially rebuilt.

## Private publication

Published successfully on 18 October 2026 at https://data-city-conversation.lukecraven36.chatgpt.site, with the existing owner-only audience preserved.

Site source commit: `4b6d7a3434b3a70eb121359e29f095a65deeda26`.
Saved version: `appgprj_6acf1c4ed75c8191b1c46bcce73705e3~appgver_98200a13a4dc8191a74dcd9c82632515`.
Deployment: `appgdep_6ad4ba33ca148191bcd5731e5220175b` (`succeeded`).

The existing Site source history was reconciled in an ignored publication checkout. The GitHub checkout remains on `main` at `8a6fc4a996a2680c2e1096b388f708bbab8d8160`, with all migration, research and homepage changes preserved locally. No GitHub push was made during publication. The original `.private` directory remains outside OneDrive and was excluded from the published source and static archive.
