"""Optional browser-only email entry screen for the public demonstration."""
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def wrap(document):
    document = document.replace('<html lang="en">', '<html lang="en" class="review-required">', 1)
    document = document.replace('</head>', '<link rel="stylesheet" href="/review-access.css"><script src="/review-access.js" defer></script></head>', 1)
    document = re.sub(r'(<body[^>]*>)', lambda match: match[0] + render(), document, count=1)
    document = document.replace('<span class="avatar"', '<button type="button" id="review-sign-out">Leave review</button><span class="avatar"', 1)
    return document.replace('PRIVATE WORKING DRAFT', 'REVIEW DRAFT').replace('Private working draft', 'Review draft')


def configuration():
    config = json.loads((ROOT / 'data/review-access.json').read_text(encoding='utf-8'))
    hashes = config['allowed_email_hashes']
    if not hashes or any(len(value) != 64 or any(c not in '0123456789abcdef' for c in value) for value in hashes):
        raise ValueError('Review access must contain valid SHA-256 email digests.')
    revision = hashlib.sha256(''.join(sorted(hashes)).encode()).hexdigest()[:16]
    return {'allowedEmailHashes': hashes, 'storageKey': 'tdc-demo-review:' + revision}


def render():
    config = html.escape(json.dumps(configuration(), separators=(',', ':')), quote=False)
    return '''<section id="review-entry" class="review-entry" aria-labelledby="review-entry-title">
      <div class="review-entry-card"><div class="review-brand"><span aria-hidden="true">LC</span><div>Luke Craven<small>The Data City conversation</small></div></div>
      <span class="review-eyebrow">An invitation to explore</span><h1 id="review-entry-title">A conversation.<br><em>Made tangible.</em></h1>
      <p>Enter your invited email address to explore the demonstration and my proposed contribution to The Data City.</p>
      <form id="review-entry-form" novalidate><label for="review-email">Your email address</label><input id="review-email" type="email" name="review_email" autocomplete="email" inputmode="email" maxlength="254" required placeholder="you@organisation.com" aria-describedby="review-entry-error"><p id="review-entry-error" class="review-entry-error" role="status" aria-live="polite"></p><button id="review-enter" type="submit" disabled>Explore the proposal <span aria-hidden="true">↗</span></button></form>
      <p class="review-entry-note">No password or ChatGPT account needed. Your email is checked in this browser and is not sent anywhere.</p><noscript><p>Enable JavaScript to use this demonstration’s email entry screen.</p></noscript>
      <span class="review-entry-footer">Independent concept demonstration · Luke Craven</span></div>
    </section><template id="review-access-config">''' + config + '</template>'
