from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RAG Backend API",
    description="Backend API for RAG chatbot with OpenAI Agents SDK, Cohere embeddings, and Gemini-2.5-flash",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://alihaidernoorani.github.io", "https://alihaidernoorani.github.io/Physical-AI-Humanoid-Robotics-Book", "http://localhost:3000", "http://localhost:3001", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routes
from .chat import router as chat_router

app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "RAG Backend API is running with OpenAI Agents SDK and Gemini bridge"}

@app.get("/api/v1/health")
def health_check():
    from .chat import health_check as chat_health_check
    return chat_health_check()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)