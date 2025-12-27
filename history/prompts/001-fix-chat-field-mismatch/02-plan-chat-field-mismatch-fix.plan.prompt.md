---
id: 02
title: Plan Chat Field Mismatch Fix
stage: plan
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-fix-chat-field-mismatch
branch: 001-fix-chat-field-mismatch
user: developer
command: /sp.plan
labels: [bug-fix, chat, api, planning, implementation-plan]
links:
  spec: specs/001-fix-chat-field-mismatch/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fix-chat-field-mismatch/plan.md
  - specs/001-fix-chat-field-mismatch/research.md
  - specs/001-fix-chat-field-mismatch/data-model.md
  - specs/001-fix-chat-field-mismatch/quickstart.md
  - specs/001-fix-chat-field-mismatch/contracts/chat-api.yaml
tests:
  - N/A (planning phase)
---

## Prompt

- Task 1: Update frontend ChatKit.tsx field name from "query" → "message"
- Task 2: Update backend chat.py exception handling to pass-through HTTPExceptions
- Task 3: Manually restart HuggingFace backend Space
- Task 4: Test sending a chat message via frontend
- Task 5: Confirm assistant replies appear, no 500 errors in logs

## Response snapshot

Created comprehensive implementation plan for the chat API field mismatch bug fix. Key artifacts generated:

**Phase 0 - Research (research.md)**:
- Confirmed field mismatch: frontend sends `query`, backend expects `message`
- Identified exception handling issue: all errors converted to 500
- Decision: change frontend (not backend) to align with existing API contract

**Phase 1 - Design & Contracts**:
- `data-model.md`: Documented ChatMessageRequest/Response schemas
- `contracts/chat-api.yaml`: OpenAPI 3.0 specification for /chat endpoint
- `quickstart.md`: Step-by-step implementation guide

**Implementation Plan (plan.md)**:
- Task 1: Frontend fix at ChatKit.tsx:124-126 (query → message)
- Task 2: Backend fix at chat.py:108-113 (add HTTPException pass-through)
- Task 3-5: Deployment and verification steps

**Constitution Check**: PASSED - No violations, minimal targeted changes

## Outcome

- Impact: Complete planning artifacts ready for task generation
- Tests: N/A (planning phase - no tests yet)
- Files: plan.md, research.md, data-model.md, quickstart.md, contracts/chat-api.yaml
- Next prompts: /sp.tasks to generate actionable task list
- Reflection: Simple bug fix with well-defined scope; code inspection revealed exact line numbers for changes

## Evaluation notes (flywheel)

- Failure modes observed: None - clear requirements with specific code references
- Graders run and results (PASS/FAIL): Constitution check - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks for implementation task generation
