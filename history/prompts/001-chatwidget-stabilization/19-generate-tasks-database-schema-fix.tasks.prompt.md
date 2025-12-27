---
id: 19
title: Generate tasks for database schema fix
stage: tasks
date_iso: 2025-12-27
surface: agent
model: claude-sonnet-4.5
feature: 001-chatwidget-stabilization
branch: 001-chatwidget-stabilization
user: Claude Sonnet 4.5
command: sp.tasks
labels:
  - database
  - schema
  - neon-postgres
  - migration
  - tasks
links:
  spec: specs/001-chatwidget-stabilization/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-chatwidget-stabilization/tasks.md
tests_yaml: |
  - T052: Schema verification queries
  - T053: Session creation API test
  - T057: Full chat flow test
outcome: |
  Successfully generated 19 new tasks (T047-T065) for Phase 11: Database
  Schema Alignment. Tasks organized into Critical, Verification, Restart,
  and Optional Hardening categories.
evaluation: |
  Tasks are small, actionable, and verifiable. Includes SQL migration
  scripts and verification queries inline for immediate executability.
---

# Prompt History Record: Generate tasks for database schema fix

## Original Prompt

Based on the approved plan, create a step-by-step task list to fully resolve the ChatKit session failure caused by Postgres schema issues.

Tasks must include:
- Database schema alignment for the conversations table
- Handling of updated_at expectations
- Restart and verification steps on Hugging Face Spaces
- Optional hardening steps to prevent DB failures from breaking chat sessions in the future

Each task should be:
- Small
- Actionable
- Verifiable

Output format:
- Markdown task list
- Ordered from critical to optional

## Implementation Response

### Tasks Generated

Added **Phase 11: Database Schema Alignment - Neon Postgres** to tasks.md with 19 new tasks:

#### Critical Tasks (T047-T052) - 6 tasks
- Schema migration SQL execution in Neon console
- Table and column verification

#### Verification Tasks (T053-T057) - 5 tasks
- API endpoint testing
- Backend log verification
- End-to-end chat flow testing

#### Restart and Deployment Tasks (T058-T060) - 3 tasks
- Hugging Face Spaces restart
- Frontend cache clear
- Live deployment verification

#### Optional Hardening Tasks (T061-T065) - 5 tasks [Parallelizable]
- Schema validation at startup
- Connection health check
- Graceful error handling
- Reproducible schema script
- Documentation updates

### Summary

| Category | Task Range | Count | Status |
|----------|------------|-------|--------|
| Critical | T047-T052 | 6 | Pending |
| Verification | T053-T057 | 5 | Pending |
| Restart | T058-T060 | 3 | Pending |
| Hardening | T061-T065 | 5 | Pending (Optional) |
| **Total** | T047-T065 | **19** | |

### Parallel Opportunities

- T061-T065 can all run in parallel (different files, no dependencies)
- T047-T048 can run in parallel (different ALTER TABLE statements)

### MVP Scope

Complete T047-T060 (14 tasks) for immediate fix. T061-T065 are recommended but optional for production stability.
