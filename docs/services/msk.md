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

## Next steps

- **ECS / EC2** (Producers publish to topics.) — see `ecs---ec2`
- **Lambda** (Consumes from topics natively.) — see `lambda`
- **S3** (Kafka Connect sinks the stream.) — see `s3`
