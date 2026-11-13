#!/usr/bin/env python3
"""Resolve the external sources that packs need (pack.yaml requires.external).

In pack files, `<key>` (for example `<shared_folder>`) means the path that this script prints
for that key. The paths are per user, in local/settings/external.yaml (git-ignored).

Usage:
  python3 core/scripts/resolve_external.py                 # which files of each active pack need a path
  python3 core/scripts/resolve_external.py shared_folder   # print one path, exit 1 if not usable
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, frontmatter, pack_dirs, pack_files, parse_yaml  # noqa: E402

SETTINGS = ROOT / 'local/settings/external.yaml'


def paths() -> dict[str, Path]:
    if not SETTINGS.is_file():
        return {}
    raw = parse_yaml(SETTINGS.read_text(encoding='utf-8'))
    return {k: Path(str(v)).expanduser() for k, v in raw.items() if v}


def main() -> int:
    known = paths()
    if len(sys.argv) > 1:
        p = known.get(sys.argv[1])
        if p is None or not p.is_dir():
            print(f'{sys.argv[1]}: not set or not a folder in local/settings/external.yaml', file=sys.stderr)
            return 1
        print(p)
        return 0
    for pack in pack_dirs():
        need = [f for f in pack_files(pack) if (frontmatter(f) or {}).get('requires_external')]
        keys = sorted({str(frontmatter(f)['requires_external']) for f in need})
        missing = [k for k in keys if k not in known or not known[k].is_dir()]
        if not need:
            print(f'{pack.name}: ready (needs nothing external)')
        elif not missing:
            print(f'{pack.name}: ready ({len(need)} files use {", ".join(keys)}, path is set)')
        else:
            print(f'{pack.name}: ready, except {len(need)} files that need {", ".join(missing)}:')
            for f in need:
                print(f'    {f.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
