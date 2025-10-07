"""Simple tools for MLR-Bench agents."""

from typing import List, Dict, Any
import json
from datetime import datetime


def search_papers(query: str, max_results: int = 5) -> dict:
    """Search for research papers (mock implementation for educational purposes).
    
    Args:
        query: Search query for papers
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary with search results
    """
    # Mock implementation - returns simulated results
    mock_papers = [
        {
            "title": f"Research on {query} - Paper {i+1}",
            "authors": f"Author {i+1} et al.",
            "year": 2024 - i,
            "abstract": f"This paper explores {query} using novel methods...",
            "relevance": f"Highly relevant to {query}"
        }
        for i in range(min(max_results, 3))
    ]
    
    return {
        "status": "success",
        "query": query,
        "results": mock_papers,
        "count": len(mock_papers)
    }


def calculate_average_score(scores: List[float]) -> dict:
    """Calculate average score from a list of scores.
    
    Args:
        scores: List of numerical scores
        
    Returns:
        Dictionary with average and statistics
    """
    if not scores:
        return {
            "status": "error",
            "error": "No scores provided"
        }
    
    valid_scores = [s for s in scores if isinstance(s, (int, float))]
    
    if not valid_scores:
        return {
            "status": "error",
            "error": "No valid scores found"
        }
    
    avg = sum(valid_scores) / len(valid_scores)
    
    return {
        "status": "success",
        "average": round(avg, 2),
        "min": min(valid_scores),
        "max": max(valid_scores),
        "count": len(valid_scores)
    }


def parse_json_response(text: str) -> dict:
    """Parse JSON from text response.
    
    Args:
        text: Text containing JSON
        
    Returns:
        Parsed JSON object or error
    """
    try:
        # Try to find JSON in text
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start == -1 or end == 0:
            return {
                "status": "error",
                "error": "No JSON found in text"
            }
        
        json_str = text[start:end]
        parsed = json.loads(json_str)
        
        return {
            "status": "success",
            "data": parsed
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error": f"JSON parsing failed: {str(e)}"
        }


def extract_scores_from_text(text: str) -> dict:
    """Extract numerical scores from text.
    
    Args:
        text: Text containing scores
        
    Returns:
        Dictionary with extracted scores
    """
    import re
    
    scores = {}
    
    # Common score patterns
    patterns = {
        'consistency': r'consistency[:\s]+(\d+(?:\.\d+)?)',
        'clarity': r'clarity[:\s]+(\d+(?:\.\d+)?)',
        'novelty': r'novelty[:\s]+(\d+(?:\.\d+)?)',
        'feasibility': r'feasibility[:\s]+(\d+(?:\.\d+)?)',
        'significance': r'significance[:\s]+(\d+(?:\.\d+)?)',
        'soundness': r'soundness[:\s]+(\d+(?:\.\d+)?)',
        'overall': r'overall[:\s]+(\d+(?:\.\d+)?)'
    }
    
    text_lower = text.lower()
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            try:
                score = float(match.group(1))
                if 0 <= score <= 10:
                    scores[key] = score
            except ValueError:
                continue
    
    return {
        "status": "success",
        "scores": scores,
        "count": len(scores)
    }


def save_to_file(content: str, filename: str) -> dict:
    """Save content to a file (mock implementation).
    
    Args:
        content: Content to save
        filename: Target filename
        
    Returns:
        Status dictionary
    """
    # Mock implementation - just returns success
    return {
        "status": "success",
        "message": f"Content saved to {filename}",
        "filename": filename,
        "size": len(content),
        "timestamp": datetime.now().isoformat()
    }


def execute_python_code(code: str) -> dict:
    """Execute Python code (mock implementation for safety).
    
    Args:
        code: Python code to execute
        
    Returns:
        Execution results
    """
    # Mock implementation - does not actually execute code for safety
    return {
        "status": "success",
        "message": "Code execution simulated (not actually run for safety)",
        "code_length": len(code),
        "lines": len(code.split('\n')),
        "note": "In production, this would use a sandboxed Python executor"
    }


def format_paper_section(title: str, content: str) -> dict:
    """Format a paper section with proper structure.
    
    Args:
        title: Section title
        content: Section content
        
    Returns:
        Formatted section
    """
    formatted = f"## {title}\n\n{content}\n"
    
    return {
        "status": "success",
        "formatted": formatted,
        "title": title,
        "word_count": len(content.split())
    }
