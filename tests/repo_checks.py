"""Shared check logic for the repo check suite.

Each check takes a repo root and returns a list of problem strings.
An empty list means the check passes. Test modules call these on the
real repo and on small broken fixtures, so every check is proven to
fail on the bug it guards.

To add a check: write a `check_*(root)` function here (or in its own
module under tests/) and add a test module `tests/test_<topic>.py`.
`python -m unittest discover -s tests` picks it up.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".scratch", "node_modules", "__pycache__"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def parse_frontmatter(text):
    """Return top-level frontmatter keys as {key: value}, or None if absent.

    Handles `key: value`, folded (`>`) and literal (`|`) blocks, and
    nested maps (a key with no inline value and indented children keeps
    the children joined as its value).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None
    fields, key = {}, None
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            value = m.group(2).strip()
            fields[key] = "" if value in (">", "|", ">-", "|-") else value
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def check_skill_shape(root):
    problems = []
    skills = Path(root) / "skills"
    if not skills.is_dir():
        return ["skills/ directory is missing"]
    for d in sorted(p for p in skills.iterdir() if p.is_dir()):
        rel = f"skills/{d.name}"
        md = d / "SKILL.md"
        if not md.is_file():
            problems.append(f"{rel}: SKILL.md is missing")
            continue
        fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        if fm is None:
            problems.append(f"{rel}/SKILL.md: frontmatter is missing")
            continue
        if not fm.get("name"):
            problems.append(f"{rel}/SKILL.md: name is missing")
        elif fm["name"].strip("\"'") != d.name:
            problems.append(f"{rel}/SKILL.md: name '{fm['name']}' does not match folder")
        if not fm.get("description"):
            problems.append(f"{rel}/SKILL.md: description is missing")
    return problems


def _load_json(path, problems):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        problems.append(f"{path.name}: file is missing")
    except json.JSONDecodeError as e:
        problems.append(f"{path.name}: invalid JSON ({e})")
    return None


def check_manifests(root):
    """plugin.json and marketplace.json parse, carry semver, and agree."""
    problems = []
    base = Path(root) / ".claude-plugin"
    plugin = _load_json(base / "plugin.json", problems)
    market = _load_json(base / "marketplace.json", problems)
    versions = {}
    if plugin is not None:
        versions["plugin.json"] = plugin.get("version")
        for k in ("name", "description"):
            if not plugin.get(k):
                problems.append(f"plugin.json: {k} is missing")
    if market is not None:
        versions["marketplace.json"] = (market.get("metadata") or {}).get("version")
        for p in market.get("plugins", []):
            if plugin and p.get("name") != plugin.get("name"):
                problems.append("marketplace.json: plugin name differs from plugin.json")
    for name, v in versions.items():
        if not isinstance(v, str) or not SEMVER.match(v):
            problems.append(f"{name}: version '{v}' is not semver (X.Y.Z)")
    if len(set(versions.values())) > 1:
        problems.append(f"manifest versions disagree: {versions}")
    return problems


LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)|!\[[^\]]*\]\(\s*<?([^)\s>]+)>?")
FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")


def markdown_files(root):
    for p in sorted(Path(root).rglob("*.md")):
        if not SKIP_DIRS.intersection(p.relative_to(root).parts):
            yield p


def check_relative_links(root):
    """Every relative markdown link points at a file or folder that exists."""
    root = Path(root).resolve()
    problems = []
    for md in markdown_files(root):
        in_fence = False
        for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in LINK.finditer(INLINE_CODE.sub("", line)):
                target = (m.group(1) or m.group(2)).split("#")[0].split("?")[0]
                if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                    continue
                base = root if target.startswith("/") else md.parent
                dest = (base / target.lstrip("/")).resolve()
                if not dest.exists():
                    problems.append(f"{md.relative_to(root)}:{n}: broken link '{target}'")
    return problems
