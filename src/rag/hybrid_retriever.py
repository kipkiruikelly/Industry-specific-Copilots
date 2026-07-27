import math
import numpy as np
from typing import Any, Dict, List, Optional
from src.rag.store import ClinicalDocument, InMemoryVectorStore, SearchResult


class MockEmbeddingGenerator:
    """Deterministic embedding generator for testing and demonstration."""
    def embed_text(self, text: str, dimension: int = 1536) -> List[float]:
        # Generate stable normalized pseudorandom vector seeded by text length and hash
        seed = sum(ord(c) for c in text) % 1000
        rng = np.random.RandomState(seed)
        vec = rng.randn(dimension)
        return (vec / np.linalg.norm(vec)).tolist()


class HybridRetriever:
    """
    Hybrid RAG Retrieval Engine combining Dense Vector Cosine Similarity
    with Lexical BM25 term matching using Reciprocal Rank Fusion (RRF).
    """

    def __init__(self, vector_store: InMemoryVectorStore, rrf_k: int = 60):
        self.vector_store = vector_store
        self.rrf_k = rrf_k
        self.embedder = MockEmbeddingGenerator()

    def _compute_bm25_scores(
        self, query: str, docs: List[ClinicalDocument], metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Lexical BM25 scoring algorithm over clinical text content."""
        query_terms = [t.lower() for t in query.split() if len(t) > 2]
        if not query_terms:
            return []

        filtered_docs = [
            doc for doc in docs if self.vector_store._matches_filter(doc, metadata_filter)
        ]

        if not filtered_docs:
            return []

        doc_terms_list = [doc.content.lower().split() for doc in filtered_docs]
        doc_lens = [len(terms) for terms in doc_terms_list]
        avg_doc_len = sum(doc_lens) / max(len(doc_lens), 1)

        k1, b = 1.5, 0.75
        num_docs = len(filtered_docs)
        results: List[SearchResult] = []

        for idx, doc in enumerate(filtered_docs):
            terms = doc_terms_list[idx]
            doc_len = doc_lens[idx]
            score = 0.0

            for q_term in query_terms:
                doc_freq = sum(1 for d_terms in doc_terms_list if q_term in d_terms)
                if doc_freq == 0:
                    continue

                idf = math.log((num_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
                term_freq = terms.count(q_term)
                numerator = term_freq * (k1 + 1)
                denominator = term_freq + k1 * (1 - b + b * (doc_len / max(avg_doc_len, 1e-5)))
                score += idf * (numerator / max(denominator, 1e-5))

            if score > 0:
                results.append(SearchResult(document=doc, score=score, retrieval_type="bm25"))

        results.sort(key=lambda x: x.score, reverse=True)
        return results

    async def search(
        self, query: str, top_k: int = 5, metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Perform Hybrid Search utilizing Reciprocal Rank Fusion (RRF).
        """
        # 1. Dense Semantic Vector Search
        query_vec = self.embedder.embed_text(query)
        dense_results = await self.vector_store.similarity_search(
            query_vector=query_vec, top_k=top_k * 2, metadata_filter=metadata_filter
        )

        # 2. Lexical BM25 Search
        bm25_results = self._compute_bm25_scores(
            query=query, docs=self.vector_store._docs, metadata_filter=metadata_filter
        )

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        doc_map: Dict[str, ClinicalDocument] = {}

        for rank, res in enumerate(dense_results, start=1):
            doc_map[res.document.id] = res.document
            rrf_scores[res.document.id] = rrf_scores.get(res.document.id, 0.0) + 1.0 / (self.rrf_k + rank)

        for rank, res in enumerate(bm25_results[: top_k * 2], start=1):
            doc_map[res.document.id] = res.document
            rrf_scores[res.document.id] = rrf_scores.get(res.document.id, 0.0) + 1.0 / (self.rrf_k + rank)

        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        return [
            SearchResult(document=doc_map[doc_id], score=score, retrieval_type="hybrid")
            for doc_id, score in sorted_docs[:top_k]
        ]
