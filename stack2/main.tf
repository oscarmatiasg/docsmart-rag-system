# Stack 2: Bedrock Knowledge Base Configuration
# AWS AI Engineer Nanodegree - Final Project
# DocSmart RAG System - Knowledge Base with Aurora PostgreSQL + pgvector

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "DocSmart-RAG-System"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Course      = "AWS-AI-Engineer-Nanodegree"
      Stack       = "Stack2-KnowledgeBase"
    }
  }
}

# ============================================================================
# Data Sources from Stack 1
# ============================================================================

data "aws_s3_bucket" "documents" {
  bucket = var.s3_bucket_name
}

data "aws_iam_role" "bedrock_kb_role" {
  name = var.bedrock_kb_role_name
}

# ============================================================================
# Bedrock Knowledge Base
# ============================================================================

resource "aws_bedrockagent_knowledge_base" "docsmart" {
  name        = "${var.project_name}-knowledge-base"
  description = "DocSmart Knowledge Base for HR policy documents using Aurora PostgreSQL with pgvector"
  role_arn    = data.aws_iam_role.bedrock_kb_role.arn

  knowledge_base_configuration {
    type = "VECTOR"
    
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock:${var.aws_region}::foundation-model/${var.embedding_model_id}"
    }
  }

  storage_configuration {
    type = "RDS"
    
    rds_configuration {
      credentials_secret_arn = aws_secretsmanager_secret.aurora_credentials.arn
      database_name          = var.database_name
      resource_arn           = var.aurora_cluster_arn
      table_name             = "bedrock_integration.bedrock_kb"
      
      field_mapping {
        metadata_field     = "metadata"
        primary_key_field  = "id"
        text_field         = "chunks"
        vector_field       = "embedding"
      }
    }
  }

  tags = {
    Name = "${var.project_name}-knowledge-base"
  }
}

# ============================================================================
# Secrets Manager for Aurora Credentials
# ============================================================================

resource "aws_secretsmanager_secret" "aurora_credentials" {
  name        = "${var.project_name}-aurora-credentials-${random_id.secret_suffix.hex}"
  description = "Aurora PostgreSQL credentials for Bedrock Knowledge Base"

  tags = {
    Name = "${var.project_name}-aurora-credentials"
  }
}

resource "random_id" "secret_suffix" {
  byte_length = 4
}

resource "aws_secretsmanager_secret_version" "aurora_credentials" {
  secret_id = aws_secretsmanager_secret.aurora_credentials.id
  secret_string = jsonencode({
    username = var.database_master_username
    password = var.database_master_password
  })
}

# IAM Policy for Secrets Manager Access
resource "aws_iam_role_policy" "bedrock_secrets_policy" {
  name = "${var.project_name}-bedrock-secrets-policy"
  role = data.aws_iam_role.bedrock_kb_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = aws_secretsmanager_secret.aurora_credentials.arn
      }
    ]
  })
}

# IAM Policy for RDS Data API Access
resource "aws_iam_role_policy" "bedrock_rds_data_policy" {
  name = "${var.project_name}-bedrock-rds-data-policy"
  role = data.aws_iam_role.bedrock_kb_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "rds:DescribeDBClusters",
          "rds:DescribeDBInstances",
          "rds-data:ExecuteStatement",
          "rds-data:BatchExecuteStatement",
          "rds-data:BeginTransaction",
          "rds-data:CommitTransaction",
          "rds-data:RollbackTransaction"
        ]
        Resource = var.aurora_cluster_arn
      }
    ]
  })
}

# ============================================================================
# Bedrock Data Source (S3)
# ============================================================================

resource "aws_bedrockagent_data_source" "s3_documents" {
  name              = "${var.project_name}-s3-data-source"
  description       = "S3 data source for DocSmart HR policy documents"
  knowledge_base_id = aws_bedrockagent_knowledge_base.docsmart.id

  data_source_configuration {
    type = "S3"
    
    s3_configuration {
      bucket_arn = data.aws_s3_bucket.documents.arn
    }
  }

  vector_ingestion_configuration {
    chunking_configuration {
      chunking_strategy = var.chunking_strategy
      
      dynamic "fixed_size_chunking_configuration" {
        for_each = var.chunking_strategy == "FIXED_SIZE" ? [1] : []
        content {
          max_tokens         = var.chunk_max_tokens
          overlap_percentage = var.chunk_overlap_percentage
        }
      }
    }
  }
}

# ============================================================================
# CloudWatch Log Group for Knowledge Base
# ============================================================================

resource "aws_cloudwatch_log_group" "knowledge_base" {
  name              = "/aws/bedrock/${var.project_name}-kb"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-kb-logs"
  }
}
