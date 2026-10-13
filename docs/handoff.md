# The Data City — simplified Codex handoff

Updated: 13 October 2026
Owner: Luke Craven
Intended repository: `the-data-city` (private)

## Purpose and scope

Create a simple, credible site for a conversation with Alex Craven and Natalia at The Data City. It should show an interest in their business, two potential ways Luke could contribute, and the personal background behind reconnecting.

**This document replaces the previous handoff in full.** Remove the earlier sprawling dashboard requirements, cheat-sheet page, conversion calculators, sector scenarios and embedded source-code appendix. Do not carry them forward as requirements.

The current task is only to update this Markdown. No site, repository, account or API connection has been created or changed by this update. The instructions below are for a subsequent Codex task.

Use exactly four pages, in this order:

| Navigation | Purpose |
|---|---|
| Data | Present actual information obtained through The Data City’s APIs. The final layout is undecided. |
| AI Lead | Explain their existing AI activity, emerging ambition and where Luke could contribute. |
| Commercial Product Lead | Start with customer and market needs; identify valuable use cases before proposing tools. |
| About Me | Present Luke’s relevant history, earlier conversations and reasons for reconsidering. |

Keep the experience calm, readable and visually polished: clear navigation, generous spacing, restrained colour and short sections. Reuse the Family Hub’s visual style only if its source or reference is available; do not invent a match. Avoid a fifth page, dense dashboards or decorative interactions. Place source links alongside factual claims.

## 1. Data — connect first, decide the presentation afterwards

This is the opening page. Its purpose is to present The Data City’s data, not Luke’s work at Simpson Associates. **Do not decide its charts, filters or dashboard shape until the first real response has been inspected.** Begin with an honest connection status and, once available, a straightforward view of the retrieved information.

### Access route: distinguish the two APIs

| Route | What it provides | Access requirement |
|---|---|---|
| Instant Classification API | Classifies a supplied description or website; may return classification codes and similar companies. | Self-service work-email signup; documented evaluation allowance. |
| Industry Engine / UK company-data API | Company records, including classifications, financials and metadata according to access rights. | API key issued manually by The Data City; unrestricted free access is not confirmed. |

**An Instant Classification account is not access to the full company dataset.** Do not describe a classification response as a download of their database, and do not use its login token against the company-data API.

Planned account email: `luke@pathedconsulting.co.uk`. This is the email Luke has authorised for the proposed setup; it is not a password, token or proof of an existing account. Keep it out of the public-facing page.

### Future Codex: initial connection and retrieval instructions

1. Read the current [Instant Classification quickstart](https://docs.thedatacity.com/instant-classification/guides/quickstart), [authentication guide](https://docs.thedatacity.com/instant-classification/guides/authentication) and [limits](https://docs.thedatacity.com/instant-classification/guides/rate-limits).
2. Use an existing account if Luke has one. Otherwise guide him through the [official signup](https://instant-classification-api.thedatacity.com/signup) with the email above. A work email is required. Luke completes password entry, verification if requested, and acceptance of the provider’s terms. Do not claim signup has succeeded until it has.
3. Obtain and retain authentication on the server using the documented flow below. Never put credentials in the frontend, Git, screenshots or logs. Supply an `.env.example` containing placeholders only.
4. Let Luke choose one or two public company websites or descriptions. Validate the payload locally before dispatch. Do not choose confidential customer material from Simpson.
5. Make one request, save the result, inspect the actual fields and explain what the access supports. Use the second request only if it adds value. **Stop after a maximum of two data-request attempts in total.**
6. Cache results privately so development and repeated viewing do not spend additional calls. Discuss the opening page’s shape with Luke after inspecting the sample. If access is unavailable, show “Not connected” and the next access step; do not fabricate a live dataset.

“Starting to scrape their data” here means this small, authorised API retrieval. Do not crawl their signed-in platform, bypass access controls, bulk-download records or attempt to reconstruct their proprietary dataset.

### Authentication and classification reference

Base URL: `https://instant-classification-api.thedatacity.com`

| Step | Request | Details |
|---|---|---|
| Login | `POST /api/v1/login/access-token` | Form-encoded `username` and `password`; use the returned `access_token`. |
| Check token | `POST /api/v1/login/test-token` | `Authorization: Bearer <token>`; checks authentication without a classification call. |
| Retrieve classification | `POST /api/v1/instantClassification` | Bearer header plus JSON containing exactly one of `Text` or `Website`. |

Example payloads — select one, not both:

```json
{"Website": "https://a-company-chosen-by-luke.example"}
```

```json
{"Text": "A public company description chosen by Luke"}
```

These are illustrative payloads, not selected companies or requests to execute automatically. Set the classification timeout to at least 120 seconds. Tokens are documented as valid for eight days, with no refresh-token flow; handle expiry deliberately without silently replaying a data request.

The response can include `RTICs`, `RSICs`, `RNAICs`, `SICs` and `SimilarCompanies`. Inspect the actual schema, tolerate empty or missing fields and retain the original response. Explain classification labels in plain English where they appear. Do not treat similarity or classification scores as calibrated probabilities, or infer unreturned company details.

### Preserve the evaluation allowance

The provider currently documents **20 successful classifications over the account’s lifetime**, with no reset, and **five requests per minute**. Failed 4xx/5xx responses do not consume its successful-classification allowance.

Luke’s stricter initial limit is **two dispatched data-request attempts**, including failures, across all runs and sessions. Implement a persistent server-side counter, reserve an attempt before dispatch and prevent concurrent calls from exceeding the cap. If the usage state is missing unexpectedly, stop rather than reset it. Disable automatic retries, scheduled refreshes, pagination and data calls on page load. Keep token checks separate from the data-request counter. Existing account usage means the provider allowance may already be partly consumed.

Do not increase the cap or purchase access without a further instruction from Luke. Show local attempts used separately from provider quota; do not claim to know his remaining provider balance without evidence. Verify the cap and cached viewing without spending live requests.

### If the opening page needs richer company records

Follow the [Industry Engine API quickstart](https://docs.thedatacity.com/api-reference/guides/quickstart). Keys are issued manually; Luke can request evaluation access from `support@thedatacity.com`. Prepare the request for him if needed; do not send it without instructions.

The documented starting endpoint is:

```text
GET https://product-api.thedatacity.com/api/v2/companies/{CompanyNumber}
Authorization: Bearer <separately-issued-API-key>
```

Check licensing, permitted display and available fields before retrieval. If Luke later provides this key, keep the same two-attempt initial budget across data APIs rather than creating another allowance. Richer access is a possible next step, not a dependency to hide or a promise of free data.

## 2. AI Lead

This page should answer: **What are The Data City already doing with AI, where does their ambition lead, and what could Luke contribute?**

### Evidence to build on

- Their core proposition uses machine learning and company information to understand business activity. AI is already part of their data product, rather than simply a future chatbot layer.
- [Instant Classification was introduced in September 2025](https://thedatacity.com/blog/introducing-instant-classification-tool/). It makes their classification capability available from a website or description. Do not label it a new 2026 launch.
- Their [September 2026 strategic update](https://thedatacity.com/blog/the-future-of-business-intelligence/) describes globally scalable AI-powered data infrastructure and a delivered first version of their global product. It specifically identifies customers building their own AI insight tools using maintained, auditable company data. It sets out expansion ambitions for 2027/28; distinguish ambition from achieved rollout.
- The [AMRC North West case study](https://thedatacity.com/case-studies/amrc-north-west/) offers an example of API-supported supplier discovery using natural-language queries. Describe its prototype status accurately; do not imply a generally available production product.

Recheck these sources before building. Distinguish existing machine-learning classification from newer generative-AI workflows. Luke’s contact has described Alex as enthusiastic and hands-on with Claude Code; that is conversation context, not an official product announcement.

### Luke’s potential contribution

Luke reports approaching five months of recent customer conversations about AI, including NHS organisations, councils and financial businesses. His contribution is understanding the decision, workflow, constraints and desired outcome, then helping turn them into a practical, demonstrable approach.

Present the proposed AI Lead contribution as:

- Discover and prioritise customer problems where their data can support AI-assisted work.
- Translate those problems into small, evidence-backed prototypes with the technical team.
- Define what a good result looks like: useful answers, traceable evidence, appropriate human review and a measurable improvement to the workflow.
- Help customers understand and adopt the capability through tailored demonstrations and clear explanations.

One possible direction to explore is an evidence-linked company or supplier discovery assistant. **This is a hypothesis to validate with customers, not an instruction to build a chatbot now.** Any later prototype must reflect the API fields and access actually available.

Use Luke’s sector experience as evidence of discovery skills. Do not import Simpson project examples, client records or Microsoft architecture into The Data City’s product story. Do not imply Luke has already led their AI strategy or that an AI Lead vacancy exists.

## 3. Commercial Product Lead

Lead with the principle: **Understand the customer’s challenge before deciding what to build.**

This is a proposal for helping the business connect customer discovery, product decisions and commercial conversations. It is not an assertion that a vacancy exists or that existing products were poorly built.

Explain the work in four simple steps:

1. **Understand:** Who is the customer, what decision or task matters, and where does the current approach fail?
2. **Validate:** How frequent and costly is that problem? What evidence shows a customer would adopt or pay for an improvement?
3. **Shape:** Identify the smallest useful use case; check available data, feasibility and constraints with the solution architect and product team.
4. **Prove:** Demonstrate against the customer’s requirements, agree success measures and feed learning back into product priorities.

Luke’s strengths are engaging customers, qualifying interest, discovering requirements, tailoring demonstrations and translating findings into a clear commercial and technical handoff. His previous Data City discussions centred on helping convert interest into deals. Keep that context concise; omit speculative funnel numbers and conversion calculators.

If a simple interaction would help the future page, use one editable customer-needs brief: customer, challenge, current process, desired outcome, required data and success measure. Do not add scoring engines or multiple tools before the page’s purpose is agreed.

Keep a clear distinction from AI Lead: this page addresses product value and market fit across the portfolio; AI Lead addresses applying AI effectively. Both begin with a customer problem.

Do not publish Ryan’s comments about internal frustration, individual targets or product decisions as facts. The constructive proposition is customer-led discovery and validation.

## 4. About Me

Write in Luke’s voice. Keep it personal, balanced and suitable for a direct conversation with Alex or Natalia.

### Relevant work history and evidence

| Background | What can currently be used |
|---|---|
| Panintelligence | Public LinkedIn material identifies Luke as a Pre Sales Consultant. Relevant to his customer-facing analytics and demonstration experience. |
| Simpson Associates | Luke describes his current work as AI-focused presales with exposure to Microsoft and customer AI needs. Confirm the exact job title and dates before publishing a formal timeline. |
| Pathed Consulting | Public LinkedIn material links Luke to Pathed Consulting and discusses BI, presales and making dashboards useful to the people using them. Confirm the formal role and dates. |
| Earlier analytics / consultancy experience | Include Luke’s BI, analytics, requirements discovery and demonstration background. Earlier material mentions Catalyst BI / Catalyst Cloud; verify exact employer, role and dates before adding a dated entry. |

LinkedIn identity found: [Luke Craven](https://www.linkedin.com/in/luke-craven-887b3a81/). The full profile could not be retrieved during this update, so this is not a complete verified CV. Do not invent dates, tenure, qualifications, results or a chronological order for unverified roles.

Public supporting posts:

- [Panintelligence presales / AI event](https://www.linkedin.com/posts/luke-craven-887b3a81_not-another-ai-event-going-down-an-absolute-activity-7244403179319099392-o1Wb)
- [Pathed Consulting / BI and presales](https://www.linkedin.com/posts/luke-craven-887b3a81_pathed-consulting-bi-and-pre-sales-excellence-activity-7457743743950180352-mJRF)

### Previous conversations and reconsidering the decision

Luke previously spoke with Natalia about a customer-facing presales opportunity at The Data City. He chose Simpson Associates because he saw a clearer AI-focused opportunity involving Microsoft. He now recognises that he did not fully appreciate how central AI already was to The Data City’s proposition.

Suggested draft for the page, to review with Luke before sharing:

> When we spoke previously, I chose an AI-focused opportunity with Simpson Associates. At the time, I did not fully appreciate how central AI was to The Data City’s business, or where you were taking it.
>
> Since then, I have spent more time with customers understanding their AI needs and the problems they actually want to solve. I have also encountered challenges around culture and expectations at Simpson, which have made me reflect on where I work best and what I want to contribute. Looking back, I wonder whether I got the decision wrong.
>
> I would like to reopen the conversation with a clearer view of how I could help: understanding customers and the market, shaping useful products, and turning your AI ambition into practical customer value.

This is Luke’s personal reflection, not an objective claim about Simpson’s culture. Do not invent incidents, criticise individuals or add accusations. Keep the reflection brief and spend most of the page on what he brings and why he wants to reconnect. Use “Natalia” as supplied in the latest instruction; confirm spelling before direct correspondence.

## Future Codex workflow and completion criteria

1. Use or create a **private** GitHub repository named `the-data-city` when repository creation is authorised and available. Otherwise, Luke creates it with a README and uploads this file as `docs/handoff.md`.
2. Connect that repository to a Codex Cloud environment and give Codex the prompt below. Private GitHub access does not automatically make a hosted site private; keep any review preview private too.
3. Implement the connection separately from the page design. Obtain a maximum of two real sample responses once credentials and selected inputs are available. If blocked, report the exact missing access and continue only with work that does not require it.
4. Agree the opening page’s presentation after reviewing the actual data. Build the four-page site from this brief with clear sources and simple navigation. Do not resurrect the previous app’s complexity.
5. Check navigation, factual labels, credential handling, persistent request limits and cached viewing. Report what is connected, what remains unverified and any access limitations. Do not publish the site or contact The Data City automatically.

### Paste into Codex for the later build

```text
Read docs/handoff.md. It replaces all previous instructions for this project.

Create a simple private four-page site: Data, AI Lead, Commercial Product Lead,
and About Me. Do not build the old dashboard or add a cheat-sheet page.

Start with the documented Data City API connection. The planned account email
is luke@pathedconsulting.co.uk. Do not assume an account or dataset entitlement
exists. Guide me through secure provider signup/authentication as needed.

Use at most two dispatched data-request attempts across runs, with a persistent
server-side limit and no automatic retries. Cache responses and keep secrets
out of the frontend and Git. Do not scrape the signed-in platform or bulk data.

Inspect the first real response before deciding the opening page's visual shape.
If access is blocked, tell me exactly what is missing and show a truthful pending
state. Keep the AI and commercial pages focused on The Data City's needs and
my proposed contribution. Use the About Me narrative carefully and flag missing
career dates for verification. Do not invent history, live data or product claims.

Keep the implementation small and easy to review. Do not publish the site or
send messages to anyone without my instruction.
```
