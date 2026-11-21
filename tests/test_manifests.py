import json
import tempfile
import unittest
from pathlib import Path

from repo_checks import REPO, check_manifests


def write(root, plugin_v="1.0.0", market_v="1.0.0"):
    d = Path(root) / ".claude-plugin"
    d.mkdir(parents=True, exist_ok=True)
    (d / "plugin.json").write_text(json.dumps({"name": "p", "description": "d", "version": plugin_v}))
    (d / "marketplace.json").write_text(json.dumps(
        {"metadata": {"version": market_v}, "plugins": [{"name": "p"}]}))


class Manifests(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_manifests(REPO), [])

    def test_matching_versions_pass(self):
        with tempfile.TemporaryDirectory() as t:
            write(t)
            self.assertEqual(check_manifests(t), [])

    def test_version_drift_fails(self):
        with tempfile.TemporaryDirectory() as t:
            write(t, plugin_v="2.0.0", market_v="1.3.0")
            self.assertIn("disagree", "\n".join(check_manifests(t)))

    def test_non_semver_fails(self):
        with tempfile.TemporaryDirectory() as t:
            write(t, plugin_v="v2", market_v="v2")
            self.assertIn("not semver", "\n".join(check_manifests(t)))

    def test_missing_or_bad_json_fails(self):
        with tempfile.TemporaryDirectory() as t:
            write(t)
            (Path(t) / ".claude-plugin" / "plugin.json").write_text("{")
            (Path(t) / ".claude-plugin" / "marketplace.json").unlink()
            out = "\n".join(check_manifests(t))
            self.assertIn("invalid JSON", out)
            self.assertIn("marketplace.json: file is missing", out)


if __name__ == "__main__":
    unittest.main()
