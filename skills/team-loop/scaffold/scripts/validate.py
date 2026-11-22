#!/usr/bin/env python3
"""Team loop workspace validator.

CLI mode:   python3 scripts/validate.py <instance-dir>
            exit 0 on pass, 1 on any finding, one line per finding.
Hook mode:  no argument, Claude Code PostToolUse JSON on stdin.
            Validates the written file only. Exit 2 on a blocking finding
            (missing decision heading, bad status, untagged evidence row,
            malformed log row), exit 0 with a stderr warning on a broken link
            or an untagged populated context file.
Manifest:   python3 scripts/validate.py --manifest
            every file the scaffold ships, one path per line.
Summary:    python3 scripts/validate.py --summary <instance-dir>
            context sections populated, and populated context files tagged.

Checks: required files, relative markdown links, decision-record headings,
decision-log row shape, provenance tags on evidence rows and log rows, and a
provenance tag under '## Provenance' in every populated context file.
Stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "INDEX.md",
    "README.md",
    ".claude/settings.json",
    "scripts/validate.py",
    "context/strategy.md",
    "context/product.md",
    "context/consumers.md",
    "context/team-and-decision-rights.md",
    "context/data-contract.md",
    "context/metrics-and-quality.md",
    "context/commercial-and-access-boundaries.md",
    "rules/INDEX.md",
    "rules/discovery.md",
    "rules/commitment.md",
    "rules/launch.md",
    "packets/INDEX.md",
    "packets/_TEMPLATE.md",
    "decisions/INDEX.md",
    "decisions/_SCHEMA.md",
    "decisions/LOG.md",
    "risks/LOG.md",
    "source/INDEX.md",
    "ingestion/INDEX.md",
    "maintenance/INDEX.md",
    "maintenance/scorecard.md",
    "maintenance/owner-guide.md",
]
# Shipped by the scaffold but not required: init skips it when the operator already has one.
OPTIONAL_FILES = [".gitignore"]
MANIFEST = REQUIRED_FILES + OPTIONAL_FILES

DECISION_HEADINGS = [
    "Status",
    "Date",
    "Decider",
    "Decision",
    "Evidence",
    "What would reverse this",
    "Review date",
]
STATUS_VALUES = {"pending", "decided", "superseded"}
LOG_CELLS = 7
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROVENANCE_DIRS = ("source", "ingestion")
LOG_PROVENANCE_DIRS = ("source", "ingestion", "decisions")
INSTANCE_DIRS = ("context", "rules", "packets", "decisions", "risks", "ingestion", "maintenance")
TOP_LEVEL_MD = ("INDEX.md", "CLAUDE.md", "AGENTS.md", "README.md")

UNKNOWN_RE = re.compile(r"\bUnknown(\s*\([^)]*\))?\s*`?\s*$")
PROVENANCE_RES = (
    re.compile(r"\(stakeholder-verbal,\s*[^,]+,\s*\d{4}-\d{2}-\d{2}\)\s*`?\s*$", re.I),
    re.compile(r"\(intuition,\s*[^,]+,\s*\d{4}-\d{2}-\d{2}\)\s*`?\s*$", re.I),
    re.compile(r"\(hub,\s*[^,]+,\s*\d{4}-\d{2}-\d{2}\)\s*`?\s*$", re.I),
    re.compile(r"\(industry-knowledge\)\s*`?\s*$", re.I),
    re.compile(r"\(chat,\s*no artifact\)\s*`?\s*$", re.I),
    UNKNOWN_RE,
)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TABLE_SEP_RE = re.compile(r"^\|?[\s:|-]*-{3,}[\s:|-]*$")
CONTEXT_DIR = "context"
PROVENANCE_HEADING = "Provenance"
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```[^\n]*\n.*?^```[ \t]*$", re.S | re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
PLACEHOLDER_RE = re.compile(r"^\s*(<[^>]*>|\(none( yet)?\)|tbd|todo|-)\s*(`<provenance-tag>`)?\s*$", re.I)
ROOT_MARKERS = ("context", "decisions", "rules", "packets")


def _strip_code(text: str) -> str:
    return INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))


def find_root(path: Path) -> Path | None:
    cur = path.resolve()
    cur = cur if cur.is_dir() else cur.parent
    while True:
        if (cur / "INDEX.md").is_file() and sum((cur / m).is_dir() for m in ROOT_MARKERS) >= 2:
            return cur
        if cur.parent == cur:
            return None
        cur = cur.parent


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _link_resolves(target: str, base: Path) -> bool:
    target = target.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "tel:")):
        return True
    if "<" in target or "{{" in target:
        return True
    return (base / target).resolve().exists()


def _provenance_link_ok(target: str, base: Path, root: Path, dirs: tuple[str, ...]) -> bool:
    """A provenance link must be a real file under one of the allowed instance folders."""
    target = target.split("#", 1)[0].strip()
    if not target or "<" in target or "{{" in target or target.startswith(("http://", "https://")):
        return False
    resolved = (base / target).resolve()
    if not resolved.is_file():
        return False
    try:
        rel = resolved.relative_to(root.resolve())
    except ValueError:
        return False
    return len(rel.parts) > 1 and rel.parts[0] in dirs


def has_provenance(row: str, base: Path, root: Path, dirs: tuple[str, ...] = PROVENANCE_DIRS) -> bool:
    """A row is tagged when it ends with an enum tag, `Unknown`, or a link into an allowed folder."""
    if any(rx.search(row) for rx in PROVENANCE_RES):
        return True
    links = LINK_RE.findall(row)
    if links:
        _, target = links[-1]
        after = row[row.rfind("(" + target + ")") + len(target) + 2 :].strip().strip("`")
        if after == "" and _provenance_link_ok(target, base, root, dirs):
            return True
    return False


def check_required(root: Path) -> list[str]:
    return [f"{rel}: required file missing" for rel in REQUIRED_FILES if not (root / rel).is_file()]


def check_links(path: Path, root: Path, text: str) -> list[str]:
    if path.name == "_SCHEMA.md":
        return []
    text = _strip_code(text)
    out = []
    for _, target in LINK_RE.findall(text):
        if not _link_resolves(target, path.parent):
            out.append(f"{_rel(path, root)}: link does not resolve: {target.split('#', 1)[0]}")
    return out


def _section(text: str, heading: str) -> list[str]:
    """Lines under `## <heading>` up to the next heading."""
    lines = text.splitlines()
    out, inside = [], False
    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m:
            inside = m.group(2).strip().lower() == heading.lower()
            continue
        if inside:
            out.append(line)
    return out


def _is_decision_record(path: Path, root: Path) -> bool:
    rel = _rel(path, root)
    return (
        rel.startswith("decisions/")
        and path.suffix == ".md"
        and path.name not in {"_SCHEMA.md", "INDEX.md", "LOG.md"}
    )


def _first_value(text: str, heading: str) -> str:
    return next((l.strip() for l in _section(text, heading) if l.strip()), "")


def check_decision(path: Path, root: Path, text: str) -> list[str]:
    rel = _rel(path, root)
    text = _strip_code(text)
    headings = {re.sub(r"^#{2,6}\s+", "", h).strip().lower() for h in re.findall(r"^#{2,6}\s+.*$", text, re.M)}
    out = []
    for h in DECISION_HEADINGS:
        if h.lower() not in headings:
            out.append(f"{rel}: missing heading '## {h}'")
    status = _first_value(text, "Status")
    if not status:
        out.append(f"{rel}: missing value under '## Status'")
    elif status.lower() not in STATUS_VALUES:
        out.append(f"{rel}: status '{status}' not in {sorted(STATUS_VALUES)}")
    if not _first_value(text, "Decider"):
        out.append(f"{rel}: missing value under '## Decider'")
    date = _first_value(text, "Date")
    if date and not DATE_RE.match(date):
        out.append(f"{rel}: '## Date' value '{date}' is not YYYY-MM-DD")
    review = _first_value(text, "Review date")
    if not review:
        out.append(f"{rel}: missing value under '## Review date'")
    elif not (DATE_RE.match(review) or review.startswith("Unknown")):
        out.append(f"{rel}: '## Review date' value '{review}' is not YYYY-MM-DD or Unknown")
    evidence_rows = 0
    for heading in ("Evidence", "Explicitly NOT doing"):
        for i, line in enumerate(_section(text, heading), 1):
            m = re.match(r"^\s*[-*]\s+(.*)$", line)
            if not m:
                continue
            row = m.group(1).strip()
            if not row or PLACEHOLDER_RE.match(row):
                continue
            if heading == "Evidence":
                evidence_rows += 1
            if not has_provenance(row, path.parent, root):
                out.append(f"{rel}: untagged row {i} under '## {heading}': {row[:60]}")
    if status.lower() == "decided" and evidence_rows == 0:
        out.append(f"{rel}: decided record has no evidence row")
    return out


def check_log(path: Path, root: Path, text: str) -> list[str]:
    rel = _rel(path, root)
    out = []
    rows = [l for l in text.splitlines() if l.lstrip().startswith("|")]
    for n, line in enumerate(rows):
        if n < 2:
            continue  # header and separator
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != LOG_CELLS:
            out.append(f"{rel}: row {n + 1} has {len(cells)} cells, expected {LOG_CELLS}")
            continue
        if not DATE_RE.match(cells[0]):
            out.append(f"{rel}: row {n + 1} date '{cells[0]}' is not YYYY-MM-DD")
        if not (DATE_RE.match(cells[5]) or cells[5].startswith("Unknown")):
            out.append(f"{rel}: row {n + 1} review date '{cells[5]}' is not YYYY-MM-DD or Unknown")
        status = cells[4].lower()
        if status not in STATUS_VALUES:
            out.append(f"{rel}: row {n + 1} status '{cells[4]}' not in {sorted(STATUS_VALUES)}")
        if not has_provenance(cells[3], path.parent, root, LOG_PROVENANCE_DIRS):
            out.append(f"{rel}: row {n + 1} evidence cell has no tag, link, or Unknown")
    return out


def _h2_sections(text: str) -> list[tuple[str, list[str]]]:
    # Inline code stays: a provenance tag is often written in backticks.
    text = COMMENT_RE.sub("", FENCE_RE.sub("", text))
    out: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*?)\s*$", line)
        if m:
            out.append((m.group(1), []))
        elif out:
            out[-1][1].append(line)
    return out


def _populated(lines: list[str]) -> bool:
    seen_header = False
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            seen_header = False
            if s:
                return True
            continue
        if not seen_header:
            seen_header = True
            continue
        if TABLE_SEP_RE.match(s):
            continue
        # Templates ship row labels (role names) in the first cell, so only the other cells count.
        _label, *values = [c.strip() for c in s.strip("|").split("|")]
        if any(values):
            return True
    return False


class ContextStatus(NamedTuple):
    sections: int
    populated: int
    tagged: bool
    unknown: bool


def context_status(path: Path, root: Path, text: str) -> ContextStatus:
    content: list[list[str]] = []
    provenance: list[str] = []
    for heading, lines in _h2_sections(text):
        if heading.lower() == PROVENANCE_HEADING.lower():
            provenance = lines
        else:
            content.append(lines)
    tags = [l.strip() for l in provenance if l.strip() and has_provenance(l.strip(), path.parent, root)]
    return ContextStatus(
        sections=len(content),
        populated=sum(_populated(lines) for lines in content),
        tagged=bool(tags),
        unknown=any(UNKNOWN_RE.search(t) for t in tags),
    )


def _is_context_file(path: Path, root: Path) -> bool:
    rel = _rel(path, root)
    return rel.startswith(f"{CONTEXT_DIR}/") and rel.count("/") == 1 and path.suffix == ".md"


def check_context(path: Path, root: Path, text: str) -> list[str]:
    status = context_status(path, root, text)
    if status.populated and not status.tagged:
        return [f"{_rel(path, root)}: populated context has no provenance tag under '## {PROVENANCE_HEADING}'"]
    return []


def context_summary(root: Path) -> list[str]:
    files = sorted((root / CONTEXT_DIR).glob("*.md"))
    stats = [context_status(p, root, p.read_text(encoding="utf-8")) for p in files]
    populated = [s for s in stats if s.populated]
    return [
        f"context sections populated: {sum(s.populated for s in stats)} of {sum(s.sections for s in stats)}",
        f"context files populated: {len(populated)} of {len(stats)}, "
        f"tagged: {sum(s.tagged for s in populated)}, Unknown: {sum(s.unknown for s in populated)}",
    ]


def validate_file(path: Path, root: Path) -> tuple[list[str], list[str]]:
    """Returns (blocking, warnings)."""
    if path.suffix != ".md" or not path.is_file():
        return [], []
    text = path.read_text(encoding="utf-8")
    warnings = check_links(path, root, text)
    if _is_context_file(path, root):
        warnings += check_context(path, root, text)
    blocking: list[str] = []
    if _is_decision_record(path, root):
        blocking += check_decision(path, root, text)
    if _rel(path, root) == "decisions/LOG.md":
        blocking += check_log(path, root, text)
    return blocking, warnings


def _in_instance(rel: str) -> bool:
    """Only the instance's own files are validated; source/ is verbatim and host files are not ours."""
    parts = rel.split("/")
    if len(parts) == 1:
        return parts[0] in TOP_LEVEL_MD
    return parts[0] in INSTANCE_DIRS or rel == "source/INDEX.md"


def _instance_paths(root: Path):
    # Walk only instance folders, never the host repo, so an active-repo root's node_modules is not read.
    candidates = [root / name for name in TOP_LEVEL_MD]
    for d in INSTANCE_DIRS:
        candidates += sorted((root / d).rglob("*.md"))
    candidates.append(root / "source" / "INDEX.md")
    for path in candidates:
        if path.is_file() and _in_instance(_rel(path, root)):
            yield path


def validate_dir(root: Path) -> list[str]:
    findings = check_required(root)
    for path in _instance_paths(root):
        b, w = validate_file(path, root)
        findings += b + w
    return findings


def _hook() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    fp = (payload.get("tool_input") or {}).get("file_path")
    if not fp:
        return 0
    path = Path(fp)
    if not path.exists() or path.suffix != ".md":
        return 0
    root = find_root(path)
    if root is None or not _in_instance(_rel(path, root)):
        return 0
    blocking, warnings = validate_file(path, root)
    if warnings:
        print("[team-loop] warnings:\n" + "\n".join(warnings), file=sys.stderr)
    if blocking:
        print("[team-loop] BLOCKING, fix this turn:\n" + "\n".join(blocking), file=sys.stderr)
        return 2
    return 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--manifest"]:
        print("\n".join(MANIFEST))
        return 0
    summary = len(argv) == 3 and argv[1] == "--summary"
    if len(argv) > 1:
        arg = argv[2] if summary else argv[1]
        root = Path(arg)
        if not root.is_dir():
            print(f"{arg}: not a directory")
            return 1
        if summary:
            print("\n".join(context_summary(root)))
            return 0
        findings = validate_dir(root)
        for f in findings:
            print(f)
        return 1 if findings else 0
    return _hook()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
