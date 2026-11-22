"""Banned words from the CLAUDE.md "NEVER use:" line stay out of shipped prose.

CLAUDE.md is the single source of truth for the list. Only bare words are
checked; quoted phrases and "Gartner-speak" need a human reader.
"""
import re
from pathlib import Path

from repo_checks import _prose, markdown_files

VOICE_SCOPE = ("README.md", "docs", "skills", "team-loop", "commands")
NEVER_LINE = re.compile(r"^NEVER use:\s*(.+)$", re.M)


def banned_words(root):
    m = NEVER_LINE.search((Path(root) / "CLAUDE.md").read_text(encoding="utf-8"))
    if not m:
        return []
    items = [i.strip().rstrip(".") for i in re.split(r",\s*(?:or\s+)?", m.group(1))]
    return [i for i in items if re.fullmatch(r"[a-z]+", i)]


def word_pattern(word):
    """The word and its verb forms: leverage, leverages, leveraged, leveraging."""
    forms = [word + "s", word + "d", word + "ed", word + "ing"]
    if word.endswith("e"):
        forms.append(word[:-1] + "ing")
    alts = "|".join(re.escape(f) for f in [word] + forms)
    return re.compile(rf"(?<![\w]){'(?:' + alts + ')'}(?![\w])", re.I)


def check_banned_words(root):
    root = Path(root)
    patterns = [(w, word_pattern(w)) for w in banned_words(root)]
    problems = []
    for md in markdown_files(root):
        rel = md.relative_to(root)
        if rel.parts[0] not in VOICE_SCOPE:
            continue
        for n, line in enumerate(_prose(md.read_text(encoding="utf-8")), 1):
            for w, pat in patterns:
                if pat.search(line):
                    problems.append(f"{rel}:{n}: uses banned word '{w}' (see CLAUDE.md Voice)")
    return problems
