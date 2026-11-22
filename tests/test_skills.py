import tempfile
import unittest
from pathlib import Path

from repo_checks import REPO, check_skill_shape, parse_frontmatter


def make_skill(root, name, body):
    d = Path(root) / "skills" / name
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(body, encoding="utf-8")


class SkillShape(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_skill_shape(REPO), [])

    def test_missing_description_fails(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "a", "---\nname: a\n---\n# A\n")
            self.assertEqual(check_skill_shape(t), ["skills/a/SKILL.md: description is missing"])

    def test_empty_folded_description_fails(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "a", "---\nname: a\ndescription: >\nversion: 1\n---\n")
            self.assertTrue(check_skill_shape(t))

    def test_missing_name_and_missing_file_and_wrong_name_fail(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "a", "---\ndescription: x\n---\n")
            make_skill(t, "b", "---\nname: other\ndescription: x\n---\n")
            (Path(t) / "skills" / "c").mkdir()
            out = "\n".join(check_skill_shape(t))
            self.assertIn("a/SKILL.md: name is missing", out)
            self.assertIn("name 'other' does not match", out)
            self.assertIn("skills/c: SKILL.md is missing", out)

    def test_both_frontmatter_styles_pass(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "a", '---\nname: a\ndescription: Does a thing.\nmetadata:\n  version: "0.1.0"\n---\n')
            make_skill(t, "b", "---\nname: b\nversion: 0.1.0\ndescription: >\n  Folded\n  text.\nuser-invocable: false\n---\n")
            self.assertEqual(check_skill_shape(t), [])

    def test_release_skill_with_top_level_version_fails(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "a", "---\nname: a\nversion: 0.1.0\ndescription: x\n---\n")
            out = check_skill_shape(t, release_skills=("a",))
            self.assertEqual(len(out), 1)
            self.assertIn("metadata.version", out[0])

    def test_release_skill_without_any_version_fails(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "a", "---\nname: a\ndescription: x\n---\n")
            self.assertEqual(len(check_skill_shape(t, release_skills=("a",))), 1)

    def test_release_skill_with_metadata_version_passes(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "a", '---\nname: a\ndescription: x\nmetadata:\n  version: "0.1.0"\n---\n')
            self.assertEqual(check_skill_shape(t, release_skills=("a",)), [])

    def test_older_skill_with_top_level_version_is_allowed(self):
        with tempfile.TemporaryDirectory() as t:
            make_skill(t, "old", "---\nname: old\nversion: 0.1.0\ndescription: x\n---\n")
            self.assertEqual(check_skill_shape(t, release_skills=()), [])

    def test_release_list_names_real_skills(self):
        from repo_checks import RELEASE_2_SKILLS
        for name in RELEASE_2_SKILLS:
            self.assertTrue((REPO / "skills" / name / "SKILL.md").is_file(), name)

    def test_team_loop_points_at_operator_skills_and_loops(self):
        text = (REPO / "skills" / "team-loop" / "SKILL.md").read_text(encoding="utf-8")
        for name in ("strategy-review", "decision-follow-up", "weekly-metric-review", "data-quality-watch",
                     "agent-eval-regression", "data-product-retro", "analytics-agent", "metric-glossary",
                     "launch-and-adoption", "shipping-bridge"):
            self.assertIn(f"`{name}`", text, name)

    def test_parse_folded_description(self):
        fm = parse_frontmatter("---\nname: x\ndescription: >\n  one\n  two\n---\n")
        self.assertEqual(fm["description"], "one two")


if __name__ == "__main__":
    unittest.main()
