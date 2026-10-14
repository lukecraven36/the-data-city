"""Present an explicitly reviewed response; never contact a provider."""
import html
import json
from pathlib import Path
from urllib.parse import urlsplit
import api

SNAPSHOT = Path(__file__).resolve().parent / "data/reviewed-sample.json"


def esc(value):
    return html.escape(str(value), quote=True)


def website_link(value):
    if not isinstance(value, str) or not value:
        return '', 'Not returned'
    url = value if '://' in value else 'https://' + value
    try:
        parsed = urlsplit(url)
        if parsed.scheme not in ('https', 'http') or not parsed.hostname or parsed.username or parsed.password:
            return '', 'Link unavailable'
    except ValueError:
        return '', 'Link unavailable'
    return url, value


def reviewed_sample():
    try:
        private_sample = api.PRIVATE / 'reviewed-sample.json'
        path = private_sample if private_sample.exists() else SNAPSHOT
        sample = json.loads(path.read_text(encoding='utf-8'))
        if sample.get('attempt') != 1 or not isinstance(sample.get('response'), dict):
            return None
        return sample
    except (OSError, ValueError, AttributeError):
        return None


def entries(response, key):
    value = response.get(key)
    return [row for row in value if isinstance(row, dict)] if isinstance(value, list) else []


def taxonomy(response, key, title, explanation, expanded=False):
    rows = entries(response, key)
    if rows:
        body = '<div class="table-wrap"><table><caption class="sr-only">' + esc(title) + ' returned by the API</caption><thead><tr><th scope="col">Classification</th><th scope="col">Code</th><th scope="col">Raw score</th></tr></thead><tbody>'
        for row in rows:
            body += f'<tr><td>{esc(row.get("Description", "Not returned"))}</td><td class="code">{esc(row.get("Code", "Not returned"))}</td><td>{esc(row.get("Score", "Not returned"))}</td></tr>'
        body += '</tbody></table></div>'
    else:
        body = '<p class="empty">No classifications returned in this sample.</p>'
    return f'<details class="taxonomy"{" open" if expanded else ""}><summary>{esc(title)} <span>{len(rows)} returned</span></summary><p class="small">{esc(explanation)}</p>{body}</details>'


def render(sample):
    response = sample['response']
    companies = entries(response, 'SimilarCompanies')
    try:
        used = len(api.summary())
        usage = f'Current local ledger: {used} of 2 attempts used'
    except api.Blocked:
        usage = 'At retrieval: 1 of 2 attempts used · authoritative ledger remains on Luke’s PC'
    classifications = ''.join(taxonomy(response, *args) for args in [
        ('RTICs', 'Real-Time Industrial Classifications', 'The Data City’s activity categories for emerging industries. These are matches to the submitted description.', True),
        ('RSICs', 'Real-Time SIC classifications', 'AI-derived matches to Standard Industrial Classification categories. Raw scores are shown as returned.'),
        ('RNAICs', 'Real-Time North American classifications', 'Matches to North American industry categories. Raw scores use their own scale.'),
        ('SICs', 'SIC classifications', 'The SIC field is empty here. A hypothetical description does not establish an official company classification.')
    ])
    cards = ''
    for index, row in enumerate(companies):
        url, label = website_link(row.get('Website'))
        name = esc(row.get('CompanyName', 'Name not returned'))
        number = esc(row.get('CompanyNumber', 'Not returned'))
        similarity = esc(row.get('Similarity', 'Not returned'))
        link = f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} ↗<span class="sr-only"> (opens a new tab)</span></a>' if url else esc(label)
        cards += f'''<article class="company" data-name="{name}" data-number="{number}" data-website="{esc(url)}" data-similarity="{similarity}"><div class="company-heading"><span class="rank">{index+1:02d}</span><h3>{name}</h3></div><dl><div><dt>Company number</dt><dd>{number}</dd></div><div><dt>Similarity score</dt><dd>{similarity}</dd></div></dl><p class="company-link">{link}</p><label class="compare-choice" hidden><input type="checkbox" aria-label="Compare {name}"> Compare company</label></article>'''
    return f'''<div class="eyebrow">01 / Data · a working example</div>
    <h1>From a description<br>to <em>market context.</em></h1>
    <p class="intro">Explore how The Data City classifies an AI business idea and surfaces companies to investigate. One real API response, presented in a different way.</p>
    <div class="sample-status"><span class="tag">Saved API response · HTTP 200</span><span class="small">13 October 2026 · Instant Classification</span></div>
    <section class="brief"><div class="eyebrow">The starting point · hypothetical company</div><h2>Computer vision for manufacturing</h2><blockquote>{esc(response.get('Description', 'Description not returned'))}</blockquote><p class="small">This description was written for the experiment. It does not describe an identified company.</p></section>
    <section aria-labelledby="classifications-title"><div class="section-heading"><div><span class="eyebrow">Understand the activity</span><h2 id="classifications-title">What the engine returned</h2></div></div>{classifications}
    <aside class="note"><strong>Questions worth investigating.</strong> The textile and engineering-biology matches are unexpected for this input. Keep them visible as leads to examine; the response does not explain why they matched. Scores are not calibrated probabilities, and scales differ across classification systems.</aside></section>
    <section aria-labelledby="companies-title"><div class="section-heading"><div><span class="eyebrow">Explore potential peers</span><h2 id="companies-title">{len(companies)} similar companies returned</h2></div></div><p class="small">In the provider’s returned order. Similarity is a starting point for research, not proof of supplier suitability. Company websites have not been independently verified.</p>
    <div class="compare-toolbar" hidden><p id="selection-status" role="status" aria-live="polite">Select two companies to compare the returned fields.</p><button id="clear-comparison" type="button">Clear selection</button></div>
    <div class="companies">{cards or '<p>No similar companies returned.</p>'}</div>
    <section id="comparison" class="comparison" aria-labelledby="comparison-title" hidden><h3 id="comparison-title">The returned details, side by side</h3><p class="small">The API supplied no individual company descriptions, financials or verified capabilities for these matches.</p><div id="comparison-content"></div></section></section>
    <section class="sample-footer"><h2>Read the evidence with its limits</h2><p>These results came from one successful classification request. This view reads the saved sample; selecting companies and reopening pages make no API calls. It is not a live market search or access to the full company dataset.</p><p class="small">{usage}. Provider remaining balance: unknown.</p>
    <a class="source" href="https://docs.thedatacity.com/instant-classification/guides/quickstart" target="_blank" rel="noopener noreferrer">API documentation ↗</a></section>'''
