import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_site
import review_gate


class ReviewExport(unittest.TestCase):
    def test_project_path_export_keeps_all_pages_behind_entry_ui(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(build_site, 'OUT', Path(folder) / 'dist'):
            build_site.build('/the-data-city/', email_gate=True)
            out = build_site.OUT
            for route in ['index.html', 'about-me/index.html', 'role-at-data-city/index.html', 'interview/index.html']:
                document = (out / route).read_text(encoding='utf-8')
                self.assertIn('class="review-required"', document)
                self.assertIn('id="review-entry"', document)
                self.assertIn('src="/the-data-city/review-access.js"', document)
                self.assertNotIn('href="/about-me', document)
                self.assertNotIn('src="/discovery.js', document)
                self.assertNotIn('ryanatwilds@gmail.com', document)
            redirect = (out / 'ai-lead/index.html').read_text(encoding='utf-8')
            self.assertIn('url=/the-data-city/role-at-data-city/', redirect)
            self.assertFalse((out / '.private').exists())
            self.assertFalse((out / 'data/review-access.json').exists())
        with self.assertRaises(ValueError):
            build_site.build('/../../outside')

    def test_allowlist_is_validated_and_revision_changes_when_access_changes(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(review_gate, 'ROOT', Path(folder)):
            target = Path(folder) / 'data/review-access.json'
            target.parent.mkdir()
            digest = hashlib.sha256(b'person@example.com').hexdigest()
            target.write_text(json.dumps({'allowed_email_hashes': [digest]}))
            first = review_gate.configuration()
            target.write_text(json.dumps({'allowed_email_hashes': [hashlib.sha256(b'other@example.com').hexdigest()]}))
            self.assertNotEqual(first['storageKey'], review_gate.configuration()['storageKey'])
            target.write_text(json.dumps({'allowed_email_hashes': []}))
            with self.assertRaises(ValueError):
                review_gate.configuration()

    def test_profile_metadata_cannot_add_an_unapproved_viewer(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(review_gate, 'ROOT', Path(folder)):
            target = Path(folder) / 'data/review-access.json'
            target.parent.mkdir()
            allowed = hashlib.sha256(b'allowed@example.com').hexdigest()
            other = hashlib.sha256(b'other@example.com').hexdigest()
            profile = dict(firstName='Test', surname='Reviewer', jobTitle='Director', organisation='Example', phone='0333 335 5665', industry='Local Government')
            target.write_text(json.dumps({'allowed_email_hashes': [allowed], 'review_profiles': {other: profile}}))
            with self.assertRaises(ValueError):
                review_gate.configuration()
            target.write_text(json.dumps({'allowed_email_hashes': [allowed], 'review_profiles': {allowed: profile}}))
            self.assertEqual(review_gate.configuration()['reviewProfiles'][allowed], profile)


if __name__ == '__main__':
    unittest.main()
