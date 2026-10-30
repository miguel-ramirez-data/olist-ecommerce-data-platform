"""Integration tests: require the PostgreSQL container (docker compose up -d)."""

import psycopg
import pytest

from olist_platform.config import load_settings
from olist_platform.db import connect

EXPECTED_SCHEMAS = {"raw", "staging", "marts", "audit"}


def _db_available() -> bool:
    try:
        with connect(load_settings().db):
            return True
    except psycopg.OperationalError:
        return False


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not _db_available(), reason="PostgreSQL is not running"),
]


def test_layer_schemas_exist():
    with connect(load_settings().db) as conn:
        rows = conn.execute("SELECT schema_name FROM information_schema.schemata").fetchall()
    assert {r[0] for r in rows} >= EXPECTED_SCHEMAS


def test_load_audit_table_exists():
    with connect(load_settings().db) as conn:
        cols = conn.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'audit' AND table_name = 'load_runs'
            """
        ).fetchall()
    assert {"run_id", "source_table", "batch_date", "rows_loaded", "status"} <= {c[0] for c in cols}
