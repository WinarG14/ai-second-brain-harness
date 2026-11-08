"""Shared helpers for the core scripts. Standard library only (no PyYAML)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIRS = ('processes', 'knowledge', 'recipes')
TYPES = ('knowledge', 'process', 'recipe', 'skill', 'contact', 'entity', 'memory')
FOLDER_TYPE = {'processes': 'process', 'knowledge': 'knowledge', 'recipes': 'recipe', 'skills': 'skill'}
STATUSES = ('draft', 'active', 'superseded', 'archived')
REQUIRED = ('type', 'pack', 'source', 'status')


def _scalar(v: str):
    v = v.strip()
    if v[:1] == "'":  # single-quoted: '' is an escaped quote; keep ' #' inside
        m = re.match(r"'((?:[^']|'')*)'", v)
        return m.group(1).replace("''", "'") if m else v[1:]
    if v[:1] == '"':
        m = re.match(r'"((?:[^"\\]|\\.)*)"', v)
        return m.group(1).replace('\\"', '"') if m else v[1:]
    v = re.sub(r'(^|\s+)#.*$', '', v).strip()  # trailing comment
    if v.startswith('[') and v.endswith(']'):
        return [x.strip().strip('"\'') for x in v[1:-1].split(',') if x.strip()]
    return v


def parse_yaml(text: str) -> dict:
    """Parse the flat YAML used here: `key: value`, `key: [a, b]`, a `key:` with `- item`
    lines, and one level of nested `  sub: value` maps. Enough for workspace.yaml and pack.yaml."""
    data: dict = {}
    key = None
    for raw in text.splitlines():
        line = '' if raw.lstrip().startswith('#') else raw.rstrip()
        if not line.strip():
            continue
        if not line.startswith(' '):
            k, _, v = line.partition(':')
            key = k.strip()
            data[key] = _scalar(v) if v.strip() else None
        elif key is not None and line.strip().startswith('- '):
            if not isinstance(data[key], list):
                data[key] = []
            data[key].append(_scalar(line.strip()[2:]))
        elif key is not None and ':' in line:
            if not isinstance(data[key], dict):
                data[key] = {}
            k, _, v = line.strip().partition(':')
            data[key][k.strip()] = _scalar(v)
    return data


def frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return None
    end = text.find('\n---', 4)
    return parse_yaml(text[4:end]) if end > 0 else None


def workspace() -> dict:
    return parse_yaml((ROOT / 'workspace.yaml').read_text(encoding='utf-8'))


def pack_dirs(active_only: bool = True) -> list[Path]:
    """Pack folders, without `_template`. With active_only, only packs in workspace.yaml."""
    active = workspace().get('active_packs') or []
    out = []
    for p in sorted((ROOT / 'packs').iterdir()):
        if p.is_dir() and not p.name.startswith(('_', '.')) and (p / 'pack.yaml').is_file():
            if not active_only or p.name in active:
                out.append(p)
    return out


def pack_files(pack: Path) -> list[Path]:
    """Knowledge files of a pack: .md files in processes/, knowledge/, recipes/ and each skills/*/SKILL.md."""
    files = []
    for d in KNOWLEDGE_DIRS:
        files += sorted((pack / d).glob('*.md'))
    files += sorted((pack / 'skills').glob('*/SKILL.md'))
    return files


def cells(line: str) -> list[str]:
    """Split a Markdown table row on unescaped pipes only."""
    return [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]

