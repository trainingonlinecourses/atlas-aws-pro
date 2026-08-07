# Privacy & Data Model

## Where the data lives

- **Service catalog** (100 services): code-defined in `backend/services_data.py`, served over the API. No database involved.
- **User progress** (learned services, quiz best score): private **SQLite** database, `backend/db.py`. The frontend only ever calls the API — it never touches the DB.

## Data path

```
Browser (frontend)  --GET/PUT /api/v1/user-state-->  FastAPI backend  --sqlite-->  DB file
        ^                                                            |
        +-------------------- JSON response --------------------------+
```

## Privacy guarantees

- The DB file is **never served** to clients and is **gitignored** (`*.db`, `data/`).
- **No credentials in the repo.** The only knob is `ATLAS_DB_PATH` (an env var), set via `ATLAS_DB_PATH=/path/to/atlas.db`.
- `.env`, `CLAUDE.md`, `.claude/`, `config/`, and DB files are excluded from GitHub.
- Deleting your data: `DELETE /api/v1/user-state?user_id=<id>` wipes a row; the user_id is generated client-side and stored in the browser's localStorage.

## Serverless note (Vercel)

Vercel serverless filesystems are ephemeral. On Vercel the SQLite store falls back to **in-memory** so every endpoint keeps working, but data does not persist across cold starts. For durable persistence, use **Turso/libSQL** — the API layer and schema do not change.

## Making it durable with Turso (recommended)

1. Create a database: `turso db create atlas-pro`
2. Get your URL + token: `turso db show atlas-pro --url` and `turso db tokens create atlas-pro`
3. Set the env vars on the host (Vercel: *Settings → Environment Variables*):
   - `ATLAS_DB_URL` = `libsql://<db>.turso.io`
   - `ATLAS_DB_AUTH_TOKEN` = the token from step 2

When `ATLAS_DB_URL` is set, `backend/db.py` uses the `libsql_client` driver (a drop-in `sqlite3` replacement) so the schema and queries are identical. Without it, the app runs on local SQLite (or in-memory on serverless).

> **Tokens are secret.** Set them as environment variables on the host only — never in the repo. Neither `ATLAS_DB_URL` nor `ATLAS_DB_AUTH_TOKEN` is committed.
