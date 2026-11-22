"""Checks for the v2.0.0 release surface: manifests, README order, the
README's example Team Loop packet, and the release notes' moved paths."""
import importlib.util
import json
import re
import shutil
import tempfile
from pathlib import Path

VERSION = "2.0.1"
AUDIENCE = "data leaders, data product operators, and their teams"
KEYWORDS = ("analytics-agents", "data-mesh", "claude-code")

# README H2 headings, in the order the spec and ticket 13 set. Other
# headings may sit between them.
PROMISE = "Decisions, not dashboards"
README_SECTIONS = (
    "The cycle",
    "Quick start",
    "Example",
    "Match grid",
    "Person, team, company",
    "Jobs and skills",
    "Credits",
    "Formerly dpm_os",
)

SCAFFOLD = Path("skills") / "team-loop" / "scaffold"
PACKET_TEMPLATE = SCAFFOLD / "packets" / "_TEMPLATE.md"
PLACEHOLDER = re.compile(r"<(?!!--)[a-z][^>\n]*>|YYYY-MM-DD|<!--")

NOTES = "docs/releases/v2.0.0.md"
NOTES_SECTIONS = ("What's new", "What moved", "Upgrade", "Credits")
# Every tracked dpm_os path and where it lives now (rename commit cceaab5,
# and `git ls-files` in the archived dpm_os repo).
MOVED = (
    (".claude/skills/dpm-os/", "skills/team-loop/"),
    (".claude/skills/dpm-os/SKILL.md", "skills/team-loop/SKILL.md"),
    (".claude/skills/dpm-os/prompts/", "skills/team-loop/prompts/"),
    (".claude/skills/dpm-os/scaffold/", "skills/team-loop/scaffold/"),
    ("README.md", "team-loop/README.md"),
    ("CLAUDE.md", "team-loop/CLAUDE.md"),
    ("LICENSE", "team-loop/LICENSE"),
    (".gitignore", "team-loop/.gitignore"),
    ("docs/install.md", "team-loop/docs/install.md"),
    ("grader/", "team-loop/grader/"),
    ("tests/test_containment.py", "tests/test_containment.py"),
    ("tests/test_grader.py", "tests/test_grader.py"),
    ("tests/test_validate.py", "tests/test_validate.py"),
)


def _load(path, problems):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        problems.append(f"{path.name}: cannot read ({e})")
        return None


def check_release_manifests(root):
    base = Path(root) / ".claude-plugin"
    problems = []
    plugin = _load(base / "plugin.json", problems)
    market = _load(base / "marketplace.json", problems)
    if plugin is not None:
        if plugin.get("version") != VERSION:
            problems.append(f"plugin.json: version is not {VERSION}")
        if AUDIENCE not in plugin.get("description", ""):
            problems.append(f"plugin.json: description does not name '{AUDIENCE}'")
        for k in KEYWORDS:
            if k not in plugin.get("keywords", []):
                problems.append(f"plugin.json: keyword '{k}' is missing")
    if market is not None:
        if (market.get("metadata") or {}).get("version") != VERSION:
            problems.append(f"marketplace.json: metadata.version is not {VERSION}")
        descs = [(market.get("metadata") or {}).get("description", "")]
        descs += [p.get("description", "") for p in market.get("plugins", [])]
        for d in descs:
            if AUDIENCE not in d:
                problems.append(f"marketplace.json: description does not name '{AUDIENCE}': {d[:50]}")
    return problems


def _h2(text):
    return [m.group(1).strip() for m in re.finditer(r"^## (.+)$", _no_fences(text), re.M)]


def _no_fences(text):
    return re.sub(r"^```.*?^```[ \t]*$", "", text, flags=re.S | re.M)


def check_readme_order(root):
    path = Path(root) / "README.md"
    if not path.is_file():
        return ["README.md: file is missing"]
    text = path.read_text(encoding="utf-8")
    problems = []
    first_h2 = text.find("\n## ")
    if PROMISE not in text[: first_h2 if first_h2 > 0 else len(text)]:
        problems.append(f"README.md: the promise '{PROMISE}' is not above the first section")
    heads = _h2(text)
    found = []
    for want in README_SECTIONS:
        idx = next((i for i, h in enumerate(heads) if h.startswith(want)), None)
        if idx is None:
            problems.append(f"README.md: no '## {want}' section")
        else:
            found.append((idx, want))
    order = [w for _, w in sorted(found)]
    if order != [w for _, w in found]:
        problems.append(f"README.md: sections out of order: {order}")
    return problems


def example_packet(text):
    """The first ```markdown block under the README's '## Example' section."""
    m = re.search(r"^## Example.*?^```markdown\n(.*?)^```", text, re.S | re.M)
    return m.group(1) if m else None


def _validator(root):
    spec = importlib.util.spec_from_file_location("tl_validate", Path(root) / SCAFFOLD / "scripts" / "validate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_example_packet(root):
    root = Path(root)
    packet = example_packet((root / "README.md").read_text(encoding="utf-8"))
    if packet is None:
        return ["README.md: no ```markdown packet under '## Example'"]
    problems = []
    want = re.findall(r"^## (.+)$", (root / PACKET_TEMPLATE).read_text(encoding="utf-8"), re.M)
    have = re.findall(r"^## (.+)$", packet, re.M)
    for h in want:
        if h not in have:
            problems.append(f"README.md: example packet lacks template heading '## {h}'")
    if [h for h in have if h in want] != [h for h in want if h in have]:
        problems.append("README.md: example packet headings are out of template order")
    for n, line in enumerate(packet.splitlines(), 1):
        if PLACEHOLDER.search(line):
            problems.append(f"README.md: example packet line {n} keeps a template placeholder: {line.strip()[:50]}")
    with tempfile.TemporaryDirectory() as t:
        inst = Path(t)
        shutil.copytree(root / SCAFFOLD, inst, dirs_exist_ok=True)
        week = re.search(r"^week:\s*(\S+)", packet, re.M)
        name = f"{week.group(1) if week else 'example'}-weekly-packet.md"
        (inst / "packets" / name).write_text(packet, encoding="utf-8")
        problems += [f"README.md example packet: {f}" for f in _validator(root).validate_dir(inst)]
    return problems


def check_release_notes(root):
    root = Path(root)
    path = root / NOTES
    if not path.is_file():
        return [f"{NOTES}: file is missing"]
    text = path.read_text(encoding="utf-8")
    heads = _h2(text)
    problems = [f"{NOTES}: no '## {s}' section" for s in NOTES_SECTIONS if not any(h.startswith(s) for h in heads)]
    moved = re.search(r"^## What moved\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    body = moved.group(1) if moved else ""
    rows = [l for l in body.splitlines() if l.startswith("|")]
    for old, new in MOVED:
        if not any(f"`{old}`" in r and f"`{new}`" in r for r in rows):
            problems.append(f"{NOTES}: 'What moved' has no row for `{old}` -> `{new}`")
        if not (root / new.rstrip("/")).exists():
            problems.append(f"{NOTES}: moved path `{new}` does not exist in the repo")
    return problems
