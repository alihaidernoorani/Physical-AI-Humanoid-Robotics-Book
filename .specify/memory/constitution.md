<!--
SYNC IMPACT REPORT:
Version change: 1.1.0 → 1.2.0
Added sections: Internal verification requirements, RAG grounding enforcement, metadata requirements
Modified sections: Content Verification & Plagiarism Standards, Book Format & Deployment, Content Constraints, Backend Architecture
Removed sections: Reader-facing citation requirements
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ⚠ pending
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

### Visual & Accessibility Standards
Non-copyright diagrams preferred. Provide descriptions of all figures for accessibility. All visuals must be original or properly licensed for educational use.

## Technical Architecture

### Frontend (Docusaurus)
- Homepage with interactive module cards
- Modules → chapters → subsections matching the course outline
- Glossary, quizzes, exercises, diagrams
- Reusable MDX components: callouts, quizzes, Urdu toggle, personalization toggle
- Clean navigation and stable routing

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

### Acceptance Criteria
- Zero build warnings or broken links
- RAG chatbot answers at least 90% of seeded test questions correctly
- Personalization and Urdu toggles work across all chapters
- Folder structure complies with Docusaurus standards
- Project is fully deployable to GitHub Pages and/or Vercel

### Change Control & Failure Rules
Module names, structure, and hierarchy are immutable. Any conflict, missing dependency, or build failure must pause execution and be reported. No autonomous scope expansion or renaming is allowed.

## Governance

The constitution governs all content generation, review, editing, and verification across the full book creation process. All chapters and content must comply with these principles before acceptance. Any deviation from these principles requires explicit amendment to the constitution following the project governance process.

**Version**: 1.2.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-14