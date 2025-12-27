# Implementation Plan: ChatWidget Stabilization

**Branch**: `001-chatwidget-stabilization` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-chatwidget-stabilization/spec.md`

**Note**: This plan covers Phase 11 - Database Schema Alignment to fix the production ChatKit session creation failures.

## Summary

Fix the ChatKit backend database schema mismatch that causes session creation failures on Hugging Face Spaces. The Neon Postgres database was manually initialized with an incomplete schema missing the `updated_at` column on the `conversations` table, causing "column does not exist" errors and triggering fallback mode in the frontend.

**Technical Approach**: Use ALTER TABLE statements to add missing columns while preserving existing data, then add backend safeguards to prevent future schema-related crashes.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript (frontend)
**Primary Dependencies**: FastAPI, psycopg2, Docusaurus, React
**Storage**: Neon Postgres (cloud), Qdrant (vector DB)
**Testing**: pytest, manual verification via Neon console
**Target Platform**: Hugging Face Spaces (backend), GitHub Pages (frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: Session creation < 500ms, 90% query success rate
**Constraints**: No data loss during migration, maintain backward compatibility
**Scale/Scope**: Single-tenant deployment, ~100 daily users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Scientific Accuracy: All technical claims must be verifiable and traceable to reputable sources
- Academic Clarity: Content must be written for undergraduate-level audience with proper terminology definitions
- Reproducibility & Transparency: All methods and algorithms must be presented with sufficient detail for reproduction
- Ethical & Safety Awareness: All content must address ethical implications and safety constraints
- Module Structure Compliance: All content must follow the fixed 4-module structure (The Robotic Nervous System (ROS 2), The Digital Twin (Gazebo & Unity), The AI-Robot Brain (NVIDIA Isaac™), Vision-Language-Action (VLA))
- Frontend Architecture: Must implement Docusaurus-based frontend with interactive module cards, glossary, quizzes, and reusable MDX components
- Backend Architecture: Must implement FastAPI backend with RAG chatbot, Qdrant vector database, and translation/personalization endpoints
- Personalization & Translation: Urdu toggle and personalization must function on every chapter
- Change Control: Module names, structure, and hierarchy are immutable - no autonomous scope expansion allowed

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

---

## Phase 11: Database Schema Alignment

### Problem Statement

The ChatKit backend on Hugging Face Spaces is failing to create chat sessions due to a schema mismatch between the backend code expectations and the actual Neon Postgres database schema.

**Observed Errors**:
- `relation "conversations" does not exist` (initial state)
- `column "updated_at" of relation "conversations" does not exist` (current state)

**Root Cause**: The Neon database was manually initialized with an incomplete schema.

### Design Decision: ALTER vs DROP/RECREATE

**Decision**: Use ALTER TABLE to add missing columns

**Rationale**:
1. Preserves any existing conversation data
2. Lower risk than DROP/RECREATE
3. Idempotent (safe to run multiple times)
4. No downtime required

**Alternatives Rejected**:
- DROP and recreate: Would lose existing data
- Backend code change: Would break ChatKit protocol compliance

### Schema Migration Plan

Execute the following SQL in Neon Postgres console:

```sql
-- Add missing columns to conversations table
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

-- Ensure messages table exists
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

### Backend Safeguards (Recommended Follow-up)

Add schema validation at backend startup:

1. **Schema validation**: Check required tables and columns exist
2. **Connection health**: Validate connection state before queries
3. **Graceful degradation**: Return error response if DB unavailable (not crash)

### Implementation Tasks

1. **T047 [P11]**: Execute schema migration SQL in Neon console
2. **T048 [P11]**: Verify session creation succeeds via API test
3. **T049 [P11]**: Verify ChatKit exits fallback mode on frontend
4. **T050 [P11]**: (Optional) Add schema validation to backend startup

### Success Criteria

1. `/api/v1/chat/session` endpoint returns 200 with valid session_id
2. No "column does not exist" errors in backend logs
3. ChatKit widget functions normally without fallback mode
4. Message storage and retrieval works correctly

### Artifacts Generated

- `specs/001-chatwidget-stabilization/research.md` - Phase 11 research findings
- `specs/001-chatwidget-stabilization/data-model.md` - Database schema documentation
- `specs/001-chatwidget-stabilization/contracts/schema-migration.sql` - SQL migration script
