# Data Model: Backend-Frontend Integration

## Entities

### Legacy Files
- **Description**: Files identified in audit report as either safe to delete or requiring review
- **Attributes**:
  - file_path: string (location of the file/directory)
  - status: enum (safe_to_delete, needs_review, archived)
  - dependencies: list (other files that depend on this file)
- **Relationships**: None

### Core Backend Files
- **Description**: Essential files that must remain unchanged (app/main.py, app/agent.py, app/rag.py, app/chat.py, app/config.py)
- **Attributes**:
  - file_path: string (location of the core file)
  - checksum: string (to verify file integrity after cleanup)
  - functionality: string (description of what the file does)
- **Relationships**: None

### API Endpoints
- **Description**: Backend services accessible via /chat, /translate, and /personalize endpoints
- **Attributes**:
  - endpoint_path: string (URL path like /chat, /translate, /personalize)
  - method: string (HTTP method like GET, POST)
  - request_schema: object (structure of expected request)
  - response_schema: object (structure of expected response)
  - status: enum (active, inactive, under_maintenance)
- **Relationships**: None

### ChatKit UI Components
- **Description**: Frontend components providing chat interface for user interaction
- **Attributes**:
  - component_name: string (name of the UI component)
  - purpose: string (what the component does)
  - props: object (expected input properties)
  - state: object (internal state managed by component)
- **Relationships**: None

### Integration Tasks
- **Description**: Documented steps in tasks.md for implementing cleanup and frontend integration
- **Attributes**:
  - task_id: string (unique identifier for the task)
  - description: string (what needs to be done)
  - type: enum (cleanup, integration, testing, documentation)
  - priority: enum (P1, P2, P3)
  - status: enum (pending, in_progress, completed)
  - dependencies: list (other tasks this task depends on)
- **Relationships**: None

## State Transitions

### Legacy Files State Transitions
- Initial state: identified_in_audit
- Transition 1: identified_in_audit → safe_to_delete (when confirmed safe)
- Transition 2: identified_in_audit → needs_review (when ambiguous)
- Transition 3: needs_review → archived (when moved for manual approval)
- Transition 4: safe_to_delete → deleted (when removed from codebase)

### Integration Tasks State Transitions
- Initial state: pending
- Transition 1: pending → in_progress (when work begins)
- Transition 2: in_progress → completed (when task is finished)
- Transition 3: in_progress → blocked (when dependencies not met)
- Transition 4: blocked → in_progress (when dependencies resolved)