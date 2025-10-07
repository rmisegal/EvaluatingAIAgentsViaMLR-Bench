"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path

from mlr_bench.config.config import Config
from mlr_bench.models.task import Task, TaskCategory


@pytest.fixture
def test_config(tmp_path):
    """Create test configuration."""
    config = Config(
        model_name="gemini-2.0-flash",
        temperature=0.7,
        data_dir=tmp_path / "data",
        results_dir=tmp_path / "results",
        workspaces_dir=tmp_path / "workspaces",
        log_file=tmp_path / "logs" / "test.log"
    )
    config.ensure_directories()
    return config


@pytest.fixture
def sample_task():
    """Create sample task for testing."""
    return Task(
        task_id="test_task_001",
        title="Test Research Task",
        category=TaskCategory.TRUSTWORTHY_AI,
        description="This is a test task for unit testing",
        workshop_name="Test Workshop",
        conference="ICLR",
        year=2025,
        topics=["testing", "validation"]
    )


@pytest.fixture
def sample_tasks():
    """Create multiple sample tasks."""
    return [
        Task(
            task_id=f"test_task_{i:03d}",
            title=f"Test Task {i}",
            category=TaskCategory.TRUSTWORTHY_AI,
            description=f"Test task {i} description",
            conference="ICLR",
            year=2025,
            topics=["test"]
        )
        for i in range(1, 4)
    ]
