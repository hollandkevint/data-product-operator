#!/usr/bin/env python3
"""Checker for the strategy review loop. Stdlib only, no model calls.

Usage: python3 check.py <workspace-dir>
Prints one problem per line and exits 1 if there are any. Exits 0 when clean.

It reads decisions/LOG.md (the Team Loop decision log) and the newest decision
follow-up output, then verifies the maker's review
(loops/strategy-review/<last_run>.md) and state file against SKILL.md.
"""
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

# Shared helpers live in <repo>/lib. The plugin installs the whole repo, so this path holds.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from loop_helpers import line_value, parse_date, read_log, table_rows  # noqa: E402

LOOP = "strategy-review"
DATE = r"\d{4}-\d{2}-\d{2}"
GROUPS = ["keep", "reverse", "extend", "no-outcome", "superseded", "not-reviewed"]
CALLS = {"pending", "keep", "change", "stop", "n/a"}
QUESTION = "Keep, change or stop?"


def quarter_range(label):
    m = re.fullmatch(r"(\d{4})-Q([1-4])", str(label))
    if not m:
        return None
    year, q = int(m.group(1)), int(m.group(2))
    start = date(year, 3 * q - 2, 1)
    end = date(year + (q == 4), 1 if q == 4 else 3 * q + 1, 1) - timedelta(days=1)
    return start, end


def follow_up_dispositions(root):
    """Record filename to disposition, from the newest decision follow-up output."""
    base = root / "loops" / "decision-follow-up"
    try:
        state = json.loads((base / "state.json").read_text(encoding="utf-8"))
        text = (base / f"{state['last_run']}.md").read_text(encoding="utf-8")
    except (OSError, ValueError, KeyError):
        return {}
    return {c[1]: c[5] for c in table_rows(text, "Decision") if len(c) == 7}


def check(root):
    root = Path(root)
    problems = []
    state_path = root / "loops" / LOOP / "state.json"
    if not state_path.exists():
        return [f"loops/{LOOP}/state.json is missing"]
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"state.json is not valid JSON: {e}"]
    for key in ("loop", "last_run", "next_run", "quarter", "operator", "reviewed", "open"):
        if key not in state:
            problems.append(f"state.json: key '{key}' is missing")
    if problems:
        return problems
    if state["loop"] != LOOP:
        problems.append(f"state.json: loop is '{state['loop']}', expected '{LOOP}'")
    last, nxt = parse_date(state["last_run"]), parse_date(state["next_run"])
    if not last:
        return problems + ["state.json: last_run is not a date"]
    if not nxt or nxt < last + timedelta(days=60):
        problems.append("state.json: next_run must be a date at least 60 days after last_run (quarterly)")
    window = quarter_range(state["quarter"])
    if not window:
        return problems + [f"state.json: quarter '{state['quarter']}' is not like 2026-Q3"]
    if window[1] >= last:
        problems.append(f"state.json: quarter {state['quarter']} has not ended by {state['last_run']}")

    out_path = state_path.parent / f"{state['last_run']}.md"
    if not out_path.exists():
        return problems + [f"maker output {out_path.name} is missing for last_run {state['last_run']}"]
    text = out_path.read_text(encoding="utf-8")
    if parse_date(line_value(text, "As of")) != last:
        problems.append(f"{out_path.name}: 'As of:' line must equal state last_run {state['last_run']}")
    if line_value(text, "Quarter") != state["quarter"]:
        problems.append(f"{out_path.name}: 'Quarter:' must equal state quarter {state['quarter']}")
    if line_value(text, "Input") != "decisions/LOG.md":
        problems.append(f"{out_path.name}: 'Input:' must name decisions/LOG.md, the Team Loop decision log")

    log = read_log(root, problems, lambda cells, record: {
        "date": parse_date(cells[0]), "decision": cells[1], "decider": cells[2],
        "status": cells[4], "supersedes": cells[6], "record": record})
    deciders = {r["decider"] for r in log}
    operator = line_value(text, "Operator")
    if not operator or operator != state["operator"]:
        problems.append(f"{out_path.name}: 'Operator:' must equal state operator '{state['operator']}'")
    elif operator not in deciders:
        problems.append(f"{out_path.name}: operator '{operator}' is not a decider in decisions/LOG.md")

    in_scope = {r["record"]: r for r in log
                if r["record"] and r["date"] and window[0] <= r["date"] <= window[1]
                and r["status"] in ("decided", "superseded")}
    superseded_by = {}
    for r in log:
        if r["supersedes"] and r["record"]:
            superseded_by[r["supersedes"]] = r["record"].removesuffix(".md")
    dispositions = follow_up_dispositions(root)

    seen, order, pending = {}, [], set()
    for cells in table_rows(text, "Decision"):
        if len(cells) != 7:
            problems.append(f"{out_path.name}: row has {len(cells)} cells, expected 7: {cells[:1]}")
            continue
        decision, record, decider, outcome, question, call, note = cells
        if record in seen:
            problems.append(f"{record}: reviewed twice")
            continue
        seen[record] = outcome
        row = in_scope.get(record)
        if not row:
            problems.append(f"{record}: not a decided or superseded decision in {state['quarter']} in the log")
            continue
        if decision != row["decision"]:
            problems.append(f"{record}: decision text differs from the log")
        if decider != row["decider"]:
            problems.append(f"{record}: decider differs from the log")
        want = "superseded" if row["status"] == "superseded" else dispositions.get(record, "not-reviewed")
        if outcome != want:
            problems.append(f"{record}: outcome '{outcome}' should be '{want}' (from the log and the decision follow-up output)")
        order.append(GROUPS.index(outcome) if outcome in GROUPS else -1)
        if outcome not in GROUPS:
            problems.append(f"{record}: outcome '{outcome}' is not one of {GROUPS}")
        if question != QUESTION:
            problems.append(f"{record}: question must be '{QUESTION}'")
        if call not in CALLS:
            problems.append(f"{record}: operator call '{call}' is not one of {sorted(CALLS)}")
            continue
        has_note = note.strip("- ") != ""
        if call == "pending":
            pending.add(record)
        if (call == "n/a") != (outcome == "superseded"):
            problems.append(f"{record}: call 'n/a' is for superseded decisions only, and they must use it")
        if call in ("change", "stop") and not has_note:
            problems.append(f"{record}: '{call}' needs a note saying what changes")
        if call == "keep" and outcome == "reverse" and not has_note:
            problems.append(f"{record}: 'keep' against a reverse outcome needs a note saying why")
        if outcome == "superseded" and record.removesuffix(".md") in superseded_by \
                and superseded_by[record.removesuffix(".md")] not in note:
            problems.append(f"{record}: note must name the record that supersedes it, {superseded_by[record.removesuffix('.md')]}")

    for record in sorted(set(in_scope) - set(seen)):
        problems.append(f"{record}: decided in {state['quarter']} but missing from the review")
    if order != sorted(order):
        problems.append(f"{out_path.name}: rows must be grouped in this order: {', '.join(GROUPS)}")
    counts = ", ".join(f"{g} {sum(1 for o in seen.values() if o == g)}" for g in GROUPS)
    if line_value(text, "Groups") != counts:
        problems.append(f"{out_path.name}: 'Groups:' must read '{counts}'")
    if set(state["reviewed"]) != set(seen):
        problems.append("state.json: reviewed does not match the review rows")
    if set(state["open"]) != pending:
        problems.append("state.json: open does not match rows with operator call pending")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check.py <workspace-dir>")
    found = check(sys.argv[1])
    for p in found:
        print(p)
    sys.exit(1 if found else 0)
