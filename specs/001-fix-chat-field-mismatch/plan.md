# Implementation Plan: Fix Chat API Field Mismatch

**Branch**: `001-fix-chat-field-mismatch` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fix-chat-field-mismatch/spec.md`

## Summary

Fix the chat widget bug where frontend sends `query` field but backend expects `message`, combined with improving error handling to preserve HTTP status codes instead of masking all errors as 500.

## Technical Context

**Language/Version**: TypeScript 5.x (Frontend), Python 3.11+ (Backend)
**Primary Dependencies**: React 18.x, FastAPI 0.100+
**Storage**: N/A (stateless request-response)
**Testing**: Manual testing via chat widget
**Target Platform**: Web (GitHub Pages frontend, HuggingFace Space backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: N/A (bug fix, no performance changes)
**Constraints**: Manual HuggingFace Space restart required for backend deployment
**Scale/Scope**: 2 file changes (1 frontend, 1 backend)

## Constitution Check

*GATE: Passed - This is a targeted bug fix that does not violate any constitution principles.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Scientific Accuracy | N/A | No content changes |
| Academic Clarity | N/A | No content changes |
| Module Structure | N/A | No structural changes |
| Frontend Architecture | ✅ Compliant | Fixing existing component |
| Backend Architecture | ✅ Compliant | Improving error handling per best practices |
| Change Control | ✅ Compliant | Minimal, targeted changes |

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-chat-field-mismatch/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Research findings
├── data-model.md        # Data model documentation
├── quickstart.md        # Implementation quickstart
├── contracts/           # API contracts
│   └── chat-api.yaml    # OpenAPI specification
└── checklists/
    └── requirements.md  # Quality checklist
```

### Source Code (affected files)

```text
frontend/
└── src/
    └── components/
        └── ChatKit/
            └── ChatKit.tsx      # Line 124-126: Change 'query' to 'message'

backend/
└── app/
    └── chat.py                  # Line 108-113: Add HTTPException pass-through
```

**Structure Decision**: Web application pattern - separate frontend (Docusaurus) and backend (FastAPI) repositories with changes isolated to specific files.

## Complexity Tracking

No constitution violations. This is a minimal bug fix with no added complexity.

## Implementation Details

### Task 1: Frontend Field Name Fix

**File**: `frontend/src/components/ChatKit/ChatKit.tsx`
**Lines**: 124-126

**Current Code**:
```typescript
const response = await chatService.sendMessage({
  query: message,
  session_id: currentSessionId
});
```

**Fixed Code**:
```typescript
const response = await chatService.sendMessage({
  message: message,
  session_id: currentSessionId
});
```

**Rationale**: Backend `chat.py:39` expects `request.get("message")`. The frontend must align with the backend's expected field name.

### Task 2: Backend Exception Handling Fix

**File**: `backend/app/chat.py`
**Lines**: 108-113

**Current Code**:
```python
except Exception as e:
    logger.error(f"Error in chat endpoint: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )
```

**Fixed Code**:
```python
except HTTPException:
    raise
except Exception as e:
    logger.error(f"Error in chat endpoint: {type(e).__name__}: {str(e)}", exc_info=True)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )
```

**Rationale**: FastAPI's HTTPException (raised at line 44-47 for validation errors) should propagate unchanged to return proper 400 status codes. The current code catches all exceptions and converts them to 500.

### Task 3: Deploy Backend

1. Commit backend changes
2. Push to repository
3. Navigate to HuggingFace Space: `alihaidernoorani-deploy-docusaurus-book`
4. Click "Restart Space" to apply changes

### Task 4: Deploy Frontend

1. Commit frontend changes
2. Run `npm run build`
3. Deploy to GitHub Pages

### Task 5: Verification

Test the fix by:
1. Opening the chat widget on the textbook site
2. Sending a test message
3. Confirming a response is received (not an error)
4. Checking browser console for no 500 errors

## Acceptance Criteria

From spec, mapped to implementation:

| Requirement | Implementation | Verification |
|-------------|---------------|--------------|
| FR-001: Frontend sends `message` field | Task 1 | Manual test |
| FR-002: Backend preserves HTTP status codes | Task 2 | Send invalid request, verify 400 returned |
| FR-003: Backend logs detailed errors | Task 2 (enhanced logging) | Check HF Space logs |
| FR-004: HTTPException re-raised unchanged | Task 2 | Validation error returns 400 |
| FR-005: Validation returns 4xx codes | Task 2 | Manual test |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Frontend change breaks other callers | Only ChatKit.tsx uses chatService.sendMessage |
| Backend deployment fails | Test locally before HF Space restart |
| Missed test cases | Changes are minimal and directly address known bug |

## Post-Implementation

After `/sp.tasks` generates tasks and implementation is complete:
1. Create PHR documenting the fix
2. Consider ADR if this pattern should be standardized across other endpoints
3. Monitor production logs for any remaining errors
