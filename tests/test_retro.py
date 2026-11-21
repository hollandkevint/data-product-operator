import tempfile
import unittest
from pathlib import Path

from checks_retro import RETRO, check_retro
from repo_checks import REPO


def repo_with(text):
    t = tempfile.TemporaryDirectory()
    p = Path(t.name) / RETRO
    p.parent.mkdir(parents=True)
    p.write_text(text, encoding="utf-8")
    return t


class Retro(unittest.TestCase):
    def check(self, mutate):
        text = (REPO / RETRO).read_text(encoding="utf-8")
        t = repo_with(mutate(text))
        self.addCleanup(t.cleanup)
        return "\n".join(check_retro(t.name))

    def test_current_repo_passes(self):
        self.assertEqual(check_retro(REPO), [])

    def test_dropped_decision_question_fails(self):
        out = self.check(lambda s: s.replace("- **Did the decision change?** One line", "- **Status:** One line"))
        self.assertIn("Did the decision change?", out)

    def test_dropped_data_question_fails(self):
        out = self.check(lambda s: s.replace("- **Did the data hold up?** One line", "- **Data:** One line"))
        self.assertIn("Did the data hold up?", out)

    def test_actions_not_tied_to_log_fails(self):
        out = self.check(lambda s: s.replace("- **Actions tied to the decision log:**", "- **Actions:**"))
        self.assertIn("Actions tied to the decision log", out)

    def test_log_path_dropped_from_output_fails(self):
        out = self.check(lambda s: s.split("## Output")[0] + "## Output\n\n- **Did the decision change?** x\n- **Did the data hold up?** x\n- **Actions tied to the decision log:** x\n")
        self.assertIn("decisions/LOG.md", out)

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIn("file is missing", "\n".join(check_retro(d)))


if __name__ == "__main__":
    unittest.main()
