# Architecture Decision Records

Short notes explaining *why* the project is built the way it is.
Format: context → decision → consequences.

| # | Decision | Status |
|---|----------|--------|
| [0001](0001-local-first-postgres.md) | Start local-first on PostgreSQL in Docker | Accepted |
| [0002](0002-elt-with-layered-schemas.md) | ELT with `raw` / `staging` / `marts` layers and dbt | Accepted |
| [0003](0003-daily-replay-simulation.md) | Simulate daily batches from the static dataset | Accepted |
