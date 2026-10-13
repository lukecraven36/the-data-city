"""Explicit CLI-only provider access; no data calls from web routes."""
import argparse
import getpass
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.private'
DB = PRIVATE / 'usage.sqlite3'
TOKEN = PRIVATE / 'token.json'
BASE = 'https://instant-classification-api.thedatacity.com'
CAP = 2

class Blocked(Exception):
    pass

def private_dir():
    PRIVATE.mkdir(mode=0o700, exist_ok=True)
    PRIVATE.chmod(0o700)

def connect(path=None):
    path = path or DB
    # mode=rw is essential: missing state must never silently recreate a budget.
    try:
        c = sqlite3.connect(f'{path.as_uri()}?mode=rw', uri=True, timeout=10)
        c.execute('PRAGMA synchronous=FULL')
        count = c.execute('SELECT COUNT(*) FROM attempts').fetchone()[0]
        row = c.execute('SELECT cap FROM budget WHERE id=1').fetchone()
        if row != (CAP,) or count > CAP:
            raise Blocked('Usage ledger is invalid. Stop and reconcile existing attempts.')
        return c
    except sqlite3.Error:
        raise Blocked('Usage ledger missing or damaged. Stop; restore it before making requests.') from None

def initialize():
    private_dir()
    # One-time bootstrap marker prevents reinitialization if the DB disappears.
    marker = PRIVATE / 'initialized'
    if marker.exists() or DB.exists():
        raise Blocked('Already initialized or partial state exists. Never reset the budget.')
    fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    c = sqlite3.connect(DB)
    DB.chmod(0o600)
    with c:
        c.execute('CREATE TABLE budget (id INTEGER PRIMARY KEY CHECK(id=1), cap INTEGER NOT NULL CHECK(cap=2))')
        c.execute('INSERT INTO budget VALUES (1,2)')
        c.execute('''CREATE TABLE attempts (id INTEGER PRIMARY KEY, route TEXT NOT NULL,
            fingerprint TEXT UNIQUE NOT NULL, payload TEXT NOT NULL, created REAL NOT NULL,
            status TEXT NOT NULL, http_status INTEGER, body BLOB)''')
        c.execute('''CREATE TRIGGER enforce_cap BEFORE INSERT ON attempts
            WHEN (SELECT COUNT(*) FROM attempts)>=2
            BEGIN SELECT RAISE(ABORT, 'two-attempt cap reached'); END''')
    c.close()

def validate(payload):
    if not isinstance(payload, dict) or len(payload) != 1 or next(iter(payload), '') not in ('Text', 'Website'):
        raise Blocked('Supply exactly one of Text or Website.')
    key, value = next(iter(payload.items()))
    if not isinstance(value, str) or not value.strip() or len(value) > 10000:
        raise Blocked('Input must be nonempty text, at most 10,000 characters.')
    if key == 'Website':
        p = urllib.parse.urlsplit(value)
        if p.scheme not in ('https', 'http') or not p.hostname or p.username or p.password or p.fragment:
            raise Blocked('Choose a public HTTP(S) company website without credentials or a fragment.')
        host = p.hostname.lower()
        if '.' not in host or host.endswith(('.localhost', '.local', '.internal')):
            raise Blocked('Choose a public company website.')
        try:
            if not ipaddress.ip_address(host).is_global:
                raise Blocked('Private network addresses are not permitted.')
        except ValueError:
            pass
    return payload

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

# Default proxy/CA trust retained. No retries and no redirects, including POST replay.
def request(path, body, token=None, form=False):
    headers = {'Content-Type': 'application/x-www-form-urlencoded' if form else 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method='POST')
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req, timeout=150) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def token_value():
    token = os.environ.get('TDC_ACCESS_TOKEN')
    if token:
        if token == 'YOUR_SERVER_SIDE_TOKEN':
            raise Blocked('Configure a real server-side token or use login.')
        return token
    try:
        data = json.loads(TOKEN.read_text())
        if data['expires_at'] <= time.time():
            raise Blocked('Token expired. Log in deliberately; no data request has been replayed.')
        return data['access_token']
    except (OSError, ValueError, KeyError):
        raise Blocked('No usable token. Complete official signup if needed, then run login.') from None

def login():
    email = input('Work account email: ').strip()
    password = getpass.getpass('Provider password (hidden; not stored): ')
    status, raw = request('/api/v1/login/access-token', urllib.parse.urlencode({'username': email, 'password': password}).encode(), form=True)
    del password
    if status != 200:
        raise Blocked(f'Login returned HTTP {status}. Check credentials/account activation; no data call made.')
    try:
        token = json.loads(raw)['access_token']
        if not isinstance(token, str) or not token:
            raise ValueError()
    except (ValueError, KeyError):
        raise Blocked('Login did not return an access token.') from None
    private_dir()
    # File mode remains private even when overwriting.
    fd = os.open(TOKEN, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        json.dump({'access_token': token, 'expires_at': time.time() + 8*86400 - 60}, f)
    TOKEN.chmod(0o600)
    print('Token saved privately on the server. Password discarded.')

def classify(payload, path=None, transport=request, token=None):
    validate(payload)
    encoded = json.dumps(payload, sort_keys=True).encode()
    fingerprint = hashlib.sha256(b'instant-classification:' + encoded).hexdigest()
    c = connect(path)
    try:
        # Serialize reservation across processes; commit durably before dispatch.
        c.execute('BEGIN IMMEDIATE')
        existing = c.execute('SELECT id,status FROM attempts WHERE fingerprint=?', (fingerprint,)).fetchone()
        if existing:
            c.rollback()
            return existing[0], True
        if c.execute('SELECT COUNT(*) FROM attempts').fetchone()[0] >= CAP:
            raise Blocked('Two-attempt cap reached. Use cached results; no further request permitted.')
        credential = token or token_value()
        cur = c.execute('INSERT INTO attempts(route,fingerprint,payload,created,status) VALUES (?,?,?,?,?)',
                        ('instant-classification', fingerprint, encoded.decode(), time.time(), 'reserved'))
        attempt = cur.lastrowid
        c.commit()
        try:
            status, raw = transport('/api/v1/instantClassification', encoded, credential)
        except Exception:
            # Ambiguous network outcomes still consume the reserved attempt.
            with c:
                c.execute("UPDATE attempts SET status='network outcome unknown' WHERE id=?", (attempt,))
            raise Blocked('Network outcome unknown. Attempt retained; no retry. Check the ledger.') from None
        with c:
            c.execute('UPDATE attempts SET status=?,http_status=?,body=? WHERE id=?',
                      ('response saved' if 200 <= status < 300 else 'provider rejected', status, raw, attempt))
        return attempt, False
    finally:
        c.close()

def summary(path=None):
    c = connect(path)
    try:
        return c.execute('SELECT id,route,created,status,http_status FROM attempts ORDER BY id').fetchall()
    finally:
        c.close()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('init'); sub.add_parser('login'); sub.add_parser('test-token'); sub.add_parser('status')
    call = sub.add_parser('classify')
    call.add_argument('--payload', required=True, help='Local JSON file with one public Text or Website input.')
    call.add_argument('--confirm-public-input', action='store_true')
    inspect = sub.add_parser('inspect'); inspect.add_argument('id', type=int)
    args = p.parse_args()
    try:
        if args.command == 'init':
            initialize(); print('Persistent budget initialized once: 0 of 2 attempts.')
        elif args.command == 'login': login()
        elif args.command == 'test-token':
            status, _ = request('/api/v1/login/test-token', b'', token_value())
            print(f'Token check HTTP {status}; not a classification call. Provider remaining balance unknown.')
        elif args.command == 'status':
            rows = summary(); print(f'Local attempts used: {len(rows)}/2. Provider remaining balance: unknown.')
            for row in rows: print(row)
        elif args.command == 'inspect':
            c = connect()
            row = c.execute('SELECT http_status,body FROM attempts WHERE id=?', (args.id,)).fetchone(); c.close()
            if not row or row[1] is None: raise Blocked('No saved response for that attempt.')
            # Explicit terminal-only inspection. Never route raw provider output into frontend or logs.
            print(f'HTTP {row[0]}')
            print(row[1].decode('utf-8', errors='replace'))
        elif args.command == 'classify':
            if not args.confirm_public_input: raise Blocked('Confirm that Luke selected this public input.')
            payload = json.loads(Path(args.payload).read_text())
            attempt, cached = classify(payload)
            print(f'Attempt {attempt}: {"cached; no dispatch" if cached else "dispatch recorded"}. Inspect privately before designing Data.')
    except (Blocked, OSError, ValueError, sqlite3.Error):
        # Known errors are useful; transport errors must not print request headers or secrets.
        import sys
        error = sys.exc_info()[1]
        print(str(error) if isinstance(error, Blocked) else 'Local operation failed; no automatic retry. Check input and private ledger.')
        raise SystemExit(1)

if __name__ == '__main__': main()
