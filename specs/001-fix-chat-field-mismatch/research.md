# Research: Fix Chat API Field Mismatch

**Feature Branch**: `001-fix-chat-field-mismatch`
**Date**: 2025-12-27
**Status**: Complete

## Executive Summary

This is a targeted bug fix with no unknowns. The issue is clearly identified through code inspection:

1. **Frontend ChatKit.tsx (line 124-125)** sends `{ query: message, session_id }`
2. **Backend chat.py (line 39)** expects `request.get("message")`
3. **Backend chat.py (line 108-113)** catches all exceptions including HTTPException, converting 400 → 500

## Research Findings

### 1. Field Name Mismatch Analysis

**Decision**: Change frontend from `query` to `message`

**Rationale**:
- Backend schema is authoritative (defines the API contract)
- Backend already uses `message` field in ChatRequest class (line 16)
- Backend validation returns 400 for empty `message` (lines 43-47)
- Changing backend would require updating multiple endpoints and tests

**Alternatives considered**:
- Accept both `query` and `message` on backend → Adds unnecessary complexity
- Change backend to use `query` → Would break existing contracts/tests

**Code references**:
- Frontend sends: `ChatKit.tsx:124-126` → `{ query: message, session_id: currentSessionId }`
- Backend expects: `chat.py:39` → `message = request.get("message", "")`

### 2. Exception Handling Analysis

**Decision**: Add explicit HTTPException pass-through before generic Exception handler

**Rationale**:
- FastAPI HTTPException should propagate unchanged to return proper status codes
- Current code catches HTTPException as part of generic Exception handler
- This masks validation errors (400) as server errors (500)
- Standard FastAPI best practice is to re-raise HTTPException

**Alternatives considered**:
- Use middleware for exception handling → Overkill for this fix
- Custom exception classes → Not needed for simple validation errors

**Code references**:
- Current handler: `chat.py:108-113` catches all exceptions
- HTTPException raised at: `chat.py:44-47` (validation error)

### 3. Similar Patterns in Codebase

Found same error handling issue in:
- `translate_endpoint` (chat.py:157-162)
- `personalize_endpoint` (chat.py:217-222)

**Recommendation**: Fix all three endpoints for consistency, but only `/chat` is in scope for this fix per spec.

## Technical Validation

### Frontend Change Verification

```typescript
// Current (ChatKit.tsx:124-126)
const response = await chatService.sendMessage({
  query: message,        // ❌ Wrong field name
  session_id: currentSessionId
});

// Fixed
const response = await chatService.sendMessage({
  message: message,      // ✅ Matches backend expectation
  session_id: currentSessionId
});
```

### Backend Change Verification

```python
# Current (chat.py:108-113)
except Exception as e:
    logger.error(f"Error in chat endpoint: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )

# Fixed
except HTTPException:
    raise  # ✅ Preserve original status code (400, 401, 403, etc.)
except Exception as e:
    logger.error(f"Error in chat endpoint: {type(e).__name__}: {str(e)}", exc_info=True)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )
```

## Dependencies

| Dependency | Version | Notes |
|------------|---------|-------|
| React | 18.x | Frontend framework |
| TypeScript | 5.x | Frontend types |
| FastAPI | 0.100+ | Backend framework |
| Python | 3.11+ | Backend runtime |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Breaking other frontend consumers | Low | High | Single consumer (ChatKit.tsx) |
| Backend deployment failure | Low | Medium | Test locally before HF restart |
| Missed edge cases | Low | Low | Changes are minimal and targeted |

## Conclusion

No NEEDS CLARIFICATION items remain. This is a straightforward bug fix:
1. One-line change in frontend (field name)
2. Two-line addition in backend (exception handling)
3. Manual restart of HuggingFace Space after deployment

Ready to proceed to Phase 1: Design & Contracts.
