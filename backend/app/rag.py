from typing import Dict, List, Optional, Literal
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from .config import settings

logger = logging.getLogger(__name__)

InputType = Literal["search_query", "search_document"]


# -----------------------------
# Cohere Embedding Service
# -----------------------------

class CohereEmbeddingService:
    API_TIMEOUT = 30

    def __init__(self):
        self.client = cohere.Client(
            api_key=settings.cohere_api_key,
            timeout=self.API_TIMEOUT
        )
        self.model = settings.embedding_model

    def generate_single_embedding(
        self,
        text: str,
        input_type: InputType = "search_query"
    ) -> List[float]:
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type=input_type
        )
        return response.embeddings[0]


# -----------------------------
# Qdrant Retrieval Service
# -----------------------------

class QdrantRetrievalService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = settings.qdrant_collection_name
        self.relevance_threshold = settings.relevance_threshold
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,
                    distance=models.Distance.COSINE
                )
            )

    def _format_result(self, point) -> Dict:
        return {
            "chunk_id": str(point.id),
            "content": point.payload.get("content", ""),
            "score": point.score,
            "module": point.payload.get("metadata", {}).get("module", ""),
            "chapter": point.payload.get("metadata", {}).get("chapter", ""),
            "subsection": point.payload.get("metadata", {}).get("subsection", ""),
            "page_reference": point.payload.get("metadata", {}).get("page_reference", "")
        }

    def _filter_by_relevance(self, results: List[Dict]) -> List[Dict]:
        return [r for r in results if r["score"] >= self.relevance_threshold]

    def _build_filter(self, filters: Optional[Dict]) -> Optional[models.Filter]:
        if not filters:
            return None

        conditions = []
        for key, value in filters.items():
            if isinstance(value, list):
                conditions.append(
                    models.FieldCondition(
                        key=f"metadata.{key}",
                        match=models.MatchAny(any=value)
                    )
                )
            else:
                conditions.append(
                    models.FieldCondition(
                        key=f"metadata.{key}",
                        match=models.MatchValue(value=value)
                    )
                )

        return models.Filter(must=conditions) if conditions else None

    def search_chunks_full_book(
        self,
        query_embedding: List[float],
        limit: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:

        qdrant_filter = self._build_filter(filters)

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit * 2,
            with_payload=True,
            prefetch=[
                models.Prefetch(
                    filter=qdrant_filter,
                    limit=limit * 2
                )
            ] if qdrant_filter else None
        )

        points = response.points or []

        logger.info(f"Qdrant returned {len(points)} points")

        formatted = [self._format_result(p) for p in points]
        filtered = self._filter_by_relevance(formatted)

        return filtered[:limit]

    def search_chunks_per_page(
        self,
        query_embedding: List[float],
        selected_text_embedding: List[float],
        limit: int = 5
    ) -> List[Dict]:

        results = {}

        for embedding in (selected_text_embedding, query_embedding):
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=embedding,
                limit=limit,
                with_payload=True
            )

            for p in response.points or []:
                results[p.id] = self._format_result(p)

        sorted_results = sorted(
            results.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        filtered = self._filter_by_relevance(sorted_results)
        return filtered[:limit]

    def health_check(self) -> bool:
        try:
            self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False


# -----------------------------
# RAG Service
# -----------------------------

class RAGService:
    def __init__(self):
        self.cohere_service = CohereEmbeddingService()
        self.qdrant_service = QdrantRetrievalService()

    def retrieve_context(
        self,
        query: str,
        retrieval_mode: str = "full-book",
        selected_text: Optional[str] = None,
        metadata_filters: Optional[Dict] = None
    ) -> List[Dict]:

        query_embedding = self.cohere_service.generate_single_embedding(
            query,
            input_type="search_query"
        )

        if retrieval_mode == "full-book":
            return self.qdrant_service.search_chunks_full_book(
                query_embedding=query_embedding,
                limit=5,
                filters=metadata_filters
            )

        if not selected_text:
            return []

        selected_text_embedding = self.cohere_service.generate_single_embedding(
            selected_text,
            input_type="search_query"
        )

        return self.qdrant_service.search_chunks_per_page(
            query_embedding=query_embedding,
            selected_text_embedding=selected_text_embedding,
            limit=5
        )

    def health_check(self) -> bool:
        return self.qdrant_service.health_check()


rag_service = RAGService()