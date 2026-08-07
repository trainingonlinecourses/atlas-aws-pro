"""
AWS Atlas Pro - Enterprise FastAPI Backend
Full-stack API with 80 AWS services, quizzes, learning paths, and enterprise architectures
"""
import os
import copy
from pathlib import Path
from fastapi.responses import FileResponse
from typing import List, Optional, Dict, Any
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
FRONTEND_DIR = PROJECT_ROOT / "dist"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# Initialize app
app = FastAPI(
    title="AWS Atlas Pro API",
    version="1.0.0",
    description="Enterprise API for AWS learning platform with 80 services, quizzes, and architectures",
    openapi_url="/docs.json",
    docs_url=None,  # Serve custom docs
    redoc_url=None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if DEBUG else ["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class CategoryStats(BaseModel):
    total: int
    categories: Dict[str, int]

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

# ============================================================
# API ROUTES
# ============================================================

@app.get("/api/v1/services", response_model=List[ServiceDetail])
async def get_services():
    """Get all services"""
    return SERVICES_DATA

@app.get("/api/v1/services/{service_id}", response_model=ServiceDetail)
async def get_service(service_id: str):
    """Get a single service by ID"""
    for service in SERVICES_DATA:
        if service["id"] == service_id:
            return service
    raise HTTPException(status_code=404, detail="Service not found")

@app.get("/api/v1/categories")
async def get_categories():
    """Get categories with counts"""
    categories: Dict[str, int] = {}
    for service in SERVICES_DATA:
        cat = service["category"]
        categories[cat] = categories.get(cat, 0) + 1
    return {"total": len(SERVICES_DATA), "categories": categories}

@app.get("/api/v1/services/search")
async def search_services(q: str = Query(..., min_length=1), limit: int = 50):
    """Search services by query"""
    results = [
        s for s in SERVICES_DATA
        if q.lower() in s["name"].lower()
        or q.lower() in s["tagline"].lower()
        or q.lower() in s.get("why_it_exists", "").lower()
    ][:limit]
    return results

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
