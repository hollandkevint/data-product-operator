import shutil
import tempfile
import unittest
from pathlib import Path

from checks_demo_sync import PAIRS, check_demo_sync
from repo_checks import REPO


class DemoSync(unittest.TestCase):
    def test_repo_copies_match(self):
        self.assertEqual(check_demo_sync(), [])

    def fixture(self):
        t = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, t)
        for copy, orig in PAIRS:
            for d in (copy, orig):
                shutil.copytree(REPO / d, t / d)
        return t

    def test_edited_copy_fails(self):
        t = self.fixture()
        f = t / PAIRS[0][0] / "LOG.md"
        f.write_text(f.read_text() + "\n")
        self.assertIn("LOG.md differs from", "\n".join(check_demo_sync(t)))

    def test_missing_copy_file_fails(self):
        t = self.fixture()
        (t / PAIRS[1][0] / "state.json").unlink()
        self.assertIn("state.json is missing", "\n".join(check_demo_sync(t)))

    def test_extra_copy_file_fails(self):
        t = self.fixture()
        (t / PAIRS[0][0] / "stray.md").write_text("x")
        self.assertIn("stray.md has no original", "\n".join(check_demo_sync(t)))


if __name__ == "__main__":
    unittest.main()
