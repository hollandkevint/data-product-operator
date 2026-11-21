"""Output-field check for the launch-and-adoption and shipping-bridge skills.

Each skill ends with an `## Output` section that lists the fields its result must
carry. Removing a field from that section makes the check fail.
"""
from pathlib import Path

REQUIRED = {
    "launch-and-adoption": ("Consumer", "Decision changed", "Adoption signal",
                            "Countermetric", "Onboarding", "Channels", "Retire rule"),
    "shipping-bridge": ("Gate", "Source", "Owner", "Evidence", "Outcome"),
}


def output_section(text):
    marker = "\n## Output"
    i = text.find(marker)
    if i < 0:
        return None
    rest = text[i + len(marker):]
    j = rest.find("\n## ")
    return rest if j < 0 else rest[:j]


def check_launch_outputs(root):
    problems = []
    for name, fields in REQUIRED.items():
        path = Path(root) / "skills" / name / "SKILL.md"
        if not path.exists():
            problems.append(f"skills/{name}/SKILL.md: missing")
            continue
        section = output_section(path.read_text(encoding="utf-8"))
        if section is None:
            problems.append(f"skills/{name}/SKILL.md: no '## Output' section")
            continue
        for f in fields:
            if f"**{f}:**" not in section:
                problems.append(f"skills/{name}/SKILL.md: output field '{f}' is missing")
    return problems
