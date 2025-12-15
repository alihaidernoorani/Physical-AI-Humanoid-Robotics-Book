---
id: 3
title: recreate-implementation-plan
stage: plan
date: 2025-12-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-textbook-mdx-compliance
branch: 001-textbook-mdx-compliance
user: unknown
command: /sp.plan
labels: [plan, mdx, textbook, compliance, recreation]
links:
  spec: specs/001-textbook-mdx-compliance/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-textbook-mdx-compliance/plan.md
  - specs/001-textbook-mdx-compliance/research.md
  - specs/001-textbook-mdx-compliance/data-model.md
  - specs/001-textbook-mdx-compliance/quickstart.md
  - specs/001-textbook-mdx-compliance/contracts/
tests:
  - npm run build (validation)
---

## Prompt

Project: Physical AI & Humanoid Robotics Textbook
Phase 1: Content, Navigation, MDX Migration & Interactive Frontend

Objective:
Update the existing textbook to comply with the constitution by:
- Migrating all chapters from .md → .mdx
- Adding interactive components (Urdu/English toggles, callouts, quizzes)
- Improving chapter content quality
- Fixing internal links
- Ensuring a clear frontpage with all modules

---

## Subagents & Skills

1. **MDXMigrationAgent**
   - **Skills:**
     - `convert_to_mdx(chapter_file)`: Converts any .md file to .mdx while preserving routes, slugs, titles
     - `validate_mdx_structure(chapter_file)`: Ensures MDX files are ready for React components
   - **Responsibilities:**
     - Convert all chapters in all modules to MDX
     - Ensure file structure, slugs, and titles remain intact

2. **ToggleAgent**
   - **Skills:**
     - `add_toggle_button(chapter_file, languages=["English","Urdu"])`: Adds a frontend toggle
     - `verify_toggle_render(chapter_file)`: Confirms toggle renders properly
   - **Responsibilities:**
     - Add Urdu/English toggles to all chapters
     - Ensure toggles are functional and visible

3. **ContentWriterAgent**
   - **Skills:**
     - `refine_text(chapter_file)`: Improves clarity and pedagogical quality
     - `add_exercise(chapter_file)`: Inserts exercises
     - `add_diagram(chapter_file)`: Adds diagrams
     - `add_quiz(chapter_file)`: Inserts MCQs and answers
     - `add_glossary_entry(term, definition)`: Updates glossary
   - **Responsibilities:**
     - Refine and complete all chapter content
     - Ensure technical correctness, clarity, and consistency

4. **LinkCheckerAgent**
   - **Skills:**
     - `verify_links(chapter_file)`: Checks internal links, images, diagrams
     - `fix_broken_links(chapter_file)`: Corrects any broken references
   - **Responsibilities:**
     - Scan all chapters for broken or missing links
     - Ensure Docusaurus build has zero warnings

5. **FrontpageDesignAgent**
   - **Skills:**
     - `update_module_cards(frontpage_file)`: Ensures correct module links and layout
     - `verify_frontpage(frontpage_file)`: Confirms all modules are visible and clickable
   - **Responsibilities:**
     - Update homepage to clearly show all four modules
     - Ensure module names match the constitution exactly

---

## Task Sequence

1. **MDX Migration**
   - MDXMigrationAgent converts all chapters to .mdx
   - Validate routes, slugs, and titles

2. **Toggle Addition**
   - ToggleAgent inserts Urdu/English toggles in all chapters
   - Verify toggle rendering

3. **Content Refinement**
   - ContentWriterAgent refines text and adds exercises, quizzes, diagrams, glossary entries
   - Ensure content aligns with robotics fundamentals and outline

4. **Link Verification**
   - LinkCheckerAgent scans for broken links
   - Fix any broken references
   - Confirm Docusaurus build passes without warnings

5. **Frontpage Update**
   - FrontpageDesignAgent updates homepage module cards
   - Confirm links navigate to correct module entry pages

6. **Validation**
   - Manual + automated verification:
     - Docusaurus build passes with zero warnings
     - Sidebar matches folder structure
     - No 404 errors
     - Toggle buttons functional on all chapters
     - Frontpage provides clear access to all modules

---

## Execution Rules

- Phase 1 focuses only on frontend, content, navigation, and MDX migration
- Backend (RAG, API, translation) is deferred to Phase 2
- Constitution takes precedence over existing content if conflicts occur
- Pause execution and report any missing or unclear information

End of /sp.plan

## Response snapshot

# Implementation Plan: textbook-mdx-compliance

**Branch**: `001-textbook-mdx-compliance` | **Date**: 2025-12-14 | **Spec**: [specs/001-textbook-mdx-compliance/spec.md](specs/001-textbook-mdx-compliance/spec.md)
**Input**: Feature specification from `/specs/001-textbook-mdx-compliance/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Update the existing Physical AI & Humanoid Robotics textbook to comply with the constitution by migrating .md files to .mdx where interactive components are required, improving chapter content quality, fixing broken links, ensuring proper frontpage navigation, and adding missing Urdu/English toggle controls. The implementation will maintain the locked module structure while enhancing the educational value and technical compliance of the textbook.

## Technical Context

**Language/Version**: JavaScript/TypeScript, Node.js 18+
**Primary Dependencies**: Docusaurus v3.9.2, React, MDX, Node.js
**Storage**: File-based (Markdown/MDX files in docs/ directory)
**Testing**: Manual verification and Docusaurus build validation
**Target Platform**: Web-based documentation site (GitHub Pages)
**Project Type**: Web documentation site
**Performance Goals**: Fast page load times, responsive interactive components
**Constraints**: Must maintain existing URLs and navigation structure, zero build warnings
**Scale/Scope**: Four modules with multiple chapters each, supporting Urdu/English toggles

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Scientific Accuracy: All technical claims must be verifiable and traceable to reputable sources
- Academic Clarity: Content must be written for undergraduate-level audience with proper terminology definitions
- Reproducibility & Transparency: All methods and algorithms must be presented with sufficient detail for reproduction
- Ethical & Safety Awareness: All content must address ethical implications and safety constraints
- Module Structure Compliance: All content must follow the fixed 4-module structure (The Robotic Nervous System (ROS 2), The Digital Twin (Gazebo & Unity), The AI-Robot Brain (NVIDIA Isaac™), Vision-Language-Action (VLA))
- Frontend Architecture: Must implement Docusaurus-based frontend with interactive module cards, glossary, quizzes, and reusable MDX components
- Personalization & Translation: Urdu toggle and personalization must function on every chapter
- Change Control: Module names, structure, and hierarchy are immutable - no autonomous scope expansion allowed

## Project Structure

### Documentation (this feature)

```text
specs/001-textbook-mdx-compliance/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
textbook-physical-ai/
├── docs/
│   ├── intro.md
│   ├── tutorial-basics/
│   │   ├── _category_.json
│   │   ├── create-a-document.md
│   │   ├── create-a-page.md
│   │   ├── create-a-blog-post.md
│   │   ├── deploy-your-site.md
│   │   └── markdown-features.mdx
│   └── tutorial-extras/
│       ├── _category_.json
│       └── manage-docs-versions.md
├── src/
│   ├── components/
│   ├── pages/
│   └── css/
├── static/
├── docusaurus.config.js
├── sidebars.js
└── package.json
```

**Structure Decision**: The existing Docusaurus project structure will be used with updates to MD/MDX files in the docs/ directory and potential component updates in src/components/ for interactive elements.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None identified] | [N/A] | [N/A] |

## Research & Design Phase Completion

The planning process has completed both Phase 0 (Research) and Phase 1 (Design) as required:

- Created `research.md` with analysis of MDX migration strategy, frontend technology stack, module structure compliance, link verification approach, and Urdu/English toggle implementation
- Created `data-model.md` describing content entities, relationships, and validation rules
- Created `quickstart.md` with essential steps for implementation
- Created `contracts/` directory to store API contracts and interface definitions
- Updated agent context with project-specific information

## Subagent Implementation Strategy

The implementation will follow the subagent responsibilities defined in the specification:
1. MDXMigrationAgent - Handles file format conversions
2. ToggleAgent - Adds language toggle functionality
3. ContentWriterAgent - Improves content quality
4. LinkCheckerAgent - Verifies all internal links
5. FrontpageDesignAgent - Updates homepage layout

## Validation Criteria

- Docusaurus build completes with zero broken link warnings
- All interactive components function correctly
- Frontpage provides clear access to all four modules
- Content maintains technical accuracy and academic clarity
- Navigation structure matches file structure

## Execution Rules Compliance

- Phase 1 focuses only on frontend, content, navigation, and MDX migration (as specified)
- Backend implementation deferred to Phase 2 (as specified)
- Constitution requirements prioritized over existing content (as specified)
- Module names remain unchanged as required by constitution

## Architectural Decision Record Suggestion

📋 Architectural decision detected: Selection of MDX for interactive components - Document reasoning and tradeoffs? Run `/sp.adr MDX-selection-for-interactive-components`

## Ready for Task Generation

The planning phase is complete and ready for the next step: task generation using `/sp.tasks`.

## Outcome

- ✅ Impact: Created comprehensive implementation plan with research, data model, quickstart guide, and contracts directory for textbook MDX compliance update
- 🧪 Tests: Docusaurus build validation planned as part of implementation
- 📁 Files: Created/updated plan.md, research.md, data-model.md, quickstart.md, and contracts/ directory
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Planning phase successfully completed with all design artifacts created and agent context updated
- 📋 ADR: Suggested architectural decision record for MDX selection

## Evaluation notes (flywheel)

- Failure modes observed: None identified during planning phase
- Graders run and results (PASS/FAIL): All constitution checks passed
- Prompt variant (if applicable): Standard /sp.plan workflow followed
- Next experiment (smallest change to try): Execute /sp.tasks to generate implementation tasks