# Implementation Tasks: textbook-mdx-compliance

**Feature**: textbook-mdx-compliance | **Date**: 2025-12-15 | **Plan**: [specs/001-textbook-mdx-compliance/plan.md](specs/001-textbook-mdx-compliance/plan.md)

**Note**: This template is filled in by the `/sp.tasks` command. See `.specify/templates/commands/tasks.md` for the execution workflow.

## Task Generation Summary

- **Total Tasks**: 84
- **User Story Tasks**: 76 (US1: 8, US2: 32, US3: 8, US4: 8)
- **Setup & Foundational Tasks**: 8
- **Parallel Opportunities**: Chapter-level tasks can be executed in parallel using specialized agents
- **MVP Scope**: User Story 1 (Inventory and Safety Audit) provides foundational compliance verification
- **Specialized Agents**: Explore, mdx-syntax-fixer, link-integrity, content-refinement

## Dependencies & Execution Order

- **Setup Phase**: Must complete before any user stories
- **Foundational Phase**: Must complete before user stories
- **User Stories**: Can be implemented in parallel after foundational tasks using specialized agents
- **Polish Phase**: Final validation and cross-cutting concerns

## Parallel Execution Examples

- All chapter MDX audits can run in parallel
- All chapter rewrites can run in parallel
- All chapter content refinements can run in parallel across modules
- All chapter formatting standardizations can run in parallel
- All module link validations can run in parallel

---

## Phase 1: Setup Tasks

### Goal
Initialize project environment and inventory existing content structure

- [X] T001 Create backup of original content files before modifications in backup/ directory
- [X] T002 Identify all existing .md and .mdx files in docs/ directory for inventory
- [X] T003 [P] Create inventory of Module 1 chapters (docs/ros2-nervous-system/*.mdx)
- [X] T004 [P] Create inventory of Module 2 chapters (docs/digital-twin/*.mdx)
- [X] T005 [P] Create inventory of Module 3 chapters (docs/ai-robot-brain/*.mdx)
- [X] T006 [P] Create inventory of Module 4 chapters (docs/vla/*.mdx)
- [X] T007 [P] Document module names, order, and hierarchy to ensure preservation
- [X] T008 Verify Docusaurus build process works with current content (baseline)

---

## Phase 2: Foundational Tasks

### Goal
Establish core MDX safety and audit infrastructure needed by all user stories

- [X] T009 [P] Configure MDX linting rules to detect JSX-breaking syntax
- [X] T010 [P] Set up automated MDX syntax validation tooling
- [X] T011 [P] Create MDX compliance checklist based on constitutional requirements
- [X] T012 [P] Establish content verification workflow for technical accuracy
- [X] T013 [P] Set up link validation tooling for broken link detection
- [X] T014 [P] Create backup and restore procedures for content files
- [X] T015 [P] Document existing module structure to ensure preservation during rewrite
- [X] T016 Establish baseline Docusaurus build validation process

---

## Phase 3: User Story 1 - Inventory and MDX Safety Audit (Priority: P1) 🎯 MVP

### Goal
As a content maintainer, I want to create a complete inventory of all textbook chapters and audit them for MDX and JSX failure risks so that I can identify all compliance issues before making changes.

### Independent Test Criteria
Can be fully tested by reviewing the complete inventory and safety audit reports to confirm all chapters are catalogued and all MDX risks are identified.

- [X] T017 [P] [US1] Perform MDX safety audit on Module 1 Chapter 1: docs/ros2-nervous-system/01-ros2-nodes.mdx
- [X] T018 [P] [US1] Perform MDX safety audit on Module 1 Chapter 2: docs/ros2-nervous-system/02-ros2-topics-services-actions.mdx
- [X] T019 [P] [US1] Perform MDX safety audit on Module 1 Chapter 3: docs/ros2-nervous-system/03-writing-ros2-agents-python.mdx
- [X] T020 [P] [US1] Perform MDX safety audit on Module 1 Chapter 4: docs/ros2-nervous-system/04-urdf-kinematic-modeling.mdx
- [X] T021 [P] [US1] Perform MDX safety audit on Module 1 Chapter 5: docs/ros2-nervous-system/05-lifecycle-nodes-composition.mdx
- [X] T022 [P] [US1] Perform MDX safety audit on Module 1 Intro: docs/ros2-nervous-system/intro.mdx
- [X] T023 [P] [US1] Create comprehensive inventory document with all identified MDX risks
- [X] T024 [P] [US1] Validate inventory completeness against existing file structure

---

## Phase 4: User Story 2 - Chapter Rewrite and Refinement (Priority: P2)

### Goal
As a student reading the Physical AI & Humanoid Robotics textbook, I want to access refined chapter content with improved clarity, narrative flow, and pedagogical quality while preserving all original technical meaning.

### Independent Test Criteria
Can be fully tested by reviewing chapter content for improved clarity, flow, and pedagogical quality while ensuring technical accuracy remains intact.

- [X] T025 [P] [US2] Rewrite Module 1 Chapter 1 for clarity and flow: docs/ros2-nervous-system/01-ros2-nodes.mdx
- [X] T026 [P] [US2] Rewrite Module 1 Chapter 2 for clarity and flow: docs/ros2-nervous-system/02-ros2-topics-services-actions.mdx
- [X] T027 [P] [US2] Rewrite Module 1 Chapter 3 for clarity and flow: docs/ros2-nervous-system/03-writing-ros2-agents-python.mdx
- [X] T028 [P] [US2] Rewrite Module 1 Chapter 4 for clarity and flow: docs/ros2-nervous-system/04-urdf-kinematic-modeling.mdx
- [X] T029 [P] [US2] Rewrite Module 1 Chapter 5 for clarity and flow: docs/ros2-nervous-system/05-lifecycle-nodes-composition.mdx
- [X] T030 [P] [US2] Rewrite Module 1 Intro for clarity and flow: docs/ros2-nervous-system/intro.mdx
- [X] T031 [P] [US2] Add pedagogical explanations and smooth transitions to Module 1 content
- [X] T032 [P] [US2] Verify technical accuracy preservation in Module 1 rewrites

### Phase 4.5: User Story 2 - Module 2 Content Refinement and Citation Removal (Priority: P2)
### Goal
Complete content refinement for Module 2 chapters to improve clarity, narrative flow, and pedagogical quality while preserving all original technical meaning and removing reader-facing references.

### Independent Test Criteria
Can be fully tested by reviewing Module 2 chapter content for improved clarity, flow, and pedagogical quality while ensuring technical accuracy remains intact and no reader-facing references exist.

- [X] T061 [P] [US2] Rewrite Module 2 Chapter 1 for clarity and flow: docs/digital-twin/01-rigid-body-dynamics-gazebo.mdx
- [X] T062 [P] [US2] Rewrite Module 2 Chapter 2 for clarity and flow: docs/digital-twin/02-sensor-simulation.mdx
- [X] T063 [P] [US2] Rewrite Module 2 Chapter 3 for clarity and flow: docs/digital-twin/03-unity-high-fidelity-env.mdx
- [X] T064 [P] [US2] Rewrite Module 2 Chapter 4 for clarity and flow: docs/digital-twin/04-synchronizing-gazebo-unity.mdx
- [X] T065 [P] [US2] Rewrite Module 2 Intro for clarity and flow: docs/digital-twin/intro.mdx
- [X] T066 [P] [US2] Remove external references from Module 2 content and internally verify factual claims
- [X] T067 [P] [US2] Add pedagogical explanations and smooth transitions to Module 2 content
- [X] T068 [P] [US2] Verify technical accuracy preservation in Module 2 rewrites

### Phase 4.6: User Story 2 - Module 3 Content Refinement and Citation Removal (Priority: P2)
### Goal
Complete content refinement for Module 3 chapters to improve clarity, narrative flow, and pedagogical quality while preserving all original technical meaning and removing reader-facing references.

### Independent Test Criteria
Can be fully tested by reviewing Module 3 chapter content for improved clarity, flow, and pedagogical quality while ensuring technical accuracy remains intact and no reader-facing references exist.

- [X] T069 [P] [US2] Rewrite Module 3 Chapter 1 for clarity and flow: docs/ai-robot-brain/01-synthetic-data-generation.mdx
- [X] T070 [P] [US2] Rewrite Module 3 Chapter 2 for clarity and flow: docs/ai-robot-brain/02-isaac-ros-gems.mdx
- [X] T071 [P] [US2] Rewrite Module 3 Chapter 3 for clarity and flow: docs/ai-robot-brain/03-nav2-bipedal-navigation.mdx
- [X] T072 [P] [US2] Rewrite Module 3 Chapter 4 for clarity and flow: docs/ai-robot-brain/04-edge-inference-jetson.mdx
- [X] T073 [P] [US2] Rewrite Module 3 Intro for clarity and flow: docs/ai-robot-brain/intro.mdx
- [X] T074 [P] [US2] Remove external references from Module 3 content and internally verify factual claims
- [X] T075 [P] [US2] Add pedagogical explanations and smooth transitions to Module 3 content
- [X] T076 [P] [US2] Verify technical accuracy preservation in Module 3 rewrites

### Phase 4.7: User Story 2 - Module 4 Content Refinement and Citation Removal (Priority: P2)
### Goal
Complete content refinement for Module 4 chapters to improve clarity, narrative flow, and pedagogical quality while preserving all original technical meaning and removing reader-facing references.

### Independent Test Criteria
Can be fully tested by reviewing Module 4 chapter content for improved clarity, flow, and pedagogical quality while ensuring technical accuracy remains intact and no reader-facing references exist.

- [X] T077 [P] [US2] Rewrite Module 4 Chapter 1 for clarity and flow: docs/vla/01-voice-to-text-whisper.mdx
- [X] T078 [P] [US2] Rewrite Module 4 Chapter 2 for clarity and flow: docs/vla/02-llm-task-decomposition.mdx
- [X] T079 [P] [US2] Rewrite Module 4 Chapter 3 for clarity and flow: docs/vla/03-grounding-language-ros2.mdx
- [X] T080 [P] [US2] Rewrite Module 4 Chapter 4 for clarity and flow: docs/vla/04-capstone-end-to-end.mdx
- [X] T081 [P] [US2] Rewrite Module 4 Intro for clarity and flow: docs/vla/intro.mdx
- [X] T082 [P] [US2] Remove external references from Module 4 content and internally verify factual claims
- [X] T083 [P] [US2] Add pedagogical explanations and smooth transitions to Module 4 content
- [X] T084 [P] [US2] Verify technical accuracy preservation in Module 4 rewrites

---

## Phase 5: User Story 3 - Citation Removal and Content Standardization (Priority: P3)

### Goal
As a student reading the Physical AI & Humanoid Robotics textbook, I want to access content without distracting external references so that I can focus on learning without interruption from reader-facing citations.

### Independent Test Criteria
Can be fully tested by reviewing chapters to ensure all reader-facing external references, citations, and bibliographies have been removed.

- [X] T033 [P] [US3] Remove external references from Module 2 Chapter 1: docs/digital-twin/01-rigid-body-dynamics-gazebo.mdx
- [X] T034 [P] [US3] Remove external references from Module 2 Chapter 2: docs/digital-twin/02-sensor-simulation.mdx
- [X] T035 [P] [US3] Remove external references from Module 2 Chapter 3: docs/digital-twin/03-unity-high-fidelity-env.mdx
- [X] T036 [P] [US3] Remove external references from Module 2 Chapter 4: docs/digital-twin/04-synchronizing-gazebo-unity.mdx
- [X] T037 [P] [US3] Remove external references from Module 2 Intro: docs/digital-twin/intro.mdx
- [X] T038 [P] [US3] Internally verify factual claims in Module 2 content against reliable sources
- [X] T039 [P] [US3] Standardize Module 2 content formatting to pure Markdown
- [X] T040 [P] [US3] Validate citation removal and technical accuracy in Module 2

---

## Phase 6: User Story 4 - MDX-Safe Formatting and Validation (Priority: P4)

### Goal
As a content publisher, I want to ensure all chapters follow MDX-safe formatting standards so that the Docusaurus build completes successfully with zero MDX or JSX errors.

### Independent Test Criteria
Can be fully tested by running Docusaurus build to ensure zero syntax errors and proper rendering of all content.

- [X] T041 [P] [US4] Apply MDX-safe formatting to Module 3 Chapter 1: docs/ai-robot-brain/01-synthetic-data-generation.mdx
- [X] T042 [P] [US4] Apply MDX-safe formatting to Module 3 Chapter 2: docs/ai-robot-brain/02-isaac-ros-gems.mdx
- [X] T043 [P] [US4] Apply MDX-safe formatting to Module 3 Chapter 3: docs/ai-robot-brain/03-nav2-bipedal-navigation.mdx
- [X] T044 [P] [US4] Apply MDX-safe formatting to Module 3 Chapter 4: docs/ai-robot-brain/04-edge-inference-jetson.mdx
- [X] T045 [P] [US4] Apply MDX-safe formatting to Module 3 Intro: docs/ai-robot-brain/intro.mdx
- [X] T046 [P] [US4] Apply MDX-safe formatting to Module 4 chapters: docs/vla/*.mdx
- [X] T047 [P] [US4] Standardize heading hierarchy and code blocks across all chapters
- [X] T048 [P] [US4] Eliminate JSX-triggering syntax in all MDX files

---

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Final validation, link integrity, and comprehensive testing across all modules

- [X] T049 [P] Verify all module names, order, and hierarchy remain unchanged
- [X] T050 [P] Run link-integrity validation across Module 1 chapters
- [X] T051 [P] Run link-integrity validation across Module 2 chapters
- [X] T052 [P] Run link-integrity validation across Module 3 chapters
- [X] T053 [P] Run link-integrity validation across Module 4 chapters
- [X] T054 [P] Cross-check completed chapters against initial inventory
- [X] T055 [P] Review all chapters for consistent terminology and tone
- [X] T056 Run final Docusaurus build to validate zero MDX/JSX errors and warnings
- [X] T057 Run comprehensive broken-link validation across entire textbook
- [X] T058 Final verification that build completes with zero errors and zero warnings
- [X] T059 Validate module structure compliance with constitutional requirements
- [X] T060 Final content quality review across all chapters

---

## Implementation Strategy

### MVP First Approach
1. Complete Phase 1-2: Setup and foundational tasks (T001-T016)
2. Focus on User Story 1 (P1): Inventory and safety audit (T017-T024)
3. This provides foundational compliance verification before proceeding
4. Content rewriting for Module 1 already completed (User Story 2: T025-T032)
5. Follow with citation removal and standardization (User Story 3: T033-T040)
6. Complete with MDX-safe formatting (User Story 4: T041-T048)
7. Add content refinement for remaining modules (Phase 4.5: T061-T068, Phase 4.6: T069-T076, Phase 4.7: T077-T084)
8. End with comprehensive validation (Phase 7: T049-T060)

### Incremental Delivery
- **MVP**: Complete Phase 1, 2, and 3 (T001-T024) - Provides complete inventory and safety audit
- **Phase 2**: Phase 4 already completed - Module 1 refined content (T025-T032)
- **Phase 3**: Complete Phase 5 (T033-T040) - Provides citation-free Module 2 content
- **Phase 4**: Complete Phase 6 (T041-T048) - Provides MDX-safe formatting for remaining modules
- **Phase 5**: Complete Phase 4.5 (T061-T068) - Provides refined content for Module 2
- **Phase 6**: Complete Phase 4.6 (T069-T076) - Provides refined content for Module 3
- **Phase 7**: Complete Phase 4.7 (T077-T084) - Provides refined content for Module 4
- **Final**: Complete Phase 7 (T049-T060) - Full validation and compliance verification