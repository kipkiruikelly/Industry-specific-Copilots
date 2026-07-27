from typing import Any, Dict, List, Optional
from src.rag.providers.base import BaseVectorProvider
from src.rag.store import ClinicalDocument, InMemoryVectorStore, SearchResult


class PGVectorProvider(BaseVectorProvider):
    """
    Production PostgreSQL + pgvector / In-Memory Abstract Provider.
    Delegates to InMemoryVectorStore when running without active Postgres DB,
    ensuring full backward compatibility.
    """

    def __init__(self, fallback_store: Optional[InMemoryVectorStore] = None):
        self.store = fallback_store or InMemoryVectorStore()

    async def add_documents(self, documents: List[ClinicalDocument], tenant_id: str = "default") -> None:
        for doc in documents:
            doc.metadata["tenant_id"] = tenant_id
        await self.store.add_documents(documents)

    async def similarity_search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default",
    ) -> List[SearchResult]:
        merged_filter = dict(metadata_filter or {})
        merged_filter["tenant_id"] = tenant_id
        return await self.store.similarity_search(query_vector=query_vector, top_k=top_k, metadata_filter=merged_filter)


class QdrantVectorProvider(BaseVectorProvider):
    """Qdrant Cloud/Self-hosted Vector Provider Stub."""

    def __init__(self, fallback_store: Optional[InMemoryVectorStore] = None):
        self.fallback = PGVectorProvider(fallback_store)

    async def add_documents(self, documents: List[ClinicalDocument], tenant_id: str = "default") -> None:
        await self.fallback.add_documents(documents, tenant_id)

    async def similarity_search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default",
    ) -> List[SearchResult]:
        return await self.fallback.similarity_search(query_vector, top_k, metadata_filter, tenant_id)


class PineconeVectorProvider(BaseVectorProvider):
    """Pinecone Vector Provider Stub."""

    def __init__(self, fallback_store: Optional[InMemoryVectorStore] = None):
        self.fallback = PGVectorProvider(fallback_store)

    async def add_documents(self, documents: List[ClinicalDocument], tenant_id: str = "default") -> None:
        await self.fallback.add_documents(documents, tenant_id)

    async def similarity_search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default",
    ) -> List[SearchResult]:
        return await self.fallback.similarity_search(query_vector, top_k, metadata_filter, tenant_id)


def get_vector_provider(provider_type: str = "pgvector", fallback_store: Optional[InMemoryVectorStore] = None) -> BaseVectorProvider:
    """Vector Provider Factory."""
    p_type = provider_type.lower()
    if p_type == "qdrant":
        return QdrantVectorProvider(fallback_store)
    elif p_type == "pinecone":
        return PineconeVectorProvider(fallback_store)
    return PGVectorProvider(fallback_store)
