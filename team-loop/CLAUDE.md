# CLAUDE.md — Team Loop (maintainer), formerly dpm_os

Team Loop is one Claude Code skill, `team-loop`, that scaffolds an instance. It lives in the `data-product-operator` repo. This file is for people and agents editing it, not for people using an instance. An instance's manual is `skills/team-loop/scaffold/CLAUDE.md`.

## Rules

- **Edit `scaffold/`, never an instance.** Instances are copies. A fix belongs in the scaffold and ships in the next version.
- **This repo is public. It contains no client, customer, or engagement terms.** `tests/test_containment.py` (repo root) holds the only list of such terms and fails on any hit. The pre-commit hook runs it (`git config core.hooksPath .githooks`). Before any push, also grep tracked files and `git log -p` by hand for names the list does not know.
- **No CE artifacts here.** Plans, solutions, and other compound-engineering documents live outside this repo.
- **Bump `SCAFFOLD_VERSION`** in `scaffold/README.md` when the scaffold changes shape, and say in the release notes whether instances must upgrade ([install](docs/install.md#upgrade-an-instance)).
- **Stdlib only** in `scripts/validate.py`. It must run on a bare `python3`.
- **Shared skills: public wins.** `data-product-operator` owns the body of every analysis skill the initializer names. A private collection copies those bodies unchanged. A private-only difference goes in a sibling `overlay.md` in the private copy, never as an edit to the shared `SKILL.md`. Improve a shared skill in the library first, then re-sync.

## Test

```bash
python3 -m unittest discover -s tests
python3 skills/team-loop/scaffold/scripts/validate.py skills/team-loop/scaffold
```

## Layout

- `skills/team-loop/SKILL.md` — the initializer
- `skills/team-loop/prompts/` — mode detection, migration, interview, post-scaffold
- `skills/team-loop/scaffold/` — the instance, copied as-is
- `team-loop/grader/` — sample grader: questions, answer-key SQL, harnesses, ship rule
- `tests/` (repo root) — validator, grader, and containment tests
- `team-loop/docs/install.md` — install and uninstall
