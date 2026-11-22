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


# Skills added in the 2.0 release. They use `metadata.version`; older skills
# keep their top-level `version:` and are not force-migrated.
RELEASE_2_SKILLS = (
    "strategy-review", "decision-follow-up", "weekly-metric-review",
    "data-quality-watch", "agent-eval-regression", "data-product-retro",
    "analytics-agent", "metric-glossary", "launch-and-adoption",
    "shipping-bridge", "data-dictionary-grill", "team-loop",
)


def check_skill_shape(root, release_skills=RELEASE_2_SKILLS):
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
        if d.name in release_skills and ("version" in fm or "version:" not in fm.get("metadata", "")):
            problems.append(f"{rel}/SKILL.md: 2.0 skills use metadata.version, not a top-level version")
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


# --- glossary checks ---------------------------------------------------------

# Avoid terms that are ordinary words and cannot be banned from prose. Each
# entry says why. A term here is still checked nowhere, so keep this short.
GLOSSARY_ALLOWED = {
    "dashboard": "a real kind of delivery surface; the glossary bans it only as a synonym for 'data product'",
    "report": "an ordinary noun; banned only as a synonym for 'data product'",
    "the data": "an ordinary phrase; banned only as a name for the product itself",
    "stakeholder": "part of skill and command names (stakeholder alignment, stakeholder brief)",
    "customer": "domain vocabulary in the ecommerce and support guides",
}

GLOSSARY_USE_SCOPE = ("README.md", "CLAUDE.md", "docs", "skills", "team-loop")
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')
HTML_COMMENT = re.compile(r"<!--.*?-->")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
BARE_URL = re.compile(r"https?://\S+")


def _split_top_level(text):
    parts, depth, quoted, cur = [], 0, False, ""
    for ch in text:
        if ch == '"':
            quoted = not quoted
        elif ch == "(" and not quoted:
            depth += 1
        elif ch == ")" and not quoted:
            depth -= 1
        if ch == "," and depth == 0 and not quoted:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def avoid_terms(root):
    """Avoid terms with no qualifier. A term with '(...)' only applies in a
    named context, so it is not matched as plain text."""
    glossary = Path(root) / "GLOSSARY.md"
    if not glossary.is_file():
        return []
    terms = []
    for line in glossary.read_text(encoding="utf-8").splitlines():
        if line.startswith("_Avoid_:"):
            for item in _split_top_level(line.split(":", 1)[1]):
                if "(" not in item:
                    terms.append(item.strip('"'))
    return terms


def check_glossary_shape(root):
    """Every glossary entry has a bold term, a definition and an _Avoid_ line."""
    glossary = Path(root) / "GLOSSARY.md"
    if not glossary.is_file():
        return ["GLOSSARY.md: file is missing"]
    problems, term, body = [], None, []

    def close():
        if term is None:
            return
        if not any(b.strip() and not b.startswith("_Avoid_") for b in body):
            problems.append(f"GLOSSARY.md: '{term}' has no definition")
        if not any(b.startswith("_Avoid_:") for b in body):
            problems.append(f"GLOSSARY.md: '{term}' has no _Avoid_ line")

    for line in glossary.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\*\*(.+?)\*\*:\s*$", line)
        if m:
            close()
            term, body = m.group(1), []
        elif line.startswith("#"):
            close()
            term, body = None, []
        elif term is not None:
            body.append(line)
    close()
    return problems


def _prose(text):
    """Text a reader sees as plain words: no code, quotes, comments or link targets."""
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            out.append("")
            continue
        line = HTML_COMMENT.sub("", line)
        line = INLINE_CODE.sub("", line)
        line = LINK_TARGET.sub("]", line)
        line = BARE_URL.sub("", line)
        out.append(QUOTED.sub("", line))
    return out


def check_glossary_use(root, allowed=None):
    """Avoid terms from GLOSSARY.md do not appear unquoted in README.md, docs/, skills/ or team-loop/."""
    root = Path(root)
    allowed = GLOSSARY_ALLOWED if allowed is None else allowed
    terms = [t for t in avoid_terms(root) if t.lower() not in allowed]
    problems = []
    for md in markdown_files(root):
        rel = md.relative_to(root)
        if rel.parts[0] not in GLOSSARY_USE_SCOPE:
            continue
        for n, line in enumerate(_prose(md.read_text(encoding="utf-8")), 1):
            for t in terms:
                if re.search(rf"(?<![\w-]){re.escape(t)}s?(?![\w-])", line, re.I):
                    problems.append(f"{rel}:{n}: uses avoided term '{t}' (see GLOSSARY.md)")
    return problems


# --- first-principles page ---------------------------------------------------

FP_PATH = "docs/first-principles.md"
MIN_DISAGREEMENTS = 8
URL = re.compile(r"\]\(https?://[^)\s]+\)")


def _sections(text, level):
    """Split text into {heading: body} at the given heading level."""
    pat = re.compile(rf"^{'#' * level} (.+)$", re.M)
    marks = list(pat.finditer(text))
    return {
        m.group(1): text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        for i, m in enumerate(marks)
    }


RECHECK_MARKER = "<!-- recheck quote -->"


def check_no_recheck_markers(root):
    """Release gate: every quote is verified, so no recheck marker may remain in README or docs/."""
    problems = []
    for p in markdown_files(root):
        rel = p.relative_to(root)
        if rel.parts[0] != "docs" and str(rel) != "README.md":
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if RECHECK_MARKER in line:
                problems.append(f"{rel}:{n}: unverified quote still carries a recheck marker")
    return problems


def check_first_principles(root):
    page = Path(root) / FP_PATH
    if not page.is_file():
        return [f"{FP_PATH}: file is missing"]
    text = page.read_text(encoding="utf-8")
    problems = []
    principles = {h: b for h, b in _sections(text, 3).items() if re.match(r"P\d+\.", h)}
    if len(principles) != 9:
        problems.append(f"{FP_PATH}: expected 9 principles, found {len(principles)}")
    for h, body in principles.items():
        if not URL.search(body):
            problems.append(f"{FP_PATH}: {h.split('.')[0]} names no source with a link")
    disagree = next((b for h, b in _sections(text, 2).items() if h.lower().startswith("where the sources disagree")), None)
    count = len(re.findall(r"^[-*] ", disagree or "", re.M))
    if count < MIN_DISAGREEMENTS:
        problems.append(f"{FP_PATH}: disagreements section has {count} items, need {MIN_DISAGREEMENTS}")
    if "Kevin Holland's synthesis" not in text:
        problems.append(f"{FP_PATH}: maturity model is not labelled Kevin Holland's synthesis")
    problems += check_no_recheck_markers(root)
    return problems
