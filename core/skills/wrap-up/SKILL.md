---
name: wrap-up
description: "Close a session that did real work: report the result and the verification, record the session in local/STATUS.md, the run ledger, the learning log and memory when it is useful, and propose new knowledge through add-knowledge. Use at the end of a session, or when the user says wrap up."
type: skill
pack: core
source: adapted from the SC workspace AGENTS.md session wrap-up section (2026-10-29)
status: active
---

# Wrap-up

Run this skill automatically at the end of every task that did real work. Do not ask the user
whether to run it, and never skip it. Skip it only for a short question with no lasting result.

1. Give the result, the verification that you ran, and each open blocker.
2. Read `local/settings/autonomy.md`. Do each local write below that has a grant without a
   question. Only a write outside the grants (for example `add-knowledge` into a pack) needs the
   user's OK: put all of those in one question at the end. The granted records are still written
   even if the user does not answer that question. If `local/settings/autonomy.md` is missing,
   run `python3 core/scripts/setup.py` to restore it, then continue.
3. Work worth a record: append one dated line to `local/STATUS.md`.
4. A completed deliverable or a useful evaluation: add one row to `local/logs/run_ledger.md`.
   Name the recipe or skill that you used, or `none`.
5. A correction or a reusable finding: find an existing entry in `local/logs/learning_log.md`.
   Add one occurrence to it, or add a new `[pattern]` entry.
6. A durable fact or preference: update `local/memory/` and its `INDEX.md`. Update an existing
   entry. Do not make a duplicate.
7. A new process, fact or recipe: run `add-knowledge`.
8. Close with one line: "Recorded: <list>".

External writes stay confirm-first. Do not turn a recommendation that the user did not
accept into a commitment.
