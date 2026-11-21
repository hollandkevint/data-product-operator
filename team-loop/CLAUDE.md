# CLAUDE.md — dpm_os (maintainer)

This repo ships one Claude Code skill, `dpm-os`, that scaffolds a DPM OS instance. This file is for people and agents editing the repo, not for people using an instance. An instance's manual is `.claude/skills/dpm-os/scaffold/CLAUDE.md`.

## Rules

- **Edit `scaffold/`, never an instance.** Instances are copies. A fix belongs in the scaffold and ships in the next version.
- **This repo is public. It contains no client, customer, or engagement terms.** `tests/test_containment.py` holds the only list of such terms and fails on any hit. Before any push, also grep tracked files and `git log -p` by hand for names the list does not know.
- **No CE artifacts here.** Plans, solutions, and other compound-engineering documents live outside this repo.
- **Bump `SCAFFOLD_VERSION`** in `scaffold/README.md` when the scaffold changes shape.
- **Stdlib only** in `scripts/validate.py`. It must run on a bare `python3`.
- **Shared skills: public wins.** `data-product-operator` owns the body of every analysis skill the initializer names. A private collection copies those bodies unchanged. A private-only difference goes in a sibling `overlay.md` in the private copy, never as an edit to the shared `SKILL.md`. Improve a shared skill in the library first, then re-sync.

## Test

```bash
python3 -m unittest discover tests
python3 .claude/skills/dpm-os/scaffold/scripts/validate.py .claude/skills/dpm-os/scaffold
```

## Layout

- `.claude/skills/dpm-os/SKILL.md` — the initializer
- `.claude/skills/dpm-os/prompts/` — mode detection, migration, interview, post-scaffold
- `.claude/skills/dpm-os/scaffold/` — the instance, copied as-is
- `grader/` — sample grader: questions, answer-key SQL, harnesses, ship rule
- `tests/` — validator, grader, and containment tests
- `docs/install.md` — install and uninstall
