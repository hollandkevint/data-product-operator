---
name: dpm-os
description: Initialize a DPM OS — a markdown workspace for one data product manager to move one data product decision from discovery to controlled release with three manual gates, a weekly decision packet, and an append-only decision log. Detects greenfield, migration, or active-repo mode, asks only for missing load-bearing context, copies the deterministic scaffold without overwriting, populates fields with provenance tags, runs the validator, and hands off the first three actions. Use when invoked as `/dpm-os` or when asked to set up a DPM OS in a directory.
---

# dpm-os — initializer

Scaffolds and initializes a DPM OS instance in the current working directory. Structure is deterministic (copied from `scaffold/`). Reasoning is adaptive (loaded from `prompts/` per phase).

| Layer | Where | Why |
| --- | --- | --- |
| Static structure: manual, index, context files, gates, templates, schemas, validator | `scaffold/` | Same every time. Never regenerated. |
| Adaptive reasoning: mode detection, migration, interview, post-scaffold | `prompts/` | Depends on the directory and the operator's answers. |
| Orchestration | this file | Glue. |

## When to invoke

- The operator runs `/dpm-os` or asks to set up a DPM OS here.
- Do not invoke for routine work after init. The seeded `CLAUDE.md` in the instance owns that.

## Workflow

### 1. Detect mode

Load `prompts/mode-detection.md`. Decide **greenfield** (empty), **migration** (product artifacts present), or **active-repo** (a working software repo). Announce the mode in one line. In active-repo mode do not proceed without the operator's confirmation.

### 2. Migrate if needed

Load `prompts/migration.md`. Copy pre-existing artifacts into `source/`. Never move. Record cross-document conflicts for the post-scaffold contradictions block.

### 3. Interview

Load `prompts/interview.md`. Ask the four batches, or only the gaps the source artifacts leave open. Confirm back what you heard before scaffolding.

### 4. Copy the scaffold, never overwrite

Copy every file and folder from `scaffold/` into the current directory, including `.claude/`, `.gitignore`, and `scripts/`. Run exactly this form, which carries dotfiles and never overwrites:

```bash
cp -Rn "<skill-dir>/scaffold/." .
```

Plain `cp -R` overwrites collisions; do not use it. On macOS, `cp -n` exits 1 when it skipped an existing file; that is a collision report, not a failure. Then apply these rules:

- A path that already existed at the destination was skipped by `-n`. List each such path as a collision.
- `.claude/settings.json` already present: merge the scaffold's one `PostToolUse` hook entry into the existing `hooks.PostToolUse` list. Do not replace the file.
- The current directory is the project root. Do not create a nested subfolder.
- Do not modify files under `scaffold/` at the source.

Verify by listing the destination: `INDEX.md`, `CLAUDE.md`, `.claude/settings.json`, `scripts/validate.py`, and the folders `context/`, `rules/`, `packets/`, `decisions/`, `risks/`, `source/`, `ingestion/`, `maintenance/` are present.

### 5. Populate with provenance

Walk the copied `context/` files and fill each section from the interview or the source artifacts, per the table in `prompts/interview.md`. Every populated section ends with a tag from the enum in `scaffold/decisions/_SCHEMA.md` or the literal `Unknown`. Fill the `## Current decision` block in `INDEX.md`; when no decision exists yet, write the first decision the operator named and mark its evidence gap.

### 6. Validate

Run `python3 scripts/validate.py .` from the instance root. Fix every finding before continuing.

### 7. Commit

If the directory is inside a git work tree, stage the scaffolded files and commit once: `feat: initialize DPM OS`. Otherwise `git init` here first. Never push. The operator controls publication.

### 8. Hand off

Load `prompts/post-scaffold.md`. Lead with the three first actions, then contradictions, then two or three gaps, then one paragraph on what was built.

## Skill surface

This initializer does not bundle analysis skills. When the `data-product-operator` skill library is installed under `.claude/skills/` at project or user scope, these resolve by name. When it is absent, the names below will not resolve; install it first (see the repo's `docs/install.md`).

| Skill | Reach for it when |
| --- | --- |
| `data-product-thinking` | Framing the problem before the data |
| `data-consumer-discovery` | Finding the first user and the decision they make |
| `data-product-validation` | Testing demand before building |
| `research-synthesis-data` | Turning interviews into evidence rows |
| `data-team-positioning` | Deciding whether the team is a service or a product team |
| `metrics-definition` | Writing the outcome metric with grain and window |
| `data-quality-assessment` | Filling the quality assertions table |
| `data-pipeline-quality` | Testing the pipeline behind a claim |
| `data-model-design` | Reviewing the schema behind a contract |
| `stakeholder-alignment` | Filling decision rights and bringing owners in early |
| `data-team-operating-model` | Setting cadence and handoffs |
| `ethical-risk-assessment` | The fifth risk in the assumptions list |
| `healthcare-data-domain` | Any regulated health data context |
| `data-storytelling` | Writing the packet's recommendation |
| `dashboards-to-decisions` | Turning a dashboard request into a decision |
| `grill-me-data` | Pressure-testing a packet before the gate |
| `arbitrage-audit-data` | Finding where the data creates an edge |

## Anti-patterns

- Regenerating scaffold content instead of copying it.
- Overwriting a file the operator already had.
- Skipping the validator.
- Inventing contradictions. If none were found, say so.
- Pushing.

## Files

- `SKILL.md` — this file
- `prompts/mode-detection.md`, `prompts/migration.md`, `prompts/interview.md`, `prompts/post-scaffold.md`
- `scaffold/` — the instance, copied as-is
