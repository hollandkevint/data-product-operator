# DPM OS instance

A markdown workspace for one data product decision. One repo, plain files, git history.

SCAFFOLD_VERSION: 0.1.0

## The habit loop

1. **Monday: the packet.** Copy `packets/_TEMPLATE.md` to `packets/YYYY-MM-DD-weekly-packet.md`. Decisions requested go first.
2. **When a decision is due: the gate.** Open the matching file in `rules/`, fill the evidence table, record the outcome as one decision record and one log row.
3. **Friday: the log.** Run the checklist in `maintenance/INDEX.md`. Append to `decisions/LOG.md` and `risks/LOG.md`.

## How it thinks

- `source/` holds verbatim inputs. `ingestion/` holds notes that cite them. `context/` holds the durable picture.
- Every evidence row ends with a provenance tag or `Unknown`. The enum is in `decisions/_SCHEMA.md`.
- Gates flag. People decide.

## Validation

```bash
python3 scripts/validate.py .
```

Exit 0 means the instance is well-formed. Each finding prints as `path: message`.
