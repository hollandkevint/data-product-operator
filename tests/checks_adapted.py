"""License-line check for adapted skills.

A skill adapted from someone else's work carries `adapted_from:` in its
frontmatter (format: `Author, repo or title, part`) and ends with a
`Source:` line that names the author, links the original and states the
license. See docs/adapted-skills.md.
"""
import re
from pathlib import Path

from repo_checks import parse_frontmatter

# Licenses cleared for adaptation. Add one only after reading its terms.
ADAPT_LICENSES = ("MIT",)
# Authors whose text this repo adapts. A skill that names one must be marked.
KNOWN_ADAPTED_AUTHORS = re.compile(r"Matt Pocock|Pawel Huryn|Paweł Huryn|phuryn", re.I)
SOURCE_LINK = re.compile(r"\]\(https?://[^)\s]+\)")


def check_adapted_sources(root):
    problems = []
    for md in sorted((Path(root) / "skills").glob("*/SKILL.md")):
        rel = md.relative_to(root)
        text = md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text) or {}
        marked = fm.get("adapted_from", "").strip()
        lines = [l for l in text.splitlines() if l.strip()]
        if not marked:
            if KNOWN_ADAPTED_AUTHORS.search(text):
                problems.append(f"{rel}: names an adapted-from author but has no adapted_from frontmatter")
            continue
        author = marked.split(",")[0].strip()
        if not author:
            problems.append(f"{rel}: adapted_from has no author")
            continue
        if not lines or not lines[-1].startswith("Source:"):
            problems.append(f"{rel}: adapted skill must end with a Source: line")
            continue
        src = lines[-1]
        if author.lower() not in src.lower():
            problems.append(f"{rel}: Source line does not name the author '{author}'")
        if not SOURCE_LINK.search(src):
            problems.append(f"{rel}: Source line has no link")
        if not any(re.search(rf"\b{re.escape(l)}\b", src) for l in ADAPT_LICENSES):
            problems.append(f"{rel}: Source line names no cleared license ({', '.join(ADAPT_LICENSES)})")
    return problems
