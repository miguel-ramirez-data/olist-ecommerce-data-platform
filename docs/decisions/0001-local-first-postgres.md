# 0001 · Start local-first on PostgreSQL in Docker

**Status:** Accepted

## Context
The end goal is a cloud deployment (Phase 5), but building directly in the cloud makes
every iteration slower and costs money while the pipeline logic is still changing.

## Decision
Develop phases 0–4 against PostgreSQL 16 running in Docker Compose. Keep SQL portable
(ANSI where possible) and keep connection details in environment variables so the
warehouse can be swapped later.

## Consequences
- Anyone can run the whole project with `docker compose up -d`.
- CI can spin up the same database as a service container.
- Moving to Snowflake in Phase 5 requires a new dbt profile and minor SQL dialect changes.
