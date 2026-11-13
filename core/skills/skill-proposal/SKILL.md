---
name: skill-proposal
description: Propose new reusable second brain skills for repeated workflows; ask for approval before creating or editing skill files.
type: skill
pack: core
title: Skill Proposal
owner: pack owner
source: 'adapted from a private PM workspace'
valid_from: 2026-10-29
review_by: 2027-01-28
status: active
---

# Skill Proposal

Use when the user wants the AI co-worker to learn a new recurring workflow.

## Workflow

1. Identify repeated trigger phrases.
2. Define scope and non-goals.
3. Define required sources.
4. Define output format.
5. Define approval and safety gates.
6. Propose exact skill filename and contents summary.
7. Ask user approval before writing files. **On approval, hand off to the core `add-knowledge` skill**
   (type `skill`) for placement in `packs/<pack>/skills/<name>/SKILL.md`, the router row, the index
   rebuild and the validator run.

## Output

```markdown
## Skill Proposal
- Proposed skill name:
- Trigger phrases:
- Purpose:
- Sources:
- Workflow:
- Output format:
- Approval gates:
- Tests:
```

## Safety

Creating or changing skill files requires user approval unless the user explicitly asked to implement a plan that includes those specific files.
Do not perform external writes without explicit user confirmation. External writes include sending email, editing shared documents, changing tickets, or editing a shared knowledge base.
