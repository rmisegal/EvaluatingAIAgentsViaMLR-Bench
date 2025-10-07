"""Unit tests for TaskManager."""

import pytest
import json
from pathlib import Path

from mlr_bench.tasks.task_manager import TaskManager
from mlr_bench.models.task import Task, TaskCategory


def test_task_manager_load_tasks(tmp_path, sample_tasks):
    """Test loading tasks from JSON file."""
    # Create tasks file
    tasks_file = tmp_path / "tasks.json"
    tasks_data = [task.model_dump() for task in sample_tasks]
    
    with open(tasks_file, 'w') as f:
        json.dump(tasks_data, f)
    
    # Load tasks
    manager = TaskManager(tasks_file)
    
    assert len(manager.tasks) == len(sample_tasks)
    assert manager.get_task("test_task_001") is not None


def test_task_manager_get_task(tmp_path, sample_tasks):
    """Test getting specific task."""
    tasks_file = tmp_path / "tasks.json"
    tasks_data = [task.model_dump() for task in sample_tasks]
    
    with open(tasks_file, 'w') as f:
        json.dump(tasks_data, f)
    
    manager = TaskManager(tasks_file)
    task = manager.get_task("test_task_001")
    
    assert task is not None
    assert task.task_id == "test_task_001"


def test_task_manager_get_all_tasks(tmp_path, sample_tasks):
    """Test getting all tasks."""
    tasks_file = tmp_path / "tasks.json"
    tasks_data = [task.model_dump() for task in sample_tasks]
    
    with open(tasks_file, 'w') as f:
        json.dump(tasks_data, f)
    
    manager = TaskManager(tasks_file)
    all_tasks = manager.get_all_tasks()
    
    assert len(all_tasks) == len(sample_tasks)


def test_task_manager_nonexistent_file(tmp_path):
    """Test loading from nonexistent file."""
    tasks_file = tmp_path / "nonexistent.json"
    manager = TaskManager(tasks_file)
    
    assert len(manager.tasks) == 0
