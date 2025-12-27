"""
Database Manager with Connection Pooling and Retry Logic

Provides resilient database operations for Neon Postgres with:
- SQLAlchemy connection pooling with pool_pre_ping
- Exponential backoff retry logic using tenacity
- Graceful degradation on connection failures
"""
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, InterfaceError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

from ..config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages database connections with pooling and retry logic.
    Implements graceful degradation when database is unavailable.
    """

    def __init__(self):
        self._engine = None
        self._session_factory = None
        self._is_healthy = False
        self._initialize_engine()

    def _initialize_engine(self):
        """
        Initialize SQLAlchemy engine with connection pooling.
        """
        if not settings.database_url:
            logger.warning("DATABASE_URL not configured - database features disabled")
            return

        try:
            # Configure engine with connection pooling
            self._engine = create_engine(
                settings.database_url,
                pool_size=settings.db_pool_size,
                max_overflow=settings.db_max_overflow,
                pool_recycle=settings.db_pool_recycle,
                pool_pre_ping=True,  # Validates connections before use
                pool_timeout=30,
                echo=settings.debug
            )
            self._session_factory = sessionmaker(bind=self._engine)
            self._is_healthy = True
            logger.info("Database engine initialized with connection pooling")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {str(e)}")
            self._is_healthy = False

    @property
    def is_available(self) -> bool:
        """Check if database is available."""
        return self._engine is not None and self._is_healthy

    @contextmanager
    def get_session(self):
        """
        Context manager for database sessions.
        Handles commit/rollback automatically.
        """
        if not self.is_available:
            yield None
            return

        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type((OperationalError, InterfaceError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def execute_with_retry(self, query: str, params: Dict = None) -> Optional[List[Dict]]:
        """
        Execute a query with exponential backoff retry.

        Args:
            query: SQL query string
            params: Optional query parameters

        Returns:
            List of result dictionaries, or None on failure
        """
        if not self.is_available:
            logger.warning("Database unavailable - skipping query execution")
            return None

        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(query), params or {})
                if result.returns_rows:
                    return [dict(row._mapping) for row in result]
                connection.commit()
                return []
        except OperationalError as e:
            logger.error(f"Database operational error: {str(e)}")
            self._handle_connection_error()
            raise
        except InterfaceError as e:
            logger.error(f"Database interface error: {str(e)}")
            self._handle_connection_error()
            raise

    def _handle_connection_error(self):
        """
        Handle connection errors by attempting to reinitialize.
        """
        logger.warning("Attempting to reinitialize database connection...")
        self._is_healthy = False
        try:
            if self._engine:
                self._engine.dispose()
            self._initialize_engine()
        except Exception as e:
            logger.error(f"Failed to reinitialize database: {str(e)}")

    def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check.

        Returns:
            Dict with health status and details
        """
        if not self.is_available:
            return {
                "healthy": False,
                "message": "Database not configured or unavailable",
                "pool_size": 0
            }

        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                pool_status = self._engine.pool.status()
                return {
                    "healthy": True,
                    "message": "Database connection healthy",
                    "pool_status": pool_status
                }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "healthy": False,
                "message": str(e),
                "pool_size": 0
            }

    def create_conversation(self, session_id: str, metadata: Dict = None) -> bool:
        """
        Create a new conversation record.

        Args:
            session_id: Unique session identifier
            metadata: Optional conversation metadata

        Returns:
            True if created successfully, False otherwise
        """
        if not self.is_available:
            logger.warning(f"DB unavailable - conversation {session_id} not persisted")
            return False

        try:
            import json
            from datetime import datetime

            query = """
                INSERT INTO conversations (id, created_at, updated_at, metadata)
                VALUES (:id, :created_at, :updated_at, :metadata)
                ON CONFLICT (id) DO NOTHING
            """
            params = {
                "id": session_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "metadata": json.dumps(metadata or {})
            }
            self.execute_with_retry(query, params)
            logger.info(f"Created conversation: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create conversation: {str(e)}")
            return False

    def get_conversation(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve a conversation by ID.

        Args:
            session_id: Session identifier

        Returns:
            Conversation dict or None
        """
        if not self.is_available:
            return None

        try:
            query = "SELECT * FROM conversations WHERE id = :session_id"
            results = self.execute_with_retry(query, {"session_id": session_id})
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to get conversation: {str(e)}")
            return None

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        citations: List[str] = None,
        selected_text: str = ""
    ) -> bool:
        """
        Add a message to a conversation.

        Args:
            session_id: Session identifier
            role: Message role (user, assistant, system)
            content: Message content
            citations: Optional list of citation IDs
            selected_text: Optional selected text context

        Returns:
            True if added successfully, False otherwise
        """
        if not self.is_available:
            logger.warning(f"DB unavailable - message not persisted for session {session_id}")
            return False

        try:
            import json
            import uuid
            from datetime import datetime

            # Validate role
            if role not in ["user", "assistant", "system"]:
                role = "user"

            query = """
                INSERT INTO messages (id, session_id, role, content, timestamp, citations, selected_text)
                VALUES (:id, :session_id, :role, :content, :timestamp, :citations, :selected_text)
            """
            params = {
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow(),
                "citations": json.dumps(citations or []),
                "selected_text": selected_text or ""
            }
            self.execute_with_retry(query, params)
            logger.debug(f"Added message to conversation {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add message: {str(e)}")
            return False

    def get_messages(self, session_id: str, limit: int = 50) -> List[Dict]:
        """
        Get messages for a conversation.

        Args:
            session_id: Session identifier
            limit: Maximum messages to retrieve

        Returns:
            List of message dicts
        """
        if not self.is_available:
            return []

        try:
            query = """
                SELECT * FROM messages
                WHERE session_id = :session_id
                ORDER BY timestamp ASC
                LIMIT :limit
            """
            results = self.execute_with_retry(query, {"session_id": session_id, "limit": limit})
            return results or []
        except Exception as e:
            logger.error(f"Failed to get messages: {str(e)}")
            return []

    def validate_schema(self) -> bool:
        """
        Validate that required database tables exist.

        Returns:
            True if schema is valid, False otherwise
        """
        if not self.is_available:
            return False

        try:
            # Check conversations table
            conv_query = """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'conversations'
            """
            conv_cols = self.execute_with_retry(conv_query)
            if not conv_cols:
                logger.error("conversations table not found")
                return False

            conv_columns = {row['column_name'] for row in conv_cols}
            required_conv = {'id', 'created_at', 'updated_at', 'metadata'}
            if not required_conv.issubset(conv_columns):
                missing = required_conv - conv_columns
                logger.error(f"Missing columns in conversations: {missing}")
                return False

            # Check messages table
            msg_query = """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'messages'
            """
            msg_cols = self.execute_with_retry(msg_query)
            if not msg_cols:
                logger.error("messages table not found")
                return False

            msg_columns = {row['column_name'] for row in msg_cols}
            required_msg = {'id', 'session_id', 'role', 'content', 'timestamp', 'citations', 'selected_text'}
            if not required_msg.issubset(msg_columns):
                missing = required_msg - msg_columns
                logger.error(f"Missing columns in messages: {missing}")
                return False

            logger.info("Database schema validation passed")
            return True
        except Exception as e:
            logger.error(f"Schema validation error: {str(e)}")
            return False

    def close(self):
        """Close database connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database connections closed")


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """
    Get or create the singleton DatabaseManager instance.

    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
