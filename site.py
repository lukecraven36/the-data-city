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
import discovery_view
import role_view
import interview_view
import review_gate

ROOT = Path(__file__).resolve().parent
NAV = [('/interview', 'Interview'), ('/', 'Discover Your Market'), ('/role-at-data-city', 'A Role at The Data City'), ('/about-me', 'About Me')]
REDIRECTS = {'/ai-lead': '/role-at-data-city', '/commercial-product-lead': '/role-at-data-city'}

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

def about_page():
    return cv_view.render()

PAGES = {'/interview': interview_view.render, '/': discovery_view.render, '/role-at-data-city': role_view.render, '/about-me': about_page}

def render(path, email_gate=False):
    title = dict(NAV)[path]
    symbols = ['✦', '◈', '↗', '◎']
    nav = ''.join(f'<a href="{url}"'+(' data-review-feature="interview"' if url == '/interview' else '')+(' aria-current="page"' if url == path else '')+f'><span class="nav-symbol" aria-hidden="true">{symbols[i]}</span>{label}</a>' for i, (url, label) in enumerate(NAV))
    script_path = {'/interview': '/interview.js', '/': '/discovery.js', '/role-at-data-city': '/role.js', '/about-me': '/cv.js'}.get(path)
    script = f'<script src="{script_path}" defer></script>' if script_path else ''
    if path == '/':
        script += '<link rel="stylesheet" href="/discovery.css">'
    if path == '/role-at-data-city':
        script += '<link rel="stylesheet" href="/role.css">'
    if path == '/interview':
        script += '<link rel="stylesheet" href="/interview.css">'
    body_class = ' class="discovery-layout"' if path == '/' else (' class="interview-layout"' if path == '/interview' else '')
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#100a2d"><title>{title} · The Data City conversation</title><link rel="stylesheet" href="/style.css">{script}<link rel="stylesheet" href="/brand.css"><link rel="icon" type="image/svg+xml" href="/datacity-logo-icon.svg"></head><body{body_class}><a class="skip" href="#main">Skip to content</a><div class="app-shell"><aside class="sidebar"><a class="identity" href="/"><span class="site-brand"><img src="/datacity-logo.svg" alt="The Data City" width="172" height="53"><small>Luke Craven · a proposed contribution</small></span></a><p class="side-caption">A PROPOSED CONTRIBUTION</p><nav aria-label="Main navigation">{nav}</nav><div class="side-bottom"><strong>PRIVATE WORKING DRAFT</strong>A conversation about customer needs, useful AI and what I could contribute.</div></aside><div class="site-content"><header class="topbar"><span class="topbar-date">The Data City / {title}</span><div class="topbar-right"><span class="private">Private working draft</span><span class="avatar" aria-hidden="true">LC</span></div></header><main id="main">{PAGES[path]()}</main><footer><span>Prepared for a conversation with Alex &amp; Mitali</span><span>Working draft · 18 October 2026</span></footer></div></div></body></html>'''
    return review_gate.wrap(document) if email_gate else document


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
        if path.rstrip('/') in REDIRECTS:
            self.send_response(308)
            self.send_header('Location', REDIRECTS[path.rstrip('/')])
            self.send_header('Cache-Control', 'no-store')
            self.end_headers(); return
        if path in ('/style.css', '/discovery.css', '/role.css', '/interview.css', '/brand.css'):
            content = (ROOT / 'static' / path.lstrip('/')).read_bytes(); mime = 'text/css'
        elif path in ('/datacity-logo.svg', '/datacity-logo-icon.svg'):
            content = (ROOT / 'static' / path.lstrip('/')).read_bytes(); mime = 'image/svg+xml'
        elif path in ('/fonts/poppins-400.woff2', '/fonts/poppins-500.woff2', '/fonts/poppins-600.woff2', '/fonts/poppins-700.woff2'):
            content = (ROOT / 'static' / path.lstrip('/')).read_bytes(); mime = 'font/woff2'
        elif path in ('/data.js', '/cv.js', '/discovery.js', '/role.js', '/interview.js'):
            content = (ROOT / 'static' / path.lstrip('/')).read_bytes(); mime = 'text/javascript; charset=utf-8'
        elif path in PAGES:
            content = render(path).encode(); mime = 'text/html; charset=utf-8'
        else:
            self.send_error(404); return
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'self'; font-src 'self'; img-src 'self'; script-src 'self'; connect-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
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
