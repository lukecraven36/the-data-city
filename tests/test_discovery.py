import html
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import discovery_view


class Discovery(unittest.TestCase):
    def test_demo_layer_preserves_researched_values_and_complete_sample(self):
        root = discovery_view.ROOT
        researched = json.loads((root / 'data/technology-discovery-enriched.json').read_text(encoding='utf-8'))
        before = (root / 'data/technology-discovery-enriched.json').read_bytes()
        preview = discovery_view.payload()
        self.assertEqual({c['company_number'] for c in researched['companies']}, {c['id'] for c in preview['companies']})
        self.assertEqual(len(preview['companies']), 10)
        lookup = {c['company_number']: c for c in researched['companies']}
        for company in preview['companies']:
            actual = lookup[company['id']]
            self.assertEqual(company['employees'], actual['metrics']['average_employees']['value'])
            self.assertEqual(company['netAssets'], actual['metrics']['net_assets_gbp']['value'])
            self.assertEqual(company['metricProvenance']['funding'], 'illustrative')
            self.assertIsNone(actual['public_funding']['total_gbp'])
        reported = next(c for c in preview['companies'] if c['id'] == '15474498')
        self.assertEqual(reported['turnover'], 2000)
        self.assertEqual(reported['metricProvenance']['turnover'], 'filed')
        self.assertEqual((root / 'data/technology-discovery-enriched.json').read_bytes(), before)

    def test_embedded_company_data_cannot_break_out_of_template(self):
        malicious = {'companies': [{'name': '</template><script>alert(1)</script>'}]}
        with patch.object(discovery_view, 'payload', return_value=malicious):
            output = discovery_view.render()
        self.assertNotIn('</template><script>', output)
        self.assertIn('&lt;/template&gt;&lt;script&gt;', output)

    def test_journey_uses_authorised_contact_defaults_without_submission_target(self):
        output = discovery_view.render()
        for value in ['Luke', 'Craven', 'luke@pathedconsulting.co.uk', '07985 606824', 'AI specialist', 'Pathed Consulting', 'Local Government']:
            self.assertIn(value, output)
        self.assertNotIn(' action=', output)
        self.assertEqual(output.count('<textarea '), 3)
        self.assertIn('Nothing is sent to The Data City', output)
        self.assertIn('No enquiry has been sent', output)
        self.assertIn('Prepared demonstration sequence', output)


if __name__ == '__main__':
    unittest.main()
