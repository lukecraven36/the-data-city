import concurrent.futures
import base64
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import api
# Python's built-in site module is already loaded. Load the app explicitly.
import importlib.util
spec = importlib.util.spec_from_file_location('review_site', Path(api.ROOT)/'site.py')
review = importlib.util.module_from_spec(spec); spec.loader.exec_module(review)

class Safety(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)/'.private'
        self.patch = patch.multiple(api, PRIVATE=self.folder, DB=self.folder/'usage.sqlite3', TOKEN=self.folder/'token.json')
        self.patch.start(); api.initialize(); self.path = api.DB
        self.calls = []
    def tearDown(self):
        self.patch.stop(); self.tmp.cleanup()
    def transport(self, *args):
        self.calls.append(args)
        return 200, b'{"RTICs": [], "UnknownField": null}'
    def classify(self, text, transport=None):
        return api.classify({'Text': text}, self.path, transport or self.transport, token='test-only')
    def test_cap_and_cache_across_reopened_connections(self):
        self.assertEqual(self.classify('public one'), (1, False))
        self.assertEqual(self.classify('public one'), (1, True))
        self.classify('public two')
        with self.assertRaises(api.Blocked): self.classify('public three')
        self.assertEqual(len(self.calls), 2)
        c=api.connect(self.path)
        self.assertEqual(c.execute('SELECT body FROM attempts WHERE id=1').fetchone()[0], b'{"RTICs": [], "UnknownField": null}')
        c.close()
    def test_concurrent_reservations_share_cap(self):
        def run(i):
            try: return self.classify(f'public {i}')
            except api.Blocked: return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(run, range(6)))
        self.assertEqual(sum(x is not None for x in results), 2)
        self.assertEqual(len(self.calls), 2)
    def test_failure_is_retained_without_retry(self):
        def fail(*args):
            self.calls.append(args); raise TimeoutError()
        with self.assertRaises(api.Blocked): self.classify('public one', fail)
        self.assertEqual(self.classify('public one'), (1, True))
        self.classify('public two', lambda *a: (401,b'{"detail":"expired"}'))
        with self.assertRaises(api.Blocked): self.classify('public three')
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(len(api.summary(self.path)), 2)
    def test_missing_or_corrupt_state_fails_closed(self):
        self.path.unlink()
        with self.assertRaises(api.Blocked): self.classify('public one')
        with self.assertRaises(api.Blocked): api.initialize()
        self.assertEqual(self.calls, [])
        self.path.write_bytes(b'not sqlite')
        with self.assertRaises(api.Blocked): self.classify('public one')
    def test_invalid_payload_and_missing_token_do_not_spend(self):
        for payload in [{'Text':'x','Website':'https://x.com'}, {}, {'Website':'http://127.0.0.1'}, {'Text':''}]:
            with self.assertRaises(api.Blocked): api.classify(payload, self.path, self.transport, token='test-only')
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(api.Blocked): api.classify({'Text':'public'}, self.path, self.transport)
        self.assertEqual(api.summary(self.path), [])
    def test_page_reads_never_dispatch_or_expose_secrets(self):
        with patch.object(api, 'request', side_effect=AssertionError('Web dispatched')):
            for _ in range(3):
                for path in review.PAGES:
                    output = review.render(path)
                    self.assertIn('aria-current="page"', output)
                    self.assertNotIn('luke@pathedconsulting.co.uk', output)
                    self.assertNotIn('access_token', output)
        self.assertEqual(len(review.PAGES), 4)
        self.assertEqual(api.summary(self.path), [])
        self.classify('public one')
        self.assertIn('Response awaiting review', review.render('/'))
        self.assertNotIn('UnknownField', review.render('/'))
    def test_http_access_and_exact_page_routes(self):
        review.Handler.expected = 'Basic ' + base64.b64encode(b'luke:test-review-password').decode()
        server = review.ThreadingHTTPServer(('127.0.0.1', 0), review.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        client = http.client.HTTPConnection('127.0.0.1', server.server_port)
        try:
            for path in list(review.PAGES) + ['/style.css']:
                client.request('GET', path)
                response=client.getresponse(); response.read()
                self.assertEqual(response.status, 401)
                client.request('GET', path, headers={'Authorization':review.Handler.expected})
                response=client.getresponse(); response.read()
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader('Cache-Control'), 'no-store')
            for path in ['/.private/token.json', '/docs/handoff.md', '/cheat-sheet']:
                client.request('GET', path, headers={'Authorization':review.Handler.expected})
                response=client.getresponse(); response.read(); self.assertEqual(response.status,404)
            client.request('GET', '/', headers={'Authorization':review.Handler.expected, 'Host':'evil.example'})
            response=client.getresponse(); response.read(); self.assertEqual(response.status,403)
            self.assertEqual(api.summary(self.path), [])
        finally:
            client.close(); server.shutdown(); server.server_close(); thread.join()

    def test_db_trigger_also_enforces_cap(self):
        self.classify('one'); self.classify('two')
        import sqlite3
        c=api.connect(self.path)
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO attempts(route,fingerprint,payload,created,status) VALUES ('x','x','{}',0,'x')")
        c.close()

if __name__ == '__main__': unittest.main()
