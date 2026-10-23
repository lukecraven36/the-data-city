import concurrent.futures
import base64
import http.client
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import api
import data_view
# Python's built-in site module is already loaded. Load the app explicitly.
import importlib.util
spec = importlib.util.spec_from_file_location('review_site', Path(api.ROOT)/'site.py')
review = importlib.util.module_from_spec(spec); spec.loader.exec_module(review)

class PrivateDirectory(unittest.TestCase):
    def test_external_state_selection_never_initializes_or_copies_state(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            external = root / 'existing-private'
            with patch.object(api, 'ROOT', root), patch.dict(os.environ, {}, clear=True):
                self.assertEqual(api.private_directory(), root / '.private')
                config = root / '.openai/local/private-directory.txt'
                config.parent.mkdir(parents=True)
                config.write_text(str(external), encoding='utf-8')
                self.assertEqual(api.private_directory(), external)
                self.assertFalse(external.exists())
                with patch.dict(os.environ, {'TDC_PRIVATE_DIR': str(root / 'override')}):
                    self.assertEqual(api.private_directory(), root / 'override')
                for invalid in ('', 'relative-private'):
                    config.write_text(invalid, encoding='utf-8')
                    with self.assertRaises(api.Blocked):
                        api.private_directory()

class Safety(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)/'.private'
        self.patch = patch.multiple(api, PRIVATE=self.folder, DB=self.folder/'usage.sqlite3', TOKEN=self.folder/'token.json')
        self.patch.start(); api.initialize(); self.path = api.DB
        self.sample_patch = patch.object(data_view, "SNAPSHOT", self.folder / "not-reviewed.json")
        self.sample_patch.start()
        self.calls = []
    def tearDown(self):
        self.sample_patch.stop(); self.patch.stop(); self.tmp.cleanup()
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
                    if path != '/':
                        self.assertNotIn('luke@pathedconsulting.co.uk', output)
                    self.assertNotIn('access_token', output)
        self.assertEqual(len(review.PAGES), 4)
        self.assertEqual(api.summary(self.path), [])
        self.classify('public one')
        self.assertIn('Response awaiting review', review.data_page())
        self.assertNotIn('UnknownField', review.render('/'))
    def test_http_access_and_exact_page_routes(self):
        review.Handler.expected = 'Basic ' + base64.b64encode(b'luke:test-review-password').decode()
        server = review.ThreadingHTTPServer(('127.0.0.1', 0), review.Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        client = http.client.HTTPConnection('127.0.0.1', server.server_port)
        try:
            for path in list(review.PAGES) + ['/style.css', '/data.js', '/cv.js', '/discovery.js', '/discovery.css', '/role.css', '/role.js', '/interview.css', '/interview.js']:
                client.request('GET', path)
                response=client.getresponse(); response.read()
                self.assertEqual(response.status, 401)
                client.request('GET', path, headers={'Authorization':review.Handler.expected})
                response=client.getresponse(); response.read()
                self.assertEqual(response.status, 200)
                self.assertEqual(response.getheader('Cache-Control'), 'no-store')
            for path, destination in review.REDIRECTS.items():
                client.request('GET', path, headers={'Authorization':review.Handler.expected})
                response=client.getresponse(); response.read()
                self.assertEqual(response.status, 308)
                self.assertEqual(response.getheader('Location'), destination)
            for path in ['/.private/token.json', '/.private/reviewed-sample.json', '/docs/handoff.md', '/cheat-sheet']:
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

    def test_init_cli_requires_explicit_history_confirmation(self):
        with patch.object(sys, 'argv', ['api.py', 'init']), patch.object(api, 'initialize') as initialize:
            with self.assertRaises(SystemExit):
                api.main()
            initialize.assert_not_called()

    def test_login_refuses_echoed_password_fallback(self):
        with patch('builtins.input', return_value='test@example.com'), \
             patch.object(api.getpass, 'getpass', side_effect=api.getpass.GetPassWarning()), \
             patch.object(api, 'request') as request:
            with self.assertRaises(api.Blocked):
                api.login()
            request.assert_not_called()

    def test_missing_ledger_page_is_truthful_and_does_not_reset(self):
        self.path.unlink()
        with patch.object(api, 'initialize', side_effect=AssertionError('Reset')), \
             patch.object(api, 'request', side_effect=AssertionError('Dispatch')):
            output = review.data_page()
            self.assertIn('Usage state unavailable', output)
            self.assertIn('reconcile its history', output)
            self.assertNotIn('0 of 2 local attempts used', output)

    def test_reviewed_response_is_cached_and_escaped(self):
        sample = {'attempt': 1, 'response': {
            'Description': '<script>private input</script>',
            'RTICs': [{'Description': '<b>AI</b>', 'Code': 'A', 'Score': 0.614}],
            'SimilarCompanies': [{'CompanyName': '<img src=x>', 'CompanyNumber': '001',
                                 'Website': 'javascript://alert(1)', 'Similarity': 0.8376199}]}}
        (self.folder / 'reviewed-sample.json').write_text(json.dumps(sample))
        with patch.object(api, 'request', side_effect=AssertionError('Dispatch')):
            for _ in range(3):
                output = review.data_page()
                self.assertIn('Saved API response', output)
                self.assertIn('&lt;script&gt;', output)
                self.assertNotIn('<img src=x>', output)
                self.assertNotIn('href="javascript:', output)
                self.assertIn('No classifications returned', output)
                self.assertNotIn('61.4%', output)
        self.assertEqual(api.summary(), [])

    def test_cloud_dispatch_disabled_after_handoff(self):
        (self.folder / 'dispatch-disabled').write_text('transferred')
        with self.assertRaises(api.Blocked):
            self.classify('public input')
        self.assertEqual(self.calls, [])

    def test_cv_has_five_profile_points_and_three_highlights_per_role(self):
        import cv_view
        cv = json.loads((cv_view.ROOT / 'data/cv.json').read_text())
        output = review.render('/about-me')
        self.assertEqual(len(cv['profile']['summary']), 5)
        for section in [cv['skills'], cv['interests'], cv['pathed'], *cv['roles']]:
            self.assertEqual(len(section['summary']), 3)
        self.assertEqual(output.count('class="cv-card"'), 6)
        self.assertEqual(output.count('<details class="cv-detail">'), 10)
        self.assertNotIn('<details class="cv-detail" open', output)
        self.assertIn('8 June 2026', output)
        self.assertIn('Head of Pre Sales and CSM', output)
        self.assertIn('£48k to £150k', output)
        self.assertIn('over 500 members', output)
        self.assertNotIn('Full role description still to confirm', output)
        self.assertIn('£100,000', output)
        self.assertIn('Keltbray', output)
        self.assertIn('src="/cv.js"', output)
        self.assertEqual(api.summary(), [])

    def test_cv_does_not_publish_private_documents_or_contact_details(self):
        output = review.render('/about-me')
        for private in ['14 BROMLEY', 'BD18', '07985', '£62,000', 'passport',
                        'lukecraven36@gmail.com', 'People@', 'Contract of Employment']:
            self.assertNotIn(private, output)

if __name__ == '__main__': unittest.main()
