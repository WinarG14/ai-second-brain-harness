# ai-second-brain-harness

A domain-neutral second brain for Claude Code and Codex. You add a process or a fact, the
system files it in one home with a source, and a later session finds it again.

## Layout

| Path | What it holds | Committed |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md` | Master policy (both runtimes) | yes |
| `workspace.yaml` | Active packs, work folders, runtime options | yes |
| `core/policy/` | Approval gates, filing, registries, provenance | yes |
| `core/skills/` | `add-knowledge`, `find-knowledge`, `learning-digest`, `workspace-janitor`, `wrap-up` | yes |
| `core/scripts/` | Build, validate, find, setup | yes |
| `core/registry_rows/` | Core rows for the router and where-to-look | yes |
| `core/router.md`, `core/where_to_look.md`, `core/boot_card.md` | Generated | yes |
| `packs/<name>/` | One domain: `processes/`, `knowledge/`, `recipes/`, `skills/`, `registry_rows/`, `evals/` | yes |
| `packs/general/` | The shipped pack | yes |
| `packs/_template/` | Empty pack to copy | yes |
| `BOOTSTRAP.md` | Setup guide | yes |
| `templates/` | Empty forms of the personal files | yes |
| `local/` | All personal state (status, memory, registries, logs, settings) | no |
| `work/` | Deliverables | no |

## Start

See `BOOTSTRAP.md`.

## Commands

| Command | What it does |
|---|---|
| `python3 core/scripts/setup.py` | Copies `templates/` to `local/`, makes `work/` folders, builds indexes |
| `python3 core/scripts/build_indexes.py --write` | Pack indexes, merged registries, skill pointers |
| `python3 core/scripts/build_boot_card.py --write` | Boot card from active packs and recipes |
| `python3 core/scripts/validate.py` | The 5 validator rules, with the personal-data scan |
| `python3 core/scripts/find_knowledge.py <words>` | Search titles, then bodies |
