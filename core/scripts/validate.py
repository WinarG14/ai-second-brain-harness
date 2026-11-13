#!/usr/bin/env python3
"""Validate the repository against design section 5.2. Exit 1 on any FAIL.

Rules:
  1. Each knowledge file has frontmatter with type, pack, source and status (valid values).
  2. Each file is in its pack INDEX.md and each index row points to a file (generated indexes,
     merged registries, skill pointers and the boot card are up to date).
  3. No two active files in one pack have the same title.
  4. No personal data in tracked areas (built-in patterns + local/settings/privacy_patterns.txt).
  5. A superseded file has superseded_by, and that path exists.
Also: workspace.yaml and pack.yaml have their required keys.

Usage: python3 core/scripts/validate.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FOLDER_TYPE, REQUIRED, ROOT, STATUSES, TYPES, frontmatter, pack_files,  # noqa: E402
                     parse_yaml, workspace)
import build_boot_card  # noqa: E402
import build_indexes  # noqa: E402

TOP_SKIP = {'.git', 'local', 'work'}  # git-ignored or git-internal, only at the repo root
ANY_SKIP = {'__pycache__', 'node_modules', '.git'}
ALLOWED_EMAIL = re.compile(r'@(example\.(com|org|net)|anthropic\.com)$', re.I)
BUILTIN = [
    ('home path', re.compile(r'/(?:Users|home)/(?!<)[A-Za-z0-9._-]+')),
    ('email', re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')),
    ('token', re.compile(r'\b(?:glpat-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|xox[abp]-[A-Za-z0-9-]{10,})')),
]


def private_patterns() -> list[tuple[str, re.Pattern]]:
    f = ROOT / 'local/settings/privacy_patterns.txt'
    if not f.is_file():
        return []
    lines = [x.strip() for x in f.read_text(encoding='utf-8-sig').splitlines()]
    return [('private pattern', re.compile(x, re.I)) for x in lines if x and not x.startswith('#')]


def tracked_files():
    for f in ROOT.rglob('*'):
        parts = f.relative_to(ROOT).parts
        if f.is_file() and parts[0] not in TOP_SKIP and not ANY_SKIP & set(parts):
            yield f


def scan_personal() -> list[str]:
    hits = []
    pats = BUILTIN + private_patterns()
    for f in tracked_files():
        try:
            text = f.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for label, pat in pats:
                for m in pat.finditer(line):
                    if label == 'email' and ALLOWED_EMAIL.search(m.group(0)):
                        continue
                    hits.append(f'{f.relative_to(ROOT)}:{n}: {label}')
    return hits


def check_files(pack: str, files: list[Path]) -> list[str]:
    """Rules 1, 3 and 5 for one pack (or `core`), plus type against folder."""
    fails: list[str] = []
    titles: dict[str, Path] = {}
    for f in files:
        rel = f.relative_to(ROOT)
        fm = frontmatter(f)
        if fm is None:  # rule 1
            fails.append(f'{rel}: no frontmatter'); continue
        for k in REQUIRED:
            if not fm.get(k):
                fails.append(f'{rel}: frontmatter has no {k}')
        if fm.get('type') and fm['type'] not in TYPES:
            fails.append(f"{rel}: type {fm['type']} is not one of {', '.join(TYPES)}")
        if fm.get('status') and fm['status'] not in STATUSES:
            fails.append(f"{rel}: status {fm['status']} is not one of {', '.join(STATUSES)}")
        if fm.get('pack') and fm['pack'] != pack:
            fails.append(f"{rel}: pack is {fm['pack']}, but the file is in {pack}")
        title = str(fm.get('title') or fm.get('name') or f.stem).strip().lower()
        if fm.get('status') == 'active':  # rule 3
            if title in titles:
                fails.append(f'{rel}: same active title as {titles[title].relative_to(ROOT)}')
            titles[title] = f
        if fm.get('status') == 'superseded':  # rule 5
            target = fm.get('superseded_by')
            if not target:
                fails.append(f'{rel}: superseded but no superseded_by')
            elif not (ROOT / str(target)).exists():
                fails.append(f'{rel}: superseded_by {target} does not exist')
        folder = rel.parts[-3] if f.name == 'SKILL.md' else rel.parts[-2]
        if folder in FOLDER_TYPE and fm.get('type') and fm['type'] != FOLDER_TYPE[folder]:
            fails.append(f"{rel}: type {fm['type']} does not match folder {folder}/")
    return fails


def core_files() -> list[Path]:
    return sorted((ROOT / 'core/recipes').glob('*.md')) + sorted((ROOT / 'core/skills').glob('*/SKILL.md'))


def orphans(pack: Path) -> list[str]:
    """Markdown files in a pack that are not knowledge files, so they would not be indexed."""
    known = set(pack_files(pack)) | {pack / 'INDEX.md'}
    out = []
    for f in pack.rglob('*.md'):  # skills/ support files are not knowledge files
        top = f.relative_to(pack).parts[0]
        if f in known or top in ('registry_rows', 'evals', '_archive') or top == 'skills':
            continue
        out.append(f'{f.relative_to(ROOT)}: not in a knowledge folder, so it is not indexed (move it to processes/, knowledge/ or recipes/)')
    return out


def external_tokens(pack: Path, meta: dict) -> list[str]:
    """Rule 6: shared folder paths use the `<key>` token, and the pack declares the key."""
    need = set((meta.get('requires') or {}).get('external') or [])
    out = []
    for f in sorted(pack.rglob('*')):
        if not f.is_file() or f.suffix not in ('.md', '.yaml'):
            continue
        text = f.read_text(encoding='utf-8', errors='ignore')
        rel = f.relative_to(ROOT)
        if '../../../' in text:
            out.append(f'{rel}: use <shared_folder>/... instead of ../../../')
        for key in sorted(set(re.findall(r'<(shared_folder)>', text)) - need):
            out.append(f'{rel}: uses <{key}> but {pack.name}/pack.yaml requires.external lacks {key}')
        fm = frontmatter(f) if f.suffix == '.md' else None
        if fm is not None and '<shared_folder>' in text and fm.get('requires_external') != 'shared_folder':
            out.append(f'{rel}: uses <shared_folder>; add requires_external: shared_folder to its frontmatter')
    return out


def core_standalone() -> list[str]:
    """The core must work with no external source."""
    out = []
    for f in sorted((ROOT / 'core').rglob('*.md')):
        if f.name in ('router.md', 'where_to_look.md', 'boot_card.md', 'boot_card.template.md'):
            continue
        text = f.read_text(encoding='utf-8', errors='ignore')
        if re.search(r'<shared_folder>|\.\./\.\./\.\./|requires_external:', text):
            out.append(f'{f.relative_to(ROOT)}: core files must not need the shared folder')
    return out


def main() -> int:
    fails: list[str] = []
    ws = workspace()
    for k in ('active_packs', 'work_folders'):
        if k not in ws:
            fails.append(f'workspace.yaml: missing {k}')
    for name in ws.get('active_packs') or []:
        if not (ROOT / 'packs' / name / 'pack.yaml').is_file():
            fails.append(f'workspace.yaml: active pack {name} has no packs/{name}/pack.yaml')

    packs = [p for p in sorted((ROOT / 'packs').iterdir()) if (p / 'pack.yaml').is_file()]
    for p in packs:
        meta = parse_yaml((p / 'pack.yaml').read_text(encoding='utf-8'))
        for k in ('name', 'scope', 'status', 'triggers'):
            if not meta.get(k) and not (p.name == '_template' and k == 'triggers'):
                fails.append(f'{p.name}/pack.yaml: missing {k}')
        if p.name.startswith('_'):
            continue
        fails += check_files(p.name, pack_files(p))
        fails += orphans(p)
        fails += external_tokens(p, meta)

    fails += check_files('core', core_files())
    fails += build_indexes.drift()  # rule 2
    fails += build_boot_card.check()
    fails += scan_personal()  # rule 4
    fails += core_standalone()

    for rel in ('local/settings/autonomy.md', 'local/settings/owner.md'):
        if not (ROOT / rel).is_file():
            print(f'WARN {rel} is missing. Run python3 core/scripts/setup.py to restore it.')
    for f in fails:
        print(f'FAIL {f}')
    n = sum(len(pack_files(p)) for p in packs if not p.name.startswith('_'))
    print(f"{'FAIL' if fails else 'PASS'}: {len(fails)} problems, {len(packs)} packs, {n} knowledge files checked")
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
