import pytest
from src.rag.hybrid_retriever import HybridRetriever, MockEmbeddingGenerator
from src.rag.store import ClinicalDocument, InMemoryVectorStore
from src.security.rbac import UserAuthContext


@pytest.mark.asyncio
async def test_hybrid_retriever_and_rbac_filtering():
    store = InMemoryVectorStore()
    retriever = HybridRetriever(vector_store=store)
    embedder = MockEmbeddingGenerator()

    # Doc 1: Clearance Level 2, Department: endocrinology
    doc1 = ClinicalDocument(
        id="doc-endo",
        patient_id="P-1",
        content="Metformin guidelines for Type 2 Diabetes treatment.",
        required_clearance=2,
        department="endocrinology",
        vector=embedder.embed_text("Metformin guidelines for Type 2 Diabetes treatment."),
    )

    # Doc 2: Clearance Level 3, Department: oncology
    doc2 = ClinicalDocument(
        id="doc-onco",
        patient_id="P-2",
        content="Chemotherapy dosing guidelines for Stage IV Oncology.",
        required_clearance=3,
        department="oncology",
        vector=embedder.embed_text("Chemotherapy dosing guidelines for Stage IV Oncology."),
    )

    await store.add_documents([doc1, doc2])

    # Nurse Auth Context (Clearance level 2, endocrinology only)
    nurse_auth = UserAuthContext(
        user_id="nurse_1",
        role="nurse",
        assigned_departments=["endocrinology"],
    )

    filter_dict = {
        "required_clearance": {"$lte": 2},
        "department": {"$in": ["endocrinology"]},
    }

    results = await retriever.search(query="Metformin dosage", top_k=5, metadata_filter=filter_dict)

    assert len(results) == 1
    assert results[0].document.id == "doc-endo"
