from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize rate limiter
# limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Backend API",
    description="Backend API for RAG chatbot with Cohere embeddings and Gemini-2.5-flash",
    version="1.0.0"
)

# Import and set up rate limiting
# from src.utils.rate_limiting import handle_rate_limit_error
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, handle_rate_limit_error)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routes
from src.api.rag import router as rag_router
# from src.api.embeddings import router as embeddings_router
# from src.api.user import router as user_router
# from src.api.translate import router as translate_router

app.include_router(rag_router, prefix="/api", tags=["rag"])
# app.include_router(embeddings_router, prefix="/api", tags=["embeddings"])
# app.include_router(user_router, prefix="/api", tags=["user"])
# app.include_router(translate_router, prefix="/api", tags=["translate"])

@app.get("/")
def read_root():
    return {"message": "RAG Backend API is running"}

@app.get("/api/health")
def health_check():
    from src.services.qdrant_service import qdrant_service
    from src.services.cohere_service import cohere_service
    from src.services.gemini_service import gemini_service

    # Check each service
    qdrant_healthy = qdrant_service.health_check()
    cohere_healthy = cohere_service.health_check()
    gemini_healthy = gemini_service.health_check()
    # For Neon DB, we would need to add a health check method to the database models
    # For now, assuming it's healthy if no exception occurs

    all_healthy = all([qdrant_healthy, cohere_healthy, gemini_healthy])

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "services": {
            "qdrant": qdrant_healthy,
            "cohere": cohere_healthy,
            "gemini": gemini_healthy,
            "neon_db": True  # Placeholder - would need actual DB health check
        },
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)