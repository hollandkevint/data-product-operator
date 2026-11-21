# Decision log

Append only. One row per decision. The evidence cell holds a link to the decision record, a provenance tag from `_SCHEMA.md`, or `Unknown`. Status is `pending`, `decided`, or `superseded`.

| Date | Decision | Decider | Evidence | Status | Review date | Supersedes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-07-10 | Refresh the feed every day | Ana Reyes | [record](./2026-07-10-daily-refresh.md) | superseded | 2026-08-01 | |
| 2026-08-04 | Move the weekly refresh from Monday to Friday | Ana Reyes | [record](./2026-08-04-friday-refresh.md) | decided | 2026-09-15 | 2026-07-10-daily-refresh |
| 2026-09-01 | Retire the legacy export of the claims-lag table | Ana Reyes | [record](./2026-09-01-retire-lag-export.md) | decided | 2026-10-30 | |
| 2026-09-20 | Define readmission as a return within 30 days | Priya Nair | [record](./2026-09-20-thirty-day-window.md) | decided | 2026-11-10 | |
| 2026-11-02 | Pause new consumer onboarding until the data contract is signed | Priya Nair | [record](./2026-11-02-pause-onboarding.md) | decided | 2027-01-15 | |
| 2026-11-05 | Adopt a vendor-neutral terminology table | Priya Nair | [record](./2026-11-05-terminology-table.md) | pending | 2026-11-12 | |
