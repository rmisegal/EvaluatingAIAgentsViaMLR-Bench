"""File utilities for MLR-Bench."""

import json
import aiofiles
from pathlib import Path
from typing import Any, Dict
from loguru import logger


async def save_json(data: Dict[str, Any], file_path: Path) -> None:
    """Save data to JSON file asynchronously.
    
    Args:
        data: Data to save
        file_path: Path to save file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, indent=2, ensure_ascii=False))
    
    logger.debug(f"Saved JSON to {file_path}")


async def load_json(file_path: Path) -> Dict[str, Any]:
    """Load data from JSON file asynchronously.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded data
    """
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
        content = await f.read()
        return json.loads(content)


async def save_text(text: str, file_path: Path) -> None:
    """Save text to file asynchronously.
    
    Args:
        text: Text to save
        file_path: Path to save file
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(text)
    
    logger.debug(f"Saved text to {file_path}")


async def load_text(file_path: Path) -> str:
    """Load text from file asynchronously.
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content
    """
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
        return await f.read()
