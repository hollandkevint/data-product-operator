# Install Healthcare Data Readiness Debrief

The source is `skills/healthcare-data-readiness-debrief/` in this repository. Keep the complete folder, including references and examples. No separate plugins or data connectors are required.

## Codex

Ask Codex to install `skills/healthcare-data-readiness-debrief` from `hollandkevint/data-product-operator`. Its skill installer can select that folder without installing the entire library. For a version-pinned install, specify the desired commit as the source ref.

For an existing local checkout, copy that one folder into your Codex skills directory, normally `~/.codex/skills/`. If a folder with the same name already exists, inspect it and preserve local changes before replacing it. Use a fresh turn or session and invoke `$healthcare-data-readiness-debrief`.

## Claude Code

Copy the same complete folder into `.claude/skills/` in the project where you want to use it, or `~/.claude/skills/` for personal cross-project use. Check whether the destination is a symlink before copying. Do not replace the skills root or overwrite an existing skill without checking it.

Start a fresh session and invoke `/healthcare-data-readiness-debrief`. The repository also supports a Claude marketplace installation as described in the root README; namespaced plugin invocation may differ from the standalone installation.

## First use

Describe one project and its intended use in an approved summary, then ask for an interview or a brief. Use synthetic examples rather than patient records. The package's `CONTEXT.md` explains the output, source boundaries and testing limits.

Check that the assistant loads this skill and its relevant reference, asks one question when context is missing, and produces a brief when requested. File installation alone does not prove the host loaded the skill.

## Updates and removal

Treat this repository as the source. Record the commit or package content hashes used for a local copy. Update the whole skill folder together so instructions and references stay aligned. Keep private project notes outside the skill.

To uninstall, remove only the installed `healthcare-data-readiness-debrief` folder after confirming its exact location and preserving any local additions. Never remove a whole skills directory.
