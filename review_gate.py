"""Optional browser-only email entry screen for the public demonstration."""
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def wrap(document):
    document = document.replace('<html lang="en">', '<html lang="en" class="review-required review-permissions">', 1)
    document = document.replace('<link rel="stylesheet" href="/brand.css">', '<link rel="stylesheet" href="/review-access.css"><script src="/review-access.js" defer></script><link rel="stylesheet" href="/brand.css">', 1)
    document = re.sub(r'(<body[^>]*>)', lambda match: match[0] + render(), document, count=1)
    document = document.replace('<span class="avatar"', '<button type="button" id="review-sign-out">Leave review</button><span class="avatar"', 1)
    return document.replace('PRIVATE WORKING DRAFT', 'REVIEW DRAFT').replace('Private working draft', 'Review draft')


def configuration():
    config = json.loads((ROOT / 'data/review-access.json').read_text(encoding='utf-8'))
    hashes = config['allowed_email_hashes']
    if not hashes or any(len(value) != 64 or any(c not in '0123456789abcdef' for c in value) for value in hashes):
        raise ValueError('Review access must contain valid SHA-256 email digests.')
    profiles = config.get('review_profiles', {})
    fields = {'firstName', 'surname', 'jobTitle', 'organisation', 'phone', 'industry'}
    for digest, profile in profiles.items():
        if digest not in hashes or not isinstance(profile, dict) or set(profile) != fields or any(not isinstance(value, str) for value in profile.values()):
            raise ValueError('Reviewer profiles must belong to allowed addresses and contain the expected text fields.')
    interview_hashes = config.get('interview_email_hashes', [])
    if not isinstance(interview_hashes, list) or any(value not in hashes for value in interview_hashes):
        raise ValueError('Interview viewers must already be approved reviewers.')
    revision = hashlib.sha256(json.dumps({'hashes': sorted(hashes), 'profiles': profiles, 'interview': sorted(interview_hashes)}, sort_keys=True).encode()).hexdigest()[:16]
    return {'allowedEmailHashes': hashes, 'reviewProfiles': profiles, 'interviewEmailHashes': interview_hashes, 'storageKey': 'tdc-demo-review:' + revision}


def render():
    config = html.escape(json.dumps(configuration(), separators=(',', ':')), quote=False)
    return '''<section id="review-entry" class="review-entry" aria-labelledby="review-entry-title">
      <div class="review-entry-card"><div class="review-brand"><img src="/datacity-logo.svg" alt="The Data City" width="172" height="53"><small>Luke Craven · a conversation made tangible</small></div>
      <span class="review-eyebrow">An invitation to explore</span><h1 id="review-entry-title">A conversation.<br><em>Made tangible.</em></h1>
      <p>Enter your invited email address to explore the demonstration and my proposed contribution to The Data City.</p>
      <form id="review-entry-form" novalidate><label for="review-email">Your email address</label><input id="review-email" type="email" name="review_email" autocomplete="email" inputmode="email" maxlength="254" required placeholder="you@organisation.com" aria-describedby="review-entry-error"><p id="review-entry-error" class="review-entry-error" role="status" aria-live="polite"></p><button id="review-enter" type="submit" disabled>Explore the proposal <span aria-hidden="true">↗</span></button></form>
      <noscript><p>Enable JavaScript to use this demonstration’s email entry screen.</p></noscript>
      <span class="review-entry-footer">Independent concept demonstration · Luke Craven</span></div>
    </section><template id="review-access-config">''' + config + '</template>'
