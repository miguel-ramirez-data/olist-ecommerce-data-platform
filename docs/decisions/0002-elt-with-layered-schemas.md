# 0002 · ELT with layered schemas and dbt

**Status:** Accepted

## Context
Source files contain duplicates, missing values and Portuguese labels. If cleaning
happens during the load, bad rows break the job and the original data is lost.

## Decision
Use ELT: load files as-is into `raw`, then transform in the database with dbt:
`raw` → `staging` (typed, renamed, deduplicated) → `marts` (star schema).
Every load attempt is recorded in `audit.load_runs`.

## Consequences
- Raw data can always be re-processed after a logic change.
- Transformations are version-controlled SQL with tests and lineage docs.
- Requires discipline: no business logic in the ingestion code.
