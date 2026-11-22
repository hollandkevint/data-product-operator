import json
import shutil
import tempfile
import unittest
from pathlib import Path

from checks_release import (
    VERSION,
    AUDIENCE,
    MOVED,
    NOTES,
    check_example_packet,
    check_readme_order,
    check_release_manifests,
    check_release_notes,
)
from repo_checks import REPO


def copy_of(paths):
    """A temp repo with the named files and folders copied from this repo."""
    t = tempfile.TemporaryDirectory()
    for p in paths:
        src, dst = REPO / p, Path(t.name) / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy(src, dst)
    return t


class ReleaseManifests(unittest.TestCase):
    def mutate(self, name, fn):
        t = copy_of([".claude-plugin"])
        self.addCleanup(t.cleanup)
        p = Path(t.name) / ".claude-plugin" / name
        data = json.loads(p.read_text())
        fn(data)
        p.write_text(json.dumps(data))
        return "\n".join(check_release_manifests(t.name))

    def test_current_repo_passes(self):
        self.assertEqual(check_release_manifests(REPO), [])

    def test_old_version_fails(self):
        out = self.mutate("plugin.json", lambda d: d.update(version="1.3.0"))
        self.assertIn(VERSION, out)

    def test_old_audience_fails(self):
        out = self.mutate("marketplace.json", lambda d: d["plugins"][0].update(description="For data product managers."))
        self.assertIn(AUDIENCE, out)

    def test_missing_keyword_fails(self):
        out = self.mutate("plugin.json", lambda d: d["keywords"].remove("data-mesh"))
        self.assertIn("data-mesh", out)


class ReadmeOrder(unittest.TestCase):
    def run_on(self, text):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        (Path(t.name) / "README.md").write_text(text, encoding="utf-8")
        return "\n".join(check_readme_order(t.name))

    def test_current_repo_passes(self):
        self.assertEqual(check_readme_order(REPO), [])

    def test_missing_promise_fails(self):
        text = (REPO / "README.md").read_text(encoding="utf-8").replace("Decisions, not dashboards", "Hello")
        self.assertIn("Decisions, not dashboards", self.run_on(text))

    def test_swapped_sections_fail(self):
        text = (REPO / "README.md").read_text(encoding="utf-8")
        head, rest = text.split("## Quick start", 1)
        quick, after = rest.split("## Example", 1)
        swapped = head + "## Example" + after.split("## Match grid", 1)[0] + "## Quick start" + quick + "## Match grid" + after.split("## Match grid", 1)[1]
        self.assertIn("out of order", self.run_on(swapped))


class ExamplePacket(unittest.TestCase):
    def run_on(self, mutate):
        t = copy_of(["README.md", "skills/team-loop/scaffold"])
        self.addCleanup(t.cleanup)
        p = Path(t.name) / "README.md"
        p.write_text(mutate(p.read_text(encoding="utf-8")), encoding="utf-8")
        return "\n".join(check_example_packet(t.name))

    def test_current_repo_passes(self):
        self.assertEqual(check_example_packet(REPO), [])

    def test_dropped_template_heading_fails(self):
        out = self.run_on(lambda s: s.replace("## Reviewer note", "## Notes"))
        self.assertIn("Reviewer note", out)

    def test_leftover_placeholder_fails(self):
        out = self.run_on(lambda s: s.replace("owner: Priya Patel", "owner: <working owner>"))
        self.assertIn("placeholder", out)

    def test_broken_link_fails_the_validator(self):
        out = self.run_on(lambda s: s.replace("## Changed evidence\n", "## Changed evidence\n\nSee [record](../decisions/gone.md).\n", 1))
        self.assertIn("link does not resolve", out)


class ReleaseNotes(unittest.TestCase):
    def run_on(self, mutate):
        t = copy_of([NOTES] + sorted({new.rstrip("/") for _, new in MOVED}))
        self.addCleanup(t.cleanup)
        p = Path(t.name) / NOTES
        p.write_text(mutate(p.read_text(encoding="utf-8")), encoding="utf-8")
        return "\n".join(check_release_notes(t.name))

    def test_current_repo_passes(self):
        self.assertEqual(check_release_notes(REPO), [])

    def test_missing_moved_path_fails(self):
        out = self.run_on(lambda s: s.replace("`grader/`", "`the grader`"))
        self.assertIn("grader/", out)

    def test_missing_section_fails(self):
        out = self.run_on(lambda s: s.replace("## Upgrade", "## Later"))
        self.assertIn("Upgrade", out)

    def test_new_path_that_does_not_exist_fails(self):
        t = copy_of([NOTES])
        self.addCleanup(t.cleanup)
        self.assertIn("does not exist", "\n".join(check_release_notes(t.name)))


if __name__ == "__main__":
    unittest.main()
