#!/usr/bin/env python3
"""Checker for the decision follow-up loop. Stdlib only, no model calls.

Usage: python3 check.py <workspace-dir>
Prints one problem per line and exits 1 if there are any. Exits 0 when clean.

It reads decisions/LOG.md and the decision records, then verifies the
maker's output (loops/decision-follow-up/<last_run>.md) and the state file
(loops/decision-follow-up/state.json) against the rules in SKILL.md.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

DISPOSITIONS = {"keep", "reverse", "extend", "no-outcome"}
OPEN = {"extend", "no-outcome"}
NEEDS_EVIDENCE = {"keep", "reverse"}
DATE = r"\d{4}-\d{2}-\d{2}"
EVIDENCE = [
    re.compile(r"^\[(source|ingestion)/[^\]]*\]\(\.\./(source|ingestion)/[^)]+\)$"),
    re.compile(rf"^\((stakeholder-verbal|intuition|hub),\s*[^,)]+,\s*{DATE}\)$"),
    re.compile(r"^\(industry-knowledge\)$"),
    re.compile(r"^\(chat, no artifact\)$"),
    re.compile(r"^Unknown$"),
]
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def parse_date(text):
    try:
        return date.fromisoformat(text.strip())
    except ValueError:
        return None


def table_rows(text, header_start):
    """Return rows (list of cell lists) of the first table whose header starts with header_start."""
    rows, in_table = [], False
    for line in text.splitlines():
        line = line.strip()
        if not in_table:
            in_table = line.startswith("|") and line.lstrip("| ").startswith(header_start)
            continue
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return " ".join(m.group(1).split()) if m else ""


def read_log(root, problems):
    path = root / "decisions" / "LOG.md"
    if not path.exists():
        problems.append("decisions/LOG.md is missing")
        return []
    out = []
    for cells in table_rows(path.read_text(encoding="utf-8"), "Date"):
        if len(cells) != 7:
            problems.append(f"decisions/LOG.md: row has {len(cells)} cells, expected 7: {cells[:2]}")
            continue
        link = LINK.search(cells[3])
        out.append({
            "decision": cells[1], "status": cells[4], "review": cells[5],
            "record": Path(link.group(1)).name if link else None,
        })
    return out


def check(root):
    root = Path(root)
    problems = []

    state_path = root / "loops" / "decision-follow-up" / "state.json"
    if not state_path.exists():
        return ["loops/decision-follow-up/state.json is missing"]
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"state.json is not valid JSON: {e}"]
    for key in ("loop", "last_run", "next_run", "followed_up", "open"):
        if key not in state:
            problems.append(f"state.json: key '{key}' is missing")
    if problems:
        return problems
    if state["loop"] != "decision-follow-up":
        problems.append(f"state.json: loop is '{state['loop']}', expected 'decision-follow-up'")
    last, nxt = parse_date(str(state["last_run"])), parse_date(str(state["next_run"]))
    if not last:
        return problems + ["state.json: last_run is not a date"]
    if not nxt or nxt <= last:
        problems.append("state.json: next_run must be a date after last_run")

    out_path = state_path.parent / f"{state['last_run']}.md"
    if not out_path.exists():
        return problems + [f"maker output {out_path.name} is missing for last_run {state['last_run']}"]
    out_text = out_path.read_text(encoding="utf-8")
    m = re.search(rf"^As of:\s*({DATE})\s*$", out_text, re.M)
    if not m or parse_date(m.group(1)) != last:
        problems.append(f"{out_path.name}: 'As of:' line must equal state last_run {state['last_run']}")

    log = read_log(root, problems)
    by_record = {r["record"]: r for r in log if r["record"]}
    due = {r["record"] for r in log
           if r["status"] == "decided" and r["record"]
           and (parse_date(r["review"]) or date.max) <= last}
    for r in log:
        if r["status"] == "decided" and not parse_date(r["review"]):
            problems.append(f"LOG: '{r['decision']}' has no valid review date")

    seen, open_rows = {}, set()
    for cells in table_rows(out_text, "Decision"):
        if len(cells) != 7:
            problems.append(f"{out_path.name}: row has {len(cells)} cells, expected 7: {cells[:1]}")
            continue
        decision, record, review, reverse, evidence, disp, step = cells
        evidence = evidence.strip("`")
        if record in seen:
            problems.append(f"{record}: followed up twice")
            continue
        seen[record] = disp
        row = by_record.get(record)
        if not row:
            problems.append(f"{record}: not in decisions/LOG.md (invented decision)")
            continue
        if record not in due:
            problems.append(f"{record}: not due (status '{row['status']}', review {row['review']}), must not be followed up")
        if decision != row["decision"]:
            problems.append(f"{record}: decision text differs from the log")
        if review != row["review"]:
            problems.append(f"{record}: review date differs from the log")
        rec_path = root / "decisions" / record
        if not rec_path.exists():
            problems.append(f"{record}: decision record file is missing")
        else:
            rec = rec_path.read_text(encoding="utf-8")
            if section(rec, "Status") != row["status"]:
                problems.append(f"{record}: record status differs from the log")
            if section(rec, "Review date") != row["review"]:
                problems.append(f"{record}: record review date differs from the log")
            if " ".join(reverse.split()) != section(rec, "What would reverse this"):
                problems.append(f"{record}: reverse condition does not match the record")
        if not any(p.match(evidence) for p in EVIDENCE):
            problems.append(f"{record}: evidence '{evidence}' is not a provenance tag or Unknown")
        if disp not in DISPOSITIONS:
            problems.append(f"{record}: disposition '{disp}' is not one of {sorted(DISPOSITIONS)}")
            continue
        if disp in NEEDS_EVIDENCE and evidence == "Unknown":
            problems.append(f"{record}: '{disp}' needs observed outcome evidence, not Unknown")
        if disp in OPEN:
            open_rows.add(record)
            if not any((parse_date(d) or last) > last for d in re.findall(DATE, step)):
                problems.append(f"{record}: '{disp}' needs a next review date after {state['last_run']} in Next step")
        elif not step.strip("- "):
            problems.append(f"{record}: next step is empty")

    for record in sorted(due - set(seen)):
        problems.append(f"{record}: due for follow-up but missing from the output")
    if set(state["followed_up"]) != set(seen):
        problems.append("state.json: followed_up does not match the output rows")
    if set(state["open"]) != open_rows:
        problems.append("state.json: open does not match rows with extend or no-outcome")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check.py <workspace-dir>")
    found = check(sys.argv[1])
    for p in found:
        print(p)
    sys.exit(1 if found else 0)
