#!/usr/bin/env python3
"""Setup for a new user, and after each update. Works on macOS, Linux and Windows.

Copies templates/ to local/ (personal state, git-ignored). If local/ exists, it adds only the
template files that are missing and never overwrites a file. Then it makes the work/ folders
that workspace.yaml lists, and builds the indexes and the boot card.

Usage: python3 core/scripts/setup.py   (Windows: py -3 core/scripts/setup.py)
"""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, pack_dirs, parse_yaml, workspace  # noqa: E402
import build_boot_card  # noqa: E402
import build_indexes  # noqa: E402


def copy_templates() -> None:
    templates, local = ROOT / 'templates', ROOT / 'local'
    if local.exists():
        print('local/ exists. Setup adds missing template files only and overwrites nothing.')
    added = 0
    for src in sorted(p for p in templates.rglob('*') if p.is_file() and p.name != '.gitkeep'):
        rel = src.relative_to(templates)
        dest = local / rel
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            print(f'added: local/{rel.as_posix()}')
            added += 1
    print(f'Added {added} missing template file(s).')


def make_work_folders() -> None:
    ws = workspace()
    base = ws.get('work_root') or 'work'
    names: list[str] = []
    if str(ws.get('pack_work_folders')).lower() == 'true':
        for p in pack_dirs():
            names += parse_yaml((p / 'pack.yaml').read_text(encoding='utf-8')).get('work_folders') or []
    names = names or list(ws.get('work_folders') or [])  # the pack set replaces the generic set
    seen = set()
    for name in names:
        if name.lower() in seen:  # macOS and Windows file systems ignore case
            continue
        seen.add(name.lower())
        d = ROOT / base / name
        d.mkdir(parents=True, exist_ok=True)
        print(f'work folder: {d.relative_to(ROOT).as_posix()}')


def main() -> int:
    copy_templates()
    make_work_folders()
    for mod in (build_indexes, build_boot_card):
        sys.argv = [mod.__file__, '--write']
        if mod.main():
            return 1
    print('Setup done. Next: fill in local/settings/owner.md, then run python3 core/scripts/validate.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
