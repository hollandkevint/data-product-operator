"""Grid-integrity check for docs/match-grid.md.

The grid has nine jobs (J1 to J9) and nine source columns in a fixed order.
Each cell is a link to a skill in this repo, an outside skill name with a link
to its pack, or the word "gap". See docs/match-grid.md.
"""
import re
from pathlib import Path

GRID_PATH = "docs/match-grid.md"
COLUMNS = ["Data Product Operator", "Team Loop", "kh-os", "Pawel pm-skills",
           "Pawel product-engineering", "90n PM guide", "Aakash PM-OS",
           "Aakash loops and graphs", "Matt Pocock"]
JOBS = [f"J{n}" for n in range(1, 10)]
LOCAL = (0, 1)
PRIVATE = 2  # kh-os is a private repo: skill names in backticks, no links
EXTERNAL_PREFIX = {
    3: "https://github.com/phuryn/pm-skills",
    4: "https://github.com/phuryn/product-engineering",
    5: "https://github.com/polar-bear-org/claude-skills/",
    6: "https://news.aakashg.com",
    7: "https://news.aakashg.com",
    8: "https://github.com/mattpocock/skills",
}
LINK = re.compile(r"^\[([^\]]+)\]\(([^)\s]+)\)$")
NAME = re.compile(r"^[A-Za-z0-9_.:\-]+$")  # one token: a skill name, never prose
TICKED = re.compile(r"^`([A-Za-z0-9_.:\-]+)`$")
ROW_LABEL = re.compile(r"^(J[1-9])(\.\d+)?\s+\S")
NOTE = re.compile(r"^-\s+(J[1-9]\.\d+)\s*/\s*([^:]+):\s*(\S.*)$")
FENCE = re.compile(r"^```(\w*)\s*$")


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _split(text):
    """Return (mermaid blocks with their line numbers, table lines with line numbers)."""
    mermaid, tables, block, lang = [], [], None, None
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line)
        if m and block is None:
            block, lang = [], m.group(1)
            start = n
        elif m and block is not None:
            if lang == "mermaid":
                mermaid.append((start, "\n".join(block)))
            block = None
        elif block is not None:
            block.append(line)
        elif line.lstrip().startswith("|"):
            tables.append((n, line))
    return mermaid, tables


def _check_cell(col, text, where, root, page_dir):
    if not text:
        return [f"{where}: empty cell"]
    if text.lower() == "gap":
        return [] if text == "gap" else [f"{where}: write 'gap' in lower case"]
    problems = []
    for part in text.split("<br>"):
        part = part.strip()
        if col == PRIVATE:
            if not TICKED.match(part):
                problems.append(f"{where}: kh-os cell must be skill names in backticks, got '{part}'")
            continue
        m = LINK.match(part)
        if not m:
            problems.append(f"{where}: '{part}' is not a link or 'gap'")
            continue
        name, url = m.groups()
        if col in LOCAL:
            target = (page_dir / url.split("#")[0]).resolve()
            roots = [(Path(root) / d).resolve() for d in ("skills", "docs")]
            if not any(r in target.parents for r in roots):
                problems.append(f"{where}: '{url}' is not a skill or doc in this repo")
            elif not target.is_file():
                problems.append(f"{where}: link to missing skill or doc '{url}'")
        else:
            if not NAME.match(name):
                problems.append(f"{where}: outside cell holds '{name}', names only")
            if not url.startswith(EXTERNAL_PREFIX[col]):
                problems.append(f"{where}: '{url}' is not under {EXTERNAL_PREFIX[col]}")
    return problems


def check_match_grid(root):
    page = Path(root) / GRID_PATH
    if not page.is_file():
        return [f"{GRID_PATH}: file is missing"]
    text = page.read_text(encoding="utf-8")
    mermaid, table_lines = _split(text)
    problems = []

    if not mermaid:
        problems.append(f"{GRID_PATH}: no mermaid diagram of the cycle")
    else:
        line, body = mermaid[0]
        for job in JOBS:
            if not re.search(rf"\b{job}\b", body):
                problems.append(f"{GRID_PATH}: cycle diagram does not show {job}")
        for needed in ("Team Loop", "strategy review"):
            if needed not in body:
                problems.append(f"{GRID_PATH}: cycle diagram has no '{needed}' loop-back")
        first_table = table_lines[0][0] if table_lines else None
        if first_table is not None and line > first_table:
            problems.append(f"{GRID_PATH}: cycle diagram must come above the table")

    seen_jobs, headers, gaps = set(), 0, set()
    page_dir = page.parent
    for n, line in table_lines:
        cells = _cells(line)
        if cells and cells[0] == "Job":
            headers += 1
            if cells[1:] != COLUMNS:
                problems.append(f"{GRID_PATH}:{n}: columns must be exactly {COLUMNS} in this order")
            continue
        if set("".join(cells)) <= set("-: "):
            continue  # separator row
        label = ROW_LABEL.match(cells[0])
        if not label:
            problems.append(f"{GRID_PATH}:{n}: row label '{cells[0]}' does not start with J1 to J9")
            continue
        seen_jobs.add(label.group(1))
        if len(cells) != len(COLUMNS) + 1:
            problems.append(f"{GRID_PATH}:{n}: {cells[0]} has {len(cells) - 1} cells, need {len(COLUMNS)}")
            continue
        for col, cell in enumerate(cells[1:]):
            if cell == "gap" and col in LOCAL:
                gaps.add((cells[0].split()[0], COLUMNS[col]))
            problems += _check_cell(col, cell, f"{GRID_PATH}:{n}: {cells[0]} / {COLUMNS[col]}", root, page_dir)
    if headers == 0:
        problems.append(f"{GRID_PATH}: no grid table found")
    for job in JOBS:
        if job not in seen_jobs:
            problems.append(f"{GRID_PATH}: row {job} is missing")
    problems += _check_notes(text, gaps)
    return problems


def _check_notes(text, gaps):
    """Every gap in this repo's two columns needs one note line; no note may be stale."""
    out, notes, in_section = [], set(), False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line.strip() == "## Gap notes"
        elif in_section and line.startswith("-"):
            m = NOTE.match(line)
            if m:
                notes.add((m.group(1), m.group(2).strip()))
            else:
                out.append(f"{GRID_PATH}: gap note '{line[:40]}' must read '- J1.1 / Column: reason'")
    for job, col in sorted(gaps - notes):
        out.append(f"{GRID_PATH}: {job} / {col} is a gap with no line under 'Gap notes'")
    for job, col in sorted(notes - gaps):
        out.append(f"{GRID_PATH}: note for {job} / {col} but that cell is not a gap")
    return out
