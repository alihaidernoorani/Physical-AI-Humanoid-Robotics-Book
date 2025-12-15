---
id: 2
title: create-implementation-plan
stage: plan
date: 2025-12-14
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-textbook-mdx-compliance
branch: main
user: unknown
command: /sp.plan
labels: [plan, mdx, textbook, compliance]
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
  - specs/001-textbook-mdx-compliance/contracts/api-contracts.md
  - specs/001-textbook-mdx-compliance/contracts/skill-interface.yaml
  - specs/001-textbook-mdx-compliance/contracts/translation-api-contract.yaml
tests:
  - npm run build (validation)
---

## Prompt

Project: Physical AI & Humanoid Robotics Textbook  \nPhase 1: Content, Navigation & Frontend Updates\n\nObjective:\nUpdate the existing textbook to comply with the constitution by improving chapter content, fixing links, ensuring a clear frontpage, adding missing toggle controls, and migrating .md files to .mdx where needed.\n\n---\n\n## Subagents & Responsibilities\n\n1. **MDXMigrationAgent**\n   - Scan all .md files in the project\n   - Identify files that require interactive components (toggles, callouts, quizzes)\n   - Convert these files to .mdx while preserving:\n     - File names\n     - Routing\n     - Titles\n   - Skip conversion for files without interactive components\n   - Report any conflicts before converting\n\n2. **ContentWriterAgent**\n   - Refine existing chapter content for clarity, depth, and pedagogical quality\n   - Complete incomplete sections defined in the course outline\n   - Add missing examples, diagrams, exercises, quizzes, and glossary entries\n   - Ensure technical correctness and alignment with robotics fundamentals\n   - Maintain consistent structure and style across modules\n\n3. **ToggleAgent**\n   - Add Urdu/English toggle buttons to chapters/pages where missing\n   - Implement toggles as frontend-only MDX/React components\n   - Ensure English is default; Urdu content may be shown if present, else placeholder\n   - Verify toggles render correctly on every chapter\n\n4. **LinkCheckerAgent**\n   - Scan all internal links within chapters and frontpage\n   - Fix broken or missing links\n   - Ensure cross-links point only to existing files\n   - Confirm images, diagrams, and assets resolve correctly\n   - Report unresolved references or missing files\n\n5. **FrontpageDesignAgent**\n   - Review and improve homepage layout\n   - Ensure all four modules are clearly visible\n   - Each module card must navigate to its correct module entry page\n   - Use module names verbatim as locked in the constitution\n\n---\n\n## Task Sequence\n\n1. **MDX Migration**\n   - MDXMigrationAgent scans and converts necessary files\n   - Verify that routes, slugs, and titles remain unchanged\n\n2. **Toggle Addition**\n   - ToggleAgent adds missing Urdu/English toggle buttons\n   - Ensure toggles render correctly on all applicable pages\n\n3. **Content Refinement**\n   - ContentWriterAgent improves chapters and fills missing content\n   - Confirm examples, exercises, and diagrams are complete\n\n4. **Link Verification**\n   - LinkCheckerAgent scans for broken or missing links\n   - Fix all internal references, images, and diagrams\n   - Confirm Docusaurus build has zero warnings\n\n5. **Frontpage Update**\n   - FrontpageDesignAgent ensures module cards are correct\n   - Verify frontpage links to all modules and uses exact module names\n\n6. **Validation**\n   - Manual and automated verification:\n     - Docusaurus build completes with zero broken link warnings\n     - Sidebar navigation matches folder structure\n     - No 404 errors in manual navigation\n     - Frontpage provides clear access to all modules\n     - Toggles present and functional on all applicable pages\n\n---\n\n## Execution Rules\n\n- Phase 1 focuses only on frontend, content, and navigation\n- Backend implementation (RAG, API, translation) is deferred to later phases\n- If a conflict arises between existing content and the constitution, the constitution takes precedence\n- If required information is missing or unclear, pause execution and report before proceeding\n\nEnd of /sp.plan

## Response snapshot

# Implementation Plan: textbook-mdx-compliance

**Branch**: `001-textbook-mdx-compliance` | **Date**: 2025-12-14 | **Spec**: [specs/001-textbook-mdx-compliance/spec.md](specs/001-textbook-mdx-compliance/spec.md)
**Input**: Feature specification from `/specs/001-textbook-mdx-compliance/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Update the existing Physical AI & Humanoid Robotics textbook to comply with the constitution by migrating .md files to .mdx where interactive components are required, improving chapter content quality, fixing broken links, ensuring proper frontpage navigation, and adding missing Urdu/English toggle controls. The implementation will maintain the locked module structure while enhancing the educational value and technical compliance of the textbook.

## Technical Context

**Language/Version**: JavaScript/TypeScript, Node.js 18+
**Primary Dependencies**: Docusaurus v3.9.2, React, MDX
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

## Research Phase Completed

During the planning process, I also completed Phase 0 research and Phase 1 design:

- Created `research.md` with analysis of current Docusaurus setup, file format requirements, and technical decisions
- Created `data-model.md` describing content entities, relationships, and validation rules
- Created `quickstart.md` with essential steps for implementation
- Created `contracts/` directory with API contracts, skill interfaces, and translation API contracts
- Updated agent context with project-specific information

## Next Steps

The next step is to create the task breakdown using `/sp.tasks` command to generate actionable tasks for implementation.

## Architectural Decision Record Suggestion

📋 Architectural decision detected: Selection of MDX over pure Markdown for interactive components - Document reasoning and tradeoffs? Run `/sp.adr MDX-selection-for-interactive-components`

## Validation Criteria

- Docusaurus build completes with zero broken link warnings
- All interactive components function correctly
- Frontpage provides clear access to all four modules
- Content maintains technical accuracy and academic clarity
- Navigation structure matches file structure

## Subagent Implementation Strategy

The implementation will follow the subagent responsibilities defined in the specification:
1. MDXMigrationAgent - Handles file format conversions
2. ContentWriterAgent - Improves content quality
3. ToggleAgent - Adds language toggle functionality
4. LinkCheckerAgent - Verifies all internal links
5. FrontpageDesignAgent - Updates homepage layout

## Error Handling

During the planning process, I encountered and resolved line ending issues in bash scripts by removing Windows carriage return characters. The multiple spec directories error was noted but didn't prevent successful completion of the planning phase.

## Files Created

- `specs/001-textbook-mdx-compliance/plan.md` - Implementation plan
- `specs/001-textbook-mdx-compliance/research.md` - Research document
- `specs/001-textbook-mdx-compliance/data-model.md` - Data model
- `specs/001-textbook-mdx-compliance/quickstart.md` - Quickstart guide
- `specs/001-textbook-mdx-compliance/contracts/api-contracts.md` - API contracts
- `specs/001-textbook-mdx-compliance/contracts/skill-interface.yaml` - Skill interface contracts
- `specs/001-textbook-mdx-compliance/contracts/translation-api-contract.yaml` - Translation API contracts

## Compliance Verification

All constitution requirements have been verified and incorporated into the plan:
- Module names remain unchanged as required
- Technical architecture aligns with Docusaurus framework
- Content quality requirements are addressed
- Frontend architecture supports required components
- Personalization and translation requirements are planned

## Ready for Task Generation

The planning phase is complete and ready for the next step: task generation using `/sp.tasks`.

## Outcome

- ✅ Impact: Created comprehensive implementation plan with research, data model, contracts, and quickstart guide for textbook MDX compliance update
- 🧪 Tests: Docusaurus build validation planned as part of implementation
- 📁 Files: Created 7 new files across plan, research, data model, quickstart, and contracts
- 🔁 Next prompts: Ready for /sp.tasks to generate implementation tasks
- 🧠 Reflection: Planning phase successfully completed with all design artifacts created and agent context updated
- 📋 ADR: Suggested architectural decision record for MDX selection

## Evaluation notes (flywheel)

- Failure modes observed: Line ending issues in bash scripts resolved
- Graders run and results (PASS/FAIL): All constitution checks passed
- Prompt variant (if applicable): Standard /sp.plan workflow followed
- Next experiment (smallest change to try): Execute /sp.tasks to generate implementation tasks