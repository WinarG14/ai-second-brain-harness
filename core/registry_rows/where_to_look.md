# Core where-to-look rows

| Need | First source | Fallback | Freshness rule |
|---|---|---|---|
| Approval rules for writes | `core/policy/approval_gates.md` | `AGENTS.md` | Policy changes are confirm-first |
| Where a new file goes | `core/policy/filing_rules.md` | skill `add-knowledge` | none |
| How registries are kept | `core/policy/registries_rules.md` | none | none |
| How to cite a source | `core/policy/provenance.md` | none | none |
| Prior work and current state | `local/STATUS.md` | `local/logs/run_ledger.md` | Last 30 days first |
| Personal names and terms | `local/registries/contacts.md`, `local/registries/entities.md` | Ask the user once, then add a row | Check before you name a person in an external draft |
