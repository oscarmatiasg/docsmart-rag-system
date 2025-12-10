"""
S3 Upload Script for DocSmart RAG System
AWS AI Engineer Nanodegree - Final Project

This script uploads documents from the spec-sheets folder to an S3 bucket,
maintaining the folder structure. It handles various document types including
PDF, DOCX, TXT, and other formats supported by Bedrock Knowledge Base.

Usage:
    python scripts/upload_to_s3.py

Configuration:
    Update the BUCKET_NAME variable with your S3 bucket name from Stack 1 output.
    Optionally, modify PREFIX to upload to a specific folder in S3.
"""

import os
import boto3
import sys
from pathlib import Path
from botocore.exceptions import ClientError, NoCredentialsError
import mimetypes

# ============================================================================
# Configuration
# ============================================================================

# S3 bucket name - UPDATE THIS with your bucket name from Stack 1
BUCKET_NAME = "docsmart-documents-967663481769"

# S3 prefix (folder path in S3) - leave empty for root, or use "spec-sheets/"
PREFIX = ""

# Local directory containing documents to upload
LOCAL_DIR = "spec-sheets"

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.pdf', '.docx', '.doc', '.txt', '.md', 
    '.html', '.csv', '.json', '.xml'
}

# AWS Region
AWS_REGION = "us-east-1"

# ============================================================================
# Initialize AWS Clients
# ============================================================================

def initialize_s3_client():
    """Initialize S3 client with error handling."""
    try:
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        # Test connection
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"✓ Connected to S3 bucket: {BUCKET_NAME}")
        return s3_client
    except NoCredentialsError:
        print("✗ ERROR: AWS credentials not found.")
        print("Please configure your AWS credentials using:")
        print("  - AWS CLI: aws configure")
        print("  - Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
        print("  - Or run quick_credentials.py to update credentials")
        sys.exit(1)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"✗ ERROR: Bucket '{BUCKET_NAME}' not found.")
            print("Please create the bucket using Stack 1 Terraform or update BUCKET_NAME.")
        elif error_code == '403':
            print(f"✗ ERROR: Access denied to bucket '{BUCKET_NAME}'.")
            print("Please check your AWS credentials and IAM permissions.")
        else:
            print(f"✗ ERROR: {e}")
        sys.exit(1)

# ============================================================================
# File Upload Functions
# ============================================================================

def get_mime_type(file_path):
    """Get MIME type for a file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type or 'application/octet-stream'

def is_supported_file(file_path):
    """Check if file extension is supported."""
    return Path(file_path).suffix.lower() in SUPPORTED_EXTENSIONS

def get_files_to_upload(directory):
    """
    Get list of all supported files in the directory.
    
    Args:
        directory: Path to local directory
        
    Returns:
        List of file paths relative to the directory
    """
    files = []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"✗ ERROR: Directory '{directory}' not found.")
        print(f"Please create the directory and add your documents:")
        print(f"  mkdir {directory}")
        return []
    
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = Path(root) / filename
            if is_supported_file(file_path):
                # Get path relative to the base directory
                relative_path = file_path.relative_to(directory_path)
                files.append((str(file_path), str(relative_path)))
            else:
                print(f"⚠ Skipping unsupported file: {filename}")
    
    return files

def upload_file_to_s3(s3_client, local_path, s3_key):
    """
    Upload a file to S3.
    
    Args:
        s3_client: boto3 S3 client
        local_path: Local file path
        s3_key: S3 object key
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get file size for progress display
        file_size = os.path.getsize(local_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # Get MIME type
        mime_type = get_mime_type(local_path)
        
        # Upload with metadata
        extra_args = {
            'ContentType': mime_type,
            'Metadata': {
                'uploaded-by': 'docsmart-upload-script',
                'original-filename': Path(local_path).name
            }
        }
        
        print(f"  Uploading {Path(local_path).name} ({file_size_mb:.2f} MB)...", end=' ')
        
        s3_client.upload_file(
            Filename=local_path,
            Bucket=BUCKET_NAME,
            Key=s3_key,
            ExtraArgs=extra_args
        )
        
        print("✓")
        return True
        
    except ClientError as e:
        print(f"✗")
        print(f"    ERROR: {e}")
        return False
    except Exception as e:
        print(f"✗")
        print(f"    ERROR: {e}")
        return False

def upload_directory(s3_client, local_dir, prefix=""):
    """
    Upload all supported files from a directory to S3.
    
    Args:
        s3_client: boto3 S3 client
        local_dir: Local directory path
        prefix: S3 key prefix (folder path)
    """
    print(f"\n{'='*70}")
    print(f"Starting upload from '{local_dir}' to s3://{BUCKET_NAME}/{prefix}")
    print(f"{'='*70}\n")
    
    # Get all files to upload
    files = get_files_to_upload(local_dir)
    
    if not files:
        print("✗ No supported files found to upload.")
        print(f"\nSupported extensions: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        return
    
    print(f"Found {len(files)} file(s) to upload.\n")
    
    # Upload each file
    success_count = 0
    fail_count = 0
    
    for local_path, relative_path in files:
        # Construct S3 key maintaining folder structure
        if prefix:
            s3_key = f"{prefix.rstrip('/')}/{relative_path}"
        else:
            s3_key = relative_path
        
        # Replace backslashes with forward slashes for S3
        s3_key = s3_key.replace('\\', '/')
        
        if upload_file_to_s3(s3_client, local_path, s3_key):
            success_count += 1
        else:
            fail_count += 1
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"Upload Summary:")
    print(f"  ✓ Successful: {success_count}")
    if fail_count > 0:
        print(f"  ✗ Failed: {fail_count}")
    print(f"  Total files: {len(files)}")
    print(f"{'='*70}\n")

# ============================================================================
# Verification Functions
# ============================================================================

def verify_uploads(s3_client, prefix=""):
    """
    Verify uploaded files in S3 bucket.
    
    Args:
        s3_client: boto3 S3 client
        prefix: S3 key prefix to list
    """
    print("Verifying uploads in S3...")
    
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix
        )
        
        if 'Contents' not in response:
            print("  No objects found in bucket.")
            return
        
        objects = response['Contents']
        print(f"\n  Found {len(objects)} object(s) in S3:\n")
        
        total_size = 0
        for obj in objects:
            size_mb = obj['Size'] / (1024 * 1024)
            total_size += obj['Size']
            print(f"    • {obj['Key']} ({size_mb:.2f} MB)")
        
        total_size_mb = total_size / (1024 * 1024)
        print(f"\n  Total size: {total_size_mb:.2f} MB\n")
        
    except ClientError as e:
        print(f"  ✗ ERROR verifying uploads: {e}")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("DocSmart S3 Upload Script")
    print("AWS AI Engineer Nanodegree - Final Project")
    print("="*70 + "\n")
    
    # Display configuration
    print("Configuration:")
    print(f"  Bucket: {BUCKET_NAME}")
    print(f"  Region: {AWS_REGION}")
    print(f"  Prefix: {PREFIX if PREFIX else '(root)'}")
    print(f"  Local directory: {LOCAL_DIR}")
    print(f"  Supported extensions: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
    print()
    
    # Initialize S3 client
    s3_client = initialize_s3_client()
    
    # Upload files
    upload_directory(s3_client, LOCAL_DIR, PREFIX)
    
    # Verify uploads
    verify_uploads(s3_client, PREFIX)
    
    # Print next steps
    print("Next Steps:")
    print("  1. Verify files in AWS Console: S3 > Buckets > " + BUCKET_NAME)
    print("  2. Sync Knowledge Base data source using Terraform output command")
    print("  3. Or use AWS CLI:")
    print(f"     aws bedrock-agent start-ingestion-job \\")
    print(f"       --knowledge-base-id <YOUR_KB_ID> \\")
    print(f"       --data-source-id <YOUR_DATA_SOURCE_ID> \\")
    print(f"       --region {AWS_REGION}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Upload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)
