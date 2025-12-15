# Implementation Plan: Interactive Physical AI & Humanoid Robotics Textbook

**Branch**: `001-full-book-plus` | **Date**: 2025-12-09 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-full-book-plus/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a complete, interactive Docusaurus textbook for *Physical AI & Humanoid Robotics* with enhanced features: better-auth integration with client-side localStorage for user profiles, personalization using React conditional rendering based on user background, on-demand Urdu translation via Claude Code Subagent/Skill pattern, and improved UI/UX with custom CSS overrides. The solution maintains all 21 chapters with simplified formatting for improved readability while ensuring GitHub Pages compatibility through static deployment and relative links.

## Technical Context

**Language/Version**: JavaScript/TypeScript, Node.js 20+, Docusaurus v3.9.2
**Primary Dependencies**: Docusaurus, React, better-auth, LibreTranslate API or browser translation API
**Storage**: localStorage (client-side only), Markdown files for content
**Testing**: Jest for unit tests, Cypress for end-to-end tests
**Target Platform**: Web browser (GitHub Pages deployment, static site)
**Project Type**: Web application (static site with client-side interactivity)
**Performance Goals**: Lighthouse mobile audit score >85, JS bundle <500KB (excluding Docusaurus core)
**Constraints**: GitHub Pages compatible (static only), relative links for navigation, all client-side logic
**Scale/Scope**: 21 textbook chapters, client-side personalization, on-demand translation to Urdu

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Scientific Accuracy Compliance
- ✓ Content will be preserved from existing chapters with simplified formatting
- ✓ All personalization and translation features will not alter factual content
- ✓ Mathematical formulations and technical content remain unchanged

### Academic Clarity Compliance
- ✓ Content simplification will maintain academic rigor while improving readability
- ✓ Personalization features will adjust depth without compromising accuracy
- ✓ All technical terminology will remain properly defined

### Reproducibility & Transparency Compliance
- ✓ All client-side features will be implemented with clear, reproducible code
- ✓ Translation and personalization logic will be transparent in implementation
- ✓ All variables and state will be properly documented

### Rigor & Peer-Review Standards Compliance
- ✓ No new content is being created that would require additional sources
- ✓ Existing content with peer-reviewed sources remains unchanged
- ✓ Technical implementation follows established patterns

### Ethical & Safety Awareness Compliance
- ✓ All ethical considerations in original content are preserved
- ✓ Personalization features respect user privacy (client-side only)
- ✓ Translation features maintain ethical context of original content

### Content Verification & Plagiarism Standards Compliance
- ✓ No new content being generated - only enhancing existing content with features
- ✓ All existing citations and sources remain intact
- ✓ Code implementation will follow original development standards

### Structural Requirements Compliance
- ✓ Docusaurus-based format maintained
- ✓ GitHub Pages deployment maintained
- ✓ All 21 chapters preserved with enhanced functionality
- ✓ Each chapter retains required elements (learning objectives, summaries, etc.)

### Visual & Accessibility Standards Compliance
- ✓ Enhanced typography and spacing will improve accessibility
- ✓ RTL layout for Urdu translation will meet accessibility standards
- ✓ All existing visual descriptions preserved

## Project Structure

### Documentation (this feature)

```text
specs/001-full-book-plus/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure for Docusaurus-based textbook
docs/
├── intro.md             # Main intro page with "Start Learning" button
├── 01-ros2-nervous-system/
├── 02-digital-twin/
├── 03-ai-robot-brain/
├── ...                  # All 21 chapters as subdirectories
└── ...                  # All existing chapter content preserved

src/
├── components/          # Custom React components for personalization, translation
│   ├── PersonalizationButton/
│   ├── UrduTranslationButton/
│   ├── UserProfileModal/
│   ├── KeyTakeaways/
│   └── EthicalNotes/
├── pages/               # Custom pages if needed
├── theme/               # Custom Docusaurus theme overrides
│   ├── MDXComponents/   # Custom MDX components
│   └── ...              # Theme customization
├── css/                 # Custom CSS for typography and styling
│   └── custom.css
└── utils/               # Utility functions for translation, personalization

static/
└── img/                 # Static images for the textbook

.clauude/
├── subagents/
│   └── urdu_translator/ # Urdu translation subagent
│       └── agent.md
└── skills/
    └── urdu-translation-skill/ # Urdu translation skill
        ├── skill.yaml
        └── implementation.js

# Docusaurus configuration
docusaurus.config.js
package.json
```

**Structure Decision**: Web application with static Docusaurus site structure. All functionality implemented through client-side React components and Docusaurus theme customization. Subagent and Skill components follow Claude Code conventions in dedicated directories.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
