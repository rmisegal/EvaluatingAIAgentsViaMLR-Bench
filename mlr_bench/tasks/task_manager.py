"""Task manager for loading and managing research tasks."""

import json
from pathlib import Path
from typing import List, Optional, Dict
from loguru import logger

from mlr_bench.models.task import Task, TaskCategory


class TaskManager:
    """Manager for 201 research tasks."""
    
    def __init__(self, tasks_file: Path):
        """Initialize task manager.
        
        Args:
            tasks_file: Path to tasks JSON file
        """
        self.tasks_file = Path(tasks_file)
        self.tasks: Dict[str, Task] = {}
        self._load_tasks()
    
    def _load_tasks(self) -> None:
        """Load tasks from JSON file."""
        if not self.tasks_file.exists():
            logger.warning(f"Tasks file not found: {self.tasks_file}")
            return
        
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
            
            for task_data in tasks_data:
                task = Task(**task_data)
                self.tasks[task.task_id] = task
            
            logger.info(f"Loaded {len(self.tasks)} tasks from {self.tasks_file}")
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            raise
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task object or None if not found
        """
        return self.tasks.get(task_id)
    
    def get_tasks_by_category(self, category: TaskCategory) -> List[Task]:
        """Get all tasks in a category.
        
        Args:
            category: Task category
            
        Returns:
            List of tasks in the category
        """
        return [
            task for task in self.tasks.values()
            if task.category == category
        ]
    
    def get_tasks_by_conference(self, conference: str) -> List[Task]:
        """Get all tasks from a conference.
        
        Args:
            conference: Conference name (ICLR, NeurIPS, etc.)
            
        Returns:
            List of tasks from the conference
        """
        return [
            task for task in self.tasks.values()
            if task.conference and task.conference.upper() == conference.upper()
        ]
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.
        
        Returns:
            List of all tasks
        """
        return list(self.tasks.values())
