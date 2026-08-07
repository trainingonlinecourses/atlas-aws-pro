# AWS Atlas Pro Enterprise

Enterprise-grade AWS learning platform with **94 services**, interactive quizzes, learning paths, enterprise architectures, and an AI-powered career radar.

- **Live demo**: https://atlas-aws-pro.vercel.app
- **GitHub**: https://github.com/trainingonlinecourses/atlas-aws-pro

## Features

- **94 AWS Services** — Complete catalog with Terraform, CDK, and Boto3 examples, expert tips, real-world case studies, and next-step learning
- **Enterprise Architectures** — Financial services, healthcare, retail, media architectures
- **Production Playbooks** — HA, DR, cost optimization, security hygiene
- **AI Career Radar** — Industry AI maturity assessment and predictions
- **Interactive Quiz** — Test your knowledge with instant feedback
- **Learning Paths** — Curated tracks for DevOps, Data, ML/AI careers
- **Deployment Blueprints** — Web apps, serverless, data lakes, GenAI
- **Responsive UI** — Dark theme, mobile-first design

## Data Architecture

Two kinds of data, two storage models:

**1. Service catalog (94 services)** — code-defined, no database.
```
frontend/index.html (embedded 94 services = OFFLINE FALLBACK)
        │  fetch("/api/v1/services")  on load
        ▼
backend/services_data.py   ← single source of truth (94 services, full detail)
        │
        ▼
backend/main.py (FastAPI) → /api/v1/* endpoints → JSON
```

**2. User progress (learned services, quiz best score)** — private SQLite DB.
```
Browser → GET/PUT /api/v1/user-state → FastAPI → backend/db.py → SQLite file
                                    └──── JSON response back ────┘
```
The browser **never touches the database** — it only calls the API. The SQLite file is private (gitignored, never served, no credentials). `backend/db.py` uses Python's stdlib `sqlite3`, with an in-memory fallback on read-only filesystems (e.g. Vercel serverless) so every endpoint keeps working. Path is configurable via the `ATLAS_DB_PATH` env var; swapping to a serverless-persistent store (Turso/libSQL) later is a one-line change. See [docs/PRIVACY.md](docs/PRIVACY.md).

- The frontend calls `loadFromAPI()` on startup: it fetches `/api/v1/services`, adapts the backend schema to its render schema, and re-renders. If the API is unreachable, the embedded copy keeps the site fully functional.
- Browser `localStorage` keeps a local cache of progress and a generated `user_id`; the server copy is synced through the API so progress can survive across browsers.

## Quick Start

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

The frontend is served directly by FastAPI at `http://localhost:8000` (from the `dist/` directory). To rebuild `dist/` from `frontend/`:

```bash
mkdir -p dist && cp -r frontend/* dist/
```

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
├── backend/
│   ├── main.py            # FastAPI application with all endpoints
│   ├── services_data.py   # 94 services dataset (generated, single source of truth)
│   ├── db.py              # Private SQLite persistence (user progress)
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── index.html         # Single-page application (SPA)
│   └── static/            # Static assets (CSS, JS, images)
├── docs/                  # Generated documentation
│   ├── README.md          # Service index
│   ├── services/          # One markdown page per service (94 pages)
│   ├── api.md             # API reference (auto-derived)
│   └── PRIVACY.md         # Privacy & data model
├── scripts/
│   └── gen_docs.py        # Regenerates docs/ from the dataset + routes
├── tests/
│   ├── test_backend.py    # Pytest suite (API + data integrity + DB)
│   └── frontend.test.js   # Node suite (frontend integrity + adapter)
├── dist/                  # Built frontend (served in production)
├── api/
│   └── index.py           # Vercel entrypoint: `from backend.main import app`
├── vercel.json            # Vercel build/deploy config
├── .gitignore
└── README.md
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/services` | List all 94 services (full detail) |
| `GET /api/v1/services/{id}` | Get a single service by ID |
| `GET /api/v1/categories` | Categories with service counts |
| `GET /api/v1/services/search?q=` | Search services |
| `GET /api/v1/quiz` | Get quiz questions |
| `GET /api/v1/projects` | Learning projects |
| `GET /api/v1/architecture-flows` | Architecture diagrams |
| `GET /api/v1/deployment-blueprints` | Deployment patterns |
| `GET /api/v1/enterprise-architectures` | Enterprise reference architectures |
| `GET /api/v1/production-playbooks` | Operational playbooks |
| `GET /api/v1/ai-radar` | Industry AI maturity radar |
| `GET /api/v1/db` | Private DB status (no data exposed) |
| `GET /api/v1/user-state?user_id=` | Read a user's saved progress |
| `PUT /api/v1/user-state` | Save a user's progress (learned + quiz best) |
| `DELETE /api/v1/user-state?user_id=` | Wipe a user's saved progress |
| `GET /health` | Health check |

See [docs/api.md](docs/api.md) for the full auto-generated reference.

## Deployment (Vercel)

The project deploys as a Python serverless function. `vercel.json`:

- `buildCommand`: installs backend deps and copies `frontend/*` → `dist/`
- `outputDirectory`: `dist` (static assets + served SPA)
- `framework`: `python` (entrypoint `backend.main:app`)

```bash
vercel --prod
```

### Local deployment

Docker (optional):

```bash
cd backend
docker build -t aws-atlas-api .
docker run -p 8000:8000 aws-atlas-api
```

Or any platform supporting Python/FastAPI (AWS Lambda w/ Mangum, GCP Cloud Run, Railway, Render, Fly.io, etc.).

## Technology Stack

- **Backend**: FastAPI, Uvicorn, Pydantic, SlowAPI
- **Frontend**: Vanilla JS, CSS Grid/Flexbox, CSS Variables
- **Data**: In-memory (80 services with full examples), served via the API

## License

MIT License
