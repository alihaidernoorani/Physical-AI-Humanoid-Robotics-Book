# Tasks: Fix Chat API Field Mismatch

**Input**: Design documents from `/specs/001-fix-chat-field-mismatch/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Tests**: Manual testing only - no automated tests requested

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/src/`
- Frontend: Docusaurus-based (GitHub Pages)
- Backend: FastAPI (HuggingFace Space)

---

## Phase 1: Setup (Not Required)

**Purpose**: No setup needed - this is a targeted bug fix on existing infrastructure

*No tasks in this phase - project is already set up*

---

## Phase 2: Foundational (Not Required)

**Purpose**: No foundational work needed - infrastructure already exists

*No tasks in this phase - all infrastructure is already in place*

---

## Phase 3: User Story 1 - Successful Chat Message (Priority: P1) 🎯 MVP

**Goal**: Fix the field name mismatch so users can successfully send and receive chat messages

**Independent Test**: Open the chat widget, type "What is ROS 2?", click send, and verify an AI response is displayed

### Implementation for User Story 1

- [x] T001 [P] [US1] Change field name from `query` to `message` in frontend/src/components/ChatKit/ChatKit.tsx at lines 124-126

**Details for T001**:
```typescript
// Current code (line 124-126):
const response = await chatService.sendMessage({
  query: message,
  session_id: currentSessionId
});

// Change to:
const response = await chatService.sendMessage({
  message: message,
  session_id: currentSessionId
});
```

**Checkpoint**: After T001, valid chat messages will be sent with the correct field name. However, error handling improvements (US2) should also be applied for complete fix.

---

## Phase 4: User Story 2 - Meaningful Error Messages (Priority: P2)

**Goal**: Improve error handling so validation errors return proper 400 status codes instead of being masked as 500 errors

**Independent Test**: Send a request with empty message body to `/api/v1/chat` and verify 400 status is returned (not 500)

### Implementation for User Story 2

- [x] T002 [P] [US2] Add HTTPException pass-through in exception handler in backend/app/chat.py at lines 108-113

**Details for T002**:
```python
# Current code (lines 108-113):
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Change to:
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

**Checkpoint**: After T002, HTTPException (including 400 Bad Request) will propagate correctly instead of being masked as 500.

---

## Phase 5: Deployment & Verification

**Goal**: Deploy changes and verify the fix works in production

### Deployment Tasks

- [ ] T003 [US1] [US2] Commit and push backend changes to repository for backend/app/chat.py
- [ ] T004 [US1] [US2] Manually restart HuggingFace Space at alihaidernoorani-deploy-docusaurus-book to apply backend changes
- [ ] T005 [US1] Commit and push frontend changes to repository for frontend/src/components/ChatKit/ChatKit.tsx
- [ ] T006 [US1] Build frontend with `npm run build` and deploy to GitHub Pages

### Verification Tasks

- [ ] T007 [US1] Manual Test: Open chat widget on textbook site and send message "Hello" - verify AI response appears
- [ ] T008 [US1] Manual Test: Check browser console for no 500 errors during chat interaction
- [ ] T009 [US2] Manual Test: Verify empty message returns 400 status (not 500) via browser dev tools or curl
- [ ] T010 [US2] Manual Test: Check HuggingFace Space logs for proper error logging format

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)       → SKIP (not needed)
Phase 2 (Foundation)  → SKIP (not needed)
Phase 3 (US1)         → T001 (frontend fix)
Phase 4 (US2)         → T002 (backend fix) - can run in parallel with T001
Phase 5 (Deploy)      → T003-T006 (depends on T001 and T002)
Phase 5 (Verify)      → T007-T010 (depends on T003-T006)
```

### User Story Dependencies

- **User Story 1 (P1)**: T001 → T003, T005, T006 → T007, T008
- **User Story 2 (P2)**: T002 → T003, T004 → T009, T010

### Parallel Opportunities

```
T001 [Frontend] ─┐
                 ├─→ T003-T006 [Deploy] ─→ T007-T010 [Verify]
T002 [Backend]  ─┘
```

T001 and T002 can be executed in parallel since they modify different files in different repositories.

---

## Parallel Example

```bash
# Execute both code changes in parallel:
Task T001: "Change field name from query to message in frontend/src/components/ChatKit/ChatKit.tsx"
Task T002: "Add HTTPException pass-through in backend/app/chat.py"

# Then deploy sequentially:
Task T003: "Commit and push backend changes"
Task T004: "Restart HuggingFace Space"
Task T005: "Commit and push frontend changes"
Task T006: "Build and deploy frontend"

# Finally verify:
Task T007-T010: "Manual verification tests"
```

---

## Implementation Strategy

### MVP First (Fastest Path)

1. ✅ Complete T001 (frontend field fix) - fixes the core issue
2. ✅ Complete T002 (backend error handling) - improves debugging
3. ✅ Deploy backend (T003, T004) - requires manual HF Space restart
4. ✅ Deploy frontend (T005, T006)
5. ✅ Verify (T007-T010)

**Total estimated effort**: 4 code changes, 2 deploys, 4 manual verifications

### Risk Mitigation

| Step | Risk | Mitigation |
|------|------|------------|
| T001 | Field name typo | Copy exact code from plan.md |
| T002 | Syntax error in Python | Verify indentation matches existing code |
| T004 | HF Space fails to restart | Check Space logs, retry restart |
| T007 | Chat still fails | Review browser network tab for actual error |

---

## Acceptance Criteria Mapping

| Requirement | Task | Verification |
|-------------|------|--------------|
| FR-001: Frontend sends `message` field | T001 | T007, T008 |
| FR-002: Backend preserves HTTP status codes | T002 | T009 |
| FR-003: Backend logs detailed errors | T002 | T010 |
| FR-004: HTTPException re-raised unchanged | T002 | T009 |
| FR-005: Validation returns 4xx codes | T002 | T009 |

---

## Notes

- [P] tasks = different files, no dependencies (T001 and T002 are parallel)
- [Story] label maps task to specific user story for traceability
- Manual testing is sufficient for this bug fix (no automated tests requested)
- HuggingFace Space restart is a manual step that cannot be automated
- Commit after each task for easy rollback if needed
