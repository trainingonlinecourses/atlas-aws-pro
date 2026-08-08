"""
AWS Atlas Pro - Enterprise FastAPI Backend
Full-stack API with 80 AWS services, quizzes, learning paths, and enterprise architectures
"""
import os
import copy
import traceback
from pathlib import Path
from fastapi.responses import FileResponse, JSONResponse
from typing import Annotated, List, Optional, Dict, Any
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, StringConstraints
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime, timedelta, timezone

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "dist"
# DEBUG must be explicit; NEVER default on in production (it widens CORS).
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Initialize app
app = FastAPI(
    title="AWS Atlas Pro API",
    version="1.0.0",
    description="Enterprise API for AWS learning platform with 80 services, quizzes, and architectures",
    openapi_url="/docs.json",
    docs_url=None,  # Serve custom docs
    redoc_url=None,
)

# CORS — the frontend is served same-origin from dist/ at the app root, so
# cross-origin only matters for local dev / Vercel preview. Never "*".
# In DEBUG (local) allow localhost; otherwise the explicit ATLAS_ORIGINS list.
_ATLAS_ORIGINS = [o.strip() for o in os.getenv("ATLAS_ORIGINS", "").split(",") if o.strip()]
if not _ATLAS_ORIGINS:
    _ATLAS_ORIGINS = ["https://atlas-aws-pro.vercel.app"]
if DEBUG:
    _ATLAS_ORIGINS += ["http://localhost:8000", "http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_ATLAS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "X-Requested-With", "Accept"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# ============================================================
# SERVICES DATA (80 Services) - generated, single source of truth
# ============================================================
try:
    from services_data import SERVICES_DATA
except ImportError:  # imported as backend.main
    from backend.services_data import SERVICES_DATA

# Private SQLite persistence (see backend/db.py for the privacy model)
try:
    import db as db_store
except ImportError:  # imported as backend.main
    from backend import db as db_store

# Auth core (email+password, bcrypt, JWT cookies, Turso persistence)
try:
    import auth as auth_core
except ImportError:  # imported as backend.main
    from backend import auth as auth_core

# Real-world industry scenarios & issues (see backend/industry_issues.py)
try:
    import industry_issues as industry
except ImportError:  # imported as backend.main
    from backend import industry_issues as industry

# Per-service environment operating model (see backend/env_model.py)
try:
    import env_model as env_model_store
except ImportError:  # imported as backend.main
    from backend import env_model as env_model_store


def _with_env(service: dict) -> dict:
    """Attach the environment operating model (dev -> staging -> prod -> DR -> lifecycle)."""
    enriched = dict(service)
    enriched["env_model"] = env_model_store.for_service(service)
    return enriched

# ============================================================
# Pydantic Models
# ============================================================
class Service(BaseModel):
    id: str
    name: str
    full_name: str
    category: str
    icon: str
    tagline: str

class ServiceDetail(BaseModel):
    id: str
    name: str
    full_name: str
    category: str
    icon: str
    tagline: str
    why_it_exists: str
    when_to_use: str
    use_cases: str
    learn_first: List[str]
    terraform: str
    cdk: str
    boto3: str
    delete: str
    expert_tips: List[str]
    real_world: List[str]
    next_steps: List[List[str]]
    enterprise: bool = False
    ai_enabled: bool = False
    env_model: Optional[List[Dict[str, Any]]] = None

class CategoryStats(BaseModel):
    total: int
    categories: Dict[str, int]

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class UserState(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    # each item a bounded service id; list itself capped (~100 services exist)
    learned: List[Annotated[str, StringConstraints(max_length=64)]] = Field(default=[], max_length=300)
    quiz_best: int = Field(default=0, ge=0, le=100)

# ---- Auth models ----
class RegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=72)

class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)

class TokenRequest(BaseModel):
    token: str = Field(min_length=10, max_length=512)

class EmailRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)

class ResetConfirmRequest(BaseModel):
    token: str = Field(min_length=10, max_length=512)
    new_password: str = Field(min_length=8, max_length=72)

_EMAIL_RE = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
import re as _re

# ============================================================
# API ROUTES
# ============================================================

@app.get("/api/v1/services", response_model=List[ServiceDetail])
async def get_services():
    """Get all services"""
    return [_with_env(s) for s in SERVICES_DATA]

@app.get("/api/v1/services/search")
async def search_services(q: str = Query(..., min_length=1), limit: int = 50):
    """Search services by query"""
    results = [
        s for s in SERVICES_DATA
        if q.lower() in s["name"].lower()
        or q.lower() in s["tagline"].lower()
        or q.lower() in s.get("why_it_exists", "").lower()
    ][:limit]
    return [_with_env(s) for s in results]

@app.get("/api/v1/services/{service_id}", response_model=ServiceDetail)
async def get_service(service_id: str):
    """Get a single service by ID"""
    for service in SERVICES_DATA:
        if service["id"] == service_id:
            return _with_env(service)
    raise HTTPException(status_code=404, detail="Service not found")

@app.get("/api/v1/categories")
async def get_categories():
    """Get categories with counts"""
    categories: Dict[str, int] = {}
    for service in SERVICES_DATA:
        cat = service["category"]
        categories[cat] = categories.get(cat, 0) + 1
    return {"total": len(SERVICES_DATA), "categories": categories}

@app.get("/api/v1/quiz")
async def get_quiz(count: int = 8):
    """Get quiz questions (static for demo)"""
    questions = [
        {"id": "q1", "question": "Which AWS service provides managed Kubernetes?", "options": ["ECS", "EKS", "Fargate", "App Runner"], "correct_answer": 1, "explanation": "EKS (Elastic Kubernetes Service) is AWS's managed Kubernetes service."},
        {"id": "q2", "question": "What is the primary use case for DynamoDB?", "options": ["Relational OLTP", "Key-value NoSQL at scale", "Data warehousing", "File storage"], "correct_answer": 1, "explanation": "DynamoDB is a managed NoSQL database for single-digit millisecond latency."},
        {"id": "q3", "question": "Which service provides a global CDN?", "options": ["Route 53", "CloudFront", "ALB", "API Gateway"], "correct_answer": 1, "explanation": "CloudFront is AWS's global content delivery network."},
        {"id": "q4", "question": "What does S3 stand for?", "options": ["Simple Storage Service", "Secure Storage System", "Scalable Storage Solution", "Standard Storage Service"], "correct_answer": 0, "explanation": "S3 stands for Simple Storage Service."},
        {"id": "q5", "question": "Which service is used for serverless functions?", "options": ["EC2", "Lambda", "ECS", "EKS"], "correct_answer": 1, "explanation": "Lambda runs code without provisioning servers, paying only for compute time."},
    ]
    return {"questions": questions[:count], "total": len(questions)}

@app.get("/api/v1/db")
async def get_db_status():
    """Private DB status (driver, persistence mode). No data is exposed."""
    try:
        return db_store.status()
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=503, content={"error": "storage unavailable"})

# ============================================================
# AUTH (see backend/auth.py + spec docs/superpowers/specs/)
# ============================================================
def _client_ip(request: Request) -> str:
    """Client IP honoring X-Forwarded-For (Vercel) with fallback."""
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _current_email(request: Request) -> str:
    """Email from the httpOnly access cookie, or raise 401."""
    token = request.cookies.get(auth_core.access_cookie_name())
    if not token:
        raise HTTPException(status_code=401, detail="not authenticated")
    email = auth_core.verify_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="session expired")
    return email


def _require_csrf_header(request: Request) -> None:
    """SameSite=Lax blocks cross-site POSTs; belt-and-suspenders header check."""
    if request.headers.get("x-requested-with", "").lower() != "xmlhttprequest":
        raise HTTPException(status_code=403, detail="forbidden")


@app.get("/api/v1/auth/me")
async def auth_me(request: Request):
    """Current logged-in user profile (progress read from user_state)."""
    email = _current_email(request)
    user = db_store.get_user(email)
    state = db_store.get_user_state(email) or {"user_id": email, "learned": [], "quiz_best": 0}
    return {
        "email": email,
        "email_verified": bool(user["email_verified"]) if user else False,
        "progress": state,
    }


@app.post("/api/v1/auth/register")
@limiter.limit("5/hour")
async def auth_register(request: Request, body: RegisterRequest):
    """Create account, send email-verification link."""
    email = body.email.strip().lower()
    if not _re.fullmatch(_EMAIL_RE, email):
        raise HTTPException(status_code=400, detail="invalid email")
    if len(body.password) < 8 or not any(c.isdigit() for c in body.password) or not any(c.isalpha() for c in body.password):
        raise HTTPException(status_code=400, detail="password must be 8+ chars with letters and numbers")
    if db_store.get_user(email):
        raise HTTPException(status_code=409, detail="email already registered")
    password_hash = auth_core.hash_password(body.password)
    try:
        db_store.create_user(email, password_hash)
    except Exception:
        raise HTTPException(status_code=409, detail="email already registered")
    raw = auth_core.new_raw_token()
    db_store.delete_user_verify_tokens(email, "verify_email")
    db_store.create_verify_token(
        auth_core.hash_token(raw), email, "verify_email",
        (datetime.now(timezone.utc) + timedelta(hours=auth_core.VERIFY_TOKEN_TTL_HOURS)).isoformat(),
    )
    auth_core.send_verify_email(email, raw)
    return {"email": email, "message": "registered; check your email to verify"}


@app.post("/api/v1/auth/verify-email")
@limiter.limit("10/10minute")
async def auth_verify_email(request: Request, body: TokenRequest):
    """Verify email with the single-use token from the email link."""
    row = db_store.get_verify_token(auth_core.hash_token(body.token))
    if row is None or row["purpose"] != "verify_email" or row["used"]:
        raise HTTPException(status_code=400, detail="invalid or expired token")
    expires = datetime.fromisoformat(row["expires_at"])
    if expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="invalid or expired token")
    db_store.mark_email_verified(row["email"])
    db_store.mark_verify_token_used(row["token_hash"])
    return {"email": row["email"], "message": "email verified"}


@app.post("/api/v1/auth/login")
@limiter.limit("30/15minute")  # coarse IP throttle; per-email lockout is the real gate
async def auth_login(request: Request, body: LoginRequest):
    """Login: bcrypt check, lockout, issue httpOnly cookie session."""
    _require_csrf_header(request)
    email = body.email.strip().lower()
    ip = _client_ip(request)
    if not _re.fullmatch(_EMAIL_RE, email):
        raise HTTPException(status_code=401, detail="invalid credentials")
    user = db_store.get_user(email)
    if user is None:
        auth_core._dummy_verify()  # equalize timing against unknown email
        auth_core.record_failed_login(email, ip)
        raise HTTPException(status_code=401, detail="invalid credentials")
    if auth_core._is_locked_out(email, ip):
        raise HTTPException(status_code=429, detail="too many attempts; try again later")
    if not auth_core.verify_password(body.password, user["password_hash"]):
        auth_core.record_failed_login(email, ip)
        raise HTTPException(status_code=401, detail="invalid credentials")
    if not user["email_verified"]:
        raise HTTPException(status_code=403, detail="email_not_verified")
    auth_core.clear_login_failures(email, ip)
    response = JSONResponse({"email": email, "email_verified": True})
    auth_core.issue_session(email, response)
    return response


@app.post("/api/v1/auth/logout")
@limiter.limit("30/minute")
async def auth_logout(request: Request):
    """Revoke refresh session family and clear cookies."""
    _require_csrf_header(request)
    raw = request.cookies.get(auth_core.refresh_cookie_name())
    if raw:
        auth_core.revoke_session(raw)
    response = JSONResponse({"message": "logged out"})
    auth_core._clear_auth_cookies(response)
    return response


@app.post("/api/v1/auth/refresh")
@limiter.limit("30/minute")
async def auth_refresh(request: Request):
    """Rotate refresh token; reuse detection revokes family on replay."""
    raw = request.cookies.get(auth_core.refresh_cookie_name())
    if not raw:
        raise HTTPException(status_code=401, detail="no session")
    response = JSONResponse({"message": "refreshed"})
    if not auth_core.refresh_session(raw, response):
        auth_core._clear_auth_cookies(response)
        raise HTTPException(status_code=401, detail="session expired")
    return response


@app.post("/api/v1/auth/reset-password")
@limiter.limit("3/hour")
async def auth_reset_request(request: Request, body: EmailRequest):
    """Send password-reset link if account exists (no enumeration on response)."""
    email = body.email.strip().lower()
    user = db_store.get_user(email)
    if user is not None:
        raw = auth_core.new_raw_token()
        db_store.delete_user_verify_tokens(email, "reset_password")
        db_store.create_verify_token(
            auth_core.hash_token(raw), email, "reset_password",
            (datetime.now(timezone.utc) + timedelta(hours=auth_core.VERIFY_TOKEN_TTL_HOURS)).isoformat(),
        )
        auth_core.send_reset_email(email, raw)
    return {"message": "if that email exists, a reset link was sent"}


@app.post("/api/v1/auth/reset-password/confirm")
@limiter.limit("10/10minute")
async def auth_reset_confirm(request: Request, body: ResetConfirmRequest):
    """Set a new password with a valid reset token; revoke all sessions."""
    row = db_store.get_verify_token(auth_core.hash_token(body.token))
    if row is None or row["purpose"] != "reset_password" or row["used"]:
        raise HTTPException(status_code=400, detail="invalid or expired token")
    expires = datetime.fromisoformat(row["expires_at"])
    if expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="invalid or expired token")
    if len(body.new_password) < 8 or not any(c.isdigit() for c in body.new_password) or not any(c.isalpha() for c in body.new_password):
        raise HTTPException(status_code=400, detail="password must be 8+ chars with letters and numbers")
    db_store.update_password(row["email"], auth_core.hash_password(body.new_password))
    db_store.mark_verify_token_used(row["token_hash"])
    db_store.revoke_all_user_sessions(row["email"])
    return {"message": "password updated"}


# ---- user-state (auth-protected; user_id pinned to logged-in email) ----
@app.get("/api/v1/user-state")
async def get_user_state(request: Request, user_id: str = Query(None, min_length=1, max_length=128)):
    """Read the logged-in user's saved progress."""
    email = _current_email(request)
    try:
        state = db_store.get_user_state(email)
        if state is not None:
            return state
        return {"user_id": email, "learned": [], "quiz_best": 0}
    except Exception:
        traceback.print_exc()
        return {"user_id": email, "learned": [], "quiz_best": 0}


@app.put("/api/v1/user-state", response_model=UserState)
async def put_user_state(request: Request, state: UserState):
    """Persist the logged-in user's progress. user_id is server-pinned."""
    email = _current_email(request)
    try:
        return db_store.upsert_user_state(email, state.learned, state.quiz_best)
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=503, content={"error": "storage unavailable"})


@app.delete("/api/v1/user-state")
async def delete_user_state(request: Request, user_id: str = Query(None, min_length=1, max_length=128)):
    """Delete the logged-in user's saved progress (privacy: full wipe)."""
    email = _current_email(request)
    try:
        removed = db_store.delete_user_state(email)
        return {"deleted": removed, "user_id": email}
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=503, content={"error": "storage unavailable"})

@app.get("/api/v1/industry-issues")
async def get_industry_issues():
    """Real-world industry scenarios & failure modes per service (teaching reference)."""
    return industry.get_all()

@app.get("/api/v1/industry-issues/{service_id}")
async def get_industry_issue(service_id: str):
    """One service's industry scenario + issue + fix + alerts."""
    issue = industry.get_by_service(service_id)
    if issue is None:
        raise HTTPException(status_code=404, detail=f"no industry entry for '{service_id}'")
    return issue

@app.get("/api/v1/projects")
async def get_projects():
    """Get learning projects"""
    return {
        "projects": [
            {"id": "web-app", "name": "Production Web App", "description": "Deploy a scalable web application with ALB, Auto Scaling, and RDS", "services": ["vpc", "alb", "autoscaling", "rds"], "difficulty": "Intermediate", "duration": "4-6 hours"},
            {"id": "serverless-api", "name": "Serverless REST API", "description": "Build a serverless API with API Gateway, Lambda, and DynamoDB", "services": ["apigateway", "lambda", "dynamodb", "cognito"], "difficulty": "Beginner", "duration": "2-3 hours"},
            {"id": "data-lake", "name": "Data Lake & Analytics", "description": "Build a data lake with S3, Glue, Athena, and Redshift", "services": ["s3", "glue", "athena", "redshift", "quicksight"], "difficulty": "Advanced", "duration": "6-8 hours"},
        ]
    }

@app.get("/api/v1/architecture-flows")
async def get_architecture_flows():
    """Get architecture flows"""
    return {
        "flows": [
            {"id": "web-request", "name": "Production Web Request", "description": "DNS → EDGE → COMPUTE → DATA", "steps": [
                {"service": "route53", "label": "Route 53", "description": "DNS"},
                {"service": "cloudfront", "label": "CloudFront", "description": "Edge cache"},
                {"service": "alb", "label": "ALB", "description": "TLS termination"},
                {"service": "autoscaling", "label": "Auto Scaling", "description": "2-40 EC2"},
                {"service": "rds", "label": "RDS Multi-AZ", "description": "Private subnet"}
            ]},
            {"id": "serverless", "name": "Serverless Architecture", "description": "API → Lambda → DynamoDB → S3", "steps": [
                {"service": "apigateway", "label": "API Gateway", "description": "HTTP endpoints"},
                {"service": "lambda", "label": "Lambda", "description": "Compute"},
                {"service": "dynamodb", "label": "DynamoDB", "description": "NoSQL"},
                {"service": "s3", "label": "S3", "description": "Object storage"}
            ]},
        ]
    }

@app.get("/api/v1/deployment-blueprints")
async def get_blueprints():
    """Get deployment blueprints"""
    return {
        "blueprints": [
            {"id": "web-app", "name": "Web Application", "description": "Classic 3-tier with ALB, EC2/ECS, and RDS",
             "layers": ["Edge (Route 53, CloudFront, WAF)", "Compute (ALB, EC2/ECS/Fargate)", "Data (RDS, ElastiCache, S3)", "Async (SQS, SNS, EventBridge)", "Identity (IAM, Cognito)", "Observability (CloudWatch, X-Ray)"]},
            {"id": "serverless", "name": "Serverless Application", "description": "Fully managed with API Gateway, Lambda, DynamoDB",
             "layers": ["Edge (Route 53, CloudFront, WAF)", "API (API Gateway, Lambda Authorizers)", "Compute (Lambda, Step Functions, EventBridge)", "Data (DynamoDB, S3, Aurora Serverless)", "Identity (Cognito, IAM)", "Observability (CloudWatch, X-Ray)"]},
            {"id": "data-lake", "name": "Data Lake & Analytics", "description": "Centralized data platform for analytics and ML",
             "layers": ["Ingest (Kinesis, MSK, DMS)", "Store (S3, Lake Formation, Glue Catalog)", "Process (EMR, Glue, Athena, Redshift)", "Analyze (QuickSight, SageMaker, OpenSearch)", "Govern (Lake Formation, IAM, CloudTrail)"]},
            {"id": "genai", "name": "Generative AI Application", "description": "RAG-powered GenAI apps with Bedrock",
             "layers": ["Frontend (Amplify, CloudFront, Cognito)", "API (API Gateway, Lambda, AppSync)", "Orchestration (Bedrock Agents, Step Functions, EventBridge)", "Knowledge (Bedrock KB, OpenSearch, S3)", "Safety (Guardrails, Comprehend)", "Models (Bedrock, SageMaker)", "Observability (CloudWatch, X-Ray)"]},
        ]
    }

@app.get("/api/v1/enterprise-architectures")
async def get_enterprise_architectures():
    """Get enterprise architectures"""
    return {
        "architectures": [
            {"id": "financial", "name": "Financial Services", "description": "Regulated banking with compliance and audit trails",
             "components": ["Organizations", "Control Tower", "Macie", "Config", "WAF", "Shield", "CloudTrail", "IAM", "VPC", "RDS", "Backup"],
             "compliance": ["PCI-DSS", "SOX", "GDPR"]},
            {"id": "healthcare", "name": "Healthcare & Life Sciences", "description": "HIPAA-compliant architecture with patient data",
             "components": ["Macie", "Config", "Backup", "Vault Lock", "Organizations", "IAM", "KMS", "KMS", "VPC", "RDS", "S3"],
             "compliance": ["HIPAA", "HITECH"]},
            {"id": "retail", "name": "Retail & E-commerce", "description": "Global retail with personalization and analytics",
             "components": ["CloudFront", "WAF", "Shield", "Fargate", "App Runner", "DynamoDB", "ElastiCache", "Auto Scaling", "Cost Explorer", "QuickSight"],
             "compliance": ["PCI-DSS"]},
            {"id": "media", "name": "Media & Entertainment", "description": "Streaming and content delivery at scale",
             "components": ["CloudFront", "MediaConvert", "MediaStore", "S3", "Batch", "EKS", "EFS", "Backup", "CloudWatch", "X-Ray"],
             "compliance": []},
        ]
    }

@app.get("/api/v1/production-playbooks")
async def get_production_playbooks():
    """Get production playbooks"""
    return {
        "playbooks": [
            {"id": "high-availability", "name": "High Availability Playbook", "description": "Ensure 99.99% uptime with multi-AZ and failover",
             "steps": ["Deploy to 3+ AZs", "Use Multi-AZ RDS", "Configure ALB health checks", "Set up Route 53 failover", "Enable automated backups", "Test failover quarterly"]},
            {"id": "disaster-recovery", "name": "Disaster Recovery Playbook", "description": "Recover from region failure in under 4 hours",
             "steps": ["Cross-region backups", "Global DynamoDB tables", "Route 53 health checks", "CloudEndure DR", "Test DR monthly"]},
            {"id": "cost-optimization", "name": "Cost Optimization Playbook", "description": "Reduce cloud costs by 30% or more",
             "steps": ["Enable Cost Explorer", "Set up budgets and alerts", "Identify unused resources", "Right-size instances", "Use Reserved Instances", "Implement tagging"]},
            {"id": "security-hygiene", "name": "Security Hygiene Playbook", "description": "Prevent security incidents through proactive measures",
             "steps": ["Enable GuardDuty", "Configure Config rules", "Activate Macie", "Implement least privilege IAM", "Enable MFA", "Rotate credentials quarterly"]},
        ]
    }

@app.get("/api/v1/ai-radar")
async def get_ai_radar():
    """Get AI radar - current AI capabilities assessment"""
    return {
        "industries": [
            {"name": "Software Development", "maturity": "Advanced", "ai_tools": ["CodeWhisperer", "CodeGuru", "CloudAssist", "Claude", "Gemini", "Copilot"], "predictability": "High"},
            {"name": "Content Creation", "maturity": "High", "ai_tools": ["Polly", "Textract", "Comprehend", "Rekognition", "Transcribe", "Translate"], "predictability": "High"},
            {"name": "Customer Service", "maturity": "Advanced", "ai_tools": ["Lex", "Polly", "Transcribe", "Transcribe Analytics", "Connect", "Contact Lens"], "predictability": "High"},
            {"name": "Supply Chain", "maturity": "Emerging", "ai_tools": ["Forecasting", "Anomaly Detection", "Recommendation", "Optimization"], "predictability": "Medium"},
            {"name": "Healthcare", "maturity": "Regulated Emerging", "ai_tools": ["Comprehend Medical", "Rekognition", "Textract", "Transcribe Medical", "HealthLake"], "predictability": "Medium"},
        ],
        "predictions_2025": [
            "Agentic workflows become mainstream",
            "AI cost optimization becomes a dedicated role",
            "Foundation models replace custom models",
            "Real-time AI becomes default for new products"
        ]
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "version": "1.0.0"}

# Serve frontend
@app.get("/")
async def serve_frontend():
    """Serve frontend index.html"""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"error": "Frontend not built yet"}

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve single page app routes"""
    index_path = FRONTEND_DIR / "index.html"
    if full_path.startswith("api/") or full_path in ["health", "docs", "docs.json"]:
        # These are handled by other routes
        raise HTTPException(status_code=404)
    if index_path.exists():
        return FileResponse(index_path)
    return {"error": "Frontend not built yet"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
