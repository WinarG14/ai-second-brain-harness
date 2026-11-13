# Registries rules

A registry is a lookup table that the agent reads before it asks the user a question.

| Registry | Shared rows (roles, no names) | Personal rows |
|---|---|---|
| Router | `core/registry_rows/router.md`, `packs/<pack>/registry_rows/router.md` | none |
| Where to look | `core/registry_rows/where_to_look.md`, pack `registry_rows/where_to_look.md` | none |
| Entities | pack `registry_rows/entities.md` | `local/registries/entities.md` |
| Contacts | pack `registry_rows/contacts.md` (roles only) | `local/registries/contacts.md` |

Rules:

1. Ask once. When the user answers a question about a name, a term or an owner, propose a registry row.
2. Sessions propose rows. The learning digest curates them. Do not delete a row without a reason.
3. Each row that has a fact has a source and a "last checked" date when the table has those columns.
4. Shared rows name a role, never a person. A person's name goes only in `local/`.
5. All registry_rows tables of one name must have the same columns. `build_indexes.py` merges
   them into `core/<name>.md` and adds a Pack column.
