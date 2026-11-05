#!/usr/bin/env python3
"""MCP tests — pure paths only. No Bailian calls, no spending, ever."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import mcp_server as M


def run_rpc(payload):
    p = subprocess.run([sys.executable, str(ROOT / 'mcp_server.py'), 'serve'],
                       input=json.dumps(payload), text=True, capture_output=True)
    assert p.returncode == 0, p.stderr
    return json.loads(p.stdout)


class McpTests(unittest.TestCase):
    def test_presets_match_files_on_disk(self):
        got = M.presets()
        self.assertGreaterEqual(len(got['presets']), 4)
        for entry in got['presets']:
            raw = (ROOT / f"{entry['preset']}.yaml").read_bytes()
            self.assertEqual(entry['sha256'], hashlib.sha256(raw).hexdigest())

    def test_seal_prompt_is_hermetic_and_textless(self):
        r = M.seal_prompt('The infinite has somehow started experiencing itself as finite.',
                          chapter='tantrasara-20')
        self.assertEqual(r['preset'], 'lora2-inv')
        self.assertEqual(r['status'], 'machine-proposed-unreviewed')
        self.assertIn('No text', r['prompt'])
        self.assertIn(r['preset_sha256'],
                      [p['sha256'] for p in M.presets()['presets']])

    def test_render_refuses_without_confirm_paid(self):
        r = M.render_seal(prompt='x', name='x')
        self.assertTrue(r.get('refused'))
        r2 = M.render_seal(prompt='x', name='x', confirm_paid=False)
        self.assertTrue(r2.get('refused'))

    def test_rpc_lists_tools_and_rejects_unknown(self):
        tools = run_rpc({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'})
        names = [t['name'] for t in tools['result']['tools']]
        self.assertIn('seal_prompt', names)
        self.assertIn('render_seal', names)
        bad = run_rpc({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
                       'params': {'name': 'nope', 'arguments': {}}})
        self.assertIn('error', bad)

    def test_rpc_seal_prompt_round_trip(self):
        r = run_rpc({'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call',
                     'params': {'name': 'seal_prompt',
                                'arguments': {'text': 'A garland of fifty names.'}}})
        body = json.loads(r['result']['content'][0]['text'])
        self.assertEqual(body['preset'], 'lora2-inv')


if __name__ == '__main__':
    unittest.main()
