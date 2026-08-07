"""
AWS Atlas Pro - Environment Operating Models.

For every service, the industry-standard way it runs across environments:
Development -> Staging/Pre-prod -> Production -> Multi-region/DR -> Lifecycle & IaC.

Content is deterministic and category-aware (compute vs database vs security ...):
the operating model for a DB is not the operating model for a CDN. {name} / {full}
are interpolated with each service's own name so every page reads as bespoke.

Served as `env_model` on /api/v1/services (list + detail) and rendered in the
service modal + docs.
"""

# Each category: 5 environment blocks. {name} = short name, {full} = full name.
_MODELS = {
    "compute": {
        "dev": {
            "desc": "In development, run {name} at the smallest valid size. Provision with IaC so the box you test on is the same shape as the one that ships.",
            "points": [
                "Use spot or the cheapest instance class for throwaway workloads; never the production size.",
                "Keep a dev AMI/image that's rebuilt from the same recipe as staging, so drift stays zero.",
                "Secrets in dev come from a dev-only store — never copy prod credentials down.",
            ],
        },
        "stage": {
            "desc": "Staging is where {full} gets load-tested and the deploy path is proven. It must mirror prod's topology, not its size.",
            "points": [
                "Run the same instance types and subnets as prod so performance surprises surface here.",
                "Run a load test that reaches prod's projected peak before every release.",
                "Test the scaling policy (CPU or request target) against synthetic traffic, not vibes.",
            ],
        },
        "prod": {
            "desc": "In production {full} runs hardened and elastic: at least two AZs, an autoscaling policy with sane min/max, and immutable images.",
            "points": [
                "Put instances behind a load balancer inside an Auto Scaling Group with a target-tracking policy.",
                "Enable detailed monitoring, schedule a weekly security scan of the image, and never SSH in to hand-fix.",
                "Apply least-privilege instance roles; store config in SSM/Secrets Manager, not in the image.",
            ],
        },
        "dr": {
            "desc": "For disaster recovery, the industry standard is 're-apply IaC, re-sync data' in a secondary region within a tested RTO.",
            "points": [
                "Replicate images/AMIs to the DR region on a schedule, or rebuild them from the pipeline.",
                "Decide RTO/RPO upfront (e.g. 1h/15min) and drill the failover quarterly.",
                "Keep a runbook: promote the DR stack, flip DNS or Global Accelerator, verify, then backfill.",
            ],
        },
        "life": {
            "desc": "Lifecycle is code-first: the {name} stack lives in git, deploys through CI, and tears down cleanly.",
            "points": [
                "One Terraform module or CDK stack per environment; promote the same artifact, don't drift.",
                "Protect prod with a manual approval + `terraform plan` diff posted to the PR.",
                "Tag every resource (env, team, cost-center) and alert the owning team on spend.",
            ],
        },
    },
    "storage": {
        "dev": {
            "desc": "In dev, {full} holds throwaway data. Versioning and lifecycle are on from day one so bad deletes stay reversible.",
            "points": [
                "Enable versioning and object-lock from the first bucket — retrofitting is painful.",
                "Use a dev-only prefix/account; never let dev code write to a prod path.",
                "Set a short lifecycle rule to expire dev objects automatically and keep the bill near zero.",
            ],
        },
        "stage": {
            "desc": "Staging proves the data pipeline end-to-end with realistic volumes and the same policies as prod.",
            "points": [
                "Mirror prod's bucket names, permissions, and lifecycle — test the policy, not a happy path.",
                "Run the migration/replication job against staging data before production cutover.",
                "Verify restore from a versioned snapshot here, where failure costs nothing.",
            ],
        },
        "prod": {
            "desc": "In production {full} is the durability backbone: versioning, MFA-delete, replication, and access auditing are non-negotiable.",
            "points": [
                "Enable versioning + MFA Delete and cross-region replication to a second bucket.",
                "Use Object Lock/WORM for anything auditable; block public access at the account level.",
                "Centralize access with bucket policies + IAM and watch Macie/GuardDuty findings on the data.",
            ],
        },
        "dr": {
            "desc": "DR means a second copy in another region with a tested restore path, not a bucket that only exists once.",
            "points": [
                "Cross-region replicate critical prefixes; set an RPO you can actually honor.",
                "Test a full restore from the replica at least quarterly and log the elapsed time.",
                "Automate promotion: if the primary region degrades, the replica bucket takes over with the same DNS.",
            ],
        },
        "life": {
            "desc": "Lifecycle manages the data class, not just the bucket: hot -> warm -> archive on a policy.",
            "points": [
                "Define lifecycle rules (S3 -> Glacier -> Expire) so cost shrinks automatically.",
                "Own the bucket in Terraform with a remote-state lock so two pipelines can't clobber it.",
                "Add cost-alerting per bucket and a monthly report of the top spenders.",
            ],
        },
    },
    "database": {
        "dev": {
            "desc": "In dev {full} runs minimal — smallest instance, short retention — but with the same schema engine so migrations behave.",
            "points": [
                "Use a tiny instance or a local/containerized equivalent for day-to-day coding.",
                "Run schema migrations through the same tool as prod so `apply` is boring and tested.",
                "Seed with sanitized data, never production PII.",
            ],
        },
        "stage": {
            "desc": "Staging is where {full} gets the schema migration, index, and query-plan validation that prod demands.",
            "points": [
                "Apply the migration, then run the top 10 production queries and compare plans.",
                "Load-test write and read paths; tune parameters before they become a prod page.",
                "Exercise the backup-and-restore procedure against staging data.",
            ],
        },
        "prod": {
            "desc": "In production {full} is HA and observable: multi-AZ, automated backups, statement timeouts, and performance insights on.",
            "points": [
                "Enable multi-AZ, automated backups, and Performance Insights from the start.",
                "Set statement/query timeouts and alarm on CPU, storage, and deadlocks.",
                "Use read replicas for reporting and right-size before the CPU knee, not after.",
            ],
        },
        "dr": {
            "desc": "DR for {full} is a readable copy in another region with a defined RPO/RTO and a tested promotion.",
            "points": [
                "Configure cross-region read replicas or continuous backup to a second region.",
                "Set explicit RPO/RTO and run a quarterly failover drill that ends with DNS flipped back.",
                "Keep the DR instance warm enough to take over fast, or accept the cold-start RTO honestly.",
            ],
        },
        "life": {
            "desc": "Lifecycle keeps {full} disciplined: IaC-managed, versioned, and with a teardown that removes data.",
            "points": [
                "Own the instance and all config in Terraform; use a secrets store for the master password.",
                "Keep migration files in the repo, applied in order by CI, never by hand.",
                "Define a deletion policy — snapshots retained N days, then gone — so teardown is safe.",
            ],
        },
    },
    "networking": {
        "dev": {
            "desc": "In dev, {full} runs in a small VPC with an obvious CIDR and permissive-but-tagged rules.",
            "points": [
                "Use a dedicated dev CIDR (e.g. 10.0.0.0/16) and never overlap the prod block.",
                "Create security groups from IaC so a peer can read exactly what's open.",
                "Tear down unused resources at the end of the week to keep dev costs near zero.",
            ],
        },
        "stage": {
            "desc": "Staging proves the connectivity model: same topology as prod, smaller and cheaper.",
            "points": [
                "Mirror prod's subnets/AZs and route table split to catch topology bugs early.",
                "Test cross-account peering/transit and PrivateLink paths before prod needs them.",
                "Enable flow logs in staging so you learn to read them where it's cheap to experiment.",
            ],
        },
        "prod": {
            "desc": "In production {full} is the security boundary: least-open security groups, VPC flow logs, and IPAM-managed addressing.",
            "points": [
                "Restrict security groups to the minimum (app tier to db tier, and nothing to the internet unless needed).",
                "Turn on VPC Flow Logs and a reject-rate alarm to spot scanning or misconfig.",
                "Plan CIDR with VPC IPAM and monitor subnet free-IP capacity before deploys stall.",
            ],
        },
        "dr": {
            "desc": "DR for {full} is a second region with its own VPC and a DNS failover path, drilled in advance.",
            "points": [
                "Stand up the DR VPC with non-overlapping CIDRs and the same SG structure.",
                "Wire Route 53 failover (or Global Accelerator) with health checks so cutover is a policy change.",
                "Include the network in the DR drill: promote DNS, verify connectivity, then flip back.",
            ],
        },
        "life": {
            "desc": "Lifecycle makes the network reproducible: every route, peering link, and SG is a reviewable artifact.",
            "points": [
                "Define VPC, subnets, SGs, and peering in Terraform with a shared module across accounts.",
                "Put network changes behind review — a wrong SG or route is a security incident.",
                "Document the CIDR map centrally; overlap is the #1 blocker in future migrations.",
            ],
        },
    },
    "security": {
        "dev": {
            "desc": "In dev, {full} is configured but audited: the same controls as prod exist, just scoped to dev accounts.",
            "points": [
                "Create the service with least-privilege and a dev-only boundary, not admin-by-default.",
                "Store any keys/secrets in a secrets manager, never in code or env files.",
                "Enable basic logging so dev behavior is visible and reproducible.",
            ],
        },
        "stage": {
            "desc": "Staging is where {full} is exercised against realistic policies and evidence starts being collected.",
            "points": [
                "Run the same Config/Security Hub rules as prod and fix findings before release.",
                "Test rotation and break-glass access paths here, where mistakes are recoverable.",
                "Scan the artifact (image/code/package) the same way prod will be scanned.",
            ],
        },
        "prod": {
            "desc": "In production {full} is hardened, monitored, and evidence-producing for auditors.",
            "points": [
                "Enforce least privilege with permission boundaries; audit access with Access Analyzer.",
                "Alert on anomalies (GuardDuty/Detective) and on root/privileged usage via CloudTrail.",
                "Automate evidence collection (Audit Manager/Security Hub) so a SOC 2 walkthrough is minutes.",
            ],
        },
        "dr": {
            "desc": "DR for {full} means the control plane answers in the backup region too — logging, KMS, and IAM included.",
            "points": [
                "Replicate KMS keys and logging (CloudTrail/Security Hub) to the DR region.",
                "Test that privileged access, rotation, and alerts all function in the backup region.",
                "Include the security stack in the DR runbook, not just the workloads.",
            ],
        },
        "life": {
            "desc": "Lifecycle keeps {full} continuously compliant: policies as code, rotation automated, findings tracked.",
            "points": [
                "Define policies (IAM/SCP) in Terraform and review them like application code.",
                "Automate secret rotation and never let a static key outlive a quarter.",
                "Close the loop: every security finding becomes a tracked issue with an owner.",
            ],
        },
    },
    "messaging": {
        "dev": {
            "desc": "In dev, {full} is a thin pipe: small queues/topics, short retention, and obvious test producers.",
            "points": [
                "Use a dev-only queue/topic name so dev and prod never cross-deliver.",
                "Seed the message shape from the schema so consumers fail loudly on changes.",
                "Clear the dev queue nightly so stale messages don't linger.",
            ],
        },
        "stage": {
            "desc": "Staging is where {full} is load-tested and failure paths (DLQ, redrive, retry) are proven.",
            "points": [
                "Inject a poison message and confirm it lands on the DLQ with a redrive policy.",
                "Load-test consumer throughput and back-pressure before prod traffic hits.",
                "Verify exactly-once/idempotency behavior against staging consumers.",
            ],
        },
        "prod": {
            "desc": "In production {full} is the reliability backbone: DLQs configured, retries bounded, lag monitored.",
            "points": [
                "Configure a DLQ with a max-receive count so poisoned messages can't loop forever.",
                "Monitor age of oldest message and DLQ depth; page the owning team on lag.",
                "Keep consumers idempotent so retries never double-apply.",
            ],
        },
        "dr": {
            "desc": "DR for {full} is an alternate path in a second region or account, with a defined loss tolerance.",
            "points": [
                "Replicate the queue/topic policy and consumer config to the DR region.",
                "Accept or mitigate the RPO: messages produced during a regional failure are the decision.",
                "Test that consumers can drain the DR path and reconcile afterwards.",
            ],
        },
        "life": {
            "desc": "Lifecycle treats {full} as code: schemas versioned, topics registered, consumers owned.",
            "points": [
                "Manage queues/topics and their policies in Terraform, with the schema in a registry.",
                "Keep a subscriber manifest so every new consumer is reviewed, not silently added.",
                "Alert on delivery failures and prune unused topics to cut noise and cost.",
            ],
        },
    },
    "analytics": {
        "dev": {
            "desc": "In dev, {full} runs on a slice of data — small tables, small clusters, same shapes.",
            "points": [
                "Use sample data with the same column types so queries behave like prod.",
                "Keep a dev-only catalog/database so experiments never touch real tables.",
                "Turn on cost controls from the start; ad-hoc querying is where bills balloon.",
            ],
        },
        "stage": {
            "desc": "Staging validates pipelines and query cost on realistic volumes before they hit prod.",
            "points": [
                "Run the ETL/ingestion job on staging volume and check row counts + schema drift.",
                "Measure bytes-scanned per query and tune partitioning/compression here.",
                "Test workgroup data limits so a runaway query can't surprise finance.",
            ],
        },
        "prod": {
            "desc": "In production {full} is governed: partitioned, compressed, and cost-controlled.",
            "points": [
                "Store data as partitioned Parquet/ORC so scan cost stays low.",
                "Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.",
                "Monitor pipeline state and freshness; stale data is a silent prod failure.",
            ],
        },
        "dr": {
            "desc": "DR for {full} is a catalog and pipeline that can re-run against a replicated data copy.",
            "points": [
                "Replicate the raw data to a DR region and keep the catalog definitions in code.",
                "Define an RPO for ingested data; re-run the pipeline to catch up after failover.",
                "Drill 're-apply the pipeline in the backup region' annually.",
            ],
        },
        "life": {
            "desc": "Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.",
            "points": [
                "Use a catalog with schema evolution so renamed columns don't break ETL.",
                "Enable job bookmarks for incremental loads; reprocess only what changed.",
                "Delete or archive stale experiment tables on a schedule to control cost.",
            ],
        },
    },
    "migration": {
        "dev": {
            "desc": "In dev, {full} is used to prove the migration path on a sample: small data, same tooling.",
            "points": [
                "Set up the replication/migration job in dev against a subset of records.",
                "Validate checksums and row counts on the sample before widening the net.",
                "Keep the dev source isolated so trial runs can't touch real systems.",
            ],
        },
        "stage": {
            "desc": "Staging is the dress rehearsal: a full dry-run migration with a rollback plan.",
            "points": [
                "Run the full migration on staging data and compare record counts end-to-end.",
                "Time it and log throughput; the staging number is your prod forecast.",
                "Write and test the rollback script before you ever need it.",
            ],
        },
        "prod": {
            "desc": "In production {full} executes the cutover: incremental sync, a short frozen window, and verification.",
            "points": [
                "Use continuous sync to near-zero downtime, then a brief cutover window.",
                "Verify with a reconciliation query, not vibes, before traffic is re-routed.",
                "Keep the old system available for rollback until the new one is proven stable.",
            ],
        },
        "dr": {
            "desc": "DR for a migration is the ability to re-run or roll back: source is intact until cutover is complete.",
            "points": [
                "Snapshot the source before cutover so rollback is instant if verification fails.",
                "Store the migration plan and runbook in the repo, not in one engineer's head.",
                "Define the 'abort criteria' — the exact metric that stops the cutover.",
            ],
        },
        "life": {
            "desc": "Lifecycle formalizes the migration as a project: plan, dry-run, execute, decommission.",
            "points": [
                "Track the migration as an IaC-driven project with the source and target in Terraform.",
                "After a stable period, decommission the source and archive its final snapshot.",
                "Post-incident: document what was learned and fold it into the next migration.",
            ],
        },
    },
    "devops": {
        "dev": {
            "desc": "In dev, {full} keeps the loop fast: cheap monitoring, feature flags, and a per-dev environment.",
            "points": [
                "Give each engineer a short-lived environment or namespace, not shared chaos.",
                "Set a low retention on dev logs and metrics so noise doesn't mask signal.",
                "Wire the service into CI so a failing check blocks merge early.",
            ],
        },
        "stage": {
            "desc": "Staging is where {full} is hardened for operations: alerts, dashboards, and runbooks proven.",
            "points": [
                "Create the real dashboards and alarms here, then copy them to prod unchanged.",
                "Test the on-call routing and runbook against a deliberately-induced failure.",
                "Verify the release pipeline promotes through staging with the same approval gates as prod.",
            ],
        },
        "prod": {
            "desc": "In production {full} is the observability and governance backbone of every service.",
            "points": [
                "Standardize on the four golden signals (latency, traffic, errors, saturation) per service.",
                "Route alerts by severity; page only on actionable, and keep runbooks one click away.",
                "Make every change reviewed via IaC PRs, with an audit trail in CloudTrail.",
            ],
        },
        "dr": {
            "desc": "DR for {full} means the observability and governance stack answers from the backup region too.",
            "points": [
                "Replicate dashboards, alarms, and log/metrics destinations to the DR region.",
                "Include the monitoring stack in the failover drill so you can actually see the DR state.",
                "Keep the incident-response runbook in a second location, not only in the primary tool.",
            ],
        },
        "life": {
            "desc": "Lifecycle is continuous: everything the org runs is tagged, measured, and improvable.",
            "points": [
                "Maintain cost-allocation tags (team, env, service) enforced by policy.",
                "Run periodic right-sizing and idle-resource reviews with the owning teams.",
                "Close the loop: every incident produces a runbook update or a new automated check.",
            ],
        },
    },
    "ml": {
        "dev": {
            "desc": "In dev, {full} runs on small data and a notebo0k loop, but with the model and eval tracked from the start.",
            "points": [
                "Use a dev dataset and keep every experiment logged (data, code, metrics).",
                "Track the model in a registry even at prototype stage — lineage is cheap to start, expensive to add.",
                "Write a small eval set (golden questions) before you write the fancy prompt.",
            ],
        },
        "stage": {
            "desc": "Staging validates {full} against the eval harness and a shadow deployment before real traffic.",
            "points": [
                "Run the golden eval set and require it to pass a quality gate in CI.",
                "Shadow-deploy the candidate while the current model serves, and compare outputs.",
                "Check drift baselines (data and model quality) against staging signals.",
            ],
        },
        "prod": {
            "desc": "In production {full} is governed: versioned, guarded, monitored for drift, and rollback-ready.",
            "points": [
                "Serve a pinned, registered model version behind a stable alias for instant rollback.",
                "Enable guardrails, content filters, and PII controls on any generative surface.",
                "Monitor drift + latency + token spend and alert on any regression.",
            ],
        },
        "dr": {
            "desc": "DR for {full} is the ability to re-serve the model in a second region and roll back a bad version.",
            "points": [
                "Replicate the model artifact and endpoints to a DR region; the registry makes this reproducible.",
                "Keep the previous known-good alias deployable in seconds.",
                "Drill a rollback and a region promotion annually — models rot like everything else.",
            ],
        },
        "life": {
            "desc": "Lifecycle is MLOps/AgentOps: registry gates, evals in CI, and a feedback loop back into data.",
            "points": [
                "Gate every model/agent promotion on eval + guardrail checks, never a manual 'looks good'.",
                "Log every inference with trace + source so you can audit what the model said and why.",
                "Close the loop: production feedback becomes new eval cases for the next retrain.",
            ],
        },
    },
    "generic": {
        "dev": {
            "desc": "In development {full} runs small and disposable, provisioned the same way it will be in production.",
            "points": ["Use the smallest valid config and IaC from day one.", "Keep dev data separate and disposable.", "Never use prod credentials in a dev environment."],
        },
        "stage": {
            "desc": "Staging mirrors {full}'s production topology and policy so the release path is proven.",
            "points": ["Match prod's shape, not its size.", "Exercise the deploy and rollback path here.", "Run the alerting and monitoring you plan for prod."],
        },
        "prod": {
            "desc": "In production {full} is resilient, monitored, and security-baselined.",
            "points": ["Enable HA/multi-AZ or a redundant path where it matters.", "Watch the golden signals and route alerts by severity.", "Enforce least privilege and keep an audit trail."],
        },
        "dr": {
            "desc": "DR for {full} is a second-region answer with a defined RPO/RTO, drilled on a schedule.",
            "points": ["Replicate data or config to a backup region.", "Set explicit RPO/RTO and test the failover.", "Automate promotion and make rollback boring."],
        },
        "life": {
            "desc": "Lifecycle is code-first: {full} is reviewed in git, deployed by CI, and torn down safely.",
            "points": ["Own it in Terraform/CDK with a PR review gate.", "Tag for cost and ownership; alert on spend.", "Define a teardown that removes data and snapshots on schedule."],
        },
    },
}

_ENV_KEYS = [
    ("dev", "Development", "🛠️"),
    ("stage", "Staging / Pre-prod", "🧪"),
    ("prod", "Production", "🚀"),
    ("dr", "Multi-region / DR", "🌍"),
    ("life", "Lifecycle & IaC", "♻️"),
]


def for_service(service: dict) -> list:
    """Return the environment operating model for a service: 5 blocks, ordered dev->DR."""
    template = _MODELS.get(service.get("category"), _MODELS["generic"])
    name, full = service.get("name", service.get("id", "")), service.get("full_name", "")
    blocks = []
    for key, label, icon in _ENV_KEYS:
        b = template[key]
        blocks.append({
            "env": label,
            "icon": icon,
            "desc": b["desc"].replace("{name}", name).replace("{full}", full),
            "points": [p.replace("{name}", name).replace("{full}", full) for p in b["points"]],
        })
    return blocks
