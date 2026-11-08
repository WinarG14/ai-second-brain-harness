# Filing rules

Each item has one home. The `add-knowledge` skill applies the tree in `core/skills/add-knowledge/SKILL.md`.

| Kind of item | Home |
|---|---|
| Fact about a product or domain | `packs/<pack>/knowledge/<topic>.md` |
| How a team does work | `packs/<pack>/processes/<name>.md` |
| How to make one deliverable type | `packs/<pack>/recipes/<name>.recipe.md` (domain-neutral: `core/recipes/`) |
| Workflow that the agent runs with tools | `packs/<pack>/skills/<name>/SKILL.md` (domain-neutral: `core/skills/`) |
| Person, preference, correction, dated status | `local/` (see the tree) |
| Deliverable (a document, a page, a deck) | `work/<folder from workspace.yaml>/` |

Rules:

- Use kebab-case or snake_case file names. Do not use spaces.
- Do not make a second copy of a file. Link to the one home.
- Keep drafts and final versions apart. Mark the state in frontmatter `status`.
- Never edit a generated file: `packs/*/INDEX.md`, `core/router.md`, `core/where_to_look.md`,
  `core/boot_card.md`, `.claude/skills/`, `.agents/skills/`. Change the source, then run
  `python3 core/scripts/build_indexes.py --write` and `python3 core/scripts/build_boot_card.py --write`.
- A superseded file stays in place with `superseded_by`. The janitor proposes a move to
  `packs/<pack>/_archive/` after 12 weeks.
