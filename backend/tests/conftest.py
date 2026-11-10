import os
import tempfile
from pathlib import Path

# Force automated tests to use an isolated SQLite database.
_test_db_dir = tempfile.mkdtemp(prefix="sentinelai-pytest-")

os.environ["DATABASE_URL"] = ""
os.environ["DATABASE_PATH"] = str(
    Path(_test_db_dir) / "sentinelai_test.db"
)
