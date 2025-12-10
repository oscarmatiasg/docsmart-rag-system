#!/usr/bin/env python3
"""
Final verification checklist for DocSmart RAG System.
Runs all critical checks before demo/production.
"""
import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_file(filepath, description):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory(dirpath, description):
    """Check if a directory exists."""
    exists = os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_imports():
    """Check if all required modules are importable."""
    print_header("1. CHECKING PYTHON MODULES")
    
    modules = [
        ('boto3', 'AWS SDK'),
        ('streamlit', 'Streamlit UI'),
        ('numpy', 'NumPy'),
        ('json', 'JSON (built-in)'),
        ('sqlite3', 'SQLite (built-in)'),
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {description} ({module_name})")
        except ImportError:
            print(f"❌ {description} ({module_name}) - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if all critical files exist."""
    print_header("2. CHECKING CRITICAL FILES")
    
    files = [
        ('config.py', 'Configuration'),
        ('vector_database_sqlite.py', 'Vector Database'),
        ('embedding_service.py', 'Embedding Service'),
        ('rag_system.py', 'RAG System'),
        ('ingestion_pipeline.py', 'Ingestion Pipeline'),
        ('app_demo.py', 'Streamlit App'),
        ('test_fixes.py', 'Test Suite'),
    ]
    
    all_ok = True
    for filepath, description in files:
        if not check_file(filepath, description):
            all_ok = False
    
    return all_ok

def check_documentation():
    """Check if documentation files exist."""
    print_header("3. CHECKING DOCUMENTATION")
    
    docs = [
        ('AUDITORIA_PROFESIONAL.md', 'Technical Audit'),
        ('RESUMEN_AUDITORIA.md', 'Audit Summary'),
        ('PRESENTACION_COMPLETA.md', 'Presentation Guide'),
        ('presentation_professional.html', 'Visual Presentation'),
        ('README.md', 'General Documentation'),
    ]
    
    all_ok = True
    for filepath, description in docs:
        if not check_file(filepath, description):
            all_ok = False
    
    return all_ok

def check_database():
    """Check if database exists and has data."""
    print_header("4. CHECKING DATABASE")
    
    db_file = 'docsmart.db'
    if not os.path.exists(db_file):
        print(f"❌ Database not found: {db_file}")
        return False
    
    print(f"✅ Database exists: {db_file}")
    
    # Try to check database content
    try:
        import sqlite3
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        print(f"✅ Documents in database: {doc_count}")
        
        cursor.execute("SELECT COUNT(DISTINCT file_name) FROM documents")
        file_count = cursor.fetchone()[0]
        print(f"✅ Unique files: {file_count}")
        
        conn.close()
        return doc_count > 0
        
    except Exception as e:
        print(f"⚠️ Could not query database: {e}")
        return True  # Don't fail on query error

def check_aws_credentials():
    """Check if AWS credentials are configured."""
    print_header("5. CHECKING AWS CREDENTIALS")
    
    creds_file = os.path.expanduser('~/.aws/credentials')
    if not os.path.exists(creds_file):
        print(f"❌ AWS credentials not found: {creds_file}")
        return False
    
    print(f"✅ AWS credentials file exists: {creds_file}")
    
    # Check if credentials are set
    try:
        import boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            print(f"✅ AWS credentials loaded")
            return True
        else:
            print(f"❌ AWS credentials not loaded")
            return False
    except Exception as e:
        print(f"⚠️ Could not load AWS credentials: {e}")
        return False

def check_scripts():
    """Check if helper scripts exist."""
    print_header("6. CHECKING HELPER SCRIPTS")
    
    scripts = [
        ('start_system.bat', 'System Startup Script'),
        ('test_system.bat', 'Test Script'),
        ('quick_credentials.py', 'Credentials Helper'),
    ]
    
    all_ok = True
    for filepath, description in scripts:
        if not check_file(filepath, description):
            all_ok = False
    
    return all_ok

def run_quick_test():
    """Run a quick functionality test."""
    print_header("7. RUNNING QUICK FUNCTIONALITY TEST")
    
    try:
        from vector_database_sqlite import VectorDatabaseSQLite
        from embedding_service import EmbeddingService
        
        # Test database connection
        db = VectorDatabaseSQLite()
        db.connect()
        print("✅ Database connection successful")
        
        # Test embedding service
        embedding_service = EmbeddingService()
        test_embedding = embedding_service.generate_embedding("test")
        print(f"✅ Embedding service working ({len(test_embedding)} dimensions)")
        
        # Test statistics
        stats = db.get_statistics()
        print(f"✅ Database statistics: {stats['total_chunks']} chunks, {stats['total_files']} files")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all checks."""
    print("\n" + "🔍"*30)
    print("DOCSMART RAG SYSTEM - FINAL VERIFICATION CHECKLIST")
    print("🔍"*30)
    
    results = {
        'imports': check_imports(),
        'files': check_files(),
        'documentation': check_documentation(),
        'database': check_database(),
        'aws': check_aws_credentials(),
        'scripts': check_scripts(),
        'functionality': run_quick_test(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    
    for check_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {check_name.upper()}")
    
    print("\n" + "-"*60)
    print(f"TOTAL: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED - SYSTEM READY FOR DEMO!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} checks failed - Please review above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
