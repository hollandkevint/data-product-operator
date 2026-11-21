import shutil
import tempfile
import unittest
from pathlib import Path

from checks_launch import REQUIRED, check_launch_outputs
from repo_checks import REPO


def copy_skills(tmp):
    for name in REQUIRED:
        shutil.copytree(REPO / "skills" / name, Path(tmp) / "skills" / name)
    return tmp


class LaunchOutputs(unittest.TestCase):
    def test_repo_passes(self):
        self.assertEqual(check_launch_outputs(REPO), [])

    def test_removing_each_field_fails(self):
        for name, fields in REQUIRED.items():
            for field in fields:
                with tempfile.TemporaryDirectory() as t:
                    copy_skills(t)
                    p = Path(t) / "skills" / name / "SKILL.md"
                    text = p.read_text(encoding="utf-8")
                    token = f"**{field}:**"
                    out = text.index("\n## Output")
                    head, tail = text[:out], text[out:]
                    p.write_text(head + tail.replace(token, "**x:**", 1), encoding="utf-8")
                    problems = check_launch_outputs(t)
                    self.assertTrue(any(f"'{field}'" in s for s in problems), (name, field))

    def test_missing_output_section_fails(self):
        with tempfile.TemporaryDirectory() as t:
            copy_skills(t)
            p = Path(t) / "skills" / "shipping-bridge" / "SKILL.md"
            p.write_text(p.read_text(encoding="utf-8").replace("## Output", "## Result"), encoding="utf-8")
            self.assertTrue(any("no '## Output'" in s for s in check_launch_outputs(t)))


if __name__ == "__main__":
    unittest.main()
