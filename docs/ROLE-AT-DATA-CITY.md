# A Role at Data City — 18 October 2026

Latest refinements: the single role-title pill is replaced by four outlined boxes (Commercial, AI, Product, Pre-sales). The hero scroll link and arrow are removed. The business-opportunity copy no longer names Ryan. The doughnut centre is empty and its fourth legend entry is Product and AI Development. The initial roadmap outputs are process clarity/challenges/opportunities and demonstrations/concepts customers recognise. Existing tests, static build and responsive browser checks passed after these edits.

The former AI Lead and Commercial Product Lead pages are combined at `/role-at-data-city`, with the navigation label **A Role at Data City** and proposed role **Commercial AI Product Lead**. There are now three main pages. Both previous role URLs retain a route to the combined page: authenticated 308 redirects locally and minimal redirect documents in the static export.

The visual story centres on customer value: Discover → Demonstrate → Convert → Develop. Four keyboard-accessible tabs reveal problem discovery, a tailored demo storyboard, a commercial next step and a product learning loop. With JavaScript disabled, all four panels remain readable. The existing discovery demonstration is linked directly, so the proposal shows an example of the approach.

The hero uses an orbital responsibility diagram; a four-part doughnut expresses connected contributions without assigning measured time proportions. The sample sector bars are explicitly illustrative. A proposed 30/60/90-day roadmap and outcome scorecard add a concrete starting point without inventing company metrics or conversion forecasts.

Ryan's business-priority/US-expansion perspective comes from Luke's message and is attributed accordingly. The Keltbray example (five challenges, £100,000 contract and later AI opportunity) comes from Luke's supplied current-role account. The proposed title and scope are a discussion proposal, not a claim of an advertised vacancy or agreed appointment.

Implementation: `role_view.py`, `static/role.css`, `static/role.js`, route/build integration and three-item shared navigation. About Me retains its content, with its navigation ordinal changed from 04 to 03. The discovery flow, API code and private state are unchanged.

Verification: 19 Python tests, JavaScript syntax and static export passed. Authenticated loopback browser checks passed for all four panels, keyboard navigation, three-item navigation, both legacy redirects, existing homepage and five-point About Me profile, no-JavaScript content, and responsive widths 320/375/390/650/768/900/1024/1440. No browser errors or external page requests occurred. Desktop and mobile screenshots were visually inspected. Mobile checks use emulation, not physical Safari. Temporary QA servers were stopped.

Published successfully with the existing owner-only audience at https://data-city-conversation.lukecraven36.chatgpt.site/role-at-data-city/ . Site source commit: `553047ce354849bc4204edf1419925fe6723d591`. Saved version: `appgprj_6acf1c4ed75c8191b1c46bcce73705e3~appgver_de989b2ba52c8191a643a4edeb412d41`. Deployment: `appgdep_6ad4c2573a788191903662eeab361abe`. Local GitHub working changes remain preserved; the Site source was published separately.
