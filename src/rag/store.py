import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ClinicalDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    vector: Optional[List[float]] = None
    required_clearance: int = 1
    department: str = "general"


class SearchResult(BaseModel):
    document: ClinicalDocument
    score: float
    retrieval_type: str  # "dense", "bm25", "hybrid"


class VectorStoreInterface:
    """
    Abstract Interface for Vector Storage and Semantic Search Engine.
    """

    async def add_documents(self, documents: List[ClinicalDocument]) -> None:
        raise NotImplementedError

    async def similarity_search(
        self, query_vector: List[float], top_k: int = 5, metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        raise NotImplementedError


class InMemoryVectorStore(VectorStoreInterface):
    """
    Production-grade in-memory Vector Index implementation with metadata filter support.
    Uses Cosine Similarity for dense retrieval.
    """

    def __init__(self):
        self._docs: List[ClinicalDocument] = []

    async def add_documents(self, documents: List[ClinicalDocument]) -> None:
        self._docs.extend(documents)

    def _matches_filter(self, doc: ClinicalDocument, metadata_filter: Optional[Dict[str, Any]]) -> bool:
        if not metadata_filter:
            return True

        if "required_clearance" in metadata_filter:
            clearance_rule = metadata_filter["required_clearance"]
            if isinstance(clearance_rule, dict) and "$lte" in clearance_rule:
                if doc.required_clearance > clearance_rule["$lte"]:
                    return False

        if "department" in metadata_filter:
            dept_rule = metadata_filter["department"]
            if isinstance(dept_rule, dict) and "$in" in dept_rule:
                if doc.department not in dept_rule["$in"]:
                    return False

        return True

    async def similarity_search(
        self, query_vector: List[float], top_k: int = 5, metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        if not query_vector or not self._docs:
            return []

        import numpy as np

        q_vec = np.array(query_vector, dtype=float)
        q_norm = np.linalg.norm(q_vec) + 1e-10

        results: List[SearchResult] = []

        for doc in self._docs:
            if not self._matches_filter(doc, metadata_filter):
                continue

            if doc.vector is None:
                continue

            d_vec = np.array(doc.vector, dtype=float)
            d_norm = np.linalg.norm(d_vec) + 1e-10
            score = float(np.dot(q_vec, d_vec) / (q_norm * d_norm))

            results.append(SearchResult(document=doc, score=score, retrieval_type="dense"))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
