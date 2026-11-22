import tempfile
import unittest

from checks_voice import banned_words, check_banned_words
from repo_checks import REPO
from test_links import tree

CLAUDE = 'NEVER use: leverage, utilize, robust, "drive insights", or Gartner-speak.\n'


class BannedWords(unittest.TestCase):
    def test_list_comes_from_claude_md_bare_words_only(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"CLAUDE.md": CLAUDE})
            self.assertEqual(banned_words(t), ["leverage", "utilize", "robust"])

    def test_verb_forms_and_hyphenated_uses_fail(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"CLAUDE.md": CLAUDE,
                     "skills/x/SKILL.md": "We are leveraging it.\nThe highest-leverage move.\nA robust plan.\n"})
            self.assertEqual(len(check_banned_words(t)), 3)

    def test_domain_noun_utilization_and_code_pass(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"CLAUDE.md": CLAUDE,
                     "docs/a.md": "Inpatient utilization by period.\n`leverage` in code.\n"})
            self.assertEqual(check_banned_words(t), [])

    def test_claude_md_itself_is_out_of_scope(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"CLAUDE.md": CLAUDE})
            self.assertEqual(check_banned_words(t), [])

    def test_current_repo_passes(self):
        self.assertEqual(check_banned_words(REPO), [])


if __name__ == "__main__":
    unittest.main()
