import tempfile
import unittest
from pathlib import Path

from checks_adapted import check_adapted_sources
from repo_checks import REPO

GOOD = (
    "---\nname: a\nadapted_from: Matt Pocock, mattpocock/skills, grilling\ndescription: x\n---\n"
    "Body.\n\nSource: Matt Pocock, [mattpocock/skills](https://github.com/mattpocock/skills), MIT license.\n"
)


def repo_with(skill_text, name="a"):
    t = tempfile.TemporaryDirectory()
    d = Path(t.name) / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(skill_text, encoding="utf-8")
    return t


class AdaptedSources(unittest.TestCase):
    def check(self, text):
        t = repo_with(text)
        self.addCleanup(t.cleanup)
        return "\n".join(check_adapted_sources(t.name))

    def test_current_repo_passes(self):
        self.assertEqual(check_adapted_sources(REPO), [])

    def test_new_skills_are_marked_adapted(self):
        for name in ("metric-glossary", "data-dictionary-grill"):
            text = (REPO / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("adapted_from: Matt Pocock", text, name)

    def test_good_skill_passes(self):
        self.assertEqual(self.check(GOOD), "")

    def test_dropped_source_line_fails(self):
        self.assertIn("must end with a Source: line", self.check(GOOD.split("\nSource:")[0] + "\n"))

    def test_source_line_not_last_fails(self):
        self.assertIn("must end with a Source: line", self.check(GOOD + "\nFooter.\n"))

    def test_missing_link_fails(self):
        self.assertIn("no link", self.check(GOOD.replace("](https://github.com/mattpocock/skills)", "]")))

    def test_missing_license_fails(self):
        self.assertIn("no cleared license", self.check(GOOD.replace(", MIT license", "")))

    def test_unlisted_license_fails(self):
        self.assertIn("no cleared license", self.check(GOOD.replace("MIT", "GPL-3.0")))

    def test_wrong_author_fails(self):
        self.assertIn("does not start with", self.check(GOOD.replace("Source: Matt Pocock,", "Source: [x](https://a.b),")))

    def test_bare_url_counts_as_link(self):
        self.assertEqual(self.check(GOOD.replace("[mattpocock/skills](https://github.com/mattpocock/skills)", "https://github.com/mattpocock/skills")), "")

    def test_unmarked_adaptation_fails(self):
        text = "---\nname: a\ndescription: x\n---\nBased on Matt Pocock's grill-me skill.\n"
        self.assertIn("no adapted_from frontmatter", self.check(text))


if __name__ == "__main__":
    unittest.main()
