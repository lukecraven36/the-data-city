# Interview briefing

The `/interview` page is Luke’s internal preparation reference. Its three sections are company overview (history, senior leadership, business model and classification workflow), recent public developments and expansion, and a proposed role/contribution. The previous promotional hero and presentation journey have been replaced.

`interview_view.py` holds concise research checked on 26 October 2026, with links to official sources. Current leadership is reproduced from the company team page, including Mitali Mookerjee as Managing Director (UK). No reporting hierarchy is inferred. Performance figures and expansion plans are labelled with their announcement date; Luke’s interpretation and potential responsibilities are clearly distinguished from company facts. Country coverage is described as an announcement, with current availability to confirm.

`static/interview.css` provides large text, a history timeline, six leadership cards, a data pipeline, SIC/RSIC/RTIC comparison, news cards and contribution cards. The only disclosure uses native HTML details/summary, which works without page-specific JavaScript. The obsolete Interview script has been removed from exports and workflow checks.

The page retains its existing route, hosting prefixes and reviewer visibility. Only the configured Luke email can see it in the app; other reviewers are redirected to discovery and do not see the Interview navigation. This is a browser convenience on a public static site, not server-enforced access control. Research uses public material only.

The existing demonstration, About Me, role content, datasets, access configuration, provider client and private API state are outside this change. No classification requests are needed.

Validation: 26 offline tests and remaining JavaScript syntax checks pass. Root and Pages-prefix exports pass. Local Edge/Chromium checks cover 1440/390/375/320px with no horizontal overflow, all three section links, native disclosure keyboard control, both CTA destinations and all four reviewer identities. Original page content, access settings and datasets match their pre-change hashes. Physical Safari remains unverified.
