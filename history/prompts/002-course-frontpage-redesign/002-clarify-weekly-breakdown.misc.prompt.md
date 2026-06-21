---
id: 002
title: Clarify Course Weekly Breakdown and Module Structure
stage: misc
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-course-frontpage-redesign
branch: 002-course-frontpage-redesign
user: alihaidernoorani
command: /sp.clarify
labels: ["clarification", "course-structure", "modules", "weekly-breakdown"]
links:
  spec: specs/002-course-frontpage-redesign/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-course-frontpage-redesign/spec.md
tests:
  - N/A (clarification phase)
---

## Prompt

You are in the Clarify phase.

Goal:
Finalize and confirm the authoritative weekly breakdown for a 13-week Physical AI & Humanoid Robotics course so it can be used consistently across:
- Frontpage module cards
- Timeline indicators
- Module descriptions
- Navigation and summaries

[User provided detailed proposed weekly breakdown with 6 modules and clarification questions about:
1. Module title finality
2. Unity dependency status
3. Week 13 standalone vs integrated
4. Prerequisites display
5. Assessment milestone timing]

## Response snapshot

Conducted structured clarification session with 5 sequential questions:

**Q1: Module Structure**
- Resolved discrepancy between 4-module codebase structure vs proposed 6-module breakdown
- Answer: Keep existing 4-module structure aligned with current docs (ROS 2, Digital Twin, AI Brain, VLA)

**Q2: Module Titles**
- Confirmed finality of existing titles
- Answer: Titles are final — use as-is (no renaming)

**Q3: Unity Dependency**
- Clarified Unity's role in Module 2 (Digital Twin)
- Answer: Introductory only — not a core dependency (Gazebo is primary)

**Q4: Prerequisites Display**
- Determined whether to show prerequisites on frontpage cards
- Answer: No — sequential numbering implies order; details on module pages

**Q5: Assessment Milestones**
- Clarified whether assessments should appear on frontpage timeline
- Answer: No — assessments belong in module content, not frontpage overview

**Updated Spec Sections**:
- Added Clarifications section with session date and Q&A record
- Updated Assumptions with corrected 13-week distribution (Weeks 1-3, 4-6, 7-10, 11-13)
- Enhanced Key Entities with clarification context (titles final, no assessments on timeline)
- Updated Existing Content assumption to note Unity as introductory/optional

## Outcome

- ✅ Impact: Resolved 5 critical ambiguities that would have caused implementation conflicts
- 🧪 Tests: N/A (clarification phase)
- 📁 Files: Updated spec.md with clarifications section and refined assumptions
- 🔁 Next prompts: `/sp.plan` to generate implementation architecture
- 🧠 Reflection: Clarifications aligned proposed 6-module breakdown with existing 4-module codebase structure, preventing major restructuring work

## Evaluation notes (flywheel)

- Failure modes observed: None — all questions answered with recommended defaults
- Graders run and results (PASS/FAIL): 5/5 questions resolved successfully
- Prompt variant (if applicable): Sequential questioning with recommendations
- Next experiment (smallest change to try): Proceed to planning phase with clarified structure
