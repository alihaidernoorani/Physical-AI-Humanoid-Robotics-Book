# Research: ChatWidget Stabilization and End-to-End Communication

## Overview
This research document addresses the requirements for stabilizing the global ChatWidget in the Docusaurus frontend and ensuring reliable end-to-end communication with the deployed backend RAG API.

## 1. Current ChatWidget Mounting Location Analysis

### Current State
- The ChatKit component is currently mounted in `frontend/src/theme/Root.tsx`
- This location may cause interaction issues in the deployed GitHub Pages environment
- Root.tsx is a low-level Docusaurus theme component that wraps all content

### Recommended Change
- Move ChatKit to a Docusaurus Layout component for better stability
- The Layout component is more appropriate for global UI elements
- This ensures consistent behavior across all pages

## 2. React State Logic Verification

### Current State
- ChatKit component uses React hooks (useState, useEffect) for state management
- State includes: messages, session ID, visibility, loading, error
- State transitions handle: open/close, minimize/maximize, message submission

### Issues Identified
- No apparent issues with current state logic
- Proper loading and error state handling implemented
- Session management with proper initialization

## 3. CSS and Positioning Analysis

### Current State
- ChatKit has CSS in `frontend/src/components/ChatKit/ChatKit.css`
- Uses relative/absolute positioning with z-index for layering
- Toggle button for open/close functionality

### Issues Identified
- Positioning may not be optimal for all Docusaurus page layouts
- Z-index and layering might conflict with other UI elements
- Need to ensure pointer-events don't interfere with page content

## 4. Frontend API Configuration

### Current State
- API base URL defined in `frontend/src/services/api.js`
- Default: `http://localhost:8000/api/v1`
- Can be overridden with `REACT_APP_API_BASE_URL` environment variable

### Required Change
- Configure for production backend: `https://alihaidernoorani-deploy-docusaurus-book.hf.space/`
- Ensure environment-safe base URL for GitHub Pages deployment

## 5. Backend CORS Configuration

### Current State
- Backend in `backend/app/main.py` has CORS middleware
- Currently allows: `https://alihaidernoorani.github.io/Physical-AI-Humanoid-Robotics-Book`
- This should already allow requests from the deployed frontend

### Verification Needed
- Confirm exact origin matches deployment URL
- Verify CORS settings allow all necessary headers/methods

## 6. Backend API Endpoints

### Current Endpoints
- `/api/v1/chat` - Send/receive chat messages
- `/api/v1/chat/session` - Create chat sessions
- `/api/v1/chat/history/{sessionId}` - Get chat history
- `/api/v1/health` - Health check

### Implementation Plan
- Ensure endpoints are properly configured for production use
- Verify session management works across page navigation

## 7. Deployment Considerations

### Frontend (GitHub Pages)
- Static hosting with potential routing limitations
- Environment variables must be set at build time
- Need to ensure ChatKit works with client-side routing

### Backend (Hugging Face Space)
- Serverless deployment with potential cold start delays
- Need to handle timeout scenarios gracefully
- API response times may vary

## 8. Testing Strategy

### Frontend Tests
- Unit tests for ChatKit component state management
- Integration tests for API communication
- UI behavior tests for open/close/minimize interactions

### End-to-End Tests
- Full flow testing from frontend to backend
- Error handling verification
- Cross-page consistency testing

## Decision: Implementation Approach

### Approach Selected: SSG-Safe Theme Wrapper
1. Keep ChatKit in Root.tsx (correct location for global components)
2. Remove @theme/Layout override to prevent circular dependencies
3. Create ChatLoader component with useState/useEffect for lazy loading
4. Use dynamic imports to prevent SSG evaluation of browser APIs
5. Implement BrowserOnly pattern with proper useEffect hooks

### Rationale:
- Addresses "RangeError: Maximum call stack size exceeded" during SSG builds
- Prevents circular dependencies that occur with Layout.tsx override
- Ensures browser-specific code only executes after hydration
- Maintains global availability of ChatWidget across all pages

## Alternatives Considered

### Alternative 1: Layout.tsx Override (Previous Approach)
- Rejected: Causes circular dependencies and SSG build failures
- Creates "RangeError: Maximum call stack size exceeded" during builds

### Alternative 2: Direct BrowserOnly with require() (Previous Approach)
- Rejected: Causes infinite recursion during SSG processing
- Still evaluates browser APIs during static generation

## Dependencies and Best Practices

### Dependencies
- React 18+ for hooks and state management
- Docusaurus for Layout component integration
- FastAPI for backend API compatibility

### Best Practices
- Follow React performance guidelines (avoid unnecessary re-renders)
- Use proper error boundaries for error handling
- Implement proper cleanup for useEffect hooks
- Follow accessibility guidelines (ARIA labels, keyboard navigation)

## Risk Analysis

### High Risk Items
- Backend deployment availability during testing
- CORS configuration changes affecting other functionality

### Medium Risk Items
- CSS conflicts with existing Docusaurus components
- Session persistence across page navigation

### Mitigation Strategies
- Thorough testing in staging environment before production
- Maintain backward compatibility during migration
- Implement fallback error handling

---

## Phase 11: Database Schema Alignment (2025-12-27)

### Problem Statement

The ChatKit backend on Hugging Face Spaces is failing to create chat sessions due to a schema mismatch between the backend code expectations and the actual Neon Postgres database schema.

**Observed Errors**:
- `relation "conversations" does not exist` (initial state)
- `column "updated_at" of relation "conversations" does not exist` (current state)

### Backend Schema Requirements (from agent.py)

The backend code expects two tables:

#### Table: `conversations`
Required columns based on backend code analysis (agent.py lines 86-91):
- `id`: VARCHAR(36) PRIMARY KEY - Session identifier
- `created_at`: TIMESTAMP - Creation timestamp
- `updated_at`: TIMESTAMP - Last update timestamp
- `metadata`: JSONB - Optional metadata storage

**Decision**: The `conversations` table must have all four columns to match the INSERT statement in `create_conversation()` method.

#### Table: `messages`
Required columns based on backend code analysis (agent.py lines 139-152):
- `id`: VARCHAR(36) PRIMARY KEY - Message identifier
- `session_id`: VARCHAR(36) FOREIGN KEY - References conversations.id
- `role`: VARCHAR(20) NOT NULL - 'user', 'assistant', or 'system'
- `content`: TEXT NOT NULL - Message content
- `timestamp`: TIMESTAMP - Message timestamp
- `citations`: JSONB - Array of citation references
- `selected_text`: TEXT - User-selected text context

### Current Database State Analysis

**Finding**: The Neon database was initialized manually with an incomplete schema missing:
- The `updated_at` column on `conversations` table
- Potentially missing columns on `messages` table

### Alternatives Considered

| Option | Description | Verdict |
|--------|-------------|---------|
| A. ALTER existing tables | Add missing columns with defaults | **Recommended** - Preserves existing data |
| B. DROP and recreate | Drop tables and create fresh | Not recommended - Loses data |
| C. Backend code change | Remove `updated_at` usage | Not recommended - Breaks ChatKit protocol |

### Transaction Cascade Issue

When a query fails (e.g., missing column), Postgres marks the transaction as aborted. Any subsequent queries in the same transaction will fail with:
```
current transaction is aborted, commands ignored until end of transaction block
```

**Decision**: The backend already has `self.db_connection.rollback()` in exception handlers. Connection pooling should be verified.

### Recommended SQL Migration

```sql
-- Fix conversations table (add missing column)
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();

-- Ensure conversations has correct columns
ALTER TABLE conversations
ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

-- Ensure messages table exists with correct schema
CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    citations JSONB DEFAULT '[]'::jsonb,
    selected_text TEXT DEFAULT ''
);

-- Add index for session_id lookups
CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id);
```

### Backend Safeguards Recommended

1. **Schema validation at startup**: Verify tables and columns exist
2. **Connection health check**: Validate connection state before queries
3. **Graceful degradation**: Return fallback response if DB unavailable

### Success Criteria

1. Session creation succeeds without schema errors
2. Messages are stored and retrieved correctly
3. No transaction-aborted cascades occur
4. ChatKit widget exits fallback mode