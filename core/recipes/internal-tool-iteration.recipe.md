---
type: recipe
pack: core
title: 'Internal tool / skill iteration (scripts, scorecards, generators, dashboards)'
owner: pack owner
source: 'adapted from a private PM workspace'
valid_from: 2026-10-29
review_by: 2027-01-28
status: draft
trigger: 'Build / iterate / "enhance-fix-extend" ANY internal tool or skill with user-facing output (scripts, scorecards, generators, dashboards)'
---

# Recipe — Internal tool / skill iteration (scripts, scorecards, generators, dashboards)

> **Version 1.0 · compiled 2026-07-10 · maturity: draft** (distilled from the
> token-efficiency-scorecard build: ~15 iterations, of which roughly half were avoidable rework —
> this recipe exists to eliminate the avoidable half).
>
> **Trigger:** building or iterating ANY tool with user-facing output — a skill script, CLI,
> scorecard, report generator, dashboard, Apps Script — including "enhance/fix/extend the X skill"
> requests. Read this BEFORE planning the change.

## Why this recipe exists (the failure modes it prevents)

Observed across the token-efficiency-scorecard iterations (2026-07): a renderer rewrite silently
dropped 11 established output sections; costs were 4.5x inflated until cross-checked against an
external tool; the scoring rubric flattered a known-wasteful user; output text used unexplained
jargon a non-technical PM couldn't act on; the saved-report path wasn't clickable so the user
couldn't do his next action (drag → send to your manager). **Root cause common to all: plans and
verification described the DELTA; nothing owned the full contract of what the tool must keep
doing.**

## Intake — ask ONCE at the start of any new tool (registry rule 2 applies)

1. **Who are ALL the end users** (not just the requester)? Technical level? → sets the language
   register for every user-facing string.
2. **What platforms/tools do they use?** (e.g. "half the team is on Codex, not Claude" surfaced
   only at v1.1 — one intake question would have caught it at v0.1.)
3. **What is the user's NEXT ACTION with each output artifact?** (share to whom, via what channel)
   → every artifact must be one click/drag from that action.
4. **Which displayed numbers will users cross-check, against what reference?** (codeburn, /usage,
   a dashboard) → build the reconciliation in from v0.1, don't wait for the user to find the gap.

## Standing rules during EVERY iteration

- **Output contract, not conversation memory.** Maintain a committed section-inventory manifest
  (or golden output fixtures) of everything the DEFAULT output displays. Long build sessions get
  compacted — conversation memory of "what the product looked like" degrades; files don't.
- **Additive-evolution gate.** A new version's default output must be a SUPERSET of the previous
  release's default output. Every removed section must be intentional and stated in the changelog.
  A regression gate scoped only to a legacy flag (`--no-codex`-style) does NOT count — gate the
  surface users actually see.
- **Diff outputs, not plans.** Before shipping any renderer/formatter/rewrite: run old and new
  side-by-side and diff the section inventory. Applies doubly to DELEGATED implementations
  (Codex rescue, subagents): accept on old-vs-new output diff, never on plan-conformance alone —
  plan-conformance inherits the plan's blind spots.
- **Numbers reconcile from v0.1.** Every user-visible number needs an internal identity
  (parts sum to total) or an external reference check BEFORE first ship. A number the user has to
  challenge costs a full iteration.
- **Scoring systems need discriminant fixtures.** A grade/rubric ships only after a known-good
  fixture scores high AND a known-wasteful fixture scores low. "Everyone gets 100" is a design
  smell, not a success.
- **Persona + next-action pass on all user-facing text.** Read every output string as the least
  technical end user (per intake Q1). Apply the user's standing global rules to TOOL OUTPUT, not
  just chat replies — esp. "explain terms/acronyms inline" and "cite sources". Jargon needs an
  inline plain-English definition or a glossary entry. File paths shown to users must be rendered
  as clickable links (markdown `[name](file://…)` below the notes marker) plus a copyable plain
  path. Offer further-reading links where a guide exists.
- **Release flow (when the tool is a published team skill):** edit working copy → verify (contract
  diff + fixtures + real data) → repo commit + tag → copy to shared skill folder → mirror sync
  `--check` → KB action log → memory update. Never edit the shared copy directly.

## Verification checklist (run before declaring any iteration done)

1. Section-inventory diff vs previous release = intentional changes only.
2. All fixtures pass (incl. the wasteful/adversarial one); real-data run renders every section.
3. Every displayed number reconciles (identity or external reference).
4. Every flag/option still works on the DEFAULT path (a flag read only by a legacy branch = bug).
5. Persona read-through of new/changed text; next-action walkthrough of artifacts.
6. Changelog states restorations/removals explicitly.

