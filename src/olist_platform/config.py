"""Runtime configuration loaded from environment variables.

All settings have local-development defaults that match ``docker-compose.yml``,
so the project runs out of the box. In any shared environment, override them
through a ``.env`` file or real environment variables — never hard-code secrets.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def dsn(self) -> str:
        """libpq connection string (password intentionally not logged anywhere)."""
        return (
            f"host={self.host} port={self.port} dbname={self.name} "
            f"user={self.user} password={self.password}"
        )

    def __repr__(self) -> str:  # keep secrets out of logs and tracebacks
        return (
            f"DatabaseConfig(host={self.host!r}, port={self.port}, "
            f"name={self.name!r}, user={self.user!r}, password='***')"
        )


@dataclass(frozen=True)
class Settings:
    db: DatabaseConfig
    data_dir: Path
    raw_schema: str = "raw"


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    """Build settings from ``env`` (defaults to ``os.environ``)."""
    env = os.environ if env is None else env

    port_raw = env.get("POSTGRES_PORT", "5432")
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise ValueError(f"POSTGRES_PORT must be an integer, got {port_raw!r}") from exc

    db = DatabaseConfig(
        host=env.get("POSTGRES_HOST", "localhost"),
        port=port,
        name=env.get("POSTGRES_DB", "olist"),
        user=env.get("POSTGRES_USER", "olist"),
        password=env.get("POSTGRES_PASSWORD", "olist"),
    )
    data_dir = Path(env.get("OLIST_DATA_DIR", str(PROJECT_ROOT / "data")))
    return Settings(db=db, data_dir=data_dir)
