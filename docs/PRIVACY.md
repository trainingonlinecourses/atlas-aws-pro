# Privacy & Data Model

## Where the data lives

- **Service catalog** (94 services): code-defined in `backend/services_data.py`, served over the API. No database involved.
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

Vercel serverless filesystems are ephemeral. On Vercel the SQLite store falls back to **in-memory** so every endpoint keeps working, but data does not persist across cold starts. For durable persistence on Vercel, point `ATLAS_DB_PATH` at a serverless-friendly SQLite service (e.g. Turso/libSQL) — the API layer and schema do not change.
