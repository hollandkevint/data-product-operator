# Contributing

Thanks for helping. This repo is public, so a few rules are firm.

## Run the checks

```sh
pip install -r team-loop/grader/requirements.txt
python team-loop/grader/data.py
python -m unittest discover -s tests
```

CI runs the same three steps. Run them before you open a PR.

## Add a skill

- Put it in `skills/<name>/SKILL.md`.
- Frontmatter needs `name`, `description` and, for a new skill, `metadata.version`.
- Write headings and rules in sentence case.
- Use the terms in [GLOSSARY.md](GLOSSARY.md). Do not use a word it lists under `_Avoid_` for something else.
- Add the skill to the [match grid](docs/match-grid.md) if it covers a job.

## Add a loop

Follow the [loop pattern](docs/loop-pattern.md). The checker must be a script, not a model. It must reject a broken demo.

## Add a check

- Put the function in `tests/checks_<topic>.py`.
- Put its tests in `tests/test_<topic>.py`.
- Each check must fail on the bug it guards. Break the thing once on purpose and watch the test fail.
- Edit `tests/repo_checks.py` only if you must, and keep the edit small.

## Sources and licenses

- You may adapt MIT sources, such as Matt Pocock and Pawel Huryn. Mark the skill as described in [adapted skills](docs/adapted-skills.md): `adapted_from:` in the frontmatter and a closing `Source:` line with the author, a link and the license.
- Aakash Gupta and 90n are commercial or not for resale. Give a name and a link only. Never copy their text.
- Add a license to `ADAPT_LICENSES` in `tests/checks_adapted.py` only after you read its terms.

## Voice

- Plain words. Short sentences. Commas and periods, no em dashes.
- Avoid the banned words in [CLAUDE.md](CLAUDE.md).
- Say what you tested.

## Privacy

- Name no client or employer from your own work. A containment test scans every tracked file and fails on a hit. If it fails, remove the term. Do not edit the digest list.
- Include no private facts about people or companies.
- Healthcare examples use synthetic or public data, such as OMOP.

## Commit hooks

Turn the hooks on once per clone with `git config core.hooksPath .githooks`. Pre-commit runs the containment, glossary, banned-word and link tests. Pre-push runs the full suite.

## Commits and PRs

Write a plain, imperative commit message. Describe the change and how you checked it.
