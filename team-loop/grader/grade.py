#!/usr/bin/env python3
"""Sample grader: score dpm-os harnesses on 28 data-team questions and apply the ship rule.

    python3 grader/grade.py key                 recompute answer_key.json from key/*.sql
    python3 grader/grade.py run <harness>       score one harness
    python3 grader/grade.py ship <harness>      ship-rule verdict for a specialized harness vs base
    python3 grader/grade.py demo                score every harness, write RUNS.md
    python3 grader/grade.py live <harness>      regenerate a harness's SQL with `claude -p`, then replay
    python3 grader/grade.py materialize <harness> <dir>   write the resolved harness as a dpm-os instance

A harness is a folder under harnesses/: harness.json, context/, definitions/*.sql,
sql/<question-id>.sql. A specialized harness names a parent and holds only the files it
overrides. Any file it does not hold resolves to the nearest ancestor that does, and the
base resolves to the dpm-os scaffold for context files. Replay is the only scorer; live
mode only rewrites SQL files.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import data  # noqa: E402

REPO = HERE.parent
SCAFFOLD = REPO / ".claude" / "skills" / "dpm-os" / "scaffold"
HARNESSES = HERE / "harnesses"
KEY_DIR = HERE / "key"
KEY_FILE = HERE / "answer_key.json"
QUESTIONS_FILE = HERE / "questions.json"
RUNS_FILE = HERE / "RUNS.md"
BASE = "base"


# ---------- questions and key ----------

def questions() -> list[dict]:
    return json.loads(QUESTIONS_FILE.read_text())["questions"]


def answer_key() -> dict:
    return json.loads(KEY_FILE.read_text())["answers"]


def compute_key() -> dict:
    con = data.connect()
    answers = {}
    for q in questions():
        value = con.execute((KEY_DIR / f"{q['id']}.sql").read_text()).fetchone()[0]
        answers[q["id"]] = normalize(value)
    return {
        "dataset": {"url": data.URL, "sha256": data.SHA256},
        "computed_by": "grader/key/<id>.sql",
        "answers": answers,
    }


def normalize(value):
    """Store aggregates as plain JSON numbers: ints stay ints, floats round to 6 places."""
    if value is None:
        return None
    f = float(value)
    return int(f) if f.is_integer() else round(f, 6)


# ---------- harness resolution ----------

def harness_meta(name: str) -> dict:
    path = HARNESSES / name / "harness.json"
    if not path.is_file():
        raise SystemExit(f"no harness named {name!r} under {HARNESSES}")
    return json.loads(path.read_text())


def lineage(name: str) -> list[str]:
    """Return [root, ..., name]. Rejects cycles."""
    chain = []
    cur = name
    while cur:
        if cur in chain:
            raise SystemExit(f"harness inheritance cycle at {cur!r}")
        chain.append(cur)
        cur = harness_meta(cur)["parent"]
    return chain[::-1]


def resolve(name: str) -> dict[str, Path]:
    """Map each relative path to the file that wins: nearest harness first, scaffold last for context/."""
    files: dict[str, Path] = {}
    for rel in (SCAFFOLD / "context").glob("*.md"):
        files[f"context/{rel.name}"] = rel
    for h in lineage(name):
        root = HARNESSES / h
        for p in root.rglob("*"):
            if p.is_file() and p.name != "harness.json":
                files[p.relative_to(root).as_posix()] = p
    return files


def owner(name: str, rel: str) -> str:
    """Which harness supplies this file after resolution."""
    for h in reversed(lineage(name)):
        if (HARNESSES / h / rel).is_file():
            return h
    return "scaffold"


# ---------- replay ----------

def harness_connection(files: dict[str, Path]):
    import duckdb

    con = duckdb.connect()
    con.execute(f"ATTACH '{data.build()}' AS cdm (READ_ONLY)")
    for t in data.TABLES:
        con.execute(f"CREATE VIEW {t} AS SELECT * FROM cdm.main.{t}")
    for rel in sorted(r for r in files if r.startswith("definitions/") and r.endswith(".sql")):
        con.execute(files[rel].read_text())
    return con


def replay(name: str) -> dict[str, dict]:
    """Run every question's SQL for a harness. Returns {id: {value, error, source}}."""
    files = resolve(name)
    con = harness_connection(files)
    out = {}
    for q in questions():
        rel = f"sql/{q['id']}.sql"
        res = {"value": None, "error": None, "source": owner(name, rel) if rel in files else None}
        if rel not in files:
            res["error"] = "no SQL file"
        else:
            try:
                row = con.execute(files[rel].read_text()).fetchone()
                res["value"] = normalize(row[0]) if row else None
            except Exception as e:  # a broken answer is a failed item, not a crashed run
                res["error"] = f"{type(e).__name__}: {str(e).splitlines()[0]}"
        out[q["id"]] = res
    return out


def correct(value, expected, scoring: dict) -> bool:
    if value is None or expected is None:
        return False
    if scoring["type"] == "exact":
        return float(value) == float(expected)
    if scoring["type"] == "tolerance":
        return abs(float(value) - float(expected)) <= scoring["abs"]
    raise ValueError(f"unknown scoring type {scoring['type']!r}")


def score(results: dict[str, dict], key: dict | None = None) -> dict[str, bool]:
    key = key if key is not None else answer_key()
    return {q["id"]: correct(results[q["id"]]["value"], key[q["id"]], q["scoring"]) for q in questions()}


# ---------- ship rule ----------

def ship_verdict(base_pass: dict[str, bool], cand_pass: dict[str, bool], slice_ids: list[str]) -> dict:
    """A specialized harness ships only if it beats base on its slice and breaks nothing base gets right."""
    base_slice = sum(base_pass[i] for i in slice_ids)
    cand_slice = sum(cand_pass[i] for i in slice_ids)
    regressions = sorted(i for i in base_pass if base_pass[i] and not cand_pass[i])
    fixed = sorted(i for i in base_pass if cand_pass[i] and not base_pass[i])
    reasons = []
    if cand_slice <= base_slice:
        reasons.append(f"does not beat base on its slice ({cand_slice} vs {base_slice} of {len(slice_ids)})")
    if regressions:
        reasons.append(f"regresses {len(regressions)} item(s) base gets right: {', '.join(regressions)}")
    return {
        "ship": not reasons,
        "slice_base": base_slice,
        "slice_candidate": cand_slice,
        "slice_size": len(slice_ids),
        "fixed": fixed,
        "regressions": regressions,
        "reasons": reasons,
    }


def slice_ids(slice_name: str) -> list[str]:
    ids = [q["id"] for q in questions() if q["slice"] == slice_name]
    if not ids:
        raise SystemExit(f"no questions in slice {slice_name!r}")
    return ids


def verdict_for(name: str, runs: dict[str, dict] | None = None) -> dict:
    meta = harness_meta(name)
    if not meta.get("parent"):
        raise SystemExit(f"{name!r} is a base harness; the ship rule applies to specialized harnesses")
    runs = runs or {}
    base_pass = score(runs.get(BASE) or replay(BASE))
    cand_pass = score(runs.get(name) or replay(name))
    return ship_verdict(base_pass, cand_pass, slice_ids(meta["slice"]))


# ---------- reporting ----------

def fmt(value) -> str:
    if value is None:
        return "—"
    if isinstance(value, int):
        return str(value)
    return f"{value:.4g}" if abs(value) < 1000 else f"{value:.1f}"


def all_harnesses() -> list[str]:
    names = sorted(p.parent.name for p in HARNESSES.glob("*/harness.json"))
    return [BASE] + [n for n in names if n != BASE]


def render_runs(runs: dict[str, dict]) -> str:
    qs = questions()
    key = answer_key()
    names = list(runs)
    passes = {n: score(runs[n], key) for n in names}
    slices = list(dict.fromkeys(q["slice"] for q in qs))
    lines = [
        "# Grader runs",
        "",
        "Generated by `python3 grader/grade.py demo`. Do not edit by hand.",
        "",
        f"- Dataset: OHDSI Eunomia GiBleed, OMOP CDM 5.3, synthetic (Synthea). SHA-256 `{data.SHA256[:16]}…`",
        f"- Questions: {len(qs)}, answers computed by `grader/key/<id>.sql` into `grader/answer_key.json`",
        "- Mode: replay. Each harness's committed SQL is what an agent wrote under that harness; this run replays it.",
        "",
        "## Ship rule",
        "",
        "A specialized harness ships only if it (1) gets more of its own slice right than base does and",
        "(2) gets every item right that base gets right, in every slice. Otherwise base stays the default.",
        "",
        "## Score by slice",
        "",
        "| Slice | Items | " + " | ".join(names) + " |",
        "| --- | --- | " + " | ".join("---" for _ in names) + " |",
    ]
    for s in slices:
        ids = [q["id"] for q in qs if q["slice"] == s]
        lines.append(f"| {s} | {len(ids)} | " + " | ".join(str(sum(passes[n][i] for i in ids)) for n in names) + " |")
    lines.append(f"| **total** | {len(qs)} | " + " | ".join(f"**{sum(passes[n].values())}**" for n in names) + " |")
    lines += ["", "## Verdicts", ""]
    for n in names[1:]:
        meta = harness_meta(n)
        v = ship_verdict(passes[BASE], passes[n], slice_ids(meta["slice"]))
        word = "SHIP" if v["ship"] else "REJECT"
        lines.append(f"### `{n}`: {word}")
        lines.append("")
        lines.append(meta["summary"])
        lines.append("")
        lines.append(f"- Slice `{meta['slice']}`: {v['slice_base']}/{v['slice_size']} on base, {v['slice_candidate']}/{v['slice_size']} on `{n}`.")
        lines.append(f"- Fixed: {', '.join(v['fixed']) or 'none'}.")
        lines.append(f"- Regressed: {', '.join(v['regressions']) or 'none'}.")
        if v["reasons"]:
            lines.append(f"- Rejected because it {'; and '.join(v['reasons'])}.")
        lines.append("")
    lines += [
        "## Item detail",
        "",
        "`ok` = within the scoring rule. `x` = wrong. Values are the harness's answer.",
        "",
        "| Item | Slice | Scoring | Key | " + " | ".join(names) + " |",
        "| --- | --- | --- | --- | " + " | ".join("---" for _ in names) + " |",
    ]
    for q in qs:
        i = q["id"]
        sc = "exact" if q["scoring"]["type"] == "exact" else f"±{q['scoring']['abs']}"
        cells = []
        for n in names:
            r = runs[n][i]
            mark = "ok" if passes[n][i] else "x"
            shown = "error" if r["error"] else fmt(r["value"])
            cells.append(f"{mark} {shown}")
        lines.append(f"| {i} | {q['slice']} | {sc} | {fmt(key[i])} | " + " | ".join(cells) + " |")
    lines += ["", "Question text lives in `grader/questions.json`.", ""]
    return "\n".join(lines)


# ---------- materialize and live ----------

RUN_SQL = '''#!/usr/bin/env python3
"""Run one SQL file against the grader database with this harness's definitions loaded."""
import sys
from pathlib import Path
import duckdb

HERE = Path(__file__).resolve().parent
con = duckdb.connect()
con.execute("ATTACH '{db}' AS cdm (READ_ONLY)")
for t in {tables!r}:
    con.execute(f"CREATE VIEW {{t}} AS SELECT * FROM cdm.main.{{t}}")
for p in sorted((HERE / "definitions").glob("*.sql")):
    con.execute(p.read_text())
print(con.sql(Path(sys.argv[1]).read_text()))
'''

TASK = """# Grader task

You are working inside a dpm-os instance. Read `CLAUDE.md`, then `context/data-contract.md`.
The definitions in `definitions/*.sql` are already loaded as views and macros.

For each question below, write exactly one SQL file at `sql/<id>.sql`. The file holds one
DuckDB SELECT that returns one row and one column: the answer. Use the definitions where
they apply. Test each file with `python3 run_sql.py sql/<id>.sql`. Do not write the
answers anywhere else.

{questions}
"""


def materialize(name: str, dest: Path, ids: list[str] | None = None) -> Path:
    """Write the resolved harness as a full dpm-os instance: scaffold, then harness files on top."""
    dest = Path(dest)
    shutil.copytree(SCAFFOLD, dest, dirs_exist_ok=True)
    for rel, src in resolve(name).items():
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
    ids = ids or [q["id"] for q in questions()]
    qtext = "\n".join(f"- `{q['id']}`: {q['question']}" for q in questions() if q["id"] in ids)
    (dest / "GRADER_TASK.md").write_text(TASK.format(questions=qtext))
    (dest / "run_sql.py").write_text(RUN_SQL.format(db=data.DB, tables=data.TABLES))
    return dest


def live_targets(name: str) -> list[str]:
    meta = harness_meta(name)
    return [q["id"] for q in questions()] if not meta.get("parent") else slice_ids(meta["slice"])


def live_command() -> list[str]:
    return [
        "claude", "-p", "Do the task in GRADER_TASK.md.",
        "--permission-mode", "acceptEdits",
        "--allowedTools", "Read,Write,Edit,Bash(python3 run_sql.py:*)",
    ]


def live(name: str, dry_run: bool = False) -> list[str]:
    """Regenerate a harness's SQL with claude -p. Writes only that harness's own sql/ files."""
    ids = live_targets(name)
    work = Path(tempfile.mkdtemp(prefix=f"harness-{name}-"))
    materialize(name, work, ids)
    for i in ids:  # the agent writes fresh answers; it does not see the old ones
        (work / "sql" / f"{i}.sql").unlink(missing_ok=True)
    cmd = live_command()
    if dry_run:
        print(f"materialized {name} at {work}\nwould run in that folder: {' '.join(cmd)}")
        return ids
    if shutil.which("claude") is None:
        raise SystemExit("live mode needs the Claude Code CLI (`claude`) on PATH and a signed-in account")
    subprocess.run(cmd, cwd=work, check=True)
    out = HARNESSES / name / "sql"
    out.mkdir(exist_ok=True)
    written = []
    for i in ids:
        src = work / "sql" / f"{i}.sql"
        if src.is_file():
            shutil.copyfile(src, out / f"{i}.sql")
            written.append(i)
    print(f"wrote {len(written)}/{len(ids)} SQL files into {out}")
    return written


# ---------- CLI ----------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("key")
    sub.add_parser("demo")
    for c in ("run", "ship"):
        sub.add_parser(c).add_argument("harness")
    lp = sub.add_parser("live")
    lp.add_argument("harness")
    lp.add_argument("--dry-run", action="store_true", help="materialize and print the command; do not call claude")
    mp = sub.add_parser("materialize")
    mp.add_argument("harness")
    mp.add_argument("dest")
    a = ap.parse_args(argv)

    if a.cmd == "key":
        KEY_FILE.write_text(json.dumps(compute_key(), indent=2) + "\n")
        print(f"wrote {KEY_FILE.relative_to(REPO)}")
    elif a.cmd == "run":
        passes = score(replay(a.harness))
        for i, ok in passes.items():
            print(f"{i} {'ok' if ok else 'x'}")
        print(f"{a.harness}: {sum(passes.values())}/{len(passes)}")
    elif a.cmd == "ship":
        v = verdict_for(a.harness)
        print(json.dumps(v, indent=2))
        return 0 if v["ship"] else 1
    elif a.cmd == "demo":
        runs = {n: replay(n) for n in all_harnesses()}
        RUNS_FILE.write_text(render_runs(runs))
        print(f"wrote {RUNS_FILE.relative_to(REPO)}")
    elif a.cmd == "live":
        live(a.harness, dry_run=a.dry_run)
        if not a.dry_run:
            passes = score(replay(a.harness))
            print(f"{a.harness} after live: {sum(passes.values())}/{len(passes)}")
    elif a.cmd == "materialize":
        print(materialize(a.harness, Path(a.dest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
