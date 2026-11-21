#!/usr/bin/env python3
"""Checker for the agent eval regression loop. Stdlib only, no model calls.

Usage: python3 check.py <workspace-dir>
Prints one problem per line and exits 1 if there are any. Exits 0 when clean.

It rescores two recorded runs (a baseline and a candidate) against
eval/answer_key.json with the rules in eval/questions.json, then verifies the
maker's report (loops/agent-eval-regression/<last_run>.md) and state file.
The set has the shape of team-loop/grader: questions.json, answer_key.json,
one answers file per harness.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

LOOP = "agent-eval-regression"
DATE = r"\d{4}-\d{2}-\d{2}"
SCORING = {"exact", "tolerance", "abstain"}


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


def load_json(path, problems, label):
    if not path.exists():
        problems.append(f"{label} is missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        problems.append(f"{label} is not valid JSON: {e}")
        return None


def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def right(question, key, answers):
    """Score one item. A missing answer is wrong."""
    if question["id"] not in answers:
        return False
    got, want, rule = answers[question["id"]], key.get(question["id"]), question["scoring"]
    if rule["type"] == "abstain":
        return got is None
    if got is None or not is_number(got) or want is None:
        return False
    if rule["type"] == "exact":
        return got == want
    return abs(got - want) <= rule["abs"]


def line_value(text, label):
    m = re.search(rf"^{label}:\s*(.*?)\s*$", text, re.M)
    return m.group(1) if m else None


def id_list(text):
    return [] if text is None or text.lower() == "none" else [s.strip() for s in text.split(",") if s.strip()]


def check(root):
    root = Path(root)
    problems = []
    state = load_json(root / "loops" / LOOP / "state.json", problems, f"loops/{LOOP}/state.json")
    if state is None:
        return problems
    for key in ("loop", "last_run", "next_run", "baseline", "candidate", "verdict", "regressed"):
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
    if state["candidate"] != f"{state['last_run']}.json":
        problems.append(f"state.json: candidate must be {state['last_run']}.json")

    qs = load_json(root / "eval" / "questions.json", problems, "eval/questions.json")
    key = load_json(root / "eval" / "answer_key.json", problems, "eval/answer_key.json")
    base = load_json(root / "eval" / "runs" / state["baseline"], problems, f"eval/runs/{state['baseline']}")
    cand = load_json(root / "eval" / "runs" / state["candidate"], problems, f"eval/runs/{state['candidate']}")
    if None in (qs, key, base, cand):
        return problems

    questions, ids = qs.get("questions", []), [q.get("id") for q in qs.get("questions", [])]
    if len(set(ids)) != len(ids):
        problems.append("eval/questions.json: duplicate question ids")
    for q in questions:
        if q.get("scoring", {}).get("type") not in SCORING:
            problems.append(f"{q.get('id')}: scoring type must be one of {sorted(SCORING)}")
        elif q["scoring"]["type"] == "tolerance" and not is_number(q["scoring"].get("abs")):
            problems.append(f"{q['id']}: tolerance scoring needs a numeric 'abs'")
    if problems:
        return problems
    if not qs.get("owner"):
        problems.append("eval/questions.json: the set needs a named owner")
    answers_key = key.get("answers", {})
    for q in questions:
        if q["id"] not in answers_key:
            problems.append(f"{q['id']}: no answer in eval/answer_key.json")
        elif (q["scoring"]["type"] == "abstain") != (answers_key[q["id"]] is None):
            problems.append(f"{q['id']}: abstain questions have a null key, all others a value")
        elif q["scoring"]["type"] != "abstain" and not is_number(answers_key[q["id"]]):
            problems.append(f"{q['id']}: answer key value must be a number for {q['scoring']['type']} questions")
    pin = key.get("data_pin")
    if not pin:
        problems.append("eval/answer_key.json: data_pin is missing")
    for name, run in (("baseline", base), ("candidate", cand)):
        if run.get("data_pin") != pin:
            problems.append(f"{name} run was scored against different data than the key (data_pin differs)")
        for extra in sorted(set(run.get("answers", {})) - set(ids)):
            problems.append(f"{name} run answers unknown question {extra}")
    if problems:
        return problems

    ok_b = {q["id"]: right(q, answers_key, base["answers"]) for q in questions}
    ok_c = {q["id"]: right(q, answers_key, cand["answers"]) for q in questions}
    regressed = [i for i in ids if ok_b[i] and not ok_c[i]]
    fixed = [i for i in ids if not ok_b[i] and ok_c[i]]
    verdict = "HOLD" if regressed else "PASS"

    out_path = root / "loops" / LOOP / f"{state['last_run']}.md"
    if not out_path.exists():
        return [f"maker output {out_path.name} is missing for last_run {state['last_run']}"]
    text = out_path.read_text(encoding="utf-8")
    if parse_date(line_value(text, "As of")) != last:
        problems.append(f"{out_path.name}: 'As of:' line must equal state last_run {state['last_run']}")
    for label, run, fname in (("Baseline", base, state["baseline"]), ("Candidate", cand, state["candidate"])):
        if line_value(text, label) != f"eval/runs/{fname} ({run.get('harness')})":
            problems.append(f"{out_path.name}: '{label}:' line must be 'eval/runs/{fname} ({run.get('harness')})'")
    if line_value(text, "Data pin") != pin:
        problems.append(f"{out_path.name}: 'Data pin:' must equal the key's data_pin")

    slices = {}
    for q in questions:
        s = slices.setdefault(q["slice"], [0, 0, 0])
        s[0] += 1
        s[1] += ok_b[q["id"]]
        s[2] += ok_c[q["id"]]
    wanted = {name: [str(n) for n in v] for name, v in slices.items()}
    wanted["total"] = [str(len(ids)), str(sum(ok_b.values())), str(sum(ok_c.values()))]
    got = {}
    for cells in table_rows(text, "Slice"):
        if len(cells) != 4:
            problems.append(f"{out_path.name}: score row has {len(cells)} cells, expected 4: {cells[:1]}")
            continue
        got[cells[0]] = cells[1:]
    for name, vals in wanted.items():
        if name not in got:
            problems.append(f"{out_path.name}: slice '{name}' is missing from the score table")
        elif got[name] != vals:
            problems.append(f"{out_path.name}: slice '{name}' scores {got[name]}, rescoring gives {vals} (items, baseline, candidate)")
    for name in sorted(set(got) - set(wanted)):
        problems.append(f"{out_path.name}: slice '{name}' is not in the question set")

    if line_value(text, "Verdict") != verdict:
        problems.append(f"{out_path.name}: verdict must be {verdict} (items the baseline got right and the candidate now gets wrong: {regressed or 'none'})")
    if id_list(line_value(text, "Regressed")) != regressed:
        problems.append(f"{out_path.name}: 'Regressed:' must list {regressed or 'none'}")
    if id_list(line_value(text, "Fixed")) != fixed:
        problems.append(f"{out_path.name}: 'Fixed:' must list {fixed or 'none'}")
    owner = qs.get("owner", "")
    if line_value(text, "Owner") != owner:
        problems.append(f"{out_path.name}: 'Owner:' must be {owner}")
    if verdict == "HOLD":
        step = line_value(text, "Next step") or ""
        if owner not in step:
            problems.append(f"{out_path.name}: HOLD needs a Next step that names the owner {owner}")
        if not any((parse_date(d) or last) > last for d in re.findall(DATE, step)):
            problems.append(f"{out_path.name}: HOLD needs a decision date after {state['last_run']} in Next step")
    if state["verdict"] != verdict:
        problems.append(f"state.json: verdict is '{state['verdict']}', rescoring gives {verdict}")
    if state["regressed"] != regressed:
        problems.append("state.json: regressed does not match the rescored run")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: check.py <workspace-dir>")
    found = check(sys.argv[1])
    for p in found:
        print(p)
    sys.exit(1 if found else 0)
