"""Export the four reviewed pages without credentials, a server, or API calls."""
import importlib.util
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('review_site', ROOT / 'site.py')
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)
OUT = ROOT / 'dist'

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for route in site.PAGES:
        target = OUT / ('index.html' if route == '/' else route.lstrip('/') + '/index.html')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(site.render(route), encoding='utf-8')
    for name in ['style.css', 'data.js']:
        shutil.copyfile(ROOT / 'static' / name, OUT / name)
    # Platform access control must protect these files; never use public Pages.
    (OUT / '_headers').write_text('/*\n  Cache-Control: private, no-store\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: no-referrer\n  Content-Security-Policy: default-src \'none\'; style-src \'self\'; script-src \'self\'; connect-src \'none\'; base-uri \'none\'; frame-ancestors \'none\'; form-action \'none\'\n')
    print('Four pages exported from the reviewed cache. No provider request made.')

if __name__ == '__main__':
    build()
