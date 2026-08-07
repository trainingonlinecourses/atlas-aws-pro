# 🏞️ AWS Lake Formation (`lakeformation`)

> Fine-grained permissions over the lake — column-level security, no IAM acrobatics.

- **Category:** Analytics
- **Service id:** `lakeformation`
- **AI-enabled:** yes

## Why it exists
Bucket policies can't say 'analysts see revenue but not salaries'. Lake Formation grants table/column/cell access on the Glue Catalog.

## When to use it
Lake permissions, column-level masking, cross-account sharing, curated zones.

## Learn first

- LF-tags & data location registration
- Grant/revoke on catalog objects
- Column filters
- Cross-account sharing

## Terraform
```hcl
resource "aws_lakeformation_permissions" "analyst_read" {
  principal = aws_iam_role.analyst.arn
  permissions = ["SELECT", "DESCRIBE"]
  database { name = aws_glue_catalog_database.raw.name }
}
# Column-level: table_with_columns with excluded_column_names = ["ssn", "salary"]
```

## AWS CDK
```ts
import * as lakeformation from "aws-cdk-lib/aws-lakeformation";
new lakeformation.CfnDataLakeSettings(this, "Admins", {
  admins: [{ dataLakePrincipalIdentifier: platformRole.roleArn }],
});
```

## Boto3 (Python)
```python
import boto3
lf = boto3.client("lakeformation", region_name="us-east-1")
for g in lf.list_permissions()["PrincipalResourcePermissions"]:
    print(g["Principal"], g["Permissions"])
```

## Delete / teardown
```python
lf.batch_revoke_permissions(...)  # then deregister locations
```

## Expert tips

- Register S3 locations BEFORE granting on them.
- LF-tags scale better than per-principal grants.

## Real-world example

**Regulated data teams** — Analysts query revenue freely while PII columns stay masked automatically.

## Next steps

- **Glue** (Catalog objects are what you grant on.) — see `glue`
- **Athena / Redshift / EMR** (Engines enforce LF permissions.) — see `athena---redshift---emr`
- **RAM** (Shares the lake across accounts.) — see `ram`
