#!/usr/bin/env bash
# Wrapper for core/scripts/setup.py, kept for old instructions. On Windows, run
# `py -3 core/scripts/setup.py` directly: it needs no bash.
set -eu
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for py in python3 python; do
  # Skip a name that does not run Python 3 (for example the Windows Store stub).
  if "$py" -c 'import sys; sys.exit(sys.version_info[0] != 3)' >/dev/null 2>&1; then
    exec "$py" "$DIR/setup.py" "$@"
  fi
done
if py -3 -c '' >/dev/null 2>&1; then exec py -3 "$DIR/setup.py" "$@"; fi
echo "Python 3 not found. Install Python 3.10 or later, then run: python core/scripts/setup.py" >&2
exit 1
