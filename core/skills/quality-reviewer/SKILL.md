---
name: quality-reviewer
description: 'Review PM outputs for source grounding, acronym clarity, hallucination risk, lifecycle completeness, approval gates, and executive-readiness before delivery.'
type: skill
pack: core
title: PM Quality Reviewer
owner: pack owner
source: 'adapted from a private PM workspace'
valid_from: 2026-07-04
review_by: 2026-10-03
status: active
---

# PM Quality Reviewer

Use before finalizing important PM deliverables.

## Checklist

- Are acronyms explained on first use?
- Are factual claims cited or marked as open questions?
- Are claims from requests, drafts and meeting notes kept apart from confirmed facts?
- Are metrics, dates, owners, APIs, tables, and Service Level Agreement values sourced?
- Is the lifecycle stage clear?
- Are next actions concrete?
- Are any pie, donut, circular, or multi-pie charts present? If yes, fail the review unless the user explicitly approved an exception. Use a bar chart or a table in its place.
- If a chart needs exact figures, are those figures also in a table or a caption next to it?
- Is an external write proposed? If yes, is there an approval gate?
- Are risks and blockers visible?

## Output

Return pass/warn/fail with specific fixes. Do not rewrite the whole artifact unless requested.

## Safety

Do not perform external writes without explicit user confirmation. External writes include sending email, editing shared documents, changing tickets, or editing a shared knowledge base.
