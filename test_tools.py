"""Test tool usage by agents."""

from mlr_bench.agent.tools import (
    search_papers,
    calculate_average_score,
    extract_scores_from_text,
    format_paper_section
)


def test_search_papers():
    """Test search_papers tool."""
    print("=" * 60)
    print("Testing search_papers tool")
    print("=" * 60)
    
    result = search_papers("deep learning", max_results=2)
    
    if result.get("status") == "success":
        print(f"✅ PASS: Found {result.get('count', 0)} papers")
        return True
    else:
        print(f"❌ FAIL: {result}")
        return False


def test_calculate_average():
    """Test calculate_average_score tool."""
    print("=" * 60)
    print("Testing calculate_average_score tool")
    print("=" * 60)
    
    scores = [7.5, 8.0, 6.5, 9.0, 7.0]
    result = calculate_average_score(scores)
    
    if result.get("status") == "success":
        avg = result.get("average")
        expected = 7.6
        if abs(avg - expected) < 0.1:
            print(f"✅ PASS: Average = {avg} (expected ~{expected})")
            return True
        else:
            print(f"❌ FAIL: Average = {avg}, expected {expected}")
            return False
    else:
        print(f"❌ FAIL: {result}")
        return False


def test_extract_scores():
    """Test extract_scores_from_text tool."""
    print("=" * 60)
    print("Testing extract_scores_from_text tool")
    print("=" * 60)
    
    text = """
    Evaluation Results:
    - Clarity: 8.5
    - Novelty: 7.0
    - Overall: 8.0
    """
    
    result = extract_scores_from_text(text)
    
    if result.get("status") == "success":
        scores = result.get("scores", {})
        if "clarity" in scores and "novelty" in scores:
            print(f"✅ PASS: Extracted {len(scores)} scores")
            print(f"  Scores: {scores}")
            return True
        else:
            print(f"❌ FAIL: Missing expected scores")
            return False
    else:
        print(f"❌ FAIL: {result}")
        return False


def test_format_section():
    """Test format_paper_section tool."""
    print("=" * 60)
    print("Testing format_paper_section tool")
    print("=" * 60)
    
    result = format_paper_section("Introduction", "This is the introduction.")
    
    if result.get("status") == "success":
        formatted = result.get("formatted", "")
        if "## Introduction" in formatted:
            print(f"✅ PASS: Section formatted correctly")
            return True
        else:
            print(f"❌ FAIL: Formatting incorrect")
            return False
    else:
        print(f"❌ FAIL: {result}")
        return False


def main():
    """Run all tool tests."""
    print()
    print("🔧 MLR-Bench Tool Tests")
    print()
    
    results = []
    
    results.append(("search_papers", test_search_papers()))
    results.append(("calculate_average_score", test_calculate_average()))
    results.append(("extract_scores_from_text", test_extract_scores()))
    results.append(("format_paper_section", test_format_section()))
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    return all(p for _, p in results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
