# Local autonomy grants (personal)

The core default is confirm-first for every write. A grant here lets the agent do a LOCAL
write without asking. External writes are never on this list.

The four default rows below let the `wrap-up` skill record each session without a question.
Delete any row to turn that record off. Add a row with a date to grant more.

| Granted on | Local write the agent may do without asking | Report rule |
|---|---|---|
| default | At wrap-up after real work: append one dated line to `local/STATUS.md`. | Closing line "Recorded: ..." |
| default | At wrap-up: add one row to `local/logs/run_ledger.md`. | Closing line "Recorded: ..." |
| default | At wrap-up: add a new `[pattern]` entry, or an occurrence to an existing entry, in `local/logs/learning_log.md`. | Closing line "Recorded: ..." |
| default | At wrap-up: update or add one `local/memory/` file and its `INDEX.md` line (update, do not duplicate). | Closing line "Recorded: ..." |

Not granted (these stay confirm-first): changes in `packs/`, `core/`, `templates/`, the root
files, skills or policy; deleting or rewriting entries in a log or in memory; changes to
`local/registries/` and `local/settings/`.
