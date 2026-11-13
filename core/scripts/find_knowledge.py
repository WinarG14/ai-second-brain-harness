#!/usr/bin/env python3
"""Find a knowledge item again (design section 6, step 5).

Search order: frontmatter titles and pack triggers first, then file bodies. Each hit shows
the path, title, status, valid_from and source, so the agent can judge if the item is current.

Usage: python3 core/scripts/find_knowledge.py <words> [--pack <name>] [--all-packs] [--limit N]
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ROOT, frontmatter, pack_dirs, pack_files  # noqa: E402


def candidates(pack: str | None, all_packs: bool) -> list[Path]:
    files = sorted((ROOT / 'core/policy').glob('*.md')) + sorted((ROOT / 'core/recipes').glob('*.md'))
    files += sorted((ROOT / 'core/skills').glob('*/SKILL.md'))
    for p in pack_dirs(active_only=not all_packs):
        if pack is None or p.name == pack:
            files += pack_files(p)
    files += sorted((ROOT / 'local/memory').glob('*.md'))
    return [f for f in files if pack is None or f'packs/{pack}/' in f.as_posix()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('words', nargs='+')
    ap.add_argument('--pack')
    ap.add_argument('--all-packs', action='store_true')
    ap.add_argument('--limit', type=int, default=10)
    a = ap.parse_args()
    words = [w.lower() for w in a.words]
    hits = []
    for f in candidates(a.pack, a.all_packs):
        fm = frontmatter(f) or {}
        title = str(fm.get('title') or fm.get('name') or f.stem)
        head = f'{title} {fm.get("trigger", "")} {f.stem}'.lower()
        body = f.read_text(encoding='utf-8').lower()
        t = sum(w in head for w in words)
        b = sum(w in body for w in words)
        if t or b:
            hits.append((t * 10 + b, 'title' if t else 'body', f, title, fm))
    hits.sort(key=lambda h: (-h[0], str(h[2])))
    if not hits:
        print('No match. Ask the user one question, or try other words.')
        return 1
    for score, where, f, title, fm in hits[:a.limit]:
        print(f"[{where}] {f.relative_to(ROOT)}\n    title: {title} | status: {fm.get('status', '?')} | "
              f"valid_from: {fm.get('valid_from', '?')} | source: {fm.get('source', '?')}"
              + (f" | needs: {fm['requires_external']}" if fm.get('requires_external') else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
