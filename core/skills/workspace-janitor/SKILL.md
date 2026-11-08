---
name: workspace-janitor
description: "Check the workspace against the filing rules and propose a move list: generated files that are out of date, superseded files older than 12 weeks, stale inbox files, sync-conflict copies, files past review_by. Propose-only. Use for tidy the workspace, run the janitor, filing check."
type: skill
pack: core
source: adapted from the SC harness workspace-janitor skill (2026-10-29)
status: active
---

# Workspace janitor

The janitor finds filing problems and proposes fixes. It never moves a file on its own.
Prevention comes first: recipes and `add-knowledge` file items correctly when they are made.
A problem that comes back is a signal to fix the recipe or the skill that made it.
Log it in `local/logs/learning_log.md`.

## Checks

1. Run `python3 core/scripts/validate.py </dev/null`. Each FAIL is a finding.
2. Superseded files: `status: superseded` and `valid_from` more than 12 weeks ago.
   Propose a move to `packs/<pack>/_archive/`.
3. Review dates: files in packs whose `review_by` date is in the past. Propose a check, not a move.
4. Inbox: files in the first `work_folders` entry (the inbox) older than 14 days. Propose a home.
5. Sync conflicts: names like `name 2.md` or `name (1).md`. Propose a review.
6. Root files: files at the repository root that are not in the README layout. Propose a home.

## Workflow

1. Run the checks. Do not change files during the checks.
2. Show a manifest: counts first, then a table with path, rule, proposed action.
3. Apply the moves only after one batch approval. The user can remove items from the batch.
4. After the moves, run `build_indexes.py --write`, `build_boot_card.py --write` and `validate.py`.
