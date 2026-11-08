#!/usr/bin/env python3
"""Build core/boot_card.md from core/boot_card.template.md, the active packs and their recipes.

Adapted from the SC harness build_boot_card.py. The source of the recipe table is now the
frontmatter of `core/recipes/*.recipe.md` and `packs/<active pack>/recipes/*.recipe.md`.

Usage:
  python3 core/scripts/build_boot_card.py            # print the card
  python3 core/scripts/build_boot_card.py --write    # write it
  python3 core/scripts/build_boot_card.py --check    # exit 1 if out of date or over budget
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, frontmatter, pack_dirs, pack_files, parse_yaml  # noqa: E402

CARD, TEMPLATE = ROOT / 'core/boot_card.md', ROOT / 'core/boot_card.template.md'
MAX_LINES, MAX_BYTES, TRIGGER_CHARS = 50, 4000, 52


def short(text: str) -> str:
    t = re.sub(r'\s+', ' ', str(text).replace('|', '/')).strip()
    return t if len(t) <= TRIGGER_CHARS else t[:TRIGGER_CHARS].rsplit(' ', 1)[0].rstrip(',;:/') + ' …'


def pack_state(pack: Path) -> str:
    """Static count of files that need an external path. The card is committed, so it must not
    read git-ignored local/ state."""
    n = sum(1 for f in pack_files(pack) if (frontmatter(f) or {}).get('requires_external'))
    return f"{n} files need shared_folder" if n else 'standalone'


def recipes() -> list[tuple[str, str, str]]:
    files = sorted((ROOT / 'core/recipes').glob('*.recipe.md'))
    for p in pack_dirs():
        files += sorted((p / 'recipes').glob('*.recipe.md'))
    rows = []
    for f in files:
        fm = frontmatter(f) or {}
        if fm.get('status') in ('superseded', 'archived'):
            continue
        rows.append((short(fm.get('trigger') or fm.get('title') or f.stem),
                     f.relative_to(ROOT).as_posix(), str(fm.get('status', '?'))))
    return rows


def render() -> str:
    packs = [f"- `{p.name}`: {short(parse_yaml((p / 'pack.yaml').read_text(encoding='utf-8')).get('scope', ''))} ({pack_state(p)})"
             for p in pack_dirs()] or ['- (no active packs)']
    rows = recipes()
    table = ['| Trigger | Recipe | Status |', '|---|---|---|'] + [f"| {t} | `{f.removeprefix('packs/')}` | {s} |" for t, f, s in rows]
    if not rows:
        table.append('| (no recipes yet) | | |')
    return (TEMPLATE.read_text(encoding='utf-8')
            .replace('{{packs}}', '\n'.join(packs)).replace('{{recipes}}', '\n'.join(table)))


def check() -> list[str]:
    new = render()
    errs = []
    if not CARD.is_file() or CARD.read_text(encoding='utf-8') != new:
        errs.append('core/boot_card.md is out of date; run python3 core/scripts/build_boot_card.py --write')
    lines, size = new.count('\n') + 1, len(new.encode())
    if lines > MAX_LINES or size > MAX_BYTES:
        errs.append(f'Boot card over budget: {lines} lines / {size} bytes (max {MAX_LINES} / {MAX_BYTES})')
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    if a.check:
        errs = check()
        print('\n'.join(errs) or 'PASS: boot card is up to date and in budget')
        return 1 if errs else 0
    new = render()
    lines, size = new.count('\n') + 1, len(new.encode())
    if lines > MAX_LINES or size > MAX_BYTES:
        print(f'Refused: card would be {lines} lines / {size} bytes (max {MAX_LINES} / {MAX_BYTES})')
        return 1
    if a.write:
        CARD.write_text(new, encoding='utf-8')
        print(f'Wrote core/boot_card.md: {len(recipes())} recipes, {lines} lines, {size} bytes')
    else:
        print(new)
    return 0


if __name__ == '__main__':
    sys.exit(main())
