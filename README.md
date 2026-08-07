# AWS Atlas Pro Enterprise

Enterprise-grade AWS learning platform with **80 services**, interactive quizzes, learning paths, enterprise architectures, and an AI-powered career radar.

- **Live demo**: https://atlas-aws-pro.vercel.app
- **GitHub**: https://github.com/trainingonlinecourses/atlas-aws-pro

## Features

- **80 AWS Services** — Complete catalog with Terraform, CDK, and Boto3 examples, expert tips, real-world case studies, and next-step learning
- **Enterprise Architectures** — Financial services, healthcare, retail, media architectures
- **Production Playbooks** — HA, DR, cost optimization, security hygiene
- **AI Career Radar** — Industry AI maturity assessment and predictions
- **Interactive Quiz** — Test your knowledge with instant feedback
- **Learning Paths** — Curated tracks for DevOps, Data, ML/AI careers
- **Deployment Blueprints** — Web apps, serverless, data lakes, GenAI
- **Responsive UI** — Dark theme, mobile-first design

## Data Architecture

> **No database.** All service data is in-memory and code-defined — the backend serves it from a generated module, and the frontend consumes it over the API.

```
frontend/index.html (embedded 80 services = OFFLINE FALLBACK)
        │  fetch("/api/v1/services")  on load
        ▼
backend/services_data.py   ← single source of truth (80 services, full detail)
        │
        ▼
backend/main.py (FastAPI) → /api/v1/* endpoints → JSON
```

- `backend/services_data.py` holds all 80 services with full detail (tagline, why-it-exists, use cases, learn-first list, Terraform/CDK/Boto3/delete snippets, expert tips, real-world uses, next steps).
- `backend/main.py` imports `SERVICES_DATA` from that module — it is **not** duplicated inline anymore.
- The frontend calls `loadFromAPI()` on startup: it fetches `/api/v1/services`, adapts the backend schema to its render schema, and re-renders. If the API is unreachable, the embedded copy keeps the site fully functional.
- Browser `localStorage` stores only quiz best score and "learned" progress flags — client-side, per-browser, not a server DB.

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
│   ├── services_data.py   # 80 services dataset (generated, single source of truth)
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── index.html         # Single-page application (SPA, ~4000 lines)
│   └── static/            # Static assets (CSS, JS, images)
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
| `GET /api/v1/services` | List all 80 services (full detail) |
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
| `GET /health` | Health check |

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
