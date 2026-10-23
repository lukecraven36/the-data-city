from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_site
import interview_view


class InterviewPage(unittest.TestCase):
    def test_route_is_featured_and_offline(self):
        with patch.object(build_site.site.api, 'request', side_effect=AssertionError('No API requests')):
            document = build_site.site.render('/interview')
        self.assertEqual(build_site.site.NAV[0], ('/interview', 'Interview'))
        self.assertIn('href="/interview" aria-current="page"', document)
        self.assertIn('href="/interview.css"', document)
        self.assertIn('src="/interview.js"', document)
        self.assertIn('href="/"', document)
        self.assertIn('href="/role-at-data-city"', document)
        self.assertEqual(len(build_site.site.PAGES), 4)

    def test_journey_is_complete_without_javascript(self):
        document = interview_view.render()
        self.assertEqual(document.count('class="journey-stage"'), 5)
        self.assertEqual(document.count('class="handoff-panel"'), 5)
        for key, name, *_ in interview_view.STAGES:
            self.assertIn(f'aria-controls="handoff-{key}"', document)
            self.assertIn(f'aria-labelledby="stage-{key}"', document)
            self.assertIn(name, document)
        for text in ['Independent proposal for discussion', 'prepared sample', 'illustrative financials', 'subject to validating', 'Baseline first.', 'Attract + Explore', 'Product', 'human review']:
            self.assertIn(text, document)
        for text in ['Keltbray', 'Simpson', 'Natalia', '£100,000', 'access_token', '@', 'conversion problems', 'broken operations', 'private email']:
            self.assertNotIn(text, document)

    def test_both_hosting_prefixes_export_assets_and_links(self):
        for prefix in ['', '/the-data-city/']:
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as folder, patch.object(build_site, 'OUT', Path(folder) / 'dist'):
                build_site.build(prefix, email_gate=True)
                document = (build_site.OUT / 'interview/index.html').read_text(encoding='utf-8')
                base = prefix.rstrip('/')
                for target in ['/interview.css', '/interview.js', '/review-access.js', '/role-at-data-city']:
                    self.assertIn(f'"{base}{target}"', document)
                self.assertIn('id="review-entry"', document)
                for asset in ['interview.css', 'interview.js']:
                    self.assertEqual((build_site.OUT / asset).read_text(encoding='utf-8'), (Path('static') / asset).read_text(encoding='utf-8'))
                for old in ['ai-lead', 'commercial-product-lead']:
                    redirect = (build_site.OUT / old / 'index.html').read_text()
                    self.assertIn(f'url={base}/role-at-data-city/', redirect)


if __name__ == '__main__':
    unittest.main()
