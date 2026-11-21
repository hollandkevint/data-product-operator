# Install and uninstall

## Claude Code

1. Clone this repo.
2. Copy the skill into the project that will hold the instance:

   ```bash
   cp -R dpm_os/.claude/skills/dpm-os <your-project>/.claude/skills/dpm-os
   ```

   For every project on the machine, copy to `~/.claude/skills/dpm-os` instead.
3. Open the project in Claude Code and run `/dpm-os`. The skill detects whether the directory is empty, holds product artifacts, or is an active code repo, asks for what it cannot infer, copies the scaffold without overwriting anything you already have, runs the validator, and hands you the first three actions.

Requirements: `python3` on the path for the validator and its hook. Nothing else.

## Skill library

The initializer's "Skill surface" table names analysis skills from [data-product-operator](https://github.com/hollandkevint/data-product-operator). They are a separate install. Without them the names in that table do not resolve; the scaffold, gates, packet, log, and validator work without them.

```bash
git clone https://github.com/hollandkevint/data-product-operator.git
cp -R data-product-operator/skills/* <your-project>/.claude/skills/
```

## Uninstall

An instance is the set of files the scaffold copied. Remove them and nothing else:

```bash
rm -rf context rules packets decisions risks source ingestion maintenance scripts
rm -f AGENTS.md CLAUDE.md INDEX.md README.md
```

If `.claude/settings.json` existed before install, remove only the `PostToolUse` entry whose command is `python3 scripts/validate.py`. If it did not, remove the file. Then delete `.claude/skills/dpm-os`.

Source artifacts you copied into `source/` during migration are copies; the originals were never moved.

## Codex and other harnesses

Not documented yet. The scaffold is plain markdown and works in any editor; only the initializer skill and the write hook are Claude Code specific.
