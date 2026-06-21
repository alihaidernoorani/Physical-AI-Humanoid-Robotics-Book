---
id: 005
title: Task Decomposition for Frontpage Redesign
stage: tasks
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-course-frontpage-redesign
branch: 002-course-frontpage-redesign
user: alihaidernoorani
command: /sp.tasks
labels: ["tasks", "decomposition", "implementation", "ui-ux"]
links:
  spec: specs/002-course-frontpage-redesign/spec.md
  plan: specs/002-course-frontpage-redesign/plan.md
  tasks: specs/002-course-frontpage-redesign/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-course-frontpage-redesign/tasks.md
tests:
  - N/A (task generation phase)
---

## Prompt

Context:
This project is a Docusaurus v3-based technical course book for a 13-week Physical AI & Humanoid Robotics program.
The architecture and design decisions have been finalized in the Plan phase.
The goal now is to break the UI/UX redesign into small, independent, testable tasks.

[User provided detailed task groups covering:
1. Design Tokens & Theme Foundations
2. Dark Mode Component Fixes
3. Frontpage Cleanup & Ownership
4. Frontpage Layout & Hero Section
5. Module Cards & Timeline Visualization
6. Responsive Behavior
7. Accessibility & Quality Checks
8. Performance & Regression Safety]

## Response snapshot

Generated consolidated task list with 55 tasks (reduced from initial 120) organized into 8 groups:

**GROUP 1: Design Tokens & Theme Foundations** (5 tasks)
- Define CSS variables for surface, color, typography, spacing, radius
- Define module accent colors (4 modules)
- Validate WCAG AA contrast ratios

**GROUP 2: Dark Mode Component Fixes** (7 tasks)
- Create dark-mode-fixes.css
- Fix quiz, exercise, callout, interactive component rendering
- Test internal content pages in dark mode

**GROUP 3: Frontpage Cleanup & Branding** (5 tasks)
- Remove default Docusaurus content
- Replace favicon and logos
- Update navbar and footer branding

**GROUP 4: Frontpage Layout & Hero Section (US1)** (5 tasks)
- Create HeroSection component with gradient background
- Implement responsive typography
- Integrate into frontpage

**GROUP 5: Module Cards & Timeline Visualization (US1, US5)** (9 tasks)
- Create ModuleCard and TimelineBar components
- Implement week range calculations
- Render 4-card grid with timelines

**GROUP 6: Module Card Interactions (US2)** (5 tasks)
- Add hover/focus animations (2-4px, 200ms)
- Verify navigation and keyboard accessibility
- Test screen reader announcements

**GROUP 7: Responsive Behavior (US4)** (5 tasks)
- Define responsive breakpoints and grid
- Scale typography for mobile
- Verify touch targets and viewport testing

**GROUP 8: Accessibility, Performance & Final Validation (US3)** (14 tasks)
- Validate theme switching and contrast
- Run Lighthouse audits (Performance ≥90, Accessibility ≥90)
- Test progressive enhancement, keyboard navigation
- Cross-browser and mobile device testing

**Task Organization**:
- 25 parallelizable tasks (45%)
- 30 sequential tasks (55%)
- Clear dependencies between groups
- MVP scope: Groups 1-5 (29 tasks)

## Outcome

- ✅ Impact: Generated 55-task implementation plan (down from 120) with clear checkpoints per group
- 🧪 Tests: Each group has acceptance criteria and verification tasks
- 📁 Files: Created tasks.md with 8 task groups mapped to 5 user stories
- 🔁 Next prompts: Begin implementation with Group 1 (Design Tokens), proceed through groups sequentially
- 🧠 Reflection: Consolidated tasks by combining verification steps, grouping related work, focusing on deliverables vs granular substeps

## Evaluation notes (flywheel)

- Failure modes observed: Initial task count too high (120 tasks); user requested consolidation
- Graders run and results (PASS/FAIL): Revised to 55 tasks (46% reduction) while maintaining atomic, testable units
- Prompt variant (if applicable): Consolidated approach - group related substeps, focus on checkpoints
- Next experiment (smallest change to try): Begin with Group 1 (5 tasks), validate approach before proceeding
