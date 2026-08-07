# Real-World Industry Scenarios & Issues

Production incidents, the failure mode behind each, the industry-standard fix, and the alert that would have caught it first. Per-service teaching reference — each entry doubles as an interview answer.

**30 scenarios** across compute, storage, database, networking, security, messaging, data, and ML.

## Scenarios by service

### Application Load Balancer (`alb`)

- **Category:** Compute
- **Scenario:** Rollout to a new version of the service passed health checks at startup but immediately started returning 500s. Users hit the bad version for 25 minutes because the target group kept the box 'healthy'.
- **The industry issue:** Health checks too shallow (only TCP/HTTP 200 on a liveness path), no slow-start, no canary weight shifting.
- **Impact:** Broken traffic served to real users during every deploys, silent until complaints.
- **The standard fix:** Use deep health checks (a ready path that exercises the DB), set slow-start for warmup, deploy via weighted target groups or CodeDeploy blue/green, and alert on target-deregistration spikes.
- **Alerts:** UnHealthyHostCount > 0, TargetResponseTime p99 > SLO, 5XX error rate > 1%
- **Tags:** load-balancing, deployment, resilience

### API Gateway (`apigateway`)

- **Category:** Compute
- **Scenario:** A mobile client started hammering an endpoint with retries after a timeout bug. The gateway had no throttling configured, so the flood cascaded into the backend Lambda pool and out through the downstream ERP.
- **The industry issue:** No API-level throttling or quota, no client-rate limiting, and no circuit breaker — one buggy client takes down the backend.
- **Impact:** Cross-tenant outage, downstream vendor blacklist, reputational damage.
- **The standard fix:** Configure account/API-level throttling, per-key quotas for tenants, burst limits, caching for hot GETs, and WAF rules with rate-based ban on abusive IPs.
- **Alerts:** 4XX > 5%, 5XX > 0 with retries, Throttled request count, WAF blocked request spikes
- **Tags:** api, rate-limiting, resilience

### Athena (`athena`)

- **Category:** data
- **Scenario:** A BI team's monthly query suddenly cost $1,400 instead of $40. The data team had appended a raw CSV 'temp' partition that was never compressed or partitioned, so Athena scanned the whole thing every time.
- **The industry issue:** Query cost scales with bytes scanned; unpartitioned/plain-CSV tables, no compression, no cost guardrails.
- **Impact:** Bill shock on every ad-hoc query, data teams afraid to query.
- **The standard fix:** Partition by date/region, store Parquet/ORC with compression, use columnar projections + workgroup data-usage limits, and set cost controls at the workgroup level.
- **Alerts:** Workgroup data-scanned > budget, Query failed > threshold, BytesScanned per query anomaly
- **Tags:** analytics, cost, serverless

### Auto Scaling (`autoscaling`)

- **Category:** Compute
- **Scenario:** A morning batch job scaled the fleet from 10 to 400 instances in an hour and racked up a $40k bill before anyone noticed. The group had 'desired = max' and no scale-down protection.
- **The industry issue:** Misconfigured min/max (desired = max), no scale-down cooldown, no budget alarm — asymmetric scaling blows cost.
- **Impact:** Runaway spend, cloud bill shock, finance intervention.
- **The standard fix:** Set realistic min/max, use target-tracking + predictive scaling, add instance protection, enforce budget alerts and anomaly detection, and use Spot with capacity-optimized allocation for batch.
- **Alerts:** DesiredCapacity jump > 5× in 10 min, Projected EC2 cost > budget, InstancesInService drift from desired
- **Tags:** scaling, cost, autoscaling

### Bedrock (`bedrock`)

- **Category:** Machine Learning & AI
- **Scenario:** A support chatbot started quoting outdated product prices after the catalog updated. Users were told wrong prices for two days; the RAG knowledge base had no refresh schedule and no provenance on sources.
- **The industry issue:** Stale knowledge bases, no content freshness checks, no guardrails on generated output, no eval harness.
- **Impact:** Wrong answers at scale, brand damage, no way to prove what the model said or why.
- **The standard fix:** Schedule KB syncs, add guardrails + topic bans, log every query with trace + source citations, and run an eval harness (golden set) before every KB update.
- **Alerts:** KB sync failure, Guardrail intervention rate spike, Hallucination/refusal eval score drop
- **Tags:** genai, rag, governance

### CloudFront (`cloudfront`)

- **Category:** Networking & Delivery
- **Scenario:** A marketing email drove 100× normal traffic. The site's S3 origin had no rate limiting, CloudFront had no origin shield, and the origin bucketed into 503s while the CDN served stale cache with 200s.
- **The industry issue:** Origin unprotected from cache-miss storms; no origin shield, weak cache-control headers, no WAF.
- **Impact:** Origin meltdown, stale content served as 'fresh', confused caching bugs.
- **The standard fix:** Enable Origin Shield, set correct Cache-Control/immutable for assets, use a WAF + rate-based rule in front, and configure origin failover to a secondary origin.
- **Alerts:** Origin error rate (5XX) > 1%, Cache miss ratio jump, WAF blocked request spike
- **Tags:** cdn, caching, resilience

### CloudWatch (`cloudwatch`)

- **Category:** management
- **Scenario:** The on-call page fired at 3am for a p99 latency spike. The team spent 90 minutes digging through three accounts before realizing the metric was coming from a stale test environment nobody decommissioned.
- **The industry issue:** No metric/log tagging strategy, no structured logging, and alerts without routing — noise drowns the real signal.
- **Impact:** Missed real incidents, alert fatigue, slow MTTD/MTTR, burned-out on-call.
- **The standard fix:** Tag everything (env, team, app), use structured JSON logs, consolidate metrics into one dashboard per service with well-defined SLO burn alerts, and route pages by severity.
- **Alerts:** SLO burn-rate > 14.4×/10× windows, Any CloudWatch Alarm in ALARM > 30 min, Log error-rate anomaly
- **Tags:** observability, alerting, sre

### Cognito (`cognito`)

- **Category:** Security, Identity & Compliance
- **Scenario:** A growth campaign spiked signups 50×. The user pool's default limits throttled the sign-in API, new users got 'too many requests', and the login page looked broken to every new customer for hours.
- **The industry issue:** Default (unscalable) user-pool limits, no adaptive auth, no MFA policy, no rate-limit planning for spikes.
- **Impact:** Lost signups at the exact moment of peak acquisition, support flood.
- **The standard fix:** Pre-warm the pool before campaigns, raise account limits proactively, enable adaptive authentication, add WAF rate rules on the sign-in path, and monitor sign-in failures vs successes.
- **Alerts:** Sign-up/sign-in throttling errors, Failed auth attempts > baseline, Cognito internal errors
- **Tags:** identity, auth, scaling

### Connect (`connect`)

- **Category:** Application Integration
- **Scenario:** A bank's IVR hit its concurrent-calls limit during a system outage when call volume tripled. Callers got a busy signal instead of a queue, so the 'fail-safe' contact center failed exactly when it was needed.
- **The industry issue:** Default concurrency limits never raised, no overflow to voicemail/secondary routing, no call-volume alerting.
- **Impact:** Customers abandoned, SLA breaches, reputational hit during incidents.
- **The standard fix:** Pre-provision capacity for peak, route overflow to a secondary queue/voicemail, use Contact Lens to catch 'can't reach support' sentiment spikes, and alert on concurrent calls near the limit.
- **Alerts:** Concurrent calls > 80% of limit, Abandon rate > 10%, Average queue wait > target
- **Tags:** contact-center, capacity, ivr

### Detective (`detective`)

- **Category:** Security, Identity & Compliance
- **Scenario:** GuardDuty flagged a compromised role. The SOC team spent 6 hours chasing CloudTrail exports across three accounts before finally finding the API call that triggered the takeover — the blast radius was never visible.
- **The industry issue:** Findings without investigation tooling: no graph of related entities, no timeline, evidence scattered across raw logs.
- **Impact:** Slow MTTR, attacker time-to-exfiltrate, incomplete forensics.
- **The standard fix:** Enable Detective before incidents (it ingests ~2 weeks of history), link it to GuardDuty + Security Hub, and walk findings through the entity graph to trace source → impact in minutes.
- **Alerts:** New high-severity GuardDuty finding, Detective graph data source issues, Investigation started/finished
- **Tags:** security, forensics, mttr

### DynamoDB (`dynamodb`)

- **Category:** Database
- **Scenario:** A promotional campaign caused a hot partition: one popular item absorbed all reads, hit the partition's 3000 RCU ceiling, and throttled the whole table during peak checkout.
- **The industry issue:** A single partition key with low cardinality plus on-demand mode that can't react fast enough — the classic hot-key problem.
- **Impact:** Throttled writes, failed checkouts, spiky error rates at exactly the moment of highest demand.
- **The standard fix:** Use high-cardinality keys or shard hot keys with a suffix, add read/write capacity autoscaling with aggressive scale-up, enable DAX for read-heavy bursts, and add exponential backoff + retry with jitter in code.
- **Alerts:** ThrottledRequests > 0, ReadThrottleEvents/WriteThrottleEvents, DAX CPU > 70%
- **Tags:** database, scaling, serverless

### EC2 (`ec2`)

- **Category:** Compute
- **Scenario:** During a Black-Friday sale, a single 3-Tier app is built on one large c5.4xlarge. Traffic triples, the box pegs at 100% CPU, and every user request times out for 40 minutes.
- **The industry issue:** Vertical scaling on one box has a hard ceiling and a single point of failure. Teams discover the limit mid-incident instead of ahead of it.
- **Impact:** Full outage, lost revenue, burned engineering hours during peak.
- **The standard fix:** Run instances behind an ALB in an Auto Scaling Group with a mixed-instances policy, min/max bounds, and a target-tracking policy on CPU or request count. Use Scheduled Scaling for predictable peaks.
- **Alerts:** CPUUtilization > 85% for 5 min, StatusCheckFailed_Instance > 0, Scheduled-scaling misses forecast
- **Tags:** compute, scaling, high-availability

### ECS (`ecs`)

- **Category:** Compute
- **Scenario:** A container kept crash-looping after an image update, but the task count never changed because ECS kept restarting the same task definition with a bad env var from a stale parameter.
- **The industry issue:** Config drift between secrets/env and task definitions; no rollout strategy, no rollback guard, restart storms masked as 'transient'.
- **Impact:** Flapping services, delayed feature delivery, mystery failures that survive restarts.
- **The standard fix:** Use ECS Service Connect/Service Discovery, secrets from Secrets Manager mounted at deploy, and rolling or blue/green deployments with a minimum healthy percent; add deployment circuit breaker for repeated failures.
- **Alerts:** Stopped task reason spikes, Deployment failed (circuit breaker), Service CPU > 80% sustained
- **Tags:** containers, deployment, config

### EKS (`eks`)

- **Category:** Compute
- **Scenario:** A node auto-replacement drained 30% of pods at once during a version upgrade, and the new nodes couldn't pull images because the cluster had no image cache and OCI rate limits kicked in.
- **The industry issue:** Node pool upgrades without PDBs and max-unavailable control; no image caching; cluster autoscaler reacting too late.
- **Impact:** Partial downtime during every upgrade, slow pod scheduling, cascading restarts.
- **The standard fix:** Define PodDisruptionBudgets on every workload, upgrade node groups one AZ at a time with surge, use Bottlerocket AMIs + ECR image cache (or pre-pulled snapshots), and right-size the cluster autoscaler.
- **Alerts:** Unschedulable pods > 0, Node NotReady duration, Image pull errors, PDB disruption budget violated
- **Tags:** kubernetes, containers, upgrades

### EventBridge (`eventbridge`)

- **Category:** application
- **Scenario:** An 'order.created' event was being consumed by two teams. One team's subscriber threw an unhandled exception and silently stopped processing for a week — no one noticed because EventBridge drops failed invocations by default.
- **The industry issue:** No retry policy or DLQ on targets, unmonitored invocations, schema evolution breaking consumers.
- **Impact:** Silent data loss, divergent systems, uncoordinated consumers.
- **The standard fix:** Set target retry policy + DLQ, monitor InvocationFailureCount per rule, use schemas to version events, and test consumers against the schema registry before deploy.
- **Alerts:** Rule InvocationFailureCount > 0, DLQ depth > 0, Schema registry incompatible change
- **Tags:** events, decoupling, reliability

### Glue (`glue`)

- **Category:** data
- **Scenario:** A nightly ETL job that worked for months suddenly failed every run after a source schema changed (a column was renamed). The job used position-based extraction and had no schema drift handling.
- **The industry issue:** Brittle ETL with hard-coded schemas, no schema registry, no job bookmark checks, silent reprocessing.
- **Impact:** Blocked daily pipelines, data quality issues, late reports.
- **The standard fix:** Use Glue Data Catalog with schema evolution, enable job bookmarks for incremental loads, add `enableSchemaEvolution`/resilience to schema changes, and alert on job state and DPU usage.
- **Alerts:** Job FAILED/STOPPED, DataQuality run fail, DPU-hours > budget
- **Tags:** etl, data, schema

### IAM (`iam`)

- **Category:** Security, Identity & Compliance
- **Scenario:** A leaked access key from a developer laptop was used to spin up hundreds of bitcoin miners in 20 minutes. The key had full admin because the team 'didn't have time' for fine-grained roles.
- **The industry issue:** Long-lived static keys with over-privileged policies; no access analyzer, no permission boundary, no rotation.
- **Impact:** Six-figure surprise bill, breach disclosure, keys still valid while revoked one-by-one.
- **The standard fix:** Prefer IAM roles + instance profiles over static keys, enforce least privilege with Access Analyzer, add permission boundaries, rotate keys automatically, and enable CloudTrail + GuardDuty to detect anomalous usage.
- **Alerts:** Root account sign-in, CloudTrail unauthorized-action spikes, GuardDuty CryptoCurrency/EC2 finding
- **Tags:** security, identity, compliance

### IoT Core (`iot`)

- **Category:** Application Integration
- **Scenario:** A firmware rollout pushed bad configuration to 40,000 devices. Every device tried to reconnect at once, the MQTT broker flooded, and the fleet went offline for hours while support calls poured in.
- **The industry issue:** No fleet-level deployment strategy: unauthenticated reconnects, no shadow throttling, certificates shared across devices.
- **Impact:** Fleet-wide outage, stale telemetry, costly field support.
- **The standard fix:** Use per-device certificates, OTA via IoT Jobs (not raw shadows), device shadows with rate limits, and a reconnect backoff policy. Monitor connection count and messages per device.
- **Alerts:** Connection attempt spikes, Disconnect rate > baseline, Device shadow update failures
- **Tags:** iot, fleet, ota

### Kinesis Data Streams (`kinesis`)

- **Category:** data
- **Scenario:** A shard hot partition (one device id = 90% of events) throttled writes during a firmware rollout, dropping telemetry. The team had set shard count once at launch and never resharded.
- **The industry issue:** Static shard count, hot keys, and no lag monitoring — the stream silently loses the exact data you need.
- **Impact:** Lost telemetry, skewed analytics, blind spots during incidents.
- **The standard fix:** Right-size shard count for peak with headroom, use adaptive shard splitting, monitor GetRecords.IteratorAgeMilliseconds per shard, and fall back to S3 for the long tail.
- **Alerts:** IteratorAgeMilliseconds > 60 s, WriteProvisionedThroughputExceeded, Per-shard throttling
- **Tags:** streaming, data, scaling

### Lambda (`lambda`)

- **Category:** Compute
- **Scenario:** A payment callback function started timing out under load. Cold starts spiked to 9 seconds after a busy holiday rollout and the API gateway returned 504s to the upstream card network.
- **The industry issue:** Cold starts from large layers/runtimes and no reserved concurrency; downstream calls without timeout budgets pile up and saturate the account's concurrency limit.
- **Impact:** Slow callbacks, lost webhook deliveries, downstream retries amplifying load.
- **The standard fix:** Provisioned concurrency for latency-critical paths, separate Lambda per concern (don't bundle heavy deps), set explicit timeouts/retries, and reserve concurrency to protect core flows from noisy neighbors.
- **Alerts:** Duration p99 > 80% of timeout, Throttles > 0, IteratorAge > 1 min (stream sources)
- **Tags:** compute, serverless, latency

### RDS (`rds`)

- **Category:** Database
- **Scenario:** A nightly ETL job grew and started running 40 minutes past its window, locking a critical table. The app team 'fixed' it by raising instance size — but the root cause was a missing index and a runaway query.
- **The industry issue:** Scaling the box instead of the query. No performance insights, no statement timeouts, and maintenance windows that collide with business hours.
- **Impact:** Slow page loads, blocked writes, escalating RDS spend for zero real gain.
- **The standard fix:** Turn on Performance Insights, add `max_execution_time`/`statement_timeout`, review slow-query logs weekly, use read replicas for reporting, and right-size before the CPU knee, not after.
- **Alerts:** CPU > 80% sustained, FreeableMemory < 5%, Deadlocks > threshold, Storage > 90%
- **Tags:** database, performance, scaling

### Redshift (`redshift`)

- **Category:** data
- **Scenario:** Dashboards slowed to a crawl during month-end reporting. The warehouse was on a single node class with no WLM, so one analyst's ad-hoc query starved the entire BI team.
- **The industry issue:** No workload management, sort/compression keys guessed once, no concurrency scaling, no vacuum/analyze.
- **Impact:** Slow dashboards, analyst frustration, warehouse consolidation projects triggered.
- **The standard fix:** Enable concurrency scaling, define WLM queues for BI vs ETL, design sort keys on common filters and distribution on join columns, and schedule VACUUM/ANALYZE on a maintenance window.
- **Alerts:** WLM queue wait > threshold, Concurrency scaling events, Skew ratio > 4
- **Tags:** data-warehouse, performance, analytics

### Route 53 (`route53`)

- **Category:** Networking & Delivery
- **Scenario:** A DNS change to flip a failover was made at 4pm; by 6pm the support inbox was full of 'site unreachable' reports. The TTL on the old record was 86400 (24h), so users cached the dead endpoint.
- **The industry issue:** Long TTLs on records that should be quick to flip; no health-check routing; changes made without a rollback plan.
- **Impact:** Slow failover, users stuck on dead endpoints, extended outage window.
- **The standard fix:** Use low TTL (60-300s) on records you may flip, Route 53 health checks + failover/failover routing policies, and test DNS propagation in a staging domain first.
- **Alerts:** Health check status DOWN, DNSSEC key rollover failure, Query volume anomaly
- **Tags:** dns, failover, availability

### S3 (`s3`)

- **Category:** Storage
- **Scenario:** A data engineer accidentally ran `aws s3 rm --recursive` on a bucket that was the only copy of the company's customer exports. The data was gone in minutes and backups didn't exist.
- **The industry issue:** Buckets treated as backup targets; no versioning, no lifecycle rule, and MFA-delete not enabled — the classic 'single bucket of truth' failure.
- **Impact:** Irrecoverable data loss, audit/compliance exposure, legal liability.
- **The standard fix:** Enable Bucket Versioning + MFA Delete, cross-region replication to a backup bucket, Object Lock (WORM) for immutable archives, and lifecycle policies that promote to Glacier. Never delete without IAM deny + preflight checks.
- **Alerts:** DeleteObject from prod IAM role, Bucket size drop > 20% in 1 h, Lifecycle transition errors
- **Tags:** storage, data-loss, backup

### SageMaker (`sagemaker`)

- **Category:** Machine Learning & AI
- **Scenario:** A model retrained nightly drifted silently — churn predictions looked fine in the dashboard but the business saw response rates drop for two weeks before anyone noticed the data drift.
- **The industry issue:** Training and serving drift detection missing; no lineage, no version pinning, no rollback to a known-good model.
- **Impact:** Silent model degradation, wrong business decisions, no audit trail.
- **The standard fix:** Use SageMaker Model Monitor for data/drift alerts, store model lineage in Model Registry with approval gates, shadow-deploy canaries, and automate rollback on guardrail failure.
- **Alerts:** DataQuality baseline drift, Model quality metric drop, Inference latency p99 > SLO
- **Tags:** ml, maturity, governance

### Secrets Manager (`secretsmanager`)

- **Category:** Security, Identity & Compliance
- **Scenario:** A DB password rotated automatically, but a batch job still used a 6-month-old cached copy. The job failed silently for a day until an alert surfaced 500 errors — secrets rotated without downstream consumers knowing.
- **The industry issue:** Rotated secrets cached in apps, no rotation-to-consumer sync, secrets committed to git history, no access audit.
- **Impact:** Silent auth failures, hard-to-diagnose outages, leaked credentials in repos.
- **The standard fix:** Store secrets only in Secrets Manager, rotate on schedule with Lambda, have apps fetch at startup + on 401 (not cache forever), scan git history for leaked keys, and enable CloudTrail for secret access.
- **Alerts:** Secret rotation failure, AccessDenied on secret fetch, Secret fetched from new principal (unusual)
- **Tags:** security, secrets, rotation

### SNS (`sns`)

- **Category:** application
- **Scenario:** A CI pipeline published 'deploy complete' to a topic that had grown to 12 subscribers, two of which were HTTP endpoints that started failing silently. Nobody noticed notifications were dead for a week.
- **The industry issue:** HTTP/S subscribers without retry policies or delivery logging; fan-out growing without governance.
- **Impact:** Silent notification loss, missed deploys, undetected downstream failures.
- **The standard fix:** Set delivery retry policies, log delivery failures to CloudWatch, use DLQ for SNS->SQS, and keep a subscriber manifest so additions are reviewed.
- **Alerts:** NumberOfNotificationsDelivered drop, Delivery failure count > 0, SQS DLQ for topic > 0
- **Tags:** messaging, fanout, notifications

### SQS (`sqs`)

- **Category:** application
- **Scenario:** A producer wrote a retry loop with no backoff that redelivered the same message thousands of times. With no dead-letter queue, poisoned messages were retried forever and the consumer fell behind.
- **The industry issue:** No DLQ, no maxReceiveCount, redrive policy missing, and consumers without idempotency.
- **Impact:** Unbounded retry storms, message pile-up, downstream duplicate effects.
- **The standard fix:** Configure a DLQ with maxReceiveCount (3-5), exponential backoff + jitter on the consumer, idempotency keys in messages, and monitor ApproximateAgeOfOldestMessage.
- **Alerts:** ApproximateAgeOfOldestMessage > 5 min, DLQ depth > 0, ReceiveCount near maxReceiveCount
- **Tags:** messaging, resilience, queueing

### Step Functions (`stepfunctions`)

- **Category:** application
- **Scenario:** An order orchestration workflow hit a transient DB error at step 7 of 12, and the whole execution failed. The retried run double-charged the customer because the payment step wasn't idempotent.
- **The industry issue:** Workflows without retry/catch policies on steps, no idempotency, no execution history retention policy, no SLA monitoring.
- **Impact:** Duplicate charges, stuck orders, hard-to-audit failures.
- **The standard fix:** Attach retry with jittered backoff per state, catch and route failures to a compensation step, enforce idempotency keys, and monitor execution failures + run time per state.
- **Alerts:** ExecutionFailed rate > 0, State retries > N, Execution duration p99 > SLA
- **Tags:** workflow, orchestration, reliability

### VPC (`vpc`)

- **Category:** Networking & Delivery
- **Scenario:** A subnet ran out of IPs at 2am during a deploy. New EC2 instances failed to start with 'Insufficient IP addresses', and the team had no idea because nothing monitored subnet capacity.
- **The industry issue:** Sparse /24 subnets sized 'because we always did it that way', no IPAM, and no capacity alerting until instances fail to launch.
- **Impact:** Deploys blocked, autoscaling stalls, emergency redesign of CIDR layout under pressure.
- **The standard fix:** Plan CIDR blocks for 2-3x future growth, use VPC IPAM, monitor `EC2-InsufficientIP` CloudWatch metrics, and reserve space per AZ with headroom for ASG buffers.
- **Alerts:** Subnet free IPs < 10%, EC2-InsufficientIP-Address, VPC flow-log reject rate > 5%
- **Tags:** networking, capacity, planning

## Per-pillar failure modes

The recurring, industry-standard pitfalls every team should design against.

### compute — Reliability

- **Single-instance everything** — One box, one AZ, no ASG. The #1 cause of preventable outages in SMBs.
- **Scaling the box, not the query/code** — Vertical upgrade masks root cause and doubles the bill.
- **No rollback path** — Bad deploy = manual revert under pressure. Automate blue/green or weighted routing.

### database — Performance

- **Missing indexes discovered in prod** — Slow queries hit exactly when traffic grows. Use Performance Insights from day one.
- **Hot partitions/keys** — Low-cardinality keys cause throttling at peak. Design keys for distribution, not convenience.
- **Backups that were never restored** — A backup that has never been tested is not a backup. Restore-drill quarterly.

### storage — Data Protection

- **No versioning / no WORM** — Accidental deletes are irreversible. Enable versioning + MFA delete + Object Lock.
- **Single copy of truth** — One bucket, one region, no replication. Add CRR and test the failover.

### networking — Connectivity

- **Subnet IP exhaustion** — Subnets sized for launch-day, never grown. Use IPAM and monitor free IPs.
- **DNS TTLs too long** — Failover can't happen if clients cache 24h. Keep flip-able records at 60-300s.

### security — Security

- **Static keys with admin** — Leaked key = full account compromise. Prefer roles, rotate, add permission boundaries.
- **Secrets in git** — Committed secrets survive repo deletion. Scan history, rotate immediately.
- **No MFA on root** — Root is the crown jewels. Hardware MFA + CloudTrail on root usage.

### management — Operational Excellence

- **Alerts without routing** — Noise is the real incident. Tag resources, route by severity, page only for actionable.
- **No SLOs** — You can't manage what you don't measure. Define burn-rate alerts per critical path.

### data — Analytics

- **Cost scales with scans** — Plain CSV tables blow Athena/Redshift bills. Partition + Parquet + workgroup limits.
- **Schema drift breaks ETL** — Position-based jobs break silently. Use catalogs, bookmarks, and drift tests.

### ml — ML/AI Governance

- **Silent drift** — Models decay without alerts. Monitor data/model quality continuously.
- **No eval before release** — Ship the prompt, skip the golden set, regret it in prod. Eval-first or don't deploy.
