---
id: 1
title: backend-frontend-integration-spec
stage: spec
date: 2025-12-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-frontend-integration
branch: 001-backend-frontend-integration
user: Claude
command: sp.specify
labels: [spec, backend, frontend, integration]
links:
  spec: specs/001-backend-frontend-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-backend-frontend-integration/spec.md
 - specs/001-backend-frontend-integration/checklists/requirements.md
tests:
 - null
---

## Prompt

Objective:
Define the scope and rules for safely cleaning up legacy backend files and integrating the frontend ChatKit UI.

Scope:
- Backend:
  - Remove legacy or duplicate files identified in the audit report (src/, tests/, main.py, src/config.py, CONFIGURATION.md, venv/)
  - Keep core 5-file backend intact (app/main.py, app/agent.py, app/rag.py, app/chat.py, app/config.py)
  - Archive any ambiguous files (index_textbook.py, README.md, =1.24.3) until confirmed safe
  - Ensure API endpoints remain functional

- Frontend:
  - Implement ChatKit UI
  - Connect frontend to backend API endpoints (/chat, /translate, /personalize)
  - Ensure end-to-end functionality and proper UI/UX

Rules:
1. Files marked as "safe to delete" in the audit may be removed during `/sp.implement`.
2. Files flagged as "review" must be archived or manually approved before deletion.
3. Core backend files cannot be altered.
4. Frontend must consume backend APIs correctly.
5. All tasks must be documented in tasks.md.
6. No new backend features will be added in this phase.

Output:
- Confirmation of scope and rules
- Ready state for planning tasks, including deletion and frontend integration

## Response snapshot

Created specification for backend-frontend integration feature that covers:
- Legacy file cleanup with proper safety measures
- ChatKit UI implementation
- Backend-frontend API connection
- All requirements properly documented with measurable success criteria

## Outcome

- ✅ Impact: Specification created for backend-frontend integration including legacy file cleanup and ChatKit UI implementation
- 🧪 Tests: null
- 📁 Files: specs/001-backend-frontend-integration/spec.md, specs/001-backend-frontend-integration/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Specification clearly defines scope for both backend cleanup and frontend integration with proper priorities and acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null