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
       Uses the official `libsql` client (sqlite3-compatible, qmark params)
       which talks to Turso over HTTPS. (The older `libsql-client` package
       only speaks WebSocket, which Turso no longer accepts — hence 400s.)
  - Fallback ................. if neither store is writable, an in-memory
       SQLite DB keeps every endpoint working (data resets on cold start).

The API layer and schema are driver-agnostic. Rows are read back as dicts
(keyed by column name) regardless of driver.
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
_last_error = None


def _redact(text: str) -> str:
    """Never let a token leak into the public /api/v1/db status."""
    token = os.getenv(TURSO_TOKEN_ENV)
    if token and token in text:
        text = text.replace(token, "***")
    return text


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


def _turso_connect(url: str):
    """Open a durable Turso/libSQL connection over HTTPS.

    Uses the official `libsql` client. Turso no longer accepts the WebSocket
    Hrana handshake (old `libsql-client` gets HTTP 400 "protocol upgrade not
    supported"), so auth_token must be passed as the string used by libsql.
    Normalise `https://` to `libsql://` for a console copy-paste.
    """
    from libsql import connect as libsql_connect  # lazy: optional dependency

    token = os.getenv(TURSO_TOKEN_ENV)
    if url.startswith("https://"):
        url = "libsql://" + url[len("https://"):]
    return libsql_connect(url, auth_token=token or "", timeout=10.0)


def _row_to_dict(cur, row):
    """Turn a fetched row into a column-keyed dict (driver-agnostic).

    sqlite3.Row supports row["col"]; the `libsql` client returns plain tuples,
    so map positional values back to names via cursor.description.
    """
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    cols = [d[0] for d in (cur.description or [])]
    return dict(zip(cols, row))


def _connect() -> sqlite3.Connection:
    """Open (once) the configured store, falling back to in-memory."""
    global _conn, _is_file, _ephemeral, _last_error
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
        # Note: use execute(), not executescript() — the official libsql client
        # swallows network failures inside executescript, so a dead/unauthorized
        # Turso must surface here or we'd report a "persistent" store that is
        # silently local-only.
        conn.execute(_SCHEMA)
        conn.commit()
        _is_file = True
        _ephemeral = False
        _last_error = None
    except Exception as exc:
        # Read-only / unwritable filesystem (Vercel serverless) or Turso
        # unreachable: keep the API alive with an in-memory DB. Data resets
        # between cold starts.
        _last_error = _redact(repr(exc))
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
        "error": _last_error,
        "token_set": bool(os.getenv(TURSO_TOKEN_ENV)),
        "url_scheme": os.getenv(TURSO_URL_ENV, "").split(":")[0],
    }


def get_user_state(user_id: str):
    """Read a user's saved state, or None if never saved."""
    conn = _connect()
    with _lock:
        cur = conn.execute(
            "SELECT learned, quiz_best FROM user_state WHERE user_id = ?",
            (user_id,),
        )
        row = _row_to_dict(cur, cur.fetchone())
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
