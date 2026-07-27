from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.rag.store import ClinicalDocument, SearchResult


class BaseVectorProvider(ABC):
    """
    Abstract Vector Database Provider Interface.
    Enables zero-code provider switching across pgvector, Qdrant, Pinecone, Milvus, and InMemory.
    """

    @abstractmethod
    async def add_documents(self, documents: List[ClinicalDocument], tenant_id: str = "default") -> None:
        pass

    @abstractmethod
    async def similarity_search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default",
    ) -> List[SearchResult]:
        pass
