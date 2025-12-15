---
id: 16
title: "Generate MDX compliance implementation tasks"
stage: tasks
date: 2025-12-15
surface: agent
model: Claude Sonnet 4.5
feature: textbook-mdx-compliance
branch: 001-textbook-mdx-compliance
user: claude
command: /sp.tasks
labels: ["mdx", "compliance", "tasks", "textbook"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-textbook-mdx-compliance/tasks.md"
tests: []
---

# Generate MDX compliance implementation tasks

## Prompt Text

```
Task 1: Inventory and coverage confirmation
Create a complete inventory of all textbook chapters and MDX files in the repository. Confirm that the inventory matches the existing module names, order, and hierarchy. This inventory will be used as a coverage checklist to ensure no chapter is skipped.

Task 2: Chapter-by-chapter MDX safety audit
For each chapter in the inventory, scan the content to identify MDX and JSX failure risks, including invalid JSX-like syntax, square bracket misuse, raw HTML, improper attributes, and unwrapped code examples. Record all issues found for that chapter.

Task 3: Substantive chapter rewrite and refinement
Rewrite each chapter at the sentence and paragraph level to improve clarity, narrative flow, and pedagogical quality while preserving all original technical meaning. Convert dense or informal sections into clear instructional prose and add short explanations where logical gaps exist.

Task 4: Removal of external references and citations
Remove all reader-facing external references, citations, bibliographies, and inline citation markers from each chapter. Ensure that no links or references are presented as sources in the final MDX output.

Task 5: Internal verification of factual claims
Verify all factual and technical claims internally against reliable sources during the rewrite process. Ensure accuracy is preserved, but do not expose sources or citations in the chapter content.

Task 6: MDX-safe formatting standardization
Standardize each chapter to pure Markdown suitable for MDX. Apply consistent heading hierarchy, wrap all code examples in fenced code blocks, ensure lists and tables follow Markdown standards, and eliminate any syntax that could trigger JSX parsing.

Task 7: Consistency and quality review
Review all rewritten chapters for consistent terminology, tone, and instructional quality across the entire textbook. Confirm that module names, order, and hierarchy remain unchanged.

Task 8: Build validation and error resolution
Run the Docusaurus build process to validate that all chapters compile successfully with zero MDX or JSX errors. Resolve any remaining issues and re-run the build until it completes without warnings or failures.

Task 8.5: Link and asset integrity validation
Check all internal links, Markdown links, and asset references across every chapter. Resolve or remove any broken links or missing assets so that the build produces zero broken-link warnings.

Task 9: Completion verification
Cross-check the completed chapters against the initial inventory to confirm that every chapter has been processed, rewritten, and validated.

Task 10: Hard completion gate
Do not mark this feature complete unless the Docusaurus build finishes successfully with zero errors and zero warnings, including MDX/JSX issues, broken links, and asset validation warnings. If any errors or warnings remain, return to the relevant task and repeat until the build is completely clean.
```

## Response Text

Created a comprehensive tasks.md file with 60 tasks organized across 7 phases:

1. Phase 1: Setup Tasks (T001-T008) - Inventory and environment setup
2. Phase 2: Foundational Tasks (T009-T016) - MDX safety infrastructure
3. Phase 3: User Story 1 - Inventory and MDX Safety Audit (T017-T024) - Complete chapter auditing
4. Phase 4: User Story 2 - Chapter Rewrite and Refinement (T025-T032) - Content improvement
5. Phase 5: User Story 3 - Citation Removal and Content Standardization (T033-T040) - Remove references
6. Phase 6: User Story 4 - MDX-Safe Formatting and Validation (T041-T048) - Format compliance
7. Phase 7: Polish & Cross-Cutting Concerns (T049-T060) - Final validation

All tasks follow the required format with checkboxes, sequential IDs, parallel markers [P], user story labels [US1-4], and specific file paths. The implementation strategy follows an MVP-first approach with parallel execution opportunities.

## Outcome

Successfully generated implementation tasks that map directly to the user's requirements for MDX compliance. The tasks are organized by priority and can be executed in parallel at the chapter level, with clear dependencies and validation checkpoints throughout the process.

## Evaluation

The generated tasks.md file provides a complete roadmap for implementing MDX compliance across all textbook chapters, with proper tracking, validation, and quality assurance steps.