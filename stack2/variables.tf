# Variables for Stack 2 - Bedrock Knowledge Base
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
# Stack 1 Outputs (Import these values)
# ============================================================================

variable "s3_bucket_name" {
  description = "Name of the S3 bucket from Stack 1"
  type        = string
}

variable "aurora_cluster_arn" {
  description = "ARN of the Aurora cluster from Stack 1"
  type        = string
}

variable "database_name" {
  description = "Name of the PostgreSQL database from Stack 1"
  type        = string
}

variable "database_master_username" {
  description = "Master username for Aurora PostgreSQL from Stack 1"
  type        = string
  sensitive   = true
}

variable "database_master_password" {
  description = "Master password for Aurora PostgreSQL from Stack 1"
  type        = string
  sensitive   = true
}

variable "bedrock_kb_role_name" {
  description = "Name of the IAM role for Bedrock KB from Stack 1"
  type        = string
}

# ============================================================================
# Bedrock Configuration
# ============================================================================

variable "embedding_model_id" {
  description = "Bedrock embedding model ID"
  type        = string
  default     = "amazon.titan-embed-text-v2:0"
  
  validation {
    condition = contains([
      "amazon.titan-embed-text-v1",
      "amazon.titan-embed-text-v2:0",
      "cohere.embed-english-v3",
      "cohere.embed-multilingual-v3"
    ], var.embedding_model_id)
    error_message = "Must be a valid Bedrock embedding model ID."
  }
}

variable "llm_model_id" {
  description = "Bedrock LLM model ID for generation"
  type        = string
  default     = "anthropic.claude-3-5-sonnet-20240620-v1:0"
}

# ============================================================================
# Data Source Configuration
# ============================================================================

variable "s3_inclusion_prefixes" {
  description = "List of S3 prefixes to include in data source"
  type        = list(string)
  default     = []
}

variable "chunking_strategy" {
  description = "Chunking strategy for documents (FIXED_SIZE, NONE, HIERARCHICAL, SEMANTIC)"
  type        = string
  default     = "FIXED_SIZE"
  
  validation {
    condition = contains([
      "FIXED_SIZE",
      "NONE",
      "HIERARCHICAL",
      "SEMANTIC"
    ], var.chunking_strategy)
    error_message = "Must be a valid chunking strategy."
  }
}

variable "chunk_max_tokens" {
  description = "Maximum tokens per chunk (for FIXED_SIZE strategy)"
  type        = number
  default     = 300
  
  validation {
    condition     = var.chunk_max_tokens >= 100 && var.chunk_max_tokens <= 8192
    error_message = "Chunk max tokens must be between 100 and 8192."
  }
}

variable "chunk_overlap_percentage" {
  description = "Overlap percentage between chunks (0-99)"
  type        = number
  default     = 20
  
  validation {
    condition     = var.chunk_overlap_percentage >= 0 && var.chunk_overlap_percentage < 100
    error_message = "Chunk overlap percentage must be between 0 and 99."
  }
}

# ============================================================================
# Retrieval Configuration
# ============================================================================

variable "max_results" {
  description = "Maximum number of results to return from knowledge base"
  type        = number
  default     = 5
  
  validation {
    condition     = var.max_results >= 1 && var.max_results <= 100
    error_message = "Max results must be between 1 and 100."
  }
}

variable "score_threshold" {
  description = "Minimum similarity score threshold (0.0-1.0)"
  type        = number
  default     = 0.1
  
  validation {
    condition     = var.score_threshold >= 0.0 && var.score_threshold <= 1.0
    error_message = "Score threshold must be between 0.0 and 1.0."
  }
}
