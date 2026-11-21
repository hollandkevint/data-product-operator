"""Check that the data product retro keeps its two core questions and ties
actions to the decision log. See skills/data-product-retro/SKILL.md."""
import re
from pathlib import Path

RETRO = Path("skills") / "data-product-retro" / "SKILL.md"
QUESTIONS = ("Did the decision change?", "Did the data hold up?")


def output_section(text):
    m = re.search(r"^## Output\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def check_retro(root):
    path = Path(root) / RETRO
    if not path.is_file():
        return [f"{RETRO}: file is missing"]
    out = output_section(path.read_text(encoding="utf-8"))
    if not out:
        return [f"{RETRO}: no '## Output' section"]
    problems = [f"{RETRO}: Output section does not name the question '{q}'" for q in QUESTIONS if q not in out]
    if not re.search(r"Actions tied to the decision log", out):
        problems.append(f"{RETRO}: Output section has no 'Actions tied to the decision log' item")
    if "decisions/LOG.md" not in out:
        problems.append(f"{RETRO}: Output section does not tie actions to decisions/LOG.md")
    return problems
