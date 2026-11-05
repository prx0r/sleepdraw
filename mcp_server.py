"""Sleepdraw MCP server — the etch renderer as an agent-callable seam.

Stdio JSON-RPC ({jsonrpc, id, method, params}) + CLI mode:
  python3 mcp_server.py seal_prompt '{"text": "...", "chapter": "tantrasara-20"}'

Tools: presets, seal_prompt, render_seal. Pure except render_seal, which
spends real Bailian money and refuses without explicit confirm_paid:true.
Every ship carries a recipe; every seal names its preset SHA (the hermetic
part: art is reproducible from prompt + preset + env, or it is not sealed).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRESETS = ('lora1', 'lora2', 'lora2-inv', 'lora3')
SEAL_PRESET = 'lora2-inv'


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def presets():
    """Locked house looks with SHAs. New look = new file, never silent drift."""
    out = []
    for name in PRESETS:
        p = ROOT / f'{name}.yaml'
        if p.is_file():
            out.append({'preset': name, 'sha256': _sha(p), 'path': str(p)})
    return {'presets': out, 'law': 'lora1/lora2 locked; lora2-inv is the parable inverse (black ink on white, staged bands roots→web→thread→spider-last)'}


def seal_prompt(text: str, chapter: str = ""):
    """Draft a hermetic seal prompt for one narration block (machine-proposed).

    House rules (lora2-inv): one world, end-state freedom (never the
    struggle), black ink on white, dense detail on the subject + breathing
    white space, no text/letters/numbers, staged reveal roots→web→thread→
    subject-last with contemplative breaths. Returns prompt + preset pin;
    the owner/agent disposes, the tool never approves.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError('text is required')
    clean = ' '.join(text.strip().split())
    head = clean[:220].rsplit(' ', 1)[0]
    preset_path = ROOT / f'{SEAL_PRESET}.yaml'
    prompt = (
        f'Black ink sketch on warm white paper, hand-drawn storybook etching: {head}. '
        'The final snapshot — the end-state, freedom rendered, always the arrival. '
        'One world: all elements in a single wide landscape, dense etched detail on the '
        'subject, vast breathing white space everywhere else. Rasa in bands: roots and '
        'web below, horizon and thread across the middle, the living subject last, '
        'breath between bands. All greyscale, luminous accents as densest ink. '
        'No text, no letters, no numbers, no words.'
    )
    return {'prompt': prompt, 'preset': SEAL_PRESET,
            'preset_sha256': _sha(preset_path),
            'chapter': chapter,
            'rules': ['one-world', 'end-state-only', 'no-text', 'subject-last-bands'],
            'status': 'machine-proposed-unreviewed'}


def render_seal(prompt: str, name: str, duration_ms: int = 0,
                confirm_paid: bool = False, no_ship: bool = True,
                preset: str = SEAL_PRESET):
    """Render a seal via cli.py make (SPENDS Bailian money — confirm first).

    confirm_paid must be literally true or the call is refused with the
    estimate path instead. Default no_ship:true (local run dir + recipe,
    nothing uploaded). Returns the cli receipt (mp4, frames, recipe).
    """
    if not confirm_paid:
        return {'refused': True,
                'reason': 'render_seal spends paid Bailian generation budget; '
                          're-run with confirm_paid:true to proceed',
                'estimate': 'qwen-image-3.0 sketch ≈ CNY 0.18 per still (see docs/BAILIAN-STACK.md)'}
    if preset not in PRESETS:
        raise ValueError(f'unknown preset {preset!r}')
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError('prompt is required')
    if not isinstance(name, str) or not name.strip():
        raise ValueError('name is required')
    cmd = [sys.executable, str(ROOT / 'cli.py'), 'make', '--prompt', prompt,
           '--name', name, '--preset', preset, '--dur', str(int(duration_ms or 0))]
    if no_ship:
        cmd.append('--no-ship')
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800,
                           cwd=str(ROOT))
    except subprocess.TimeoutExpired as exc:
        raise ValueError(f'render timed out: {exc}') from exc
    if r.returncode != 0:
        raise ValueError(f'cli make failed: {(r.stderr or r.stdout)[-2000:]}')
    return {'preset': preset, 'preset_sha256': _sha(ROOT / f'{preset}.yaml'),
            'log': (r.stdout or '')[-3000:], 'no_ship': no_ship,
            'status': 'rendered-machine-unreviewed'}


TOOLS = {
    'presets': (presets, 'Locked presets + SHAs.'),
    'seal_prompt': (seal_prompt, 'Draft a hermetic seal prompt (machine-proposed, owner disposes).'),
    'render_seal': (render_seal, 'Render via cli make. REFUSES without confirm_paid:true (paid generation).'),
}


def handle(req):
    """One JSON-RPC request -> response dict (never raises)."""
    try:
        if req.get('jsonrpc') != '2.0' or req.get('method') != 'tools/call':
            if req.get('method') == 'tools/list':
                return {'jsonrpc': '2.0', 'id': req.get('id'),
                        'result': {'tools': [{'name': n, 'description': d}
                                             for n, (f, d) in TOOLS.items()]}}
            return {'jsonrpc': '2.0', 'id': req.get('id'),
                    'error': {'code': -32601, 'message': 'unknown method'}}
        name = (req.get('params') or {}).get('name')
        args = (req.get('params') or {}).get('arguments') or {}
        if name not in TOOLS:
            return {'jsonrpc': '2.0', 'id': req.get('id'),
                    'error': {'code': -32602, 'message': f'unknown tool {name}'}}
        return {'jsonrpc': '2.0', 'id': req.get('id'),
                'result': {'content': [{'type': 'text',
                                        'text': json.dumps(TOOLS[name][0](**args),
                                                           ensure_ascii=False)}]}}
    except Exception as exc:
        return {'jsonrpc': '2.0', 'id': req.get('id'),
                'error': {'code': -32603, 'message': str(exc)[:500]}}


def serve():
    for line in sys.stdin:
        line = line.strip()
        if line:
            sys.stdout.write(json.dumps(handle(json.loads(line))) + '\n')
            sys.stdout.flush()


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] in TOOLS:
        print(json.dumps(TOOLS[sys.argv[1]][0](
            **(json.loads(sys.argv[2]) if len(sys.argv) > 2 else {})),
            ensure_ascii=False))
    elif len(sys.argv) >= 2 and sys.argv[1] == 'serve':
        serve()
    else:
        print('usage: mcp_server.py (serve|presets|seal_prompt|render_seal) [json-args]')
        sys.exit(2)
