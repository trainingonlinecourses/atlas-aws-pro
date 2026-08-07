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

## Next steps

- **S3** (EMRFS reads/writes the lake directly.) — see `s3`
- **Glue Catalog** (Spark SQL uses the same schemas.) — see `glue-catalog`
- **Step Functions** (Orchestrates cluster lifecycles.) — see `step-functions`
