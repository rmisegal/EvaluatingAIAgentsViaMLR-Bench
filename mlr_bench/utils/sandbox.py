"""Sandbox manager for isolated experiment execution."""

import shutil
import platform
from pathlib import Path
from typing import Optional
from loguru import logger


class SandboxManager:
    """Manager for isolated workspaces."""
    
    def __init__(self, base_dir: Path):
        """Initialize sandbox manager.
        
        Args:
            base_dir: Base directory for workspaces
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_workspace(self, task_id: str) -> Path:
        """Create isolated workspace for a task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Path to workspace
        """
        workspace = self.base_dir / task_id
        workspace.mkdir(parents=True, exist_ok=True)
        
        # Set permissions (Linux/macOS only)
        if platform.system() != "Windows":
            import os
            os.chmod(workspace, 0o700)
        
        logger.info(f"Created workspace: {workspace}")
        return workspace
    
    async def cleanup_workspace(self, workspace: Path) -> None:
        """Clean up workspace.
        
        Args:
            workspace: Path to workspace
        """
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)
            logger.info(f"Cleaned up workspace: {workspace}")
    
    def get_workspace(self, task_id: str) -> Optional[Path]:
        """Get existing workspace path.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Path to workspace if exists, None otherwise
        """
        workspace = self.base_dir / task_id
        return workspace if workspace.exists() else None
