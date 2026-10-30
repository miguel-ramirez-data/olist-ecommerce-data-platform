-- =============================================================================
-- Runs once, on the first start of the PostgreSQL container.
-- Creates one schema per data layer plus an audit schema for pipeline metadata.
-- =============================================================================

-- Untouched copy of the source files, loaded by the Python ingestion job.
CREATE SCHEMA IF NOT EXISTS raw;

-- Cleaned, typed and renamed source data (dbt staging models).
CREATE SCHEMA IF NOT EXISTS staging;

-- Business-facing star schema: facts and dimensions (dbt marts).
CREATE SCHEMA IF NOT EXISTS marts;

-- Pipeline metadata: one row per load attempt.
CREATE SCHEMA IF NOT EXISTS audit;

CREATE TABLE IF NOT EXISTS audit.load_runs (
    run_id        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_table  TEXT        NOT NULL,
    batch_date    DATE        NOT NULL,
    source_file   TEXT,
    rows_loaded   INTEGER     NOT NULL DEFAULT 0,
    status        TEXT        NOT NULL
        CHECK (status IN ('running', 'success', 'failed', 'skipped')),
    error_message TEXT,
    started_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at   TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_load_runs_table_date
ON audit.load_runs (source_table, batch_date);
