---
id: 2
title: Create Textbook Blueprint Spec
stage: spec
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: physical-ai-textbook
branch: 001-physical-ai-textbook
user: user
command: /sp.specify
labels: [spec,physical-ai,robotics,textbook,blueprint]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-physical-ai-textbook/spec.md
 - specs/001-physical-ai-textbook/textbook-blueprint.md
 - specs/001-physical-ai-textbook/checklists/requirements.md
tests:
 - none
---

## Prompt

```text
Physical AI & Humanoid Robotics – Textbook Blueprint

**Goal**:
Generate a complete, production-ready **book outline** (no content) for a Docusaurus-based textbook aligned with the official 4-module capstone course on Physical AI and Humanoid Robotics. This blueprint will directly drive chapter authoring, site architecture, and eventual deployment to **GitHub Pages**.

**Target audience**:
Advanced undergraduate or graduate students in AI/robotics with prior experience in Python, Linux, and basic machine learning. They are preparing to build embodied AI systems using industry-standard robotics frameworks.

**Course theme**:
"AI Systems in the Physical World: Embodied Intelligence" — bridging digital AI models with physical humanoid agents in simulation and reality.

**Required output**:
A hierarchical Markdown outline containing:
- 4 top-level modules (as defined below)
- 3–6 chapters per module
- 2–5 clearly named subtopics per chapter
- For each module:
  • 3–5 measurable learning outcomes
  • Core software stack (e.g., ROS 2 Humble, Gazebo Harmonic, NVIDIA Isaac Sim 2024+, Unity Robotics)
  • Recommended hardware (e.g., NVIDIA Jetson AGX Orin, Intel RealSense, etc.)
  • Dependencies on prior modules

**Module definitions (must use these exact titles and focus areas)**:

**Module 1: The Robotic Nervous System (ROS 2)**
Focus: Middleware for real-time robot control
- ROS 2 nodes, topics, services, and actions
- Writing ROS 2 agents in Python (rclpy)
- URDF for humanoid kinematic modeling
- Lifecycle nodes and composition

**Module 2: The Digital Twin (Gazebo & Unity)**
Focus: Physics-based simulation and human-robot interaction
- Rigid body dynamics, gravity, and collision in Gazebo
- Sensor simulation (LiDAR, RGB-D cameras, IMUs)
- High-fidelity environments in Unity with ROS 2 integration
- Synchronizing Gazebo and Unity for hybrid simulation

**Module 3: The AI-Robot Brain (NVIDIA Isaac™)**
Focus: Perception, navigation, and hardware-accelerated AI
- NVIDIA Isaac Sim for synthetic data generation
- Isaac ROS GEMs: VSLAM, object detection, and depth estimation
- Nav2 stack for bipedal path planning and recovery behaviors
- Real-time inference on edge devices (Jetson)

**Module 4: Vision-Language-Action (VLA)**
Focus: Multimodal reasoning for autonomous humanoids
- Voice-to-text with Whisper (local or cloud)
- LLM-based task decomposition (e.g., “Clean the room” → pick, place, avoid)
- Grounding language in ROS 2 action servers
- Capstone: End-to-end autonomous humanoid in simulation (voice → plan → navigate → perceive → act)

**Success criteria**:
✅ Outline mirrors the official 12–16 week course flow
✅ Each chapter maps to ~1 week of instruction
✅ Subtopics are concrete enough to become individual Docusaurus documentation pages
✅ Tools/hardware reflect 2024–2025 academic/industry standards
✅ Capstone project is scaffolded across Modules 1–4
✅ Structure assumes **static site deployment via GitHub Pages** (no server-side logic)

**Constraints**:
- Format: **Pure Markdown** (h2/h3 headings, bullet lists only)
- **No prose, explanations, code, or examples**—structure only
- Do not invent new modules or deviate from the 4 given themes
- Avoid ethics, history, or vendor comparisons
- All content must be **static and self-contained** (GitHub Pages compatible)

**Not building**:
- Chapter content, tutorials, or concept explanations
- Code snippets, CLI commands, or config files
- Assessments, quizzes, or grading rubrics
- Marketing language or motivational text

**Specify+ note**:
This blueprint will be used to generate individual /sp.specify prompts per chapter. Structure must enable modular, parallel content development for a Docusaurus site deployed on **GitHub Pages**.
```

## Response snapshot

Created a comprehensive specification and textbook blueprint for the Physical AI & Humanoid Robotics textbook. The work included:

1. Feature specification (specs/001-physical-ai-textbook/spec.md) with user scenarios, functional requirements, and success criteria
2. Detailed textbook blueprint (specs/001-physical-ai-textbook/textbook-blueprint.md) with 4 modules, chapters, learning outcomes, software stacks, and hardware recommendations
3. Quality checklist (specs/001-physical-ai-textbook/checklists/requirements.md) to validate the specification

The blueprint covers all 4 required modules with appropriate chapters and subtopics, following a 13-week course structure as specified. Each module includes measurable learning outcomes, recommended software stacks, hardware requirements, and dependencies on prior modules.

## Outcome

- ✅ Impact: Created complete textbook blueprint aligned with 4-module capstone course
- 🧪 Tests: none
- 📁 Files: spec.md, textbook-blueprint.md, requirements.md
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: The blueprint provides a solid foundation for modular content development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning individual chapters