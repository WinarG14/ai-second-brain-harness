---
name: find-knowledge
description: "Find a stored process, fact, recipe, skill or memory again and report its source, status and date. Use when the user asks where is X, what do we know about X, find the note or the process for X, or when the router and the pack index give no match."
type: skill
pack: core
source: design section 6 (generic second brain design, 2026-10-29)
status: active
---

# Find knowledge

Read as little as possible. Go from the small index files to one file.

1. If the boot card is not loaded, read `core/boot_card.md`.
2. Read `core/router.md`. If a row matches the intent, follow its route.
3. Read the `INDEX.md` of the matching pack. Choose the row by title and type.
4. Read only that file, or only the matching line range of a large file.
5. If steps 2 to 4 give no match, run:
   `python3 core/scripts/find_knowledge.py <words>`
   It searches titles and triggers first, then file bodies. Add `--pack <name>` to narrow it,
   or `--all-packs` to include packs that are not active.
6. For names and terms, read `core/where_to_look.md`, then `local/registries/`.

## Report

- Give the path, the `source`, the `status` and the `valid_from` date.
- If the file is `draft` or `superseded`, or past `review_by`, say so before you use it.
- If a `superseded` file matches, follow `superseded_by` to the current file.
- If nothing matches, say "I did not find it". Ask one question, or offer `add-knowledge`.
