"""Demos that carry a copy of another skill's demo files must keep them identical."""
from pathlib import Path

from repo_checks import REPO

# (copy, original) directory pairs, relative to the repo root.
PAIRS = [
    ("skills/strategy-review/demo/decisions", "skills/decision-follow-up/demo/decisions"),
    ("skills/strategy-review/demo/loops/decision-follow-up", "skills/decision-follow-up/demo/loops/decision-follow-up"),
]


def check_demo_sync(repo=REPO, pairs=PAIRS):
    problems = []
    for copy, orig in pairs:
        c, o = Path(repo) / copy, Path(repo) / orig
        for d in (c, o):
            if not d.is_dir():
                problems.append(f"{d.relative_to(repo)} is missing")
        if problems:
            continue
        names_c = {p.relative_to(c) for p in c.rglob("*") if p.is_file()}
        names_o = {p.relative_to(o) for p in o.rglob("*") if p.is_file()}
        for n in sorted(names_o - names_c):
            problems.append(f"{copy}/{n} is missing, copy of {orig}/{n}")
        for n in sorted(names_c - names_o):
            problems.append(f"{copy}/{n} has no original in {orig}")
        for n in sorted(names_c & names_o):
            if (c / n).read_bytes() != (o / n).read_bytes():
                problems.append(f"{copy}/{n} differs from {orig}/{n}")
    return problems
