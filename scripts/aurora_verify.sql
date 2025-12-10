-- Verification Script for Aurora PostgreSQL + pgvector Setup
-- Run this script after aurora_init.sql to verify the installation

-- ============================================================================
-- CONNECTION INFORMATION
-- ============================================================================

SELECT 
    'Database verification started at: ' || CURRENT_TIMESTAMP AS message;

-- Display current database and user
SELECT 
    current_database() AS database_name,
    current_user AS current_user,
    version() AS postgres_version;

-- ============================================================================
-- EXTENSION VERIFICATION
-- ============================================================================

SELECT '=== EXTENSION VERIFICATION ===' AS section;

-- Check pgvector extension
SELECT 
    extname AS extension_name,
    extversion AS version,
    CASE 
        WHEN extname = 'vector' THEN '✓ pgvector is installed'
        ELSE '✗ Extension not found'
    END AS status
FROM pg_extension 
WHERE extname = 'vector';

-- ============================================================================
-- SCHEMA VERIFICATION
-- ============================================================================

SELECT '=== SCHEMA VERIFICATION ===' AS section;

-- Check if bedrock_integration schema exists
SELECT 
    schema_name,
    '✓ Schema exists' AS status
FROM information_schema.schemata 
WHERE schema_name = 'bedrock_integration';

-- ============================================================================
-- TABLE VERIFICATION
-- ============================================================================

SELECT '=== TABLE STRUCTURE VERIFICATION ===' AS section;

-- Verify bedrock_kb table structure
SELECT 
    column_name,
    data_type,
    CASE 
        WHEN is_nullable = 'NO' THEN 'NOT NULL'
        ELSE 'NULL'
    END AS nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'bedrock_integration' 
    AND table_name = 'bedrock_kb'
ORDER BY ordinal_position;

-- ============================================================================
-- INDEX VERIFICATION
-- ============================================================================

SELECT '=== INDEX VERIFICATION ===' AS section;

-- List all indexes on bedrock_kb table
SELECT 
    schemaname AS schema_name,
    tablename AS table_name,
    indexname AS index_name,
    indexdef AS definition,
    '✓ Index exists' AS status
FROM pg_indexes
WHERE schemaname = 'bedrock_integration' 
    AND tablename = 'bedrock_kb'
ORDER BY indexname;

-- ============================================================================
-- FUNCTION VERIFICATION
-- ============================================================================

SELECT '=== FUNCTION VERIFICATION ===' AS section;

-- List all functions in bedrock_integration schema
SELECT 
    routine_name AS function_name,
    routine_type AS type,
    data_type AS return_type,
    '✓ Function exists' AS status
FROM information_schema.routines
WHERE routine_schema = 'bedrock_integration'
ORDER BY routine_name;

-- ============================================================================
-- VIEW VERIFICATION
-- ============================================================================

SELECT '=== VIEW VERIFICATION ===' AS section;

-- List all views in bedrock_integration schema
SELECT 
    table_name AS view_name,
    '✓ View exists' AS status
FROM information_schema.views
WHERE table_schema = 'bedrock_integration'
ORDER BY table_name;

-- ============================================================================
-- PERMISSION VERIFICATION
-- ============================================================================

SELECT '=== PERMISSION VERIFICATION ===' AS section;

-- Check table permissions
SELECT 
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'bedrock_integration' 
    AND table_name = 'bedrock_kb'
ORDER BY grantee, privilege_type;

-- ============================================================================
-- DATA VERIFICATION
-- ============================================================================

SELECT '=== DATA VERIFICATION ===' AS section;

-- Count records in bedrock_kb
SELECT 
    COUNT(*) AS total_records,
    COUNT(CASE WHEN chunks IS NOT NULL THEN 1 END) AS records_with_chunks,
    COUNT(CASE WHEN embedding IS NOT NULL THEN 1 END) AS records_with_embeddings,
    COUNT(CASE WHEN metadata IS NOT NULL THEN 1 END) AS records_with_metadata
FROM bedrock_integration.bedrock_kb;

-- Show sample records
SELECT 
    id,
    LEFT(chunks, 50) || '...' AS chunk_preview,
    metadata->>'source' AS source,
    created_at
FROM bedrock_integration.bedrock_kb
LIMIT 5;

-- ============================================================================
-- STATISTICS VERIFICATION
-- ============================================================================

SELECT '=== KNOWLEDGE BASE STATISTICS ===' AS section;

-- Get comprehensive statistics
SELECT * FROM bedrock_integration.get_kb_statistics();

-- ============================================================================
-- HEALTH METRICS VERIFICATION
-- ============================================================================

SELECT '=== HEALTH METRICS ===' AS section;

-- Get health metrics from view
SELECT * FROM bedrock_integration.kb_health_metrics;

-- ============================================================================
-- VECTOR SEARCH TEST
-- ============================================================================

SELECT '=== VECTOR SEARCH TEST ===' AS section;

-- Test vector similarity search with a zero vector
SELECT 
    'Testing vector search functionality...' AS test;

-- Check if we can query using cosine similarity
SELECT 
    id,
    LEFT(chunks, 50) AS chunk_preview,
    1 - (embedding <=> ARRAY_FILL(0, ARRAY[1024])::VECTOR(1024)) AS similarity_score
FROM bedrock_integration.bedrock_kb
WHERE embedding IS NOT NULL
ORDER BY embedding <=> ARRAY_FILL(0, ARRAY[1024])::VECTOR(1024)
LIMIT 3;

-- ============================================================================
-- CONFIGURATION VERIFICATION
-- ============================================================================

SELECT '=== DATABASE CONFIGURATION ===' AS section;

-- Check relevant PostgreSQL configuration
SELECT 
    name,
    setting,
    unit,
    short_desc
FROM pg_settings
WHERE name IN (
    'shared_preload_libraries',
    'max_connections',
    'shared_buffers',
    'effective_cache_size',
    'work_mem'
)
ORDER BY name;

-- ============================================================================
-- DISK USAGE VERIFICATION
-- ============================================================================

SELECT '=== DISK USAGE ===' AS section;

-- Check table and index sizes
SELECT 
    'bedrock_kb' AS table_name,
    pg_size_pretty(pg_total_relation_size('bedrock_integration.bedrock_kb')) AS total_size,
    pg_size_pretty(pg_relation_size('bedrock_integration.bedrock_kb')) AS table_size,
    pg_size_pretty(pg_indexes_size('bedrock_integration.bedrock_kb')) AS indexes_size;

-- ============================================================================
-- READINESS CHECK
-- ============================================================================

SELECT '=== READINESS CHECK ===' AS section;

-- Comprehensive readiness check
WITH checks AS (
    SELECT 
        EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector') AS has_pgvector,
        EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'bedrock_integration') AS has_schema,
        EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 'bedrock_integration' AND table_name = 'bedrock_kb') AS has_table,
        (SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'bedrock_integration' AND tablename = 'bedrock_kb') >= 4 AS has_indexes,
        EXISTS(SELECT 1 FROM information_schema.routines WHERE routine_schema = 'bedrock_integration' AND routine_name = 'search_similar_documents') AS has_search_function,
        EXISTS(SELECT 1 FROM information_schema.views WHERE table_schema = 'bedrock_integration' AND table_name = 'kb_health_metrics') AS has_views
)
SELECT 
    CASE WHEN has_pgvector THEN '✓' ELSE '✗' END || ' pgvector extension' AS check_1,
    CASE WHEN has_schema THEN '✓' ELSE '✗' END || ' bedrock_integration schema' AS check_2,
    CASE WHEN has_table THEN '✓' ELSE '✗' END || ' bedrock_kb table' AS check_3,
    CASE WHEN has_indexes THEN '✓' ELSE '✗' END || ' Required indexes (4)' AS check_4,
    CASE WHEN has_search_function THEN '✓' ELSE '✗' END || ' Search function' AS check_5,
    CASE WHEN has_views THEN '✓' ELSE '✗' END || ' Monitoring views' AS check_6,
    CASE 
        WHEN has_pgvector AND has_schema AND has_table AND has_indexes AND has_search_function AND has_views 
        THEN '✓✓✓ DATABASE IS READY FOR BEDROCK KNOWLEDGE BASE ✓✓✓'
        ELSE '✗✗✗ SETUP INCOMPLETE - REVIEW ERRORS ABOVE ✗✗✗'
    END AS overall_status
FROM checks;

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

SELECT 
    'Verification completed at: ' || CURRENT_TIMESTAMP AS message;

SELECT 
    'If all checks passed, your Aurora PostgreSQL database is ready for Bedrock Knowledge Base integration!' AS final_message;
