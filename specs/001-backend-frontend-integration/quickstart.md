# Quickstart Guide: Backend-Frontend Integration

## Prerequisites
- Python 3.11+
- Node.js 20+
- Git
- Access to OpenAI API key
- Qdrant vector database (local or remote)

## Setup Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. Start the backend server:
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

## Setup Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Backend Cleanup Process
1. Before running cleanup, verify core functionality:
   ```bash
   # Test that core endpoints are working
   curl http://localhost:8000/health
   ```

2. Run the cleanup script (details in tasks.md):
   - Remove legacy directories: `src/`, `tests/`
   - Remove legacy files: `main.py`, `src/config.py`, `CONFIGURATION.md`
   - Archive ambiguous files: `index_textbook.py`, `README.md`, `=1.24.3`

## Frontend Integration
1. The ChatKit UI will be integrated into the existing Docusaurus structure
2. API endpoints will be mapped to frontend components:
   - `/chat` → Chat interface
   - `/translate` → Translation service
   - `/personalize` → Personalization service

## Verification Steps
1. Confirm backend endpoints are functional after cleanup
2. Test ChatKit UI integration with backend APIs
3. Verify translation and personalization features work
4. Ensure all core functionality remains intact