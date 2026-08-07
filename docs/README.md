# AWS Atlas Pro — Service Documentation

**100 AWS services**, each with a full reference page: tagline, why-it-exists, when-to-use, learning checklist, Terraform / CDK / Boto3 / delete code, expert tips, a real-world example, and next-step links.

- [API reference](api.md)
- [Real-world industry scenarios & failure modes](industry-issues.md)
- [Privacy & data model](PRIVACY.md)

## Analytics (8)

- [🦉 Amazon Athena (`athena`)](services/athena.md) — SQL straight against S3 — no cluster, no loading, pay per query.
- [📊 AWS Cost Explorer (`costexplorer`)](services/costexplorer.md) — See, filter and forecast what you spend on AWS — by service, account, tag or day.
- [🐘 Elastic MapReduce (`emr`)](services/emr.md) — Managed Spark / Hadoop clusters for heavy big-data lifting.
- [🧪 AWS Glue (`glue`)](services/glue.md) — Serverless Spark ETL + the catalog that makes S3 data queryable.
- [🌊 Amazon Kinesis (`kinesis`)](services/kinesis.md) — Real-time streaming at scale — ingest millions of events per second.
- [🏞️ AWS Lake Formation (`lakeformation`)](services/lakeformation.md) — Fine-grained permissions over the lake — column-level security, no IAM acrobatics.
- [🎛️ Managed Streaming for Apache Kafka (`msk`)](services/msk.md) — Managed Apache Kafka — the event backbone for serious streaming platforms.
- [📉 Amazon QuickSight (`quicksight`)](services/quicksight.md) — Serverless BI dashboards — pay per session, embed anywhere, ask Q.

## Compute (11)

- [🚤 AWS App Runner (`apprunner`)](services/apprunner.md) — Container to public HTTPS in one click — the simplest compute on AWS.
- [📈 EC2 Auto Scaling (`autoscaling`)](services/autoscaling.md) — Fleets that grow with traffic and replace themselves when they break.
- [🧮 AWS Batch (`batch`)](services/batch.md) — Managed batch computing — thousands of jobs, right-sized and Spot-priced.
- [🖥️ Elastic Compute Cloud (`ec2`)](services/ec2.md) — Rent virtual servers by the second — the original building block of the cloud.
- [🐳 Elastic Container Service (`ecs`)](services/ecs.md) — AWS-native container orchestration — Docker without the Kubernetes tax.
- [☸️ Elastic Kubernetes Service (`eks`)](services/eks.md) — Managed Kubernetes control plane — the industry standard, minus the ops.
- [🌱 AWS Elastic Beanstalk (`elasticbeanstalk`)](services/elasticbeanstalk.md) — Paste your app code; AWS provisions the servers, load balancer and scaling for you.
- [🛸 AWS Fargate (`fargate`)](services/fargate.md) — Serverless compute for containers — no hosts, no patching, just tasks.
- [🖼️ EC2 Image Builder (`imagebuilder`)](services/imagebuilder.md) — Build and maintain golden AMIs. Recipes, pipelines, automated patching on a schedule.
- [λ AWS Lambda (`lambda`)](services/lambda.md) — Run code on events. Zero servers, pay per 128ms slice.
- [💡 Amazon Lightsail (`lightsail`)](services/lightsail.md) — Simplest way to launch a VM or container — fixed price, predictable, zero cloud jargon.

## Database (10)

- [🌌 Amazon Aurora (`aurora`)](services/aurora.md) — Cloud-native SQL — several times the throughput, storage that never runs out.
- [🍃 Amazon DocumentDB (`documentdb`)](services/documentdb.md) — MongoDB-compatible, fully managed document database.
- [🧲 Amazon DynamoDB (`dynamodb`)](services/dynamodb.md) — Millisecond NoSQL at any scale — the default for serverless apps.
- [🧠 Amazon ElastiCache (`elasticache`)](services/elasticache.md) — Managed Redis / Valkey — sub-millisecond memory in front of everything.
- [⚡ Amazon MemoryDB (`memorydb`)](services/memorydb.md) — Redis-compatible, durable in-memory database — for when losing data is not an option.
- [🔱 Amazon Neptune (`neptune`)](services/neptune.md) — Graph database for relationships — fraud rings, social graphs, knowledge.
- [🔎 Amazon OpenSearch Service (`opensearch`)](services/opensearch.md) — Search + analytics + the vector engine behind most AWS RAG stacks.
- [🛢️ Relational Database Service (`rds`)](services/rds.md) — Managed SQL databases — patching, backups and failover on autopilot.
- [📊 Amazon Redshift (`redshift`)](services/redshift.md) — Petabyte-scale data warehouse for the questions joins were born to answer.
- [⏱️ Amazon Timestream (`timestream`)](services/timestream.md) — Serverless time-series database for IoT, telemetry and metrics.

## Management & Governance (13)

- [🎯 AWS Budgets (`budgets`)](services/budgets.md) — Set spend limits and get alerted before the invoice surprises you.
- [🏗️ AWS CloudFormation (`cloudformation`)](services/cloudformation.md) — AWS-native infrastructure-as-code — the engine under CDK itself.
- [🥾 AWS CloudTrail (`cloudtrail`)](services/cloudtrail.md) — Who did what, when, from where — every API call, recorded.
- [👁️ Amazon CloudWatch (`cloudwatch`)](services/cloudwatch.md) — Metrics, logs, alarms and dashboards — the nervous system of AWS.
- [🧱 AWS CodeBuild (`codebuild`)](services/codebuild.md) — Serverless build farm — compile, test and containerize on demand.
- [🚀 AWS CodeDeploy (`codedeploy`)](services/codedeploy.md) — Zero-downtime deployments to EC2 fleets — with automatic rollback.
- [🔁 AWS CodePipeline (`codepipeline`)](services/codepipeline.md) — CI/CD orchestrator — commit, build, test, deploy on rails.
- [📋 AWS Config (`config`)](services/config.md) — Continuous inventory of your infrastructure + compliance rules as code.
- [📦 Elastic Container Registry (`ecr`)](services/ecr.md) — Private Docker registry — scan on push, immutable tags, lifecycle policies.
- [🧞 Amazon Q Developer (`qdeveloper`)](services/qdeveloper.md) — AWS's AI pair programmer — code gen, upgrades, chat in the IDE & console.
- [🔧 AWS Systems Manager (`ssm`)](services/ssm.md) — The remote-control plane for fleets — sessions, patches, parameters.
- [🛡️ AWS Trusted Advisor (`trustedadvisor`)](services/trustedadvisor.md) — AWS's built-in auditor — security, cost, performance and fault-tolerance checks across your account.
- [🧵 AWS X-Ray (`xray`)](services/xray.md) — Distributed tracing — follow one request across every service it touched.

## Application Integration (9)

- [🔗 AWS AppSync (`appsync`)](services/appsync.md) — Managed GraphQL API — realtime subscriptions, offline sync, many data sources.
- [📞 Amazon Connect (`connect`)](services/connect.md) — Cloud contact center — IVR, queues, agent desktops, analytics. Pay per minute.
- [🚌 Amazon EventBridge (`eventbridge`)](services/eventbridge.md) — The event bus every AWS service plugs into — rules react to anything.
- [📡 AWS IoT Core (`iot`)](services/iot.md) — Connect millions of devices. MQTT pub/sub, device shadows, rules that route telemetry.
- [📣 Amazon Pinpoint (`pinpoint`)](services/pinpoint.md) — Multi-channel engagement — email, SMS, push, in-app. Segment, send, measure.
- [✉️ Amazon Simple Email Service (`ses`)](services/ses.md) — Transactional and bulk email at scale — deliverability handled.
- [📢 Simple Notification Service (`sns`)](services/sns.md) — Publish once, deliver everywhere — fan-out messaging.
- [📬 Simple Queue Service (`sqs`)](services/sqs.md) — A queue between services — spikes land here, workers drain at their pace.
- [🪜 AWS Step Functions (`stepfunctions`)](services/stepfunctions.md) — Visual state machines — orchestrate Lambdas, jobs and humans with retries.

## Migration & Transfer (3)

- [🔄 AWS DataSync (`datasync`)](services/datasync.md) — High-speed mover for on-prem ↔ AWS — NFS/SMB/S3 at up to 10 Gbps.
- [🚚 Database Migration Service (`dms`)](services/dms.md) — Migrate live databases to AWS with near-zero downtime — including CDC.
- [❄️ Snowball / Snowmobile (`snow`)](services/snow.md) — Petabyte-mover by truck — when the network is simply too slow.

## Machine Learning & AI (14)

- [🪨 Amazon Bedrock (`bedrock`)](services/bedrock.md) — Foundation models via one API — Claude, Nova & friends, no GPUs to babysit.
- [🦾 Agents for Amazon Bedrock (`bedrockagents`)](services/bedrockagents.md) — Give an LLM tools, knowledge and memory — and ship it with AgentOps.
- [🚧 Amazon Bedrock Guardrails (`bedrockguardrails`)](services/bedrockguardrails.md) — Policy rails for GenAI — block toxic, off-topic and PII-leaking traffic.
- [📚 Bedrock Knowledge Bases (`bedrockkb`)](services/bedrockkb.md) — RAG as a service — your documents become a live, searchable knowledge base.
- [📝 Amazon Comprehend (`comprehend`)](services/comprehend.md) — NLP as an API: sentiment, entities, key phrases, PII, language.
- [📈 Amazon Forecast (`forecast`)](services/forecast.md) — Time-series forecasting with ML — demand, staffing, capacity — without building models.
- [🔍 Amazon Kendra (`kendra`)](services/kendra.md) — Enterprise search powered by ML — answers from your documents, not a keyword list.
- [🗨️ Amazon Lex (`lex`)](services/lex.md) — Managed conversational bots — the engine behind Alexa-style dialog.
- [🎯 Amazon Personalize (`personalize`)](services/personalize.md) — ML-based recommendations — 'customers also bought' — without a data-science team.
- [🔊 Amazon Polly (`polly`)](services/polly.md) — Text-to-speech API — turn content into natural, human-like voices.
- [📸 Amazon Rekognition (`rekognition`)](services/rekognition.md) — Vision as an API call: labels, faces, moderation, text in images & video.
- [🤖 Amazon SageMaker (`sagemaker`)](services/sagemaker.md) — The full ML workshop: notebooks, training jobs, registries, endpoints.
- [📄 Amazon Textract (`textract`)](services/textract.md) — Extract tables, forms and handwriting from any scanned document.
- [🎙️ Amazon Transcribe (`transcribe`)](services/transcribe.md) — Speech-to-text at scale — calls, meetings, media archives.

## Networking & Delivery (10)

- [⚖️ Application Load Balancer (`alb`)](services/alb.md) — Layer-7 load balancing — routes by path, host, header; terminates TLS.
- [🚪 Amazon API Gateway (`apigateway`)](services/apigateway.md) — The front door for your APIs — auth, throttling, routing, metering.
- [🌍 Amazon CloudFront (`cloudfront`)](services/cloudfront.md) — The CDN — your content served from 310+ edge locations worldwide.
- [🔌 AWS Direct Connect (`directconnect`)](services/directconnect.md) — A private fiber line from your data center straight into AWS.
- [🛰️ AWS Global Accelerator (`globalaccelerator`)](services/globalaccelerator.md) — Two static anycast IPs + AWS backbone routing across regions.
- [🚦 Network Load Balancer (`nlb`)](services/nlb.md) — Layer-4 load balancer — millions of connections/sec, static IPs, TCP/UDP/TLS.
- [🔐 AWS PrivateLink (`privatelink`)](services/privatelink.md) — Consume services across VPCs & accounts over the AWS backbone — no internet.
- [🧭 Amazon Route 53 (`route53`)](services/route53.md) — DNS with superpowers: health checks, failover, latency routing.
- [🔀 AWS Transit Gateway (`tgw`)](services/tgw.md) — One hub that connects every VPC, on-prem network and shared service.
- [🕸️ Virtual Private Cloud (`vpc`)](services/vpc.md) — Your private network in AWS — the boundary every other service lives inside.

## Security, Identity & Compliance (16)

- [📜 Certificate Manager (`acm`)](services/acm.md) — Free TLS certificates, issued and auto-renewed.
- [📋 AWS Audit Manager (`auditmanager`)](services/auditmanager.md) — Automate audit evidence collection. Map controls to resources, get a ready-to-review report.
- [👤 Amazon Cognito (`cognito`)](services/cognito.md) — Production sign-up/sign-in without building an auth server.
- [🗼 AWS Control Tower (`controltower`)](services/controltower.md) — Landing zone as code — guardrails, account vending, baseline security.
- [🕵️ Amazon Detective (`detective`)](services/detective.md) — Graph-based investigation of suspicious activity. Walk the blast radius of a GuardDuty finding.
- [🚨 Amazon GuardDuty (`guardduty`)](services/guardduty.md) — ML-powered threat detection — finds the crypto-miner before finance does.
- [🪪 Identity & Access Management (`iam`)](services/iam.md) — Who can do what, where. Learn this before literally everything else.
- [🎫 IAM Identity Center (SSO) (`idc`)](services/idc.md) — SSO for humans — one login to every account, mapped to permission sets.
- [🐞 Amazon Inspector (`inspector`)](services/inspector.md) — Automated vulnerability scanning for EC2, containers and Lambda.
- [🔑 Key Management Service (`kms`)](services/kms.md) — The vault for your encryption keys — used by nearly every AWS service.
- [🔬 Amazon Macie (`macie`)](services/macie.md) — ML that hunts PII inside S3 — finds the secret nobody remembered storing.
- [🏛️ AWS Organizations (`organizations`)](services/organizations.md) — Multi-account governance — SCPs, consolidated billing, account factories.
- [🗝️ AWS Secrets Manager (`secretsmanager`)](services/secretsmanager.md) — Credentials live here, not in .env files — with automatic rotation.
- [🕵️ AWS Security Hub (`securityhub`)](services/securityhub.md) — One pane of glass: GuardDuty + Inspector + Config findings, scored vs CIS.
- [☂️ AWS Shield (`shield`)](services/shield.md) — DDoS protection — always-on L3/4 defense; Advanced guards L7.
- [🛡️ Web Application Firewall (`waf`)](services/waf.md) — Block SQLi, XSS, bots and brute force before they reach your app.

## Storage (6)

- [🧰 AWS Backup (`backup`)](services/backup.md) — One central policy engine backing up EC2, RDS, DynamoDB, EFS and S3.
- [💾 Elastic Block Store (`ebs`)](services/ebs.md) — Real block storage for EC2 — the hard drive that survives a reboot.
- [🗂️ Elastic File System (`efs`)](services/efs.md) — One shared NFS mount, readable by hundreds of servers at once.
- [🗂️ Amazon FSx (`fsx`)](services/fsx.md) — Fully managed, high-performance file systems — Lustre, NetApp ONTAP, OpenZFS, Windows File Server.
- [🪣 Simple Storage Service (`s3`)](services/s3.md) — The infinite object store where every byte of your data lake begins.
- [🚪 AWS Storage Gateway (`storagegateway`)](services/storagegateway.md) — Bridge your on-premises storage to AWS — cache, backup and archive without re-architecting.
