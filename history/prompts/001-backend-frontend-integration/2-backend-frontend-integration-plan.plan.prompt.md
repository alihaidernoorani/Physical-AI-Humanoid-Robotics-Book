---
id: 2
title: backend-frontend-integration-plan
stage: plan
date: 2025-12-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-frontend-integration
branch: 001-backend-frontend-integration
user: Claude
command: sp.plan
labels: [plan, backend, frontend, integration, cleanup]
links:
  spec: specs/001-backend-frontend-integration/spec.md
  plan: specs/001-backend-frontend-integration/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-backend-frontend-integration/plan.md
 - specs/001-backend-frontend-integration/research.md
 - specs/001-backend-frontend-integration/data-model.md
 - specs/001-backend-frontend-integration/contracts/api-contracts.md
 - specs/001-backend-frontend-integration/quickstart.md
 - specs/001-backend-frontend-integration/tasks.md
tests:
 - null
---

## Prompt

Objective:
Create a detailed plan for backend cleanup (including deletion) and frontend ChatKit integration.

Backend Cleanup Tasks:
1. Delete legacy directories: src/, tests/
2. Delete duplicate files: main.py, src/config.py, CONFIGURATION.md, venv/
3. Archive ambiguous files: index_textbook.py, README.md, =1.24.3
4. Confirm core backend (app/main.py, app/agent.py, app/rag.py, app/chat.py, app/config.py) remains functional

Frontend Integration Tasks:
1. Define frontend folder structure for ChatKit components
2. Map backend API endpoints (/chat, /translate, /personalize) to UI components
3. Design UI/UX for chat, translation, and personalization
4. Add error handling and response validation in the frontend
5. Identify additional supporting files (assets, configs, styles)

Deliverables:
- tasks.md updated with backend cleanup and frontend integration tasks
- Mapping table of backend endpoints → frontend components
- Documentation for any archived or ambiguous files

Restrictions:
- Core backend files cannot be modified
- Do not implement frontend code yet
- Deletions will be performed only in `/sp.implement`

## Response snapshot

Created comprehensive implementation plan for backend-frontend integration including:
- Detailed implementation plan document
- Research summary with decision rationales
- Data model defining key entities
- API contracts for backend endpoints
- Quickstart guide for setup
- Tasks breakdown with priorities and acceptance criteria

## Outcome

- ✅ Impact: Complete planning artifacts created for backend cleanup and ChatKit frontend integration
- 🧪 Tests: null
- 📁 Files: specs/001-backend-frontend-integration/plan.md, research.md, data-model.md, contracts/api-contracts.md, quickstart.md, tasks.md
- 🔁 Next prompts: /sp.tasks to generate additional tasks if needed
- 🧠 Reflection: Plan thoroughly addresses both backend cleanup and frontend integration with clear task breakdown and dependencies

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null