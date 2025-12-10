# Variables for Stack 1 - Base Infrastructure
# DocSmart RAG System - AWS AI Engineer Nanodegree Final Project

variable "aws_region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "docsmart"
}

# ============================================================================
# VPC Configuration
# ============================================================================

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_count" {
  description = "Number of public subnets"
  type        = number
  default     = 2
}

variable "private_subnet_count" {
  description = "Number of private subnets for Aurora"
  type        = number
  default     = 2
}

# ============================================================================
# Aurora Serverless Configuration
# ============================================================================

variable "aurora_engine_version" {
  description = "Aurora PostgreSQL engine version with pgvector support"
  type        = string
  default     = "15.14"
}

variable "database_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "docsmart_kb"
}

variable "database_master_username" {
  description = "Master username for Aurora PostgreSQL"
  type        = string
  default     = "dbadmin"
  sensitive   = true
}

variable "database_master_password" {
  description = "Master password for Aurora PostgreSQL (minimum 8 characters)"
  type        = string
  sensitive   = true
  
  validation {
    condition     = length(var.database_master_password) >= 8
    error_message = "Database password must be at least 8 characters long."
  }
}

variable "aurora_min_capacity" {
  description = "Minimum capacity for Aurora Serverless v2 (ACU)"
  type        = number
  default     = 0.5
}

variable "aurora_max_capacity" {
  description = "Maximum capacity for Aurora Serverless v2 (ACU)"
  type        = number
  default     = 2
}

# ============================================================================
# S3 Configuration
# ============================================================================

variable "s3_bucket_name" {
  description = "Name for S3 bucket to store documents (must be globally unique)"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.s3_bucket_name))
    error_message = "S3 bucket name must contain only lowercase letters, numbers, and hyphens."
  }
}
