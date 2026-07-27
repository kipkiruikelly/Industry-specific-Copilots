import pytest
from src.eval.ai_evaluator import AIQualityEvaluator
from src.rag.store import ClinicalDocument


def test_ai_quality_evaluator_precision_recall():
    evaluator = AIQualityEvaluator()

    doc1 = ClinicalDocument(id="doc-1", patient_id="P-1", content="Metformin dosage guidelines.")
    doc2 = ClinicalDocument(id="doc-2", patient_id="P-2", content="Warfarin interaction warnings.")

    score = evaluator.evaluate(
        retrieved_docs=[doc1, doc2],
        expected_doc_ids=["doc-1"],
        generated_synthesis="Metformin dosage guidelines summary.",
    )

    assert score.retrieval_precision == 0.5
    assert score.retrieval_recall == 1.0
    assert score.overall_quality_score > 0.5
    assert score.hallucination_rate < 0.5
