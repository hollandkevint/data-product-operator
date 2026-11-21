# Gates

Three manual gates. Each one is a checklist with named acceptance owners. A gate flags; a named person decides. The outcome of any gate is one decision record from [../decisions/_SCHEMA.md](../decisions/_SCHEMA.md) and one row in [../decisions/LOG.md](../decisions/LOG.md).

| Gate | File | Question it answers | Fail action |
| --- | --- | --- | --- |
| Intake | [discovery.md](./discovery.md) | Should we work on this at all? | Stop or reframe |
| Engineering commitment | [commitment.md](./commitment.md) | Is the spec and data good enough to commit a team? | Back to intake or discovery |
| Controlled launch | [launch.md](./launch.md) | Can this reach a first cohort safely? | Revise or stop |
