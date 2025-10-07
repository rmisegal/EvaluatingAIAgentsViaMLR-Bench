"""Integration tests for the full pipeline."""

import pytest
from pathlib import Path

from mlr_bench.agent.mlr_agent import MLRAgent
from mlr_bench.judge.mlr_judge import MLRJudge
from mlr_bench.models.task import Task, TaskCategory


@pytest.mark.asyncio
async def test_idea_generation(test_config, sample_task):
    """Test idea generation stage."""
    agent = MLRAgent(test_config)
    
    idea = await agent.generate_idea(sample_task)
    
    assert idea is not None
    assert idea.task_id == sample_task.task_id
    assert len(idea.title) > 0
    assert len(idea.main_idea) > 0


@pytest.mark.asyncio
async def test_literature_review(test_config, sample_task):
    """Test literature review stage."""
    agent = MLRAgent(test_config)
    
    # Generate idea first
    idea = await agent.generate_idea(sample_task)
    
    # Review literature
    literature = await agent.review_literature(idea, sample_task)
    
    assert literature is not None
    assert literature.task_id == sample_task.task_id
    assert len(literature.key_findings) > 0


@pytest.mark.asyncio
async def test_proposal_generation(test_config, sample_task):
    """Test proposal generation stage."""
    agent = MLRAgent(test_config)
    
    # Generate idea and literature review
    idea = await agent.generate_idea(sample_task)
    literature = await agent.review_literature(idea, sample_task)
    
    # Generate proposal
    proposal = await agent.generate_proposal(sample_task, idea, literature)
    
    assert proposal is not None
    assert proposal.task_id == sample_task.task_id
    assert len(proposal.abstract) > 0
    assert len(proposal.methodology) > 0


@pytest.mark.asyncio
async def test_idea_evaluation(test_config, sample_task):
    """Test idea evaluation."""
    agent = MLRAgent(test_config)
    judge = MLRJudge(test_config)
    
    # Generate idea
    idea = await agent.generate_idea(sample_task)
    
    # Evaluate
    evaluation = await judge.evaluate_idea(idea, sample_task)
    
    assert evaluation is not None
    assert 0 <= evaluation.average_score <= 10
    assert len(evaluation.evaluations) > 0


@pytest.mark.asyncio
@pytest.mark.slow
async def test_full_pipeline(test_config, sample_task):
    """Test complete pipeline (slow test)."""
    agent = MLRAgent(test_config)
    
    # Run full pipeline
    paper = await agent.run_full_pipeline(sample_task)
    
    assert paper is not None
    assert paper.task_id == sample_task.task_id
    assert len(paper.title) > 0
    assert len(paper.abstract) > 0
    
    # Check that results were saved
    results_dir = test_config.results_dir / sample_task.task_id
    assert results_dir.exists()
    assert (results_dir / "idea.json").exists()
    assert (results_dir / "paper.json").exists()
    assert (results_dir / "paper.md").exists()
