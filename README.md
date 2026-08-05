# AWS Atlas Pro Enterprise

Enterprise-grade AWS learning platform with 80 services, interactive quizzes, learning paths, enterprise architectures, and AI-powered career radar.

## Features

- **80 AWS Services** — Complete catalog with Terraform, CDK, and Boto3 examples
- **Enterprise Architectures** — Financial services, healthcare, retail, media architectures
- **Production Playbooks** — HA, DR, cost optimization, security hygiene
- **AI Career Radar** — Industry AI maturity assessment and predictions
- **Interactive Quiz** — Test your knowledge with instant feedback
- **Learning Paths** — Curated tracks for DevOps, Data, ML/AI careers
- **Deployment Blueprints** — Web apps, serverless, data lakes, GenAI
- **Responsive UI** — Dark theme, mobile-first design

## Quick Start

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

The frontend is served directly by FastAPI at `http://localhost:8000`

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
├── backend/
│   ├── main.py           # FastAPI application with all endpoints
│   ├── requirements.txt  # Python dependencies
│   └── README.md         # Backend documentation
├── frontend/
│   ├── index.html        # Single-page application (3563+ lines)
│   └── static/           # Static assets (CSS, JS, images)
├── .gitignore
└── README.md
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/services` | List all 80 services |
| `GET /api/v1/services/{id}` | Get service detail with code examples |
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

## Deployment

### Docker (optional)

```bash
# Backend
cd backend
docker build -t aws-atlas-api .
docker run -p 8000:8000 aws-atlas-api
```

### Cloud Deployment

Deploy to any platform supporting Python/FastAPI:
- AWS Elastic Beanstalk / ECS / Lambda (Mangum)
- Google Cloud Run
- Azure Container Apps
- Railway / Render / Fly.io
- Vercel (with Python support)

## Technology Stack

- **Backend**: FastAPI, Uvicorn, Pydantic, SlowAPI
- **Frontend**: Vanilla JS, CSS Grid/Flexbox, CSS Variables
- **Data**: In-memory (80 services with full examples)

## GitHub

```bash
git remote add origin https://github.com/yourusername/aws-atlas-pro.git
git push -u origin main
```

## License

MIT License - see LICENSE file