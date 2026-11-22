"""Helpers shared by the loop checkers (skills/*/check.py). Stdlib only.

Each check.py adds the repo's lib/ folder to sys.path and imports from here.
The plugin installs the whole repo, so the path holds after install.
See docs/loop-pattern.md.
"""
import json
import re
from datetime import date
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def parse_date(text):
    """Return a date for a strict YYYY-MM-DD string, else None. Never raises.

    The strictest copy wins: str() so a non-string (a JSON number or null) returns
    None instead of crashing, and a YYYY-MM-DD shape check so Python 3.11+ does not
    accept compact or week forms (20261121, 2026-W47-1) that 3.10 rejects.
    """
    text = str(text).strip()
    if not ISO_DATE.fullmatch(text):
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def table_rows(text, header_start):
    """Return rows (list of cell lists) of the first table whose header starts with header_start."""
    rows, in_table = [], False
    for line in text.splitlines():
        line = line.strip()
        if not in_table:
            in_table = line.startswith("|") and line.lstrip("| ").startswith(header_start)
            continue
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def read_log(root, problems, build):
    """Read decisions/LOG.md. build(cells, record) returns one entry; record is the linked file name or None."""
    path = root / "decisions" / "LOG.md"
    if not path.exists():
        problems.append("decisions/LOG.md is missing")
        return []
    out = []
    for cells in table_rows(path.read_text(encoding="utf-8"), "Date"):
        if len(cells) != 7:
            problems.append(f"decisions/LOG.md: row has {len(cells)} cells, expected 7: {cells[:2]}")
            continue
        link = LINK.search(cells[3])
        out.append(build(cells, Path(link.group(1)).name if link else None))
    return out


def load_json(path, problems, label):
    if not path.exists():
        problems.append(f"{label} is missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        problems.append(f"{label} is not valid JSON: {e}")
        return None


def line_value(text, label):
    m = re.search(rf"^{label}:\s*(.*?)\s*$", text, re.M)
    return m.group(1) if m else None


def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)
