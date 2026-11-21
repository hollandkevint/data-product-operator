"""Checks for docs/analytics-agents/.

A page that names a vendor must open with an as-of banner: a date and a
reminder to check vendor docs. Vendor pages go stale fast, so the date
tells a reader how far to trust the page.
"""
import datetime
import re
from pathlib import Path

PAGES_DIR = "docs/analytics-agents"
BANNER_WINDOW = 12  # the banner must sit in the first lines of the page
AS_OF = re.compile(r"as of (\d{4}-\d{2}-\d{2})", re.I)
CHECK_DOCS = re.compile(r"check vendor docs", re.I)

# Vendor and product names. Add a name here when a page starts to cover it.
VENDORS = [
    "Snowflake", "Cortex", "Databricks", "Genie", "Agent Bricks", "Unity Catalog",
    "BigQuery", "Looker", "LookML", "Google Cloud", "dbt", "MetricFlow", "MotherDuck",
    "DuckDB", "nao", "Hex", "Claude Agent SDK", "Anthropic",
]
VENDOR = re.compile(r"(?<![\w-])(" + "|".join(re.escape(v) for v in VENDORS) + r")(?![\w-])", re.I)


def pages(root):
    return sorted((Path(root) / PAGES_DIR).glob("*.md"))


def check_vendor_banners(root):
    """Every page under docs/analytics-agents/ that names a vendor carries a dated banner."""
    root = Path(root)
    if not (root / PAGES_DIR).is_dir():
        return [f"{PAGES_DIR}: folder is missing"]
    problems = []
    for md in pages(root):
        rel = md.relative_to(root)
        text = md.read_text(encoding="utf-8")
        # Inline code and link targets do not count as naming a vendor.
        prose = re.sub(r"\]\([^)]*\)|`[^`]*`", "", text)
        vendors = sorted({m.group(1).lower() for m in VENDOR.finditer(prose)})
        if not vendors:
            continue
        head = "\n".join(text.splitlines()[:BANNER_WINDOW])
        m = AS_OF.search(head)
        if not m:
            problems.append(f"{rel}: names {', '.join(vendors)} but has no 'As of YYYY-MM-DD' banner near the top")
            continue
        try:
            datetime.date.fromisoformat(m.group(1))
        except ValueError:
            problems.append(f"{rel}: banner date '{m.group(1)}' is not a real date")
        if not CHECK_DOCS.search(head):
            problems.append(f"{rel}: banner does not say 'check vendor docs'")
    return problems


def check_skill_points_at_pages(root):
    """The skill links every page in docs/analytics-agents/ and the grader it uses as its example."""
    root = Path(root)
    skill = root / "skills" / "analytics-agent" / "SKILL.md"
    if not skill.is_file():
        return ["skills/analytics-agent/SKILL.md: file is missing"]
    text = skill.read_text(encoding="utf-8")
    problems = [f"skills/analytics-agent/SKILL.md: does not link {PAGES_DIR}/{p.name}"
                for p in pages(root) if f"{PAGES_DIR}/{p.name}" not in text]
    if "team-loop/grader/" not in text:
        problems.append("skills/analytics-agent/SKILL.md: does not point at team-loop/grader/")
    return problems
