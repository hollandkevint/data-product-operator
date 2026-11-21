#!/usr/bin/env python3
"""Checker for the data quality watch loop. Stdlib only, no model calls.

Usage: python3 check.py <workspace-dir>
Prints one problem per line and exits 1 if there are any. Exits 0 when clean.

It recomputes every freshness, volume, null and schema check from
quality/expectations.json and quality/observed.json, then verifies the maker's
report (loops/data-quality-watch/<last_run>.md) and state file against SKILL.md.
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

LOOP = "data-quality-watch"
DATE = r"\d{4}-\d{2}-\d{2}"


def parse_date(text):
    try:
        return date.fromisoformat(str(text).strip())
    except ValueError:
        return None


def parse_time(text):
    try:
        return datetime.fromisoformat(str(text).replace("Z", "+00:00"))
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


def load_json(path, problems, label):
    if not path.exists():
        problems.append(f"{label} is missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        problems.append(f"{label} is not valid JSON: {e}")
        return None


def expected_checks(exp, obs, observed_at, problems, name):
    """Return {check name: (expected text, observed text, passed)} for one table."""
    out = {}
    loaded = parse_time(obs.get("loaded_at"))
    if not loaded or not observed_at:
        problems.append(f"{name}: loaded_at or observed_at is not a timestamp")
    else:
        age = (observed_at - loaded).total_seconds() / 3600
        out["freshness"] = (f"<= {exp['max_age_hours']:g} h", f"{age:.1f} h", age <= exp["max_age_hours"])
    rows = obs.get("rows")
    out["volume"] = (f"{exp['min_rows']} to {exp['max_rows']} rows", f"{rows} rows",
                     isinstance(rows, (int, float)) and exp["min_rows"] <= rows <= exp["max_rows"])
    for col, limit in sorted(exp.get("max_null_pct", {}).items()):
        pct = obs.get("null_pct", {}).get(col)
        if pct is None:
            problems.append(f"{name}: observed.json has no null_pct for column {col}")
            continue
        out[f"nulls:{col}"] = (f"<= {limit:.1f}%", f"{pct:.1f}%", pct <= limit)
    want, got = exp["columns"], obs.get("columns", {})
    diff = [f"missing {c}" for c in sorted(set(want) - set(got))]
    diff += [f"new {c}" for c in sorted(set(got) - set(want))]
    diff += [f"{c} {want[c]} to {got[c]}" for c in sorted(set(want) & set(got)) if want[c] != got[c]]
    out["schema"] = (", ".join(f"{c}:{t}" for c, t in want.items()), "; ".join(diff) or "matches", not diff)
    return out


def check(root):
    root = Path(root)
    problems = []
    state = load_json(root / "loops" / LOOP / "state.json", problems, f"loops/{LOOP}/state.json")
    if state is None:
        return problems
    for key in ("loop", "last_run", "next_run", "checked", "failing"):
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

    out_path = root / "loops" / LOOP / f"{state['last_run']}.md"
    if not out_path.exists():
        return problems + [f"maker output {out_path.name} is missing for last_run {state['last_run']}"]
    out_text = out_path.read_text(encoding="utf-8")
    m = re.search(rf"^As of:\s*({DATE})\s*$", out_text, re.M)
    if not m or parse_date(m.group(1)) != last:
        problems.append(f"{out_path.name}: 'As of:' line must equal state last_run {state['last_run']}")

    exps = load_json(root / "quality" / "expectations.json", problems, "quality/expectations.json")
    obs = load_json(root / "quality" / "observed.json", problems, "quality/observed.json")
    if exps is None or obs is None:
        return problems
    observed_at = parse_time(obs.get("observed_at"))
    if not observed_at or observed_at.date() != last:
        problems.append("quality/observed.json: observed_at must be on the last_run date")

    want = {}
    for table, exp in exps.get("tables", {}).items():
        if table not in obs.get("tables", {}):
            problems.append(f"{table}: declared in expectations.json but missing from observed.json")
            continue
        for check_name, vals in expected_checks(exp, obs["tables"][table], observed_at, problems, table).items():
            want[(table, check_name)] = (vals, exp["owner"])

    seen, failing = set(), set()
    for cells in table_rows(out_text, "Table"):
        if len(cells) != 6:
            problems.append(f"{out_path.name}: row has {len(cells)} cells, expected 6: {cells[:2]}")
            continue
        table, name, expected, observed, result, step = cells
        key = (table, name)
        if key in seen:
            problems.append(f"{table} {name}: reported twice")
            continue
        seen.add(key)
        if key not in want:
            problems.append(f"{table} {name}: not a declared check (invented)")
            continue
        (exp_text, obs_text, passed), owner = want[key]
        if expected != exp_text:
            problems.append(f"{table} {name}: expected '{expected}' should be '{exp_text}'")
        if observed != obs_text:
            problems.append(f"{table} {name}: observed '{observed}' should be '{obs_text}'")
        if result not in ("pass", "fail"):
            problems.append(f"{table} {name}: result '{result}' is not pass or fail")
        elif (result == "pass") != passed:
            problems.append(f"{table} {name}: result is '{result}' but the numbers say {'pass' if passed else 'fail'}")
        if not passed:
            failing.add(f"{table}:{name}")
            if owner not in step:
                problems.append(f"{table} {name}: failing check must name its owner {owner} in Next step")
            if not any((parse_date(d) or last) > last for d in re.findall(DATE, step)):
                problems.append(f"{table} {name}: failing check needs a date after {state['last_run']} in Next step")

    for table, name in sorted(set(want) - seen):
        problems.append(f"{table} {name}: declared check is missing from the report")
    if set(state["checked"]) != {t for t, _ in seen}:
        problems.append("state.json: checked does not match the tables in the report")
    if set(state["failing"]) != failing:
        problems.append("state.json: failing does not match rows with result fail")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check.py <workspace-dir>")
    found = check(sys.argv[1])
    for p in found:
        print(p)
    sys.exit(1 if found else 0)
