#!/usr/bin/env python3
"""Checker for the weekly metric review loop. Stdlib only, no model calls.

Usage: python3 check.py <workspace-dir>
Prints one problem per line and exits 1 if there are any. Exits 0 when clean.

It recomputes every week-over-week change from metrics/values.csv, applies the
thresholds in metrics/definitions.md, and verifies the maker's output
(loops/weekly-metric-review/<last_run>.md) and state file against SKILL.md.
"""
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

LOOP = "weekly-metric-review"
STATUSES = {"steady", "explained", "unexplained"}
DATE = r"\d{4}-\d{2}-\d{2}"
EVIDENCE = [
    re.compile(r"^\[(source|ingestion)/[^\]]*\]\(\.\./(source|ingestion)/[^)]+\)$"),
    re.compile(rf"^\((stakeholder-verbal|intuition|hub),\s*[^,)]+,\s*{DATE}\)$"),
    re.compile(r"^\(industry-knowledge\)$"),
    re.compile(r"^\(chat, no artifact\)$"),
]


def parse_date(text):
    try:
        return date.fromisoformat(str(text).strip())
    except ValueError:
        return None


def table_rows(text, header_start):
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


def number(text):
    try:
        return float(str(text).strip())
    except ValueError:
        return None


def read_definitions(root, problems):
    path = root / "metrics" / "definitions.md"
    if not path.exists():
        problems.append("metrics/definitions.md is missing")
        return {}
    defs = {}
    for cells in table_rows(path.read_text(encoding="utf-8"), "Metric"):
        if len(cells) != 5 or number(cells[4]) is None or not cells[3]:
            problems.append(f"metrics/definitions.md: bad row {cells[:1]} (need 5 cells, an owner and a numeric threshold)")
            continue
        defs[cells[0]] = {"owner": cells[3], "threshold": number(cells[4])}
    return defs


def read_values(root, problems):
    path = root / "metrics" / "values.csv"
    if not path.exists():
        problems.append("metrics/values.csv is missing")
        return {}, []
    values, weeks = {}, set()
    with path.open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            v, d = number(r.get("value")), parse_date(r.get("week_start", ""))
            if v is None or not d:
                problems.append(f"metrics/values.csv: bad row {r}")
                continue
            values[(r["metric"], d)] = v
            weeks.add(d)
    return values, sorted(weeks)[-2:]


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
    for key in ("loop", "last_run", "next_run", "reviewed", "unexplained"):
        if key not in state:
            problems.append(f"state.json: key '{key}' is missing")
    if problems:
        return problems
    if state["loop"] != LOOP:
        problems.append(f"state.json: loop is '{state['loop']}', expected '{LOOP}'")
    last, nxt = parse_date(state["last_run"]), parse_date(state["next_run"])
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

    defs = read_definitions(root, problems)
    values, weeks = read_values(root, problems)
    if len(weeks) < 2:
        return problems + ["metrics/values.csv: needs values for at least two weeks"]
    prev_week, this_week = weeks
    if this_week > last:
        problems.append(f"metrics/values.csv: newest week {this_week} is after last_run")
    m = re.search(rf"^Weeks compared:\s*({DATE}) and ({DATE})\s*$", out_text, re.M)
    if not m or (parse_date(m.group(1)), parse_date(m.group(2))) != (prev_week, this_week):
        problems.append(f"{out_path.name}: 'Weeks compared:' must be {prev_week} and {this_week}")

    seen, unexplained = set(), set()
    for cells in table_rows(out_text, "Metric"):
        if len(cells) != 8:
            problems.append(f"{out_path.name}: row has {len(cells)} cells, expected 8: {cells[:1]}")
            continue
        metric, lw, tw, chg, status, why, evidence, step = cells
        evidence = evidence.strip("`")
        if metric in seen:
            problems.append(f"{metric}: reviewed twice")
            continue
        seen.add(metric)
        if metric not in defs:
            problems.append(f"{metric}: not in metrics/definitions.md (invented metric)")
            continue
        if (metric, prev_week) not in values or (metric, this_week) not in values:
            problems.append(f"{metric}: no value in metrics/values.csv for both weeks")
            continue
        want_l, want_t = values[(metric, prev_week)], values[(metric, this_week)]
        if number(lw) is None or abs(number(lw) - want_l) > 1e-9:
            problems.append(f"{metric}: last week value '{lw}' differs from values.csv ({want_l:g})")
        if number(tw) is None or abs(number(tw) - want_t) > 1e-9:
            problems.append(f"{metric}: this week value '{tw}' differs from values.csv ({want_t:g})")
        if want_l == 0:
            moved = want_t != 0
            if chg != "n/a":
                problems.append(f"{metric}: last week is zero, change must be 'n/a'")
        else:
            pct = (want_t - want_l) / abs(want_l) * 100
            moved = abs(pct) > defs[metric]["threshold"]
            if number(chg) is None or abs(number(chg) - round(pct, 1)) > 0.05:
                problems.append(f"{metric}: change '{chg}' should be {pct:.1f}")
        if status not in STATUSES:
            problems.append(f"{metric}: status '{status}' is not one of {sorted(STATUSES)}")
            continue
        known = any(p.match(evidence) for p in EVIDENCE)
        if evidence not in ("Unknown", "-") and not known:
            problems.append(f"{metric}: evidence '{evidence}' is not a provenance tag, Unknown or '-'")
        if not moved:
            if status != "steady":
                problems.append(f"{metric}: inside its threshold, status must be steady")
            continue
        if status == "steady":
            problems.append(f"{metric}: moved past its {defs[metric]['threshold']:g}% threshold, cannot be steady")
        elif status == "explained":
            if not known:
                problems.append(f"{metric}: 'explained' needs a provenance-tagged cause, not '{evidence}'")
            if not why.strip("- "):
                problems.append(f"{metric}: 'explained' needs an explanation")
        else:
            unexplained.add(metric)
            if evidence != "Unknown":
                problems.append(f"{metric}: has evidence, so status should be explained")
            if defs[metric]["owner"] not in step:
                problems.append(f"{metric}: unexplained move must name its owner {defs[metric]['owner']} in Next step")
            if not any((parse_date(d) or last) > last for d in re.findall(DATE, step)):
                problems.append(f"{metric}: unexplained move needs a check date after {state['last_run']} in Next step")

    for metric in sorted(set(defs) - seen):
        problems.append(f"{metric}: defined but missing from the output")
    if set(state["reviewed"]) != seen:
        problems.append("state.json: reviewed does not match the output rows")
    if set(state["unexplained"]) != unexplained:
        problems.append("state.json: unexplained does not match rows with status unexplained")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check.py <workspace-dir>")
    found = check(sys.argv[1])
    for p in found:
        print(p)
    sys.exit(1 if found else 0)
