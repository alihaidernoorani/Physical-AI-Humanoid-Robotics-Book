---
id: 01
title: Specify Chat Field Mismatch Fix
stage: spec
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-fix-chat-field-mismatch
branch: 001-fix-chat-field-mismatch
user: developer
command: /sp.specify
labels: [bug-fix, chat, api, field-mismatch, error-handling]
links:
  spec: specs/001-fix-chat-field-mismatch/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fix-chat-field-mismatch/spec.md
  - specs/001-fix-chat-field-mismatch/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

- Target: Frontend ChatKit.tsx
- Lines: 124-126
- Change: Rename field "query" to "message" in chatService.sendMessage call
- Reason: Backend expects "message"; "query" causes 400 → 500 error

- Target: Backend chat.py
- Lines: 108-113 (chat_endpoint exception handling)
- Change:
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
- Reason: Preserve original HTTPExceptions like 400 instead of converting to 500

- Note: After implementing backend changes, restart the HuggingFace Space manually to apply updates.

## Response snapshot

Created feature branch `001-fix-chat-field-mismatch` and comprehensive specification for fixing the chat API field mismatch bug. The spec covers:

1. **Problem Statement**: Identified two related issues - field name mismatch (query vs message) and error masking (400→500 conversion)

2. **User Stories**:
   - P1: Successful chat message transmission (core broken functionality)
   - P2: Meaningful error messages for debugging

3. **Functional Requirements**: 5 requirements covering field naming, error preservation, logging, and validation

4. **Success Criteria**: Measurable outcomes including 100% success rate for valid messages and zero field mismatch errors

5. **Quality Checklist**: All items passed - spec is ready for planning phase

## Outcome

- Impact: Created complete feature specification for targeted bug fix
- Tests: N/A (specification phase - no tests yet)
- Files: spec.md, checklists/requirements.md created
- Next prompts: /sp.clarify (if clarification needed) or /sp.plan (to generate implementation plan)
- Reflection: Clean, focused bug fix spec with clear scope boundaries and testable acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: None - clear user requirements with specific file/line references
- Graders run and results (PASS/FAIL): Manual checklist review - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.plan for implementation planning
