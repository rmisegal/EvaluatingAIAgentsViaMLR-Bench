"""Unit tests for data models."""

import pytest
from mlr_bench.models.task import Task, TaskCategory
from mlr_bench.models.idea import ResearchIdea
from mlr_bench.models.paper import ResearchPaper
from mlr_bench.models.evaluation import EvaluationResult, AggregatedEvaluation


def test_task_creation():
    """Test Task model creation."""
    task = Task(
        task_id="test_001",
        title="Test Task",
        category=TaskCategory.TRUSTWORTHY_AI,
        description="Test description"
    )
    
    assert task.task_id == "test_001"
    assert task.title == "Test Task"
    assert task.category == TaskCategory.TRUSTWORTHY_AI


def test_research_idea_creation():
    """Test ResearchIdea model creation."""
    idea = ResearchIdea(
        task_id="test_001",
        title="Test Idea",
        motivation="Test motivation",
        main_idea="Test main idea",
        model_name="gemini-2.0-flash"
    )
    
    assert idea.task_id == "test_001"
    assert idea.title == "Test Idea"
    assert idea.model_name == "gemini-2.0-flash"


def test_research_paper_to_markdown():
    """Test ResearchPaper markdown conversion."""
    paper = ResearchPaper(
        task_id="test_001",
        title="Test Paper",
        abstract="Test abstract",
        introduction="Test intro",
        related_work="Test related work",
        methodology="Test methodology",
        experiments="Test experiments",
        results="Test results",
        discussion="Test discussion",
        conclusion="Test conclusion",
        references="Test references",
        model_name="gemini-2.0-flash"
    )
    
    markdown = paper.to_markdown()
    assert "# Test Paper" in markdown
    assert "## Abstract" in markdown
    assert "Test abstract" in markdown


def test_evaluation_result_scores():
    """Test EvaluationResult score validation."""
    result = EvaluationResult(
        evaluator_name="test_judge",
        overall_score=7.5,
        consistency_score=8.0,
        clarity_score=7.0,
        feedback="Test feedback"
    )
    
    assert result.overall_score == 7.5
    assert result.consistency_score == 8.0
    assert 0 <= result.overall_score <= 10


def test_aggregated_evaluation():
    """Test AggregatedEvaluation."""
    eval1 = EvaluationResult(
        evaluator_name="judge_1",
        overall_score=7.0,
        feedback="Good"
    )
    eval2 = EvaluationResult(
        evaluator_name="judge_2",
        overall_score=8.0,
        feedback="Very good"
    )
    
    aggregated = AggregatedEvaluation(
        task_id="test_001",
        stage="idea",
        evaluations=[eval1, eval2],
        average_score=7.5,
        score_breakdown={}
    )
    
    assert aggregated.average_score == 7.5
    assert len(aggregated.evaluations) == 2
