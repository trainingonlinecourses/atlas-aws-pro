# AWS Atlas Pro — API Reference

Base URL: `https://atlas-aws-pro.vercel.app` (or `http://localhost:8000` locally).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| DELETE | `/api/v1/user-state` | Delete a user's saved progress (privacy: full wipe on request). |
| GET | `/` | Serve frontend index.html |
| GET | `/api/v1/ai-radar` | Get AI radar - current AI capabilities assessment |
| GET | `/api/v1/architecture-flows` | Get architecture flows |
| GET | `/api/v1/categories` | Get categories with counts |
| GET | `/api/v1/db` | Private DB status (driver, persistence mode). No data is exposed. |
| GET | `/api/v1/deployment-blueprints` | Get deployment blueprints |
| GET | `/api/v1/enterprise-architectures` | Get enterprise architectures |
| GET | `/api/v1/production-playbooks` | Get production playbooks |
| GET | `/api/v1/projects` | Get learning projects |
| GET | `/api/v1/quiz` | Get quiz questions (static for demo) |
| GET | `/api/v1/services` | Get all services |
| GET | `/api/v1/services/search` | Search services by query |
| GET | `/api/v1/services/{service_id}` | Get a single service by ID |
| GET | `/api/v1/user-state` | Read a user's saved progress. Returns empty state if none saved. |
| GET | `/docs.json` |  |
| GET | `/health` | Health check endpoint |
| GET | `/{full_path:path}` | Serve single page app routes |
| PUT | `/api/v1/user-state` | Persist a user's progress (learned services + quiz best score). |

## Data path (privacy)

The browser NEVER talks to the database. It calls the API; the backend reads/writes the private SQLite store and returns JSON. See [PRIVACY.md](PRIVACY.md).
