"""MCP-based tools for agents."""

from typing import List, Dict, Any
from loguru import logger

from mlr_bench.mcp.mcp_client import MCPClient


# Global MCP client instance
_mcp_client = None


async def get_mcp_client() -> MCPClient:
    """Get or create MCP client instance.
    
    Returns:
        MCP client
    """
    global _mcp_client
    
    if _mcp_client is None:
        _mcp_client = MCPClient()
        
        # Connect to default servers
        await _mcp_client.connect_server(
            "semantic_scholar",
            {"type": "api", "url": "https://api.semanticscholar.org"}
        )
        
        await _mcp_client.connect_server(
            "python_executor",
            {"type": "local", "sandbox": True}
        )
        
        logger.info("MCP client initialized with default servers")
    
    return _mcp_client


async def search_papers_mcp(query: str, limit: int = 10) -> dict:
    """Search for research papers using Semantic Scholar API via MCP.
    
    Args:
        query: Search query
        limit: Maximum number of results
        
    Returns:
        Search results
    """
    client = await get_mcp_client()
    
    result = await client.call_tool(
        "semantic_scholar",
        "search_papers",
        {"query": query, "limit": limit}
    )
    
    if result.get("status") == "success":
        papers = result.get("data", [])
        
        # Format papers for agent consumption
        formatted_papers = []
        for paper in papers:
            formatted_papers.append({
                "title": paper.get("title", ""),
                "authors": [a.get("name", "") for a in paper.get("authors", [])],
                "year": paper.get("year"),
                "abstract": paper.get("abstract", ""),
                "citations": paper.get("citationCount", 0),
                "url": paper.get("url", "")
            })
        
        return {
            "status": "success",
            "papers": formatted_papers,
            "total": result.get("total", 0),
            "query": query
        }
    
    return result


async def execute_python_code_mcp(code: str, timeout: int = 30) -> dict:
    """Execute Python code in sandbox via MCP.
    
    Args:
        code: Python code to execute
        timeout: Execution timeout in seconds
        
    Returns:
        Execution result
    """
    client = await get_mcp_client()
    
    result = await client.call_tool(
        "python_executor",
        "execute_code",
        {"code": code, "timeout": timeout}
    )
    
    if result.get("status") == "success":
        return {
            "status": "success",
            "output": result.get("stdout", ""),
            "errors": result.get("stderr", ""),
            "exit_code": result.get("returncode", 0)
        }
    
    return result


async def install_python_package_mcp(package: str) -> dict:
    """Install Python package via MCP.
    
    Args:
        package: Package name
        
    Returns:
        Installation result
    """
    client = await get_mcp_client()
    
    result = await client.call_tool(
        "python_executor",
        "install_package",
        {"package": package}
    )
    
    return result


# Synchronous wrappers for Google ADK (which expects sync functions)
def search_papers_sync(query: str, limit: int = 10) -> dict:
    """Synchronous wrapper for search_papers_mcp.
    
    Args:
        query: Search query
        limit: Maximum number of results
        
    Returns:
        Search results
    """
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(search_papers_mcp(query, limit))


def execute_python_code_sync(code: str, timeout: int = 30) -> dict:
    """Synchronous wrapper for execute_python_code_mcp.
    
    Args:
        code: Python code to execute
        timeout: Execution timeout
        
    Returns:
        Execution result
    """
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(execute_python_code_mcp(code, timeout))
