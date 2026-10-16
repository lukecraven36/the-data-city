"""Private local review server. Read-only routes; provider access stays in api.py."""
import base64
import getpass
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import html
from pathlib import Path
import secrets
import warnings
from urllib.parse import urlsplit
import api
import data_view
import cv_view

ROOT = Path(__file__).resolve().parent
NAV = [('/', 'Data'), ('/ai-lead', 'AI Lead'), ('/commercial-product-lead', 'Commercial Product Lead'), ('/about-me', 'About Me')]

def source(url, label):
    return f'<a class="source" href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(label)} ↗</a>'

def data_page():
    sample = data_view.reviewed_sample()
    if sample:
        return data_view.render(sample)
    try:
        rows = api.summary()
        usage = f'{len(rows)} of 2 local attempts used'
        if rows:
            status = 'Response awaiting review' if any(r[4] and 200 <= r[4] < 300 for r in rows) else 'Not connected'
            next_step = 'Inspect the saved response privately and agree a useful presentation. No response is displayed until that review.' if status != 'Not connected' else 'Review the saved attempt status on the server. A failed or uncertain request still uses an attempt; no request will be retried automatically.'
        else:
            status = 'Not connected'
            next_step = 'Confirm an Instant Classification account, authenticate securely on the server, and choose one public company website or description.'
    except api.Blocked:
        usage = 'Usage state unavailable — requests blocked'
        status = 'Not connected'
        next_step = 'The persistent usage ledger is unavailable. Restore the original ledger or reconcile its history before any data request. Account access and a public input also remain unconfirmed.'
    sample_note = 'A response is saved privately and awaits inspection.' if status == 'Response awaiting review' else 'We have not yet retrieved a usable sample.'
    return f'''<div class="eyebrow">01 / Data · access first</div>
    <h1>Start with the<br>evidence.</h1>
    <p class="intro">A small, deliberate look at The Data City’s classification data. The first real response will guide what belongs here.</p>
    <section class="connection" aria-labelledby="connection-title"><div class="status"><span class="dot"></span>{status}</div>
    <h2 id="connection-title">The next step is access.</h2><p>{next_step}</p>
    <div class="ledger"><span>{usage}</span><span>Provider balance: unknown</span></div>
    <p class="small">Viewing this page uses no provider requests. Responses are saved privately; data retrieval is an explicit server-side action.</p></section>
    <section><h2>Before the first sample</h2><p>Complete official signup if needed, authenticate privately on the server, and choose one public company website or description. This environment also needs network access to the provider. No account or dataset entitlement has been established.</p>
    {source('https://instant-classification-api.thedatacity.com/signup', 'Official provider signup')}
    {source('https://docs.thedatacity.com/instant-classification/guides/authentication', 'Secure authentication guide')}</section>
    <section class="split"><div><h2>What this access can show</h2><p>Instant Classification accepts a company website or description. It can return activity classifications and similar companies. {sample_note}</p>
    {source('https://docs.thedatacity.com/instant-classification/guides/quickstart', 'Classification quickstart')}</div>
    <div><h2>For company records</h2><p>The Industry Engine API requires a separately issued key. An Instant Classification account does not establish dataset entitlement. Available fields and permitted display need confirmation.</p>
    {source('https://docs.thedatacity.com/api-reference/guides/quickstart', 'Company-data access')}</div></section>
    <aside class="note">No chart or company list has been chosen yet. Once a genuine response is reviewed, we can agree the simplest useful view.</aside>'''

def ai_page():
    return f'''<div class="eyebrow">02 / AI Lead · a proposed contribution</div><h1>Turn AI ambition<br>into <em>customer value.</em></h1>
    <p class="intro">Begin with the decision a customer needs to make. Use The Data City’s evidence to make the answer more useful, traceable and practical.</p>
    <section><h2>AI is already in the proposition</h2><p>The Data City uses machine learning to understand company activity. Instant Classification, introduced in September 2025, puts that capability into a focused company-classification workflow.</p>
    {source('https://thedatacity.com/blog/introducing-instant-classification-tool/', 'Instant Classification · September 2025')}
    <p>The September 2026 strategic update reports delivery of the first version of its global product and describes customers building AI insight tools on maintained, auditable company data. Further expansion in 2027/28 is an ambition.</p>
    {source('https://thedatacity.com/blog/the-future-of-business-intelligence/', 'Strategic update · September 2026')}</section>
    <section class="band"><h2>Where I could contribute</h2><p>My recent customer conversations about AI span NHS organisations, councils and financial businesses. I bring discovery, tailored demonstrations and a focus on the outcome people need. This is my account of that experience; its dates still need confirmation.</p>
    <ol class="steps"><li><strong>Find the useful problem</strong><span>Prioritise decisions and workflows where company data could improve the result.</span></li>
    <li><strong>Make a small prototype</strong><span>Work with the technical team on an evidence-backed demonstration of the most useful use case.</span></li>
    <li><strong>Agree what good looks like</strong><span>Traceable answers, appropriate human review and measurable workflow improvement.</span></li>
    <li><strong>Help it get adopted</strong><span>Tailor demonstrations and explain clearly where the capability helps and where judgment is still needed.</span></li></ol></section>
    <section><span class="tag">Hypothesis to validate</span><h2>Evidence-linked supplier discovery</h2><p>Could an assistant help a customer find relevant companies and explain why they match? I would first test the need with customers, then check the fields, licensing and access available. This site does not implement that prototype.</p>
    <p class="small">The supplied handoff references an AMRC North West supplier-discovery prototype. The case-study page could not be retrieved during this build, so its details remain unverified here.</p>
    {source('https://thedatacity.com/case-studies/amrc-north-west/', 'AMRC case study · verification pending')}</section>
    <aside class="note">A proposal for a conversation, with no claim that an AI Lead vacancy exists. Existing machine-learning classification and proposed generative-AI workflows are distinct.</aside>'''

def commercial_page():
    return '''<div class="eyebrow">03 / Commercial Product Lead · a proposed contribution</div><h1>Understand the need.<br>Then <em>shape the product.</em></h1>
    <p class="intro">Connect customer discovery, product decisions and commercial conversations across The Data City’s portfolio.</p>
    <section><h2>Start with the customer’s challenge</h2><p>What decision are they trying to make? Where does the current process fail? The useful starting point is the problem and its value to the customer, before choosing a tool.</p></section>
    <ol class="process"><li><span class="number">01</span><div><h2>Understand</h2><p>Identify the customer, the task that matters and the limitations of their current approach.</p></div></li>
    <li><span class="number">02</span><div><h2>Validate</h2><p>Check how often the problem occurs, what it costs and what evidence suggests a customer would adopt or pay for an improvement.</p></div></li>
    <li><span class="number">03</span><div><h2>Shape</h2><p>Define the smallest useful use case. Check data, feasibility and constraints with the solution architect and product team.</p></div></li>
    <li><span class="number">04</span><div><h2>Prove</h2><p>Demonstrate against the customer’s requirements, agree success measures and feed the learning into product priorities.</p></div></li></ol>
    <section class="band"><h2>What I would bring</h2><p>Engaging customers, qualifying interest, discovering requirements and tailoring demonstrations. I would turn those conversations into a clear commercial and technical handoff.</p><p>My earlier discussions with The Data City centred on helping convert interest into deals. This proposal develops that into a customer-led approach to value and market fit.</p></section>
    <aside class="note">This proposed contribution covers value and market fit across the portfolio. AI Lead focuses on applying AI effectively. Both begin with a customer problem; neither assumes an existing vacancy.</aside>'''

def about_page():
    return cv_view.render()

PAGES = {'/': data_page, '/ai-lead': ai_page, '/commercial-product-lead': commercial_page, '/about-me': about_page}

def render(path):
    title = dict(NAV)[path]
    symbols = ['◈', '✦', '↗', '◎']
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == path else '')+f'><span class="nav-symbol" aria-hidden="true">{symbols[i]}</span>{label}</a>' for i, (url, label) in enumerate(NAV))
    script_path = {'/': '/data.js', '/about-me': '/cv.js'}.get(path)
    script = f'<script src="{script_path}" defer></script>' if script_path else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#15242a"><title>{title} · The Data City conversation</title><link rel="stylesheet" href="/style.css">{script}</head><body><a class="skip" href="#main">Skip to content</a><div class="app-shell"><aside class="sidebar"><a class="identity" href="/"><span class="mark">LC</span><span>Luke Craven<small>The Data City conversation</small></span></a><p class="side-caption">A PROPOSED CONTRIBUTION</p><nav aria-label="Main navigation">{nav}</nav><div class="side-bottom"><strong>PRIVATE WORKING DRAFT</strong>A conversation about customer needs, useful AI and what I could contribute.</div></aside><div class="site-content"><header class="topbar"><span class="topbar-date">The Data City / {title}</span><div class="topbar-right"><span class="private">Private working draft</span><span class="avatar" aria-hidden="true">LC</span></div></header><main id="main">{PAGES[path]()}</main><footer><span>Prepared for a conversation with Alex &amp; Natalia</span><span>Working draft · 13 October 2026</span></footer></div></div></body></html>'''


class Handler(BaseHTTPRequestHandler):
    expected = None
    def log_message(self, *args):
        pass  # Never log credentials, inputs or private response content.
    def do_GET(self):
        auth = self.headers.get('Authorization', '')
        if not hmac.compare_digest(auth, self.expected or secrets.token_hex(32)):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Private local review"')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers(); return
        path = urlsplit(self.path).path
        host = self.headers.get('Host', '').split(':')[0]
        if host not in ('127.0.0.1', 'localhost'):
            self.send_error(403); return
        if path == '/style.css':
            content = (ROOT / 'static/style.css').read_bytes(); mime = 'text/css'
        elif path in ('/data.js', '/cv.js'):
            content = (ROOT / 'static' / path.lstrip('/')).read_bytes(); mime = 'text/javascript; charset=utf-8'
        elif path in PAGES:
            content = render(path).encode(); mime = 'text/html; charset=utf-8'
        else:
            self.send_error(404); return
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'self'; script-src 'self'; connect-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.end_headers(); self.wfile.write(content)

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('error', getpass.GetPassWarning)
        try:
            password = getpass.getpass('Choose a local review password (hidden; separate from your provider password): ')
        except getpass.GetPassWarning:
            raise SystemExit('Hidden entry unavailable. Open a private interactive terminal.')
    if len(password) < 12:
        raise SystemExit('Use at least 12 characters.')
    Handler.expected = 'Basic ' + base64.b64encode(('luke:' + password).encode()).decode()
    del password
    print('Private local review: http://127.0.0.1:8000 — username luke. Not published.')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
