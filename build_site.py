"""Export the four reviewed pages without credentials, a server, or API calls."""
import importlib.util
import argparse
import re
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('review_site', ROOT / 'site.py')
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)
OUT = ROOT / 'dist'

def build(base_path='', email_gate=False):
    if base_path and (not re.fullmatch(r'/[A-Za-z0-9/_-]+/?', base_path) or '//' in base_path):
        raise ValueError('Use an absolute URL path such as /the-data-city/.')
    prefix = base_path.rstrip('/')
    def public_paths(document):
        return re.sub(r'((?:href|src)=")/(?!/)', lambda match: match[1] + prefix + '/', document)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for route in site.PAGES:
        target = OUT / ('index.html' if route == '/' else route.lstrip('/') + '/index.html')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(public_paths(site.render(route, email_gate=email_gate)), encoding='utf-8')
    for old_route, destination in site.REDIRECTS.items():
        destination = prefix + destination + '/'
        target = OUT / old_route.lstrip('/') / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url={destination}"><link rel="canonical" href="{destination}"><title>A Role at The Data City</title></head><body><a href="{destination}">Continue to A Role at The Data City</a></body></html>', encoding='utf-8')
    for name in ['style.css', 'data.js', 'cv.js', 'discovery.js', 'discovery.css', 'role.css', 'role.js', 'interview.css', 'review-access.css', 'review-access.js', 'brand.css', 'datacity-logo.svg', 'datacity-logo-icon.svg']:
        content = (ROOT / 'static' / name).read_text(encoding='utf-8')
        if name.endswith('.css'):
            content = content.replace('url("/fonts/', 'url("' + prefix + '/fonts/')
        (OUT / name).write_text(content, encoding='utf-8')
    shutil.copytree(ROOT / 'static/fonts', OUT / 'fonts')
    # Host-enforced access protects the default Sites build. The optional email
    # screen is only a convenience gate for the explicitly public demonstration.
    (OUT / '_headers').write_text('/*\n  Cache-Control: private, no-store\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n  Content-Security-Policy: default-src \'none\'; style-src \'self\'; font-src \'self\'; img-src \'self\'; script-src \'self\'; connect-src \'none\'; base-uri \'none\'; frame-ancestors \'none\'; form-action \'none\'\n')
    (OUT / '.nojekyll').touch()
    (OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
    print('Four pages and two legacy redirects exported from the reviewed cache. No provider request made.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-path', default='', help='Hosting prefix, e.g. /the-data-city/.')
    parser.add_argument('--email-gate', action='store_true', help='Add the browser-only review email screen.')
    args = parser.parse_args()
    build(args.base_path, args.email_gate)
