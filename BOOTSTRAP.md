# Bootstrap

This guide sets up the second brain for a new user. All steps are local. No step writes to an
external system.

## 1. Install

1. Install Python 3.10 or later and git. The scripts use the Python standard library only.
2. Install Claude Code, Codex, or both.
3. Clone the repository to a folder that a cloud drive does not sync.

## 2. Run setup

1. Run `bash core/scripts/setup.sh`.
2. Setup copies `templates/` to `local/`, makes the `work/` folders, and builds the indexes.
3. If `local/` exists, setup adds only the template files that are missing. It never
   overwrites an existing file, and it prints each file that it adds.
4. `local/settings/autonomy.md` has four default grants. Because of them, the `wrap-up` skill
   records each session in `local/STATUS.md`, the logs and memory without a question.

`local/` holds all personal state: status, memory, registries, logs and settings.
`local/` and `work/` are git-ignored. Do not commit them.

## 3. Fill in your settings

1. Write your name, pronouns and writing style in `local/settings/owner.md`.
2. Write your name, user name and colleague names in `local/settings/privacy_patterns.txt`,
   one regular expression on each line. The validator then blocks these words in committed files.
3. Optional: review the local autonomy grants in `local/settings/autonomy.md`. Delete a row to
   turn off that automatic record, or add a row to grant more.

## 4. Choose packs

The core and the `general` pack need nothing external. Only `general` is on by default.

1. To turn on more packs, remove the `#` before their names in `active_packs` in `workspace.yaml`.
   Each pack is a folder in `packs/`.
2. Set `pack_work_folders: true` only if an active pack offers its own work folders.
3. Run `python3 core/scripts/build_indexes.py --write` and `python3 core/scripts/build_boot_card.py --write`.
4. To make a new pack, copy `packs/_template/` to `packs/<name>/` and fill in `pack.yaml`.

## 5. Connect tools

Install and sign in to the connectors that your own packs need. Verify each connector with one
harmless read before you rely on it.

## 6. Add files and knowledge

1. Say "add this process", "remember this" or "file this note". The `add-knowledge` skill
   classifies the item, proposes a path and the frontmatter, and writes after your OK.
2. Put deliverables in `work/<folder>/`. Put knowledge in a pack. Put personal facts in `local/`.
3. To find an item again, ask "where is X" or run `python3 core/scripts/find_knowledge.py <words>`.

## 7. Scheduled tasks (optional)

Set these in your runtime scheduler. They only read and report. They never apply a change.

| Task | Schedule | What it runs |
|---|---|---|
| Weekly digest | Once a week | skill `learning-digest` |
| Filing check | Once a week | skill `workspace-janitor` |

## 8. Checks

1. Run `python3 core/scripts/validate.py </dev/null`. It must show PASS.
2. Run the validator after each change to knowledge, skills, policy or indexes, and before each commit.

## 9. Updates

1. Run `git pull`. Your `local/` and `work/` folders do not change.
2. Run `bash core/scripts/setup.sh` again. It keeps your files in `local/` and makes new work
   folders and indexes.
3. Setup also adds each new file from `templates/` that is missing in `local/`. It never
   overwrites an existing file.
4. Run the validator.
