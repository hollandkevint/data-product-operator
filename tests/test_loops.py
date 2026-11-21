import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from checks_loops import check_loops, discover_loops
from repo_checks import REPO

LOOP = REPO / "skills" / "decision-follow-up"


def load_checker():
    spec = importlib.util.spec_from_file_location("decision_follow_up_check", LOOP / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def copy_loop(tmp, mutate=None):
    """Copy the real loop into a temp repo root, then let `mutate(loop_dir)` break it."""
    dest = Path(tmp) / "skills" / "decision-follow-up"
    shutil.copytree(LOOP, dest)
    if mutate:
        mutate(dest)
    return tmp


def rewrite(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, f"fixture setup: {old!r} not in {path}"
    path.write_text(text.replace(old, new), encoding="utf-8")


class LoopCheck(unittest.TestCase):
    def test_every_loop_in_repo_passes(self):
        self.assertTrue(discover_loops(REPO), "no loops found")
        self.assertEqual(check_loops(REPO), [])

    def test_checker_that_accepts_everything_fails(self):
        def lax(d):
            (d / "check.py").write_text("import sys\nsys.exit(0)\n")
        with tempfile.TemporaryDirectory() as t:
            out = "\n".join(check_loops(copy_loop(t, lax)))
            self.assertIn("accepts a broken copy", out)

    def test_checker_that_rejects_the_demo_fails(self):
        def strict(d):
            (d / "check.py").write_text("import sys\nprint('no')\nsys.exit(1)\n")
        with tempfile.TemporaryDirectory() as t:
            self.assertIn("rejects its own demo", "\n".join(check_loops(copy_loop(t, strict))))

    def test_break_that_changes_nothing_fails(self):
        def noop(d):
            m = json.loads((d / "loop.json").read_text())
            m["breaks"][0]["find"] = "text that is not in the file"
            (d / "loop.json").write_text(json.dumps(m))
        with tempfile.TemporaryDirectory() as t:
            self.assertIn("finds nothing to change", "\n".join(check_loops(copy_loop(t, noop))))

    def test_missing_demo_checker_and_headings_fail(self):
        def strip(d):
            shutil.rmtree(d / "demo")
            (d / "check.py").unlink()
            rewrite(d / "SKILL.md", "## State", "## Notes")
        with tempfile.TemporaryDirectory() as t:
            out = "\n".join(check_loops(copy_loop(t, strip)))
            self.assertIn("checker check.py is missing", out)
            self.assertIn("demo folder demo is missing", out)
            self.assertIn("heading '## State' is missing", out)


class DecisionFollowUpChecker(unittest.TestCase):
    """Each rule in the checker fails on the bug it guards."""

    def problems(self, mutate=None):
        c = load_checker()
        with tempfile.TemporaryDirectory() as t:
            ws = Path(t) / "ws"
            shutil.copytree(LOOP / "demo", ws)
            if mutate:
                mutate(ws)
            return "\n".join(c.check(ws))

    def out(self, ws):
        return ws / "loops" / "decision-follow-up" / "2026-11-21.md"

    def test_demo_is_clean(self):
        self.assertEqual(self.problems(), "")

    def test_keep_without_evidence_fails(self):
        p = self.problems(lambda ws: rewrite(self.out(ws), "`(stakeholder-verbal, Ana Reyes, 2026-09-16)`", "Unknown"))
        self.assertIn("needs observed outcome evidence", p)

    def test_open_decision_without_future_date_fails(self):
        p = self.problems(lambda ws: rewrite(self.out(ws), "Review again 2026-12-04.", "Review again soon."))
        self.assertIn("needs a next review date", p)

    def test_reverse_condition_drift_fails(self):
        p = self.problems(lambda ws: rewrite(self.out(ws), "Two or more consumers", "One consumer"))
        self.assertIn("reverse condition does not match", p)

    def test_pending_decision_followed_up_fails(self):
        p = self.problems(lambda ws: rewrite(ws / "decisions" / "LOG.md", "decided | 2026-09-15", "pending | 2026-09-15"))
        self.assertIn("must not be followed up", p)

    def test_missing_due_decision_fails(self):
        p = self.problems(lambda ws: rewrite(ws / "decisions" / "LOG.md", "2027-01-15", "2026-11-15"))
        self.assertIn("due for follow-up but missing", p)

    def test_invented_decision_fails(self):
        p = self.problems(lambda ws: rewrite(self.out(ws), "2026-08-04-friday-refresh.md", "2026-08-04-made-up.md"))
        self.assertIn("invented decision", p)

    def test_state_drift_fails(self):
        p = self.problems(lambda ws: rewrite(ws / "loops" / "decision-follow-up" / "state.json",
                                             '"2026-09-01-retire-lag-export.md"\n  ]\n}', '"2026-08-04-friday-refresh.md"\n  ]\n}'))
        self.assertIn("state.json: open does not match", p)

    def test_bad_evidence_tag_fails(self):
        p = self.problems(lambda ws: rewrite(self.out(ws), "`(stakeholder-verbal, Ana Reyes, 2026-09-16)`", "`(vibes)`"))
        self.assertIn("not a provenance tag", p)


if __name__ == "__main__":
    unittest.main()
