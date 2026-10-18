# Ryan's feedback — branding and discovery wording

Implemented on 18 October 2026 from Ryan's full supplied message, including the changes outside quotation marks. The question headings already matched and remain unchanged.

## Discovery defaults

1. **What are you trying to achieve?**

   We’re an economic development branch of a combined authority and as a part of our growth plans we want to understand the technology business landscape. We want to explore which types of businesses are active, their scale and capabilities, and where there may be opportunities for economic development and investment support.

2. **What information do you already have access to?**

   Our starting point is Companies House records, ONS data and local business surveys. We’re also currently using a free trial of Beauhurst.

3. **What information are you hoping to receive or what question do you want answered?**

   Relevant technology businesses, what they do and where they are based. We want to see the number of companies, employees per sector, jobs and skills, alongside GVA and investment data. Any data relating to our IS-8 footprint or clusters would also be a bonus.

The second answer follows Ryan's “something to this effect” guidance rather than including his editorial explanation about competitor language. The third answer replaces the previous dashboard-focused wording in full. These are desired outcomes in the customer's brief; no new company data, GVA, skills, sector-employment or IS-8 measures were fabricated or retrieved. All seven files in `data/` were checked against pre-edit SHA-256 hashes and remain byte-for-byte unchanged. The prepared ten-company report, calculations, sources and demo values remain intact. Longer pre-filled answers expand to fit on screen.

## Branding

Reference: https://us.thedatacity.com/ . Its HTML, stylesheet and screenshot were inspected directly. The visual language uses deep navy (`#100a2d`), cyan (`#02b1d0`), violet (`#6b3fb0`), magenta (`#d10956`) and Poppins. The logo is the actual full SVG lockup at https://us.thedatacity.com/datacity-logo.svg; the icon comes from https://us.thedatacity.com/datacity-logo-icon.svg. Both are used as supplied, with no path alterations. Logo use follows Luke's instruction relaying Ryan's suggestion. The experience retains its independent-concept/proposed-contribution context.

`static/brand.css` applies the reference typography and visual treatment to the sidebar, entry page, forms, report, role and About Me. Existing component colours were coordinated to the brand palette; chart values were not changed. Four local Poppins Latin font weights avoid runtime Google Fonts requests. Font sources were provided by Google Fonts; the SIL Open Font License is included at `static/fonts/OFL-Poppins.txt`. Public project-prefix builds include fonts and logos locally. The local server's CSP permits these same-origin assets.

## Other corrections

- Navigation, page title and eyebrow: **A Role at The Data City**, including legacy redirect text.
- Expansion: **in the US and globally**.
- Reflection and footer: **Mitali**, replacing Natalia. The obsolete spelling-confirmation reminder was removed; the separate Pathed role/date reminder remains.

## Verification

21 offline Python tests, JavaScript syntax checks and the GitHub Pages static build passed. Browser checks covered the exact three pre-filled answers, both approved email entries, rejected addresses, cross-page sessions, leaving the review, complete contact-to-report journey, local logo/font loading, role tabs and keyboard navigation, About Me reflection, both legacy redirects, responsive widths 320–1440, no-JavaScript behaviour and no external requests/browser errors. Desktop and mobile screenshots were visually reviewed. Mobile checks use emulation, not physical Safari. Temporary QA servers were stopped. No provider request or private-state change occurred.
