---
id: 18
title: Plan database schema alignment for ChatKit
stage: plan
date_iso: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: 001-chatwidget-stabilization
branch: 001-chatwidget-stabilization
user: Claude Sonnet 4.5
command: sp.plan
labels:
  - database
  - schema
  - neon-postgres
  - migration
  - chatkit
links:
  spec: specs/001-chatwidget-stabilization/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-chatwidget-stabilization/research.md
  - specs/001-chatwidget-stabilization/data-model.md
  - specs/001-chatwidget-stabilization/plan.md
  - specs/001-chatwidget-stabilization/contracts/schema-migration.sql
  - CLAUDE.md
tests_yaml: |
  - Schema validation queries provided in migration script
  - Session creation API test criteria defined
outcome: |
  Successfully created implementation plan for fixing ChatKit backend
  database schema mismatch. Plan includes ALTER TABLE migration strategy
  to preserve existing data, SQL scripts for Neon console execution,
  and follow-up safeguards for backend schema validation.
evaluation: |
  Phase 0 research complete - identified exact schema requirements from
  backend code (agent.py). Phase 1 design complete - data model and
  migration SQL generated. Ready for implementation phase.
---

# Prompt History Record: Plan database schema alignment for ChatKit

## Original Prompt

Context:
The ChatKit backend on Hugging Face Spaces is failing to create chat sessions.
Postgres (Neon) connection now works, but session creation fails due to schema mismatch.

Observed errors:
- relation "conversations" does not exist (previously)
- column "updated_at" of relation "conversations" does not exist (current)

Current state:
- Backend expects a conversations table with id, created_at, updated_at
- Neon database was initialized manually and schema does not match backend expectations
- These DB errors cause ChatKit to fail session creation and enter fallback mode

Goal:
Create a stable, production-safe solution that:
1. Aligns the database schema with backend expectations
2. Prevents transaction-aborted cascades
3. Ensures ChatKit sessions never fail due to missing tables or columns

Output required:
- Recommended schema changes (SQL)
- Whether to alter existing tables or recreate them
- Any backend safeguards needed to avoid future schema-related crashes

## Implementation Response

### Analysis Completed

1. **Backend Code Analysis** (backend/app/agent.py):
   - `create_conversation()` method expects: `id`, `created_at`, `updated_at`, `metadata`
   - `add_message_to_conversation()` method expects: `id`, `session_id`, `role`, `content`, `timestamp`, `citations`, `selected_text`

2. **Root Cause**: Neon database manually initialized with incomplete schema missing `updated_at` column

### Design Decision

**Selected Approach**: ALTER TABLE to add missing columns
- Preserves existing data
- Idempotent (safe to run multiple times)
- No downtime required

**Rejected Alternatives**:
- DROP/RECREATE: Loses data
- Backend code change: Breaks ChatKit protocol

### Artifacts Generated

1. **research.md** - Added Phase 11 section with schema requirements analysis
2. **data-model.md** - Added Section 5 with database schema documentation
3. **plan.md** - Added Phase 11 design section with migration plan
4. **contracts/schema-migration.sql** - Complete SQL migration script

### SQL Migration (Execute in Neon Console)

```sql
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    citations JSONB DEFAULT '[]'::jsonb,
    selected_text TEXT DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);
```

### Success Criteria

1. `/api/v1/chat/session` returns 200 with valid session_id
2. No "column does not exist" errors in backend logs
3. ChatKit exits fallback mode
4. Message storage/retrieval works correctly

### Next Steps

1. Execute SQL migration in Neon console
2. Verify session creation via API test
3. Test ChatKit frontend exits fallback mode
4. (Optional) Add schema validation to backend startup
