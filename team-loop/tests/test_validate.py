import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCAFFOLD = REPO / ".claude" / "skills" / "dpm-os" / "scaffold"
VALIDATE = SCAFFOLD / "scripts" / "validate.py"

spec = importlib.util.spec_from_file_location("validate", VALIDATE)
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)

RECORD = """# Decision: ship the thing

## Status
decided

## Date
2026-01-05

## Decider
A. Person

## Context
Text.

## Decision
Ship.

## Why
Because.

## Evidence
- The buyer asked for it  (stakeholder-verbal, A. Person, 2026-01-04)
- Prior note  [ingestion/note.md](../ingestion/note.md)

## Explicitly NOT doing
- A second cohort  Unknown

## What would reverse this
Adoption under 20 percent by 2026-03-01.

## Review date
2026-03-01
"""


def _copy_if_absent(src: str, dst: str) -> None:
    if not Path(dst).exists():
        shutil.copy2(src, dst)


def copy_scaffold(dest: Path) -> None:
    """Copy scaffold/. into dest without overwriting existing files (KTD6)."""
    shutil.copytree(SCAFFOLD, dest, dirs_exist_ok=True, copy_function=_copy_if_absent)


def run_cli(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATE), str(root)], capture_output=True, text=True)


def run_hook(file_path: Path) -> subprocess.CompletedProcess:
    payload = json.dumps({"tool_input": {"file_path": str(file_path)}})
    return subprocess.run([sys.executable, str(VALIDATE)], input=payload, capture_output=True, text=True)


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        copy_scaffold(self.tmp)
        (self.tmp / "ingestion" / "note.md").write_text("# note\n")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_raw_scaffold_passes(self):
        self.assertEqual(run_cli(SCAFFOLD).returncode, 0, run_cli(SCAFFOLD).stdout)

    def test_greenfield_copy_passes_and_has_settings(self):
        r = run_cli(self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue((self.tmp / ".claude" / "settings.json").is_file())

    def test_missing_required_file_named(self):
        (self.tmp / "rules" / "launch.md").unlink()
        r = run_cli(self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("rules/launch.md: required file missing", r.stdout)

    def test_valid_record_passes(self):
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(RECORD)
        r = run_cli(self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_missing_heading_named(self):
        bad = RECORD.replace("## What would reverse this\nAdoption under 20 percent by 2026-03-01.\n", "")
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(bad)
        r = run_cli(self.tmp)
        self.assertIn("missing heading '## What would reverse this'", r.stdout)

    def test_untagged_evidence_row_named(self):
        bad = RECORD.replace("- Prior note  [ingestion/note.md](../ingestion/note.md)", "- Prior note with no tag")
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(bad)
        r = run_cli(self.tmp)
        self.assertIn("untagged row 2 under '## Evidence'", r.stdout)

    def test_bad_status_named(self):
        bad = RECORD.replace("## Status\ndecided", "## Status\ndone")
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(bad)
        r = run_cli(self.tmp)
        self.assertIn("status 'done' not in", r.stdout)

    def test_log_row_cell_count(self):
        log = self.tmp / "decisions" / "LOG.md"
        log.write_text(log.read_text() + "| 2026-01-05 | Ship | A. Person | Unknown | decided | 2026-03-01 |\n")
        r = run_cli(self.tmp)
        self.assertIn("LOG.md: row 3 has 6 cells, expected 7", r.stdout)

    def test_log_row_evidence_cell_untagged(self):
        log = self.tmp / "decisions" / "LOG.md"
        log.write_text(log.read_text() + "| 2026-01-05 | Ship | A. Person | see thread | decided | 2026-03-01 |  |\n")
        r = run_cli(self.tmp)
        self.assertIn("row 3 evidence cell has no tag, link, or Unknown", r.stdout)

    def test_log_row_with_record_link_passes(self):
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(RECORD)
        log = self.tmp / "decisions" / "LOG.md"
        log.write_text(log.read_text() + "| 2026-01-05 | Ship | A. Person | [record](2026-01-05-ship.md) | decided | 2026-03-01 |  |\n")
        r = run_cli(self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_broken_link_fails_cli_warns_hook(self):
        f = self.tmp / "context" / "product.md"
        f.write_text(f.read_text() + "\nSee [missing](../nowhere.md).\n")
        cli = run_cli(self.tmp)
        self.assertEqual(cli.returncode, 1)
        self.assertIn("link does not resolve: ../nowhere.md", cli.stdout)
        hook = run_hook(f)
        self.assertEqual(hook.returncode, 0)
        self.assertIn("link does not resolve", hook.stderr)

    def test_link_in_fenced_code_ignored(self):
        f = self.tmp / "context" / "product.md"
        f.write_text(f.read_text() + "\n```\n[x](../nowhere.md)\n```\n")
        self.assertEqual(run_cli(self.tmp).returncode, 0)

    def test_hook_blocks_untagged_record(self):
        rec = self.tmp / "decisions" / "2026-01-05-ship.md"
        rec.write_text(RECORD.replace("- Prior note  [ingestion/note.md](../ingestion/note.md)", "- untagged"))
        hook = run_hook(rec)
        self.assertEqual(hook.returncode, 2)
        self.assertIn("BLOCKING", hook.stderr)

    def test_placeholder_link_is_not_provenance(self):
        bad = RECORD.replace("[ingestion/note.md](../ingestion/note.md)", "[source/<file>](../source/<file>)")
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(bad)
        self.assertIn("untagged row 2", run_cli(self.tmp).stdout)

    def test_self_link_and_index_link_are_not_provenance(self):
        for target in ("2026-01-05-ship.md", "../INDEX.md", "./"):
            bad = RECORD.replace("[ingestion/note.md](../ingestion/note.md)", f"[x]({target})")
            (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(bad)
            self.assertIn("untagged row 2", run_cli(self.tmp).stdout, target)

    def test_hollow_record_fails(self):
        hollow = "# D\n" + "".join(f"## {h}\n\n" for h in validate.DECISION_HEADINGS)
        (self.tmp / "decisions" / "2026-01-05-hollow.md").write_text(hollow)
        out = run_cli(self.tmp).stdout
        for field in ("Status", "Decider", "Review date"):
            self.assertIn(f"missing value under '## {field}'", out)

    def test_decided_record_needs_evidence(self):
        bad = RECORD.replace("- The buyer asked for it  (stakeholder-verbal, A. Person, 2026-01-04)\n", "").replace(
            "- Prior note  [ingestion/note.md](../ingestion/note.md)\n", "- (none yet)\n")
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(bad)
        self.assertIn("decided record has no evidence row", run_cli(self.tmp).stdout)

    def test_fenced_headings_do_not_count(self):
        fenced = "# D\n```markdown\n" + RECORD + "\n```\n"
        (self.tmp / "decisions" / "2026-01-05-ship.md").write_text(fenced)
        self.assertIn("missing heading '## Status'", run_cli(self.tmp).stdout)

    def test_source_and_host_markdown_not_scanned(self):
        (self.tmp / "source" / "brief.md").write_text("[x](../nowhere.md)\n")
        (self.tmp / "node_modules").mkdir()
        (self.tmp / "node_modules" / "README.md").write_text("[y](./missing.md)\n")
        r = run_cli(self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(run_hook(self.tmp / "source" / "brief.md").returncode, 0)

    def test_hook_outside_instance_exits_zero(self):
        outside = Path(tempfile.mkdtemp()) / "loose.md"
        outside.write_text("- untagged claim\n")
        self.assertEqual(run_hook(outside).returncode, 0)


class NoOverwriteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_preexisting_files_untouched(self):
        (self.tmp / "CLAUDE.md").write_text("mine\n")
        (self.tmp / "notes.md").write_text("notes\n")
        copy_scaffold(self.tmp)
        self.assertEqual((self.tmp / "CLAUDE.md").read_text(), "mine\n")
        self.assertEqual((self.tmp / "notes.md").read_text(), "notes\n")
        self.assertTrue((self.tmp / "INDEX.md").is_file())

    def test_existing_settings_json_untouched(self):
        (self.tmp / ".claude").mkdir()
        existing = self.tmp / ".claude" / "settings.json"
        original = json.dumps({"permissions": {"allow": ["Bash(ls:*)"]}})
        existing.write_text(original)
        copy_scaffold(self.tmp)
        self.assertEqual(existing.read_text(), original)

    def test_cp_rn_form_from_skill_does_not_overwrite(self):
        (self.tmp / "CLAUDE.md").write_text("mine\n")
        # cp -n exits 1 on macOS when it skips an existing file; the copy is still correct.
        subprocess.run(["cp", "-Rn", str(SCAFFOLD) + "/.", str(self.tmp)], capture_output=True)
        self.assertEqual((self.tmp / "CLAUDE.md").read_text(), "mine\n")
        self.assertTrue((self.tmp / ".claude" / "settings.json").is_file())


if __name__ == "__main__":
    unittest.main()
