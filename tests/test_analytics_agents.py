import tempfile
import unittest
from pathlib import Path

from checks_analytics_agents import check_skill_points_at_pages, check_vendor_banners
from repo_checks import REPO

BANNER = "> **As of 2026-11-21. Check vendor docs before you rely on this.**\n"


def make(root, files):
    for rel, body in files.items():
        p = Path(root) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")


def run(body):
    with tempfile.TemporaryDirectory() as t:
        make(t, {"docs/analytics-agents/a.md": body})
        return check_vendor_banners(t)


class VendorBanners(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_vendor_banners(REPO), [])

    def test_current_repo_has_the_three_routes(self):
        names = {p.name for p in (REPO / "docs" / "analytics-agents").glob("*.md")}
        for n in ("reference-architecture.md", "warehouse-native.md", "build-your-own.md",
                  "open-source-and-bi-native.md"):
            self.assertIn(n, names)

    def test_vendor_page_with_banner_passes(self):
        self.assertEqual(run("# T\n\n" + BANNER + "\nUse Snowflake.\n"), [])

    def test_vendor_page_without_banner_fails(self):
        self.assertEqual(len(run("# T\n\nUse Snowflake.\n")), 1)

    def test_banner_without_date_fails(self):
        self.assertTrue(run("# T\n\n> Check vendor docs.\n\nUse dbt.\n"))

    def test_banner_with_impossible_date_fails(self):
        self.assertTrue(run("# T\n\n> As of 2026-13-45. Check vendor docs.\n\nUse dbt.\n"))

    def test_banner_without_check_docs_line_fails(self):
        self.assertTrue(run("# T\n\n> As of 2026-11-21.\n\nUse dbt.\n"))

    def test_banner_buried_below_the_top_fails(self):
        self.assertTrue(run("# T\n" + "\nfiller\n" * 20 + BANNER + "Use Hex.\n"))

    def test_vendor_neutral_page_needs_no_banner(self):
        self.assertEqual(run("# T\n\nThe agent reads the semantic layer.\n"), [])

    def test_vendor_only_in_link_target_does_not_count(self):
        self.assertEqual(run("# T\n\nSee [the docs](https://docs.snowflake.com/x).\n"), [])

    def test_removing_banner_from_a_real_page_fails(self):
        real = (REPO / "docs/analytics-agents/warehouse-native.md").read_text(encoding="utf-8")
        stripped = "\n".join(l for l in real.splitlines() if "As of" not in l)
        self.assertTrue(run(stripped))

    def test_missing_folder_fails(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(len(check_vendor_banners(t)), 1)


class SkillPointsAtPages(unittest.TestCase):
    def test_current_repo_passes(self):
        self.assertEqual(check_skill_points_at_pages(REPO), [])

    def test_unlinked_page_fails(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, {"docs/analytics-agents/a.md": "x", "skills/analytics-agent/SKILL.md":
                     "see team-loop/grader/ only"})
            self.assertEqual(len(check_skill_points_at_pages(t)), 1)

    def test_missing_grader_pointer_fails(self):
        with tempfile.TemporaryDirectory() as t:
            make(t, {"skills/analytics-agent/SKILL.md": "nothing"})
            self.assertEqual(len(check_skill_points_at_pages(t)), 1)


if __name__ == "__main__":
    unittest.main()
