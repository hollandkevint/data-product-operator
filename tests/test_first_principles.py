import tempfile
import unittest

from repo_checks import REPO, check_first_principles, check_no_recheck_markers
from test_links import tree


def page(principles=9, links=True, disagreements=8, label=True, quote_marked=False):
    out = ["# First principles\n"]
    if label:
        out.append("The maturity model is Kevin Holland's synthesis.\n")
    out.append("## The nine principles\n")
    for n in range(1, principles + 1):
        out.append(f"### P{n}. Principle {n}\n")
        out.append("Text.\n")
        out.append("Sources: [A](https://example.com/a)\n" if links else "Sources: A\n")
    out.append("## Where the sources disagree\n")
    out += [f"- Item {i}\n" for i in range(disagreements)]
    mark = " <!-- recheck quote -->" if quote_marked else ""
    out.append(f'## Credits\n\nHe wrote "this is a long enough quote here" once.{mark}\n')
    return "\n".join(out)


def run(**kw):
    with tempfile.TemporaryDirectory() as t:
        tree(t, {"docs/first-principles.md": page(**kw)})
        return check_first_principles(t)


class FirstPrinciples(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_first_principles(REPO), [])

    def test_good_page_passes(self):
        self.assertEqual(run(), [])

    def test_missing_page_fails(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(len(check_first_principles(t)), 1)

    def test_eight_principles_fail(self):
        self.assertTrue(any("9 principles" in p for p in run(principles=8)))

    def test_principle_without_link_fails(self):
        self.assertTrue(any("P1" in p and "link" in p for p in run(links=False)))

    def test_too_few_disagreements_fail(self):
        self.assertTrue(any("disagree" in p for p in run(disagreements=3)))

    def test_missing_synthesis_label_fails(self):
        self.assertTrue(any("synthesis" in p for p in run(label=False)))

    def test_leftover_recheck_marker_fails(self):
        self.assertTrue(any("recheck" in p for p in run(quote_marked=True)))

    def test_marker_in_readme_fails(self):
        with tempfile.TemporaryDirectory() as t:
            tree(t, {"README.md": 'He said "a long enough quote here". <!-- recheck quote -->\n'})
            self.assertEqual(len(check_no_recheck_markers(t)), 1)

    def test_verified_quote_passes(self):
        self.assertEqual(run(quote_marked=False), [])


if __name__ == "__main__":
    unittest.main()
