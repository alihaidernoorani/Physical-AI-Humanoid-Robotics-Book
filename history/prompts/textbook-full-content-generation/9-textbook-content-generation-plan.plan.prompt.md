---
id: 9
title: Textbook Content Generation Plan
stage: plan
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: textbook-full-content-generation
branch: 001-textbook-full-content-generation
user: Claude
command: /sp.plan
labels: [planning, textbook, content-generation, architecture]
links:
  spec: specs/001-textbook-full-content-generation/spec.md
  plan: specs/001-textbook-full-content-generation/plan.md
  adr: null
  pr: null
files:
 - specs/001-textbook-full-content-generation/plan.md
 - specs/001-textbook-full-content-generation/research.md
 - specs/001-textbook-full-content-generation/data-model.md
 - specs/001-textbook-full-content-generation/quickstart.md
 - specs/001-textbook-full-content-generation/contracts/textbook-content-contract.md
 - CLAUDE.md
tests:
 - constitution compliance check
 - content structure validation
---

## Prompt

Create a technical and editorial plan for generating **all chapter content** of the *Physical AI & Humanoid Robotics* textbook, following the existing blueprint in `docs/` and governance rules in `constitution.md`.

**Deliverables**:
- Architecture sketch of the content generation workflow
- Section structure per module (aligned with course outline)
- Research approach for technical accuracy
- Quality validation and testing strategy

**Key Components**:

### Architecture Sketch
- Content will be generated **module-by-module, chapter-by-chapter** using Claude Code
- Output: GitHub Pages–compatible Markdown files with preserved frontmatter (`personalization: true`, `translation: ur`)
- No code blocks, labs, or implementation commands—only conceptual, narrative-driven technical prose
- All content will assume reader has completed prerequisite chapters

### Section Structure per Module
- **Module 1 (ROS 2)**: Focus on real-time control, node architecture, and humanoid URDF
- **Module 2 (Digital Twin)**: Physics simulation, sensor modeling, Gazebo/Unity interoperability
- **Module 3 (AI-Robot Brain)**: Isaac Sim synthetic data, hardware-accelerated perception, Nav2 for bipeds
- **Module 4 (VLA)**: Voice-to-action, LLM-based task planning, capstone integration

Each chapter must include:
- 3–5 learning objectives
- Conceptual explanations (graduate-level depth)
- Forward references to capstone project
- "Key Takeaways" summary

### Research Approach
- **Research-concurrent**: Validate tool versions (e.g., ROS 2 Humble, Isaac Sim 2024+, Jetson Orin Nano) during writing—not upfront
- Use official documentation (ROS, NVIDIA, OpenAI) as primary sources
- Follow citation style and depth guidelines from `constitution.md`
- Avoid vendor comparisons, ethics, or historical tangents

### Decisions Needing Documentation
| Decision | Options | Tradeoff |
|--------|--------|---------|
| **Depth of math/formalism** | Lightweight intuition vs. equations | Audience is applied AI developers → favor intuition with optional formal asides |
| **ROS 2 distro** | Humble vs. Iron vs. Jazzy | Use **Humble** (LTS, best Isaac ROS support) |
| **VLA architecture** | Local Whisper + open LLM vs. OpenAI API | Describe **OpenAI Whisper + GPT-4o** (allowed per hackathon), but note local alternatives |
| **Hardware references** | Jetson Orin Nano vs. AGX | Default to **Orin Nano** (matches $700 student kit), mention AGX for advanced setups |

### Quality Validation & Testing Strategy
- ✅ Every chapter scaffolds the **Autonomous Humanoid capstone**
- ✅ All tool/hardware names use **2024–2025 standards**
- ✅ No code blocks or CLI instructions (reserve for labs)
- ✅ Frontmatter unchanged (metadata intact for future personalization/Urdu)
- ✅ Tone and depth consistent with `constitution.md`
- ✅ Passes `/sp.analyze` for cross-chapter consistency

**Technical Details**:
- Use research-concurrent approach (validate while writing)
- Organize writing by phases:
  **Foundation** (Modules 1–2: control + simulation) →
  **Integration** (Module 3: AI brain) →
  **Synthesis** (Module 4: VLA + capstone)
- Follow editorial standards from `constitution.md` (e.g., no first-person, active voice, concise prose)

## Response snapshot

Created a comprehensive implementation plan for the textbook content generation including:

- **Plan document** (plan.md): Technical context, constitution check, project structure
- **Research summary** (research.md): Technology decisions, standards, validation approach
- **Data model** (data-model.md): Content structure, entities, constraints
- **Quickstart guide** (quickstart.md): Generation workflow, best practices, validation checklist
- **Content contract** (contracts/textbook-content-contract.md): Interface definitions and compliance requirements
- **Agent context update**: Updated CLAUDE.md with project-specific technologies

The plan addresses all key components requested: architecture sketch (module-by-module generation), section structure per module, research approach (research-concurrent with official docs), and quality validation strategy (compliance with constitution, frontmatter preservation, 2024-2025 standards).

## Outcome

- ✅ Impact: Complete implementation plan for textbook content generation
- 🧪 Tests: Constitution compliance and content structure validation defined
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contract files
- 🔁 Next prompts: Ready for task generation (/sp.tasks)
- 🧠 Reflection: Plan addresses all required components with clear workflow and validation

## Evaluation notes (flywheel)

- Failure modes observed: None - all components successfully generated
- Graders run and results (PASS/FAIL): PASS - constitution check passed
- Prompt variant (if applicable): Implementation planning prompt
- Next experiment (smallest change to try): Generate tasks for content creation