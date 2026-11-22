import tempfile
import unittest
from pathlib import Path

from repo_checks import REPO, avoid_terms, check_glossary_shape, check_glossary_use
from test_links import tree

GLOSSARY = (
    "# Glossary\n\n"
    "**Data product**:\nA thing with a consumer.\n_Avoid_: Dashboard, squad, \"front end\", Data owner (as a title)\n"
)


class GlossaryShape(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_glossary_shape(REPO), [])

    def test_entry_without_avoid_line_fails(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"GLOSSARY.md": "**Term**:\nA definition.\n\n**Other**:\nText.\n_Avoid_: x\n"})
            out = check_glossary_shape(t)
            self.assertEqual(len(out), 1)
            self.assertIn("Term", out[0])

    def test_missing_glossary_fails(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(len(check_glossary_shape(t)), 1)


class AvoidTerms(unittest.TestCase):
    def test_plain_terms_are_listed_and_qualified_ones_skipped(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"GLOSSARY.md": GLOSSARY})
            self.assertEqual(avoid_terms(t), ["Dashboard", "squad", "front end"])


class GlossaryUse(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_glossary_use(REPO), [])

    def run_check(self, files):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"GLOSSARY.md": GLOSSARY, **files})
            return check_glossary_use(t, allowed={})

    def test_unquoted_avoid_term_in_docs_fails(self):
        out = self.run_check({"docs/a.md": "Ask the squad first.\n"})
        self.assertEqual(len(out), 1)
        self.assertIn("docs/a.md:1", out[0])
        self.assertIn("squad", out[0])

    def test_unquoted_avoid_term_in_readme_fails(self):
        self.assertEqual(len(self.run_check({"README.md": "The Front End is late.\n"})), 1)

    def test_quoted_code_and_link_targets_pass(self):
        out = self.run_check({
            "README.md": 'Say "squad" or `squad` or [guide](docs/squad.md) or https://x.io/squad\n'
                         "```\nsquad\n```\n<!-- squad -->\n",
        })
        self.assertEqual(out, [])

    def test_whole_words_only(self):
        self.assertEqual(self.run_check({"docs/a.md": "A squadron flew.\n"}), [])

    def test_allowance_is_honoured(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"GLOSSARY.md": GLOSSARY, "docs/a.md": "A dashboard.\n"})
            self.assertEqual(len(check_glossary_use(t, allowed={})), 1)
            self.assertEqual(check_glossary_use(t, allowed={"dashboard": "generic noun"}), [])

    def test_skills_and_team_loop_are_checked(self):
        for path in ("skills/x/SKILL.md", "team-loop/README.md", "skills/team-loop/scaffold/CLAUDE.md"):
            with self.subTest(path=path):
                self.assertEqual(len(self.run_check({path: "squad\n"})), 1)

    def test_planted_dpm_os_in_a_skill_fails(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"GLOSSARY.md": (REPO / "GLOSSARY.md").read_text(encoding="utf-8"),
                     "skills/x/SKILL.md": "Initialize a DPM OS here.\n"})
            out = check_glossary_use(t)
            self.assertEqual(len(out), 1)
            self.assertIn("DPM OS", out[0])

    def test_plural_of_an_avoid_term_fails(self):
        self.assertEqual(len(self.run_check({"docs/a.md": "Two squads ship.\n"})), 1)

    def test_root_claude_md_is_checked(self):
        self.assertEqual(len(self.run_check({"CLAUDE.md": "Ask the squad.\n"})), 1)

    def test_other_folders_are_not_checked(self):
        self.assertEqual(self.run_check({"tests/x.md": "squad\n"}), [])


if __name__ == "__main__":
    unittest.main()
