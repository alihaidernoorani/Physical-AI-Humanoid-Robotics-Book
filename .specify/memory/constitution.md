<!--
SYNC IMPACT REPORT:
Version change: 1.2.0 → 1.3.0
Added sections: Visual Standards & Diagrams, Typography & Readability, Landing Page Requirements
Modified sections: Visual & Accessibility Standards (expanded), Frontend (Docusaurus) (added diagram constraints)
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated (already aligned - Constitution Check covers visual standards)
- .specify/templates/spec-template.md ✅ updated (already aligned)
- .specify/templates/tasks-template.md ✅ updated (already aligned)
- .specify/templates/commands/*.md ⚠ pending (no command files found)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### Scientific Accuracy
Every factual claim must be traceable to a verifiable source. Prefer primary research from robotics, embodied cognition, biomechanics, and AI/ML. All content must be grounded in verifiable, state-of-the-art research with no hallucinated references under any circumstances.

### Academic Clarity
Write for an audience with an undergraduate-level background in computer science, robotics, or AI. Define advanced terminology before use. Content must be instructional, analytical, and research-driven with Flesch–Kincaid Grade 10–12 writing level.

### Reproducibility & Transparency
All methods, algorithms, mathematical formulations, and conceptual frameworks must be presented with enough detail to be reproducible. Each chapter must clearly state assumptions, models, and dependencies. Include symbolic definitions for all variables in mathematical formulations.

### Rigor & Peer-Review Standards
Minimum 50% peer-reviewed sources from robotics/AI conferences and journals. Prioritize sources such as: IEEE, Nature Robotics, Science Robotics, ACM, arXiv (with caution), RSS, ICRA, IROS. No claim should appear unless verified by at least one reputable source.

### Ethical & Safety Awareness
Consider ethical implications, safety constraints, societal impact, and human-robot interaction standards. No unverified claims about capabilities or dangers. Content must address ethical considerations and safety constraints in Physical AI and Humanoid Robotics.

### Content Verification & Plagiarism Standards
Plagiarism tolerance: 0% (all text must be original). Internal verification system must ensure all content is grounded in verifiable sources with no hallucinations. Source types: ≥ 50% peer-reviewed academic sources; Remaining sources may include technical standards, robotics lab documentation, textbooks, reputable industry whitepapers, and specifications from leading robotics groups. Reader-facing citations and bibliographies are prohibited.

## Structural Requirements

### Fixed Module List (Locked)
The textbook consists of exactly four modules. These names are frozen and must not be changed, reworded, abbreviated, or reordered.

- Module 1: The Robotic Nervous System (ROS 2)
- Module 2: The Digital Twin (Gazebo & Unity)
- Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- Module 4: Vision-Language-Action (VLA)

These module names must be used verbatim in:
- Sidebar labels
- URL slugs
- Homepage module cards
- RAG indexing metadata

### Book Format & Deployment
Book Format: Docusaurus-based. Deployment: GitHub Pages. Minimum Length: 20–30 full chapters. Each chapter must meet specific requirements: Learning objectives, Key definitions, Examples & illustrations, Summary, Glossary entries where needed. No citations sections or bibliographies visible to readers.

### Landing Page Requirements
An introductory landing page is MANDATORY for the book. The landing page MUST include:
- Clear book title and subtitle
- Module overview cards linking to each of the four modules
- Visual hierarchy emphasizing textbook identity (not API documentation)
- Accessible navigation to all major sections
- Responsive design optimized for all screen sizes

### Visual Standards & Diagrams
All diagrams MUST follow these mandatory rules:

**Mermaid-First Policy:**
- All diagrams MUST be rendered using native Mermaid syntax in MDX/Markdown
- Custom diagram rendering components are PROHIBITED unless explicitly justified in writing
- Every diagram MUST have a visible visual representation (rendered Mermaid code block)
- Every diagram MUST have an accompanying caption describing its purpose

**Prohibited Content:**
- Diagram metadata without actual rendered diagrams
- Placeholder text such as "Diagram Description:", "Figure shows:", or similar conversion artifacts
- Descriptive-only diagram text that replaces visual content
- Empty or commented-out diagram blocks
- References to diagrams that do not exist in the document

**Responsive Diagrams:**
- All diagrams MUST be responsive and not overflow on mobile viewports
- Use Mermaid's built-in responsive features
- Test diagrams at mobile breakpoints (320px, 375px, 414px minimum)
- Complex diagrams MUST gracefully degrade or provide alternative views for small screens

### Typography & Readability
All content MUST adhere to these readability standards:

**Mobile-First Design:**
- Typography MUST be optimized for mobile reading first
- Body text: minimum 16px equivalent, line-height 1.5–1.7
- Spacing MUST ensure comfortable reading on small screens
- No horizontal overflow on any content element
- Touch targets MUST be at least 44x44px for interactive elements

**Dark-Mode Optimization:**
- All typography MUST maintain WCAG AA contrast ratios in both light and dark modes
- Long-form reading MUST be optimized for dark mode with reduced eye strain
- Code blocks and diagrams MUST be legible in dark mode
- Avoid pure white (#FFFFFF) text on pure black (#000000) backgrounds

**Textbook-Style Visual Hierarchy:**
- Use visual hierarchy appropriate for educational textbooks, not API documentation
- Clear distinction between headings (h1 > h2 > h3)
- Generous whitespace between sections
- Pull quotes, callouts, and key definitions MUST be visually distinct
- Chapter titles MUST be prominent and scannable

### Visual & Accessibility Standards
Non-copyright diagrams preferred. Provide descriptions of all figures for accessibility. All visuals must be original or properly licensed for educational use. All images and diagrams MUST have alt text for screen readers. Color MUST NOT be the only means of conveying information.

## Technical Architecture

### Frontend (Docusaurus)
- Homepage with interactive module cards (MANDATORY)
- Modules → chapters → subsections matching the course outline
- Glossary, quizzes, exercises, diagrams
- Reusable MDX components: callouts, quizzes, Urdu toggle, personalization toggle
- Clean navigation and stable routing
- Mermaid diagrams via native Docusaurus Mermaid support (no custom components)
- Mobile-first responsive design with dark mode support
- Textbook-style visual hierarchy throughout

### Backend (FastAPI)
- RAG chatbot using OpenAI Agents / ChatKit
- QAG chatbot must only generate answers from retrieved chunks with proper grounding
- If grounding is insufficient, respond with uncertainty rather than hallucinating
- Qdrant vector database + Neon Postgres
- Chunk size: 300–500 tokens, top_k: 5, MiniLM embeddings, cosine similarity
- Per-page RAG mode using selected page context
- All indexed chunks must include metadata: module, chapter, subsection, source_type, source_origin
- Urdu translation endpoint
- User personalization endpoint

### Personalization & Translation
Personalization may adjust explanation depth by user level but must never alter technical correctness. Urdu translations must preserve exact technical meaning. Toggles must function on every chapter.

## Development Workflow

### Chapter Creation Process
Each chapter must be generated through a spec-first workflow: outline → draft → verify → revise. Use Spec-Kit Plus commands: /sp.chapter, /sp.glossary, /sp.diagram.description, /sp.proto, /sp.checklist for all content creation.

### Role-Locked Subagents
- ContentWriterAgent
- GlossaryAgent
- QuizAgent
- TranslationAgent
- PersonalizationAgent
- RAGIndexAgent
- HomepageDesignAgent

### Content Constraints
Total Word Count: 30,000–50000 words. Minimum Sources: 40+ (internal verification only). Mathematical Accuracy: Use canonical equations from robotics, control theory, machine learning, and embodied intelligence. All factual claims must be source-verified internally. No reader-facing references or bibliographies allowed.

## Quality Assurance

### Scope Boundary
All content must strictly follow the provided course outline and verified robotics fundamentals. No speculative hardware, invented concepts, or hallucinated technologies are allowed. Module structure, titles, and hierarchy are locked.

### Visual Quality Checklist
Before any content is accepted, verify:
- [ ] All diagrams render correctly as Mermaid (no placeholder text)
- [ ] All diagrams have captions
- [ ] No "Diagram Description:" or similar conversion artifacts exist
- [ ] Content is readable on mobile (no horizontal overflow)
- [ ] Dark mode contrast meets WCAG AA standards
- [ ] Landing page exists and links to all modules
- [ ] Visual hierarchy follows textbook conventions

### Acceptance Criteria
- Zero build warnings or broken links
- RAG chatbot answers at least 90% of seeded test questions correctly
- Personalization and Urdu toggles work across all chapters
- Folder structure complies with Docusaurus standards
- Project is fully deployable to GitHub Pages and/or Vercel
- All diagrams render as visual Mermaid (no text-only placeholders)
- Mobile-first responsive design verified at 320px minimum width
- Dark mode optimized for extended reading sessions

### Change Control & Failure Rules
Module names, structure, and hierarchy are immutable. Any conflict, missing dependency, or build failure must pause execution and be reported. No autonomous scope expansion or renaming is allowed.

## Governance

The constitution governs all content generation, review, editing, and verification across the full book creation process. All chapters and content must comply with these principles before acceptance. Any deviation from these principles requires explicit amendment to the constitution following the project governance process.

**Version**: 1.3.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-29
