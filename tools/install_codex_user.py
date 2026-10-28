#!/usr/bin/env python3
"""Install the studio router and specialist roles into a Codex user directory.

Requires Python 3.11+ and PyYAML. Existing files are never overwritten.
"""
import argparse
import json
import os
import re
import stat
import sys
import tomllib
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit('Install PyYAML first: python -m pip install PyYAML') from exc

SOURCE = Path(__file__).resolve().parents[1]
NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

def check_path(path):
    for component in (path, *path.parents):
        if component.exists():
            info = component.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError(f'Link or reparse point in target path: {component}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'), help='Codex user directory')
    parser.add_argument('--apply', action='store_true', help='Create the installation; otherwise preview it')
    args = parser.parse_args()
    target = args.target.absolute()
    snapshot = target / 'game-studios' / 'codex-game-studios'
    skill = target / 'skills' / 'game-studio'
    agents = target / 'agents'
    claude = SOURCE / '.claude'
    roles = sorted((claude / 'agents').glob('*.md'))
    workflows = list((claude / 'skills').glob('*/SKILL.md'))
    if len(roles) != 49 or len(workflows) != 72:
        raise ValueError('Unexpected source catalog: expected 49 roles and 72 workflows')
    files = {}
    for path in claude.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Source links are not supported: {path}')
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            files[snapshot / '.claude' / path.relative_to(claude)] = path.read_bytes()
    files[snapshot / 'LICENSE'] = (SOURCE / 'LICENSE').read_bytes()
    template = SOURCE / 'tools' / 'codex-global' / 'game-studio'
    for path in template.rglob('*'):
        if path.is_file():
            files[skill / path.relative_to(template)] = path.read_bytes()
    for role in roles:
        if not NAME.fullmatch(role.stem):
            raise ValueError(f'Invalid role name: {role.stem}')
        _, frontmatter, _ = role.read_text(encoding='utf-8').split('---', 2)
        metadata = yaml.safe_load(frontmatter)
        if metadata.get('name') != role.stem or not isinstance(metadata.get('description'), str):
            raise ValueError(f'Invalid role metadata: {role}')
        name = 'gs_' + role.stem.replace('-', '_')
        source = (snapshot / '.claude' / 'agents' / role.name).as_posix()
        instruction = (f'You are the Codex Game Studios {role.stem} specialist. Read {source} at task start and use its relevant domain guidance. '
            'The reference snapshot is not the working project. Follow higher-priority instructions, the user request, and the target project AGENTS.md and frozen specifications. '
            'Translate Claude-specific tools and paths to available Codex capabilities. Do not impose blanket approval for already authorized work. '
            'Preserve project rules and save semantics unless changes are explicitly approved. Report evidence, completed work and limitations accurately.')
        content = ''.join(f'{key} = {json.dumps(value, ensure_ascii=False)}\n' for key, value in [('name', name), ('description', metadata['description']), ('developer_instructions', instruction)])
        if tomllib.loads(content)['name'] != name:
            raise ValueError(f'Invalid TOML for {role}')
        files[agents / (name + '.toml')] = content.encode('utf-8')
    check_path(target)
    for root in (snapshot, skill):
        if root.exists():
            raise FileExistsError(f'Refusing to merge into existing directory: {root}')
    for path in files:
        check_path(path)
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite: {path}')
    print(json.dumps({'target': str(target), 'workflows': len(workflows), 'roles': len(roles), 'files': len(files), 'apply': args.apply}))
    if not args.apply:
        return
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(content)
        if path.read_bytes() != content:
            raise IOError(f'Write verification failed: {path}')

if __name__ == '__main__':
    if sys.version_info < (3, 11):
        raise SystemExit('Python 3.11 or later is required')
    main()
