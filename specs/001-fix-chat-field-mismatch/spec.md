# Feature Specification: Fix Chat API Field Mismatch

**Feature Branch**: `001-fix-chat-field-mismatch`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "Fix frontend-backend field mismatch where frontend sends 'query' but backend expects 'message', causing 400 errors to be converted to 500 errors"

## Problem Statement

The chat widget is experiencing a critical bug where users cannot successfully send messages. The issue stems from two related problems:

1. **Field Name Mismatch**: The frontend sends a `query` field but the backend expects a `message` field, causing request validation failures
2. **Error Masking**: The backend exception handling catches all exceptions (including HTTP 400 Bad Request) and converts them to generic 500 Internal Server Error responses, hiding the actual validation error from debugging

This results in a poor user experience where chat messages fail silently with unhelpful error messages.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Successful Chat Message (Priority: P1)

A user visits the Physical AI Humanoid Robotics textbook website and uses the chat widget to ask a question. The message is sent to the backend and a response is received and displayed.

**Why this priority**: This is the core functionality that is currently broken. Without this fix, users cannot use the chat feature at all.

**Independent Test**: Can be fully tested by opening the chat widget, typing a message, and clicking send. Success is indicated by receiving a response from the AI assistant.

**Acceptance Scenarios**:

1. **Given** a user has the chat widget open, **When** they type a message and click send, **Then** the message is successfully transmitted to the backend and a response is displayed
2. **Given** a user sends a valid message, **When** the backend processes the request, **Then** the request body contains a `message` field that the backend can parse correctly

---

### User Story 2 - Meaningful Error Messages (Priority: P2)

When a chat request fails due to validation issues (e.g., empty message, missing required fields), the user receives a clear error message indicating what went wrong, rather than a generic "Internal Server Error".

**Why this priority**: Proper error handling is essential for debugging and user experience, but the primary fix (field name alignment) takes precedence.

**Independent Test**: Can be tested by sending malformed requests directly to the API and verifying appropriate HTTP status codes and error messages are returned.

**Acceptance Scenarios**:

1. **Given** a request with invalid data is sent to the chat endpoint, **When** validation fails, **Then** a 400 Bad Request response with a descriptive error message is returned (not 500)
2. **Given** a request fails due to a genuine server error, **When** the exception is caught, **Then** a 500 Internal Server Error is returned with appropriate logging

---

### Edge Cases

- What happens when the chat message is empty? (Should return 400 Bad Request with "message cannot be empty" or similar)
- What happens when the backend service is unavailable? (Should return 503 Service Unavailable or 500, not mask as different error)
- What happens when the message exceeds maximum length? (Should return 400 with appropriate length validation error)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Frontend chat component MUST send user messages using the `message` field name in the request payload
- **FR-002**: Backend MUST preserve original HTTP exception status codes (400, 401, 403, etc.) instead of converting all errors to 500
- **FR-003**: Backend MUST log detailed error information (exception type, message, stack trace) for genuine server errors
- **FR-004**: Backend MUST re-raise HTTP exceptions without modification to preserve original status codes and error details
- **FR-005**: Chat requests that fail validation MUST return appropriate 4xx status codes with descriptive error messages

### Key Entities

- **Chat Message Request**: The payload sent from frontend to backend containing the user's message
  - Required field: `message` (string) - the user's question or input
  - Optional fields: session_id, context, etc. as defined by backend schema
- **Chat Error Response**: The error payload returned when requests fail
  - Contains: status code, error detail/message

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully send and receive chat messages through the widget (100% success rate for valid messages)
- **SC-002**: Invalid requests return appropriate 4xx error codes instead of 500 errors
- **SC-003**: Error messages provide actionable information for debugging (include error type and description)
- **SC-004**: Zero field mismatch errors in production logs after deployment

## Assumptions

- The backend schema expects a `message` field (not `query`) based on the user description
- The frontend ChatKit.tsx component is the source of chat message requests
- The backend chat.py endpoint handles incoming chat requests
- After backend changes are deployed, the HuggingFace Space requires manual restart

## Out of Scope

- Changes to chat functionality beyond field name alignment
- Performance optimizations to the chat system
- Addition of new chat features
- UI/UX changes to the chat widget appearance

## Dependencies

- Frontend: ChatKit.tsx (lines 124-126) - location of the field name to change
- Backend: chat.py (lines 108-113) - location of exception handling to fix
- Deployment: HuggingFace Space hosting the backend (requires manual restart)
