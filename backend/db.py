"""
AWS Atlas Pro - Private persistence layer.

Privacy model
-------------
100% private: the DB lives on the server (or in-memory on read-only serverless
filesystems) and is never exposed to clients. The FastAPI backend is the only
process that can read/write it. Frontends never touch the DB — they call the
backend API, which is the intended data path:
    frontend -> API -> backend -> DB -> response -> frontend

Persistence
-----------
Two drivers, selected by environment (never committed):
  - SQLite (default) .......... local / Docker / self-hosted.
       Path configurable via ATLAS_DB_PATH.
  - Turso / libSQL ............ durable, serverless-persistent (recommended
       for Vercel). Enabled by setting ATLAS_DB_URL (and ATLAS_DB_AUTH_TOKEN).
       Uses libsql_client.dbapi2 — a drop-in sqlite3 replacement, so the
       schema and every query are identical.
  - Fallback ................. if neither store is writable, an in-memory
       SQLite DB keeps every endpoint working (data resets on cold start).

The API layer and schema are driver-agnostic.
"""
import json
import logging
import os
import sqlite3
import threading
from pathlib import Path

logger = logging.getLogger("atlas.db")

DB_PATH_ENV = "ATLAS_DB_PATH"
DEFAULT_DB_DIR = Path(__file__).resolve().parent.parent / "data"
TURSO_URL_ENV = "ATLAS_DB_URL"
TURSO_TOKEN_ENV = "ATLAS_DB_AUTH_TOKEN"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS user_state (
    user_id    TEXT PRIMARY KEY,
    learned    TEXT NOT NULL DEFAULT '[]',
    quiz_best  INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

_lock = threading.Lock()
_conn = None
_is_file = False
_ephemeral = False


def db_path() -> str:
    """Resolve the configured DB path.

    Order: explicit ATLAS_DB_PATH -> Turso URL -> Vercel serverless (/tmp is
    the only guaranteed-writable dir) -> project-local data dir (local/Docker).
    """
    env = os.getenv(DB_PATH_ENV)
    if env:
        return env
    if os.getenv(TURSO_URL_ENV):  # durable serverless store
        return os.getenv(TURSO_URL_ENV)
    if os.getenv("VERCEL"):  # serverless functions: /var/task may be read-only
        return "/tmp/atlas.db"
    return str(DEFAULT_DB_DIR / "atlas.db")


def _turso_connect(url: str) -> sqlite3.Connection:
    """Open a durable Turso/libSQL connection (drop-in sqlite3 replacement)."""
    from libsql_client import dbapi2 as libsql  # lazy: optional dependency

    token = os.getenv(TURSO_TOKEN_ENV)
    conn = libsql.connect(url, auth_token=token or None, check_same_thread=False, timeout=10.0)
    conn.row_factory = libsql.Row
    return conn


def _connect() -> sqlite3.Connection:
    """Open (once) the configured store, falling back to in-memory."""
    global _conn, _is_file, _ephemeral
    if _conn is not None:
        return _conn

    path = db_path()
    turso = bool(os.getenv(TURSO_URL_ENV))
    try:
        if turso:
            conn = _turso_connect(path)
        else:
            if path != ":memory:":
                Path(path).parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA busy_timeout = 5000")  # wait on locks, don't 500
        conn.executescript(_SCHEMA)
        conn.commit()
        _is_file = True
        _ephemeral = False
    except Exception as exc:
        # Read-only / unwritable filesystem (Vercel serverless) or Turso
        # unreachable: keep the API alive with an in-memory DB. Data resets
        # between cold starts.
        logger.warning("db unavailable at %s (%r); falling back to in-memory", path, exc)
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.executescript(_SCHEMA)
        conn.commit()
        _is_file = False
        _ephemeral = True
    _conn = conn
    return _conn


def status() -> dict:
    """Return DB connection status (used by /api/v1/db)."""
    _connect()
    return {
        "driver": "turso" if os.getenv(TURSO_URL_ENV) else "sqlite",
        "persistent": _is_file,
        "ephemeral": _ephemeral,
        "path": "(in-memory)" if not _is_file else db_path(),
    }


def get_user_state(user_id: str):
    """Read a user's saved state, or None if never saved."""
    conn = _connect()
    with _lock:
        row = conn.execute(
            "SELECT learned, quiz_best FROM user_state WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    if row is None:
        return None
    try:
        learned = json.loads(row["learned"])
    except (TypeError, ValueError):
        learned = []
    return {"user_id": user_id, "learned": learned, "quiz_best": int(row["quiz_best"])}


def upsert_user_state(user_id: str, learned, quiz_best: int) -> dict:
    """Insert or replace a user's saved state; returns the new state."""
    conn = _connect()
    with _lock:
        conn.execute(
            "INSERT INTO user_state (user_id, learned, quiz_best, updated_at) "
            "VALUES (?, ?, ?, datetime('now')) "
            "ON CONFLICT(user_id) DO UPDATE SET "
            "  learned = excluded.learned,"
            "  quiz_best = excluded.quiz_best,"
            "  updated_at = datetime('now')",
            (user_id, json.dumps(list(learned)), int(quiz_best)),
        )
        conn.commit()
    return get_user_state(user_id)


def delete_user_state(user_id: str) -> bool:
    """Delete a user's saved state. Returns True if a row was removed."""
    conn = _connect()
    with _lock:
        cur = conn.execute("DELETE FROM user_state WHERE user_id = ?", (user_id,))
        conn.commit()
    return cur.rowcount > 0
