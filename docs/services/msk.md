# 🎛️ Managed Streaming for Apache Kafka (`msk`)

> Managed Apache Kafka — the event backbone for serious streaming platforms.

- **Category:** Analytics
- **Service id:** `msk`
- **AI-enabled:** yes

## Why it exists
When your streaming contract is Kafka — existing ecosystem, Kafka Connect, exactly-once — MSK runs the brokers.

## When to use it
Event backbone between microservices, CDC pipelines, lake feeds.

## Learn first

- Topics / partitions / consumer groups
- Provisioned vs Serverless
- IAM auth

## Terraform
```hcl
resource "aws_msk_cluster" "events" {
  cluster_name = "events"
  kafka_version = "3.7.x"
  number_of_broker_nodes = 3
  broker_node_group_info {
    instance_type = "kafka.m7g.large"
    client_subnets = [aws_subnet.priv_a.id, aws_subnet.priv_b.id]
    storage_info { ebs_storage_info { volume_size = 100 } }
  }
  encryption_info { encryption_in_transit { client_broker = "TLS" } }
}
```

## AWS CDK
```ts
import * as msk from "aws-cdk-lib/aws-msk";
new msk.CfnCluster(this, "Events", {
  clusterName: "events", kafkaVersion: "3.7.x", numberOfBrokerNodes: 3,
  brokerNodeGroupInfo: {
    instanceType: "kafka.m7g.large",
    clientSubnets: [privA.subnetId, privB.subnetId],
    storageInfo: { ebsStorageInfo: { volumeSize: 100 } },
  },
});
```

## Boto3 (Python)
```python
import boto3
msk = boto3.client("kafka", region_name="us-east-1")
for c in msk.list_clusters_v2()["ClusterInfoList"]:
    print(c["ClusterName"], c["State"])
```

## Delete / teardown
```python
msk.delete_cluster(ClusterArn=arn)
```

## Expert tips

- 3 brokers minimum; spread across 3 AZs.
- Consumer group lag is THE health metric to alarm on.

## Real-world example

**Streaming platforms** — Order events flow through Kafka topics to dozens of consumers.

## Operating across environments

The industry-standard way this service is run at each stage of the lifecycle — from a throwaway dev box to a hardened, multi-region production system.

### 🛠️ Development

In dev, Managed Streaming for Apache Kafka runs on a slice of data — small tables, small clusters, same shapes.

- Use sample data with the same column types so queries behave like prod.
- Keep a dev-only catalog/database so experiments never touch real tables.
- Turn on cost controls from the start; ad-hoc querying is where bills balloon.

### 🧪 Staging / Pre-prod

Staging validates pipelines and query cost on realistic volumes before they hit prod.

- Run the ETL/ingestion job on staging volume and check row counts + schema drift.
- Measure bytes-scanned per query and tune partitioning/compression here.
- Test workgroup data limits so a runaway query can't surprise finance.

### 🚀 Production

In production Managed Streaming for Apache Kafka is governed: partitioned, compressed, and cost-controlled.

- Store data as partitioned Parquet/ORC so scan cost stays low.
- Enforce workgroup/budget limits and alert the owning team on bytes-scanned spikes.
- Monitor pipeline state and freshness; stale data is a silent prod failure.

### 🌍 Multi-region / DR

DR for Managed Streaming for Apache Kafka is a catalog and pipeline that can re-run against a replicated data copy.

- Replicate the raw data to a DR region and keep the catalog definitions in code.
- Define an RPO for ingested data; re-run the pipeline to catch up after failover.
- Drill 're-apply the pipeline in the backup region' annually.

### ♻️ Lifecycle & IaC

Lifecycle is data-lake discipline: schema registry, job bookmarks, and a teardown for experiments.

- Use a catalog with schema evolution so renamed columns don't break ETL.
- Enable job bookmarks for incremental loads; reprocess only what changed.
- Delete or archive stale experiment tables on a schedule to control cost.

## Next steps

- **ECS / EC2** (Producers publish to topics.) — see `ecs---ec2`
- **Lambda** (Consumes from topics natively.) — see `lambda`
- **S3** (Kafka Connect sinks the stream.) — see `s3`
