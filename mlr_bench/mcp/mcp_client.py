"""MCP Client for connecting to external tools."""

import asyncio
from typing import List, Dict, Any, Optional
from loguru import logger


class MCPClient:
    """Client for Model Context Protocol (MCP) servers."""
    
    def __init__(self):
        """Initialize MCP client."""
        self.connected_servers = {}
        logger.info("MCP Client initialized")
    
    async def connect_server(self, server_name: str, server_config: Dict[str, Any]):
        """Connect to an MCP server.
        
        Args:
            server_name: Name of the server
            server_config: Server configuration
        """
        logger.info(f"Connecting to MCP server: {server_name}")
        
        # Store server configuration
        self.connected_servers[server_name] = {
            "config": server_config,
            "status": "connected"
        }
        
        logger.info(f"Successfully connected to {server_name}")
    
    async def disconnect_server(self, server_name: str):
        """Disconnect from an MCP server.
        
        Args:
            server_name: Name of the server
        """
        if server_name in self.connected_servers:
            del self.connected_servers[server_name]
            logger.info(f"Disconnected from {server_name}")
    
    async def list_tools(self, server_name: str) -> List[str]:
        """List available tools from a server.
        
        Args:
            server_name: Name of the server
            
        Returns:
            List of tool names
        """
        if server_name not in self.connected_servers:
            logger.warning(f"Server {server_name} not connected")
            return []
        
        # Return available tools based on server type
        if server_name == "semantic_scholar":
            return ["search_papers", "get_paper_details", "get_citations"]
        elif server_name == "python_executor":
            return ["execute_code", "install_package", "list_files"]
        
        return []
    
    async def call_tool(
        self, 
        server_name: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call a tool on an MCP server.
        
        Args:
            server_name: Name of the server
            tool_name: Name of the tool
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        if server_name not in self.connected_servers:
            return {
                "status": "error",
                "error": f"Server {server_name} not connected"
            }
        
        logger.info(f"Calling {tool_name} on {server_name}")
        
        # Route to appropriate handler
        if server_name == "semantic_scholar":
            return await self._call_semantic_scholar(tool_name, arguments)
        elif server_name == "python_executor":
            return await self._call_python_executor(tool_name, arguments)
        
        return {
            "status": "error",
            "error": f"Unknown server: {server_name}"
        }
    
    async def _call_semantic_scholar(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call Semantic Scholar API.
        
        Args:
            tool_name: Tool name
            arguments: Tool arguments
            
        Returns:
            API response
        """
        # Import here to avoid dependency issues
        try:
            import aiohttp
        except ImportError:
            return {
                "status": "error",
                "error": "aiohttp not installed. Run: pip install aiohttp"
            }
        
        if tool_name == "search_papers":
            query = arguments.get("query", "")
            limit = arguments.get("limit", 10)
            
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": limit,
                "fields": "title,authors,year,abstract,citationCount,url"
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            return {
                                "status": "success",
                                "data": data.get("data", []),
                                "total": data.get("total", 0)
                            }
                        else:
                            return {
                                "status": "error",
                                "error": f"API returned status {response.status}"
                            }
            except Exception as e:
                logger.error(f"Semantic Scholar API error: {e}")
                return {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "status": "error",
            "error": f"Unknown tool: {tool_name}"
        }
    
    async def _call_python_executor(
        self, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute Python code in sandbox.
        
        Args:
            tool_name: Tool name
            arguments: Tool arguments
            
        Returns:
            Execution result
        """
        if tool_name == "execute_code":
            code = arguments.get("code", "")
            timeout = arguments.get("timeout", 30)
            
            try:
                # Create temporary file
                import tempfile
                import subprocess
                
                with tempfile.NamedTemporaryFile(
                    mode='w', 
                    suffix='.py', 
                    delete=False
                ) as f:
                    f.write(code)
                    temp_file = f.name
                
                # Execute code
                result = subprocess.run(
                    ["python3", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                # Clean up
                import os
                os.unlink(temp_file)
                
                return {
                    "status": "success",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
                
            except subprocess.TimeoutExpired:
                return {
                    "status": "error",
                    "error": f"Execution timeout after {timeout}s"
                }
            except Exception as e:
                logger.error(f"Code execution error: {e}")
                return {
                    "status": "error",
                    "error": str(e)
                }
        
        elif tool_name == "install_package":
            package = arguments.get("package", "")
            
            try:
                import subprocess
                
                result = subprocess.run(
                    ["pip3", "install", package],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "status": "error",
            "error": f"Unknown tool: {tool_name}"
        }
