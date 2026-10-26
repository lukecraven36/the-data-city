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
        self.assertIn('href="/interview" data-review-feature="interview" aria-current="page"', document)
        self.assertIn('href="/interview.css"', document)
        self.assertNotIn('src="/interview.js"', document)
        self.assertIn('href="/"', document)
        self.assertIn('href="/role-at-data-city"', document)
        self.assertEqual(len(build_site.site.PAGES), 4)

    def test_briefing_follows_requested_order_and_cites_public_sources(self):
        document = interview_view.render()
        self.assertLess(document.index('id="company"'), document.index('id="developments"'))
        self.assertLess(document.index('id="developments"'), document.index('id="my-role"'))
        self.assertEqual(document.count('class="leader-card'), 6)
        for _, name, title in interview_view.LEADERS:
            self.assertIn(name, document)
            self.assertIn(title, document)
        for text in ['2017', 'Open Innovations', 'Companies House', 'Standard Industrial Classification', 'Real-Time SIC', 'Real-Time Industrial Classification', 'Monthly maintenance', 'Oxford Economics', '2027/28', '26 OCTOBER 2026', 'MY INTERPRETATION', 'responsibilities and priorities to agree', 'human review']:
            self.assertIn(text, document)
        for url, _ in interview_view.SOURCES.values():
            self.assertIn(url, document)
            self.assertTrue(url.startswith('https://thedatacity.com/'))
        for text in ['interview-hero', 'lasting customer value', 'Keltbray', 'Natalia', 'access_token', '@', 'private email']:
            self.assertNotIn(text, document)
        self.assertIn('<details class="interview-prompts">', document)

    def test_both_hosting_prefixes_export_assets_and_links(self):
        for prefix in ['', '/the-data-city/']:
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as folder, patch.object(build_site, 'OUT', Path(folder) / 'dist'):
                build_site.build(prefix, email_gate=True)
                document = (build_site.OUT / 'interview/index.html').read_text(encoding='utf-8')
                base = prefix.rstrip('/')
                for target in ['/interview.css', '/review-access.js', '/role-at-data-city']:
                    self.assertIn(f'"{base}{target}"', document)
                self.assertIn('id="review-entry"', document)
                for asset in ['interview.css']:
                    self.assertEqual((build_site.OUT / asset).read_text(encoding='utf-8'), (Path('static') / asset).read_text(encoding='utf-8'))
                for old in ['ai-lead', 'commercial-product-lead']:
                    redirect = (build_site.OUT / old / 'index.html').read_text()
                    self.assertIn(f'url={base}/role-at-data-city/', redirect)


if __name__ == '__main__':
    unittest.main()
