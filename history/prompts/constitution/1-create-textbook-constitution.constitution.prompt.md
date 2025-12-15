---
id: 1
title: Create Textbook Constitution
stage: constitution
date: 2025-12-14
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, textbook, physical-ai]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
- .specify/templates/plan-template.md
- .specify/templates/spec-template.md
- .specify/templates/tasks-template.md
tests:

---

## Prompt

```
/sp.constitution

Project: Physical AI & Humanoid Robotics Textbook

Purpose:
Build a complete AI-native technical textbook using Docusaurus to teach the Physical AI & Humanoid Robotics 13 week course exactly as defined in the provided course outline. The textbook must include a polished landing page and a fully functional RAG chatbot backend.

Fixed Module List (Locked):
The textbook consists of exactly four modules. These names are frozen and must not be changed, reworded, abbreviated, or reordered.

Module 1: The Robotic Nervous System (ROS 2)
Module 2: The Digital Twin (Gazebo & Unity)
Module 3: The AI-Robot Brain (NVIDIA Isaac™)
Module 4: Vision-Language-Action (VLA)

These module names must be used verbatim in:
- Sidebar labels
- URL slugs
- Homepage module cards
- RAG indexing metadata

Scope Boundary:
All content must strictly follow the provided course outline and verified robotics fundamentals. No speculative hardware, invented concepts, or hallucinated technologies are allowed. Module structure, titles, and hierarchy are locked.

Primary Deliverables:

Frontend (Docusaurus):
- Homepage with interactive module cards
- Modules → chapters → subsections matching the outline
- Glossary, quizzes, exercises, diagrams
- Reusable MDX components: callouts, quizzes, Urdu toggle, personalization toggle
- Clean navigation and stable routing

Backend (FastAPI):
- RAG chatbot using OpenAI Agents / ChatKit
- Qdrant vector database + Neon Postgres
- Chunk size: 300–500 tokens, top_k: 5, MiniLM embeddings, cosine similarity
- Per-page RAG mode using selected page context
- Urdu translation endpoint
- User personalization endpoint

Personalization & Translation:
Personalization may adjust explanation depth by user level but must never alter technical correctness. Urdu translations must preserve exact technical meaning. Toggles must function on every chapter.

Subagents (Role-Locked):
- ContentWriterAgent
- GlossaryAgent
- QuizAgent
- TranslationAgent
- PersonalizationAgent
- RAGIndexAgent
- HomepageDesignAgent

Acceptance Criteria:
- Zero build warnings or broken links
- RAG chatbot answers at least 90% of seeded test questions correctly
- Personalization and Urdu toggles work across all chapters
- Folder structure complies with Docusaurus standards
- Project is fully deployable to GitHub Pages and/or Vercel

Change Control & Failure Rules:
Module names, structure, and hierarchy are immutable. Any conflict, missing dependency, or build failure must pause execution and be reported. No autonomous scope expansion or renaming is allowed.

End of constitution.
```

## Response snapshot

The constitution for the Physical AI & Humanoid Robotics Textbook has been successfully updated to version 1.1.0. The following changes were made:

### New Version: 1.1.0 (Minor version bump - new sections added)

**Added sections:**
- Fixed Module List (Locked) with the four required modules
- Technical Architecture section with Frontend (Docusaurus) and Backend (FastAPI) requirements
- Personalization & Translation requirements
- Role-Locked Subagents section
- Quality Assurance section with Scope Boundary, Acceptance Criteria, and Change Control rules

**Updated templates:**
- `.specify/templates/plan-template.md` - Added constitution checks aligned with textbook requirements
- `.specify/templates/spec-template.md` - Added functional requirements aligned with constitution
- `.specify/templates/tasks-template.md` - Added task categories aligned with textbook architecture

**Key constitution elements:**
- Scientific Accuracy: All claims must be verifiable and traceable to reputable sources
- Academic Clarity: Content for undergraduate-level audience with proper terminology
- Fixed 4-module structure: The Robotic Nervous System (ROS 2), The Digital Twin (Gazebo & Unity), The AI-Robot Brain (NVIDIA Isaac™), Vision-Language-Action (VLA)
- Frontend: Docusaurus-based with interactive components
- Backend: FastAPI with RAG chatbot, Qdrant vector database, translation/personalization
- Acceptance: 90% RAG accuracy, zero build warnings, proper deployment

The constitution now fully reflects the requirements specified in your input, ensuring all future development aligns with these principles.

## Outcome

- ✅ Impact: Constitution updated to v1.1.0 with comprehensive textbook requirements
- 🧪 Tests: constitution validation
- 📁 Files: 4 files updated to align with new constitution
- 🔁 Next prompts: Feature specification and planning based on new constitution
- 🧠 Reflection: The constitution now properly captures all requirements for the Physical AI & Humanoid Robotics Textbook project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All requirements properly captured
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification based on new constitution