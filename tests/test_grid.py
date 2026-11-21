import tempfile
import unittest
from pathlib import Path

from checks_grid import COLUMNS, check_match_grid
from repo_checks import REPO
from test_links import tree

DIAGRAM = ('```mermaid\nflowchart LR\n  A["J1 J2 J3"] --> B["J4 J5 J6"]\n'
           '  B -->|"Team Loop"| A\n  B -->|"strategy review"| C["J7 J8 J9"]\n```\n')
LOCAL_OK = "[a](../skills/a/SKILL.md)"
GOOD = [LOCAL_OK, "gap", "`kh-skill`",
        "[pm-x:y](https://github.com/phuryn/pm-skills)",
        "[ship-check](https://github.com/phuryn/product-engineering)",
        "[pmg-x](https://github.com/polar-bear-org/claude-skills/tree/main/packs/p)",
        "[cmd](https://news.aakashg.com)", "gap",
        "[tdd](https://github.com/mattpocock/skills)"]


def grid(cells=None, jobs=range(1, 10), columns=None, diagram=DIAGRAM, tables_first=False):
    cells = cells or {}
    cols = columns or COLUMNS
    out = ["# Match grid\n"]
    if not tables_first:
        out.append(diagram)
    out.append("| Job | " + " | ".join(cols) + " |")
    out.append("|" + "---|" * (len(cols) + 1))
    for j in jobs:
        row = [cells.get((j, c), GOOD[c]) for c in range(len(GOOD))]
        out.append(f"| J{j}.1 Thing | " + " | ".join(row) + " |")
    if tables_first:
        out.append(diagram)
    return "\n".join(out) + "\n"


def run(**kw):
    with tempfile.TemporaryDirectory() as t:
        tree(t, {"skills/a/SKILL.md": "x\n", "docs/match-grid.md": grid(**kw)})
        return check_match_grid(t)


class MatchGrid(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_match_grid(REPO), [])

    def test_valid_grid_passes(self):
        self.assertEqual(run(), [])

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(len(check_match_grid(t)), 1)

    def test_missing_row_fails(self):
        out = run(jobs=[1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(len(out), 1)
        self.assertIn("row J9 is missing", out[0])

    def test_missing_column_fails(self):
        out = run(columns=COLUMNS[:-1])
        self.assertTrue(any("columns must be exactly" in p for p in out))

    def test_columns_out_of_order_fail(self):
        out = run(columns=[COLUMNS[1], COLUMNS[0]] + COLUMNS[2:])
        self.assertTrue(any("columns must be exactly" in p for p in out))

    def test_empty_cell_fails(self):
        out = run(cells={(3, 2): ""})
        self.assertEqual(len(out), 1)
        self.assertIn("empty cell", out[0])

    def test_link_to_missing_skill_fails(self):
        out = run(cells={(2, 0): "[ghost](../skills/ghost/SKILL.md)"})
        self.assertEqual(len(out), 1)
        self.assertIn("missing skill", out[0])

    def test_local_link_outside_skills_fails(self):
        out = run(cells={(2, 1): "[g](../README.md)"})
        self.assertIn("not a skill in this repo", out[0])

    def test_copied_text_in_90n_cell_fails(self):
        out = run(cells={(1, 5): "[Builds a roadmap with a confidence note](https://github.com/polar-bear-org/claude-skills/x)"})
        self.assertTrue(any("names only" in p for p in out))

    def test_prose_beside_link_in_aakash_cell_fails(self):
        out = run(cells={(1, 6): "[cmd](https://news.aakashg.com) runs a full funnel review"})
        self.assertTrue(any("not a link" in p for p in out))

    def test_outside_link_to_wrong_site_fails(self):
        out = run(cells={(1, 7): "[cmd](https://example.com/x)"})
        self.assertTrue(any("is not under" in p for p in out))

    def test_kh_os_link_fails(self):
        out = run(cells={(1, 2): "[x](https://github.com/hollandkevint/kh-os)"})
        self.assertTrue(any("backticks" in p for p in out))

    def test_wrong_cell_count_fails(self):
        with tempfile.TemporaryDirectory() as t:
            text = grid().replace("| gap | `kh-skill`", "| `kh-skill`", 1)
            tree(t, {"skills/a/SKILL.md": "x\n", "docs/match-grid.md": text})
            self.assertTrue(any("cells, need 9" in p for p in check_match_grid(t)))

    def test_diagram_missing_loop_back_fails(self):
        out = run(diagram=DIAGRAM.replace("strategy review", "later"))
        self.assertTrue(any("strategy review" in p for p in out))

    def test_diagram_below_table_fails(self):
        out = run(tables_first=True)
        self.assertTrue(any("above the table" in p for p in out))

    def test_no_diagram_fails(self):
        out = run(diagram="")
        self.assertTrue(any("no mermaid diagram" in p for p in out))


if __name__ == "__main__":
    unittest.main()
