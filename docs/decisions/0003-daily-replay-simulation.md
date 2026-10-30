# 0003 · Simulate daily batches from the static dataset

**Status:** Accepted

## Context
The Olist dataset is a one-off snapshot. Loading it once would not exercise incremental
loading, scheduling, late data or backfills — the hard parts of real pipelines.

## Decision
Build a replay simulator that splits orders (and their items, payments and reviews) by
purchase date and emits one batch per day. The pipeline processes one `batch_date` per run.

## Consequences
- Airflow runs a genuine daily schedule, with backfills over historical dates.
- Loads must be idempotent: re-running a date replaces that date's data, never duplicates it.
- Failure scenarios (missing day, duplicated file) can be injected on purpose and tested.
