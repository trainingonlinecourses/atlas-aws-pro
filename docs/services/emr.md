# 🐘 Elastic MapReduce (`emr`)

> Managed Spark / Hadoop clusters for heavy big-data lifting.

- **Category:** Analytics
- **Service id:** `emr`
- **AI-enabled:** yes

## Why it exists
Some jobs are simply Spark jobs. EMR gives a managed, Spot-friendly cluster that exists for the job and vanishes.

## When to use it
Large transformations, ML feature prep, log crunching.

## Learn first

- Cluster vs step execution
- Node groups
- Spot task fleets
- EMRFS: Spark on S3

## Terraform
```hcl
resource "aws_emr_cluster" "spark" {
  name = "nightly-spark"
  release_label = "emr-7.2.0"
  applications = ["Spark"]
  master_instance_group { instance_type = "m6g.xlarge" }
  core_instance_group { instance_type = "m6g.xlarge"; instance_count = 3 }
  ec2_attributes { subnet_id = aws_subnet.priv_a.id }
}
```

## AWS CDK
```ts
import * as emr from "aws-cdk-lib/aws-emr";
new emr.CfnCluster(this, "Spark", {
  name: "nightly-spark", releaseLabel: "emr-7.2.0",
  applications: [{ name: "Spark" }],
  jobFlowRole: emrInstanceRole.roleName,
  serviceRole: emrServiceRole.roleName,
  instances: {
    masterInstanceGroup: { instanceType: "m6g.xlarge" },
    coreInstanceGroup: { instanceType: "m6g.xlarge", instanceCount: 3 },
  },
});
```

## Boto3 (Python)
```python
import boto3
emr = boto3.client("emr", region_name="us-east-1")
for c in emr.list_clusters()["Clusters"]:
    print(c["Name"], "->", c["Status"]["State"])
```

## Delete / teardown
```python
emr.terminate_job_flows(JobFlowIds=[cluster_id])
```

## Expert tips

- Task nodes on Spot = massive savings for parallel stages.
- Transient clusters (spin up → run → die) beat long-lived ones.

## Real-world example

**Zynga** — Analyzes petabytes of game telemetry on Spot-backed EMR.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Elastic MapReduce runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production Elastic MapReduce is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for Elastic MapReduce is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **S3** (EMRFS reads/writes the lake directly.) — see `s3`
- **Glue Catalog** (Spark SQL uses the same schemas.) — see `glue-catalog`
- **Step Functions** (Orchestrates cluster lifecycles.) — see `step-functions`
