---
name: wrap-up
description: "Close a session that did real work: report the result and the verification, record the session in local/STATUS.md, the run ledger, the learning log and memory when it is useful, and propose new knowledge through add-knowledge. Use at the end of a session, or when the user says wrap up."
type: skill
pack: core
source: adapted from the SC workspace AGENTS.md session wrap-up section (2026-10-29)
status: active
---

# Wrap-up

Skip this skill for a short question with no lasting result.

1. Give the result, the verification that you ran, and each open blocker.
2. Read `local/settings/autonomy.md`. Each local write below that has a grant is done without
   a question. Each other write is shown first and done after the user says OK.
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
