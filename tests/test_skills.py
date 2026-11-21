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

    def test_parse_folded_description(self):
        fm = parse_frontmatter("---\nname: x\ndescription: >\n  one\n  two\n---\n")
        self.assertEqual(fm["description"], "one two")


if __name__ == "__main__":
    unittest.main()
