# 🚀 DocSmart RAG System - Deployment Guide

**AWS AI Engineer Nanodegree - Final Project**

Complete step-by-step guide to deploy the DocSmart RAG system from scratch.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture-overview)
3. [Deployment Steps](#deployment-steps)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools

- **AWS CLI** v2.x or higher ([Install](https://aws.amazon.com/cli/))
- **Terraform** v1.0 or higher ([Install](https://www.terraform.io/downloads))
- **Python** 3.9+ ([Install](https://www.python.org/downloads/))
- **Git** ([Install](https://git-scm.com/downloads))

### AWS Account Requirements

- Active AWS Account with admin access
- AWS Bedrock access enabled in `us-east-1`
- Models enabled in Bedrock:
  - `amazon.titan-embed-text-v2:0`
  - `anthropic.claude-3-5-sonnet-20240620-v1:0`

### AWS Credentials

Configure AWS credentials using one of these methods:

```bash
# Method 1: AWS CLI configuration
aws configure

# Method 2: Environment variables
export AWS_ACCESS_KEY_ID="YOUR_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
export AWS_SESSION_TOKEN="YOUR_TOKEN"  # If using temporary credentials
export AWS_REGION="us-east-1"
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       AWS Cloud                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │   S3 Bucket  │─────▶│   Bedrock    │─────▶│  Aurora   │ │
│  │  (Documents) │      │ Knowledge Base│      │PostgreSQL │ │
│  └──────────────┘      └──────────────┘      │ + pgvector│ │
│                                               └───────────┘ │
│                              │                               │
│                              ▼                               │
│                       ┌─────────────┐                        │
│                       │   Claude    │                        │
│                       │ 3.5 Sonnet  │                        │
│                       └─────────────┘                        │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               VPC (10.0.0.0/16)                      │   │
│  │  ┌──────────────────┐    ┌──────────────────┐       │   │
│  │  │ Public Subnets   │    │ Private Subnets  │       │   │
│  │  │  (2 AZs)         │    │  (Aurora + 2 AZs)│       │   │
│  │  └──────────────────┘    └──────────────────┘       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- **Stack 1**: VPC, Aurora Serverless v2, S3, IAM Roles
- **Stack 2**: Bedrock Knowledge Base, Data Source, Secrets Manager

---

## Deployment Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/docsmart-rag-system.git
cd docsmart-rag-system
```

### Step 2: Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Deploy Stack 1 (Infrastructure)

```bash
cd stack1

# Copy example configuration
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values
# IMPORTANT: Change passwords and bucket name!
nano terraform.tfvars  # or use your preferred editor

# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Deploy infrastructure
terraform apply

# Save outputs (you'll need these for Stack 2)
terraform output > ../stack1_outputs.txt
```

**Expected Duration**: ~10 minutes

**Key Outputs** (save these):
- `aurora_cluster_arn`
- `aurora_cluster_endpoint`
- `s3_bucket_name`
- `bedrock_kb_role_arn`

### Step 4: Initialize Aurora Database

After Stack 1 completes, initialize the pgvector schema:

```bash
# Get Aurora connection details
CLUSTER_ARN=$(terraform output -raw aurora_cluster_arn)
SECRET_ARN="arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:docsmart-aurora-credentials-XXXXXX"
DB_NAME=$(terraform output -raw database_name)

# Navigate to scripts
cd ../scripts

# Create pgvector extension
aws rds-data execute-statement \
  --resource-arn "$CLUSTER_ARN" \
  --database "$DB_NAME" \
  --secret-arn "$SECRET_ARN" \
  --sql "CREATE EXTENSION IF NOT EXISTS vector;"

# Create schema
aws rds-data execute-statement \
  --resource-arn "$CLUSTER_ARN" \
  --database "$DB_NAME" \
  --secret-arn "$SECRET_ARN" \
  --sql "CREATE SCHEMA IF NOT EXISTS bedrock_integration;"

# Create table
aws rds-data execute-statement \
  --resource-arn "$CLUSTER_ARN" \
  --database "$DB_NAME" \
  --secret-arn "$SECRET_ARN" \
  --sql "CREATE TABLE IF NOT EXISTS bedrock_integration.bedrock_kb (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), chunks TEXT NOT NULL, embedding VECTOR(1024), metadata JSONB, created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);"

# Create vector index (HNSW)
aws rds-data execute-statement \
  --resource-arn "$CLUSTER_ARN" \
  --database "$DB_NAME" \
  --secret-arn "$SECRET_ARN" \
  --sql "CREATE INDEX bedrock_kb_embedding_idx ON bedrock_integration.bedrock_kb USING hnsw (embedding vector_cosine_ops);"

# Create full-text search index
aws rds-data execute-statement \
  --resource-arn "$CLUSTER_ARN" \
  --database "$DB_NAME" \
  --secret-arn "$SECRET_ARN" \
  --sql "CREATE INDEX bedrock_kb_chunks_fts_idx ON bedrock_integration.bedrock_kb USING gin (to_tsvector('english', chunks));"
```

**Alternative**: Use the provided script:
```bash
# If you have psql and bastion host access:
psql -h YOUR_AURORA_ENDPOINT -U dbadmin -d docsmart_kb -f aurora_init.sql
```

### Step 5: Deploy Stack 2 (Knowledge Base)

```bash
cd ../stack2

# Copy example configuration
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with Stack 1 outputs
nano terraform.tfvars

# Initialize Terraform
terraform init

# Deploy Knowledge Base
terraform apply

# Save Knowledge Base ID
terraform output knowledge_base_id
```

**Expected Duration**: ~3 minutes

### Step 6: Upload Sample Documents

```bash
cd ../scripts

# Upload documents to S3
python upload_to_s3.py

# Or manually via AWS CLI
aws s3 cp ../sample_docs/ s3://YOUR-BUCKET-NAME/ --recursive
```

### Step 7: Sync Knowledge Base

```bash
# Get IDs from Stack 2
cd ../stack2
KB_ID=$(terraform output -raw knowledge_base_id)
DS_ID=$(terraform output -raw data_source_id)

# Start ingestion job
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id $KB_ID \
  --data-source-id $DS_ID \
  --region us-east-1

# Monitor progress
aws bedrock-agent list-ingestion-jobs \
  --knowledge-base-id $KB_ID \
  --data-source-id $DS_ID \
  --region us-east-1
```

**Expected Duration**: 5-15 minutes depending on document count

---

## Post-Deployment Configuration

### Configure Python Application

```bash
cd ..

# Copy environment template
cp .env.example .env

# Edit with your values
nano .env
```

Required `.env` values:
```env
AWS_REGION=us-east-1
KNOWLEDGE_BASE_ID=YYIBMDUAYW
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
```

### Run Streamlit Application

```bash
streamlit run app_demo.py
```

Access at: `http://localhost:8501`

---

## Testing & Verification

### 1. Verify Aurora Database

```bash
# Check table exists
aws rds-data execute-statement \
  --resource-arn "$CLUSTER_ARN" \
  --database "$DB_NAME" \
  --secret-arn "$SECRET_ARN" \
  --sql "SELECT COUNT(*) FROM bedrock_integration.bedrock_kb;" \
  --region us-east-1
```

### 2. Test Knowledge Base Query

```python
from bedrock_utils import query_knowledge_base

result = query_knowledge_base("¿Cuántos días de vacaciones tengo?")
print(f"Found {result['count']} documents")
for doc in result['results']:
    print(f"- Score: {doc['score']:.3f}")
    print(f"  Text: {doc['text'][:100]}...")
```

### 3. Test Full RAG Pipeline

```python
from bedrock_utils import query_knowledge_base, generate_response

query = "¿Cuántos días de vacaciones tengo si llevo 2 años?"
docs = query_knowledge_base(query)
response = generate_response(query, docs['results'])
print(response['response'])
```

---

## Troubleshooting

### Issue: "Aurora engine version 15.5 not available"

**Solution**: Use version 15.6-15.14
```hcl
aurora_engine_version = "15.14"
```

### Issue: "rds:DescribeDBClusters permission denied"

**Solution**: The RDS policy was added in Stack 1. Re-apply:
```bash
cd stack1
terraform apply
```

### Issue: "DataAPIv2 is not enabled"

**Solution**: Enable in Aurora cluster:
```hcl
enable_http_endpoint = true
```

### Issue: "relation bedrock_integration.bedrock_kb does not exist"

**Solution**: Run Step 4 (Initialize Aurora Database)

### Issue: "embedding column must be indexed"

**Solution**: Create HNSW index:
```sql
CREATE INDEX bedrock_kb_embedding_idx 
ON bedrock_integration.bedrock_kb 
USING hnsw (embedding vector_cosine_ops);
```

### Issue: Terraform state conflicts

**Solution**: Remove conflicting resources from state:
```bash
terraform state rm aws_iam_role_policy.bedrock_rds_policy
```

---

## Cost Estimate

**Monthly costs** (us-east-1, low usage):
- Aurora Serverless v2: ~$43/month (0.5 ACU baseline)
- S3 Standard Storage: ~$0.50/month (20 GB)
- Bedrock Knowledge Base: $0 (no base fee)
- Bedrock API calls: ~$10/month (1000 queries)
- **Total**: ~$53-55/month

**Tips to reduce costs:**
- Use Aurora's pause/resume feature during dev
- Delete resources when not in use: `terraform destroy`
- Monitor with AWS Cost Explorer

---

## Cleanup

To delete all resources:

```bash
# Stack 2 first (dependencies)
cd stack2
terraform destroy

# Then Stack 1
cd ../stack1
terraform destroy
```

⚠️ **Warning**: This will permanently delete all data!

---

## Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/docsmart-rag-system/issues)
- **AWS Bedrock Docs**: https://docs.aws.amazon.com/bedrock/
- **Terraform AWS Provider**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs

---

**Last Updated**: December 2025  
**Version**: 1.0
