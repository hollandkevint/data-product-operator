# Team Loop

Formerly dpm_os. Part of [Data Product Operator](../README.md); the repo root README covers the full plugin.

An operating system for a data product operator. One markdown repo per product decision: seven context files, three manual gates, one weekly packet, one append-only decision log, and a validator that keeps every claim tagged with its source. Built for Claude Code. No database, no agents beyond one initializer, nothing that runs without a person.

## The habit loop

1. **Monday: the packet.** One page. Decisions requested first, then changed evidence, then blockers by owner.
2. **When a decision is due: the gate.** Intake, engineering commitment, or controlled launch. A checklist with named acceptance owners. It flags; a person decides.
3. **Friday: the log.** One row per decision, one record per decision, one row per risk. Run the maintenance checklist.

## Install

Install the plugin in Claude Code, then run the skill in the project that will hold the instance:

```text
/plugin marketplace add hollandkevint/data-product-operator
/plugin install data-product-operator@data-product-operator
/data-product-operator:team-loop
```

To copy the skill instead, upgrade an older instance, or uninstall, see [docs/install.md](docs/install.md).

## What you get

```text
INDEX.md                 current decision + area table
CLAUDE.md                operating manual for any agent
context/                 strategy, product, consumers, decision rights, data contract, metrics, boundaries
rules/                   intake, commitment, launch gates
packets/                 weekly decision packet template
decisions/               schema, log, one record per decision
risks/                   risk log
source/  ingestion/      verbatim inputs and the notes that cite them
maintenance/             weekly checklist, capability scorecard, owner guide
scripts/validate.py      required files, links, decision fields, provenance tags
```

## Where it comes from

The gates, packet, and decision log encode the Data Product Operating System (DPOS): the handoff between roles is the unit that gets engineered. The analysis skills the initializer points at ship in the same plugin. The [job map](../README.md#jobs-and-skills) lists them.

## Sample grader

A harness is what makes an agent useful to one team: the operating folder, the data definitions it works from, and the answers it writes. `grader/` shows how to tell whether a change to a harness is an improvement. It holds 28 questions a healthcare data team asks every week (cohort counts, rates, utilization by period, drug exposure), each with a known-correct answer.

- **Data.** OHDSI Eunomia GiBleed: an OMOP CDM 5.3 extract of 2,694 synthetic Synthea patients, Apache-2.0, no PHI. `grader/data.py` downloads a 6.9 MB zip pinned by commit and SHA-256 and loads it into DuckDB. No data is committed.
- **Answer key.** Every answer comes from a SQL file in `grader/key/`. `grader/answer_key.json` stores only the resulting aggregates. Counts score exact; rates and means score within a stated tolerance.
- **Harnesses.** `grader/harnesses/base` is a team-loop instance with its data contract filled in, plus one SQL answer per question. A specialized harness names `base` as its parent and holds only the files it overrides. Everything else falls back to base.
- **Ship rule.** A specialized harness ships only if it beats base on its own slice of questions and gets every item right that base gets right. Otherwise base stays the default.

The demo runs base and two candidates. `cohorts` makes condition cohorts include descendant concepts: its slice goes from 4/8 to 8/8, nothing else moves, and it ships. `utilization` fixes its 3 failing items, but it also narrows the shared study population to its own analysis window. That breaks 8 items in other slices, and the ship rule rejects it. The full log is [grader/RUNS.md](grader/RUNS.md).

```bash
pip install -r team-loop/grader/requirements.txt
python3 team-loop/grader/data.py              # fetch, verify checksum, load DuckDB
python3 team-loop/grader/grade.py demo        # score every harness, rewrite grader/RUNS.md
python3 team-loop/grader/grade.py ship cohorts
```

The committed SQL in each harness is what an agent wrote under that harness, and the default run replays it, so no model or API key is needed. `python3 team-loop/grader/grade.py live <harness>` reruns the agent: it writes the resolved harness to a temp folder, has `claude -p` write fresh SQL for that harness's questions, and copies the SQL back. The replay then scores it. Live mode needs the Claude Code CLI and a signed-in account, and each run costs money. Tests never call it. `--dry-run` shows what it would do.

**Limit.** Public data is cleaner than real client data. This set is synthetic, records one visit type, and ships the vocabulary tables every question needs. A client extract will fail in ways these 28 questions do not test. Each team writes its own grader questions against its own data.

## Verify

```bash
python3 -m unittest discover -s tests
python3 skills/team-loop/scaffold/scripts/validate.py skills/team-loop/scaffold
```

Run these from the repo root. The grader's end-to-end tests skip until `python3 team-loop/grader/data.py` has run.

## License

Apache-2.0. See [LICENSE](LICENSE).
