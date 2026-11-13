#!/usr/bin/env bash
# One-time setup for a new user. Copies templates/ to local/ (personal state, git-ignored),
# makes the work/ folders that workspace.yaml lists, then builds the indexes and the boot card.
# If local/ exists, it adds only the template files that are missing and never overwrites a file.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
if [ -e "$ROOT/local" ]; then
  echo "local/ exists. Setup adds missing template files only and overwrites nothing."
  added=0
  while IFS= read -r -d '' src; do
    rel="${src#"$ROOT/templates/"}"
    dest="$ROOT/local/$rel"
    if [ ! -e "$dest" ]; then
      mkdir -p "$(dirname "$dest")"
      cp "$src" "$dest"
      echo "added: local/$rel"
      added=$((added + 1))
    fi
  done < <(find "$ROOT/templates" -type f ! -name .gitkeep -print0)
  echo "Added $added missing template file(s)."
else
  cp -R "$ROOT/templates" "$ROOT/local"
  find "$ROOT/local" -name .gitkeep -delete
  echo "Made local/ from templates/"
fi
python3 - "$ROOT" <<'PY'
import sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / 'core/scripts'))
from _common import workspace
from _common import pack_dirs, parse_yaml
ws = workspace()
base = ws.get('work_root') or 'work'
names = []
if str(ws.get('pack_work_folders')).lower() == 'true':
    for p in pack_dirs():
        names += parse_yaml((p / 'pack.yaml').read_text(encoding='utf-8')).get('work_folders') or []
names = names or list(ws.get('work_folders') or [])  # the pack set replaces the generic set
seen = set()
for name in names:
    if name.lower() in seen:  # macOS and Windows file systems ignore case
        continue
    seen.add(name.lower())
    d = root / base / name
    d.mkdir(parents=True, exist_ok=True)
    print(f'work folder: {d.relative_to(root)}')
PY
python3 "$ROOT/core/scripts/build_indexes.py" --write
python3 "$ROOT/core/scripts/build_boot_card.py" --write
echo "Setup done. Next: fill in local/settings/owner.md, then run python3 core/scripts/validate.py </dev/null"
