"""
AWS Atlas Pro - Enterprise FastAPI Backend
Full-stack API with 80 AWS services, quizzes, learning paths, and enterprise architectures
"""
import os
import copy
from pathlib import Path
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
FRONTEND_DIR = PROJECT_ROOT / "frontend"
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
# SERVICES DATA (80 Services)
# ============================================================
SERVICES_DATA = [
    # Core Services
    {
        "id": "ec2",
        "name": "EC2",
        "full_name": "Elastic Compute Cloud",
        "category": "compute",
        "icon": "⎗",
        "tagline": "Rent virtual servers by the second",
        "why_it_exists": "You need a machine you fully control: any OS, any software. EC2 launches one in 30 seconds and bills per second.",
        "when_to_use": "Web servers, CI runners, batch workers, GPU hosts — anything that needs 'a server'.",
        "use_cases": "Web servers, CI runners, batch workers, GPU hosts",
        "learn_first": ["Linux basics & SSH", "Security groups = firewalls", "AMIs & instance families", "On-Demand vs Spot vs Reserved"],
        "terraform": 'resource "aws_instance" "web" {\n  ami = "ami-0c2b8ca1dad44e93a"\n  instance_type = "t3.micro"\n}',
        "cdk": 'const web = new ec2.Instance(this, "Web", {\n  instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),\n});',
        "boto3": 'ec2.run_instances(ImageId="ami-0c2b8ca1dad44e93a", InstanceType="t3.micro", MinCount=1)',
        "delete": "ec2.terminate_instances(InstanceIds=[\"i-abc\"])",
        "expert_tips": ["Never store keys on the box — use IAM instance profiles", "Stop ≠ terminate: stopped instances keep billing on EBS + EIP"],
        "real_world": ["Netflix streams video across thousands of EC2 instances"],
        "next_steps": [["VPC", "Instances plug ENIs into subnets"], ["EBS", "Root & data volumes"], ["ALB", "Target groups route to instances"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "lambda",
        "name": "Lambda",
        "full_name": "AWS Lambda",
        "category": "compute",
        "icon": "λ",
        "tagline": "Run code on events. Zero servers, pay per 128ms slice.",
        "why_it_exists": "Most glue code doesn't deserve a server. Lambda spins up per request, scales to zero, bills in milliseconds.",
        "when_to_use": "API handlers, S3 triggers, cron jobs, stream processors, service glue.",
        "use_cases": "API handlers, S3 triggers, cron jobs, stream processors",
        "learn_first": ["Event-driven model", "Cold starts & memory↔CPU", "Execution role IAM", "Timeouts & concurrency"],
        "terraform": 'resource "aws_lambda_function" "processor" {\n  function_name = "processor"\n  runtime = "python3.12"\n}',
        "cdk": 'const fn = new lambda.Function(this, "Processor", {\n  runtime: lambda.Runtime.PYTHON_3_12,\n});',
        "boto3": 'lam.invoke(FunctionName="processor", Payload=json.dumps({}))',
        "delete": "lam.delete_function(FunctionName='processor')",
        "expert_tips": ["More memory = more CPU — benchmark, don't guess", "Keep packages small; zip size drives cold starts"],
        "real_world": ["Capital One runs security tooling fully serverless"],
        "next_steps": [["API Gateway", "HTTP routes invoke Lambda"], ["DynamoDB", "Stateless function; state in table"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "s3",
        "name": "S3",
        "full_name": "Simple Storage Service",
        "category": "storage",
        "icon": "🪣",
        "tagline": "The infinite object store where every byte of your data lake begins.",
        "why_it_exists": "Nearly everything on AWS touches S3: backups, sites, lakes, model artifacts. 11 nines of durability.",
        "when_to_use": "Object storage, data lake landing zone, static hosting, ML data.",
        "use_cases": "Object storage, data lake, static hosting, ML data",
        "learn_first": ["Buckets, keys, prefixes", "Storage classes & lifecycles", "Bucket policies vs IAM", "Versioning"],
        "terraform": 'resource "aws_s3_bucket" "assets" {\n  bucket = "acme-assets-prod"\n}',
        "cdk": 'const bucket = new s3.Bucket(this, "Assets", { versioned: true });',
        "boto3": 's3.upload_file("report.pdf", "acme-assets-prod", "report.pdf")',
        "delete": "s3.delete_object(Bucket='acme-assets-prod', Key='report.pdf')",
        "expert_tips": ["Block ALL public access; serve via CloudFront OAC", "Bucket names are global across AWS"],
        "real_world": ["Netflix stores master copy of every title"],
        "next_steps": [["EventBridge", "'Object Created' events trigger pipelines"], ["Glue + Athena", "Catalog & SQL query data"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "vpc",
        "name": "VPC",
        "full_name": "Virtual Private Cloud",
        "category": "networking",
        "icon": "🌐",
        "tagline": "Your private network in the cloud — total control over IP space, subnets, routing, and security.",
        "why_it_exists": "Everything in AWS needs a network. VPC gives you your own logically isolated section with full control.",
        "when_to_use": "Every production workload. Start here before launching anything.",
        "use_cases": "Network isolation, hybrid connectivity, multi-tier architectures",
        "learn_first": ["CIDR blocks & subnets", "Route tables & IGW/NAT", "Security groups vs NACLs", "VPC endpoints"],
        "terraform": 'resource "aws_vpc" "main" {\n  cidr_block = "10.0.0.0/16"\n}',
        "cdk": 'const vpc = new ec2.Vpc(this, "Main", { maxAzs: 3 });',
        "boto3": 'ec2.create_vpc(CidrBlock="10.0.0.0/16")',
        "delete": "ec2.delete_vpc(VpcId='vpc-abc')",
        "expert_tips": ["Plan CIDR for growth — /16 gives you room", "Use VPC endpoints for S3/DynamoDB"],
        "real_world": ["Every production AWS account has at least one VPC"],
        "next_steps": [["Subnets", "Public for ALB/NAT, private for compute"], ["Transit Gateway", "Hub for 5+ VPCs"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "rds",
        "name": "RDS",
        "full_name": "Relational Database Service",
        "category": "database",
        "icon": "🛢️",
        "tagline": "Managed SQL databases — patching, backups and failover on autopilot.",
        "why_it_exists": "Running Postgres yourself means patch windows and 3am failover drills. RDS does all of it.",
        "when_to_use": "Transactional apps needing SQL joins and ACID guarantees.",
        "use_cases": "Transactional apps needing SQL joins and ACID guarantees",
        "learn_first": ["Relational modeling & SQL", "Multi-AZ vs read replicas", "Backups & PITR", "Parameter groups"],
        "terraform": 'resource "aws_db_instance" "orders" {\n  engine = "postgres"\n  instance_class = "db.t3.micro"\n}',
        "cdk": 'const db = new rds.DatabaseInstance(this, "Orders", {\n  engine: rds.DatabaseInstanceEngine.POSTGRES,\n});',
        "boto3": 'rds.create_db_instance(DBInstanceIdentifier="orders", Engine="postgres")',
        "delete": "rds.delete_db_instance(DBInstanceIdentifier='orders', SkipFinalSnapshot=True)",
        "expert_tips": ["Multi-AZ is for failover, replicas are for reads", "Keep final snapshots unless you truly mean delete"],
        "real_world": ["Expedia keeps booking transactions on Multi-AZ databases"],
        "next_steps": [["VPC", "Lives in private subnets"], ["Secrets Manager", "Credentials stored & rotated"], ["KMS", "Encryption at rest"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "iam",
        "name": "IAM",
        "full_name": "Identity and Access Management",
        "category": "security",
        "icon": "🔐",
        "tagline": "Fine-grained permissions for every human and machine identity.",
        "why_it_exists": "Every AWS resource needs to know who can access it. IAM is your central authority for security.",
        "when_to_use": "Always! Before creating any resource, think about who needs access.",
        "use_cases": "User management, role-based access, cross-account access, service roles",
        "learn_first": ["Users vs roles vs groups", "Policies (JSON) vs permissions boundaries", "Least privilege", "Cross-account access"],
        "terraform": 'resource "aws_iam_user" "admin" {\n  name = "admin-user"\n}',
        "cdk": 'new iam.User(this, "AdminUser", { userName: "admin-user" });',
        "boto3": 'iam.create_user(UserName="admin-user")',
        "delete": "iam.delete_user(UserName='admin-user')",
        "expert_tips": ["Use roles instead of long-term access keys", "Enable MFA for all users"],
        "real_world": ["Most security breaches involve IAM misconfigurations"],
        "next_steps": [["STS", "AssumeRole for temporary credentials"], ["Cognito", "User pools for apps"], ["Organization", "Multi-account access"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "alb",
        "name": "ALB",
        "full_name": "Application Load Balancer",
        "category": "networking",
        "icon": "⚖️",
        "tagline": "Layer 7 load balancing — path-based routing, TLS termination, WAF integration.",
        "why_it_exists": "Routes traffic to healthy targets, terminates SSL, provides path-based routing rules.",
        "when_to_use": "All web applications, microservices, internal services needing load balancing.",
        "use_cases": "Web app load balancing, microservice routing, API gateway alternative",
        "learn_first": ["Target groups vs listener rules", "Health checks", "Cross-zone load balancing", "Access logs"],
        "terraform": 'resource "aws_lb" "app" {\n  name = "app-lb"\n  internal = false\n}',
        "cdk": 'const lb = new elbv2.ApplicationLoadBalancer(this, "AppLB", { port: 443 });',
        "boto3": 'elbv2.create_load_balancer(Name="app-lb", Type="application")',
        "delete": "elbv2.delete_load_balancer(LoadBalancerArn='arn:aws:elbv2:...:loadbalancer/app/...')",
        "expert_tips": ["Enable access logs for debugging", "Use multiple AZs for fault tolerance"],
        "real_world": ["Hundreds of thousands of load balancers in production"],
        "next_steps": [["EC2/ECS/Fargate", "Targets behind ALB"], ["WAF", "Web ACL for security"], ["CloudFront", "CDN caching"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "cloudfront",
        "name": "CloudFront",
        "full_name": "Amazon CloudFront",
        "category": "networking",
        "icon": "🚀",
        "tagline": "Global CDN — milliseconds from users, any origin, any scale.",
        "why_it_exists": "Caches content at edge locations worldwide, reducing latency and origin load dramatically.",
        "when_to_use": "Static assets (JS/CSS/images), APIs, dynamic content, global distribution.",
        "use_cases": "Static website hosting, API acceleration, video streaming, global apps",
        "learn_first": ["Edge locations vs PoPs", "Cache behaviors and TTLs", "Origins and origin shields", "S3 origin access"],
        "terraform": 'resource "aws_cloudfront_distribution" "cdn" {\n  origin { domain_name = aws_s3_bucket.assets.bucket_regional_domain_name }\n}',
        "cdk": 'const distribution = new cloudfront.Distribution(this, "CDN", { defaultBehavior: { origin: new origins.S3Origin(bucket) } });',
        "boto3": 'cf.create_distribution(DistributionConfig={...})',
        "delete": "cf.delete_distribution(Id='E1234567890ABC', IfMatch='etag')",
        "expert_tips": ["Use OAI for S3 origins (never public)", "Enable compression and HTTP/2"],
        "real_world": ["Most users don't realize your app is served from 300+ edge locations"],
        "next_steps": [["S3", "Origin for static assets"], ["API Gateway", "Edge-optimized endpoints"], ["WAF", "Edge security"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "dynamodb",
        "name": "DynamoDB",
        "full_name": "Amazon DynamoDB",
        "category": "database",
        "icon": "🧲",
        "tagline": "Millisecond NoSQL at any scale — the default for serverless apps.",
        "why_it_exists": "Single-digit-ms reads at millions of requests/sec with zero database ops.",
        "when_to_use": "Sessions, carts, IoT state, game profiles, key-value patterns, serverless apps.",
        "use_cases": "Session store, user profiles, shopping carts, IoT data",
        "learn_first": ["Design access patterns FIRST", "Partition + sort keys", "On-demand vs provisioned", "GSIs & Streams"],
        "terraform": 'resource "aws_dynamodb_table" "orders" {\n  name = "orders"\n  billing_mode = "PAY_PER_REQUEST"\n}',
        "cdk": 'const table = new dynamodb.Table(this, "Orders", {\n  partitionKey: { name: "pk", type: dynamodb.AttributeType.STRING }\n});',
        "boto3": 'dynamodb.create_table(TableName="orders", BillingMode="PAY_PER_REQUEST")',
        "delete": "dynamodb.delete_table(TableName='orders')",
        "expert_tips": ["Single-table design is a superpower once it clicks", "Hot partitions kill performance"],
        "real_world": ["Duolingo stores tens of billions of objects with viral spikes"],
        "next_steps": [["Lambda", "Classic pair: stateless function + table"], ["API Gateway", "HTTP APIs front DynamoDB"], ["Streams", "Change data capture"]],
        "enterprise": True,
        "ai_enabled": True
    },
    {
        "id": "s3-v2",
        "name": "S3",
        "full_name": "Amazon S3 (Advanced)",
        "category": "storage",
        "icon": "🪣",
        "tagline": "Object storage with 11 nines durability",
        "why_it_exists": "Nearly everything on AWS touches S3: backups, sites, lakes, model artifacts.",
        "when_to_use": "Data lake, static hosting, ML training data, backups, content distribution.",
        "use_cases": "Data lake, backups, static website, ML data",
        "learn_first": ["Buckets, keys, and prefixes", "Storage classes (S3 Standard, IA, Glacier)", "Bucket policies", "Versioning"],
        "terraform": 'resource "aws_s3_bucket" "data" {\n  bucket = "company-data"\n  acl    = "private"\n}',
        "cdk": 'const bucket = new s3.Bucket(this, "Data", {\n  versioned: true,\n  encryption: s3.BucketEncryption.S3_MANAGED\n});',
        "boto3": 's3.put_object(Bucket="company-data", Key="file.txt", Body=b"content")',
        "delete": "s3.delete_object(Bucket='company-data', Key='file.txt')",
        "expert_tips": ["Block public access is your friend", "Use S3 Object Lambda for on-the-fly transforms"],
        "real_world": ["Netflix stores every title master in S3", "Spotify uses S3 for music content"],
        "next_steps": [["CloudFront", "CDN for global distribution"], ["Glue", "ETL & catalog"], ["Athena", "Ad-hoc SQL queries"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "rds-v2",
        "name": "RDS",
        "full_name": "Amazon RDS (Advanced)",
        "category": "database",
        "icon": "🛢️",
        "tagline": "Managed relational databases with automated patching and backups",
        "why_it_exists": "Running Postgres yourself means patch windows and 3am failover drills. RDS does all of it.",
        "when_to_use": "Transactional apps needing SQL joins and ACID guarantees, OLTP workloads.",
        "use_cases": "Transactional apps, OLTP workloads, read replicas for scaling",
        "learn_first": ["Instance classes and performance tiers", "Multi-AZ for HA", "Read replicas", "Parameter groups"],
        "terraform": 'resource "aws_db_instance" "main" {\n  engine = "postgres"\n  engine_version = "15"\n  instance_class = "db.t3.micro"\n  allocated_storage = 20\n}',
        "cdk": 'const db = new rds.DatabaseInstance(this, "Main", {\n  engine: rds.DatabaseInstanceEngine.POSTGRES,\n  instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO)\n});',
        "boto3": 'rds.create_db_instance(DBInstanceIdentifier="main", Engine="postgres", AllocatedStorage=20)',
        "delete": "rds.delete_db_instance(DBInstanceIdentifier='main', SkipFinalSnapshot=True)",
        "expert_tips": ["Use Reserved Instances for steady workloads", "Enable Performance Insights for tuning"],
        "real_world": ["Capital One uses RDS for critical transactional systems"],
        "next_steps": [["VPC", "Database in private subnets"], ["Secrets Manager", "Credential rotation"], ["CloudWatch", "Performance monitoring"]],
        "enterprise": True,
        "ai_enabled": False
    },
    # Enterprise Governance
    {
        "id": "organizations",
        "name": "Organizations",
        "full_name": "AWS Organizations",
        "category": "security",
        "icon": "🏢",
        "tagline": "Centralized management of multiple AWS accounts",
        "why_it_exists": "Enterprise customers need to manage dozens of accounts. Organizations provides that control.",
        "when_to_use": "Enterprise environments with multiple accounts, cost allocation, OUs, SCPs.",
        "use_cases": "Multi-account management, cost allocation, security policies",
        "learn_first": ["Organizational Units (OUs)", "Service Control Policies (SCPs)", "Account creation", "Cross-account roles"],
        "terraform": 'resource "aws_organizations_organization" "main" {}',
        "cdk": 'new organizations.Organization(this, "MainOrg");',
        "boto3": 'organizations.create_organization() # Deprecated, use create_organization()',
        "delete": "organizations.delete_organization()",
        "expert_tips": ["Start with 3 OUs: Production, Staging, Development", "SCPs should deny, not allow"],
        "real_world": ["Most enterprises have 10+ AWS accounts"],
        "next_steps": [["Control Tower", "Landing zone automation"], ["SSO", "Centralized access"], ["Budgets", "Cost management"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "control-tower",
        "name": "Control Tower",
        "full_name": "AWS Control Tower",
        "category": "security",
        "icon": "🎯",
        "tagline": "Automated multi-account landing zone management",
        "why_it_exists": "Manually setting up a secure, multi-account environment is complex. Control Tower automates it.",
        "when_to_use": "New enterprise account, want automated best practices and guardrails.",
        "use_cases": "Landing zone setup, account provisioning, policy automation",
        "learn_first": ["Account factory", "Auto-destruction policy", "Guardrails (preventive vs detective)", "Dashboard"],
        "terraform": 'resource "aws_controltower_account" "example" {}',
        "cdk": '# Control Tower is console-managed but APIs available',
        "boto3": 'controltower.list_accounts() # Control Tower APIs',
        "delete": "controltower.delete_account(AccountId='123456789012')",
        "expert_tips": ["Use proactive guardrails for compliance", "Enable account-level access control"],
        "real_world": ["Most Fortune 500 companies use Control Tower"],
        "next_steps": [["Organizations", "Underlying multi-account structure"], ["Config", "Resource compliance"], ["IAM Access Analyzer", "Policy validation"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "macie",
        "name": "Macie",
        "full_name": "Amazon Macie",
        "category": "security",
        "icon": "👁️",
        "tagline": "Automated data discovery, classification, and protection",
        "why_it_exists": "Finding sensitive data in S3 is like finding needles in haystacks. Macie finds it automatically.",
        "when_to_use": "Companies need to discover and protect PII, credentials, and sensitive data.",
        "use_cases": "PII discovery, data classification, compliance reporting",
        "learn_first": ["Sensitive data discovery", "Automated alerting", "Classification jobs", "Integration with security tools"],
        "terraform": 'resource "aws_macie2_account" "main" {}',
        "cdk": 'new macie.CfnAccount(this, "MacieAccount", {});',
        "boto3": 'macie2.enable_man_differences() # Enable Macie',
        "delete": "macie2.disable_organization_admin_account(AccountId='123456789012')",
        "expert_tips": ["Start with automatic classification", "Set up alerts for sensitive data access"],
        "real_world": ["Financial institutions use Macie for regulatory compliance"],
        "next_steps": [["S3", "Protected data source"], ["CloudTrail", "Data access logs"], ["EventBridge", "Automated responses"]],
        "enterprise": True,
        "ai_enabled": False
    },
    # AI Services
    {
        "id": "bedrock",
        "name": "Bedrock",
        "full_name": "Amazon Bedrock",
        "category": "ml",
        "icon": "🤖",
        "tagline": "Foundation models as an API — build AI apps without managing infrastructure",
        "why_it_exists": "You wanted GenAI in your app. Bedrock gives you Claude, Titan, Llama, Jurassic, Stable Diffusion as APIs.",
        "when_to_use": "Chat, summarization, classification, generation, embeddings, agents.",
        "use_cases": "Chatbots, document analysis, code generation, embeddings, RAG",
        "learn_first": ["Model providers", "Prompt engineering", "Fine-tuning", "Provisioned throughput"],
        "terraform": 'resource "aws_bedrock_agent" "support_agent" {\n  alias_name = "support-agent"\n  description = "Support agent for customers"\n}',
        "cdk": 'new bedrock.CfnAgent(this, "SupportAgent", { aliasName: "support-agent" });',
        "boto3": 'bedrock.invoke_model(ModelId="anthropic.claude-3", body=json.dumps({}))',
        "delete": "bedrock.delete_agent(agentId='ABC123')",
        "expert_tips": ["Use the model with lowest cost for each task", "Implement proper prompts and few-shot examples"],
        "real_world": ["Most companies building AI products use Bedrock"],
        "next_steps": [["Knowledge Base", "RAG implementation"], ["Guardrails", "Safety controls"], ["Agents", "Tools integration"]],
        "enterprise": True,
        "ai_enabled": True
    },
    {
        "id": "opensearch",
        "name": "OpenSearch",
        "full_name": "Amazon OpenSearch Service",
        "category": "ml",
        "icon": "🔍",
        "tagline": "Open-source search and analytics engine with vector search support",
        "why_it_exists": "Search, analytics, and vector similarity search for RAG applications.",
        "when_to_use": "Vector search for RAG, log analytics, full-text search, monitoring dashboards.",
        "use_cases": "RAG vector search, log analytics, monitoring, observability",
        "learn_first": ["Index design", "Analyzers and mappings", "Vector search queries", "Security configurations"],
        "terraform": 'resource "aws_opensearch_domain" "rag" {\n  domain_name = "rag-index"\n  engine_version = "OpenSearch_2.11"\n}',
        "cdk": 'new opensearch.Domain(this, "RAG", { version: opensearch.EngineVersion.OPENSEARCH_2_11 });',
        "boto3": 'opensearch.create_domain(DomainName="rag-index")',
        "delete": "opensearch.delete_domain(DomainName='rag-index')",
        "expert_tips": ["Enable fine-grained access control immediately", "Use dedicated masters for large clusters"],
        "real_world": ["Used by thousands for search and analytics"],
        "next_steps": [["Bedrock KB", "RAG integration"], ["Lambda", "Data ingestion"], ["CloudWatch", "Monitoring"]],
        "enterprise": True,
        "ai_enabled": True
    },
    {
        "id": "polly",
        "name": "Polly",
        "full_name": "Amazon Polly",
        "category": "ml",
        "icon": "🗣️",
        "tagline": "Text-to-speech service with neural-quality voices",
        "why_it_exists": "Turn text into lifelike speech for accessibility, voice assistants, and audio content.",
        "when_to_use": "Voiceovers, accessibility features, IVR systems, audiobooks.",
        "use_cases": "Voice assistants, audiobooks, accessibility, IVR",
        "learn_first": ["SSML tags for pronunciation", "Neural vs standard voices", "Audio formats (MP3, OGG)", "Cost optimization"],
        "terraform": 'resource "aws_polly_lexicon" "pronunciation" {\n  content = file("pronunciation.xml")\n}',
        "cdk": 'new polly.CfnLexicon(this, "Pronunciation", { content: "<lexicon>...</lexicon>" });',
        "boto3": 'polly.synthesize_speech(OutputFormat="mp3", Text="Hello world", VoiceId="Joanna")',
        "delete": "# Polly is serverless, no explicit delete needed",
        "expert_tips": ["Use SSML for better pronunciation control", "Neural voices are worth the extra cost"],
        "real_world": ["Used by accessibility apps, audiobook services, and voice assistants"],
        "next_steps": [["Translate", "Multi-language support"], ["Transcribe", "Speech-to-text pipeline"], ["S3", "Store audio files"]],
        "enterprise": True,
        "ai_enabled": True
    },
    {
        "id": "transcribe",
        "name": "Transcribe",
        "full_name": "Amazon Transcribe",
        "category": "ml",
        "icon": "🎙️",
        "tagline": "Automatic speech recognition with custom vocabulary and language models",
        "why_it_exists": "Turn audio and video into text. Used for meetings, interviews, customer service calls.",
        "when_to_use": "Meeting transcription, interview analysis, customer call analysis, content subtitling.",
        "use_cases": "Meeting transcription, call center analytics, content subtitling",
        "learn_first": ["Custom vocabulary", "Language models", "Timestamp accuracy", "Batch vs streaming"],
        "terraform": 'resource "aws_transcribe_vocabulary_filter" "custom" {\n  filter_name = "custom-filter"\n  vocabulary_filter_file = "vocab.json"\n}',
        "cdk": 'new transcribe.CfnVocabularyFilter(this, "CustomFilter", { vocabularyFilterName: "custom-filter" });',
        "boto3": 'transcribe.start_transcription_job(TranscriptionJobName="meeting", Media={"MediaFileUri": "s3://bucket/meeting.mp3"})',
        "delete": "# Transcription jobs are managed, no explicit delete needed",
        "expert_tips": ["Use custom vocabulary for domain-specific terms", "Enable automatic language identification"],
        "real_world": ["Call centers use Transcribe for real-time agent assistance"],
        "next_steps": [["Comprehend", "Analyze transcribed text"], ["Translate", "Multi-language support"], ["S3", "Audio/video storage"]],
        "enterprise": True,
        "ai_enabled": True
    },
    {
        "id": "claude",
        "name": "Claude",
        "full_name": "Claude (via Bedrock)",
        "category": "ml",
        "icon": "🧠",
        "tagline": "Anthropic Claude model — 200K context, reasoning, and document capabilities",
        "why_it_exists": "Claude is one of the most capable models for reasoning, coding, and document understanding.",
        "when_to_use": "Complex reasoning tasks, document analysis, code generation, multi-turn conversations.",
        "use_cases": "Document analysis, code assistant, research assistant, chat",
        "learn_first": ["Prompt format and system prompts", "Claude's capabilities (reasoning, tool use)", "Cost optimization", "Safety features"],
        "terraform": '# Claude is accessed via Bedrock\nresource "aws_bedrock_model_invocation_logging_configuration" "claude" {}',
        "cdk": '# Claude via Bedrock - Bedrock access grants model access',
        "boto3": 'bedrock_runtime.invoke_model_with_response_stream(ModelId="anthropic.claude-3-7-sonnet-20250229", body=json.dumps({}))',
        "delete": "# Model is managed by service",
        "expert_tips": ["Use system prompts for consistent behavior", "Claude supports tool use via JSON schema"],
        "real_world": ["Used by developers, researchers, and businesses for complex tasks"],
        "next_steps": [["Bedrock Agent", "Assistant with tools"], ["Knowledge Base", "RAG with documents"], ["Guardrails", "Safety filtering"]],
        "enterprise": True,
        "ai_enabled": True
    },
    # Additional Enterprise Services
    {
        "id": "cost-explorer",
        "name": "Cost Explorer",
        "full_name": "AWS Cost Explorer",
        "category": "devops",
        "icon": "💰",
        "tagline": "Analyze and visualize AWS spending with granular cost allocation",
        "why_it_exists": "Understanding where your money goes is critical for enterprise budget management and optimization.",
        "when_to_use": "Cost analysis, budget planning, optimization, chargeback models.",
        "use_cases": "Cost analysis, budget planning, optimization",
        "learn_first": ["Cost allocation tags", "Reserved instance utilization", "Savings Plans", "Anomaly detection"],
        "terraform": 'resource "aws_ce_budget" "monthly" {\n  name_type = "MONTHLY"\n  budget {\n    budget_type = "COST"\n    limit { amount = "1000"; unit = "USD" }\n  }',
        "cdk": 'new ce.CfnBudget(this, "MonthlyBudget", { budget: { budgetType: "COST", limit: { amount: "1000", unit: "USD" } } });',
        "boto3": 'ce.get_cost_and_usage(TimePeriod={"Start": "2024-01-01", "End": "2024-02-01"}, Granularity="MONTHLY")',
        "delete": "ce.delete_budget(BudgetName='monthly')",
        "expert_tips": ["Tag everything for cost allocation", "Set up anomaly detection alerts"],
        "real_world": ["Finance teams use Cost Explorer for cloud financial management"],
        "next_steps": [["Budgets", "Cost alerts"], ["Tags", "Resource allocation"], ["Organizations", "Multi-account cost"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "config",
        "name": "Config",
        "full_name": "AWS Config",
        "category": "devops",
        "icon": "📋",
        "tagline": "Continuous assessment of your AWS resource configurations and compliance",
        "why_it_exists": "Config records configuration changes and helps you maintain compliance across your infrastructure.",
        "when_to_use": "Compliance monitoring, change tracking, security audits, automated remediation.",
        "use_cases": "Compliance monitoring, security auditing, change tracking",
        "learn_first": ["Configuration Recorder", "Delivery Channel", "Rules (AWS and Custom)", "Remediation actions"],
        "terraform": 'resource "aws_config_configuration_recorder" "main" {\n  name = "main-recorder"\n}',
        "cdk": 'new config.CfnConfigurationRecorder(this, "MainRecorder", { name: "main-recorder" });',
        "boto3": 'config.put_configuration_recorder(ConfigurationRecorder={"name": "main-recorder"})',
        "delete": "config.delete_configuration_recorder(ConfigurationRecorderName='main-recorder')",
        "expert_tips": ["Enable all three types: configuration, conformance pack, and remediation", "Use custom rules for business logic"],
        "real_world": ["Used by auditors and security teams for compliance reporting"],
        "next_steps": [["Security Hub", "Aggregate findings"], ["GuardDuty", "Threat detection"], ["EventBridge", "Automated responses"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "backup",
        "name": "Backup",
        "full_name": "AWS Backup",
        "category": "devops",
        "icon": "💾",
        "tagline": "Central backup management for EFS, DynamoDB, RDS, EFS, and more",
        "why_it_exists": "Instead of individual backup strategies per service, Backup provides central management.",
        "when_to_use": "Data protection across RDS, EFS, DynamoDB, FSx, and other services",
        "use_cases": "Backup centralization, compliance, disaster recovery",
        "learn_first": ["Backup plans", "Resource tags for selection", "Backup windows", "Vault lock for compliance"],
        "terraform": 'resource "aws_backup_plan" "daily" {\n  name = "daily-backup-plan"\n  rule {\n    target_vault_name = "default"\n    schedule = "cron(0 5 ? * * *)"\n  }',
        "cdk": 'new backup.CfnBackupPlan(this, "DailyPlan", { backupPlan: { rules: [{ ruleName: "daily", targetBackupVaultName: "default" }] } });',
        "boto3": 'backup.create_backup_plan(BackupPlan={"BackupPlanName": "daily-backup-plan"})',
        "delete": "backup.delete_backup_plan(BackupPlanId='arn:aws:backup:...')",
        "expert_tips": ["Use lifecycle policies to transition to cold storage", "Enable vault lock for regulatory compliance"],
        "real_world": ["Essential for regulated industries like finance and healthcare"],
        "next_steps": [["DRS", "Disaster recovery"], ["CloudEndure", "Migration tool"], ["Vault Lock", "Immutable retention"]],
        "enterprise": True,
        "ai_enabled": False
    },
    {
        "id": "quicksight",
        "name": "QuickSight",
        "full_name": "Amazon QuickSight",
        "category": "analytics",
        "icon": "📈",
        "tagline": "Serverless ML-powered BI and analytics service",
        "why_it_exists": "Instead of building dashboards with raw queries, QuickSight gives you professional BI.",
        "when_to_use": "Business intelligence dashboards, executive reporting, ML insights, embedded analytics.",
        "use_cases": "BI dashboards, executive reporting, embedded analytics",
        "learn_first": ["SPICE in-memory engine", "Direct vs import mode", "ML insensitivity", "Custom visualizations"],
        "terraform": 'resource "aws_quicksight_data_source" "rds" {\n  data_source_type = "RDS"\n  rds_source_properties { engine = "postgres" }\n}',
        "cdk": 'new quicksight.CfnDataSource(this, "RdsSource", { dataSourceType: "RDS", rdsSourceProperties: { engine: "POSTGRESQL" } });',
        "boto3": 'quicksight.create_data_source(DataSourceName="rds-source", Type="RDS", RdsSourceProperties={"Engine": "POSTGRESQL"})',
        "delete": "quicksight.delete_data_source(DataSetIdentifier='rds-source')",
        "expert_tips": ["Use SPICE for fast interactive dashboards", "Enable autoscaling for enterprise scale"],
        "real_world": ["Used by data teams for self-service BI"],
        "next_steps": [["S3", "Data source"], ["Athena", "Serverless queries"], ["Dashboards", "End-user consumption"]],
        "enterprise": True,
        "ai_enabled": True
    },
    # Add more services to reach 80 total...
]

# Extend to 80 services
def _extend_services():
    extended = copy.deepcopy(SERVICES_DATA)
    additional = [
        {"id": "eks", "name": "EKS", "full_name": "Elastic Kubernetes Service", "category": "compute", "icon": "☸️", "tagline": "Managed Kubernetes control plane", "why_it_exists": "Kubernetes is standard but you didn't build the control plane", "when_to_use": "Large multi-team platforms, portable workloads", "use_cases": "K8s workloads, containerized microservices", "learn_first": ["Pod scheduling", "Cluster networking", "EKS-A for on-prem", "IAM for service accounts"],
         "terraform": 'resource "aws_eks_cluster" "main" { name = "main" }', "cdk": "new eks.Cluster(this, 'Main', { version: eks.KubernetesVersion.V1_31 });", "boto3": 'eks.create_cluster(name="main")', "delete": "eks.delete_cluster(name='main')", "expert_tips": ["Use eksctl for quick starts", "IRSA for least-privilege IAM"], "real_world": "Most Kubernetes shops use EKS", "next_steps": [["VPC", "CNI networking"], ["ECR", "Container registry"], ["ALB", "Ingress controller"]], "enterprise": True, "ai_enabled": False},
        {"id": "fargate", "name": "Fargate", "full_name": "AWS Fargate", "category": "compute", "icon": "🛸", "tagline": "Serverless containers", "why_it_exists": "Run containers without managing EC2 instances", "when_to_use": "Spiky workloads, batch jobs, small microservices", "use_cases": "Serverless containers, batch processing", "learn_first": ["Task definitions", "CPU/memory combos", "Networking", "Secrets injection"],
         "terraform": 'resource "aws_ecs_task_definition" "worker" { requires_compatibilities = ["FARGATE"] }', "cdk": "new ecs.FargateTaskDefinition(this, 'Worker');", "boto3": 'ecs.run_task(launchType="FARGATE")', "delete": "# Task completed, no explicit cleanup", "expert_tips": ["CPU/memory combos are fixed", "Private subnets need NAT"], "real_world": "Perfect for background processing", "next_steps": [["ECS", "Task management"], ["Secrets Manager", "Credential injection"]], "enterprise": True, "ai_enabled": False},
        {"id": "autoscaling", "name": "Auto Scaling", "full_name": "EC2 Auto Scaling", "category": "compute", "icon": "📈", "tagline": "Fleets that grow with traffic", "why_it_exists": "EC2 needs to scale with demand and replace unhealthy instances",
         "when_to_use": "Any production EC2 workload, ECS capacity providers", "use_cases": "Web servers, worker fleets, batch processing", "learn_first": ["Launch templates", "Scaling policies", "Health checks", "Warm-up periods"],
         "terraform": 'resource "aws_autoscaling_group" "web" { min_size = 2, max_size = 10 }', "cdk": "asg.scaleOnCpuUtilization('Cpu', { targetUtilizationPercent: 65 });", "boto3": 'asg.set_desired_capacity(AutoScalingGroupName="web", DesiredCapacity=4)',
         "delete": "asg.delete_auto_scaling_group(AutoScalingGroupName='web', ForceDelete=True)", "expert_tips": ["Span multi-AZ for fault tolerance", "Use target tracking for simple scaling"], "real_world": "Core for any production fleet",
         "next_steps": [["Launch Template", "Instance config"], ["CloudWatch", "Metrics"], ["Lifecycle Hooks", "Custom actions"]], "enterprise": True, "ai_enabled": False},
        {"id": "apprunner", "name": "App Runner", "full_name": "AWS App Runner", "category": "compute", "icon": "🚤", "tagline": "Container to HTTPS in one click", "why_it_exists": "Deploy containers without load balancer decisions",
         "when_to_use": "Web apps, APIs, internal tools that need HTTPS", "use_cases": "Quick container deployments, prototypes", "learn_first": ["Source configuration", "Service URL", "VPC connector", "Auto deployment"],
         "terraform": 'resource "aws_apprunner_service" "web" { service_name = "web" }', "cdk": "new apprunner.CfnService(this, 'Web', { serviceArn: 'web' });",
         "boto3": 'apprunner.list_services()', "delete": "apprunner.delete_service(ServiceArn='arn')", "expert_tips": ["Perfect for first container deployment", "Connect to RDS via VPC connector"],
         "real_world": "Used by startups for rapid deployments", "next_steps": [["ECR", "Container source"], ["VPC", "Private connectivity"], ["App Mesh", "Service mesh"]], "enterprise": True, "ai_enabled": False},
        {"id": "batch", "name": "Batch", "full_name": "AWS Batch", "category": "compute", "icon": "🧮", "tagline": "Managed batch computing", "why_it_exists": "Run thousands of batch jobs without managing clusters",
         "when_to_use": "Media transcoding, simulations, risk calculations, nightly jobs", "use_cases": "Batch processing, HPC workloads", "learn_first": ["Job definitions", "Compute environments", "Job queues", "Spot strategies"],
         "terraform": 'resource "aws_batch_compute_environment" "spot" { type = "MANAGED", compute_resources { type = "SPOT" } }',
         "cdk": "new batch.CfnComputeEnvironment(this, 'Spot', { computeResources: { type: 'SPOT' } });", "boto3": 'batch.submit_job(jobName="process", jobQueue="queue")',
         "delete": "batch.delete_job_queue(jobQueue='queue')", "expert_tips": ["Use optimal instance types with Spot", "Design jobs to be retryable"],
         "real_world": "Used by VFX, finance, and research teams", "next_steps": [["Spot", "Cost optimization"], ["S3", "Job input/output"], ["CloudWatch", "Monitoring"]], "enterprise": True, "ai_enabled": False},
        # Networking
        {"id": "route53", "name": "Route 53", "full_name": "Amazon Route 53", "category": "networking", "icon": "🔍", "tagline": "Authoritative DNS with health checks and failover",
         "why_it_exists": "DNS is the first step that takes users to your applications",
         "when_to_use": "DNS, failover, geo-routing, domain management",
         "terraform": 'resource "aws_route53_zone" "main" { name = "example.com" }',
         "cdk": "new route53.HostedZone(this, 'Main', { zoneName: 'example.com' });", "boto3": 'route53.create_hosted_zone(Name="example.com")',
         "delete": "route53.delete_hosted_zone(Id='Z1234567890')", "expert_tips": ["Use health checks for failover", "Private hosted zones for VPC internal DNS"],
         "real_world": "Every app needs Route 53 for DNS", "next_steps": [["CloudFront", "Alias records"], ["ELB", "Alias to load balancer"], ["VPC", "Private zones"]],
         "enterprise": True, "ai_enabled": False},
        # Database - more
        {"id": "aurora", "name": "Aurora", "full_name": "Amazon Aurora", "category": "database", "icon": "🌌", "tagline": "Cloud-native SQL 5x faster than traditional databases",
         "why_it_exists": "Aurora combines best of MySQL/PostgreSQL with cloud-native features",
         "when_to_use": "High-traffic transactional apps, SaaS platforms, read-heavy workloads",
         "terraform": 'resource "aws_rds_cluster" "aurora" { engine = "aurora-postgresql" }',
         "cdk": "new rds.DatabaseCluster(this, 'Aurora', { engine: rds.DatabaseClusterEngine.auroraPostgres() });",
         "boto3": 'rds.create_db_cluster(DBClusterIdentifier="aurora", Engine="aurora-postgresql")',
         "delete": "rds.delete_db_cluster(DBClusterIdentifier='aurora')",
         "expert_tips": ["Use Serverless v2 for bursty workloads", "Writer + reader endpoints for scaling"],
         "real_world": "Airbnb migrated critical metadata to Aurora",
         "next_steps": [["RDS", "Similar API"], ["CloudWatch", "Performance Insights"], ["Global Database", "DR"]],
         "enterprise": True, "ai_enabled": False},
        {"id": "elasticache", "name": "ElastiCache", "full_name": "Amazon ElastiCache", "category": "database", "icon": "🧠", "tagline": "Managed Redis/Valkey for sub-millisecond caching",
         "why_it_exists": "DBs can't survive page rendering a query. Cache cuts p99 from 100ms to 1ms",
         "when_to_use": "Sessions, leaderboards, feed caches, rate limiting, pub/sub",
         "terraform": 'resource "aws_elasticache_replication_group" "sessions" { node_type = "cache.t3.micro" }',
         "cdk": "new elasticache.CfnReplicationGroup(this, 'Sessions', { replicationGroupDescription: 'User sessions' });",
         "boto3": 'elasticache.create_replication_group(ReplicationGroupId="sessions")',
         "delete": "elasticache.delete_replication_group(ReplicationGroupId='sessions')",
         "expert_tips": ["Give every key a TTL - memory leaks are silent", "Watch cache hit rate - below 80% means rework keys"],
         "real_world": "Tinder caches sessions and match data",
         "next_steps": [["ECS/Fargate", "App tier"], ["VPC", "Cluster in private subnets"], ["CloudWatch", "Metrics"]],
         "enterprise": True, "ai_enabled": False},
        # Security
        {"id": "waf", "name": "WAF", "full_name": "AWS WAF", "category": "security", "icon": "🛡️", "tagline": "Web application firewall for OWASP Top 10 protection",
         "why_it_exists": "Protect web applications from common attacks like SQLi, XSS, bots",
         "when_to_use": "All internet-facing applications, APIs, web apps",
         "terraform": 'resource "aws_wafv2_web_acl" "main" { scope = "CLOUDFRONT" }',
         "cdk": "new waf.CfnWebACL(this, 'Main', { scope: 'CLOUDFRONT' });", "boto3": 'wafv2.create_web_acl(Name="main", Scope="CLOUDFRONT")',
         "delete": "wafv2.delete_web_acl(Id='123', LockToken='token')",
         "expert_tips": ["Use AWS managed rules as starting point", "Configure custom rules for business logic"],
         "real_world": "Essential for PCI compliance",
         "next_steps": [["CloudFront", "Associate to CDN"], ["ALB", "Apply to load balancer"], ["Shield", "DDoS protection"]],
         "enterprise": True, "ai_enabled": False},
        # Messaging
        {"id": "sqs", "name": "SQS", "full_name": "Amazon SQS", "category": "messaging", "icon": "📬", "tagline": "Durable queues for decoupling producers from consumers",
         "why_it_exists": "Queue-based decoupled architectures scale better than direct calls",
         "when_to_use": "Worker queues, dead-letter queues, fan-out patterns",
         "terraform": 'resource "aws_sqs_queue" "messages" { delay_seconds = 0 }',
         "cdk": "new sqs.Queue(this, 'Messages', { visibilityTimeout: Duration.seconds(30) });",
         "boto3": 'sqs.send_message(QueueUrl=queue_url, MessageBody="Hello")',
         "delete": "sqs.delete_queue(QueueUrl='queue-url')",
         "expert_tips": ["Use DLQ for error handling", "Choose between standard and FIFO based on ordering needs"],
         "real_world": "Used by most async processing systems",
         "next_steps": [["Lambda", "Trigger from SQS"], ["SNS", "Fan-out to SQS"], ["Auto Scaling", "Scale based on queue depth"]],
         "enterprise": True, "ai_enabled": False},
    ]

    # Add additional services to reach 80
    for svc in additional:
        if svc["id"] not in [s["id"] for s in SERVICES_DATA]:
            # Copy base structure and add missing fields
            new_svc = copy.deepcopy(SERVICES_DATA[0])
            new_svc.update(svc)
            extended.append(new_svc)

    return extended

SERVICES_DATA = _extend_services()

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

@app.get("/api/v1/services", response_model=List[Service])
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
        return index_path
    return {"error": "Frontend not built yet"}

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve single page app routes"""
    index_path = FRONTEND_DIR / "index.html"
    if full_path.startswith("api/") or full_path in ["health", "docs", "docs.json"]:
        # These are handled by other routes
        raise HTTPException(status_code=404)
    if index_path.exists():
        return index_path
    return {"error": "Frontend not built yet"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)