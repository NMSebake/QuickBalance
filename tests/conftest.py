"""Pytest configuration for an isolated, disposable database."""

import os
import shutil
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def pytest_configure(config):
    """Create and select a seeded database before test modules are imported."""
    database_directory = Path(tempfile.mkdtemp(prefix="quickbalance-tests-"))
    database_path = database_directory / "quickbalance-test.db"

    os.environ["QUICKBALANCE_DATABASE_PATH"] = str(database_path)
    config._quickbalance_test_database_directory = database_directory

    import create_database

    create_database.DATABASE_PATH = database_path
    create_database.create_database()


def pytest_unconfigure(config):
    """Remove the disposable database once the test session has finished."""
    database_directory = getattr(
        config,
        "_quickbalance_test_database_directory",
        None,
    )
    if database_directory:
        shutil.rmtree(database_directory, ignore_errors=True)
