# Quickstart Guide: ChatWidget Stabilization

## Overview
This guide provides instructions for setting up, configuring, and testing the stabilized ChatWidget for the Physical AI & Humanoid Robotics textbook.

## Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git
- Access to backend API at `https://alihaidernoorani-deploy-docusaurus-book.hf.space/`

## 1. Local Development Setup

### Frontend Setup
```bash
# Clone the repository
git clone <repository-url>
cd Physical-AI-Humanoid-Robotics-Textbook

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables for development
echo "REACT_APP_API_BASE_URL=http://localhost:8000/api/v1" > .env.local

# Start the development server
npm start
```

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export API_BASE_URL=https://alihaidernoorani-deploy-docusaurus-book.hf.space/

# Start the backend server
python -m uvicorn app.main:app --reload --port 8000
```

## 2. Production Configuration

### Frontend Environment Configuration
For GitHub Pages deployment, configure the API base URL:

```bash
# In frontend/.env.production
REACT_APP_API_BASE_URL=https://alihaidernoorani-deploy-docusaurus-book.hf.space/api/v1
```

### Backend CORS Configuration
The backend should already allow requests from the GitHub Pages origin:

```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://alihaidernoorani.github.io"],  # GitHub Pages origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 3. Key Components

### ChatKit Component
Located at: `frontend/src/components/ChatKit/ChatKit.tsx`

The ChatKit component provides:
- Global chat interface
- Session management
- Message history
- Loading and error states
- Responsive design

### API Service
Located at: `frontend/src/services/api.js`

Handles communication with the backend API:
- Chat message sending/receiving
- Session creation
- Error handling
- Request/response formatting

## 4. Implementation Steps

### Step 1: Move ChatKit from Root.tsx to Layout
1. Remove ChatKit import and component from `frontend/src/theme/Root.tsx`
2. Add ChatKit to the appropriate Docusaurus Layout component
3. Ensure proper CSS positioning and z-index layering

### Step 2: Update API Configuration
1. Update the API base URL in `frontend/src/services/api.js` for production
2. Ensure the URL points to the deployed backend: `https://alihaidernoorani-deploy-docusaurus-book.hf.space/api/v1`

### Step 3: CSS and Positioning Fixes
1. Review `frontend/src/components/ChatKit/ChatKit.css` for positioning issues
2. Ensure proper z-index to appear above other content
3. Test responsive behavior on different screen sizes

## 5. Testing

### Frontend Tests
```bash
# Run frontend unit tests
cd frontend
npm test

# Run specific ChatKit tests
npm test -- --testPathPattern=ChatKit
```

### Integration Tests
```bash
# Run integration tests
cd backend
python -m pytest tests/integration/
```

### End-to-End Tests
```bash
# Test the complete flow from frontend to backend
cd backend
python -m pytest tests/test_rag_e2e_flow.py
```

## 6. Deployment

### Frontend Deployment (GitHub Pages)
```bash
# Build the frontend
cd frontend
npm run build

# The build output is in the build/ directory
# GitHub Pages will serve from the root of the repository
```

### Backend Deployment (Hugging Face Space)
The backend is deployed as a Space using the provided Docker configuration.
Updates are deployed by pushing changes to the repository.

## 7. Troubleshooting

### Common Issues

#### ChatWidget not appearing
- Check that the component is properly mounted in the layout
- Verify CSS is not hiding the component
- Check browser console for JavaScript errors

#### API requests failing
- Verify the API base URL is correctly configured
- Check CORS configuration on the backend
- Ensure the backend is accessible from the frontend origin

#### Session persistence issues
- Verify session IDs are being stored and transmitted correctly
- Check that sessions are properly initialized
- Ensure session state persists across page navigation

### Debugging Tips
- Use browser developer tools to inspect network requests
- Check the browser console for JavaScript errors
- Verify API responses using tools like Postman or curl
- Review backend logs for error messages

## 8. Validation Checklist

Before deployment, ensure:

- [ ] ChatWidget appears on all pages of the textbook website
- [ ] Open/close functionality works correctly
- [ ] Message sending and receiving works with backend
- [ ] Loading indicators display properly
- [ ] Error handling works as expected
- [ ] CSS positioning is correct on all screen sizes
- [ ] Session management works across page navigation
- [ ] API requests target the correct backend URL
- [ ] CORS configuration allows frontend requests
- [ ] All tests pass successfully