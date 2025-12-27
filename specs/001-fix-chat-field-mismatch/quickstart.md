# Quickstart: Fix Chat API Field Mismatch

**Feature Branch**: `001-fix-chat-field-mismatch`
**Date**: 2025-12-27

## Overview

This quickstart guides you through implementing a targeted bug fix for the chat widget field mismatch issue.

## Prerequisites

- Git access to the repository
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Access to HuggingFace Space for deployment

## Implementation Steps

### Step 1: Frontend Fix (ChatKit.tsx)

**File**: `frontend/src/components/ChatKit/ChatKit.tsx`
**Lines**: 124-126

**Change**: Rename `query` to `message` in the sendMessage call

```typescript
// Before (line 124-126)
const response = await chatService.sendMessage({
  query: message,
  session_id: currentSessionId
});

// After
const response = await chatService.sendMessage({
  message: message,
  session_id: currentSessionId
});
```

### Step 2: Backend Fix (chat.py)

**File**: `backend/app/chat.py`
**Lines**: 108-113

**Change**: Add HTTPException pass-through before generic Exception handler

```python
# Before (lines 108-113)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# After
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

### Step 3: Deploy Backend

1. Commit and push backend changes to the repository
2. Navigate to HuggingFace Space dashboard
3. Manually restart the Space to apply updates

### Step 4: Deploy Frontend

1. Build the frontend: `npm run build`
2. Deploy to GitHub Pages or your hosting platform

### Step 5: Verify Fix

1. Open the textbook website in a browser
2. Open the chat widget
3. Send a test message: "What is ROS 2?"
4. Verify:
   - Message is sent successfully (no 500 error)
   - AI response is displayed
   - Console shows no field mismatch errors

## Testing Checklist

- [ ] Frontend sends `message` field (not `query`)
- [ ] Backend returns 400 for empty messages (not 500)
- [ ] Valid messages receive AI responses
- [ ] Error messages display meaningful information
- [ ] No 500 errors in browser console for valid requests

## Rollback

If issues occur:

1. **Frontend**: Revert ChatKit.tsx change (change `message` back to `query`)
2. **Backend**: Remove the `except HTTPException: raise` line
3. Redeploy both services

## Success Criteria

- 100% success rate for valid chat messages
- 400 status code for validation errors (not 500)
- Zero field mismatch errors in production logs
