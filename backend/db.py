"""
AWS Atlas Pro - Private SQLite persistence layer.

Privacy model
-------------
100% private: the DB file lives on the server (or in-memory on read-only
serverless filesystems) and is never exposed to clients. The FastAPI backend
is the only process that can read/write it. Frontends never touch the DB —
they call the backend API, which is the intended data path:
    frontend -> API -> backend -> SQLite -> response -> frontend

Persistence
-----------
Path is configurable with the ATLAS_DB_PATH env var (never committed):
  - default ........ <project>/data/atlas.db   (local / Docker / self-hosted)
  - read-only fs ... falls back to an in-memory SQLite DB so every endpoint
                     keeps working (e.g. Vercel serverless: data resets on
                     cold start there; durable elsewhere).

Swapping to a serverless-persistent store (Turso/libSQL, Postgres) later is a
one-line change in _connect() — the API layer and schema do not change.
"""
import json
import os
import sqlite3
import threading
from pathlib import Path

DB_PATH_ENV = "ATLAS_DB_PATH"
DEFAULT_DB_DIR = Path(__file__).resolve().parent.parent / "data"

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
    """Resolve the configured DB path (env override, else project data dir)."""
    env = os.getenv(DB_PATH_ENV)
    return env if env else str(DEFAULT_DB_DIR / "atlas.db")


def _connect() -> sqlite3.Connection:
    """Open (once) a private SQLite connection, falling back to in-memory."""
    global _conn, _is_file, _ephemeral
    if _conn is not None:
        return _conn

    path = db_path()
    try:
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.executescript(_SCHEMA)
        conn.commit()
        _is_file = path != ":memory:"
        _ephemeral = False
    except Exception:
        # Read-only / unwritable filesystem (Vercel serverless): keep the API
        # alive with an in-memory DB. Data resets between cold starts.
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
        "driver": "sqlite",
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
