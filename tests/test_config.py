from pathlib import Path

import pytest

from olist_platform.config import load_settings


def test_defaults_match_docker_compose():
    s = load_settings(env={})
    assert s.db.host == "localhost"
    assert s.db.port == 5432
    assert s.db.name == "olist"
    assert s.raw_schema == "raw"


def test_env_overrides():
    s = load_settings(
        env={
            "POSTGRES_HOST": "db",
            "POSTGRES_PORT": "6543",
            "POSTGRES_DB": "warehouse",
            "OLIST_DATA_DIR": "/tmp/olist",
        }
    )
    assert (s.db.host, s.db.port, s.db.name) == ("db", 6543, "warehouse")
    assert s.data_dir == Path("/tmp/olist")


def test_invalid_port_raises():
    with pytest.raises(ValueError, match="POSTGRES_PORT"):
        load_settings(env={"POSTGRES_PORT": "not-a-number"})


def test_password_not_in_repr():
    s = load_settings(env={"POSTGRES_PASSWORD": "super-secret"})
    assert "super-secret" not in repr(s.db)
