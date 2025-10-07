"""Test internet connectivity and MCP tools."""

import asyncio
from mlr_bench.mcp.mcp_tools import search_papers_mcp, execute_python_code_mcp


async def test_semantic_scholar():
    """Test Semantic Scholar API connection."""
    print("=" * 60)
    print("Testing Semantic Scholar API Connection")
    print("=" * 60)
    
    try:
        result = await search_papers_mcp("machine learning", limit=3)
        
        if result.get("status") == "success":
            papers = result.get("papers", [])
            print(f"✅ SUCCESS: Found {len(papers)} papers")
            print()
            
            for i, paper in enumerate(papers, 1):
                print(f"Paper {i}:")
                print(f"  Title: {paper.get('title', 'N/A')}")
                print(f"  Year: {paper.get('year', 'N/A')}")
                print(f"  Citations: {paper.get('citations', 0)}")
                print()
            
            return True
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


async def test_python_execution():
    """Test Python code execution."""
    print("=" * 60)
    print("Testing Python Code Execution")
    print("=" * 60)
    
    code = """
import sys
print("Hello from MLR-Bench!")
print(f"Python version: {sys.version}")
result = 2 + 2
print(f"2 + 2 = {result}")
"""
    
    try:
        result = await execute_python_code_mcp(code, timeout=10)
        
        if result.get("status") == "success":
            output = result.get("output", "")
            print(f"✅ SUCCESS: Code executed")
            print()
            print("Output:")
            print(output)
            return True
        else:
            print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


async def main():
    """Run all tests."""
    print()
    print("🧪 MLR-Bench Internet & MCP Tests")
    print()
    
    results = []
    
    # Test 1: Semantic Scholar
    result1 = await test_semantic_scholar()
    results.append(("Semantic Scholar API", result1))
    
    # Test 2: Python Execution
    result2 = await test_python_execution()
    results.append(("Python Execution", result2))
    
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
    success = asyncio.run(main())
    exit(0 if success else 1)
