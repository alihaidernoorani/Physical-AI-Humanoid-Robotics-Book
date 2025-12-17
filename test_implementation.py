import sys
import os
from pathlib import Path

def test_backend_setup():
    """Test that all backend components can be imported and initialized."""
    print("Testing backend setup...")

    # Change to the backend directory to ensure proper imports
    backend_dir = Path(__file__).parent / "backend"
    original_cwd = os.getcwd()
    os.chdir(backend_dir)

    try:
        # Add the current directory to Python path
        sys.path.insert(0, str(Path.cwd()))

        # Test importing main components
        from src.config.settings import settings
        print("✓ Settings imported successfully")

        from src.api.main import app
        print("✓ FastAPI app created successfully")

        from src.services.embedding_service import EmbeddingService
        service = EmbeddingService()
        print("✓ Embedding service initialized successfully")

        # Test basic embedding
        test_text = "This is a test sentence."
        embedding = service.generate_embedding(test_text)
        print(f"✓ Embedding generated successfully, length: {len(embedding)}")

        from src.services.retrieval_service import RetrievalService
        print("✓ Retrieval service imported successfully")

        from src.services.chat_service import ChatService
        print("✓ Chat service imported successfully")

        from src.utils.text_chunker import TextChunker
        print("✓ Text chunker imported successfully")

        print("\nAll backend components loaded successfully!")
        return True

    except Exception as e:
        print(f"✗ Error testing backend: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

def test_frontend_components():
    """Verify frontend component files exist."""
    print("\nTesting frontend setup...")

    # Change to the project root directory
    project_root = Path(__file__).parent
    frontend_files = [
        "frontend/src/components/ChatInterface/ChatWindow.jsx",
        "frontend/src/components/ChatInterface/ChatWindow.css",
        "frontend/src/components/RAG/TextSelectionHandler.jsx",
        "frontend/src/components/RAG/CitationDisplay.jsx",
        "frontend/src/services/chatApi.js"
    ]

    all_exist = True
    for file_path in frontend_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False

    if all_exist:
        print("\nAll frontend components exist!")
    else:
        print("\nSome frontend components are missing!")

    return all_exist

if __name__ == "__main__":
    print("Running integration tests...\n")

    backend_ok = test_backend_setup()
    frontend_ok = test_frontend_components()

    print(f"\nTest Results:")
    print(f"Backend: {'PASS' if backend_ok else 'FAIL'}")
    print(f"Frontend: {'PASS' if frontend_ok else 'FAIL'}")

    if backend_ok and frontend_ok:
        print("\n✓ All tests passed! Implementation is complete.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)