# Mode detection

Inspect the current working directory. Be conservative. If anything looks unsafe, pause and ask.

## Greenfield

Effectively empty. A `.git/`, a stray `README.md`, or empty folders do not count. Announce: "Greenfield mode. Running the full interview."

## Migration

Pre-existing product artifacts: briefs, requirements, decks, interview notes, strategy docs, data dictionaries. Announce with a one-line inventory: "Migration mode. Found N product artifacts. I will copy them into `source/` (originals stay put) and ask only the gaps." Load `migration.md` before the interview.

## Active-repo

A working software repository: build manifests (`package.json`, `pyproject.toml`, `go.mod`, and the like), `src/`, `lib/`, `tests/`, CI config, a `Dockerfile`, or substantial source code. Do not scaffold without confirmation. Ask:

> "This looks like an active working repository (detected: <signals>). I can (a) scaffold the DPM OS here alongside the code, skipping any file that already exists, or (b) stop so you can run this in a different directory. Which one?"

Wait for the answer. On (a), run migration on any product artifacts mixed in with the code, ignoring code and build directories, and apply the no-overwrite rule strictly: existing `CLAUDE.md`, `INDEX.md`, `README.md`, `.gitignore`, and `.claude/settings.json` are kept, and the scaffold versions are skipped or merged per `SKILL.md` step 4.

## Edge cases

- Artifacts belong to someone else's project (a web app with no product docs): treat as active-repo and ask.
- The operator pasted artifacts but the directory is empty: treat the paste as migration input and confirm before writing anything into `source/`.
- Ambiguous: ask one question. Mode choice changes the whole flow.
