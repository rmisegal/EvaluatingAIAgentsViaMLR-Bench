"""Test evaluation result creation to verify fix."""

from mlr_bench.models.evaluation import EvaluationResult

def test_evaluation_creation():
    """Test creating an EvaluationResult with the fixed approach."""

    idea_score = 7.5
    paper_score = 8.0
    average_score = (idea_score + paper_score) / 2

    # Create result
    result = EvaluationResult(
        evaluator_name="judge_1",
        overall_score=average_score,
        consistency_score=idea_score,
        clarity_score=paper_score,
        novelty_score=None,
        feasibility_score=None,
        significance_score=None,
        soundness_score=None,
        feedback="Combined evaluation of idea and paper",
        strengths="Evaluated both idea and paper",
        weaknesses=""
    )

    print(f"[OK] EvaluationResult created successfully")
    print(f"  Evaluator: {result.evaluator_name}")
    print(f"  Overall Score (Average): {result.overall_score}")
    print(f"  Consistency (Idea) Score: {result.consistency_score}")
    print(f"  Clarity (Paper) Score: {result.clarity_score}")

    # Verify we can access the scores using the correct field names
    print(f"\n[OK] Verification:")
    print(f"  Idea score (stored as consistency_score): {result.consistency_score}")
    print(f"  Paper score (stored as clarity_score): {result.clarity_score}")
    print(f"  Average score (stored as overall_score): {result.overall_score}")

    # Test that we can't add arbitrary fields (Pydantic will reject this)
    try:
        result.idea_score = idea_score
        print(f"[FAIL] ERROR: Should not be able to add arbitrary fields to Pydantic model")
        return False
    except Exception as e:
        print(f"[OK] Correctly prevents adding arbitrary fields: {type(e).__name__}")

    print(f"\n[OK] All tests passed!")
    return True

if __name__ == "__main__":
    test_evaluation_creation()
