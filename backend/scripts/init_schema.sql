-- ============================================================================
-- ChatKit Database Schema for Neon Postgres
-- Feature: 001-chatwidget-stabilization
-- Date: 2025-12-27
--
-- This script creates and aligns the database schema for ChatKit sessions.
-- Safe to run multiple times (idempotent with IF NOT EXISTS/IF EXISTS clauses).
-- ============================================================================

-- ============================================================================
-- STEP 1: Create conversations table if it doesn't exist
-- ============================================================================
CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- ============================================================================
-- STEP 2: Add missing columns to existing conversations table
-- These are safe to run even if columns already exist
-- ============================================================================

-- Add updated_at column if missing (T047)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conversations' AND column_name = 'updated_at'
    ) THEN
        ALTER TABLE conversations ADD COLUMN updated_at TIMESTAMP DEFAULT NOW();
    END IF;
END $$;

-- Add metadata column if missing (T048)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conversations' AND column_name = 'metadata'
    ) THEN
        ALTER TABLE conversations ADD COLUMN metadata JSONB DEFAULT '{}'::jsonb;
    END IF;
END $$;

-- ============================================================================
-- STEP 3: Create messages table if it doesn't exist (T050)
-- ============================================================================
CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    citations JSONB DEFAULT '[]'::jsonb,
    selected_text TEXT DEFAULT ''
);

-- ============================================================================
-- STEP 4: Create indexes for query performance (T051)
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);

-- ============================================================================
-- VERIFICATION QUERIES
-- Run these after migration to confirm schema is correct
-- ============================================================================

-- Uncomment and run to verify:
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'conversations'
-- ORDER BY ordinal_position;

-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'messages'
-- ORDER BY ordinal_position;

-- ============================================================================
-- TEST INSERT (verify schema works)
-- ============================================================================

-- Uncomment to test:
-- INSERT INTO conversations (id, created_at, updated_at, metadata)
-- VALUES ('test-schema-verify', NOW(), NOW(), '{"test": true}');
--
-- INSERT INTO messages (id, session_id, role, content, timestamp, citations, selected_text)
-- VALUES ('test-msg-001', 'test-schema-verify', 'user', 'Test message', NOW(), '[]', '');
--
-- -- Cleanup test data
-- DELETE FROM messages WHERE session_id = 'test-schema-verify';
-- DELETE FROM conversations WHERE id = 'test-schema-verify';
