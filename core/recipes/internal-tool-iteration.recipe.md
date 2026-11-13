---
type: recipe
pack: core
title: 'Internal tool / skill iteration (scripts, scorecards, generators, dashboards)'
owner: pack owner
source: 'this file'
valid_from: 2026-10-29
review_by: 2027-01-28
status: draft
trigger: 'Build / iterate / "enhance-fix-extend" ANY internal tool or skill with user-facing output (scripts, scorecards, generators, dashboards)'
---

# Recipe: internal tool or skill iteration

**Trigger:** you build or change a tool with output that people read: a skill script, a CLI, a
scorecard, a report generator, a dashboard. This includes "enhance, fix or extend the X skill".
Read this recipe before you plan the change.

## Why this recipe exists

Plans and checks often describe only the change. Then nothing protects what the tool must keep
doing, and a rewrite can drop output that users rely on. This recipe makes the full output the
contract.

## Intake: ask once at the start of a new tool

1. Who are all the end users, and how technical are they? This sets the words for every output text.
2. Which tools and platforms do they use?
3. What does each user do next with each output? Make every output one step from that action.
4. Which numbers will users check, and against what? Build that check into the first version.

## Rules for every iteration

- **Output contract, not memory.** Keep a committed list (or golden output files) of everything the
  default output shows. Long sessions lose detail; files do not.
- **Add, do not silently remove.** The default output of a new version shows everything that the
  last version showed. State each removal in the change log.
- **Compare outputs, not plans.** Before you ship a rewrite, run the old and the new version and
  compare the outputs. Do this also for work that a subagent did.
- **Numbers reconcile.** Each number that users see has a check: the parts add up to the total, or
  it matches an outside reference.
- **Scores need good and bad examples.** A score ships only after a known-good example scores high
  and a known-bad example scores low.
- **Read the output as the least technical user.** Define each term. Make each file path a link
  that users can click.

## Checklist before you call an iteration done

1. The output comparison with the last version shows only intended changes.
2. All example files pass, including the bad example. A run on real data shows every section.
3. Every number that users see reconciles.
4. Every option still works on the default path.
5. You read all new or changed text as the end user.
6. The change log states each removal and each restoration.
