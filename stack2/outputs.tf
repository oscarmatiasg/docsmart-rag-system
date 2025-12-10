# Outputs for Stack 2 - Bedrock Knowledge Base
# These outputs provide configuration details for the application

# ============================================================================
# Knowledge Base Outputs
# ============================================================================

output "knowledge_base_id" {
  description = "ID of the Bedrock Knowledge Base"
  value       = aws_bedrockagent_knowledge_base.docsmart.id
}

output "knowledge_base_arn" {
  description = "ARN of the Bedrock Knowledge Base"
  value       = aws_bedrockagent_knowledge_base.docsmart.arn
}

output "knowledge_base_name" {
  description = "Name of the Bedrock Knowledge Base"
  value       = aws_bedrockagent_knowledge_base.docsmart.name
}

# ============================================================================
# Data Source Outputs
# ============================================================================

output "data_source_id" {
  description = "ID of the S3 data source"
  value       = aws_bedrockagent_data_source.s3_documents.id
}

# Note: aws_bedrockagent_data_source does not expose an ARN attribute
# output "data_source_arn" {
#   description = "ARN of the S3 data source"
#   value       = aws_bedrockagent_data_source.s3_documents.arn
# }

# ============================================================================
# Secrets Manager Outputs
# ============================================================================

output "aurora_credentials_secret_arn" {
  description = "ARN of the Secrets Manager secret for Aurora credentials"
  value       = aws_secretsmanager_secret.aurora_credentials.arn
}

output "aurora_credentials_secret_name" {
  description = "Name of the Secrets Manager secret"
  value       = aws_secretsmanager_secret.aurora_credentials.name
}

# ============================================================================
# Configuration Outputs
# ============================================================================

output "embedding_model_id" {
  description = "Embedding model ID used by Knowledge Base"
  value       = var.embedding_model_id
}

output "llm_model_id" {
  description = "LLM model ID for text generation"
  value       = var.llm_model_id
}

output "chunking_configuration" {
  description = "Chunking configuration details"
  value = {
    strategy           = var.chunking_strategy
    max_tokens         = var.chunk_max_tokens
    overlap_percentage = var.chunk_overlap_percentage
  }
}

output "retrieval_configuration" {
  description = "Retrieval configuration details"
  value = {
    max_results      = var.max_results
    score_threshold  = var.score_threshold
  }
}

# ============================================================================
# CloudWatch Outputs
# ============================================================================

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group name for Knowledge Base"
  value       = aws_cloudwatch_log_group.knowledge_base.name
}

output "cloudwatch_log_group_arn" {
  description = "CloudWatch log group ARN"
  value       = aws_cloudwatch_log_group.knowledge_base.arn
}

# ============================================================================
# Summary Output
# ============================================================================

output "stack2_summary" {
  description = "Summary of Stack 2 resources"
  value = {
    knowledge_base_id    = aws_bedrockagent_knowledge_base.docsmart.id
    data_source_id       = aws_bedrockagent_data_source.s3_documents.id
    embedding_model      = var.embedding_model_id
    llm_model            = var.llm_model_id
    s3_bucket            = var.s3_bucket_name
    region               = var.aws_region
  }
}

# ============================================================================
# Integration Instructions
# ============================================================================

output "integration_details" {
  description = "Details for integrating with the application"
  value = {
    knowledge_base_id = aws_bedrockagent_knowledge_base.docsmart.id
    region            = var.aws_region
    embedding_model   = var.embedding_model_id
    llm_model         = var.llm_model_id
    max_results       = var.max_results
    score_threshold   = var.score_threshold
  }
}

# ============================================================================
# Sync Command
# ============================================================================

output "sync_data_source_command" {
  description = "AWS CLI command to sync the data source"
  value = "aws bedrock-agent start-ingestion-job --knowledge-base-id ${aws_bedrockagent_knowledge_base.docsmart.id} --data-source-id ${aws_bedrockagent_data_source.s3_documents.id} --region ${var.aws_region}"
}
