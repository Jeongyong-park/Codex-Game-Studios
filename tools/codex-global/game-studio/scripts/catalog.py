#!/usr/bin/env python3
"""Resolve installed Game Studios workflows and roles."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / 'game-studios' / 'codex-game-studios'
NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

def catalog(kind):
    if kind == 'workflow':
        return {p.parent.name: p for p in sorted((ROOT / '.claude' / 'skills').glob('*/SKILL.md'))}
    return {p.stem: p for p in sorted((ROOT / '.claude' / 'agents').glob('*.md'))}

def main(argv):
    if argv == ['list']:
        data = {kind + 's': list(catalog(kind)) for kind in ('workflow', 'role')}
        data['counts'] = {key: len(value) for key, value in data.items()}
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    if len(argv) != 2 or argv[0] not in ('workflow', 'role') or not NAME.fullmatch(argv[1]):
        print('Usage: catalog.py list | workflow NAME | role NAME', file=sys.stderr)
        return 2
    kind, name = argv
    entry = catalog(kind).get(name)
    if entry is None:
        print(f'Unknown {kind}: {name}', file=sys.stderr)
        return 1
    result = {'kind': kind, 'name': name, 'source': str(entry), 'snapshot': str(ROOT)}
    if kind == 'role':
        result['codex_agent'] = 'gs_' + name.replace('-', '_')
    print(json.dumps(result, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
