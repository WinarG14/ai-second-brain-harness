---
name: add-knowledge
description: "File a new process, fact, recipe, skill, contact, term, preference, correction or status in its one correct home, with frontmatter and an index row. Use when the user says add this process, remember this, store this, file this note, save this as knowledge, or when a session finds a reusable item. Proposes the path, then writes after the user says OK."
type: skill
pack: core
source: design section 5 (generic second brain design, 2026-10-29)
status: active
---

# Add knowledge

Put each new item in one home, give it frontmatter, and make sure a later session can find it.

## 1. Classify the item

Ask the questions in this order. Use the first "yes".

| Question | Type | Home | Index |
|---|---|---|---|
| 1. Is it a fact about how a product or domain works? | knowledge | `packs/<pack>/knowledge/<topic>.md` | pack `INDEX.md` |
| 2. Is it how a team does work (steps, gates, owners by role)? | process | `packs/<pack>/processes/<name>.md` | pack `INDEX.md` + `where_to_look` row |
| 3. Is it how to make one deliverable type? | recipe | `packs/<pack>/recipes/<name>.recipe.md` | pack `INDEX.md` + boot card |
| 4. Is it a workflow that the agent runs with tools? | skill | `packs/<pack>/skills/<name>/SKILL.md` | router row |
| 5. Is it a person or an owner? | contact | `local/registries/contacts.md` (names); pack `registry_rows/contacts.md` (roles only) | registry |
| 6. Is it a term, market, system or codename? | entity | `local/registries/entities.md` or pack `registry_rows/entities.md` | registry |
| 7. Is it a preference or a durable personal fact? | memory | `local/memory/<topic>.md` | `local/memory/INDEX.md` |
| 8. Is it a correction ("do not do X")? | learning | `local/logs/learning_log.md` | digest promotes it after 2 or more occurrences |
| 9. Is it dated, changing status? | status | `local/STATUS.md` | none |

If no question gives "yes", ask the user one question. Do not guess.

## 2. Choose the pack (types 1 to 4, and shared rows of 5 and 6)

1. Read `triggers` and `scope` in each `packs/*/pack.yaml` that `workspace.yaml` lists in `active_packs`.
2. Choose the pack with the best match.
3. If no pack matches, propose `packs/general/` or a new pack from `packs/_template/`.
   A new pack is a policy change: confirm it first.

## 3. Check for a duplicate

Run `python3 core/scripts/find_knowledge.py <two or three title words> --all-packs`.
If an active file covers the same item, propose an update of that file, not a new file.
If the new item replaces an old file, set the old file to `status: superseded` with
`superseded_by: <new path>`.

## 4. Write the frontmatter (types 1 to 4)

```yaml
---
type: knowledge | process | recipe | skill
pack: <pack name, same as the folder>
title: <short title, unique among active files in the pack>
owner: <role, or a person only in local/>
source: <URL, repository path, or "user statement YYYY-MM-DD">   # mandatory
valid_from: <YYYY-MM-DD>
review_by: <YYYY-MM-DD, about 3 months later>
status: draft | active | superseded | archived
superseded_by: <path>        # only when superseded
trigger: <recipes only: the words that start this recipe>
---
```

A skill also needs `name` (same as the folder) and `description` (when to use it).
The content follows `core/policy/provenance.md`. Shared files contain no personal data.

## 5. Propose, then write

1. Show the user: the type, the path, the frontmatter, and the index rows that will change.
2. Write after the user says OK, or without a question if `local/settings/autonomy.md` grants it.
3. For a process, add a row to `packs/<pack>/registry_rows/where_to_look.md`.
   For a skill, add a row to `packs/<pack>/registry_rows/router.md`.
4. Run `python3 core/scripts/build_indexes.py --write` and `python3 core/scripts/build_boot_card.py --write`.
5. Run `python3 core/scripts/validate.py`. Fix each FAIL before you report.
6. Run `python3 core/scripts/find_knowledge.py <title words>` and show that the new file is found.
7. Report the path and the validator result in one or two lines.

For types 5 to 9, append the row or the entry in `local/`. Only `local/memory/` needs an index line.
