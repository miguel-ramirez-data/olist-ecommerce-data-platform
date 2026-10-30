"""Database helpers."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import psycopg

from olist_platform.config import DatabaseConfig


@contextmanager
def connect(cfg: DatabaseConfig) -> Iterator[psycopg.Connection]:
    """Open a connection that commits on success and rolls back on error."""
    conn = psycopg.connect(cfg.dsn)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
