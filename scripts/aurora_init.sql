-- Aurora PostgreSQL Initialization Script
-- DocSmart RAG System - AWS AI Engineer Nanodegree Final Project
-- This script sets up the database schema for Bedrock Knowledge Base with pgvector

-- ============================================================================
-- STEP 1: Enable pgvector Extension
-- ============================================================================

-- Create pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify extension is installed
SELECT * FROM pg_extension WHERE extname = 'vector';

-- ============================================================================
-- STEP 2: Create Schema for Bedrock Integration
-- ============================================================================

-- Create dedicated schema for Bedrock Knowledge Base
CREATE SCHEMA IF NOT EXISTS bedrock_integration;

-- Set search path
SET search_path TO bedrock_integration, public;

-- ============================================================================
-- STEP 3: Create Main Knowledge Base Table
-- ============================================================================

-- Table structure required by Bedrock Knowledge Base
-- Field names match the field_mapping in Terraform configuration
CREATE TABLE IF NOT EXISTS bedrock_integration.bedrock_kb (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunks TEXT NOT NULL,
    embedding VECTOR(1024),  -- Amazon Titan Embeddings v2 produces 1024-dimensional vectors
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add comment to table
COMMENT ON TABLE bedrock_integration.bedrock_kb IS 'Main table for Bedrock Knowledge Base storing document chunks and embeddings';

-- Add comments to columns
COMMENT ON COLUMN bedrock_integration.bedrock_kb.id IS 'Unique identifier for each chunk';
COMMENT ON COLUMN bedrock_integration.bedrock_kb.chunks IS 'Text content of the document chunk';
COMMENT ON COLUMN bedrock_integration.bedrock_kb.embedding IS '1024-dimensional vector from Amazon Titan Embeddings v2';
COMMENT ON COLUMN bedrock_integration.bedrock_kb.metadata IS 'JSON metadata including source document, page number, etc.';

-- ============================================================================
-- STEP 4: Create Indexes for Performance
-- ============================================================================

-- Index for vector similarity search using cosine distance
CREATE INDEX IF NOT EXISTS bedrock_kb_embedding_idx 
ON bedrock_integration.bedrock_kb 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index for metadata queries
CREATE INDEX IF NOT EXISTS bedrock_kb_metadata_idx 
ON bedrock_integration.bedrock_kb 
USING gin (metadata);

-- Index for full-text search on chunks
CREATE INDEX IF NOT EXISTS bedrock_kb_chunks_fts_idx 
ON bedrock_integration.bedrock_kb 
USING gin (to_tsvector('english', chunks));

-- Index for timestamp queries
CREATE INDEX IF NOT EXISTS bedrock_kb_created_at_idx 
ON bedrock_integration.bedrock_kb (created_at DESC);

-- ============================================================================
-- STEP 5: Create Update Trigger for updated_at
-- ============================================================================

-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION bedrock_integration.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function before update
CREATE TRIGGER update_bedrock_kb_updated_at
BEFORE UPDATE ON bedrock_integration.bedrock_kb
FOR EACH ROW
EXECUTE FUNCTION bedrock_integration.update_updated_at_column();

-- ============================================================================
-- STEP 6: Create Helper Functions
-- ============================================================================

-- Function to search similar documents by vector
CREATE OR REPLACE FUNCTION bedrock_integration.search_similar_documents(
    query_embedding VECTOR(1024),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    chunks TEXT,
    similarity FLOAT,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        bedrock_kb.id,
        bedrock_kb.chunks,
        1 - (bedrock_kb.embedding <=> query_embedding) AS similarity,
        bedrock_kb.metadata
    FROM bedrock_integration.bedrock_kb
    WHERE 1 - (bedrock_kb.embedding <=> query_embedding) > match_threshold
    ORDER BY bedrock_kb.embedding <=> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Function to get statistics about the knowledge base
CREATE OR REPLACE FUNCTION bedrock_integration.get_kb_statistics()
RETURNS TABLE (
    total_chunks BIGINT,
    avg_chunk_length FLOAT,
    total_metadata_keys INT,
    oldest_entry TIMESTAMP WITH TIME ZONE,
    newest_entry TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT AS total_chunks,
        AVG(LENGTH(chunks))::FLOAT AS avg_chunk_length,
        COUNT(DISTINCT jsonb_object_keys(metadata))::INT AS total_metadata_keys,
        MIN(created_at) AS oldest_entry,
        MAX(created_at) AS newest_entry
    FROM bedrock_integration.bedrock_kb;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- STEP 7: Create Views for Monitoring
-- ============================================================================

-- View to monitor recent ingestions
CREATE OR REPLACE VIEW bedrock_integration.recent_ingestions AS
SELECT 
    id,
    LEFT(chunks, 100) AS chunk_preview,
    metadata->>'source' AS source_document,
    metadata->>'page' AS page_number,
    created_at
FROM bedrock_integration.bedrock_kb
ORDER BY created_at DESC
LIMIT 100;

-- View to monitor database size and statistics
CREATE OR REPLACE VIEW bedrock_integration.kb_health_metrics AS
SELECT 
    COUNT(*) AS total_documents,
    AVG(LENGTH(chunks)) AS avg_chunk_size,
    MAX(LENGTH(chunks)) AS max_chunk_size,
    MIN(LENGTH(chunks)) AS min_chunk_size,
    pg_size_pretty(pg_total_relation_size('bedrock_integration.bedrock_kb')) AS table_size,
    pg_size_pretty(pg_indexes_size('bedrock_integration.bedrock_kb')) AS indexes_size
FROM bedrock_integration.bedrock_kb;

-- ============================================================================
-- STEP 8: Grant Permissions
-- ============================================================================

-- Grant necessary permissions to the database user
-- Note: Replace 'dbadmin' with your actual database username if different
GRANT USAGE ON SCHEMA bedrock_integration TO dbadmin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA bedrock_integration TO dbadmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA bedrock_integration TO dbadmin;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA bedrock_integration TO dbadmin;

-- Grant permissions for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA bedrock_integration
GRANT ALL PRIVILEGES ON TABLES TO dbadmin;

ALTER DEFAULT PRIVILEGES IN SCHEMA bedrock_integration
GRANT ALL PRIVILEGES ON SEQUENCES TO dbadmin;

ALTER DEFAULT PRIVILEGES IN SCHEMA bedrock_integration
GRANT EXECUTE ON FUNCTIONS TO dbadmin;

-- ============================================================================
-- STEP 9: Verification Queries
-- ============================================================================

-- Check if pgvector is installed
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';

-- Check if schema exists
SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'bedrock_integration';

-- Check if table exists with correct structure
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_schema = 'bedrock_integration' AND table_name = 'bedrock_kb'
ORDER BY ordinal_position;

-- Check indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'bedrock_integration' AND tablename = 'bedrock_kb';

-- Get initial statistics
SELECT * FROM bedrock_integration.get_kb_statistics();

-- ============================================================================
-- STEP 10: Sample Data for Testing (Optional)
-- ============================================================================

-- Insert sample document chunk for testing
-- This can be removed after verification
INSERT INTO bedrock_integration.bedrock_kb (chunks, embedding, metadata)
VALUES (
    'This is a sample document chunk for testing the Bedrock Knowledge Base integration.',
    ARRAY_FILL(0, ARRAY[1024])::VECTOR(1024),  -- Zero vector for testing
    jsonb_build_object(
        'source', 'test_document.pdf',
        'page', '1',
        'section', 'introduction',
        'test', true
    )
);

-- Verify sample data insertion
SELECT COUNT(*) AS sample_count FROM bedrock_integration.bedrock_kb WHERE metadata->>'test' = 'true';

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully!';
    RAISE NOTICE 'Schema: bedrock_integration';
    RAISE NOTICE 'Table: bedrock_kb';
    RAISE NOTICE 'Vector dimension: 1024 (Amazon Titan Embeddings v2)';
    RAISE NOTICE 'Indexes created: 4 (vector similarity, metadata, full-text, timestamp)';
    RAISE NOTICE 'Helper functions created: 2 (search_similar_documents, get_kb_statistics)';
    RAISE NOTICE 'Views created: 2 (recent_ingestions, kb_health_metrics)';
END $$;
