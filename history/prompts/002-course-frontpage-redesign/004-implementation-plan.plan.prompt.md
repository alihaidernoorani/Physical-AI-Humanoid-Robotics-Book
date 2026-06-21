---
id: 004
title: Implementation Plan for Frontpage Redesign
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-course-frontpage-redesign
branch: 002-course-frontpage-redesign
user: alihaidernoorani
command: /sp.plan
labels: ["plan", "architecture", "design-system", "ui-ux", "dark-mode"]
links:
  spec: specs/002-course-frontpage-redesign/spec.md
  plan: specs/002-course-frontpage-redesign/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-course-frontpage-redesign/plan.md
tests:
  - N/A (planning phase)
---

## Prompt

Context:
This project is a Docusaurus v3-based technical course book for a 13-week Physical AI & Humanoid Robotics program.
Core content and diagrams are now stable. The remaining work focuses on UI/UX quality, visual consistency, dark mode correctness, branding, and responsiveness.

Objective:
Define the final UI/UX architecture, design system decisions, component strategy, and implementation approach needed to resolve all remaining visual issues and deliver a polished, professional course experience.

[User provided detailed requirements for 8 areas:
1. Design System Architecture
2. Dark Mode Component Strategy
3. Frontpage Architecture
4. Module Card Design & Timeline Visualization
5. Branding & Identity
6. Responsive & Mobile Strategy
7. Accessibility & Quality Gates
8. Implementation Strategy]

## Response snapshot

Created comprehensive implementation plan covering:

**Design System Architecture**:
- Dark-mode-first color system using Infima CSS variables
- Surface hierarchy (background, surface-primary, surface-elevated)
- Module accent colors (4 modules with distinct colors)
- Typography system (modular scale 1.25, system font stack)
- Spacing scale (8px base unit)
- Border radius standards

**Component Specifications** (3 new components):
1. **HeroSection**: Course title + tagline + description with gradient background
2. **ModuleCard**: Clickable card with module info + timeline (props: moduleNumber, title, subtitle, description, weekStart/End, link, accentColor)
3. **TimelineBar**: Visual week range indicator (1-13 weeks) with ARIA roles

**Dark Mode Fixes** (visual-only):
- Quiz containers: Use theme surface colors
- Exercise blocks: Border + background contrast
- Callouts/admonitions: Readable backgrounds
- Interactive components: Visible borders/outlines

**Implementation Roadmap** (7 steps):
1. Design System Foundation (P0) - CSS tokens
2. Frontpage Components (P1) - Build 3 components
3. Frontpage Integration (P1) - Replace default index.tsx
4. Dark Mode Fixes (P2) - CSS overrides for quizzes/exercises
5. Branding Updates (P2) - Favicon + logos
6. Responsive & Accessibility Audit (P3) - Lighthouse + WCAG
7. Progressive Enhancement (P3) - Works without JS

**Technical Decisions**:
- CSS-first approach (no heavy JS frameworks)
- Progressive enhancement (hero/cards work without JS)
- Rollout order to minimize regressions
- Testing gates per step (Lighthouse, contrast, keyboard nav)

## Outcome

- ✅ Impact: Comprehensive 810-line plan defining complete architecture for frontpage redesign + dark mode fixes
- 🧪 Tests: Defined validation gates for each implementation step
- 📁 Files: Created plan.md with design system, component specs, implementation roadmap
- 🔁 Next prompts: Phase 0 research tasks can begin; then `/sp.tasks` to decompose roadmap into atomic tasks
- 🧠 Reflection: Plan balances modern design with accessibility, performance, and maintainability; CSS-first approach avoids bundle bloat

## Evaluation notes (flywheel)

- Failure modes observed: None - plan completed successfully
- Graders run and results (PASS/FAIL): Constitution check PASS (9/9), all requirements mapped to implementation steps
- Prompt variant (if applicable): Comprehensive architecture-first approach
- Next experiment (smallest change to try): Proceed to Phase 0 research, then task decomposition
