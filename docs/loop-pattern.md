# Loop pattern

A loop is a skill that does one recurring job and checks its own work. Pairing a maker with a checker is a general practice, often called maker/checker loops. One public treatment is Aakash Gupta's [Loops for PMs](https://news.aakashg.com). This repo's version is written from scratch for data product work.

## The five parts

| Part | What it is | Rule |
|---|---|---|
| Maker | The step that produces the output | Names its inputs and writes one dated output file |
| Checker | A script that verifies the output against explicit rules | Stdlib only, deterministic, no model calls. It can reject. |
| State file | `state.json`: what ran, when, what is still open | Written by the maker, cross-checked by the checker |
| Trigger | When the loop runs | A cadence or an event. One line. |
| Demo data | A fake workspace the loop runs on once | Made-up data only. No client names. |

The maker is a model or a person. The checker is not. A model that grades its own work agrees with itself.

## Folder layout

```text
skills/<loop-name>/
  SKILL.md      Maker, Checker, State, Trigger, Demo data sections
  check.py      The checker: python3 check.py <workspace-dir>, exit 1 on any problem
  loop.json     Manifest read by the repo check
  demo/         Fake workspace. Holds the state file and one output file.
```

`loop.json` has these keys:

- `name`: the folder name.
- `trigger`: one line.
- `checker`: the script name, `check.py`.
- `demo`: the demo folder, `demo`.
- `breaks`: a list of `{why, file, find, replace}`. Each one edits a copy of the demo so it should fail. Use at least one.

## How the repo check works

`tests/checks_loops.py` finds every `skills/*/loop.json`. For each loop it:

1. Checks the manifest keys and the five `SKILL.md` headings: Maker, Checker, State, Trigger, Demo data.
2. Runs the checker on `demo/`. It must pass.
3. Applies each break to a copy of `demo/`, runs the checker, and requires it to fail.

A loop whose checker passes everything fails the repo check. So does a break that changes nothing.

## Add a loop

1. Copy the folder layout above.
2. Write the maker steps in `SKILL.md`. List the rules the checker enforces.
3. Write `check.py`. Each rule gets a problem message and a test in `tests/test_loops.py` that breaks that rule.
4. Build `demo/` from made-up data. Include one case for each outcome the loop can produce.
5. List breaks in `loop.json`. Run `python3 -m unittest discover -s tests`.

## Limits

A passing checker means the output follows the rules. It does not mean the judgment inside is right. Evidence can be tagged and still be thin. A named person owns every decision the loop surfaces.

The first loop built on this pattern is [decision follow-up](../skills/decision-follow-up/SKILL.md).
