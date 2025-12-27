-- ChatKit Database Schema Migration for Neon Postgres
-- Feature: 001-chatwidget-stabilization
-- Date: 2025-12-27
-- Purpose: Align database schema with backend expectations to fix session creation failures

-- ============================================================================
-- MIGRATION SCRIPT
-- Run this in Neon Postgres console to fix schema mismatch issues
-- ============================================================================

-- Step 1: Create conversations table if it doesn't exist
CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Step 2: Add missing columns to existing conversations table
-- (Safe to run even if columns already exist due to IF NOT EXISTS)
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

-- Step 3: Create messages table if it doesn't exist
CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    citations JSONB DEFAULT '[]'::jsonb,
    selected_text TEXT DEFAULT ''
);

-- Step 4: Create index for efficient session message retrieval
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);

-- Step 5: Create index for timestamp-based queries (optional, for performance)
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);

-- ============================================================================
-- VERIFICATION QUERIES
-- Run these to verify the schema is correct
-- ============================================================================

-- Verify conversations table structure
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'conversations';

-- Verify messages table structure
-- SELECT column_name, data_type, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'messages';

-- Test insert into conversations (should succeed after migration)
-- INSERT INTO conversations (id, created_at, updated_at, metadata)
-- VALUES ('test-session-001', NOW(), NOW(), '{}');

-- Clean up test data
-- DELETE FROM conversations WHERE id = 'test-session-001';

-- ============================================================================
-- ROLLBACK SCRIPT (use with caution - will lose data)
-- ============================================================================

-- DROP TABLE IF EXISTS messages;
-- DROP TABLE IF EXISTS conversations;
