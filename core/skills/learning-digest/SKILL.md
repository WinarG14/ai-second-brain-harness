---
name: learning-digest
description: "Review the learning log and the run ledger and propose evidence-backed changes to skills, recipes, processes, registries or memory. Also lists files past review_by. Run on request (weekly digest, review the learning log). Never applies a change without approval."
type: skill
pack: core
source: adapted from the SC harness learning-digest skill (2026-10-29)
status: active
---

# Learning digest

Turn captured corrections into changes that later tasks can find and use.
`AGENTS.md` and `core/policy/approval_gates.md` own the approval rules.

## Read-only review

1. Read `local/logs/learning_log.md` and the matching evidence in `local/logs/run_ledger.md`.
   Ignore entries tagged `[done→...]` or `[archived→stale]`.
2. Count the occurrences of each `[pattern]` entry: 1 is watching, 2 or 3 is emerging, 4 or more is strong.
   The normal threshold for a promotion is 2. One decisive occurrence can be promoted only with
   the user's approval in a live session.
3. For each candidate, read the destination file. If the rule is already there, propose a log
   tag change, not a duplicate rule.
4. Draft the exact change for each candidate:
   - Skill: the file, the edit, and the trigger words for its description.
   - Process or knowledge: the file and the edit, through `add-knowledge` rules.
   - Recipe: a dated refinement and a `valid_from` update.
   - Memory: one `local/memory/` file and its `INDEX.md` line.
5. List patterns with no occurrence in the last eight weeks for review, not for removal.
6. Run `python3 core/scripts/validate.py </dev/null`. List each file in a pack whose
   `review_by` date is in the past. Do not change those files.

## Report

Give one approval batch: evidence, destination, exact change, and how a later task will
show that the rule was used. An approval, a saved rule and a later use are three different states.
Do not say that behavior improved because a file changed.
