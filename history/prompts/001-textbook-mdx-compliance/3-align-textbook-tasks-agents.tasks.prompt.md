---
id: 3
title: align-textbook-tasks-agents
stage: tasks
date: 2025-12-14
surface: agent
model: Claude Sonnet 4.5
feature: 001-textbook-mdx-compliance
branch: 001-textbook-mdx-compliance
user: Claude Code
command: /sp.tasks
labels: [textbook, mdx, tasks, implementation, agents]
links:
  spec: /specs/001-textbook-mdx-compliance/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - /specs/001-textbook-mdx-compliance/tasks.md
tests:
 - null
---

## Prompt

Tasks:
- content-refinement:
  Refine existing chapter text for clarity, flow, and conciseness
  without altering technical correctness.

- chapter-refiner-skill:
  Normalize chapter structure and readability across all modules.

- link-integrity:
  Detect and fix broken internal links, routes, and anchors.

- mdx-syntax-fixer:
  Resolve MDX and Markdown syntax errors and build issues.

- frontpage-design:
  Improve frontpage / intro page UI/UX and ensure clear,
  correct linking to all four fixed modules.

Validation:
- Zero MDX build errors
- Zero broken links
- Sidebar matches file structure
- Frontpage links correctly route to all four modules
- Mobile-friendly, clean UI

## Response snapshot

Updated comprehensive implementation tasks for textbook MDX compliance feature to properly align with specialized agents. The tasks.md file now contains 45 targeted tasks organized across 6 phases with explicit agent utilization:

1. Phase 1: Setup Tasks (6 tasks) - Environment setup and agent verification
2. Phase 2: Foundational Tasks (6 tasks) - Core infrastructure for all user stories
3. Phase 3: User Story 1 - Content Refinement (12 tasks) - Priority P1 using content-refinement and chapter-refiner-skill agents
4. Phase 4: User Story 2 - Link Integrity (12 tasks) - Priority P2 using link-integrity agent
5. Phase 5: User Story 3 - MDX Syntax Compliance (9 tasks) - Priority P3 using mdx-syntax-fixer agent
6. Phase 6: Polish & Cross-Cutting Concerns (10 tasks) - Final validation using frontpage-design agent

Tasks follow the required checklist format with proper IDs, parallelization markers [P], and user story labels [US1], [US2], [US3]. Each phase now includes explicit "Agent Utilization" sections indicating which specialized agent to use. Dependencies and execution order are clearly defined, with parallel execution opportunities identified for module-level work using specialized agents. The MVP scope includes completing Phase 1, 2, and 3 for content refinement foundation.

## Outcome

- ✅ Impact: Task breakdown updated to align with specialized agents for textbook MDX compliance implementation
- 🧪 Tests: null
- 📁 Files: 1 updated tasks file in specs/001-textbook-mdx-compliance/tasks.md
- 🔁 Next prompts: Implementation can begin using the agent-aligned tasks
- 🧠 Reflection: Task generation updated to properly utilize content-refinement, chapter-refiner-skill, link-integrity, mdx-syntax-fixer, and frontpage-design agents

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation with Phase 1 tasks using specialized agents