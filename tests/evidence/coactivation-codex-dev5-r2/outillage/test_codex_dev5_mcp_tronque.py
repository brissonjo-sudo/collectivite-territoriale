"""Réception MCP tronquée : liaison exacte, aucune reconstruction du JSON."""
import unittest
from unittest.mock import patch
import controler_codex_dev5_r2_mcp_tronque as mcp

class McpTruncationTests(unittest.TestCase):
    def setUp(self):
        self.old_captures = dict(mcp.CAPTURES)
        self.old_text = dict(mcp.BY_TEXT)
        mcp.CAPTURES.clear(); mcp.BY_TEXT.clear()

    def tearDown(self):
        mcp.CAPTURES.clear(); mcp.CAPTURES.update(self.old_captures)
        mcp.BY_TEXT.clear(); mcp.BY_TEXT.update(self.old_text)

    def fixture(self):
        body = 'Warning: truncated output (original token count: 27195)\n{"broken":'
        capture = {'call_id': 'real', 'native_tool': 'mcp__droit_francais__get_decision',
                   'result_timestamp': '2026-10-07T18:00:00Z', 'native_truncation_marker': mcp.marker(body).group(0).rstrip('\n')}
        mcp.CAPTURES['real'] = capture
        mcp.BY_TEXT[body] = mcp.TruncatedNativePayload('real')
        return body

    def test_marker_strict_prefix(self):
        self.assertIsNotNone(mcp.marker('Warning: truncated output (original token count: 1)\nJSON'))
        for text in ('prefix Warning: truncated output (original token count: 1)\n',
                     'Warning: truncated output (original token count: 0)\n',
                     'Warning: truncated output (original token count: -1)\n',
                     'Warning: truncated output (original token count: many)\n',
                     'Warning: truncated output (original token count: 1) injected\n'):
            self.assertIsNone(mcp.marker(text))

    def test_registered_payload_not_parsed(self):
        body = self.fixture()
        with patch.object(mcp, 'BASE_SINGLE', side_effect=AssertionError('JSON parser must not run')):
            result = mcp.single_result(['Script completed\n', body])
        self.assertIsInstance(result, mcp.TruncatedNativePayload)

    def test_unregistered_payload_not_accepted(self):
        body = self.fixture()
        with self.assertRaises(ValueError):
            mcp.single_result(['Script completed\n', body + ' changed'])

    def test_failed_transport_not_accepted(self):
        body = self.fixture()
        with self.assertRaises(ValueError):
            mcp.single_result(['Script running\n', body])

    def test_no_document_or_provider_error_inference(self):
        body = self.fixture()
        result = mcp.evidence(mcp.BY_TEXT[body], tool='mcp__droit-francais__get_decision', call_id='real', retrieved_at='2026-10-07T18:00:00Z')
        self.assertEqual(result['status'], 'missing')
        self.assertEqual(result['documents'], [])
        self.assertTrue(result['native_transport_succeeded'])
        self.assertFalse(result['json_payload_parsed'])
        self.assertFalse(result['source_provider_error_verified'])

    def test_fabricated_identity_tool_or_timestamp_rejected(self):
        body = self.fixture()
        for tool, call_id, timestamp in (('mcp__droit-francais__get_article', 'real', '2026-10-07T18:00:00Z'),
                                         ('mcp__droit-francais__get_decision', 'fake', '2026-10-07T18:00:00Z'),
                                         ('mcp__droit-francais__get_decision', 'real', '2026-10-07T17:00:00Z')):
            with self.assertRaises(ValueError):
                mcp.evidence(mcp.BY_TEXT[body], tool=tool, call_id=call_id, retrieved_at=timestamp)

if __name__ == '__main__':
    unittest.main()
