"""The commit hooks exist, are executable, and block a bad commit."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from repo_checks import REPO

HOOKS = REPO / ".githooks"


def repo_copy(dest):
    shutil.copytree(REPO, dest, ignore=shutil.ignore_patterns(".git", ".data", "__pycache__"))
    for args in (["init", "-q"], ["add", "-A"]):
        subprocess.run(["git", *args], cwd=dest, check=True, capture_output=True)


class Hooks(unittest.TestCase):
    def test_hooks_are_executable(self):
        for name in ("pre-commit", "pre-push"):
            self.assertTrue(os.access(HOOKS / name, os.X_OK), f"{name} is not executable")

    def test_pre_commit_names_real_test_modules(self):
        mods = re.findall(r"\btest_\w+", (HOOKS / "pre-commit").read_text())
        self.assertTrue(mods)
        for m in mods:
            self.assertTrue((REPO / "tests" / f"{m}.py").is_file(), m)

    def run_hook(self, root):
        env = dict(os.environ, PYTHON=sys.executable)
        return subprocess.run([str(Path(root) / ".githooks" / "pre-commit")], cwd=root,
                              env=env, capture_output=True, text=True, timeout=120)

    def test_pre_commit_passes_on_clean_tree_and_blocks_a_banned_word(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "repo"
            repo_copy(root)
            self.assertEqual(self.run_hook(root).returncode, 0)
            bad = root / "skills" / "planted" / "SKILL.md"
            bad.parent.mkdir()
            bad.write_text("We are leveraging the data.\n", encoding="utf-8")
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            p = self.run_hook(root)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("banned word", p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
