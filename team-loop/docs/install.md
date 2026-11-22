# Install and uninstall

## Claude Code: plugin (recommended)

Install the Data Product Operator plugin once. Team Loop and every analysis skill it names come with it.

```text
/plugin marketplace add hollandkevint/data-product-operator
/plugin install data-product-operator@data-product-operator
```

Open the project that will hold the instance and run `/data-product-operator:team-loop` (formerly `/dpm-os`). The skill detects whether the directory is empty, holds product artifacts, or is an active code repo, asks for what it cannot infer, copies the scaffold without overwriting anything you already have, runs the validator, and hands you the first three actions.

## Claude Code: copy the skill

Use this when you want Team Loop without the plugin, or a copy pinned inside one project.

1. Clone `data-product-operator`. Team Loop is in it as `skills/team-loop`.
2. Copy the skill into the project that will hold the instance:

   ```bash
   cp -R data-product-operator/skills/team-loop <your-project>/.claude/skills/team-loop
   ```

   For every project on the machine, copy to `~/.claude/skills/team-loop` instead.
3. Open the project in Claude Code and run `/team-loop`.

Requirements: `python3` on the path for the validator and its hook. Nothing else.

## Skill library

The initializer's "Skill surface" table names analysis skills from this repo. The plugin install includes them. With a copied skill, copy them too, or the names in that table do not resolve. The scaffold, gates, packet, log, and validator work without them.

```bash
cp -R data-product-operator/skills/* <your-project>/.claude/skills/
```

## Upgrade an instance

An instance keeps the validator it was created with. The version is the `SCAFFOLD_VERSION` line in the instance's `README.md`; the current one is in `skills/team-loop/scaffold/README.md`. To upgrade:

1. Copy `skills/team-loop/scaffold/scripts/validate.py` over the instance's `scripts/validate.py`. Do this only if the instance copy has no local edits; diff it against its old version first.
2. Run `python3 scripts/validate.py .` in the instance and fix each finding. From scaffold 0.2.0, every populated context file needs a provenance tag, or `Unknown`, at the end of a line under `## Provenance`. Use the source the file's rows already cite. Never invent one.
3. Update the instance's `SCAFFOLD_VERSION` line.

The [release notes](../../docs/releases/) say which scaffold changes need this.

## Uninstall

An instance is the set of files the scaffold copied, plus whatever you added inside its folders. The skill's validator prints that list with `--manifest`. Run it from the installed skill, not from the instance's `scripts/validate.py`: an instance made before scaffold 0.2.0 has a validator without the flag. From the project root:

```bash
SKILL=.claude/skills/team-loop   # or ~/.claude/skills/team-loop for a per-user install
python3 "$SKILL/scaffold/scripts/validate.py" --manifest > team-loop-manifest.txt \
  && test -s team-loop-manifest.txt \
  && cut -d/ -f1 team-loop-manifest.txt | sort -u | grep -vx -e .claude -e .gitignore | xargs rm -rf \
  && rm team-loop-manifest.txt
```

The chain stops before deleting anything if the manifest is empty or the command fails. It removes every top-level file and folder the manifest names, except `.claude/` and `.gitignore`. Init never overwrites an existing `.gitignore`, so that file may be yours; remove it by hand if the scaffold created it. The same is true of any file init reported as a collision, such as an existing `CLAUDE.md` or `README.md`: the command above removes it, so set it aside first.

If `.claude/settings.json` existed before install, remove only the `PostToolUse` entry whose command is `python3 scripts/validate.py`. If it did not, remove the file. Then delete `.claude/skills/team-loop`.

Source artifacts you copied into `source/` during migration are copies; the originals were never moved.

## Codex and other harnesses

Not documented yet. The scaffold is plain markdown and works in any editor; only the initializer skill and the write hook are Claude Code specific.
