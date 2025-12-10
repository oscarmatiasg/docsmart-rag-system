# Outputs for Stack 1 - Base Infrastructure
# These outputs will be used in Stack 2 for Bedrock Knowledge Base configuration

# ============================================================================
# VPC Outputs
# ============================================================================

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

# ============================================================================
# Aurora Outputs
# ============================================================================

output "aurora_cluster_endpoint" {
  description = "Aurora cluster endpoint for write operations"
  value       = aws_rds_cluster.aurora.endpoint
}

output "aurora_reader_endpoint" {
  description = "Aurora cluster reader endpoint for read operations"
  value       = aws_rds_cluster.aurora.reader_endpoint
}

output "aurora_cluster_identifier" {
  description = "Aurora cluster identifier"
  value       = aws_rds_cluster.aurora.cluster_identifier
}

output "aurora_cluster_arn" {
  description = "Aurora cluster ARN"
  value       = aws_rds_cluster.aurora.arn
}

output "database_name" {
  description = "Name of the PostgreSQL database"
  value       = aws_rds_cluster.aurora.database_name
}

output "database_port" {
  description = "Database port"
  value       = aws_rds_cluster.aurora.port
}

output "aurora_security_group_id" {
  description = "Security group ID for Aurora cluster"
  value       = aws_security_group.aurora.id
}

# ============================================================================
# S3 Outputs
# ============================================================================

output "s3_bucket_name" {
  description = "Name of the S3 bucket for documents"
  value       = aws_s3_bucket.documents.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.documents.arn
}

output "s3_bucket_regional_domain_name" {
  description = "Regional domain name of the S3 bucket"
  value       = aws_s3_bucket.documents.bucket_regional_domain_name
}

# ============================================================================
# IAM Outputs
# ============================================================================

output "bedrock_kb_role_arn" {
  description = "ARN of the IAM role for Bedrock Knowledge Base"
  value       = aws_iam_role.bedrock_kb_role.arn
}

output "bedrock_kb_role_name" {
  description = "Name of the IAM role for Bedrock Knowledge Base"
  value       = aws_iam_role.bedrock_kb_role.name
}

# ============================================================================
# Connection String (Sensitive)
# ============================================================================

output "database_connection_string" {
  description = "Database connection string (sensitive)"
  value       = "postgresql://${var.database_master_username}:${var.database_master_password}@${aws_rds_cluster.aurora.endpoint}:${aws_rds_cluster.aurora.port}/${aws_rds_cluster.aurora.database_name}"
  sensitive   = true
}

# ============================================================================
# Summary Output
# ============================================================================

output "stack1_summary" {
  description = "Summary of Stack 1 resources"
  value = {
    vpc_id                    = aws_vpc.main.id
    aurora_endpoint           = aws_rds_cluster.aurora.endpoint
    s3_bucket                 = aws_s3_bucket.documents.id
    bedrock_role_arn          = aws_iam_role.bedrock_kb_role.arn
    region                    = var.aws_region
  }
}
